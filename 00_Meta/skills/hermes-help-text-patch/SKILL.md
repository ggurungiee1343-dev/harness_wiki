---
name: hermes-help-text-patch
description: "Use when 텔레그램 봇 도움말(/help)에 명령어가 누락되었거나 줄바꿈이 깨진 경우. pyc 의존성 우회 monkey-patch 워크플로우."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [telegram, help, monkey-patch, pyc, hermes-local]
    related_skills: []
---

# 텔레그램 도움말 텍스트 패치 (hermes-help-text-patch)

## Overview

MJ님의 하이브리드 봇 시스템에서 `hermes_handlers.py`는 **pyc로만 동작**합니다 (`.py` 파일은 패딩 위장 파일, 읽기전용). 따라서 `cmd_help`의 도움말 텍스트를 수정하려면 **pyc를 직접 수정하지 않고** `hermes_local.py`에서 **HELP_TEXT 상수 + 오버라이드 + monkey-patch** 패턴을 사용해야 합니다.

## When to Use

- 텔레그램 `/help` 명령어나 "ℹ️ 도움말" 버튼에 명령어가 누락되었을 때
- 도움말 텍스트의 Markdown 줄바꿈(`\n`)이 깨져서 표시될 때
- 새 명령어를 추가했는데 help_text에 반영되지 않았을 때
- 스크립트 정보.md의 명령어 테이블과 help_text가 불일치할 때

## Workflow

### 1. 현재 HELP_TEXT 확인

```bash
cd ~/Applications/Mjauto/Scripts
python3 -c "
import sys; sys.path.insert(0, '.')
import hermes_handlers
import dis
code = hermes_handlers.cmd_help.__code__
for c in code.co_consts:
    if isinstance(c, str) and '명령어' in c:
        print(c)
        break
"
```

또는 이미 `hermes_local.py`에 HELP_TEXT 상수가 있다면 직접 확인:
```bash
python3 -c "
from hermes_local import HELP_TEXT
print(HELP_TEXT)
"
```

### 2. HELP_TEXT 상수 작성/수정 (`hermes_local.py`)

`main()` 함수 상단(handler 정의 직전)에 HELP_TEXT 상수 추가:

```python
HELP_TEXT = """🤖 **헤르메스 V2.5 명령어 가이드**

🔹 **인텔리전스 & 팩트체크**
• `/ask [질문]` — 기본 질문/위키 Q&A
• `/searchpaper [검색어]` — OpenAlex 학술 논문 검색
...
"""
```

**중요 규칙:**
- **반드시 실제 `\n` (escaped newline이 아님)**을 사용할 것. 삼따옴표 `"""`로 감싸면 자연스러운 줄바꿈이 들어감
- literal `\\n`이 있으면 텔레그램에서 줄바꿈 대신 `\n` 문자열이 출력됨
- 명령어는 `/help`나 "ℹ️ 도움말" 버튼을 통해 사용자에게 노출되므로 Markdown 형식 준수

### 3. cmd_help 오버라이드

HELP_TEXT 직후, handler 람다 정의 전에 `cmd_help`를 async function으로 오버라이드:

```python
async def cmd_help(update, context):
    if not await check_user(update): return
    await update.message.reply_text(HELP_TEXT, parse_mode='Markdown')
```

### 4. monkey-patch 추가 (버튼 핸들러용)

handler 람다 정의 직후, `_load_module('hermes_handlers')`가 캐싱된 시점에:

```python
# 🔧 hermes_handlers.cmd_help monkey-patch (ℹ️ 도움말 버튼에서도 HELP_TEXT 사용)
_load_module('hermes_handlers').cmd_help = cmd_help
```

이렇게 하면 "ℹ️ 도움말" 버튼 클릭 → `handle_text_message` → `LOAD_GLOBAL cmd_help` → monkey-patch된 버전 호출

### 5. 검증

```bash
cd ~/Applications/Mjauto/Scripts
python3 -c "
import sys; sys.path.insert(0, '.')
from hermes_local import HELP_TEXT
print(f'길이: {len(HELP_TEXT)}자')
print(f'실제 줄바꿈: {HELP_TEXT.count(chr(10))}')
print(f'literal backslash-n: {HELP_TEXT.count(\"\\\\\\\\n\")}')
print(f'/searchpaper 포함: {\"/searchpaper\" in HELP_TEXT}')
"
```

### 6. 봇 재시작

```bash
# 서비스 등록 확인
launchctl list | grep hermes.bot

# 재시작
launchctl kickstart -k gui/501/com.hermes.bot

# 또는 PID 직접 kill 후 재시작
launchctl bootout gui/501/com.hermes.bot 2>/dev/null
sleep 2
launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.hermes.bot.plist
sleep 3
pgrep -fl hermes_local
```

### 7. 문서 업데이트

- **스크립트 정보.md**: 명령어 테이블에 추가/수정된 명령어 반영
- **hot.md**: 변경 로그 추가 (날짜/시간, v5.x.x 버전 태그)

## Common Pitfalls

1. **`\n` vs `\\n` 혼동**: 삼따옴표 `"""`를 사용하면 줄바꿈이 자연스럽게 들어감. `\n`을 literal로 쓰면 텔레그램에서 개행 안 됨.
2. **monkey-patch 위치**: 반드시 `_load_module('hermes_handlers')`가 실행된 **후**에 patching 해야 함. handler 람다 정의 직후가 안전.
3. **pyc 캐시**: `hermes_handlers.py`는 pyc로 고정되어 있어 Python이 재컴파일하지 않음. `.py` 파일을 수정해도 적용 안 됨. 반드시 `hermes_local.py`에서 오버라이드.
4. **봇 재시작 필수**: monkey-patch와 HELP_TEXT는 프로세스 메모리에만 적용되므로 재시작 없이는 반영 안 됨.
5. **HELP_TEXT 길이**: 텔레그램 메시지 제한(4096자)을 넘지 않도록 주의. 현재 1298자로 충분.

## Verification Checklist

- [ ] HELP_TEXT에 literal `\\n`이 0개인지 확인
- [ ] HELP_TEXT에 빠진 명령어 모두 포함되었는지 확인
- [ ] `hermes_handlers.cmd_help`가 function 타입인지 확인 (오버라이드 성공)
- [ ] 봇 재시작 후 `/help` 명령어 정상 출력 확인
- [ ] "ℹ️ 도움말" 버튼 정상 동작 확인
- [ ] 스크립트 정보.md 명령어 테이블 업데이트 완료
- [ ] hot.md 변경 로그 업데이트 완료

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
