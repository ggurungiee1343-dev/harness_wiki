---
title: "Your LLM Is Burning Through Tokens - Karpathy Found a Way to Save 90%"
source: "https://x.com/bonsaixbt/status/2059266993950277656"
author:
  - "[[@bonsaixbt]]"
published: 2026-05-26
created: 2026-06-01
description: "Andrej Karpathy의 아이디어에서 영감을 받은 지식 베이스 시스템 구축 방법을 논의한다. 대규모 언어 모델이 동일한 원시 파일을 반복적으로 업로드하고 재처리하는 문제를 해결한다. 토큰 낭비를 90%까지 절감할 수 있는 효율적인 방법을 제시한다."
tags: [ingested, 20_Research, llm, token-efficiency, knowledge-base, karpathy, optimization, context-management]
  - "clippings"
brief: "brief"
---

![이미지](https://pbs.twimg.com/media/HJP4lSsW0AAO9WK?format=jpg&name=large)

# More specifically, we’re going to discuss how to build a knowledge base system inspired by Andrej Karpathy

One of the biggest problems with large language models is having to repeatedly upload and reprocess the same raw files over and over again

LLMs waste huge amounts of tokens re-reading documents, lose context between files, sometimes miss important relationships, and often produce less accurate answers because of it

Karpathy’s solution is the **Wiki Layer** (LLM Wiki)

**Don’t forget to bookmark this article so you can read it later or come back to it whenever you need it**

**The idea is simple, but incredibly powerful:**

The LLM cleans, structures, and links all of your data once, then stops working with raw files entirely and instead operates on a clean, organized knowledge base

**As a result, you get:**

- massive token savings (up to 70-90% on repeated queries)
- significantly better answer quality and relevance
- automatic links between documents
- a visual knowledge graph
- a system that continuously grows and updates itself over time

## The Structure of the Wiki Layer

The entire system is built around three core folders:

1. raw/ - immutable source files

This is where all original materials are stored: HTML pages, PDFs, text notes, screenshots, spreadsheets, and any other raw data

This folder is never edited manually, it remains the single source of truth

2\. wiki/ - the main knowledge base

Clean, well-structured Markdown files generated and maintained by the LLM itself

This becomes the primary workspace the model interacts with going forward

3\. Instructions and templates

Separate files that define all the rules: How data should be cleaned, which templates to use, how links are created, what metadata should be added, and how the knowledge base should be updated over time

## Step-by-Step Guide to Building a Wiki Layer

**1\. Set Up the Project**

Create a root project folder and place all your existing materials inside a raw/ subfolder

**2\. Launch the Structuring Agent**

In Claude (or any powerful LLM with file and code support), provide a dedicated system prompt

**The agent will automatically:**

- clean files from technical junk, ads, and unnecessary formatting
- convert everything into clean, readable Markdown
- apply predefined templates
- create internal wiki links (\[\[Page\_Name\]\])
- add metadata and establish relationships between documents

**3\. Open the Knowledge Base in Obsidian**

Simply open the project folder in Obsidian

**You’ll instantly get:**

- a visual knowledge graph with automatic links
- powerful full-text search
- the ability to jump between connected notes in seconds

**4\. Work With the Finished Knowledge Base**

Now, instead of uploading dozens of files every time, you simply tell the model:

“Work with my Wiki database inside the wiki/ folder”

The LLM can then instantly retrieve information from a clean, structured, and interconnected knowledge system

## Why a Wiki Layer Is Better Than the Traditional Approach

- token efficiency - the model no longer has to repeatedly re-read raw files every time you ask a question
- higher accuracy - all information is already cleaned, structured, and interconnected
- scalability - the knowledge base can easily grow to hundreds or even thousands of documents
- better workflow - obsidian turns the entire system into a visual “second brain”
- privacy - everything stays on your local machine, nothing needs to be uploaded to the cloud

# When You Should Start Using a Wiki Layer

- you already have more than 10-20 documents on the same topic
- your data is constantly being updated or expanded
- you regularly generate content, reports, research or ideas
- you work with personal, business, or confidential information

# Adapting the System to Your Own Needs

The agent prompt is fully customizable

Inside the instruction files, you can define:

- which templates should be used for different document types
- which metadata fields are required (date, author, tags, summary, etc.)
- the rules for creating links between notes
- how the agent should handle updates and conflicts

This makes the Wiki Layer useful for almost any field: marketing, software development, learning, health, business analytics, and much more

# Final Thoughts

Karpathy’s Wiki Layer transforms a chaotic collection of files into a true AI knowledge base

Once you spend time setting it up, you get a powerful, constantly evolving system that dramatically improves both the quality and speed of working with any LLM

If you enjoyed this article or found it useful:

- I’d really appreciate a repost
- And don’t forget to follow [@bonsaixbt](https://x.com/@bonsaixbt)

I share AI-related content and discoveries daily, so don’t lose me in your feed 👀

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
