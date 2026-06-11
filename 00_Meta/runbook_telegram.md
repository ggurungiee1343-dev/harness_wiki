# 텔레그램 봇 운영 (Runbook)

## 기본 정보

- **봇 이름**: 헤르메스 V2.5
- **진입점**: `~/Applications/Mjauto/Scripts/hermes_local.py`
- **Launchd**: `com.hermes.bot`
- **실행 방식**: Launchd foreground (플랫폼 런처 래퍼 미사용)
- **폴링 모드**: python-telegram-bot `Application.run_polling()`

## 명령어 목록

도움말: `/help` 또는 키보드의 `ℹ️ 도움말` 버튼

## 주요 기능

### 인텔리전스 & 팩트체크
- `/ask`, `/cove` — 질문 답변 및 심층 분석
- `/web`, `/search`, `/readweb` — 웹 검색
- `/searchpaper` — 학술 논문 검색 (OpenAlex API)
- `/clip` — 클립보드 분석
- `/exec` — 자율 에러 복구형 Bash 실행

### 메모리 & 학습
- `/memory`, `/memory_search`, `/memory_dream` — Bio-Memory 3계층
- `/dreaming` — 일일 Journal/Memory/hot.md 자동 분배

### 하네스 컨트롤
- `/harness`, `/hdod`, `/hstatus`, `/hrollback`

### 파일 관리
- `/create`, `/read`, `/move`, `/copy`

### 모니터링
- `/recent`, `/status`

## 봇 재시작 시 주의사항

1. 봇 재시작 시 등록된 CommandHandler는 유지됨 (코드 레벨)
2. 단, 재시작 중 전송된 메시지는 유실됨 (polling 중단)
3. `/searchpaper` 등 특정 명령어가 소실된 경우 → 소스 코드 확인 후 재등록

## 문제 해결

- **응답 없음**: launchctl로 프로세스 상태 확인
- **CommandHandler 미등록**: hermes_local.py의 `app.add_handler()` 확인
- **API 호출 실패**: `.env` 파일의 토큰 확인

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*

---

## 2026-06-03 업데이트 (명령어 전체 현행화)

### 추가된 주요 명령어 (HELP_TEXT 완전판 기준)
- `/research [유형]` — local/web/deep/stats/xref/classify/timeline
- `/paper [명령]` — humanize/draft/review
- `/memory` — L1/L2/L3 Bio-Memory 상태 + L2 자동 백업
- `/memory_dream` — Dreaming V2 강제 실행 (PEMS 수렴=정상)
- `/goal [목표]` — 장기 목표 설정
- `/kanban`, `/audit`, `/secreview`, `/model`, `/reduce` 등 추가

### 봇 재시작 (현행)
```bash
# launchd 이용 (권장)
pkill -f hermes_local.py   # → launchd KeepAlive로 5초 내 자동 재시작

# 또는 명시적
launchctl stop com.hermes.bot && sleep 2 && launchctl start com.hermes.bot
```

*최종 업데이트: 2026-06-03 19:05 — 명령어 전체 현행화*
