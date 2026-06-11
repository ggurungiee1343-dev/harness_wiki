---
tags: [scanned, 10_AI_Automation]
---


# Hermes 파일 이동 및 디렉토리 통합 계획

박사님의 요청에 따라 분산되어 있던 관리 포인트를 `/Users/bluesea/Applications/Mjauto/Scripts` 로 일원화하기 위한 작업 계획입니다.

## 1. 파일 이동 (Migration)
현재 `~/hermes/` 디렉토리에 있는 핵심 파이썬 파일들을 목표 디렉토리로 이동합니다.
**이동 대상 파일:**
- `hermes_local.py`
- `hermes_handlers.py`
- `hermes_harness.py`
- `hermes_file_ops.py`
- `web_agent_module.py`
- `.md` 파일 (존재할 경우)
- `start_bots.sh` (통합 관리를 위해 같이 이동하는 것을 권장합니다)

## 2. 경로 및 설정 파일 업데이트
파일 이동에 따라 기존에 `/Users/bluesea/hermes`를 바라보던 하드코딩된 경로들을 일괄 수정합니다.
- **`hermes_local.py`**: 내부에 선언된 `_HERMES_DIR` 등의 시스템 경로 업데이트
- **`start_bots.sh`**: `hermes_local.py` 실행 경로를 Mjauto/Scripts 하위로 수정
- **`com.hermes.bot.plist`**: `launchd` 데몬이 바라보는 실행 스크립트 경로(`start_bots.sh`), 로그 파일 경로, 그리고 `WorkingDirectory` 업데이트

## 3. 데몬 재시작 및 안정성 점검
1. 기존 백그라운드 프로세스 및 `launchd` 데몬 언로드 (`launchctl unload`)
2. 이동 및 코드 수정 완료 후 데몬 리로드 (`launchctl load`)
3. 시스템 재기동 후 텔레그램 정상 연결 확인

> [!IMPORTANT]
> **User Review Required (사용자 피드백 필요)**
> `~/hermes/` 디렉토리에 있는 **`start_bots.sh`** 스크립트와 **`로그 파일(.log)`** 들도 함께 `Mjauto/Scripts` 디렉토리로 이동시킬까요? 아니면 쉘 스크립트와 로그는 기존 폴더에 남겨두는 것이 좋으신가요? (모든 걸 한 곳에서 관리하신다면 같이 이동하는 것을 추천합니다.)

확인해주시면 바로 데몬을 내리고 이전을 시작하겠습니다!

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
