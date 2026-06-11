---
tags: [scanned, 10_AI_Automation]
---


# Harness V2.5 자율 기지 구축 마스터 플랜

박사님이 서울 본진(맥 스튜디오)으로 무사히 복귀하심에 따라, 그동안 텔레그램 상에서 논의하고 구상해 두었던 **Harness V2.5 자율 기지 구축** 작업을 차근차근 안전하게 실행하기 위한 종합 이행 계획서입니다.

---

## 🎯 최종 목표
1. **보안 및 환경 격리 (.env):** 하드코딩된 토큰과 키들을 완전히 숨기고 `~/.hermes/.env`에서 동적으로 로드합니다.
2. **5대 부서 격리 및 폴더 빌딩:** 스크립트들을 전용 모듈형 경로(`~/.hermes/skills/`)로 이동하여 아키텍처 규칙을 확립합니다.
3. **Meta CoVe(검증 사슬) 도입:** 소형 로컬 LLM인 Gemma4 26B의 환각률을 0%에 수렴시키기 위한 동적 팩트체크 검증 프로세스를 구축합니다.
4. **자율 교정 및 진화 루프:** 에러 시 자동 명령 수정 루프 및 Unsorted 지식 누적 시 알림 시스템을 가동합니다.

---

## 🏗️ 단계별 세부 이행 계획

### [1단계] 기지 기초 공사 (인프라 및 보안 격리)
- **목표:** 디렉토리 뼈대를 세우고 민감 정보를 격리합니다.
- **작업 내용:**
  1. 마스터 컨트롤 룸(`~/vps-agents/`) 및 5대 부서 격리 공간(`~/srv/`) 자동 개설:
     * `~/srv/brain`, `~/srv/knowledge`, `~/srv/gardening`, `~/srv/devops`, `~/srv/academic` 생성
     * `~/.hermes/skills/` 하위 모듈 저장 폴더들 생성
  2. 보안 격리:
     * `/Users/bluesea/.hermes/.env` 파일 내부의 텔레그램 토큰 설정에 실제 박사님의 토큰 및 허용 ID 기록 및 동적 로딩 준비 (`python-dotenv` 활용)

### [2단계] 소스코드 방 배정 (부서화 및 모듈화)
- **목표:** 기존 `/Users/bluesea/Applications/Mjauto/Scripts/modules/`에 흩어져 있던 스크립트들을 정식 아키텍처 규격에 따라 격리 이사시킵니다.
- **이사 갈 위치 매핑 테이블:**
  | 파일명 | 역할 | 정식 이사 장소 |
  | :--- | :--- | :--- |
  | **hermes_local.py** | 메인 관제탑 | `~/vps-agents/` 및 `/Users/bluesea/hermes/` 동기화 |
  | **hybrid_router.py** | 로컬/클라우드 라우터 | `~/.hermes/plugins/hybrid_router.py` [신규 생성] |
  | **system_monitor.py** | 자원 모니터 | `~/.hermes/cron/system_monitor.py` |
  | **cognitive_engine.py** | 요약/추론 | `~/.hermes/skills/brain/cognitive/scripts/cognitive_engine.py` |
  | **wiki_manager.py** | 옵시디언 RAG | `~/.hermes/skills/knowledge/wiki/scripts/wiki_manager.py` |
  | **ingest_engine.py** | 자동 분류기 | `~/.hermes/skills/gardening/ingest/scripts/ingest_engine.py` |
  | **executor.py** | Bash 실행기 | `~/.hermes/skills/devops/executor/scripts/executor.py` |

### [3단계] 지능 고도화 및 신규 스킬 장착 (Meta CoVe)
- **목표:** Gemma4 26B의 답변 신뢰성을 극대화하기 위해 독립 교차 검증 루프를 구성합니다.
- **작업 내용:**
  1. `~/.hermes/skills/cove_verifier/SKILL.md` 신설하여 4단계 검증 제약 조건 정의.
  2. `verification_engine.py`를 신설하여 `wiki_manager` 및 `memory_engine`과 연동하는 실시간 교차 검증 파이프라인 구현.

### [4단계] 코어 기능 업그레이드 (Self-Correction & UI)
- **목표:** 에러 대처 및 사용자 경험을 혁신합니다.
- **작업 내용:**
  1. `executor.py`에 자율 복구 루프 적용: 실행 시 `stderr` 발생 시 Gemma4에게 에러 해결 방안 및 명령 재수정을 요청하여 최대 3회 자동 재도전.
  2. `hermes_local.py`에서 `dotenv`를 통해 보안키를 로드하도록 수정하고 버튼식 매크로 리스트 준비.

---

## 🔍 Proposed Changes

### [NEW] `~/.hermes/skills/cove_verifier/SKILL.md`
- Meta CoVe (검증 사슬) 제약 가이드를 기술합니다.

### [NEW] `~/.hermes/skills/brain/cognitive/scripts/verification_engine.py`
- 실시간 RAG 및 기억 교차 대조를 수행할 검증 브레인 엔진을 구현합니다.

### [NEW] `~/.hermes/plugins/hybrid_router.py`
- LM Studio 연결 상태 감지 및 Failover 라우터 뼈대 구현.

### [MODIFY] `/Users/bluesea/hermes/hermes_local.py`
- 하드코딩된 토큰을 지우고 `~/.hermes/.env`로부터 값을 동적 로드하도록 수정합니다.
- `/move`, `/copy`, `/read` 등에 `wiki_manager` 검색 및 `verification_engine` CoVe 파이프라인을 유기적으로 연동합니다.

---

## 🧪 Verification Plan

### Automated / Manual Verification
1. **디렉토리 무결성 확인:** `ls -R ~/srv/` 및 `ls -R ~/.hermes/skills/` 실행으로 올바른 뼈대 구축 확인.
2. **보안 검증:** `hermes_local.py`를 가동하여 하드코딩 토큰 없이 정상 기동되는지 확인.
3. **CoVe 기능 테스트:** 텔레그램으로 복잡한 사실 관계 질문을 던진 뒤 백그라운드에서 검증 질문 분할 및 위키 교차 검색이 트리거되는지 로그 모니터링.
4. **자율 복구 테스트:** 고의로 잘못된 리눅스 명령을 실행하여 `executor`가 자동으로 에러를 수정해 재시도하는지 확인.

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
