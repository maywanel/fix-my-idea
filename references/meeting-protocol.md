# Meeting protocol

## Facilitator and phases

Use `scripts/facilitator.py` as the task ledger; read [facilitator.md](facilitator.md).
Only the facilitator writes checkpoints and authorizes work. Each task needs a
budget reservation before execution. Authorize no recursive delegation. One retry
per task, including facilitator tasks; failed seats stay visible. Do not replace a
failed seat with unlimited alternate roles. Budget refusal takes precedence over
retry eligibility. Keep task outputs within the character caps returned by the
ledger (characters are output constraints, not exact token limits).

The schedule is research → independent assessments → agenda → targeted debate →
revision → validation → final synthesis. QUICK skips debate and specialist
validation. STANDARD has one exchange and one revision/validation cycle. DEEP has
up to two exchanges per cycle and two cycles; skip the second cycle task by task
unless unresolved high-impact issues can plausibly be repaired within budget.
If a new substantive change is needed after the last validation, record it as an
untested alternative, not a validated revision.

## Shared research

Before assessment, write `RESEARCH.md` with:

- Evidence IDs E01 onward; verified facts and the exact supported claim.
- Relevant competitors and substitutes, technical constraints, market observations.
- Primary-source links, retrieval dates, source dates where relevant, and limits.
- User-supplied facts separately from externally verified facts.
- Assumption IDs A01 onward, unknowns, conflicting evidence, and validation needs.
- A query log: question, tool calls, result, and unresolved evidence gaps.

Prioritize decision-critical claims. Soft research call allowances are 2/4/8 for
QUICK/STANDARD/DEEP, counting each search or page retrieval separately. Batch
related questions when possible; host-required verification takes precedence.
If the allowance cannot cover necessary verification, stop lower-priority work or
label the remaining claims unknown. Never bypass host browsing requirements.
Research caps are planning limits, not permission to fabricate evidence.

Specialists reuse this record and cite E/A IDs; they do not repeat searches.
A specialist may return a gap request naming the claim, consequence, and smallest
useful query. The facilitator deduplicates it against the query log and may approve
at most 0/1/2 supplemental research batches respectively, each at most two calls,
only if it would change a decision and fits the remaining non-synthesis budget.
Record approval, question, reservation, and actual calls in the current agenda or
debate output. Use `charge` to reserve that extra work before doing it. Keep new
evidence in that task's immutable output, referenced by subsequent tasks; do not
silently edit the already-checkpointed research file. No recursive gap requests.

If browsing is unavailable or fails, still write `RESEARCH.md`: explicitly state
no external verification, record known user facts, assumptions and unknowns, and
how to verify them. Never invent interviews, quotes, traction, prices, market
proof, or citations. Market size is not demand and listed price is not willingness
to pay. Arithmetic projections are scenarios, not measured outcomes.

## Independent assessment

Prefer fresh agent contexts without inherited conversations. Provide absolute paths
to the neutral brief, common research record, own remit, and assigned output only.
Use available native agent tools; do not assume particular tool names or nested
agents. If unavailable, execute perspectives sequentially as a clearly labeled
single-model simulation; do not claim independent agreement. Shared worker contexts
must also be disclosed. Perspectives and independent agent calls are different metrics.

Assignment:

> You are {seat}, specializing in {role}. Read {brief} and {research}; your remit
> is {remit}. Produce {phase} at {absolute_output}, at most {cap} characters.
> Preserve non-negotiables. Do not read peer openings during assessment. Do not
> delegate, browse, extend scope, or retry. Return evidence gaps to the facilitator.
> Write only the assigned output; report completion or a specific blocker.

Each opening includes:

- **Perspective:** unique contribution to this idea.
- **What can work:** strongest success mechanism and necessary conditions.
- **What can fail:** up to three risks, trigger → mechanism → outcome.
- **Evidence:** E/A IDs, unknowns, confidence and reasons, no invented probabilities.
- **Repair:** specific change per risk, cost/difficulty, tradeoff, dependencies.
- **Test:** cheapest informative experiment, metric, threshold and its basis,
  decision changed by the result.
- **Cross-functional question:** most consequential claim another seat should address.

Inspect substance before `finish`; nonempty text is insufficient. For missing
requirements, `fail` with a precise reason; retry once within remaining budget.
After two failures, preserve unavailable expertise and qualify the recommendation.
Finish the assessment phase before debate, except when budget forces synthesis.

## Adaptive debate

Write the agenda in `DISCUSSION.md`. Group overlapping issues without hiding
separate mechanisms. Use R01 onward, rank by impact, irreversibility, and evidence
uncertainty. Select only relevant owner/challenger pairs. No all-pairs discussion.
If no consequential disagreement exists, record the shared assumption that could
invalidate the recommendation and skip debate; do not manufacture conflict.

Each scheduled debate covers ONE highest-impact unresolved issue, with exactly
at most three turns: owner claim (can quote the opening), challenger response,
owner reply. Cap each turn at 1,000 characters and the full exchange plus decision
at 4,000 characters. Supply actual claims, evidence, and relevant outputs. Record
attribution and responses, not a fictional transcript or invented quotation.

Record claim IDs, consequence, competing repairs, evidence, owner response,
who bears cost, dependencies, residual risk, and disposition: resolved by evidence,
resolved by design, needs test, or unresolved blocker. Stop early when further
exchange is unlikely to change the recommendation. Link debate files from the
final report; `DISCUSSION.md` is the immutable initial agenda, with stable expected
paths to exchanges. Skipped exchanges are explained in STATUS and the report.

## Revision and final validation

Build the concrete revision from the evidence and debate. Compare original versus
minimal repair; consider a larger pivot only if necessary. All selected seats in
STANDARD and DEEP review the revision, actual decisions, and evidence, including
unfavorable evidence. Each review is at most 1,400 characters:

- Status: ready to test / conditional / blocked, with reasons.
- Addressed issue IDs and assumptions still requiring validation.
- New risks or inconsistencies introduced by repairs.
- Specific release condition or blocker and next informative test.

QUICK uses a facilitator consistency check inside its revision, not another
specialist round. Across modes, check price versus cost, acquisition versus margin,
promises versus capability, timeline versus dependencies, and safeguards versus UX.
A fatal unresolved blocker controls the recommendation regardless of other seats.
The final report must state which reviews were completed, unavailable, or skipped.
