#!/usr/bin/env python3
"""
Stop Hook v2 — 스마트 세션 종료 체크리스트
코드/문서 수정 여부를 감지해 필요한 항목만 표시.
~/.claude/settings.json hooks.Stop 에서 호출
"""
import sys, json, subprocess, os, re

data = json.load(sys.stdin) if not sys.stdin.isatty() else {}

wiki    = os.path.expanduser("~/Applications/Mjobsidian/wiki")
scripts = os.path.expanduser("~/Applications/Mjauto/Scripts")

# ── 1. Wiki 미커밋 파일 수 ───────────────────────────────
try:
    r = subprocess.run(["git", "-C", wiki, "status", "--short"],
                       capture_output=True, text=True, timeout=5)
    wiki_uncommitted = [l.strip() for l in r.stdout.strip().splitlines() if l.strip()]
except Exception:
    wiki_uncommitted = []

# ── 2. Scripts 변경 파일 감지 — 최근 30분 내 수정된 .py ──
# (Scripts/는 독립 git이 없으므로 mtime 기반 감지)
try:
    import time
    cutoff = time.time() - 1800  # 30분
    changed_py = []
    for subdir in ["modules", "handlers"]:
        target = os.path.join(scripts, subdir)
        if not os.path.isdir(target):
            continue
        for f in os.listdir(target):
            if f.endswith(".py"):
                fp = os.path.join(target, f)
                if os.path.getmtime(fp) > cutoff:
                    changed_py.append(f"{subdir}/{f}")
except Exception:
    changed_py = []

# ── 3. 수정 파일 유형 분류 ───────────────────────────────
has_module  = any("modules/" in f for f in changed_py)
has_handler = any("handlers/" in f for f in changed_py)
has_wiki    = len(wiki_uncommitted) > 0
has_any_py  = len(changed_py) > 0

# ── 4. 조건부 메시지 구성 ────────────────────────────────
lines = []

if not has_any_py and not has_wiki:
    # 변경 없는 순수 탐색 세션 → 간단 메시지
    lines.append("✅ 세션 종료 — 파일 변경 없음")
else:
    lines.append("📋 세션 종료 체크리스트")

    if has_wiki:
        lines.append(f"⚠️  Wiki 미커밋 {len(wiki_uncommitted)}개:")
        for f in wiki_uncommitted[:5]:
            lines.append(f"   {f}")
        if len(wiki_uncommitted) > 5:
            lines.append(f"   ... 외 {len(wiki_uncommitted)-5}개")
        lines.append("   → git -C wiki add -A && git commit 필요")

    if has_any_py:
        lines.append(f"📝 수정된 Python 파일 ({len(changed_py)}개):")
        for f in changed_py[:5]:
            lines.append(f"   {f}")
        if len(changed_py) > 5:
            lines.append(f"   ... 외 {len(changed_py)-5}개")

    if has_any_py or has_wiki:
        lines.append("")
        lines.append("→ 필요한 메타 업데이트:")
        if has_any_py:
            lines.append("  ✏️  05_시스템 상태.md (코드 변경 이력)")
        if has_module:
            lines.append("  ✏️  02_스크립트 정보.md (신규 모듈/함수)")
        if has_wiki:
            lines.append("  ✏️  wiki git commit")

print(json.dumps({"systemMessage": "\n".join(lines)}))
