#!/usr/bin/env python3
"""Harness safety & compliance checker (binary‑question implementation).

Run via:
    hermes skill run harness-check-vault

Outputs JSON with per‑question results and aggregated dimension scores.
"""
import os, json, re, subprocess
from hermes_tools import terminal, read_file, write_file

# Helper to run a shell command and capture output
def run_cmd(cmd):
    res = terminal(command=cmd, timeout=30)
    return res.get('output', '').strip()

# Question definitions \u2013 each returns (passed:bool, explanation:str)
QUESTIONS = [
    # Process Safety ---------------------------------------------------
    {
        "id": "lock_exists",
        "dimension": "process_safety",
        "query": "hermes_local.lock \ud30c\uc77c\uc774 \uc874\uc7ac\ud558\uace0 \ub77d\uc774 \uc815\uc0c1 \ud68d\ub4dd\ub418\uc5c8\ub294\uac00?",
        "check": lambda: (
            os.path.exists(os.path.expanduser('~/hermes_local.lock')),
            "lock file \uc874\uc7ac" if os.path.exists(os.path.expanduser('~/hermes_local.lock')) else "lock file \uc5c6\uc74c"
        ),
    },
    {
        "id": "single_instance",
        "dimension": "process_safety",
        "query": "hermes_local \ud504\ub85c\uc138\uc2a4\uac00 \ud558\ub098\ub9cc \uc2e4\ud589 \uc911\uc778\uac00?",
        "check": lambda: (
            len([p for p in run_cmd('ps aux | grep hermes_local.py | grep -v grep').split('\n') if p.strip()]) == 1,
            "\ub2e8\uc77c \uc778\uc2a4\ud134\uc2a4 \uc2e4\ud589 \uc911" if len([p for p in run_cmd('ps aux | grep hermes_local.py | grep -v grep').split('\n') if p.strip()]) == 1 else "\ub2e4\uc911 \uc778\uc2a4\ud134\uc2a4 \ubc1c\uacac"
        ),
    },
    {
        "id": "restart_cleanup",
        "dimension": "process_safety",
        "query": "\uc7ac\uc2dc\uc791 \ud6c4 \uc815\uc0c1 \uc885\ub8cc \ub9c8\ucee4 \ud30c\uc77c\uc774 \uc874\uc7ac\ud558\ub294\uac00?",
        "check": lambda: (
            os.path.exists('/tmp/hermes_restart_ok'),
            "restart OK \ub9c8\ucee4 \uc874\uc7ac" if os.path.exists('/tmp/hermes_restart_ok') else "restart OK \ub9c8\ucee4 \uc5c6\uc74c"
        ),
    },
    # Routing Integrity ------------------------------------------------
    {
        "id": "routing_sensitive",
        "dimension": "routing_integrity",
        "query": "\ubbfc\uac10 \uc9c8\ubb38\uc774 \ub85c\uceec Gemma4 \ub85c \ub77c\uc6b0\ud305\ub418\ub294\uac00?",
        "check": lambda: (
            any('engine="local"' in line for line in open(os.path.expanduser('~/Applications/Mjauto/Scripts/hybrid_router.py')).read().split('\n')),
            "local \ub77c\uc6b0\ud305 \uc124\ud0c0 \uc874\uc7ac" if any('engine="local"' in line for line in open(os.path.expanduser('~/Applications/Mjauto/Scripts/hybrid_router.py')).read().split('\n')) else "local \ub77c\uc6b0\ud305 \uc124\ud0c0 \uc5c6\uc74c"
        ),
    },
    {
        "id": "routing_general",
        "dimension": "routing_integrity",
        "query": "\uc77c\ubc18 \uc9c8\ubb38\uc774 DeepSeek API \ub85c \ub77c\uc6b0\ud305\ub418\ub294\uac00?",
        "check": lambda: (
            any('engine="deepseek"' in line for line in open(os.path.expanduser('~/Applications/Mjauto/Scripts/hybrid_router.py')).read().split('\n')),
            "DeepSeek \ub77c\uc6b0\ud305 \uc124\ud0c0 \uc874\uc7ac" if any('engine="deepseek"' in line for line in open(os.path.expanduser('~/Applications/Mjauto/Scripts/hybrid_router.py')).read().split('\n')) else "DeepSeek \ub77c\uc6b0\ud305 \uc124\ud0c0 \uc5c6\uc74c"
        ),
    },
    # Meta\u2011Doc Synchronization ------------------------------------------
    {
        "id": "meta_timestamp",
        "dimension": "meta_sync",
        "query": "7\ub300 \uba54\ud0c0 \ubb38\uc11c\uac00 \ucd5c\uc2e0 \ud0c0\uc784\uc2a4\ud0ec\ud504(YYYY\u2011MM\u2011DD HH:MM) \ub85c \uad6c\ud558\ub294\uac00?",
        "check": lambda: (
            all(re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", open(p).read()) for p in [
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/01_hot.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/02_\uc2a4\ud06c\ub9bd\ud2b8 \uc815\ubcf4.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/03_\uc2dc\uc2a4\ud15c \uc778\ubca4\ud1a0\ub9ac.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/04_\uc8fc\uc694 \uc2dc\uc2a4 \uac00\uc774\ub4dc \ubc0f FAQ.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/05_\uc2dc\uc2a4\ud15c \uc0c1\ud0dc.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/00_Meta_\uc9c0\ub3c4.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/06_\uc5d0\uc774\uc804\ud2b8_\uc624\ub958_\ubc0f_\uc7ac\ubc1c\ub29c\uc9c0_\ubcf4\uace0\uc11c.md')
            ]),
            "\ubaa8\ub4e0 \uba54\ud0c0 \ubb38\uc11c\uc5d0 \uc720\ud6a8 \ud0c0\uc784\uc2a4\ud0ec\ud504 \uc874\uc7ac" if all(re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", open(p).read()) for p in [
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/01_hot.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/02_\uc2a4\ud06c\ub9bd\ud2b8 \uc815\ubcf4.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/03_\uc2dc\uc2a4\ud15c \uc778\ubca4\ud1a0\ub9ac.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/04_\uc8fc\uc694 \uc2dc\uc2a4 \uac00\uc774\ub4dc \ubc0f FAQ.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/05_\uc2dc\uc2a4\ud15c \uc0c1\ud0dc.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/00_Meta_\uc9c0\ub3c4.md'),
                os.path.expanduser('~/Applications/Mjobsidian/wiki/00_Meta/06_\uc5d0\uc774\uc804\ud2b8_\uc624\ub958_\ubc0f_\uc7ac\ubc1c\ub29c\uc9c0_\ubcf4\uace0\uc11c.md')
            ]) else "\ud0c0\uc784\uc2a4\ud0ec\ud504 \ub204\ub77d \ub610\u97a0 \ud615\uc2dd \uc624\ub958"
        ),
    },
    # Prompt Hygiene ---------------------------------------------------
    {
        "id": "prompt_length",
        "dimension": "prompt_hygiene",
        "query": "\uc800\uc7a5\ub41c \ud504\ub86c\ud504\ud2b8 \ud30c\uc77c\uc774 2KB \uc774\ud558\uc778\uac00?",
        "check": lambda: (
            (os.path.getsize(os.path.expanduser('~/.hermes/prompt.txt')) <= 2048) if os.path.exists(os.path.expanduser('~/.hermes/prompt.txt')) else True,
            "prompt \ud06c\uae30 2KB \uc774\ud558" if (os.path.exists(os.path.expanduser('~/.hermes/prompt.txt')) and os.path.getsize(os.path.expanduser('~/.hermes/prompt.txt')) <= 2048) else "prompt \uc5c6\uac70\ub098 2KB \ucd08\uacfc"
        ),
    },
]

def main():
    results = []
    dims = {}
    for q in QUESTIONS:
        try:
            passed, explain = q["check"]()
        except Exception as e:
            passed, explain = False, f"\uc608\uc678 \ubc1c\uc0dd: {e}"
        results.append({
            "id": q["id"],
            "dimension": q["dimension"],
            "query": q["query"],
            "passed": passed,
            "explanation": explain,
        })
        dims.setdefault(q["dimension"], []).append(passed)
    scores = {dim: sum(vals)/len(vals) for dim, vals in dims.items()}
    output = {"results": results, "dimension_scores": scores}
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
