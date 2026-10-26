---
name: fix-my-idea
description: >-
  Repair and develop an idea through a collaborative meeting of domain-relevant
  specialists. Use for an idea boardroom, cross-functional repair, or a realistic
  validation and execution plan. Offers quick, standard, and deep modes; not a
  courtroom verdict or a request to implement the proposed business.
---

# Fix My Idea — v2.0

Facilitate a working meeting that preserves strengths, identifies failure
mechanisms, debates useful repairs, and produces a stronger, testable idea.
The facilitator is not a voting specialist. Never manufacture agreement or
silently replace the user's objective.

## Establish the brief and mode

Accept `$fix-my-idea <idea>` and plain language. Default to **STANDARD**.
Interpret `--mode quick|standard|deep` and `--budget <positive integer>` in the
prompt as user preferences, not Codex CLI flags. Natural language is equivalent.
If the idea is omitted, use the most recent identifiable idea; otherwise ask.
Never evaluate placeholder text as an idea.

| Mode | Perspectives | Assessment | Debate | Revision / validation | Suggested total tokens |
| --- | ---: | --- | --- | --- | ---: |
| QUICK | 3 | One independent round | None | One proposal; at most one revision, facilitator check | 8,000 |
| STANDARD (default) | 6 | One independent round | One focused exchange | One revision and all-seat validation | 25,000 |
| DEEP | 12 | One independent round | Up to two issues per cycle | Up to two revisions, all-seat validation per cycle | 60,000 |

Budgets are configurable planning targets, not enforceable runtime token caps.
Tell the user the selected mode, target, expected rounds, and whether independent
agents or a single-model simulation will be used. Do not silently upgrade modes.

Capture the original idea, beneficiary, buyer, problem, outcome, geography, stage,
resources, timeline, and non-negotiables in `BRIEF.md`. Ask only for gaps that
materially change direction; otherwise label working assumptions.

## Select the team and run the meeting

Read [meeting-protocol.md](references/meeting-protocol.md) before execution;
use [facilitator.md](references/facilitator.md) for ledger commands and recovery.
The facilitator alone selects roles, authorizes work, allocates research, advances
phases, and decides whether another permitted cycle is worthwhile. Specialists
must not spawn agents, browse independently, extend assignments, or retry themselves.

Select exactly 3, 6, or 12 distinct perspectives for the mode. Explain the reason
and non-overlapping remit of each in `ROSTER.md`; use stable IDs S01 onward.
Cover value to users, feasibility, and delivery/sustainability even in QUICK.
Adapt to the actual domain rather than filling generic executive seats:

- Cybersecurity STANDARD: Security Architect, Distributed Systems Engineer,
  Backend Engineer, DevSecOps Engineer, Startup Strategist, Enterprise Security
  Buyer. Distinguish threat model, scale, implementation, operations, business,
  and procurement remits.
- Mobile STANDARD: Mobile Engineer, UX Designer, Product Manager, Growth
  Strategist, Security Engineer, Business Analyst.
- AI STANDARD: ML Engineer, AI Safety Engineer, Infrastructure Engineer, Product
  Strategist, Domain Expert, Customer Researcher.

For QUICK combine complementary remits into three concrete specialties. For DEEP
add missing disciplines using the original coverage: customer research, domain
practice, product, engineering, experience, competition, distribution, sales,
finance, operations, legal/safety/trust, experimentation. Replace sales with
funding/governance for noncommercial work. AI roles are not actual customers or
licensed professionals.

Create `.fix-my-idea/<unique-run-id>/` only for a new meeting. On continuation,
inspect checkpoints first; never restart automatically. Use the Python ledger
when available, with one writer: the facilitator. Its sequential schedule is the
portable default. Independent agents can run sequentially in fresh contexts.
Parallel execution is optional only with a host-supported reservation mechanism
covering every in-flight task; this bundled ledger intentionally uses one task
at a time. Do not bypass it to parallelize.

Research once into `RESEARCH.md`, then share the same brief and evidence with each
opening specialist, without peer opinions. Rank disagreements by consequence and
use only relevant owners and challengers. QUICK records debate as skipped.
Synthesize the smallest repair that addresses critical mechanisms; retain a larger
pivot as an alternative if it changes non-negotiables. Validate the revision as
specified by mode. Never extend the round limits to achieve consensus.

At budget pressure stop new specialist work, skip optional debate, preserve
completed contributions, and use the synthesis reserve for a useful partial report.
Record gaps and the next executable step in `STATUS.md`.

## Deliver

Write `FIXED_IDEA.md` using [plan-template.md](references/plan-template.md).
Keep the original brief, roster, research, contributions, `DISCUSSION.md`, revisions,
reviews, and `STATUS.md`. QUICK remains concise; DEEP keeps full traceability.
Link actual evidence and preserve dissent, missing seats, and execution limitations.

Recommend proceed to validation, proceed conditionally, pivot with user agreement,
or pause. A fatal dependency cannot be outvoted. Make the plan fit the user's real
resources; assign responsible roles, not invented employees. If no viable repair
fits the constraints, say what would have to change.

Lead the final response with the revised idea, main changes, remaining uncertainty,
and first practical action; link the plan and discussion. This invocation permits
local meeting documents and available specialist work subject to host permissions.
It does not authorize contacting people, spending money, deploying software,
launching experiments, or implementing the business.
