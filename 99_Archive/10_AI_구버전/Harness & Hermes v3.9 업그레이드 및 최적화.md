---
tags: [ingested, 10_AI_Automation]
date: 2026-05-21 13:38:26
ingested_at: 2026-05-21 21:42:48
---

# Walkthrough - Harness & Hermes v3.9 Upgrade

## 변경 사항 및 작업 요약

### 1. `git_manager.py` 복구 및 의존성 오류 해결
* 백업 및 리팩토링 과정에서 유실되었던 `git_manager.py` 파일을 `Scripts/modules/git_manager.py` 경로에 재생성하고 클래스 기반 인터페이스로 구현하였습니다.
* 이로 인해 `harness_agent.py` 초기화 시 발생하던 모듈 누락(ImportError) 문제가 완전히 해결되었습니다.

### 2. `hermes_context_builder.py` 비대화 방지 필터 알고리즘 도입
* **문제:** `HERMES.md` 파일에 누적 규칙이 많아질 경우 LLM 프롬프트가 과부하되어 속도 지연 및 API 요금 낭비 우려가 발생할 수 있습니다.
* **해결:** `MAX_CONTEXT_CHARS(4000자)`를 초과하는 `HERMES.md`는 자동으로 마크다운 헤더(`#`) 및 규칙 리스트(`-`, `*`, 번호), 코드 블록만 선별하는 `_slim_context` 요약 필터를 거치게 하여 토큰 주입량을 철저하게 통제했습니다.

### 3. `harness_agent.py` 루프 개선
* 에이전틱 연쇄 반응(Agentic Chain)을 원활하게 처리할 수 있도록 루프 제한을 기존 2회에서 3회로 확대했습니다.
* `[SAVE]` 태그가 절대 경로와 상대 경로를 안전하게 판별하여 올바른 파일 매니저 및 로컬 디렉터리에 파일을 안전하게 저장하도록 강화했습니다.

### 4. 메타 문서 갱신
* [[[파일_디렉터리_구조_및_상호연결성_점검결과]].md](file:///Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/[[파일_디렉터리_구조_및_상호연결성_점검결과]].md) 신규 생성.
* [hot.md](file:///Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/hot.md), [스크립트 정보.md](file:///Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/스크립트 정보.md), [modules/HERMES.md](file:///Users/bluesea/Applications/Mjauto/Scripts/modules/HERMES.md)의 버전을 `v3.9`로 일제히 업데이트하였습니다.


---
*정리 완료 시간: 2026-05-21 21:42:48* (Harness Ingest Auto-Linker 가동)

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
