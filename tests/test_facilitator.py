import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('facilitator', Path(__file__).parents[1] / 'scripts/facilitator.py')
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'run'

    def init(self, mode='standard', budget=100000):
        roster = [dict(id=f'S{i:02}', role=f'Specialist {i}', reason='Domain risk', remit=f'Risk {i}')
                  for i in range(1, f.MODES[mode]['seats'] + 1)]
        return f.init(self.root, mode, budget, None, 'An actual idea with constraints.', roster)

    def complete(self, s, text='Substantive output inspected by the facilitator.'):
        t = f.next_task(s)
        self.assertTrue(f.start(self.root, s, 20, 100))
        (self.root / t['output']).write_text(text)
        f.finish(self.root, s)
        f.save(self.root, s)

    def test_all_modes_complete_and_counts(self):
        for mode, seats, reviews in [('quick', 3, 0), ('standard', 6, 6), ('deep', 12, 24)]:
            with self.subTest(mode=mode):
                self.root = Path(self.tmp.name) / mode
                s = self.init(mode)
                while f.next_task(s):
                    self.complete(s)
                self.assertEqual(sum(t['phase'] == 'assessment' for t in s['tasks']), seats)
                self.assertEqual(sum(t['id'].startswith('validate') for t in s['tasks']), reviews)
                self.assertEqual(s['tasks'][-1]['status'], 'done')
                self.assertFalse(f.invalid(self.root, f.load(self.root)))

    def test_budget_stops_before_reserve_and_allows_final(self):
        s = self.init('quick', 100)
        self.assertFalse(f.start(self.root, s, 70, 20))
        self.assertEqual(f.next_task(s)['id'], 'final')
        self.complete(s)
        self.assertGreater(s['used'], s['budget'])  # Soft target, honest overrun.

    def test_resume_finished_specialist_not_rerun(self):
        s = self.init('quick')
        self.complete(s)
        self.complete(s)
        loaded = f.load(self.root)
        self.assertEqual(f.next_task(loaded)['id'], 'assess-S02')

    def test_interruption_adopts_output_without_second_call(self):
        s = self.init()
        f.start(self.root, s, 40, 60)
        f.save(self.root, s)
        (self.root / 'RESEARCH.md').write_text('No browsing; assumptions and verification plan.')
        s = f.load(self.root)
        with self.assertRaises(ValueError):
            f.start(self.root, s, 40, 60)
        f.finish(self.root, s)
        self.assertEqual(s['tasks'][0]['attempts'], 1)
        self.assertEqual(s['used'], 100)

    def test_failed_specialist_bounded_retry(self):
        s = self.init()
        self.complete(s)
        for attempt in range(2):
            f.start(self.root, s, 20, 100)
            f.finish(self.root, s, failed='Worker failed')
        self.assertEqual(s['tasks'][1]['status'], 'failed')
        self.assertEqual(f.next_task(s)['id'], 'assess-S02')
        self.assertEqual(s['used'], 360)

    def test_failed_research_prevents_unsupported_assessments(self):
        s = self.init()
        for _ in range(2):
            f.start(self.root, s, 20, 100)
            f.finish(self.root, s, failed='Research task failed')
        self.assertFalse(f.start(self.root, s, 20, 100))
        self.assertEqual(f.next_task(s)['id'], 'final')

    def test_missing_research_blocks_but_partial_report_possible(self):
        s = self.init()
        self.complete(s)
        (self.root / 'RESEARCH.md').unlink()
        with self.assertRaises(ValueError):
            f.start(self.root, s, 20, 100)
        f.stop(s, 'Missing research; exclude it from the report')
        self.complete(s)
        self.assertIn('RESEARCH.md', f.invalid(self.root, s))
        self.assertIn('Next executable step: deliver partial report with recorded gaps', f.status(self.root, s))

    def test_corrupt_checkpoint_falls_back_and_keeps_work(self):
        s = self.init()
        self.complete(s)
        f.save(self.root, s)  # backup includes completed research
        (self.root / 'state.json').write_text('{broken')
        recovered = f.load(self.root)
        self.assertEqual(f.next_task(recovered)['id'], 'assess-S01')
        self.assertIn('Recovered backup', recovered['events'][-1]['error'])
        f.save(self.root, recovered)
        self.assertEqual(f.load(self.root)['tasks'][0]['status'], 'done')

    def test_incomplete_checkpoints_rejected_without_restart(self):
        self.init()
        for name in ('state.json', 'state.backup.json'):
            (self.root / name).write_text(json.dumps({'schema': 2, 'mode': 'quick'}))
        with self.assertRaises(ValueError):
            f.load(self.root)
        self.assertTrue((self.root / 'BRIEF.md').exists())

    def test_modified_artifact_detected(self):
        s = self.init()
        self.complete(s)
        (self.root / 'RESEARCH.md').write_text('Changed evidence')
        self.assertEqual(f.invalid(self.root, s), ['RESEARCH.md'])

    def test_output_caps_and_accounting(self):
        s = self.init('quick')
        f.start(self.root, s, 50, 10)
        (self.root / 'RESEARCH.md').write_text('x' * 4001)
        with self.assertRaises(ValueError):
            f.finish(self.root, s)
        (self.root / 'RESEARCH.md').write_text('x' * 1000)
        f.finish(self.root, s)
        self.assertEqual(s['used'], 300)

    def test_initialization_never_overwrites(self):
        self.init()
        with self.assertRaises(ValueError):
            self.init()

    def test_no_path_escape(self):
        with self.assertRaises(ValueError):
            f.artifact(self.root, '../escape')

    def test_atomic_failure_preserves_previous_file(self):
        from unittest.mock import patch
        p = Path(self.tmp.name) / 'state'
        p.write_text('old')
        with patch.object(f.os, 'replace', side_effect=OSError('interrupted')):
            with self.assertRaises(OSError):
                f.atomic(p, 'new')
        self.assertEqual(p.read_text(), 'old')
        self.assertEqual(list(Path(self.tmp.name).iterdir()), [p])

    def test_failed_revision_stops_dependent_validation(self):
        s = self.init()
        while f.next_task(s)['id'] != 'revise-1':
            self.complete(s)
        for _ in range(2):
            f.start(self.root, s, 20, 100)
            f.finish(self.root, s, failed='Revision unavailable')
        self.assertFalse(f.start(self.root, s, 20, 100))
        self.assertEqual(f.next_task(s)['id'], 'final')
        self.assertTrue(all(t['status'] == 'skipped' for t in s['tasks'] if t['id'].startswith('validate')))

    def test_skipped_revision_does_not_authorize_validation(self):
        s = self.init('deep')
        while f.next_task(s)['id'] != 'revise-2':
            self.complete(s)
        f.next_task(s)['status'] = 'skipped'
        f.save(self.root, s)
        s = f.load(self.root)
        self.assertFalse(f.start(self.root, s, 20, 100))
        self.assertEqual(f.next_task(s)['id'], 'final')
        self.assertTrue(all(t['status'] == 'skipped' for t in s['tasks'] if t['id'].startswith('validate-2')))

    def test_wrong_json_type_recovers_backup(self):
        s = self.init()
        f.save(self.root, s)
        (self.root / 'state.json').write_text('[]')
        self.assertEqual(f.load(self.root)['mode'], 'standard')

    def test_missing_manifest_rejected(self):
        s = self.init()
        s['inputs'] = []
        with self.assertRaises(ValueError):
            f.validate(s)

    def test_final_failure_reports_incomplete(self):
        s = self.init()
        f.stop(s, 'Partial report needed')
        for _ in range(2):
            f.start(self.root, s, 20, 100)
            f.finish(self.root, s, failed='Synthesis unavailable')
        report = f.status(self.root, s)
        self.assertIn('report final synthesis failure', report)
        self.assertNotIn('Next executable step: deliver report', report)

    def test_invalid_output_does_not_recharge(self):
        s = self.init()
        f.start(self.root, s, 20, 100)
        (self.root / 'RESEARCH.md').write_text('')
        with self.assertRaises(ValueError):
            f.finish(self.root, s, actual=500)
        self.assertEqual(s['used'], 120)

    def test_defaults_and_invalid_rosters(self):
        for mode in f.MODES:
            self.root = Path(self.tmp.name) / mode
            s = self.init(mode, None)
            self.assertEqual(s['budget'], f.MODES[mode]['budget'])
            self.assertEqual(s['reserve'], s['budget'] // 5)
        self.root = Path(self.tmp.name) / 'invalid'
        with self.assertRaises(ValueError):
            f.init(self.root, 'quick', None, None, 'Idea', [None] * 3)
        self.assertFalse(self.root.exists())

    def test_cli_optional_skips_and_compact_output(self):
        import subprocess
        import sys
        s = self.init('deep')
        while f.next_task(s)['id'] != 'debate-1-1':
            self.complete(s)
        script = str(Path(f.__file__))
        def cli(*args):
            return subprocess.run([sys.executable, script, str(self.root), *args], capture_output=True, text=True)
        result = cli('skip', '--reason', 'No material disagreement')
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary['next']['id'], 'debate-1-2')
        self.assertLess(len(result.stdout), 1500)
        self.assertEqual(cli('skip', '--reason', 'No second issue').returncode, 0)
        self.assertEqual(cli('skip', '--reason', 'Cannot skip first revision').returncode, 2)
        self.assertEqual(cli('resume').returncode, 0)
        self.assertIn('# Meeting status', cli('resume', '--verbose').stdout)

    def test_estimate_explicitly_heuristic(self):
        self.assertEqual(f.estimate('abcd'), 1)
        self.assertGreater(f.estimate('漢字'), 1)


if __name__ == '__main__':
    unittest.main()
