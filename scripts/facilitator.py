#!/usr/bin/env python3
"""Local scheduling ledger, not an agent runtime or an exact token meter."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
from datetime import datetime, timezone

MODES = {
    'quick': dict(seats=3, budget=8000, cycles=1, debates=0),
    'standard': dict(seats=6, budget=25000, cycles=1, debates=1),
    'deep': dict(seats=12, budget=60000, cycles=2, debates=2),
}


def now():
    return datetime.now(timezone.utc).isoformat()


def estimate(text):
    # Byte heuristic deliberately errs high on non-ASCII; hidden reasoning unknown.
    return math.ceil(len(text.encode('utf-8')) / 4)


def atomic(path, data):
    path = Path(path)
    fd, name = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Artifact must be inside the run directory')
    return path


def schedule(mode, roster):
    tasks = []
    def add(key, phase, output, cap, optional=False):
        tasks.append(dict(id=key, phase=phase, output=output, cap=cap,
                          optional=optional, status='pending', attempts=0))
    add('research', 'research', 'RESEARCH.md', 4000 if mode == 'quick' else 9000)
    for seat in roster:
        add('assess-' + seat['id'], 'assessment', 'assessments/' + seat['id'] + '.md',
            1800 if mode == 'quick' else 3000)
    add('agenda', 'agenda', 'DISCUSSION.md', 1800 if mode == 'quick' else 4000)
    for cycle in range(1, MODES[mode]['cycles'] + 1):
        for debate in range(MODES[mode]['debates']):
            add(f'debate-{cycle}-{debate+1}', f'debate-{cycle}',
                f'debates/{cycle}-{debate+1}.md', 4000, True)
        add(f'revise-{cycle}', f'revision-{cycle}', f'REVISION-{cycle}.md',
            3200 if mode == 'quick' else 6500, cycle > 1)
        if mode != 'quick':
            for seat in roster:
                add(f'validate-{cycle}-' + seat['id'], f'validation-{cycle}',
                    f'reviews/{cycle}-' + seat['id'] + '.md', 1400, cycle > 1)
    add('final', 'synthesis', 'FIXED_IDEA.md', {'quick': 6500, 'standard': 14000, 'deep': 22000}[mode])
    return tasks


def validate(s, initializing=False):
    if not isinstance(s, dict) or s.get('schema') != 2 or s.get('mode') not in MODES:
        raise ValueError('Unsupported or incomplete checkpoint')
    roster = s['roster']
    if not isinstance(roster, list) or len(roster) != MODES[s['mode']]['seats']:
        raise ValueError('Wrong roster size')
    for i, seat in enumerate(roster, 1):
        if not isinstance(seat, dict) or seat.get('id') != f'S{i:02}' or any(
                not isinstance(seat.get(k), str) or not seat[k].strip()
                for k in ('role', 'reason', 'remit')):
            raise ValueError('Invalid roster')
    if len({x['role'].casefold() for x in roster}) != len(roster):
        raise ValueError('Duplicate role')
    expected = schedule(s['mode'], roster)
    if not isinstance(s['tasks'], list) or len(expected) != len(s['tasks']):
        raise ValueError('Incomplete task schedule')
    for a, b in zip(expected, s['tasks']):
        if not isinstance(b, dict) or any(a[k] != b.get(k) for k in ('id', 'phase', 'output', 'cap', 'optional')):
            raise ValueError('Invalid task schedule')
        if b.get('status') not in ('pending', 'running', 'done', 'failed', 'skipped') or type(b.get('attempts')) is not int or not 0 <= b['attempts'] <= 2:
            raise ValueError('Invalid task state')
        if b['status'] == 'done' and (not isinstance(b.get('sha256'), str) or len(b['sha256']) != 64):
            raise ValueError('Missing artifact checksum')
        if b['status'] == 'running' and (b['attempts'] < 1 or any(
                type(b.get(k)) is not int or b[k] < 0 for k in ('reserved', 'input_estimate'))):
            raise ValueError('Invalid running reservation')
    for k in ('budget', 'reserve', 'used'):
        if type(s[k]) is not int or s[k] < 0:
            raise ValueError('Invalid accounting')
    if not 0 < s['reserve'] < s['budget']:
        raise ValueError('Invalid synthesis reserve')
    if sum(t['status'] == 'running' for t in s['tasks']) > 1:
        raise ValueError('Only one ledger task may run at a time')
    for k in ('events', 'inputs', 'usage'):
        if not isinstance(s[k], list):
            raise ValueError('Incomplete checkpoint')
    for entry in s['inputs']:
        if not isinstance(entry, dict) or not isinstance(entry.get('output'), str) or not isinstance(entry.get('sha256'), str) or len(entry['sha256']) != 64:
            raise ValueError('Invalid input record')
    if not initializing and (len(s['inputs']) != 2 or {x['output'] for x in s['inputs']} != {'BRIEF.md', 'ROSTER.md'}):
        raise ValueError('Incomplete input manifest')
    return s


def load(root):
    # Recover state, never reinitialize a run implicitly.
    errors = []
    for name in ('state.json', 'state.backup.json'):
        try:
            s = validate(json.loads((root / name).read_text()))
            if errors:
                s['events'].append(dict(time=now(), error='Recovered backup: ' + '; '.join(errors)))
            return s
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f'{name}: {exc}')
    raise ValueError('No valid checkpoint. Preserve files and reconstruct manually: ' + '; '.join(errors))


def invalid(root, s):
    bad = []
    for entry in s['inputs'] + [t for t in s['tasks'] if t['status'] == 'done']:
        p = artifact(root, entry['output'])
        if not p.is_file() or digest(p) != entry['sha256']:
            bad.append(entry['output'])
    return bad


def next_task(s):
    return next((t for t in s['tasks'] if t['status'] in ('pending', 'running')), None)


def status(root, s):
    t = next_task(s)
    bad = invalid(root, s)
    if not t and s['tasks'][-1]['status'] == 'done' and s.get('stop_reason'):
        step = 'deliver partial report with recorded gaps' if bad else 'deliver report with recorded omissions'
    elif bad and not (t and t['id'] == 'final' and s.get('stop_reason')):
        step = 'repair artifacts: ' + ', '.join(bad)
    elif t:
        step = ('reconcile running ' if t['status'] == 'running' else 'authorize ') + t['id']
    else:
        step = 'deliver report' if s['tasks'][-1]['status'] == 'done' else 'report final synthesis failure and preserved work'
    lines = ['# Meeting status', '', f"Mode: {s['mode']}",
             f"Current phase: {t['phase'] if t else ('complete' if s['tasks'][-1]['status'] == 'done' else 'incomplete; final task failed')}",
             f"Estimated/accounted tokens: {s['used']} (not an exact run total)",
             f"Budget target: {s['budget']}; remaining estimate: {s['budget']-s['used']}",
             f"Reserved for synthesis: {s['reserve']}",
             f"Stop reason: {s.get('stop_reason', 'none')}",
             f"Next executable step: {step}",
             '', '## Tasks / completed and pending specialists', '']
    lines += [f"- {x['id']}: {x['status']} (attempts {x['attempts']})" for x in s['tasks']]
    lines += ['', '## Generated and input files', '']
    lines += [f"- {x['output']}" for x in s['inputs'] + [x for x in s['tasks'] if x['status'] == 'done']]
    lines += ['', '## Errors, interruptions, decisions and usage', '']
    lines += ['- ' + json.dumps(x, ensure_ascii=False) for x in s['events'] + s['usage']]
    return '\n'.join(lines) + '\n'


def save(root, s):
    validate(s)
    current = root / 'state.json'
    if current.exists():
        try:
            validate(json.loads(current.read_text()))
            atomic(root / 'state.backup.json', current.read_text())
        except (ValueError, KeyError, TypeError):
            pass  # Never replace a valid backup with corrupt state.
    atomic(current, json.dumps(s, indent=2) + '\n')
    atomic(root / 'STATUS.md', status(root, s))  # Derived; regenerate after a crash.


def init(root, mode, budget, reserve, brief, roster):
    if root.exists():
        raise ValueError('Run exists; use resume, never overwrite')
    cfg = MODES[mode]
    if not isinstance(roster, list) or len(roster) != cfg['seats']:
        raise ValueError(f"{mode} requires exactly {cfg['seats']} seats")
    for i, seat in enumerate(roster, 1):
        if not isinstance(seat, dict) or seat.get('id') != f'S{i:02}' or any(not isinstance(seat.get(k), str) or not seat[k].strip() for k in ('role', 'reason', 'remit')):
            raise ValueError('Roster needs sequential IDs and nonempty role, reason, remit')
    if len({x['role'].casefold() for x in roster}) != len(roster):
        raise ValueError('Duplicate specialist role')
    if not brief.strip():
        raise ValueError('Brief is empty')
    budget = cfg['budget'] if budget is None else budget
    reserve = max(1, math.ceil(budget * .2)) if reserve is None else reserve
    s = dict(schema=2, mode=mode, budget=budget, reserve=reserve, used=0,
             roster=roster, tasks=schedule(mode, roster), inputs=[], events=[], usage=[], created=now())
    validate(s, initializing=True)
    root.mkdir(parents=True)
    for directory in ('assessments', 'debates', 'reviews'):
        (root / directory).mkdir()
    atomic(root / 'BRIEF.md', brief)
    atomic(root / 'ROSTER.md', '# Specialist roster\n\n' + '\n'.join(
        f"- {x['id']} — {x['role']}: {x['reason']} Remit: {x['remit']}" for x in roster) + '\n')
    s['inputs'] = [dict(output=p, sha256=digest(root / p)) for p in ('BRIEF.md', 'ROSTER.md')]
    save(root, s)
    return s


def stop(s, reason):
    if any(t['status'] == 'running' for t in s['tasks']):
        raise ValueError('Finish or fail the running task before stopping')
    s['stop_reason'] = reason
    for t in s['tasks']:
        if t['status'] == 'pending' and t['id'] != 'final':
            t['status'] = 'skipped'
    s['events'].append(dict(time=now(), stop=reason))


def start(root, s, input_tokens, output_tokens):
    t = next_task(s)
    if invalid(root, s) and (not t or t['id'] != 'final' or not s.get('stop_reason')):
        raise ValueError('Invalid artifacts; repair before new work, or stop for a partial report')
    if not t or t['status'] == 'running':
        raise ValueError('No pending task or a task is already running')
    if input_tokens < 0 or output_tokens <= 0:
        raise ValueError('Supply nonnegative input and positive output estimates')
    if t['id'] != 'final' and any(x['status'] == 'failed' and (x['id'] in ('research', 'agenda') or x['id'].startswith('revise-')) for x in s['tasks']):
        stop(s, 'Required research, agenda, or revision failed; synthesize with explicit gaps')
        return False
    if t['id'].startswith('validate-'):
        cycle = t['id'].split('-')[1]
        revision = next(x for x in s['tasks'] if x['id'] == 'revise-' + cycle)
        if revision['status'] != 'done':
            stop(s, 'Revision cycle omitted; dependent validation skipped')
            return False
    cost = input_tokens + output_tokens
    if t['id'] != 'final' and s['used'] + cost + s['reserve'] > s['budget']:
        stop(s, 'Estimated budget exhausted; preserve work and synthesize')
        return False
    t.update(status='running', attempts=t['attempts'] + 1, reserved=cost, input_estimate=input_tokens, started=now())
    s['used'] += cost  # Charge admission immediately, including interrupted work.
    s['usage'].append(dict(task=t['id'], attempt=t['attempts'], tokens=cost, basis='reservation estimate'))
    return True


def finish(root, s, actual=None, basis='text estimate', failed=None):
    t = next_task(s)
    if not t or t['status'] != 'running':
        raise ValueError('No running task')
    if actual is not None and actual < 0:
        raise ValueError('Usage cannot be negative')
    if not failed:
        p = artifact(root, t['output'])
        content = p.read_text()
        if not content.strip() or len(content) > t['cap']:
            raise ValueError(f"Empty or over-cap artifact ({t['cap']} characters); fix or fail task")
    if actual is not None:
        # Never refund uncertain reservations; avoid undercount on repeated contexts.
        s['used'] += max(0, actual - t['reserved'])
        s['usage'].append(dict(task=t['id'], tokens=actual, basis=basis,
                               note='Reservation retained if higher; do not add records as totals'))
    if failed:
        t['status'] = 'pending' if t['attempts'] < 2 else 'failed'
        s['events'].append(dict(time=now(), task=t['id'], error=failed))
        return
    # Semantic review belongs to the facilitator before invoking finish.
    s['used'] += max(0, t['input_estimate'] + estimate(content) - t['reserved']) if actual is None else 0
    t.update(status='done', sha256=digest(p), completed=now())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('init')
    p.add_argument('--mode', choices=MODES, default='standard')
    p.add_argument('--budget', type=int)
    p.add_argument('--reserve', type=int)
    p.add_argument('--brief', type=Path, required=True)
    p.add_argument('--roster', type=Path, required=True)
    p = sub.add_parser('resume')
    p.add_argument('--verbose', action='store_true')
    p = sub.add_parser('start')
    p.add_argument('--input-tokens', type=int, required=True)
    p.add_argument('--output-tokens', type=int, required=True)
    for name in ('finish', 'fail'):
        p = sub.add_parser(name)
        p.add_argument('--tokens', type=int)
        p.add_argument('--basis', choices=('text estimate', 'runtime metadata'), default='text estimate')
        if name == 'fail':
            p.add_argument('--reason', required=True)
    p = sub.add_parser('skip')
    p.add_argument('--reason', required=True)
    p = sub.add_parser('stop')
    p.add_argument('--reason', required=True)
    p = sub.add_parser('charge')
    p.add_argument('--tokens', type=int, required=True)
    p.add_argument('--reason', required=True)
    args = parser.parse_args()
    root = args.run.resolve()
    try:
        if args.command == 'init':
            s = init(root, args.mode, args.budget, args.reserve, args.brief.read_text(), json.loads(args.roster.read_text()))
        else:
            s = load(root)
            if args.command == 'start':
                start(root, s, args.input_tokens, args.output_tokens)
            elif args.command in ('finish', 'fail'):
                finish(root, s, args.tokens, args.basis, getattr(args, 'reason', None))
            elif args.command == 'skip':
                t = next_task(s)
                if not t or t['status'] != 'pending' or not t['optional']:
                    raise ValueError('Only a pending optional task can be skipped')
                t['status'] = 'skipped'
                s['events'].append(dict(time=now(), task=t['id'], skipped=args.reason))
            elif args.command == 'stop':
                stop(s, args.reason)
            elif args.command == 'charge':
                if args.tokens <= 0:
                    raise ValueError('Charge must be positive')
                s['used'] += args.tokens
                s['usage'].append(dict(tokens=args.tokens, basis='additional estimate', reason=args.reason))
            if args.command == 'resume':
                bad = invalid(root, s)
                if bad:
                    s['events'].append(dict(time=now(), error='Invalid artifacts: ' + ', '.join(bad)))
            save(root, s)
        if getattr(args, 'verbose', False):
            print(status(root, s))
        else:
            t = next_task(s)
            print(json.dumps(dict(mode=s['mode'], next=t, used_estimate=s['used'],
                                  remaining_estimate=s['budget']-s['used'],
                                  stop_reason=s.get('stop_reason'), invalid_artifacts=invalid(root, s),
                                  last_event=s['events'][-1] if s['events'] else None,
                                  status_file=str(root / 'STATUS.md')), ensure_ascii=False))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
