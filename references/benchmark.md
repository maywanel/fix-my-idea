# Testing and benchmark protocol

## Deterministic checks

Run `python3 -m unittest discover -s tests -v`. Fixtures test scheduling and
accounting, not model quality. Validate SKILL frontmatter with the skill-creator
validator when available. CLI smoke tests must run in a temporary directory.

## Live scenario matrix (requires real Codex execution)

| Scenario | Required observable outcome |
| --- | --- |
| QUICK | Three selected perspectives, one opening each, no debate or specialist validation, concise repair |
| STANDARD | Six perspectives, shared research, at most one relevant exchange, one revision and six validation outputs |
| DEEP | Twelve perspectives, bounded debate, no more than two revision/review cycles, traceable report |
| Budget exhaustion | No new non-synthesis tasks after admission denial; partial report and explicit omissions |
| Interrupt/resume | Stop after third opening; restart with same path; unchanged valid openings reused without calls |
| Missing research | Browsing disabled produces assumption-labeled RESEARCH; deleted completed file blocks admission |
| Failed specialist | Fail an assignment twice; no third attempt, missing expertise affects recommendation |
| Conflicting recommendations | Security says isolation; growth says frictionless access: debate concrete claims, record tradeoff and discriminating test, no artificial consensus |
| Invalid checkpoint | Truncate primary JSON: recover backup and inspect orphan outputs; corrupt both: halt for reconstruction, no new run |
| Incomplete artifact | Opening lacking risks or tests fails semantic review even when nonempty; bounded retry |

Perform failure injection on disposable copies, not the sole copy of real work.
These scenarios cannot be certified by matching section headings or fixture text.

## Fair comparison

1. Freeze v1 at its original commit and v2 at the tested checkout; record commit
   IDs (and diff hash if uncommitted), Codex version, model, reasoning setting,
   tools, concurrency, budget, environment, and dates. Use isolated installs/runs.
2. Freeze a complete idea brief and evidence packet or source snapshot. Give every
   version the same facts and permissions. Do not allow previous outputs to leak
   into the next evaluation. Use equal settings and separate clean contexts.
3. Compare original v1 twelve-seat workflow to v2 STANDARD first; also run QUICK
   and DEEP to expose the quality/cost tradeoff. Repeat at least three times per
   configuration if feasible and alternate execution order. A single pilot is
   descriptive, not a reliable performance claim.
4. Collect metrics below, grade reports without version labels where practical,
   retain raw traces, and report per-run values plus median and range. Treat
   aborted/partial runs as results, not discarded outliers.
5. Run an interrupted STANDARD copy and compare successful recovery and extra
   calls against an uninterrupted run. Verify artifact hashes, not just filenames.

## Metrics and recording template

| Metric | Definition / source |
| --- | --- |
| Estimated total tokens | Same estimator across versions; include all model inputs, outputs, repeated context, tool text and facilitator work; disclose unavailable hidden reasoning |
| Runtime-reported usage | Optional separate field with exact metadata scope, cached/reasoning treatment; unavailable is N/A, never zero |
| Ledger accounted tokens | state.used, conservative reservations included; do not equate with runtime total or sum usage-event rows |
| Execution time | Wall-clock start to final artifact; record interruptions separately and active duration if measurable |
| Specialist calls | Actual assessment/debate/review calls, including failures/retries; distinguish simulated perspectives from independent agents |
| Research calls | Each actual search/open/retrieval, including failed and supplemental calls; record duplicate questions separately |
| Actionable recommendations | Deduplicated recommendations containing problem, change, reason, evidence, cost/difficulty, residual risk, owner/test/gate |
| Report completeness | Each of eleven required sections scored 0 missing, 1 generic/incomplete, 2 specific/useful; justified N/A reported separately |
| Evidence quality | Count unsupported factual claims, invalid citations, and major recommendations traceable to evidence or explicit reasoning |
| Recovery | Valid outputs reused, extra calls, lost contributions, successful completion or honest partial report |

Use a CSV/JSON row per run with: run_id, version, mode, model, settings, brief_hash,
source_snapshot, started_at, ended_at, interruption_seconds, estimated_tokens,
estimator, metadata_tokens_or_null, ledger_tokens_or_null, specialist_calls,
research_calls, duplicate_research_calls, actionable_recommendations,
completeness_score, unsupported_claims, recovery_result, notes, artifact_path.
Populate only observed values. Keep estimates and measured metadata distinct.

Proposed acceptance gate (not a result): STANDARD uses at least 30% fewer estimated
tokens than v1 on ordinary briefs, with no missed fatal constraint, no fabricated
evidence, and completeness within two points of v1 on the 22-point rubric. Also
compare tokens per actionable recommendation; do not reward tiny generic reports.
If it misses the gate, inspect duplicated context/research and output caps before
reducing necessary expertise. Report uncertainty for small samples.

## First real benchmark: Nemesis

Obtain the actual Nemesis brief; the project name does not establish its domain.
Freeze target users and buyer, problem, architecture, development stage, market,
team/time/budget, non-negotiables, and existing validation evidence. If it is an API
security product, use the six cybersecurity roles in SKILL; otherwise adapt them.

Run v1 and v2 STANDARD with the same brief and settings, STANDARD target 25,000
estimated tokens. Record any missing context as assumptions in both. Use the
scenario matrix to interrupt a separate STANDARD run after S03, resume, and check
S01–S03 checksums and absence of repeated calls. Then run QUICK at 8,000 and DEEP
at 60,000 to determine whether their extra or reduced coverage changes a real
product decision. Judge quality on the actual highest-risk Nemesis assumptions,
not an invented description of Nemesis.

No real Codex benchmark has been run or recorded by this protocol. Automated
unit tests and isolated simulated runs are engineering validation only.
