# Fix My Idea

A Codex skill that brings **12 relevant AI specialists** into a company-style working meeting to challenge, repair, and develop your idea into a practical plan.

Inspired by the adversarial approach of the Court skill, this meeting goes beyond a verdict. Specialists identify what could fail, defend what could work, debate proposed changes, and turn the revised idea into experiments and execution milestones.

## Install

After this repository is published on GitHub, send this prompt to Codex:

```text
$skill-installer install the fix-my-idea skill from the GitHub repository maywanel/fix-my-idea, using the repository root (path .) and installation name fix-my-idea.
```

The skill should be available on your next turn. If it does not appear, start a new Codex session.

The skill lives at the repository root. Install it with the name `fix-my-idea`, including its `agents/` and `references/` directories, rather than only copying `SKILL.md`.

## Use

```text
$fix-my-idea I want to create a subscription service that delivers
affordable meals to university students in Morocco. My budget is
20,000 MAD, I’m working alone, and I want to test demand within a month.
```

For a more useful plan, include:

- Your idea and the problem it solves.
- Who will use it and who will pay for it.
- Your location or target market.
- Available budget, time, skills, and team.
- What you have already tried or learned.
- Constraints you do not want changed.

An early, rough idea is enough to start. The facilitator asks about critical missing information and labels working assumptions.

## How the meeting works

1. **Establish the brief.** Capture the idea, objective, evidence, resources, and constraints.
2. **Choose 12 specialists.** Adapt the disciplines to the idea and explain each seat’s role.
3. **Assess the idea.** Each specialist identifies strengths, failure mechanisms, potential repairs, and cheap tests.
4. **Debate and repair.** Specialists challenge specific claims and respond to each other. Every major issue gets an owner, a challenger, and a recorded outcome.
5. **Review the revision.** All 12 seats examine the revised proposal for remaining blockers and risks introduced by the changes. The process allows up to two revision/review cycles.
6. **Deliver the plan.** Produce a concrete recommendation, validation experiments, resource estimates, responsibilities, milestones, and decision gates.

The meeting preserves meaningful disagreements. It does not force consensus or treat a majority opinion as proof that an idea works.

## Who is in the room?

The starting roster covers these disciplines:

| Specialist | Focus |
| --- | --- |
| Customer research | Real pain, behavior, and willingness to change |
| Domain practice | How the problem is handled in the real world |
| Product strategy | Value proposition, differentiation, and scope |
| Technical feasibility | Buildability, dependencies, and limitations |
| Experience and service design | Usability, accessibility, and adoption friction |
| Market and competition | Alternatives and market entry |
| Distribution and growth | Acquisition channels and their economics |
| Sales and partnerships | Buying decisions, procurement, and conversion |
| Finance and business model | Pricing, costs, cash needs, and sustainability |
| Operations and delivery | Capacity, reliability, support, and supply chains |
| Legal, safety, and trust | Relevant constraints and potential harms |
| Experimentation and execution | Tests, measurement, and sequencing |

These are starting points, not a fixed panel for every idea. A food business may need manufacturing and food safety expertise; a community project may need governance and volunteer operations. The meeting retains exactly 12 specialist seats, plus a facilitator.

## What you get

Each meeting saves its records in a new folder under:

```text
.fix-my-idea/<unique-run-id>/
```

The main deliverables are:

- **`FIXED_IDEA.md`** — the revised idea, changes and tradeoffs, failure modes and repairs, smallest useful pilot, validation plan, economics, roadmap, and unresolved decisions.
- **`DISCUSSION.md`** — material arguments, challenges, responses, evidence, and decisions.
- **`ROSTER.md`** — the 12 selected specialties and their responsibilities.
- **`STATUS.md`** — progress and outstanding work for an interrupted meeting.
- The original brief and specialist contributions.

The plan connects major risks to proposed repairs and tests. Larger investments depend on explicit decision gates, with conditions for continuing, changing direction, or stopping.

## Execution and limitations

Codex uses native specialist agents when available and runs them within the host’s concurrency limits. Twelve seats do not require twelve agents running simultaneously. If workers must share contexts, the meeting discloses that limitation. If subagents are unavailable, it uses a clearly labeled single-model simulation.

Research depends on the tools and permissions available in your session. Unverified claims stay labeled as assumptions or unknowns. If file access is unavailable, records are delivered in the conversation instead.

This is a substantial multi-round workflow, so expect more time and model usage than a single response. The specialists are AI roles, not real customer interviews or licensed professional advice. The output is a plan to validate—not a guarantee of success. Sometimes the right recommendation is to pause or change a critical constraint.

Running the skill creates analysis and planning documents. It does not authorize spending money, contacting people, launching experiments, or implementing the business.

## Repository structure

```text
fix-my-idea/
├── README.md
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── meeting-protocol.md
    └── plan-template.md
```

See [the skill instructions](SKILL.md), [meeting protocol](references/meeting-protocol.md), and [plan template](references/plan-template.md) for the full workflow.
