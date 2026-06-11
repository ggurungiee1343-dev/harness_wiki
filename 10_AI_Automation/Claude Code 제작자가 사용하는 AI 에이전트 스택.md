---
title: "The AI Agent Stack the Creator of Claude Code Uses (Builder's Guide)"
source: "https://x.com/Av1dlive/status/2064292484856041558"
author:
  - "[[@Av1dlive]]"
published: 2026-06-08
created: 2026-06-10
description: "이 글은 Claude Code의 창시자가 활용하는 AI 에이전트 스택을 소개한다. 공개된 인터뷰와 포스트를 기반으로 그의 설정을 재구성하여 주요 도구와 워크플로우를 정리한다. 이를 통해 개발자들이 자동화된 루프 작성과 에이전트 기반 작업을 구현하는 방법을 참고할 수 있다."
tags: [ingested, 10_AI_Automation, claude-code, ai-agent, automation, developer-tools, workflow, reconstruction, anthropic]
  - "clippings"
brief: "brief"
---

![이미지](https://pbs.twimg.com/media/HKXWiWaaEAAg10k?format=jpg&name=large)

i don't prompt claude anymore. my job is to write loops.

that line from Boris Cherny broke the internet. so I recreated his entire setup here's what I found

> **A note up front. This is a reconstruction, not a leak. Boris hasn't published his dotfiles. What follows is built from his public interviews, posts, and the Anthropic launch writing : stitched together with the primitives Anthropic shipped this year. The exact slash commands, Routines, and file layouts are my best-faith assembly of what he describes, not literal exports from his machine. Treat it as the closest reproducible version of his setup**

## "My job is to write loops"

In May, Boris Cherny, the creator of Claude Code at Anthropic, sat down at Acquired Unplugged with WorkOS and said the quiet part out loud.

<video preload="none" tabindex="-1" playsinline="" aria-label="담아간 동영상" poster="https://pbs.twimg.com/amplify_video_thumb/2064279433503191040/img/RN9P9G-Kw27IMTK4.jpg" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"><source type="video/mp4" src="blob:https://x.com/462e8e26-28db-4628-94ee-6cff028c0470"></video>

0:04 / 4:08

The clip in question

> "My job is to write loops."

He doesn't prompt Claude anymore. He writes loops that prompt Claude.

- Five to ten interactive sessions during the day and "a few thousand" agents overnight, mostly from his phone.
- Hundreds of Claude instances monitor Twitter, GitHub, and Slack for product ideas.

He uninstalled his IDE because he hadn't opened it in a month.

1. This is a phase change, and it's reproducible. Anthropic shipped every primitive Boris uses in the last six months: /loop, /schedule, Routines, /batch, dynamic workflows, skills, hooks, and the ant CLI.
2. None of it is gated to Anthropic engineers. It's in your Claude Code right now.
3. What's been missing is someone stitching the picture together end to end: three tiers, file layout, the canonical seven loops he describes running locally, the eight Routines that fit the overnight pattern he talks about, and the composition that makes it a system instead of a pile of features.

That's this article. 3,357 words of pure builder breakdown and what I use after going through all the blogs, tweets and videos on Boris and Claude blogs

I'm calling the resulting system **THE HIVE**. It's a few thousand agents working on your codebase, inbox, X mentions, and CLAUDE.md while you sleep.

Three composable tiers, real file paths, working slash commands, and a Monday through Friday on-ramp

## What Boris just said about running Opus autonomously

On June 8, 22 hours before this went out, Boris posted five fresh tips on running Opus autonomously for hours or days. These directly anchor everything below.

> 6월 8일
> 
> Opus가 장시간 작업에 최적의 모델임을 보여주는 여러 벤치마크를 보았습니다. Opus를 몇 시간/며칠 동안 자율적으로 실행하는 5가지 팁: 1. 권한 승인에 자동 모드를 사용하세요. Claude가 승인을 요청하지 않도록 하려면 2. 동적 워크플로우를 사용하세요. Claude가 수백/수천 개의 에이전트를

> "Seeing a number of benchmarks showing Opus is the best model for long-running work."

His five rules, verbatim and unpacked:

**1\. Auto mode for permissions.** So Claude doesn't ask for approval. This is the unlock for unattended runs. No human in the loop means no idle agent waiting on a click.

**2\. Dynamic workflows.** To have Claude orchestrate hundreds or thousands of agents to get a task done. Tier 3 of THE HIVE. We build this out in Part 4.

**3\. /goal or /loop.** To nudge Claude to keep going until it's done. The structural fix for agentic laziness. /goal sets a hard completion bar. /loop keeps the workflow firing on a schedule.

**4\. Claude Code in the cloud.** So you can close your laptop. Easiest path is the desktop or mobile app. This is why Tier 2 (Routines) exists in the architecture below.

**5\. End-to-end self-verification.** Claude in Chrome for web. iOS/Android sim MCP for mobile. A way to start the full web server for backend work. Without this, every overnight run becomes a coin flip in the morning.

Read tip 5 again. It is the single most important rule for unattended Opus work.

If Claude can't verify its own output against a real environment, you wake up to a thousand hallucinated diffs.

The HIVE blueprint below operationalizes all five.

## Part 1: The three tiers of agent orchestration

Every primitive Anthropic shipped in the last six months slots into one of three tiers.

Understanding the tiers turns a pile of cool features into a system.

| Tier | Primitive | Lives in | Survives laptop closing? | Min interval | What it's for |
| --- | --- | --- | --- | --- | --- |
| 1\. Local loops | /loop | Open Claude Code session | No | 1 min | Continuous in-session work while you code |
| 2\. Routines | /schedule  \+ Routines | Anthropic cloud | Yes | 1 hour | Overnight, hands-off, durable work |
| 3\. Swarms | /batch  \+ dynamic workflows | Subagents in worktrees | No (job-bound) | N/A | Massively parallel one-shot fan-out |

The whole HIVE is these three tiers, deeply composed.

- Tier 1 keeps you sharp while you work. Tier 2 keeps the system productive while you don't. Tier 3 throws compute at problems big enough to deserve it.
- The composition pattern is the magic.
- A Tier 2 Routine fires a Tier 3 batch, which writes findings to a file, which the next Tier 1 loop picks up and acts on.
- Once that flywheel spins, you spend your time on rubrics, gotchas, and taste.

Let's build each tier.

## Part 2: Tier 1, Local loops (the daytime layer)

/loop is a session-scoped scheduler inside a live Claude Code session.

Fixed cron interval (minimum one minute), or let Claude pick the interval dynamically.

A session holds up to 50 tasks. Recurring tasks expire after 7 days and restore on claude --resume.

The two formats you'll use 99% of the time:

```bash
/loop 5m <prompt>                    # fixed interval
/loop <prompt>                       # dynamic interval (1m to 1h)
/loop 30m /<your-slash-command>      # loop a slash command, not a prompt
```

Two killer details most people miss.

1. **You can loop a slash command, not just a prompt.** Build the workflow once as a slash command in .claude/commands/, then loop it. The loop becomes a one-line scheduler for an arbitrarily complex workflow.
2. **A .claude/loop.md file replaces the built-in maintenance prompt** when you run bare /loop. Project-level beats user-level. Edits take effect on the next iteration. Keep it under 25,000 bytes.

## 7 loops Boris runs (and you should too)

Four are verbatim from Boris's setup: /babysit, /slack-feedback, /post-merge-sweeper, /pr-pruner.

The other three are the natural completions.

Drop them into a fresh session in this order:

```bash
1. Babysit your PRs (review comments, failed CI, merge conflicts)
/loop 5m /babysit

# 2. Mine Slack feedback into PRs every 30 minutes
/loop 30m /slack-feedback

# 3. Sweep up missed code review comments after merges
/loop /post-merge-sweeper

# 4. Close stale PRs hourly so your dashboard stays clean
/loop 1h /pr-pruner

# 5. Triage new GitHub issues (classify, dedupe, label, assign)
/loop 15m /triage-issues

# 6. Mine corrections you keep making into CLAUDE.md rules
/loop 2h /claude-md-distiller

# 7. Watch the deploy and ping if anything regresses
/loop 5m /deploy-watch
```

Seven slash commands. Seven loops. All session-scoped.

All behaving themselves within the safety rail that irreversible actions only proceed when they continue something the transcript already authorized.

## What a slash command actually looks like

Slash commands live in .claude/commands/ and are checked into git.

Here is the entire content of .claude/commands/babysit.md

```markdown
---
description: Shepherd all open PRs assigned to me toward landed.
---

You are managing my open pull requests. For each PR I authored that is still open:

1. Pull the latest CI status. If anything failed and the failure is obvious
   (flake, lint, formatting), push a fix. If it's a real test failure, leave
   a comment explaining the suspected cause and tag me.
2. Read any new review comments since the last loop iteration. For each:
   - If it's a nit and uncontroversial, fix it and reply with a brief note.
   - If it's a design question, draft a reply but DO NOT post it. Surface
     it to me in your iteration summary.
3. If the PR has merge conflicts against main and they look mechanical
   (imports, lock files, whitespace), resolve them. If the conflict touches
   logic, leave a note for me.
4. If the PR has been green and approved for >30 minutes, enable auto-merge.

Output: one-line status per PR. Do not be verbose.
```

That's it. A markdown file with a description and a prompt.

Loop it every 5 minutes. You now have a junior engineer babysitting your PRs continuously, that you can stop with Esc.

## The pattern that makes this scale

Compose loops by composing slash commands.

- /babysit can invoke /triage-issues or /slack-feedback.
- A slash command can spawn a subagent (--agent=<name>) with a focused system prompt and a restricted toolset, defined in .claude/agents/.

The file layout you want:

```bash
your-repo/
├── .claude/
│   ├── commands/          # Slash commands (the units of loop-able work)
│   │   ├── babysit.md
│   │   ├── triage-issues.md
│   │   ├── slack-feedback.md
│   │   └── ...
│   ├── agents/            # Custom subagents with specific tools/prompts
│   │   ├── code-reviewer.md
│   │   ├── triage-classifier.md
│   │   └── verifier.md
│   ├── skills/            # Knowledge the agents pull in (Part 5)
│   │   └── ...
│   ├── workflows/         # Saved dynamic workflows (Part 4)
│   │   └── ...
│   ├── hooks/             # PreToolUse / PostToolUse / SessionStart hooks
│   │   └── format-on-write.sh
│   ├── loop.md            # Bare /loop default prompt
│   └── settings.json      # Permissions (the safe-bash allowlist)
└── CLAUDE.md              # Project-wide context, distilled rules
```

Everything in .claude/ is git-versioned, so your whole agentic configuration travels with the repo.

New hires inherit it on day one. This is exactly what dropped Anthropic's new-engineer ramp-up time from weeks to two days.

## Part 3: Tier 2, Routines (the overnight layer)

/loop dies the moment you close your laptop.

For overnight work you need **Routines**, Anthropic's cloud-hosted scheduled tasks.

1. Set up via /schedule in the CLI or at [claude.ai/code](https://claude.ai/code). They run on Anthropic infrastructure on a fresh git clone, with connectors configured per task, autonomously, one-hour minimum interval.
2. This is exactly what Boris is pointing at when he says "use Claude Code in the cloud, so you can close your laptop."
3. You can also trigger a Routine via API call or on GitHub events (webhook-shaped). That's the unlock for hooking them into the rest of your stack.

## 8 Routines that make THE HIVE run overnight

Here is the canonical overnight set. Configure each one once via /schedule, then forget about them.

```yaml
# Morning report (fires before you wake up)
0 6 * * *    /morning-report
  → Synthesize what landed overnight: PRs merged, issues closed, deploys,
    incidents. Post to #standup.

# Deep codebase audit (runs nightly, takes hours)
0 22 * * *   /deep-audit
  → Spawn a dynamic workflow that fans out across the codebase looking for
    dead code, security issues, perf regressions, dependency drift. Write
    findings to .claude/audit/<date>.md for the morning /triage to pick up.

# Twitter / X feedback monitor (every 2 hours)
0 */2 * * *  /x-feedback
  → Pull recent mentions, replies, and quoted tweets of our product handles.
    Classify (bug / praise / feature request / spam). Write actionable items
    to a Linear feeder queue. Drop the rest.

# GitHub issue triage (every 4 hours)
0 */4 * * *  /github-triage
  → Classify new issues, dedupe against existing ones, apply labels, assign
    to the right teammate based on CODEOWNERS, and propose a severity.

# CLAUDE.md distillation (Saturdays at 3am)
0 3 * * 6    /distill-claude-md
  → Mine the last 7 days of sessions for corrections I keep making. Cluster
    them with parallel agents, adversarially verify each candidate rule,
    propose updates to CLAUDE.md. I review Sunday morning.

# Dependency hygiene (Sundays at 4am)
0 4 * * 0    /dep-hygiene
  → Check for security advisories, propose upgrade PRs for safe minors,
    flag majors for human review.

# Flake hunter (every 3 hours during work hours)
0 9-18/3 * * 1-5    /flake-hunt
  → Look at the last 50 CI runs for tests that failed intermittently.
    Spawn a workflow that reproduces and root-causes the top three.

# Weekly recap (Fridays at 5pm)
0 17 * * 5   /weekly-recap
  → Compile merged PRs, closed tickets, and deploys into a recap. Post to
    #engineering. Include a "what got better this week" section.
```

These cron expressions are exact.

Note: avoid :00 and :30 for time-sensitive tasks. Anthropic adds up to 30 minutes of jitter to recurring tasks (derived from the task ID), so an hourly job scheduled for :00 may fire anywhere up to :30.

If exact timing matters, use 3 9 \* \* \* instead of 0 9 \* \* \*.

## How a Routine differs from a /loop in practice

The mental rule:

- **Tier 1 (/loop)** is for work that needs your session's context: open files, current branch, in-progress changes. It runs every minute if you want.
- **Tier 2 (Routines)** is for work that runs on a fresh clone, in the cloud, against the repo's main branch. It runs at most every hour.

If you find yourself trying to make a Routine do something that needs your local working directory state, you've picked the wrong tier.

## Part 4: Tier 3, /batch and dynamic workflows (the swarm layer)

This is where you get to a thousand agents.

This is what Boris means by tip 2: "use dynamic workflows, to have Claude orchestrate hundreds or thousands of agents to get a task done."

/batch is Claude Code's built-in fan-out primitive. It interviews you about the change, then fans the work out to "as many worktree agents as it takes (dozens, hundreds, even thousands) to get it done."

Each worktree is an isolated git checkout, so agents don't step on each other.

**Dynamic workflows** are the more general primitive: a JavaScript file Claude writes on the fly that uses agent(), parallel(), and pipeline() to coordinate subagents with their own clean context windows.

Trigger them by asking Claude for a workflow, or enable ultracode so Claude spins one up automatically.

They shipped May 28.

Three things workflows give you that no single context can:

- **Per-agent isolation.** Each subagent gets its own context window with one focused goal. No cross-contamination.
- **Per-agent model choice.** The workflow picks Opus for hard reasoning, Sonnet for the middle, Haiku for cheap exploration.
- **Per-agent isolation level.** Worktree (isolated git checkout) or remote (no checkout). The workflow decides what each agent needs.

## The three failure modes a workflow structurally prevents

The longer Claude works in a single context window, the more it falls into three failure modes Anthropic named explicitly.

- **Agentic laziness.** Claude addresses 20 of 50 security items and calls the rest "handled." Fix: /goal <criterion> plus a loop-until-done pattern, or an explicit synthesizer that counts.
- **Self-preferential bias.** Claude grades its own work favorably. A verifier with skin in the game can't be a fair verifier. Fix: a separate verifier that has never seen the original work, ideally on a different model.
- **Goal drift.** Gradual loss of fidelity across many turns, especially after compaction. Each summarization is lossy. "Don't do X" quietly disappears at turn 47. Fix: separate Claudes with focused goals and isolated state.

If you've ever shipped an agent and quietly known it was cheating on you, this is why.

Workflows remove the conditions that create those failure modes. This is also why Boris's tip 3 (/goal or /loop) and tip 5 (self-verification) matter so much for unattended runs.

**A real thousand-agent example**

Migrate every callsite of [user.email](https://user.email/) to user.primaryEmail across a 4,000-file monorepo.

Old way: write a codemod, hope it doesn't break edge cases, spend a week reviewing the diff.

**New way:**

```markdown
ultracode migrate every callsite of user.email to user.primaryEmail.
Spawn one agent per file that touches user.email. Each agent makes the
change in its own worktree, runs the relevant test file, and adversarially
reviews its own diff. Synthesize at the end with a summary of any callsites
that needed manual intervention.
```

**Claude writes a workflow that looks roughly like this:**

```javascript
// .claude/workflows/email-migration.js
const files = await bash('rg -l "user\\.email" --type ts');

const results = await parallel(
  files.split('\n').filter(Boolean).map(file =>
    pipeline(
      [file],
      // Stage 1: make the change in an isolated worktree
      async (f) => agent(\`In a worktree, change every user.email reference
        in ${f} to user.primaryEmail. Run the colocated test file. Return
        a diff and the test result.\`, {
        model: 'sonnet',
        worktree: true,
        schema: { diff: 'string', testPass: 'boolean', notes: 'string' }
      }),
      // Stage 2: adversarial review of the change
      async (result) => agent(\`Review this diff for correctness, especially
        for cases where the rename might be wrong (e.g. external API contracts,
        DB columns, serialization). Diff: ${result.diff}\`, {
        model: 'sonnet',
        schema: { approved: 'boolean', concerns: 'array' }
      })
    )
  )
);

return synthesize(results, 'Group by approved/needs-review. List concerns.');
```

You did not write that file. Claude did.

You described the job. Claude wrote the harness.

The workflow spawned ~one agent per matching file, easily 800 agents on a real codebase, each in its own worktree, each with its own clean context window.

The Bun team rewrote their Zig codebase to Rust this exact way.

**The six harness patterns you'll compose constantly**

Anthropic published these and they cover ~90% of real builder work.

1. **Classify-and-act.** A router decides the task type, dispatches to specialists. Use for triage, support, intake.
2. **Fan-out-and-synthesize.** Split into N pieces, parallel agents, barrier merge. Use for migrations, scoring, bulk extraction.
3. **Adversarial verification.** Every producer agent gets a fresh-eyes skeptic attacking its output. The pairing rule: the verifier sees only the rubric and the artifact, not who produced it.
4. **Generate-and-filter.** Produce N candidates, kill the failures, return the survivors. Asking for "the best answer" makes Claude commit early. Generate-and-filter makes Claude commit late, after every option has been challenged.
5. **Tournament.** Pairwise comparison until a winner. Comparative judgment beats absolute scoring, especially for taste-based work. The bracket lives in deterministic loop code, not in context.
6. **Loop-until-done.** Keep spawning agents until a stop condition fires (no new findings, theory verified, zero errors). Use for flake hunting, root-cause investigation.

Real workflows compose two to four of these. The mapping from job to pattern stack:

| Use case | Pattern stack |
| --- | --- |
| Migrations & refactors | Fan-out (one agent per callsite) → adversarial verification → loop-until-done. This is how Bun was rewritten from Zig to Rust. |
| Deep research | Fan-out (parallel searches) → adversarial verification per claim → synthesize one cited report |
| Draft verification | Identify claims → fan-out (one verifier per claim) → meta-verifier checks source quality |
| Sorting 1,000+ items | Tournament: pairwise comparison, bucket-rank, or bracket |
| Root-cause investigation | Generate theories from disjoint evidence → panel of verifiers and refuters → loop until one survives |
| Triage at scale | Classify-and-act → dedupe against existing tickets → fix or escalate. Pair with  /loop |
| Design, naming, UI choices | Generate-and-filter (5 to 20 options) → tournament with a rubric |
| Lightweight evals | Run candidate in worktree → comparison agents grade against rubric → refine, re-grade |

The shortcut: identify which failure mode your task is falling into, then pick the pattern that structurally prevents it.

Drift → fan-out. Self-preference → adversarial verification. Open-ended → loop-until-done. Hard-to-score → tournament.

**Three controls that keep workflows from burning tokens**

Workflows can balloon to 5 to 10x the tokens you expected without guardrails.

- **/goal** sets a hard completion requirement. Pair with the loop pattern: "don't stop until one theory works." Without it, the workflow stops at the first soft completion point.
- **/loop** runs the workflow on a recurring schedule. Continuous triage, weekly research updates, recurring verification.
- **Explicit token budgets.** Tell Claude: "use 10k tokens." Anthropic's own team is blunt: "Dynamic workflows often use more tokens, so think carefully about when and how to use them." Most coding tasks don't need a panel of five reviewers.

```plaintext
ultracode quick adversarial review of this assumption:
  "moving to Postgres eliminates our shard rebalancing."
  Use 5k tokens. /goal don't stop until you have either
  a counterexample or three independent confirmations.
```

**The quarantine pattern for untrusted input**

Any workflow that reads content you didn't write (support tickets, bug reports, user feedback, web pages, third-party API output) has to assume that content might contain prompt injection.

The fix is structural.

A read-only reader agent with no high-privilege tools digests the untrusted content and emits a structured summary.

A separate actor agent, which never sees the raw content, takes any privileged action based on that summary.

A 30-line reader removes an entire class of injection risk.

## Part 5: Skills, the knowledge layer that makes everything else worth running

A workflow is how the agent thinks. A skill is what the agent knows.

Without skills, every loop and every Routine reinvents the wheel.

Anthropic runs hundreds of skills internally across nine categories. For HIVE, build skills in four first.

1. **Verification skills.** "Spend a week just making your verification skills excellent." Anthropic flat out says this is the highest-impact investment on output quality. This is also how you operationalize Boris's tip 5: end-to-end self-verification.
2. **Runbooks.** "Symptom → tools → query patterns" for each service. This makes overnight Routines do useful work instead of spinning.
3. **Data fetching and analysis.** Monitoring stacks, dashboard IDs, table schemas, canonical user\_id, join keys.
4. **Code quality and review.** Your rubric for adversarial-review subagents.

**Skill anatomy that actually works**

A skill is a folder, not a markdown file.

Here's the layout for a signup-flow verification skill:

```bash
.claude/skills/signup-flow/
├── SKILL.md                 # Description (for the model) + main instructions
├── references/
│   ├── api.md               # Detailed endpoint signatures, called on demand
│   └── known-gotchas.md     # The hard-won lessons
├── scripts/
│   ├── drive_signup.ts      # Playwright script: signup → email → onboarding
│   └── assert_state.sh      # Programmatic state assertion at each step
└── config.json              # Per-user setup (test email, target env)
```

The SKILL.md description field is the most important field in the entire skill.

Claude scans it at session start to decide "is there a skill for this request?"

It's a trigger condition, not a summary. Write it for the model:

```yaml
---
name: signup-flow
description: Use when the user mentions signup, onboarding, email verification,
  or activation flows. Drives the full signup→email→onboarding journey in a
  headless browser, asserts state at each step, and surfaces the failing step
  with the captured screenshot.
---
```

**Five rules from Anthropic's skills post that are easy and costly to skip:**

1. **Don't restate the obvious.** Claude already knows how to code. Focus skills on what pushes Claude out of its default.
2. **Build a Gotchas section. Grow it incrementally.** The highest-signal content is hard-won rules like "the subscriptions table is append-only, the row you want is the highest version, not the most recent created\_at."
3. **Give Claude code, not just text.** Scripts let Claude spend turns on composition, not reconstructing boilerplate.
4. **Use ${CLAUDE\_PLUGIN\_DATA} for persistent memory.** A morning-report skill that reads its own history before generating the next one is dramatically better than one starting fresh daily.
5. **Save your workflows as skills.** Drop the workflow JS into a skill folder, reference it from SKILL.md. Now it's discoverable and shareable.

That last point is the bridge between Tier 3 (workflows) and the rest of the system.

A workflow saved as a skill becomes a primitive a loop or Routine can call. This is how you compose across tiers.

## Part 6: ant, the headless conductor that makes the whole thing run from cron

ant is the official Anthropic CLI.

One install:

```bash
brew install anthropics/tap/ant
# or
go install github.com/anthropics/anthropic-cli/cmd/ant@latest
```

It hit v1.10.0 on May 28, 2026, the same day dynamic workflows shipped. That timing wasn't an accident.

- What ant gives you is a shell-native, scriptable, Unix-pipe-friendly entry point to the Anthropic API.
- Output formats: json, jsonl, yaml, pretty, raw. Input patterns: flags, heredocs, files via [@path](https://x.com/@path), data URLs via @data://. Transforms with GJSON syntax baked in.
- For HIVE, ant is the headless conductor.
- Routines run on Anthropic's cloud. /loop needs an open session. But ant runs from anywhere: your laptop's cron, your CI, a GitHub Action, a server, a webhook handler.

Here is a system cron entry that runs the entire morning report pipeline without any Claude Code session being open:

```bash
# Every weekday at 6am, generate the morning report and post to Slack
0 6 * * 1-5  cd ~/work/myrepo && \
  gh pr list --state merged --search "merged:>=$(date -v-1d +%Y-%m-%d)" --json title,url,author \
  | ant messages create \
      --model claude-haiku-4-6 \
      --message @data://stdin \
      --transform 'content.0.text' \
  | slack-cli post --channel '#standup'
```

That's a swarm-grade morning report.

Every merged PR turned into a one-line summary by Haiku in parallel, posted to Slack. Built with gh + ant + slack-cli + cron. No framework. No FastAPI. No import anthropic.

The pattern: ant is what lets a Tier 2 Routine reach out and trigger a Tier 3 workflow, or what lets a Tier 1 loop wake up a Tier 2 process.

It is the glue that makes the three tiers compose into one system.

The mental model: think of ant the way you think of curl. You don't build a curl framework. You pipe.

## Part 7: Putting THE HIVE together, the composition flywheel

You have all the parts.

Here is how they compose into the system that makes Boris's setup possible, and yours, by Friday.

The flywheel (how Boris's phone runs a few thousand agents overnight)

```markdown
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   TIER 2: Overnight Routines (Anthropic cloud)              │
│   • /deep-audit writes findings to .claude/audit/<date>.md  │
│   • /x-feedback writes ideas to .claude/inbox/x.jsonl       │
│   • /github-triage labels and assigns issues                │
│                          │                                  │
│                          ▼                                  │
│   ant cron jobs read those files, post digests to Slack     │
│                          │                                  │
│                          ▼                                  │
│   TIER 1: Morning /loops in open session read the inbox     │
│   • /loop 15m /triage-issues acts on yesterday's triage     │
│   • /loop 30m /slack-feedback turns ideas into PRs          │
│   • /loop 5m /babysit shepherds those PRs to landed         │
│                          │                                  │
│                          ▼                                  │
│   TIER 3: When a loop hits a big job (migrate 4000 files,   │
│   audit security across the repo), it spawns a /batch or    │
│   dynamic workflow with hundreds of worktree subagents      │
│                          │                                  │
│                          ▼                                  │
│   Findings flow back to .claude/audit/, CLAUDE.md, Linear   │
│                          │                                  │
│                          ▼                                  │
│   Weekly /distill-claude-md Routine mines all of this and   │
│   proposes new rules. You review Sunday morning.            │
│   The system gets smarter every week.                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

The composition rules:

1. **Tier 2 writes files. Tier 1 reads files.** Routines run on fresh clones with no access to local state, so the only durable handoff is the git repo. Have Routines write structured outputs (.jsonl, .md) into .claude/inbox/ or .claude/audit/. Loops read from there.
2. **Tier 1 spawns Tier 3 on demand.** When a loop hits a job too big for one Claude (repo-wide refactor, 1000-row triage), it invokes /batch or asks for a workflow. The swarm runs, writes results, the loop continues.
3. **Tier 3 results feed Tier 2's next cycle.** A nightly audit's findings become the next morning's triage queue. The clock cycle is measured in days.
4. **The CLAUDE.md distillation loop closes the meta-loop.** Weekly, a Routine mines your sessions, clusters corrections with parallel agents, adversarially verifies candidate rules, proposes additions to CLAUDE.md. You approve Sunday. Your agent is measurably better next week.

This is the part that compounds. Not the model, the system.

## The minimal HIVE: what to ship by Friday

If you have one week, here's what to build. In order.

1. **Monday.** Foundations.
- brew install anthropics/tap/ant and confirm it works.
- Create .claude/ with empty commands/, agents/, skills/, workflows/, a loop.md, and a settings.json with a permissions allowlist for the bash commands you run constantly.
- Write a starter CLAUDE.md, 500 to 2000 tokens of project, stack, code style, how-we-test.

**2\. Tuesday.** Your first verification skill.

- Pick the most painful "Claude wrote code that looked right but didn't work" pattern from last month.
- Build a skill folder with a script that exercises it end to end and asserts on the result.
- This is the highest-ROI engineering action you'll take this year. It is also Boris's tip 5 in concrete form.

**3\. Wednesday.** Three slash commands.

- Pick three from the canonical seven. Write the .md files in .claude/commands/. Test each manually before looping.

**4\. Thursday.** Loop them.

- One session, set /loop 5m /babysit, /loop 30m /slack-feedback, /loop 1h /pr-pruner. Let them run all day.
- Tune prompts based on what surprises you.

**5\. Friday.** Two Routines and a workflow.

- Schedule /morning-report and /deep-audit via /schedule. Run one ultracode workflow on a real codebase-wide task.
- Pro gets 5 Routines/day, Max 15, Team/Enterprise 25. Pick the most valuable first.

**6\. Weekend.** Distillation.

- Add /distill-claude-md Routine for Saturday 3am. Review and merge Sunday morning.
- Monday morning of week two, you wake up to a morning report, a triaged inbox, eight overnight audit findings, six new product ideas from X mentions, and a sharper CLAUDE.md.

## Closing: write loops

Models keep getting smarter. Every quarter, someone ships something that obsoletes whatever clever prompt you wrote last quarter.

The model is a commodity. It's meant to be one.

What compounds is the harness.

- The seven loops in your session. The eight Routines running overnight. The verification skill you spent a week perfecting. The workflow Claude wrote that you saved and invoke from a slash command. The CLAUDE.md distilling your team's tacit knowledge every Sunday morning.

Boris said his job is to write loops.

- He's been doing it long enough that he uninstalled his IDE a month before he noticed. That's the literal job now.
- The good news: Anthropic shipped every primitive you need in the last six months. The pattern language is published. The stack the creator of Claude Code describes using is reproducible from public material. You just read the spec and assemble it.
- The bad news: nobody's going to build your HIVE for you.
- Do the Monday list. Add a loop a day. By the end of the month, you'll look back at your old workflow (one Claude in a trench coat with three system prompts taped to its back) and you won't believe you used to work that way.
- The model will be a commodity. The hive is yours.

Build the loops. Ship the loops. Let the loops ship the rest.

Disclaimer This article written by the author using his notes and the latest documentation edited by Opus 4.7