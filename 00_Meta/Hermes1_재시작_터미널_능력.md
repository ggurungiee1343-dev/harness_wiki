# 헤르메스봇 1 — 재시작 및 터미널 능력 명세

**최종 업데이트:** 2026-05-31 14:30

---

## 개요

헤르메스봇 1(Hermes1)에는 두 가지 특수 명령어가 있다: **`/restart_bot`** (봇 자체 재시작)과 **`⚙️ /exec [명령어]`** (임의 터미널 명령 실행). 이 문서는 이 두 기능의 구현 구조와 작동 방식을 기록한다.

---

## 1. 🔄 `/restart_bot` — 봇 자체 재시작

### 목적
Telegram 채팅에서 `/restart_bot` 명령어를 보내면 Hermes1 봇 프로세스가 자체적으로 종료되고, launchd가 자동으로 재시작한다.

### 구현 구조

| 계층 | 파일 | 역할 |
|:---|:---|:---|
| 핸들러 함수 | `~/Applications/Mjauto/Scripts/handlers/_system.py:679-704` | `cmd_restart_bot()` 정의 — `sys.exit(0)` 호출 |
| Import 게이트 | `~/Applications/Mjauto/Scripts/handlers/__init__.py` | `from ._system import cmd_restart_bot` — 네임스페이스 노출 |
| 명령어 등록 | `~/Applications/Mjauto/Scripts/hermes_local.py` | `CommandHandler('restart_bot', ...)` + BotCommand("restart_bot", "봇 재시작") |
| 프로세스 매니저 | `~/Library/LaunchAgents/com.hermes.bot.plist` | `KeepAlive → CrashedOnly` — 종료 후 5초 내 자동 재시작 |

### 동작 흐름

```
사용자 → /restart_bot
  → PTB dispatcher → cmd_restart_bot()
  → print("---RESTARTED---")
  → sys.exit(0)
  → launchd 감지 (exit code 0)
  → ThrottleInterval 5초 후 다시 start
  → 봇이 새 PID로 재시작됨
```

### 버그 기록 (2026-05-31 수정 완료)
- **버그**: `cmd_restart_bot`이 `handlers/__init__.py`에 import 누락 → Telegram에서 `/restart_bot`이 "Unknown command"로 처리됨.
- **원인**: 다른 AI가 `_system.py`에 함수 추가했지만 `__init__.py` import 줄을 누락함.
- **수정**: `from ._system import cmd_restart_bot` 한 줄 추가.

---

## 2. ⚙️ `/exec [명령어]` — 임의 터미널 명령 실행

### 목적
Telegram 채팅에서 임의의 Bash/Python 명령어를 실행한다. AI가 자율적으로 에러 복구를 수행하는 고급 실행 체계.

### 구현 구조

| 계층 | 파일 | 역할 |
|:---|:---|:---|
| 핸들러 함수 | `~/Applications/Mjauto/Scripts/handlers/_system.py:707-740` | `cmd_exec()` 정의 |
| Import 게이트 | `~/Applications/Mjauto/Scripts/handlers/__init__.py` | `from ._system import cmd_exec` |
| 명령어 등록 | `~/Applications/Mjauto/Scripts/hermes_local.py` | `CommandHandler('exec', ...)` + BotCommand("exec", "터미널 명령 실행") |
| 실행 엔진 | `~/Applications/Mjauto/Scripts/harness_agent.py` | `execute_bash_command()` — 자율 에러 복구 (재시도 3회) |
| 보안 | 없음 (화이트리스트 없음) | 모든 명령 실행 가능, 하네스 AI가 위험도 판단 |

### 동작 흐름

```
사용자 → /exec ls -la ~/Applications
  → PTB dispatcher → cmd_exec(args, ...)
  → executor.execute_bash_command(command, ...)
    → subprocess.run() 실행
    → 실패 시 최대 3회 재시도 (에러 복구)
    → stdout + stderr + exit code 반환
  → Telegram으로 결과 전송 (최대 4000자, 초과 시 파일)
```

### 이전 아키텍처: `/run` 명령어 (2026-05-31 제거됨)

원래 `cmd_run_cmd()` + `ALLOWED_CMDS` 화이트리스트 기반으로 제한된 명령만 실행 가능했다.

**제거 사유:**
- `ALLOWED_CMDS`가 제한적이어서 사용자 요구사항(임의 명령 실행)에 부적합
- `/exec`가 이미 자율 에러 복구형으로 구현되어 중복
- AI가 화이트리스트 외 명령을 시도하면 실패 → 사용자 불편

**제거한 파일:**
- `handlers/_system.py`: `ALLOWED_CMDS` 딕셔너리 + `cmd_run_cmd()` 함수 전체 제거
- `hermes_local.py`: `/run` CommandHandler 등록 + lambda 바인딩 제거

**현재**: `/exec` 하나로 통일 — 화이트리스트 제한 없음, AI 자율 판단 기반.

---

## 3. 🧩 의존성 체인

```
hermes_local.py (진입점)
  └── handlers/__init__.py (import 게이트)
        ├── _base.py (기본 유틸리티: _reply_long, _edit_or_send_long)
        ├── _system.py (cmd_exec, cmd_restart_bot, cmd_status 등)
        └── ... (다른 7개 핸들러)
```

- `harness_agent.py`: `/exec`의 실제 Bash 실행 엔진. 자율 에러 복구 로직 포함.
- `com.hermes.bot.plist`: `/restart_bot`의 재시작을 보장하는 launchd 설정. `ThrottleInterval=5`로 재시작 지연 방지.

---

## 4. ⚠️ 주의사항

1. **`/exec`는 보안 제한이 없다** — Telegram에 접근 권한이 있는 사람이라면 누구든 서버에서 임의 명령 실행 가능. Bot Token이 노출되지 않도록 주의.
2. **`/restart_bot` 실행 직후 봇이 3-5초간 응답 불가** — launchd가 프로세스를 재시작하는 동안 메시지 손실 가능.
3. **재시작 후 메모리 초기화** — `/restart_bot`은 프로세스 재시작이므로 런타임 메모리(변수, 캐시)가 모두 사라짐. 영구 메모리(Memory/User Profile)는 유지됨.
4. **launchd KeepAlive**는 `CrashedOnly` 모드 — 정상 종료(successful exit) 시 재시작 안 함. `/restart_bot`은 `sys.exit(0)`이라 정상 종료로 launchd가 재시작하는 구조.
