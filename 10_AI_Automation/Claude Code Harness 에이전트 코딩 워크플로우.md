---
title: "How Claude Code Harness turns agent coding into a contract-first delivery loop"
source: "https://x.com/AlphaSignalAI/status/2060390090179027396"
author:
  - "[[@AlphaSignalAI]]"
published: 2026-05-30
created: 2026-06-01
description: "Claude Code Harness는 에이전트 코딩을 계약 기반 전달 루프로 전환하는 워크플로우 플러그인이다. 5-동사 루프를 통해 에이전트 코딩을 전달 증거로 변환하며 13개의 가드레일을 제공한다. README에서 강조하지 않은 4가지 한계점이 존재한다."
tags: [ingested, 10_AI_Automation, claude-code, agent-coding, contract-first, workflow, automation, guardrails, delivery-loop]
  - "clippings"
brief: "brief"
---

![이미지](https://pbs.twimg.com/media/HJWN1WAWIAEAPSH?format=jpg&name=large)

## A workflow plugin, not a magic safety layer.

> **In ~7 mins: what a 1,730-star Claude plugin actually ships, the 5-verb loop that turns agent coding into delivery evidence, the 13 guardrails behind it, and 4 rough edges the README doesn't flag.**

When you let Claude Code loose on a repo, plans live in chat, tests become optional, review happens too late, and release notes get reconstructed from memory.

**Claude Code Harness** is an MIT-licensed plugin that wraps that work in a five-verb loop and treats two files as the source of truth.

**The shift** it represents is the part worth watching: agent tooling moving from chat output to delivery evidence.

**Snapshot:** v4.12.7, Go-native runtime, +1,700 stars, +190 forks, 33 shared skills.

## Why this is worth a look

Claude Code stacks have been quietly maturing. Hermes Agent, Superpowers, and a few others have started looking less like prompt packs and more like operating systems wrapped around the model. Harness sits in that same lane.

Its specific bet is narrow. The model can write useful code. The surrounding process keeps drifting. Plans float. Scope expands quietly. Review collapses into implementation. Release notes get rebuilt by memory.

![이미지](https://pbs.twimg.com/media/HJWOIRlW4AUqGQJ?format=png&name=large)

The repo was created in December 2025 and has shipped daily since. It carries +1,700 stars and +190 forks at v4.12.7, with the last push on 2026-05-27. There is no Hacker News thread, no Reddit discussion, no YouTube demo. Just a small Threads post and a steady release cadence. High-quality, under-the-radar.

## What it actually is

The author is **Chachamaru**, a Japanese-language solo developer who built Harness for what the repo calls "vibecoders": solo developers running full-cycle contract development through an agent.

Two single-source-of-truth files do the heavy lifting:

- **spec.md** is the product contract. What must stay true.
- **Plans.md** is the task ledger. What's being worked, what's done, what's blocking.

Five verb commands sit on top: **/harness-setup**, **/harness-plan**, **/harness-work**, **/harness-review**, and **/harness-release**. After install, the default changes from "ask the agent to code" to: write the spec, implement only the approved slice, verify, review independently, package evidence.

The repo is not a small prompt pack. It ships a Claude plugin manifest, a Codex plugin manifest, OpenCode mirrors, a Go runtime, hook definitions, setup scripts, 33 shared skills, tests, and release tooling. 1,529 tracked files. Shell leads the byte count at 2.13 MB, Go follows at 1.56 MB, then JavaScript, TypeScript, and a thin Python layer.

## How it works

![이미지](https://pbs.twimg.com/media/HJWOTLQXQAwwa4C?format=jpg&name=large)

The operating loop

Plan, work, review, release. Each stage has an explicit gate. The user approves the generated contract before any code is written. Major review findings block completion. Release preflight checks tag, version, changelog, and evidence packaging before any final action.

One rule sets the tone for the whole loop: data the agent has not directly seen stays unknown instead of getting silently invented. It is stated in the spec, not implied.

The Go runtime

The guardrail engine was rewritten in Go starting at v4.0 ("Hokage"). Cold start target is 1–2 ms, compared to roughly 40–60 ms for the older bash-and-TypeScript path the repo replaced. SQLite runs through [modernc.org/sqlite](https://modernc.org/sqlite), a pure-Go driver. No CGO, no Node.js, no compiler toolchain to install.

The package layout enforces the speed contract:

- **hook-fastpath** holds rule evaluation, codec, and types. No file I/O, no network, no goroutines.
- **worker-runtime** holds the SQLite store, session lifecycle, breezing orchestration, and OTel export.

Configuration collapses into one file. **harness.toml** is the source. **harness sync** regenerates **plugin.json**, **hooks.json**, and **settings.json** from it. The user edits one file, not five.

The repo wires 58 command-hook entries and 4 agent-hook entries through **hooks/hooks.json**, covering pre-tool, post-tool, permission, session, notification, stop, and task events.

The pre-tool, post-tool, and permission paths are the only ones the Go binary owns directly. Everything else still routes through shell handlers, and the project's own doctor warns when the hook config relies on legacy bash wrappers around the binary.

Guardrail rules

The runtime ships with thirteen rules (R01–R13), each tied to a specific tool surface.

- **Deny** rules block **sudo**, **git push --force**, **\--no-verify**, **\--no-gpg-sign**, writes to **.env**/**.git/**/**\*.pem**/**\*.key**, and **git reset --hard** on protected branches.
- **Ask** rules pause on **rm -rf**, package installs, force-with-lease pushes, **npx**, and direct pushes to main or master.
- **Warn** rules cover secret-like file reads (still allowed, but flagged) and edits to **package.json**, Dockerfiles, and CI workflows.

The honest tradeoff is on the design page: the hook system fails open on infrastructure errors. Deterministic deny rules still block when they run. But if the hook plumbing itself breaks, the design prefers approving the action to breaking the user's session.

Host adapter tiers

Harness names what it supports and what it does not. The capability matrix lists four tiers:

![이미지](https://pbs.twimg.com/media/HJWOZY-X0AIF3kk?format=jpg&name=large)

The project explicitly refuses to claim parity it cannot prove. That refusal is the design choice worth noticing on its own.

## How to get started

Full How-to guide in the appendix at the end.

Four lines through Claude Code:

```bash
claude
/plugin marketplace add Chachamaru127/claude-code-harness
/plugin install claude-code-harness@claude-code-harness-marketplace
/harness-setup
```

Then a small first request:

```bash
/harness-plan Improve the README onboarding flow
```

Harness writes or updates **spec.md** and **Plans.md** and returns a plan with scope, acceptance criteria, dependencies, unknowns, and stop conditions. The user's job is to approve or correct, not hand-write the plan.

Requires Claude Code v2.1+ and write access to the repo. Existing users should run **bin/harness doctor --migration-report** before reinstalling. It inventories stale plugin caches, duplicate Codex skills, OpenCode files, and old symlinks without deleting any of them.

## The AlphaSignal Take

Four rough edges worth knowing before adoption.

**Version drift inside the checked-out repo.** **VERSION**, **plugin.json**, and **harness.toml** all report v4.12.3. The included binaries (**./bin/harness version** and **./bin/harness-darwin-amd64 version**) report 4.11.4 (Hokage). The repo's own doctor catches the mismatch and recommends **cd go && make install**. A marketplace install ships the right binary. A clone-and-run-from-bin install does not.

**TDD is not enforced by default.** The README implies TDD verification on the work step. **harness.toml** ships with TDD enforcement disabled. R14, the TDD guardrail, is registered as a local-trial path rather than a blocking rule.

**The Breezing benchmark is narrower than it looks.** The report shows 14/15 passes with validation instructions versus 3/15 without, across 30 runs. The report itself flags the limits: three tasks, one model (GLM-4.5-air through [Z.AI](https://z.ai/)'s haiku tier), two actual bug categories under the surface, a two-stage adaptive design, and it tests validation instructions rather than the full Breezing pipeline. Useful signal. Not proof of system effectiveness.

**Documentation drift from the TypeScript era.** **docs/CLAUDE\_CODE\_COMPATIBILITY.md** still references v3.10.2 and Node.js requirements. The current README and the Go-runtime spec say Node is not required. Some skill files still reference deleted concepts. The project's own **deleted-concepts.yaml** exists exactly because this residue keeps showing up after every major migration.

The stronger claim is the narrower one. For Claude Code users, Harness gives a structured way to turn agent work into reviewed, evidence-backed repo changes. Treat it as a workflow and evidence system. Not a finished safety layer.

**Which part of your agent workflow gets the loosest when you let the model drive: plans, tests, or release notes?**

**All source links are in the first reply. Full breakdown of recent updates + daily signals in our newsletter (link in bio).**

## Appendix: Full command walkthrough

![이미지](https://pbs.twimg.com/media/HJWOubzWgAY1YW-?format=jpg&name=large)

## Install and setup

```bash
claude
/plugin marketplace add Chachamaru127/claude-code-harness
/plugin install claude-code-harness@claude-code-harness-marketplace
/harness-setup
```

Setup installs project guidance, command surfaces, hooks, and a baseline check so the workflow starts from a known state.

**/harness-plan <request>**

Example:

```bash
/harness-plan Add a JSON export endpoint to the user API
```

What it produces:

- A spec delta written to **spec.md**, or a documented "spec skip reason" if the request does not change the product contract.
- Task rows in **Plans.md** with scope, acceptance criteria, dependencies, unknowns, and stop conditions.

The user approves or corrects the contract before any code is written.

**/harness-work <task>**

Example:

```bash
/harness-work 1.1.1
```

Implements one approved slice and records verification evidence. The work step refuses silent scope expansion. If the work outgrows the approved row, the loop stops and asks.

**/harness-review**

Runs as a separate step, not blended into implementation. Major findings block completion. Minor findings return as recommendations. The verdict format is fixed: APPROVE or REQUEST\_CHANGES.

**/harness-release --dry-run**

Checks changelog state, version sync across **VERSION**, **plugin.json**, and **harness.toml**, tag boundaries, and release-evidence packaging. Dry-run reports what would happen without making any release action.

## Codex CLI route (compatibility, not parity)

```bash
git clone https://github.com/Chachamaru127/claude-code-harness.git
cd claude-code-harness
./scripts/setup-codex.sh --user
```

Mirrored skills are called as [$harness-plan](https://x.com/search?q=%24harness-plan&src=cashtag_click), [$harness-work](https://x.com/search?q=%24harness-work&src=cashtag_click), [$harness-review](https://x.com/search?q=%24harness-review&src=cashtag_click). Codex gets contract injection and post-run checks. It does not get Claude Code's pre-tool hook enforcement.

## OpenCode route (mirror + bootstrap)

```bash
/path/to/claude-code-harness/scripts/setup-opencode.sh
```

Mirrors the harness skills into OpenCode-compatible files. Runtime parity is not claimed.

## Existing-user health check

```bash
bin/harness doctor --migration-report
```

Inventories stale Claude plugin caches, missing slash entries, duplicate Codex skills, OpenCode files, backup paths, and harness-mem state. Deletes nothing. Run this before reinstalling or cleaning up.

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
