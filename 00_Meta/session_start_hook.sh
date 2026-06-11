#!/bin/bash
# SessionStart Hook v2 — 스마트 컨텍스트 주입
# 01_hot.md 에서 "현재 진행 중" 항목만 추출 (최근 3개)
# 05_시스템 상태.md 에서 최근 변경 1개 헤더+요약만 추출

HOT="$HOME/Applications/Mjobsidian/wiki/00_Meta/01_hot.md"
STATUS="$HOME/Applications/Mjobsidian/wiki/00_Meta/05_시스템 상태.md"

# 01_hot.md: ## 또는 ### 헤더 단위로 최근 3개 섹션만 추출
HOT_CONTENT=""
if [ -f "$HOT" ]; then
  HOT_CONTENT=$(python3 -c "
import re, sys
text = open('$HOT', encoding='utf-8').read()
# ## 또는 ### 로 시작하는 섹션 분리
sections = re.split(r'(?=^#{1,3} )', text, flags=re.MULTILINE)
# 비어있지 않은 섹션만, 최근 3개
sections = [s.strip() for s in sections if s.strip()][-3:]
print('\n\n'.join(sections)[:800])
" 2>/dev/null | tr '\n' '|' | sed 's/"/\\\\"/g')
fi

# 05_시스템 상태.md: 가장 최근 ## 2026- 섹션 1개만 (헤더+테이블 첫 5줄)
STATUS_CONTENT=""
if [ -f "$STATUS" ]; then
  STATUS_CONTENT=$(python3 -c "
import re
text = open('$STATUS', encoding='utf-8').read()
# 가장 최근 ## 2026 섹션 찾기
matches = list(re.finditer(r'^## 2026', text, re.MULTILINE))
if matches:
    start = matches[-1].start()
    # 다음 ## 까지 또는 400자
    chunk = text[start:start+400].strip()
    print(chunk)
" 2>/dev/null | tr '\n' '|' | sed 's/"/\\\\"/g')
fi

python3 -c "
import json
hot = '''${HOT_CONTENT}'''.replace('|', '\n')
status = '''${STATUS_CONTENT}'''.replace('|', '\n')
ctx = (
    '=== 세션 시작 컨텍스트 (자동) ===\n\n'
    '[현재 진행 작업 — 01_hot.md 최근 3섹션]\n' + hot +
    '\n\n[최근 시스템 변경 — 05_시스템 상태.md]\n' + status +
    '\n\n=== 끝 ==='
)
print(json.dumps({'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': ctx}}))
"
