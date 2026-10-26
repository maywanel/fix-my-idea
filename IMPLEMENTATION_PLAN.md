# v2 implementation plan

Inspection: v1 consists of SKILL.md, README.md, two references, and UI metadata.
No executable orchestration, tests, or configurations beyond UI metadata exist.
It selects 12 domain-adapted seats, gathers independent openings, requires every
seat in debate, then reviews with every seat for up to two cycles. It preserves
brief, roster, contributions, discussion, final plan, and informal STATUS notes.
Retries are bounded to one but checkpoint integrity and budgeting are not enforced.

1. Keep the collaborative repair philosophy, formats, artifacts, and permission
   boundaries. Default to six seats; retain twelve-seat coverage in DEEP.
2. Add a standard-library Python ledger: fixed mode schedules, authorization,
   reserved synthesis budget, usage estimates, bounded attempts, hashed artifacts,
   atomic state with backup, and a derived human-readable STATUS.
3. Centralize research and select only consequential disagreements for debate.
   Preserve sequential simulation when independent agent tools are unavailable.
4. Test deterministic behavior and document real-run benchmarking separately.

Justified changes: universal twelve-seat debate is replaced with targeted exchanges;
QUICK omits specialist validation to reduce overhead. DEEP retains comprehensive
review, with the second cycle optional. No business-planning capability is removed.
