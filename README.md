# Fix My Idea v2.0

A Codex skill that brings relevant AI specialist perspectives into a collaborative
working meeting: preserve what works, expose failure mechanisms, debate repairs,
and turn the improved idea into experiments and an executable plan.

v2 keeps the original philosophy and deliverables while making **STANDARD, with
six specialists, the default**. Shared research, targeted disagreement, bounded
revision, a synthesis reserve, and recoverable checkpoints reduce unnecessary
work. Lower real-world token usage is an objective to benchmark, not a measured
claim in this release.

## Install

Clone into the user skill directory (requires Git; ledger requires Python 3.9+):

```bash
git clone https://github.com/maywanel/fix-my-idea.git ~/.agents/skills/fix-my-idea
```

For an existing installation, update it through your normal Git workflow after
preserving local changes; do not clone over it. To test an uncommitted checkout,
copy its SKILL.md, agents/, references/, and scripts/ into a separate skill install
named `fix-my-idea` once ready. Installing the published repository before these
changes are merged will still install its published version.

The existing installer request remains usable:

```text
$skill-installer install the fix-my-idea skill from maywanel/fix-my-idea, using repository root (path .) and installation name fix-my-idea.
```

Existing Skills CLI users may retain `npx skills add maywanel/fix-my-idea -a codex`
(and `-g` for global installation); this optional third-party installer is not a
runtime dependency. See its [installation documentation](https://github.com/vercel-labs/skills#install-a-skill).
Keep the whole skill bundle, not only SKILL.md. If discovery does not refresh,
start a new Codex session. The folder/manifest conventions and `$skill-name`
invocation follow [official Codex skills documentation](https://developers.openai.com/codex/skills).

## Choose a mode

| Mode | Perspectives | Debate | Revision / validation | Suggested token target |
| --- | ---: | --- | --- | ---: |
| QUICK | 3 | None | One proposal, facilitator consistency check; at most one revision | 8,000 |
| STANDARD, default | 6 | One focused exchange | One revision, six final reviews | 25,000 |
| DEEP | 12 | Up to two issues per cycle | Up to two revisions with twelve reviews each | 60,000 |

Exactly the mode's number of perspectives is selected, with reasons and distinct
remits. Failures or budget stops can leave some unfinished; the report discloses
those gaps. The facilitator is not an additional specialist. QUICK is intended for
frequent brainstorming; STANDARD for serious projects; DEEP for major decisions.

Type these into the Codex prompt, **not your shell**:

```text
$fix-my-idea --mode quick "Evaluate my API security idea"
$fix-my-idea --mode standard "Improve Nemesis"
$fix-my-idea --mode deep "Evaluate my startup architecture"
$fix-my-idea --mode standard --budget 18000 "Improve my student meal service"
```

`--mode` and `--budget` are conventions interpreted by the skill's instructions,
not registered Codex CLI options or a guaranteed argument parser. Equivalent:

```text
Use $fix-my-idea in quick mode with an estimated 8,000-token budget for this idea: ...
Use $fix-my-idea in standard mode to improve Nemesis. Here is its brief: ...
Use $fix-my-idea in deep mode with a 60,000-token target for this architecture: ...
```

The original `$fix-my-idea <idea>` invocation works and now selects STANDARD.
Include users/buyers, market, resources, timeline, evidence, and non-negotiables.
A project name alone needs an identifiable brief in context; the skill must not
invent what Nemesis is.

## Execution architecture

1. The facilitator establishes the brief, chooses domain-specific roles, and
   initializes a unique `.fix-my-idea/<run-id>/` ledger.
2. Shared research records verified facts, competitors, constraints, observations,
   sources, assumptions and unknowns. All specialists reuse it.
3. Each perspective assesses the same neutral brief independently of peer opinions.
4. The facilitator ranks actual disagreements, selects relevant owner/challenger
   pairs, and authorizes bounded exchanges only when useful.
5. A consolidated revision is checked by the selected seats in STANDARD/DEEP.
   DEEP's second cycle is optional; remaining disagreement becomes a test or blocker.
6. A final synthesis connects each major problem to a repair, evidence/reasoning,
   cost, residual risk, and measurable next action.

[`scripts/facilitator.py`](scripts/facilitator.py) is a standard-library scheduling
and accounting helper, not an autonomous model runner. The facilitator makes
semantic choices; the script enforces task ordering, mode counts, attempts,
output character caps, and admission against estimates. Specialists cannot
spawn agents, authorize research, or extend rounds. One task runs at a time in
the portable ledger. Independent agents can be used sequentially when available;
otherwise the report explicitly labels single-model simulation. No Claude-specific
APIs, assumed nested-agent support, external service, or model API key is needed.

## Budget behavior

All budgets are configurable; the helper defaults to reserving 20% for final
synthesis. It accounts for estimates of setup, repeated input context, tool output,
facilitator work, and output—not just saved prose. Prefer scoped runtime metadata
when exposed; otherwise use an explicitly approximate UTF-8-bytes/4 heuristic.
Hidden reasoning, tokenizer differences, context reuse and unavailable telemetry
make estimates uncertain. Reservations are conservatively retained if higher than
later observations. These are not exact billed-token measurements.

Before every task, reserve input + output estimates. When the next task would
consume the synthesis reserve, the ledger stops admitting specialists and skips
pending work so a partial report can be produced. It preserves completed work and
records omissions. It cannot stop model generation at a hard token limit; even
synthesis may overrun the target. Actual hard caps require runtime enforcement.
Research calls and output sizes also have explicit protocol bounds. No unlimited
retry or recursive delegation is permitted.

See [facilitator commands and accounting](references/facilitator.md) for budget
and reserve overrides, input manifests, checkpoints, and manual fallback.

## Output and recovery

Each new run saves:

| Artifact | Purpose |
| --- | --- |
| `FIXED_IDEA.md` | Revised idea, repairs, feasibility, tradeoffs, validation, action plan and recommendation |
| `STATUS.md` | Mode, phase, completed/pending tasks, estimates, errors and next step |
| `BRIEF.md`, `ROSTER.md` | User objective and specialist selection rationale |
| `RESEARCH.md` | Shared evidence, citations, assumptions and query log |
| `DISCUSSION.md`, `debates/` | Ranked agenda and actual exchanges with claim IDs |
| `assessments/`, `REVISION-*.md`, `reviews/` | Contributions, proposals and advisory validation |
| `state.json`, `state.backup.json` | Authoritative machine checkpoint and previous valid state |

The final report has eleven sections: original idea, critical weaknesses, repairs,
revised concept, technical feasibility, commercial feasibility, tradeoffs/dissent,
assumptions, prioritized actions, success criteria, and final recommendation.
Pilot definition, economics, role assignments, dependency gates, and evidence
traceability from v1 remain part of the [plan template](references/plan-template.md).

Resume explicitly:

```text
Use $fix-my-idea to resume .fix-my-idea/<run-id>. Validate the checkpoints and continue without repeating completed specialists.
```

For inspection, from the installed skill:

```bash
python3 ~/.agents/skills/fix-my-idea/scripts/facilitator.py /absolute/path/to/run resume
```

Checkpoint writes use atomic replacement and checksums. STATUS is regenerated from
JSON. A running task is reconciled with its existing output before retrying. A
corrupt primary checkpoint falls back to the prior valid state and records that
recovery. If both are invalid, automatic execution stops for manual reconstruction;
it never silently starts a new meeting. Missing/changed completed artifacts block
new work until restored, or the facilitator produces an explicitly partial report.

## Validation and benchmarking

```bash
python3 -m unittest discover -s tests -v
python3 scripts/facilitator.py --help
```

Tests cover mode schedules, budget exhaustion, interruptions, retry bounds,
missing research, checkpoint corruption, output limits, and atomic writes. They
use fixture text, not real idea evaluations. Semantic quality, role selection,
evidence reuse, debate relevance and recommendation completeness require live
Codex runs and human review; see [benchmark protocol](references/benchmark.md).
No benchmark results or claimed savings are fabricated.

Recommended first benchmark: freeze the actual Nemesis brief, compare v1 against
v2 STANDARD on the same model/settings/evidence, then test QUICK and DEEP. Interrupt
STANDARD after its third completed assessment and verify those outputs are reused.
Measure tokens and quality together; fewer calls alone are not proof of efficiency.

## Troubleshooting and migration

- **Skill not found:** verify `~/.agents/skills/fix-my-idea/SKILL.md` and restart
  discovery/session. Install the references and scripts too.
- **Python unavailable:** use the documented manual STATUS ledger; disclose that
  machine checks are unavailable. Without filesystem tools, deliver records in
  chat and disclose that disk recovery is unavailable.
- **Browsing unavailable:** RESEARCH still records user facts and unverified
  assumptions; no fabricated facts or sources. A failed research task never
  authorizes unsupported assessments automatically.
- **Budget exhausted:** inspect STATUS and complete final synthesis, preserving
  unresolved work. A smaller target can yield fewer completed perspectives.
- **Failed specialist:** one authorized retry maximum, then explicit missing
  expertise. Essential missing expertise may require pausing the recommendation.
- **Conflicting recommendations:** preserve both claims, relevant evidence and a
  discriminating experiment; no vote can override a fatal dependency.
- **Invalid checkpoint/artifact:** follow [recovery steps](references/facilitator.md),
  preserve damaged files, and avoid manual edits to hashes merely to hide changes.
- **From v1:** the default changes from twelve seats to six. Select DEEP for
  twelve-seat coverage; targeted debate replaces compulsory all-seat exchanges.
  Existing v1 runs remain intact and resume using validated manual STATUS notes,
  retaining their twelve-seat scope unless explicitly changed. New runs use v2
  JSON checkpoints. `$fix-my-idea` and the original report filenames remain.

AI roles are not real customer testimony or licensed professionals. Running the
skill authorizes analysis documents and available specialist work within host
permissions, not spending, outreach, deployment, or implementing the business.
