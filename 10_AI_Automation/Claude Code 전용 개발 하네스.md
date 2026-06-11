---
tags: [ingested, Unsorted, 10_AI_Automation, claude-code, development-harness, ai-automation, autonomous-workflow]
date: 2026-05-25 10:47:30
ingested_at: 2026-05-26 14:24:39
description: "Claude Code를 위한 전용 개발 하네스 도구에 대해 설명한다. 자율적인 계획-작업-검토 사이클을 통해 고품질의 개발 결과물을 달성하는 것이 핵심이다. AI 기반의 자동화된 개발 워크플로우를 구축하여 개발 효율성을 극대화한다."
brief: "brief"
---


---
title: "Chachamaru127/claude-code-harness: Claude Code Dedicated Development Harness - Achieving High-Quality Development Through an Autonomous Plan→Work→Review Cycle"
source: "https://github.com/Chachamaru127/claude-code-harness"
author:
  - "__WIKI_LINK_PLACEHOLDER_0__"
published:
created: 2026-05-25
description: "Claude Code Dedicated Development Harness - Achieving High-Quality Development Through an Autonomous Plan→Work→Review Cycle - Chachamaru127/claude-code-harness"
tags:
  - "clippings"
---
## Claude Code Harness

[![Claude Harness](https://github.com/Chachamaru127/claude-code-harness/raw/main/docs/images/claude-harness-logo-with-text.png)](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/images/claude-harness-logo-with-text.png)

**Plan. Work. Review. Ship.**  
*A disciplined delivery loop for Claude Code, with bounded paths for Codex and OpenCode.*

English | [日本語](https://github.com/Chachamaru127/claude-code-harness/blob/main/README_ja.md)

[![Claude Code Harness operating loop: Spec, Plan, Work, Review, Release](https://github.com/Chachamaru127/claude-code-harness/raw/main/docs/images/readme/hero-operating-loop-en.png)](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/images/readme/hero-operating-loop-en.png)

Claude Code is powerful, but raw agent work drifts: plans live in chat, tests become optional, review happens too late, and release evidence gets rebuilt by memory. Harness turns that into one repeatable operating path.

After install, the default changes from "ask the agent to code" to:

1. write the spec and plan,
2. implement only the approved slice,
3. verify the result,
4. review independently,
5. package evidence for PR or release.

## Quickstart

New users should start from the tool they already use. Existing users should run the migration report before cleanup or reinstall.

| Path | Start |
| --- | --- |
| New user | [Tool-first onboarding](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/onboarding/index.md) |
| Existing user | [Migration check](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/onboarding/migration.md) |
| Claude Code fast path | [Install in 30 seconds](#install-in-30-seconds) |
| Trigger proof | [Skill trigger gate](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/onboarding/skill-trigger-acceptance.md) |

## Install in 30 Seconds

```
claude
/plugin marketplace add Chachamaru127/claude-code-harness
/plugin install claude-code-harness@claude-code-harness-marketplace
/harness-setup
```

Next command: run `/harness-plan` with one small request.

```
/harness-plan Improve the README onboarding flow
```

## First 15 Minutes

1. Install through your tool route.
2. Run `/harness-setup` or the equivalent setup script.
3. Run `/harness-plan` with a small request; Harness writes the `spec.md` and `Plans.md` drafts for you to check.
4. Approve the generated contract or reply with the correction you want.
5. Run the smallest approved task, for example `/harness-work 1.1.1`.
6. Run `/harness-review` and keep the verification output.

Your job is not to hand-write the plan. It is to approve or correct the generated contract before execution continues.

## How It Works

Harness adds a source-of-truth loop around agent work. The 5 verb skills keep that surface small: plan, work, review, sync, release.

1. You describe the outcome in normal language.
2. `/harness-plan` drafts or updates `spec.md` and `Plans.md` with scope, acceptance criteria, unknowns, and stop conditions.
3. Harness treats those files as the source of truth. Data the agent has not seen stays `unknown` instead of being silently invented.
4. `/harness-work` implements the approved slice with TDD and verification.
5. `/harness-review` separates review from implementation.
6. `/harness-release` packages only verified evidence.

## Commands

| Command | What happens inside |
| --- | --- |
| `/harness-setup` | Installs project guidance, command surfaces, hooks, and checks so the workflow starts from one known baseline. |
| `/harness-plan` | Turns intent into `spec.md` and `Plans.md`, including scope, acceptance criteria, dependencies, unknowns, and stop conditions. |
| `/harness-work` | Executes one approved task or range, adds tests when required, runs verification, and keeps work inside the plan. |
| `/harness-work all` | Runs the approved plan through implementation and review paths; use after the plan is clear and the repo baseline is known. |
| `/harness-review` | Reviews the result separately from implementation and treats major findings as blockers. |
| `/harness-release` | Checks release readiness, CHANGELOG/tag boundaries, and evidence packaging after implementation and review are complete. |
| `bin/harness doctor --migration-report` | Inventories old plugin caches, Codex skills, OpenCode files, symlinks, and memory state without deleting data. |

## Basic Workflow

| Stage | Output | Gate |
| --- | --- | --- |
| Investigate | Evidence and unknowns | Do not promote unobserved data into claims. |
| Plan | `spec.md` + `Plans.md` | User approves or corrects the generated contract. |
| Work | Code and tests | TDD required when the task says so. |
| Review | Independent verdict | Major findings block completion. |
| PR | Evidence pack | PR ready is not release ready. |
| Release | Tag/release artifacts | Release preflight must pass on the release path. |

## Install By Tool

| Tool | Tier | Route |
| --- | --- | --- |
| Claude Code | `supported` | Claude plugin marketplace, then `/harness-setup`. |
| Codex CLI | `internal-compatible` | `scripts/setup-codex.sh --user`; direct plugin smoke is tracked separately. |
| Codex app | `candidate` | Candidate smoke only; do not reuse Codex CLI proof. |
| OpenCode | `internal-compatible` | `scripts/setup-opencode.sh`; runtime parity is not claimed. |
| Cursor | `candidate` | PM handoff or adapter research only. |
| GitHub Copilot CLI | `candidate` | Manual profile research only. |
| Antigravity CLI | `future/unsupported` | No end-user install route in this phase. |

## Existing User Migration

Run `bin/harness doctor --migration-report` before changing an existing setup. The report inventories stale Claude plugin caches, duplicate Codex skills, old symlinks, OpenCode backup paths, and harness-mem state without deleting anything.

## Support Boundary

Harness can describe candidate paths, but it does not inherit support claims from Superpowers, Hermes Agent, or any other project. A host only moves up when Harness has its own bootstrap, trigger, runtime, and release evidence.

`not_observed != absent`: missing local proof means "not proven here", not "impossible" and not "supported".

## Requirements

- Claude Code v2.1+ for the supported Claude path.
- A project repository with write access for local setup.
- No Node.js is required for the Go-native guardrail engine.
- Optional [harness-mem](https://github.com/Chachamaru127/harness-mem) for cross-session memory when configured and healthy.

## Advanced

Use these after the basic trigger path is visible.

| Capability | What it adds | Boundary |
| --- | --- | --- |
| Breezing | Planner/Critic/Worker style team execution for larger task lists. | Still gated by plan quality and review. |
| Codex companion review | Schema-backed Codex second opinion through `scripts/codex-companion.sh`. | Raw `codex exec` is not the Harness companion path. |
| OpenCode bootstrap | Mirrors Harness guidance into OpenCode-compatible surfaces. | Real runtime parity is not claimed. |
| harness-mem | Project-scoped memory and recall across sessions. | Optional companion; purge remains explicit. |

## Documentation

| Resource | Description |
| --- | --- |
| [Tool-first onboarding](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/onboarding/index.md) | Where to start by host tool. |
| [Install routes](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/onboarding/install.md) | Per-tool setup and support-tier boundaries. |
| [Migration check](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/onboarding/migration.md) | Existing-user impact, compatibility, and rollback path. |
| [Skill trigger gate](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/onboarding/skill-trigger-acceptance.md) | How install success is verified. |
| [Capability matrix](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/tool-capability-matrix.md) | Supported, internal-compatible, candidate, and unsupported host claims. |
| [Claude Code Compatibility](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/CLAUDE_CODE_COMPATIBILITY.md) | Current Claude Code requirements and compatibility notes. |
| [Cursor Integration](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/CURSOR_INTEGRATION.md) | Cursor handoff boundary and candidate-route notes. |
| [Distribution Scope](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/distribution-scope.md) | Included vs compatibility vs development-only paths. |
| [Hardening parity](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/hardening-parity.md) | Runtime safety differences between Claude hooks and Codex gates. |
| [Work All Evidence Pack](https://github.com/Chachamaru127/claude-code-harness/blob/main/docs/evidence/work-all.md) | Success/failure verification contract for full-plan execution. |
| [Changelog](https://github.com/Chachamaru127/claude-code-harness/blob/main/CHANGELOG.md) | User-facing version history. |

---
*정리 완료 시간: 2026-05-26 14:24:39* (Harness Ingest Auto-Linker 가동)

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
