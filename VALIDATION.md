# v2.0 validation record

Engineering validation completed on 2026-10-26. No real Codex idea benchmark or
billed-token measurement was performed.

- `python3 -m unittest discover -s tests -v`: 23 tests passed.
- `python3 scripts/facilitator.py --help`: passed.
- `git diff --check`: passed.
- Basic frontmatter identity/description, UI invocation, and local Markdown link
  checks: passed. These are not a full YAML schema validation.
- Skill-creator `quick_validate.py .`: could not run because its optional PyYAML
  dependency is absent (`ModuleNotFoundError: yaml`). No dependency was added to
  this standard-library skill merely to satisfy the external validator.

An independent review exercised isolated fixture-based QUICK and STANDARD runs:
interrupted output was adopted with one attempt; conflicting privacy/debugging
recommendations and their debate were preserved; budget pressure skipped remaining
work and allowed partial synthesis. These simulations did not invoke real
specialists and do not establish recommendation quality or resource savings.

Review findings fixed and covered by regressions: failed revisions cannot
schedule dependent validation; JSON of the wrong root type falls back to backup;
empty input manifests are rejected; failed final synthesis is reported as
incomplete; skipped DEEP revisions cannot authorize their reviews; partial final
reports show the proper delivery step. Command output is compact instead of
reprinting the growing full status and usage history on every call.

The automated suite also covers all mode schedules/default budgets, reserve
admission, exhausted budgets, bounded retries, missing/altered research, checkpoint
fallback, interrupted-output adoption, incomplete checkpoints, output caps,
accounting on invalid outputs, path containment, and atomic replacement failure.

Remaining validation: full skill-validator run in an environment with PyYAML,
real Codex mode invocations, meaningful domain selection, citation quality,
semantic review and conflict resolution, and matched v1/v2 Nemesis benchmarks.
Follow references/benchmark.md; do not interpret fixture token estimates as real
usage or the target acceptance gate as an achieved result.
