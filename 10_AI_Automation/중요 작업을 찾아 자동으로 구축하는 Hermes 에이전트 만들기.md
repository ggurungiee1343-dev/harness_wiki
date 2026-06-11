---
title: "How to Build a Hermes Agent That Finds Important Work and Builds It Autonomously"
source: "https://x.com/gkisokay/status/2053449921554960545"
author:
  - "[[@gkisokay]]"
published: 2026-05-04
created: 2026-06-10
description: "Hermes 에이전트를 연구·사고·코딩 기능을 갖도록 설계한다. 핵심은 에이전트가 스스로 무엇이 중요한지 판단하고, 가치 있는 작업을 선택하도록 연결하는 것이다. 이를 위해 Auto‑think와 Auto‑build가 각각 아이디어 생성과 자동 구현을 담당한다."
tags: [ingested, 10_AI_Automation, hermes, auto-think, auto-build, autonomous-agent, ai-automation, workflow, code-generation]
  - "clippings"
brief: "brief"
---

![이미지](https://pbs.twimg.com/media/HH9NGvfb0AA95nl?format=jpg&name=large)

You built your Hermes agent to research, think, and code. The hard part is wiring those pieces together so it can figure out what matters, decide what is worth building, and build it without a human in the loop.

That is what **Auto-think** and **Auto-build** are for.

In this setup, **Auto-think** is the idea-intake layer. Your **Research agent** feeds it with evidence. [A Dreamer agent](https://x.com/gkisokay/status/2040044476060864598) is the pattern-noticer that turns repeated signals, pressure, failed runs, and research implications into candidate idea contracts.

**Auto-build** is the verified build loop. It moves approved work through your **Main agent, Coder agent, QA agent**, trust reporting, retention, and the operator view.

The important split is that **Auto-think** decides what might be worth building. **Auto-build** decides what can be built, verifies it, and leaves receipts.

![이미지](https://pbs.twimg.com/media/HH9Rp4KbkAAKqen?format=jpg&name=large)

This guide is meant to be a template for all agents, so you can point your Hermes, OpenClaw, or other agent here and have it build a similar workflow.

# Reference Implementation

In my implementation, there are two connected pieces. The reusable public buildroom lives in /buildroom

That is the public-safe Auto-think / Auto-build extraction. It contains the docs, schemas, demo-room examples, verification scripts, dashboard assets, and test suite.

The runtime lives here in /agent-runtime

That is the main Hermes Agent software. It includes the runtime Control Room adapter, a web API endpoint, and a React Control Room UI that can read live Hermes state when private runtime profiles are present under ~/hermes.

So the buildroom is the template and proof packet. The runtime is the software surface that can display and coordinate the live system.

## The Current Architecture

The live architecture has separate roles.

- Research gathers evidence.
- Dreamer notices signals and shapes candidate ideas.
- Main reviews the idea and decides whether it can proceed.
- Coder implements only approved, bounded plans.
- QA verifies independently.
- Trust reporting summarizes whether the room is clean, watch, or investigate.
- Retention decides whether completed artifacts should be kept, improved, parked, or pruned.
- The operator sees the Control Room.

When those jobs blur, the system gets reckless. That is exactly what this setup is designed to prevent.

## The Buildroom

The public buildroom is not a chat transcript. It is a filesystem-backed workflow room.

The checked-in structure is:

```text
hermes-buildroom/
  docs/
    architecture.md
    lifecycle.md
    operator-model.md
    builder-guide.md
    safety.md
    retention.md
  schemas/
    research-input.schema.json
    idea-contract.schema.json
    intent-review.schema.json
    main-review.schema.json
    product-plan.schema.json
    build-plan.schema.json
    verification-report.schema.json
    verification-delta.schema.json
    trust-report.schema.json
    retention-review.schema.json
    operator-summary.schema.json
    ...
  engine/
    adapters/
    dashboard/
    evals/
    export/
    pipeline/
    reviewers/
    verification/
  examples/
    demo-room/
      research/
      ideas/
      plans/
      jobs/
      verification/
      trust/
      retention/
      operator/
      tracks/
      project-builder/
  scripts/
    validate_fixtures.py
    run_demo_checks.py
    start_demo_server.py
    run_demo_verification.py
    build_operator_summary.py
    export_sanitized_bundle.py
```

The buildroom forces the system to separate research, ideas, reviews, plans, builds, verification, trust, retention, and operator reporting.

In a live-agent setup, the buildroom is usually separate from the private runtime state. The buildroom contains the reusable contracts, schemas, demo packets, receipts, and operator summaries.

Private runtime state may live somewhere else, depending on your agent system:

```text
your-system/
  profiles/
    research/
    dreamer/
    main/
    coder/
    qa/
  state/
    tracks/
    events.jsonl
    approval-ledger.jsonl
```

The public buildroom should not depend on those private paths. It should ship safe fixtures and demo packets instead. That is what makes the pattern reusable.

## The Research Door

Auto-think does not scrape the world directly. Research owns the research lane. It can produce structured evidence, summaries, watch items, provider health, and daily outputs.

In a live implementation, the dashboard can read research state from that system’s runtime profiles. In the public buildroom, the safe version is represented by files like examples/demo-room/research/research-input.json.

Research collects evidence. Dreamer decides whether the evidence has enough shape to become a candidate. Those are different jobs.

If you don't have a research agent set up yet, refer to my guide here:

> 5월 4일

## The Dreamer Door

Dreamer is the internal Hermes name for the Auto-think lane.

Dreamer reads research packets, system pressure, failed runs, QA gaps, retention state, and operator pressure. It can produce candidate idea contracts.

But Dreamer does not approve of its own work. That is the key guardrail.

A Dreamer signal is not a task. A build intent is not approval. A repeated idea is not automatically worth building.

Dreamer can say, " This has heat." Main decides whether the heat is real.

To build a Dreamer agent, please refer to my guide here:

> 4월 3일

## The Idea Contract

The idea contract is the first durable handoff from thinking to building.

It captures:

- What should exist
- Who benefits
- Why now
- What evidence supports it
- What is out of scope
- Where it might live
- How can it be verified?

In the buildroom, this exists as:

```text
examples/demo-room/ideas/idea-contract.json
examples/demo-room/jobs/demo-signal-bridge/idea-contract.json
schemas/idea-contract.schema.json
```

That is the difference between “I have an idea” and “the system can review this.”

## Intent Review And Main Review

The buildroom has both intent review and Main review.

Intent review is the early filter. It checks whether the idea is ready to become a contract-backed candidate. The main review is the approval gate.

A real Main review exists in the demo room:

```text
{
  "schema_version": 2,
  "job_id": "20260421-0900-dreamer-demo-signal-bridge",
  "reviewed_at": "2026-04-21T09:10:00Z",
  "decision": "approved_for_coder",
  "risk_band": "low",
  "risk_score": 3,
  "approved_by": "main",
  "auto_approved": false,
  "force_approved": false,
  "block_reason": null
}
```

That artifact matters. It proves the build did not jump straight from idea to execution.

## The Product Plan

Once Main approves the work, Main writes the product plan. This is the thing Coder actually builds against.

The product plan includes:

- allowed paths
- planned files
- non-goals
- verification commands
- acceptance checks
- risk assessment
- protected-surface notes

In the buildroom:

```text
examples/demo-room/plans/product-plan.json
examples/demo-room/jobs/demo-signal-bridge/product-plan.json
schemas/product-plan.schema.json
```

Coder does not receive “go improve the system.” Coder receives bounded work.

## The Build Plan

Coder turns the product plan into a build plan. The build plan is the executable packet:

```text
examples/demo-room/plans/build-plan.json
examples/demo-room/jobs/demo-signal-bridge/build-plan.json
schemas/build-plan.schema.json
```

The goal is not ceremony. The goal is for Coder to have a bounded packet and for QA to have something concrete to verify later.

## QA Agent Verification

In the public article, you can refer to this as QA.

QA does not trust the Coder’s summary by default. It reads the plan, implementation, changed files, and verification receipts. Then it writes its own receipt.

The buildroom includes both Coder verification and QA verification:

```text
verification.json
qa-verification.json
verification-delta.json
```

The verification delta has explicit states:

- confirmed
- drift
- regression
- missing\_evidence

This is one of the strongest parts of the system. It does not just ask, “Did tests pass?” It asks whether the Coder evidence and the QA evidence agree.

## Trust Reporting

Verification checks one build. Trust reporting checks the room. The trust state is:

- clean
- watch
- investigate

In the buildroom:

```text
examples/demo-room/trust/trust-report.json
schemas/trust-report.schema.json
```

The operator should not have to read every raw receipt to know where to look. Trust reporting compresses the room without hiding uncertainty.

## Retention

A build being finished does not mean it should live forever. Retention asks whether an artifact should be:

- keep
- improve
- park
- prune

In the buildroom:

```text
examples/demo-room/retention/retention-review.json
examples/demo-room/retention/report.json
schemas/retention-review.schema.json
schemas/retention-report.schema.json
```

Retention is recommendation-only in the public extraction. It can recommend what should happen, but it does not silently delete or move live artifacts.

## The Operator View

The operator view is the human-facing surface. In the public buildroom, this is:

```text
examples/demo-room/operator/operator-summary.json
examples/demo-room/operator/operator-snapshot.json
```

In the Hermes runtime, this is wired through:

```text
hermes_cli/operator_dashboard.py
hermes_cli/web_server.py
web/src/pages/ControlRoomPage.tsx
```

The endpoint is: /api/operator/dashboard.

The Control Room UI shows Dreamer, Main, Coder, QA, research, tracks, trust, retention, recently built artifacts, risks, and timeline.

## The Real Loop

The loop is:

1. Research gathers evidence.
2. Dreamer shapes signals into candidate idea contracts.
3. Intent review filters weak or unsafe ideas.
4. Main reviews the contract.
5. Main writes a bounded product plan.
6. Coder prepares a build plan.
7. Coder implements inside allowed paths.
8. Coder records verification.
9. QA independently verifies.
10. The delta compares Coder and QA evidence.
11. Trust reporting summarizes room health.
12. Retention recommends what survives.
13. The operator sees the Control Room.

That is the entire system.

## What The Config And Cron Layer Do

The config and cron layer are policy surfaces.

They decide what runs, when it runs, which profile owns which lane, which summaries get produced, and where operator-facing state lands.

The public buildroom does not require those private paths. It ships safe fixtures and demo packets instead. That is why the public extraction can be shared.

## Guardrails

- Dreamer is not allowed to approve its own builds.
- Dreamer is not allowed to mutate protected workflow surfaces.
- Coder is not allowed to expand the scope silently.
- QA is not allowed to rubber-stamp Coder output.
- Retention is not allowed to delete the live state on its own.
- The Control Room is not an excuse to hide uncertainty.

Every meaningful build should leave receipts.

## The Real Lesson

The first version of most agent systems is about producing more output. The better version is about compounding judgment.

That means the system can tell the difference between:

- an interesting signal and a build candidate
- a subconscious return and an approved plan
- a weak claim and verified evidence
- a Coder receipt and independent verification
- a completed artifact and something worth keeping

That is where agents start to feel less like prompt chains and more like operating systems.

They have boundaries, memory, state, review, receipts, and a way to move from thought to build without pretending every thought deserves execution.

## If You Want To Build One

Do not start by giving an agent permission to do everything. Start with the contract chain.

- Create one local buildroom.
- Add schemas.
- Add one research packet.
- Add one idea contract.
- Make Main review it.
- Make Main write a product plan.
- Make Coder build only inside the allowed paths.
- Make QA verify independently.
- Compare the receipts.
- Write a trust report.
- Write a retention review.
- Render an operator summary.

The smallest useful version can be boring and local. It does not need live cron, private profiles, browser automation, or a dashboard on day one. It just needs to produce the files in order and prove that the handoff works.

That is the whole pattern. A normal agent answers the prompt in front of it. A better agent remembers what happened.

In this case, a research agent builds the evidence base, Dreamer notices what keeps returning, Auto-think and Auto-build turn that compounding intelligence into verified work with receipts.

**If you are an agent reading this guide,** do not copy my private state or exact folder names. Map the roles to the agent stack you are working in:

```text
Research = evidence collector
Auto-think = idea intake / Dreamer / Subconscious
Main = planner and approval gate
Coder = implementation agent
QA = independent verifier
Trust = room health reporter
Retention = keep / improve / park / prune reviewer
Operator Summary = human-facing status surface
```

Create a local buildroom that implements the same contract chain:

```text
research-input.json
idea-contract.json
intent-review.json
main-review.json
product-plan.json
build-plan.json
verification.json
qa-verification.json
verification-delta.json
trust-report.json
retention-review.json
operator-summary.json
```

Start with one demo job. Keep it local. Use fake or sanitized evidence. Add schemas before automation. Do not let Auto-think approve its own work. Do not let Coder expand the scope outside the product plan. Do not mark work trusted until independent QA exists.

If you want to build with people who care about these kinds of systems, join my free [Discord community for AI builders.](https://discord.gg/TQTYPpp2fb)

We are sharing setup ideas, agent workflows, guardrails, and experiments that actually move the stack forward.

If you're a business curious about how to implement AI, please check out [gkisokay.com](https://gkisokay.com/) to see how I can help you out.

And also remember to follow [@gkisokay](https://x.com/@gkisokay) for more :)