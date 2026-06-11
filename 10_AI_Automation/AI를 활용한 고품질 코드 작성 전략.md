---
title: "Using AI to write better code more slowly"
source: "https://nolanlawson.com/2026/05/25/using-ai-to-write-better-code-more-slowly/"
author:
published: 2026-05-26
created: 2026-05-27
description: "AI 코딩의 목적을 단순히 저품질 코드를 빠르게 대량 생산하는 수단으로 보는 시각이 많다. 그러나 LLM은 매우 유연하여 고품질의 코드를 작성하는 데에도 효과적으로 활용될 수 있다. 속도에 매몰되지 않고 AI를 통해 더 정교하고 나은 코드를 작성하는 방법을 제안한다."
tags: [ingested, Unsorted, 10_AI_Automation, ai-coding, software-quality, llm, development-strategy]
  - "clippings"
brief: "brief"
---


A lot of people seem convinced that the point of AI coding is to write low-quality code as fast as possible. Spew out barely-passable slop, open massive PRs, and merge them unvetted. Ship it!

But the thing is, LLMs are very flexible. And you can use them just as effectively to write *high-quality* code more *slowly*.

This statement seems completely obvious to me at this point, and I almost didn’t want to write this post for that reason. But there seem to be enough people convinced that LLMs are only good as [slop cannons](https://x.com/i/status/2021617680525172840) that it’s worth making the opposite case.

If [Mythos](https://www.anthropic.com/research/glasswing-initial-update) taught us anything, it’s that LLM agents are *really good* at finding bugs. Throw them at a codebase enough times, and they will find so many bugs that you’ll barely know what to do with them.

Like [many others](https://xbow.com/blog/mythos-like-hacking-open-to-all), I’ve also found this is true of non-Mythos models – some may be better than others at finding subtle bugs or avoiding false positives, but the fact is that the latest public models from Anthropic and OpenAI are good enough to find plenty of bugs in an unscrutinized codebase.

The problem is not so much *finding* the bugs, but instead prioritizing and validating them. For this reason I have a Claude skill I adapted from [this article](https://milvus.io/blog/ai-code-review-gets-better-when-models-debate-claude-vs-gemini-vs-codex-vs-qwen-vs-minimax.md) ‘s core insight, which is that the more, different models you throw at a PR review, the less likely you are to get hallucinations or bogus bugs.

The skill says (paraphrasing):

> Run a Claude sub-agent, Codex, and Cursor Bugbot to find bugs in this PR ranked by critical/high/medium/low. Once they’re all done, review their findings, do your own research to rule out false positives, and write a final report.

That’s basically it. You can add your own definition of “bug” if you want – mine has stipulations about the [KISS](https://en.wikipedia.org/wiki/KISS_principle) and [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) principles, writing accessible HTML/JSX, using proper indexes for SQL queries, etc.

In my experience, this skill always finds tons of bugs in a PR, and the false positive rate is near zero. It finds so many bugs that you’ll be bored senseless if you try to tackle them all. They’ll range from critical security or correctness bugs to the more mundane medium-level perf bugs to low-level “this comment is misleading”-type bugs.

My typical workflow is:

- Have an agent fix all the criticals and highs (with my guidance on the proper solution), then repeat until no criticals/highs
- Skip highs/mediums where the juice isn’t worth the squeeze (e.g. 100 lines of code to fix a narrow edge case)
- Abandon the PR if it has so many criticals that I realize the whole approach is misguided

When I use this technique, I haven’t necessarily seen my velocity go up. If anything, the review process often finds *pre-existing* bugs, so I end up on a tangential side-quest where I’m writing unit tests and fixing subtle flaws that pre-date the PR. This is the opposite of the “10x productivity” slop-cannon style of development that most people imagine when they think of vibe coding, but I find it very satisfying.

It’s a great way to improve the overall health of the codebase while also teaching you about the odd corners of it. In my experience, the happy-path of a complex architecture is less interesting than its failure modes. And pre-LLMs, this is usually how I got familiar with a codebase anyway: understanding where the assumptions break down, and then getting my hands dirty to fix it.

If you’re the kind of person who is skeptical that AI coding is good for *anything*, then I doubt this post will persuade you. But if you’re the kind of developer who uses agents to write multi-hundred-line PRs that you barely understand yourself, I’d invite you to slow down a bit and try this other, slower style of “vibe coding.” Ask an agent how your PR works and how it might fail. Have it write Markdown docs with [Mermaid charts](https://mermaid.ai/open-source) if necessary. Use [Matt Pocock’s `/grill-me`](https://www.aihero.dev/my-grill-me-skill-has-gone-viral) skill until you understand the entire PR front-to-back.

You might not be more “productive” in terms of raw lines of code. You might burn a ton of tokens just to find out that your entire plan was wrongheaded from the start. But I find this style of coding to be a more super-powered version of the kind of programming I was already trying to do before LLMs: careful, methodical, quality-obsessed, focused on making things better for the next coder.

So take a deep breath, slow down, try this technique, and see if you don’t enjoy writing better code more slowly.

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
