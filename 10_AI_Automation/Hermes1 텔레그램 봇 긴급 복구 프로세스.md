---
tags: [ingested, 10_AI_Automation, telegram-bot, launchd, python-runtime, macos, system-recovery, automation, troubleshooting]
description: "본 문서는 launchd 서비스 및 파손된 파이썬 실행 경로로 인해 발생한 장애의 최종 진단 결과와 100% 정상화를 위한 물리적 복구 절차를 요약한다. 파손된 파이썬 런타임 경로, macOS 확장 속성 오염, 스크립트 권한 차단이 주요 원인으로 분석되었다. 파일 권한 및 확장 속성 정화를 포함한 3단계 표준 복구 절차를 통해 시스템 데몬을 안전하게 정상화한다."
brief: "summary"
---

## 🛠️ Hermes1 텔레그램 봇 긴급 복구 프로세스 요약

이번 launchd 서비스 및 파손된 파이썬 실행 경로로 인해 발생한 장애의 최종 진단 결과와 100% 정상화를 위한 물리적 복구 트랙 요약입니다.

### 1. 장애 원인 분석 (Root Cause)

- **파손된 파이썬 런타임 경로**: 레거시 plist 내부의 Python3 실행 경로가 시스템 상에 존재하지 않는 `/usr/local/bin/python3`로 하드코딩되어 있어 `launchctl bootstrap` 시 물리적 `Input/output error (Failed: 5)`가 발생했습니다.
    
- **macOS 확장 속성 오염**: `com.hermes.bot.plist` 파일에 격리 마크(`@`)가 묻어있어 시스템 데몬이 인젝션을 거부했습니다.
    
- **스크립트 권한 차단**: 메인 구동 파일인 `hermes_local.py`가 소유자 전용 격리 권한(`-rw-------`)으로 설정되어 시스템 포크가 불가능했습니다.
    

### 2. 단계별 표준 복구 절차 (Standard Operating Procedure)

launchd 도메인 충돌이나 환경적 Block 현상이 발생했을 때, 프로세스를 안전하고 완벽하게 격리 기동하는 3단계 핵심 명령어 세트입니다.

#### [1단계] 파일 권한 및 확장 속성 정화

스크립트의 실행 권한을 표준화(755)하고 오염된 메타데이터를 제거하여 시스템 접근을 허용합니다.

Bash

```
chmod 755 /Users/bluesea/Applications/Mjauto/Scripts/hermes_local.py
xattr -c ~/Library/LaunchAgents/com.hermes.bot.plist
```

#### [2단계] 프로세스 및 락(Lock) 파일 강제 청소

기존에 좀비화되어 있거나 꼬여있는 fcntl 자원 선점(Occupied) 신호를 완전히 소멸시킵니다.

Bash

```
pkill -9 -f hermes_local.py
rm -f /Users/bluesea/Applications/Mjauto/Scripts/hermes_local.lock
```

#### [3단계] 독립형 백그라운드 강제 상주 (nohup 트랙)

launchctl 내부 세션이 잠겨있을 때 이를 우회하여 영구 안착시키는 가장 견고한 실행 명령어입니다.

Bash

```
nohup $(which python3) -u /Users/bluesea/Applications/Mjauto/Scripts/hermes_local.py > /Users/bluesea/Applications/Mjauto/Scripts/hermes_launchd.log 2> /Users/bluesea/Applications/Mjauto/Scripts/hermes_launchd.error.log &
```

### 3. 복구 상태 검증 및 모니터링

정상 기동 후 백그라운드 소켓이 올바르게 할당되었는지, 예외 에러 스트림이 없는지 팩트 체크하는 도구입니다.

- **상주 PID 확인**: `ps aux | grep hermes_local.py | grep -v grep`
    
- **런타임 에러 스트림 추적**: `tail -f /Users/bluesea/Applications/Mjauto/Scripts/hermes_launchd.error.log`
    

### 📅 재발 방지 행동 지침 및 장부 갱신 (헌법 §3.2 및 §4.1.3)

- **지침 누적**: 향후 봇 기동 프로토콜 가동 시, `ProgramArguments` 단의 실행 파일 절대 경로(`REAL_PYTHON`) 유효성을 사전에 교차 체크(`which python3`)하도록 자가 행동 지침에 박아 넣었습니다.
    
- **장부 마킹**: 헌법 수렴 정책에 따라 `01_hot.md` 및 `05_시스템 상태.md`에 **`PID 88993 (nohup)`** 가동 상태와 결정 맥락(Why) 기입을 정상 완료했습니다.