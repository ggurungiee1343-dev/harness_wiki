# Phase 1 · Phase 2 시스템 개선 설명서
> **작성일**: 2026-06-09
> **적용 대상**: Hermes v9.2+ (harness_agent.py, handlers/, modules/)
> **관련 파일**: `modules/optimistic_response.py`, `modules/memory_refinement.py`

---

## 개요 — 왜 Phase 1·2가 필요했는가

Hermes v9.2까지의 시스템은 **LLM 엔진·메모리 구조·보안·오케스트레이션**이 견고하게 완성된 상태였습니다. 그러나 두 가지 실사용 관점의 갭이 남아 있었습니다:

| 갭 | 증상 | 사용자 체감 |
|---|---|---|
| **응답 지연 체감** | `/ingest` 등 무거운 명령 실행 시 2~5초간 텔레그램이 무반응 | "봇이 죽었나?" → 중복 명령 발송 → 리소스 낭비 |
| **메모리 블로트** | L2 에피소드가 쌓이기만 하고 자동 정리 없음. 저장 전 판단 로직 부재 | LLM 컨텍스트에 무관한 기억이 주입 → 응답 품질 저하, 토큰 낭비 |

Phase 1은 **체감 속도**, Phase 2는 **기억 품질**을 해결합니다.

---

## Phase 1: 낙관적 응답 엔진 (Optimistic Response)

### 핵심 아이디어
Linear(프로젝트 관리 도구)의 UI 설계 원칙을 차용합니다:
> "사용자 액션 → 즉시 UI 반응 → 백그라운드에서 실제 처리 → 결과로 UI 갱신"

기존에는 `/ingest` 실행 시 "파일 처리 완료"까지 텔레그램이 멈춘 것처럼 보였습니다. 이제는:

```
사용자: /ingest
  ↓ (0.1초)
봇: ⏳ 🌱 Clippings → Wiki 이관 중...
  ↓ (백그라운드에서 실제 작업)
  ↓ (3초 후)
봇: ✅ ingest 완료 (3.2초) — 📊 처리: 7개
  + 별도 메시지로 상세 리포트 발송
```

### 구현 구조

```
modules/optimistic_response.py
├── OptimisticResponseEngine (모듈 싱글턴)
│   ├── initiate_action()     ← 즉시 피드백 + asyncio.create_task()
│   ├── _run()                ← 3회 자동 재시도 (2초 간격)
│   ├── _success_text()       ← 성공 메시지 포맷
│   ├── _error_text()         ← 실패 메시지 + recovery hint
│   └── last_failed()         ← /retry 용 조회
└── _recovery_hint()          ← 에러 유형별 복구 안내
```

### 적용된 명령어
| 명령어 | 변경 전 | 변경 후 |
|---|---|---|
| `/ingest` | 블로킹 대기 → 결과 1회 발송 | 즉시 피드백 → 백그라운드 → 메시지 편집 |
| `/ingest scan` | 동일 | 동일 패턴 적용 |
| `/ingest interrogate` | 동일 | 동일 패턴 적용 |
| `/retry` | 없음 (신규) | 마지막 실패 작업 정보 조회 |

### 시스템 발전 효과

**1. 체감 응답 속도 2~5배 향상**
실제 처리 시간은 동일하지만, 사용자가 "봇이 반응했다"고 인지하는 시점이 0.1초로 단축됩니다. 심리적 대기 시간이 사라집니다.

**2. 중복 명령 방지**
무응답 상태에서 사용자가 같은 명령을 반복 입력하는 문제가 해결됩니다. 진행 상태가 보이므로 중복 실행이 줄어듭니다.

**3. 장애 투명성**
3회 재시도 후에도 실패하면 에러 유형별 복구 힌트(권한/네트워크/파일/메모리)를 자동 제시합니다. 사용자가 "왜 실패했는지" 즉시 파악 가능합니다.

**4. 확장 가능한 패턴**
`/ingest` 외에도 `/delegate`, `/dreaming`, `/research` 등 무거운 명령어에 동일 패턴을 점진적으로 적용할 수 있습니다. `initiate_action()`에 `work_fn`만 전달하면 됩니다.

---

## Phase 2: 세밀한 메모리 (Memory Refinement)

### 핵심 아이디어
2026-06-05 "AI Agent Memory 개념 분석"에서 도출된 4대 갭을 해결합니다.
`bio_memory_engine.py`는 Lock Stack(수정 금지)이므로, **별도 래퍼 모듈**로 기존 엔진을 감싸는 설계입니다.

### 해결한 4대 갭

#### 갭 1: Forget 정책 부재 → `auto_forget()`
**문제**: L2 에피소드가 쌓이기만 하고 자동으로 정리되지 않았습니다. 에빙하우스 망각 곡선으로 `should_forget()`은 있었지만, 실제로 삭제를 실행하는 함수가 없었습니다.

**해결**: 보유율 15% 미만 + 7일 경과한 에피소드를 자동 식별하고, dry-run/confirm 2단계로 안전하게 정리합니다.

```
/memory forget          → 대상 목록만 표시 (삭제 안 함)
/memory forget confirm  → 실제 삭제 실행
```

연관 엣지(associations)도 함께 정리하여 고아 참조가 남지 않습니다.

#### 갭 2: Update 충돌 감지 → `check_conflict()`
**문제**: `save_important()`로 기억을 저장할 때, 이미 같은 주제의 기억이 L2/L3에 있는지 확인하지 않았습니다. 동일 정보가 중복 저장될 수 있었습니다.

**해결**: 저장 전에 키워드 2개 이상 겹치는 기존 기억을 탐지하여 충돌 후보를 반환합니다.

#### 갭 3: Writer self-question → `should_store()`
**문제**: "이 정보가 7일 후에도 쓸모있을까?"를 판단하는 로직이 없었습니다. 일시적 대화("ㅋㅋ", "테스트")도 L2에 승격될 수 있었습니다.

**해결**: 4가지 기준으로 자동 판단합니다:
- 중요도 3.0 미만 → 거부
- 20자 미만 → 거부
- 일시적 표현("지금", "방금", "임시", "테스트") 2개 이상 → 거부
- 유사 에피소드 3개 이상 → 중복 거부

#### 갭 4: Retrieval 품질 → `hybrid_recall()`
**문제**: `pre_query_context()`가 L2/L3만 검색하고, `semantic_index.db`(위키 전문검색 FTS5)와 연동되지 않았습니다. 위키에 답이 있어도 기억 검색에서 놓칠 수 있었습니다.

**해결**: `bio_memory.recall()` (L2 벡터+키워드+Spreading Activation) + `knowledge_indexer` FTS5+TF-IDF 결과를 병합하여 LLM 컨텍스트에 주입합니다.

```
harness_agent.py 메시지 처리 흐름:
  system prompt → style_profile → 대화 이력
  → wiki context
  → 🆕 hybrid_recall() (L2 기억 + FTS5 위키 검색 병합)
  → task context
  → 사용자 질문
```

### 구현 구조

```
modules/memory_refinement.py
├── auto_forget(dry_run)      ← Forget 정책
├── check_conflict(key, val)  ← 충돌 감지
├── should_store(text, role)  ← 저장 판단
├── hybrid_recall(query)      ← L2+FTS5 병합 검색
└── get_memory_health()       ← /memory health 출력
```

### 시스템 발전 효과

**1. 메모리 블로트 자동 방지**
`auto_forget()`이 에빙하우스 곡선에 따라 가치가 소멸된 에피소드를 자동 식별합니다. L2 파일이 무한정 커지는 것을 방지하여 LLM 컨텍스트 윈도우를 보호합니다.

**2. 저장 품질 향상**
`should_store()`가 일시적/중복/저중요도 정보의 저장을 사전에 차단합니다. L2에 "쓸모있는 기억만" 남게 됩니다.

**3. 검색 정확도 향상**
`hybrid_recall()`이 기존 L2/L3 기억 + 위키 FTS5 검색을 병합합니다. "위키에 있는데 기억에 없어서 답을 못하는" 상황이 해소됩니다.

**4. 운영 가시성**
`/memory health`로 평균 보유율, forget 대상 수, 저중요도 에피소드 수를 한눈에 파악할 수 있습니다.

---

## Phase 1 + Phase 2 시너지 효과

두 Phase를 결합하면 단순 합산 이상의 시스템 개선이 발생합니다:

```
[Phase 1 낙관적 응답]              [Phase 2 세밀한 메모리]
    즉시 피드백                          깨끗한 기억
    백그라운드 처리                       정확한 검색
    자동 재시도                          불필요 기억 정리
         │                                    │
         └─────────────┬──────────────────────┘
                       ▼
            [결합 시너지 효과]
    1. 빠른 응답 + 정확한 맥락 = 대화 품질 향상
    2. 자동 재시도 + 에러 패턴 기록 = 자가 치유 강화
    3. 메모리 경량화 + 토큰 절약 = API 비용 절감
    4. 투명한 상태 표시 + 건강 모니터링 = 운영 효율
```

### 수치 기대 효과

| 지표 | 변경 전 | Phase 1+2 적용 후 | 개선율 |
|---|---|---|---|
| 체감 응답 시간 | 2~5초 (블로킹) | 0.1초 (즉시 피드백) | **95% 감소** |
| L2 불필요 에피소드 | 수동 관리만 가능 | 자동 식별 + 2단계 정리 | **자동화** |
| 메모리 검색 범위 | L2/L3만 | L2/L3 + 위키 FTS5 | **2배 확장** |
| 장애 투명성 | 에러 메시지만 | 유형별 복구 힌트 자동 제시 | **자가 진단** |

---

## 관련 파일 목록

| 파일 | 유형 | 설명 |
|---|---|---|
| `modules/optimistic_response.py` | Phase 1 신규 | 낙관적 응답 엔진 |
| `modules/memory_refinement.py` | Phase 2 신규 | 메모리 정제 엔진 |
| `handlers/_file.py` | Phase 1 수정 | `/ingest` 3분기 낙관적 전환 |
| `handlers/_callbacks.py` | Phase 1 수정 | `/retry` 콜백 추가 |
| `handlers/_memory.py` | Phase 2 수정 | `/memory forget`, `/memory health` |
| `handlers/_ui.py` | 공통 수정 | `/help` 업데이트 |
| `harness_agent.py` | 공통 수정 | hybrid_recall 자동 주입 |
| `hermes_local.py` | Phase 1 수정 | `/retry` CommandHandler 등록 |

---

## 향후 확장 — Phase 3 (미구현)

Phase 3 "능동적 지능 (Proactive Intelligence)"은 Phase 1·2 위에 LLM 기반 패턴 증류와 선제적 제안을 추가하는 단계입니다. 설계 제안은 `HERMES3_MASTER_DEVELOPMENT_GUIDE.md`의 v9.4+ 섹션에 기록되어 있습니다.

---
*관리: `/Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/Phase1_Phase2_개선_설명서.md`*
*연관: `HERMES3_MASTER_DEVELOPMENT_GUIDE.md`, `Bio_Memory_Engine_Technical_Guide_v9.3.md`, `02_스크립트 정보.md`*
