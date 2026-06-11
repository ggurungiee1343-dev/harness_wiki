# 🧠 헤르메스3 기능 백과사전
> **목적**: Hermes3 시스템에 적용된 모든 기술·개념·기능을 쉽게 찾아볼 수 있는 참조 문서  
> **관리 방침**: 새로운 기능이 추가되거나 질문이 생길 때마다 이 파일에 계속 추가하여 백과사전처럼 키움  
> **최초 작성**: 2026-05-31  

---

## 📖 목차

| 분류 | 항목 |
|------|------|
|| 🏛️ 핵심 철학 | [카파시 다이어트 철학](#-카파시-다이어트-철학) · [12-Factor Agents](#-12-factor-agents) · [Stateless Reducer 패턴](#-stateless-reducer-패턴) |
|| 🧩 핵심 모듈 | [AgentContext](#-agentcontext) · [HermesCoreReducer](#-hermescorereducer) · [DecisionAgent](#-decisionagent) · [ExecutionAgent](#-executionagent) · [KnowledgeAgent](#-knowledgeagent) · [/reduce 명령어](#-reduce-명령어) · [ArchitecturalJudgmentGate](#-architecturaljudgmentgate) · [SelfImprovingAgent (SIA)](#-selfimprovingagent-sia) · [MonitoringEngine](#-monitoringengine) · [ModelLoadBalancer](#-modelloadbalancer) · [Tag/Exec 보안 3중 필터](#-tagexec-보안-3중-필터) · [PermissionBridge](#-permissionbridge) |
|| 🧠 지식 관리 | [DreamingV2 (FluxMem+SKILLOPT)](#-dreamingv2-fluxmemskillopt) · [PEMS 점수](#-pems-점수) · [Rejected-Edit Buffer](#-rejected-edit-buffer) · [Validation Gate](#-validation-gate) · [태깅 자동화 vs Karpathy LLM Wiki](#-태깅-자동화-시스템-vs-karpathy-llm-wiki--두-지식-시스템의-차이) · [Save vs Organize & Inbox Deferral](#-save-vs-organize--inbox-deferral) |
| ⚡ 성능 최적화 | [Context Hash Cache](#-context-hash-cache) · [KV 캐시 방어선](#-kv-캐시-방어선) · [WAL 모드](#-wal-모드) · [TTL 기반 캐시 만료](#-ttl-기반-캐시-만료) |
|| 🔗 연결 시스템 | [Pub-Sub 이벤트 버스](#-pub-sub-이벤트-버스) · [TagLinker](#-taglinker) · [AI Gateway (3-way Failover)](#-ai-gateway-3-way-failover) · [Graphify (지식 그래프)](#-graphify-지식-그래프) · [adapters.py](#-adapterspy) · [switch-model](#-switch-model-모델-전환-도구) |
| 📁 데이터 저장 | [SQLite WAL 워크벤치](#-sqlite-wal-워크벤치) · [hot.md (실시간 스트림)](#-hotmd-실시간-스트림) · [Mjobsidian 보관소](#-mjobsidian-보관소) |
| 🚫 보류 기능 | [Multi-Agent Orchestration](#-multi-agent-orchestration-보류) · [Advanced RAG / sqlite-vec](#-advanced-rag--sqlite-vec-보류) · [Auto-Refactoring](#-auto-refactoring--self-healing-보류) |

---

## 🏛️ 핵심 철학

---

### 📌 카파시 다이어트 철학

> **한 줄 요약**: 거대한 벡터 DB 대신, 사람이 읽을 수 있는 순수 마크다운 `.md` 파일로 지식을 관리하여 토큰과 메모리를 극도로 압축한다.

**유래**: 안드레이 카파시(Andrej Karpathy) — OpenAI 공동창업자, Tesla AI 전 디렉터

**핵심 아이디어**:
- AI가 기억하는 방식이 고가의 벡터 DB가 아닌, 사람이 편집할 수 있는 `.md` 텍스트 파일 기반이어야 한다.
- 텍스트가 짧고 핵심적일수록(압축적일수록) LLM이 소비하는 토큰이 줄어들고, 응답 속도가 빨라진다.

**Hermes3에 적용된 방식**:
```
옵시디언(Mjobsidian) 마크다운 보관소
   └── 대화 요약본, 결정 기록, 오류 추적 등을 .md로 저장
   └── 불필요한 군살이 많아질수록 PEMS 점수가 낮아지도록 수식 설계
   └── Caveman 모드: 질문을 LLM에 보내기 전 극도로 압축
```

**핵심 효과**:
- 토큰 사용량 **95% 절감**
- 부팅 시간 **2.5초 이하** 유지
- 유저가 직접 메모장으로 AI의 기억을 편집 가능

---

### 📌 12-Factor Agents

> **한 줄 요약**: AI 에이전트를 "소프트웨어 공학적으로 올바르게" 만드는 12가지 황금 원칙.

**유래**: Heroku의 "12-Factor App" 철학을 AI 에이전트에 맞게 재해석한 현대 설계 원칙

**Hermes3 적용 현황**: 12/12 완벽 달성 (v9.1 기준)

| Factor | 원칙 | Hermes3 적용 방법 |
|--------|------|--------------------|
| **1** | NL→JSON 변환 | DecisionAgent가 자연어 명령을 구조화된 JSON으로 변환 |
| **4** | Tool JSON 스키마 | 모든 명령어가 표준 JSON 형식으로 처리 |
| **6** | Pause/Resume | `execution_state` 플래그로 중단/재개 지원 |
| **7** | Pub-Sub 버스 | TagLinker 이벤트 버스 (느슨한 결합) |
| **8** | 중앙화된 제어 흐름 | ExecutionAgent의 단일 `match/case` 분기 |
| **12** | 무상태(Stateless) | AgentContext 불변 객체 + 결과를 DB에 저장 |

---

### 📌 Stateless Reducer 패턴

> **한 줄 요약**: 입력이 같으면 출력이 항상 같은 "순수 함수" 방식으로 봇을 설계하여 버그 재현성을 100%로 만든다.

**유래**: 함수형 프로그래밍(Functional Programming)의 Redux 패턴

**핵심 원리**:
```
입력 (AgentContext) ──► 처리 (reduce 함수) ──► 출력 (응답 텍스트)
         ↑ 불변(frozen)                              ↑ 동일 입력 = 동일 출력
```

**기존 방식(v8.x)과의 차이**:
| 항목 | 기존 (v8.x) | v9.0+ |
|------|------------|-------|
| 상태 관리 | 15개 핸들러가 각자 상태 보유 | 단일 AgentContext로 통합 |
| 버그 재현 | 거의 불가능 | AgentContext만 저장하면 100% 재현 |
| 테스트 난이도 | 매우 높음 | 극도로 낮음 (입력/출력만 비교) |
| 코드량 | ~2,500줄 | ~500줄 (-80%) |

---

### 📌 분할 명령어 연구 워크플로우

> **한 줄 요약**: 통합 파이프라인(All-in-One 명령어) 대신, 검색→분석→저장을 각각의 독립 명령어로 분할하여 각 단계마다 결정을 내리는 연구 방식. 1인 연구 환경에 최적화된 워크플로우 설계 철학.

**배경**: Claude Code + NotebookLM + Obsidian 조합에서 제안된 `/yt-pipeline` 같은 통합 파이프라인은 검색→분석→저장을 한 번에 처리한다. 그러나 이 방식은:
- 모든 검색 결과를 무조건 저장 (쓰레기 누적)
- 한 단계 에러 시 전체 재시도
- 중간 검증/선별 불가
- 팀 단위 mass research 전용

**Hermes3의 결정**: Hermes3는 1인 환경이므로 **분할 명령어 체계**가 더 적합하다.

**핵심 원리**:
```
🧭 검색 (/searchpaper)
    ↓ "볼만하네?"
📄 확인 (/ask + URL)
    ↓ "저장할 가치 있다"
💾 저장 (/ingest → 40_Thesis)
    ↓ "심층 분석 필요"
🔬 분석 (/reduce)
    ↓ "종합 필요"
🔗 비교 (/paper bundle + compare)
```
각 단계별 ✋ **STOP 결정점**이 있어 토큰과 저장 공간을 절약한다.

**통합 파이프라인 vs 분할 명령어**:

| 구분 | 통합 파이프라인 | 분할 명령어 (Hermes3) |
|------|----------------|----------------------|
| 적합 환경 | 주 20건 mass research, 무조건 저장 | 필요할 때만, 선별 저장 |
| 중간 결정 | ❌ 불가 (자동 진행) | ✅ 각 단계 검토 후 결정 |
| 에러 격리 | ❌ 한 단계 실패 = 전체 재시도 | ✅ 해당 단계만 재시도 |
| 코드 복잡도 | 높음 (분기/상태 관리) | 낮음 (각 명령어 독립) |
| 투명성 | 블랙박스 | ✅ 각 단계 결과 확인 가능 |

**관련 문서**: [[논문_워크플로우_가이드]] Section 2.5

---

## 🧩 핵심 모듈

---

### 📌 AgentContext

> **한 줄 요약**: 봇이 질문을 처리하는 동안 필요한 모든 정보를 담은 "불변 명함". 처리 중에 절대 바뀌지 않는다.

**파일 위치**: `modules/core_reducer.py`

**구성 요소**:
```python
@dataclass(frozen=True)  # ← frozen=True 가 핵심! 불변 보장
class AgentContext:
    user_query:      str    # 유저가 보낸 원문 질문
    source_channel:  str    # 어디서 왔는가? (telegram/slack/webhook...)
    hot_context:     str    # 현재 관련된 마크다운 요약 (메모리 역할)
    rejected_buffer: tuple  # 과거에 실패한 시도 목록 (오답 노트)
    pems_score:      float  # 지식 성숙도 점수 (0.0~1.0)
    execution_state: str    # 현재 상태 (RUNNING / PAUSED / DONE / ERROR)
    session_id:      str    # 이 요청의 고유 ID
```

**왜 불변(frozen)인가?**  
함수 중간에 데이터가 몰래 바뀌면 버그를 추적하기 불가능해진다. 불변으로 만들면 입력값이 보장되므로 테스트가 쉬워지고 버그가 줄어든다.

---

### 📌 HermesCoreReducer

> **한 줄 요약**: Hermes3의 두뇌. AgentContext를 받아 Decision → Execution → Knowledge 3단계 파이프라인을 조율하는 오케스트레이터.

**파일 위치**: `modules/core_reducer.py`

**처리 흐름**:
```
유저 질문
   │
   ▼
AgentContext 생성 (불변 명함)
   │
   ▼
① DecisionAgent.decide()   → "이 질문은 웹 검색이야? 태그야? 그냥 답변이야?"
   │
   ▼
② ExecutionAgent.execute()  → 결정된 액션을 실제로 실행
   │
   ▼
③ KnowledgeAgent.refine()   → 결과를 학습하고 pems_score 업데이트
   │
   ▼
응답 텍스트 반환
```

**v9.1 추가 기능**: 동일한 AgentContext가 들어오면 `decision_cache`에서 즉시 꺼내서 반환 (LLM 호출 없음, 0.001초 응답)

---

### 📌 DecisionAgent

> **한 줄 요약**: "이 질문을 어떻게 처리할지" 결정만 하는 에이전트. 실행은 하지 않는다.

**결정 방식 (우선순위 순)**:
1. **키워드 룰 매칭** (가장 빠름): `/web`, `/tag`, `/exec` 키워드가 있으면 즉시 결정
2. **LLM 결정** (중간): 키워드 없으면 LLM에게 "이 질문 어떻게 처리할까?" 물어봄
3. **기본값** (폴백): 아무것도 해당 없으면 `ask` (답변) 으로 처리

**출력 형식 (항상 JSON)**:
```json
{
  "action": "web",
  "query": "최신 AI 뉴스",
  "confidence": 0.9,
  "reasoning": "키워드 '검색해줘' 매칭"
}
```

---

### 📌 ExecutionAgent

> **한 줄 요약**: DecisionAgent의 결정을 실제로 실행하는 손발 역할. 결정은 안 하고 실행만 한다.

**지원 액션**:
| 액션 | 실행 내용 | 핸들러 |
|------|-----------|--------|
| `ask` | 메모리 기반 질의응답 | `handlers._memory.cmd_ask_logic` |
| `tag` | 문서 태깅 처리 | `handlers._approval.cmd_tag_logic` |
| `web` | 웹 검색 + 요약 | 웹 검색 CLI |
| `wiki` | 로컬 옵시디언 검색 | HybridKnowledgeIndexer |
| `exec` | Bash 명령어 실행 | `modules.executor` |

---

### 📌 KnowledgeAgent

> **한 줄 요약**: 실행 결과를 분석해서 봇이 더 똑똑해지도록 pems_score와 오답 노트를 업데이트하는 학습 에이전트.

**하는 일**:
- 실행이 성공하면 → `pems_score` 소폭 상승
- 실행이 실패하면 → 실패 원인을 `rejected_buffer`에 기록 (오답 노트)
- `hot_context` 업데이트 → 다음 질문에서 최근 맥락을 참조 가능

---

### 📌 /reduce 명령어

> **한 줄 요약**: 텔레그램에서 `/reduce <질문>`을 입력하면 HermesCoreReducer 파이프라인을 거쳐 지능적으로 응답하는 메인 명령어. 단순 QA부터 웹 검색, 위키 검색, 태그 처리까지 DecisionAgent가 자동 분류한다.

**사용법**: `/reduce <질문|명령어>`

**전체 흐름**:
```
Telegram: /reduce 오늘 날씨 어때?
   │
   ▼
① cmd_reduce (handlers/_memory.py)
   ├─ check_user() → 권한 확인
   ├─ AgentContext 생성 (message_id, user_id, query)
   └─ reduce() 호출
        │
        ▼
② DecisionAgent.decide()
   ├─ LLM + 키워드 매칭 hybrid (룰 기반 우선)
   │   web 키워드: "날씨", "뉴스", "주가", "검색 ", "http"
   │   tag 키워드: "태그", "tag"
   │   ask 키워드: 나머지 (기본값)
   └─ action 결정 → {action, query, metadata}
        │
        ▼
③ ExecutionAgent.execute(action, query)
   ├─ web  → 웹 검색 CLI 실행 → 요약 반환
   ├─ wiki → 위키 FTS5 검색 → 결과 반환 (LLM 정제 적용)
   ├─ tag  → 태그 연결 처리
   ├─ ask  → _call_llm() 호출 (일반 LLM 답변)
   └─ exec → Bash 명령어 실행 (신뢰된 쿼리만)
        │
        ▼
④ KnowledgeAgent.refine()
   └─ hot_context 업데이트, pems_score 조정
        │
        ▼
⑤ 응답 텍스트 → Telegram reply_text()
```

**DecisionAgent 액션 분류 상세**:

| 액션 | 결정 방식 | 실행 결과 |
|------|----------|---------|
| `web` | 키워드 매칭 1순위 (날씨/뉴스/주가/검색) + LLM 보조 | 웹 검색 결과 요약 |
| `wiki` | 키워드 매칭 (문서 검색 관련) + LLM 판단 | 위키 검색 결과 → LLM 정제 (v9.1.3+) |
| `ask` | 기본값 — 모든 액션이 매칭되지 않음 | LLM 직접 답변 (일반 QA) |
| `tag` | "태그", "tag" 키워드 감지 | 태깅 엔진 실행 |
| `exec` | 특수 패턴 매칭 | 시스템 명령어 실행 |

**웹 검색 (web 액션)**:
- 웹 검색 CLI로 실시간 정보 수집
- 결과를 LLM이 자연어로 요약하여 반환
- 키워드 확장: "날씨", "뉴스", "주가", "검색 " 접두사는 자동으로 web 액션 분류

**위키 검색 (wiki 액션)**:
- 로컬 옵시디언 보관소 FTS5 검색 실행
- 검색 결과를 **LLM으로 재가공**하여 자연어 답변으로 정제 (v9.1.3 추가)
- 원시 검색 결과가 아닌 읽기 쉬운 형태로 응답

**LLM 일반 질문 (ask 액션)**:
- 키워드 매칭 + LLM 결정 모두 miss된 경우 기본값
- `_call_llm()` → hybrid_router → Gemini/NVIDIA/DeepSeek 라우팅
- CoVe(구문 검증기) fallback 포함: verifier가 빈 결과 반환 시 직접 LLM 호출

**Context Hash Cache**:
- 동일한 `AgentContext` 입력이 5분 이내 재요청되면 LLM 호출 없이 캐시된 결과 반환
- 캐시 키: `(message_id, user_id, query)` 해시

**사용 예시**:

| 명령어 | 액션 | 동작 |
|--------|------|------|
| `/reduce 오늘 날씨` | web | 날씨 검색 → 요약 |
| `/reduce 최신 뉴스` | web | 뉴스 검색 → 요약 |
| `/reduce 삼성전자 주가` | web | 주가 검색 → 요약 |
| `/reduce 검색 스트레스 관리` | web | 키워드 검색 → 요약 |
| `/reduce HMM 모델이 뭐야` | wiki | 위키 검색 → 정제된 답변 |
| `/reduce 태그 추가 중요` | tag | 태깅 처리 |
| `/reduce 파이썬의 철학은?` | ask | LLM 직접 답변 |
| `/reduce ls -la ~/Applications` | exec | Bash 실행 |

**에러 처리**:
- 권한 없음 → silent return (check_user 실패)
- 빈 결과 → "죄송합니다, 응답을 생성하지 못했습니다." (방어 로직)
- LLM 호출 실패 → raw 결과 fallback (wiki 액션 _refine_result)
- f-string 등 문법 오류 → 봇 crash 방지를 위해 pre-import 구문 검사

**구현 파일**: `handlers/_memory.py` (cmd_reduce), `modules/core_reducer.py` (reduce 로직)

---

### 📌 ArchitecturalJudgmentGate — v9.2 Priority 4

> **한 줄 요약**: `/status`, `/pause`, `/resume`, `/ping` 같은 결정론적 명령어를 LLM 호출 없이(토큰 0원) 즉시 처리하는 **Harness 7 숏컷 게이트**.

**파일 위치**: `modules/core_reducer.py` → `ArchitecturalJudgmentGate` 클래스

**사용법**:
| 명령어 | 효과 |
|--------|------|
| `/status` | 현재 리듀서 상태(RUNNING/PAUSED) 확인 |
| `/pause` | 리듀서 일시정지 (모든 처리 차단) |
| `/resume` | 리듀서 재개 |
| `/ping` | 응답 확인 (health check) |
| `ping` | 슬래시 없는 `ping`도 동일 처리 |

**동작 원리**:
```python
reduce() 진입 직후
   │
   ▼
JudgmentGate.is_deterministic_shortcut(query)
   │
   ├─ 5개 숏컷 매칭 (startswith 접두사 매칭 → `ping`도 `ping something`도 ok)
   │     └─ 매칭? → LLM 호출 0회, 0.5ms 응답 🚀
   │
   └─ 미매칭? → 정상 DecisionAgent 파이프라인 진입
```

**효과**:
- 토큰 비용 **0원** — LLM 한 번도 안 탐
- 응답 시간 **0.5ms** — 기존 파이프라인 대비 1,000~6,000배 빠름
- 숏컷 처리도 **MonitoringEngine에 메트릭 기록**되어 추적 가능
- `startswith` 접두사 매칭으로 `ping` 외에도 `ping all`, `ping local` 같은 확장 자연스럽게 처리

**구현 위치**: `modules/core_reducer.py` L90-120 (JudgmentGate 클래스), L586-600 (reduce() 내 숏컷 체크)

---

### 📌 SelfImprovingAgent (SIA) — v9.2 Priority 3

> **한 줄 요약**: 사용자 👍/👎 피드백을 SQLite에 쌓아 액션별 평점을 분석하고, 저성능 액션을 자동 감지·개선 제안하는 자가 학습 엔진.

**파일 위치**: `modules/sia_engine.py`

**사용법** (코드에서 호출):
```python
# 피드백 기록
await sia.record_feedback(query="오늘 날씨", action="web", result="맑음 25도", rating=4)

# 액션별 평점 추세
trends = await sia.analyze_trends()
# → {"web": 4.2, "ask": 3.8, "tag": 4.5}

# 저성능 액션 감지 (↓ 이 액션들의 개선이 필요)
low = await sia.get_low_performers(threshold=3.0, min_samples=3)
# → ["ask", "exec"]

# LLM 개선 제안 생성
suggestion = await sia.suggest_improvements("ask")
```

**통합 지점**: `HermesCoreReducer.apply_user_feedback()` — /reduce 실행 후 사용자 피드백을 받아 SIA에 전달

**효과**:
- 어떤 액션이 자주 실패하는지 **데이터 기반**으로 파악 가능
- 사람이 일일이 로그를 뒤질 필요 없이 **자동 감지**
- 저성능 액션에 대해 **LLM이 구체적인 개선 제안** 생성
- 모든 피드백은 **SQLite (WAL 모드)** 에 영구 저장 → 재부팅 후에도 유지
- DB 위치: `~/.hermes/runtime/sia_feedback.db`

---

### 📌 MonitoringEngine — v9.2 Priority 3

> **한 줄 요약**: 모든 리듀서 실행의 응답 시간·에러율·결과 길이를 실시간 추적하고, 성능 저하 시 자동 경고하는 모니터링 대시보드 (DB 기반).

**파일 위치**: `modules/monitoring_engine.py`

**사용법** (코드에서 호출):
```python
# 메트릭 기록 (core_reducer.reduce() 마지막에 자동 호출됨)
await mon.record_metric(MetricSnapshot(
    timestamp=time.time(),
    action="web",
    response_time_ms=850.0,
    result_length=320,
    error_flag=False,
))

# 액션별 통계
stats = await mon.get_action_stats("web", hours=24)
# → {"avg_response_time_ms": 850, "success_rate": 0.95, "total_calls": 120}

# 전체 에러율
err_rate = await mon.get_error_rate()  # 2.3 → 2.3%

# 성능 저하 감지
alert = await mon.alert_if_degradation(hours=1)
# → "⚠️ 전체 에러율 12.3% — 임계값 10% 초과" 또는 None

# 시간대별 성능 트렌드 (차트용)
trend = await mon.get_performance_trend(hours=24, interval_minutes=60)
# → {"labels": ["14:00", "15:00", ...], "response_times": [...], "error_rates": [...]}
```

**경고 임계값**:
| 항목 | 임계값 | 초과 시 |
|------|--------|--------|
| 에러율 | 10% | ⚠️ 경고 |
| 응답시간 | 3,000ms 평균 | ⚠️ 경고 |
| 액션 성공률 | 80% 미만 | ⚠️ 경고 |

**효과**:
- **실시간 성능 가시화** — 어떤 액션이 느린지, 에러가 많은지 한눈에
- **자동 경고** — 사람이 안 봐도 성능 저하를 감지하고 알림
- **메모리+SQLite 이중 캐시** (최근 1,000개 메트릭 메모리 유지)
- DB 위치: `~/.hermes/runtime/metrics.db`

---

### 📌 ModelLoadBalancer — v9.2 Priority 3

> **한 줄 요약**: 3개 모델(Gemma4/DeepSeek/NVIDIA)의 응답 시간과 성공률을 실시간 측정하여 **가장 빠르고 안정적인 모델로 자동 라우팅**하는 확률적 로드 밸런서.

**파일 위치**: `modules/load_balancer.py`

**사용법** (hybrid_router.py 내부에서 자동 실행):
```python
# 최적 모델 선택 (가중치 기반 확률적)
best = await lb.select_best_model()
# → "deepseek" (성능 데이터가 쌓일수록 더 정확해짐)

# 모델 성능 기록 (각 API 호출 후 자동 호출)
await lb.record_model_performance("deepseek", 850.0, True)

# 모델 성능 순위
rankings = await lb.get_model_rankings()
# → [ModelMetric(nvidia, 1500ms, 1.0), ModelMetric(deepseek, 2000ms, 0.98)]

# 가중치 재조정 (1시간 주기 권장)
weights = await lb.rebalance_weights()
```

**알고리즘**:
```
weight = 1.0 / (avg_response_time_ms × (1.0 - success_rate + 0.01))

→ 응답시간이 짧을수록 가중치 ↑
→ 성공률이 높을수록 가중치 ↑
→ 누적 가중치 기반 확률적 선택 (고정 선택 아님 — 탐험 기회 보장)
```

**효과**:
- 항상 **가장 빠른 모델**을 우선 사용 → 사용자 응답 시간 최적화
- **탐험(exploration) 보장** — 확률적 선택으로 성능 데이터 없는 모델도 기회를 얻음
- DB 기반으로 **재부팅 후에도 학습 이력 유지**
- `hybrid_router.py`의 모든 API 호출(`_call_deepseek`, `_call_local`, `_call_nvidia`)에 통합
- DB 위치: `~/.hermes/runtime/model_metrics.db`

---

### 📌 Tag/Exec 보안 3중 필터 — v9.2 Priority 1 & 2

> **한 줄 요약**: `/tag` 핸들러와 `/exec` 실행기에 **3중 보안 필터**를 적용하여 한글/특수문자 주입, 위험 명령어, 경로 탈출을 원천 차단.

**Priority 1 — Tag 한글 보안 (`handlers/_approval.py`)**
| 단계 | 내용 |
|------|------|
| ① `shlex.quote()` | 모든 쿼리 인자 escape 처리 (셸 주입 방지) |
| ② `VALID_ACTIONS` 화이트리스트 | `pending`/`approve`/`reject` 외 모든 액션 → 일반 질의로 fallback |
| ③ 조기 반환 | 화이트리스트에 없으면 태그 명령어로서 무시 → 정상 QA로 유도 |

**Priority 2 — Exec/File 3중 필터 (`core_reducer.py`의 `_execute_exec`/`_execute_file`)**
| 단계 | Exec 필터 | File 필터 |
|------|-----------|-----------|
| ① 위험 명령어 블록리스트 | `rm -rf`, `mkfs`, `dd`, `fork` 폭탄 등 7종 차단 | — |
| ② 한글/특수문자 검사 | 한글 포함 시 → 일반 질의로 간주 (실행 차단) | 한글/특수문자 포함 경로 → 실행 차단 |
| ③ asyncio timeout | 30초 강제 타임아웃 (무한 루프 방지) | 경로 정규화(`realpath`) → 허용 경로(`/Users/bluesea/Applications/`)만 통과 + 100MB 파일 크기 제한 |

**효과**:
- ❌ 한글 명령어가 셸로 전달되어 깨지는 **버그 완전 차단**
- ❌ `rm -rf /` 같은 **파괴적 명령어 실행 불가**
- ❌ 경로 탐색(`../../etc/...`) **차단**
- ✔️ 모든 차단은 **조용히 무시(silent deny)** — 사용자 경험에 영향 없음
- ✔️ **일반 질의와 태그 명령어를 명확히 분리** — `"테스트 좀..."`이 태그로 오인되지 않음

---

### 📌 PermissionBridge — 2-tier 도구 인가 게이트웨이

> **한 줄 요약**: `modules/permission_bridge.py`에서 내부 도구(읽기 전용)는 자동 승인, 외부 영향 도구(RUN_CMD, SAVE, DELETE 등)는 Telegram 인라인 키보드 승인을 강제하는 2계층 권한 게이트웨이.

**2-Tier 구조**:

| 계층 | 구분 | 대상 도구 | 승인 방식 |
| :---: | :--- | :--- | :--- |
| **Tier 1** | 🏠 Internal (자동) | `read`, `search`, `list`, `summarize`, 모든 getter | 즉시 실행, 승인 불필요 |
| **Tier 2** | 🚪 External (승인 필요) | `RUN_CMD`(셸 명령), `SAVE`(파일 저장), `DELETE`/`MOVE`/`COPY`/`RENAME`(파일 조작) | Telegram `/confirm [id]` 인라인 버튼 필요 |

**연동 흐름**:
```python
await perm_bridge.request_approval(
    update, context,
    action="save:run_cmd",
    description="Files/...로 파일 저장",
    callback_data="perm_approve:save:12345",
    # Tier 2 → approval_keyboard 자동 생성
    # 승인 시 handle_approval_callback() → 원래 작업 실행
)
```

**통합된 파일**:
| 파일 | 통합 내용 |
| :--- | :--- |
| `modules/permission_bridge.py` | 2-tier 클래스 정의, `request_approval()`, `handle_approval_callback()` |
| `handlers/_base.py` | `perm_approve:` 콜백 라우팅 — handle_button_callback() 위임 |
| `harness_agent.py` | RUN_CMD (line 706) + SAVE (line 758) PermissionBridge 가드 |
| `harness_agent.py` | `_handle_file_op()` — 모든 파일 작업(DELETE/MOVE/COPY/RENAME) PermissionBridge 사전 승인 |

**핵심 설계 의사결정**:
- **JSON/DB 기반 상태 관리 배제** — 상태는 Telegram callback_data의 `perm_approve:<action>:<file_id>` 인코딩으로만 유지 (stateless 원칙)
- **호출자 ID 검증** — 승인 요청 발신자만 승인 가능 (다른 사용자 차단)
- **10분 TTL** — 오래된 승인 요청 자동 만료 (메모리 누수 방지)

---

## 🧠 지식 관리

---

### 📌 DreamingV2 (FluxMem+SKILLOPT)

> **한 줄 요약**: 봇이 잠든 동안(백그라운드에서) 쌓인 대화 로그를 분석하여 마크다운 지식으로 압축하는 자율 학습 엔진. 단, 이미 충분히 성숙한 지식이라면 LLM 호출을 100% 건너뛴다.

**파일 위치**: `modules/dreaming_v2.py`

**처리 흐름**:
```
SQLite 워크벤치에 쌓인 원시 로그
   │
   ▼
① PEMS 점수 계산 → 지식이 이미 성숙했다면? → 💤 LLM 호출 차단 (0원 절감)
   │ 아직 덜 익었다면 계속 진행
   ▼
② KV 방어선 (MAX_SAFE_CHAR_SIZE=12,000자) → 12,000자 초과분은 다음 번에
   │
   ▼
③ 오답 노트(Rejected Buffer) 로드 → "지난번에 이 방식은 실패했다"
   │
   ▼
④ LLM에게 "이렇게 하지 말고, 원자적 패치(Patch)만 4개 제안해" 요청
   │
   ▼
⑤ Validation Gate → 제안된 패치가 기존보다 좋아야만 적용
   │ 나쁘면 → 오답 노트에 기록 후 버림
   ▼
⑥ 옵시디언 마크다운 파일 업데이트 (distilled_knowledge.md)
```

**차용 논문**:
- **FluxMem** (Microsoft, 2026-05): 기억을 연결 그래프로 관리, 불필요한 노드 가지치기
- **SKILLOPT** (Microsoft, 2026-05): 마크다운 스킬 파일을 딥러닝처럼 점진적으로 최적화

---

### 📌 PEMS 점수

> **한 줄 요약**: 지식이 얼마나 성숙했는지 나타내는 0~1 사이의 점수. 높을수록 굳이 LLM을 다시 돌릴 필요가 없다.

**계산 공식**:
```
PEMS = 성공률(η) × 압축성(1/log(토큰길이)) × 안정성(1 - 변동폭)
```

**의미 해석**:
| 변수 | 의미 | 높을수록 |
|------|------|---------|
| η (성공률) | 최근 이 지식을 써서 성공한 비율 | 신뢰도 높음 |
| 1/log(토큰) | 지식이 짧고 압축적인가 | 카파시 철학 준수 |
| 1-변동폭(δ) | 최근에 갑자기 지식이 확 바뀌지 않았나 | 안정적 |

**ΔPEMS < 0.01이면**: 지식이 수렴(성숙)했다고 판단 → LLM 호출 전면 차단

---

### 📌 Rejected-Edit Buffer

> **한 줄 요약**: 봇이 시도했다가 실패한 지식 패치들을 기록해두는 "오답 노트". 같은 실수를 반복하지 않기 위해 다음 학습 때 프롬프트에 주입된다.

**저장 위치**: `~/.hermes/runtime/dreaming_workbench.db` → `rejected_edits` 테이블

**동작 원리**:
```
실패한 패치 발생
   │
   ▼
rejected_edits 테이블에 저장 (failed_patch, 날짜)
   │
   ▼
다음 DreamingV2 실행 시 → LLM 프롬프트에 주입:
"이 방식들은 이미 실패했으니 절대 반복하지 마세요: ..."
```

---

### 📌 Validation Gate

> **한 줄 요약**: LLM이 제안한 지식 패치가 기존보다 실제로 더 좋아졌을 때만 마크다운 파일에 영구 저장하는 검증 관문.

**동작 원리**:
```
LLM 제안 패치 생성
   │
   ▼
검증 점수 계산 (0.85 vs 기존 최고 0.80)
   │
   ▼
새 점수 > 기존 최고점? ──YES──► 옵시디언 파일 영구 업데이트 ✅
              │
             NO
              │
              ▼
         오답 노트에 저장 후 버림 🗑️
```

---

### 📌 태깅 자동화 시스템 vs Karpathy LLM Wiki — 두 지식 시스템의 차이

> **한 줄 요약**: `TagLinker`+`OntologyGraph` 기반 자동 태깅 시스템은 **문서에 태그를 붙이는** 도구이고, `KnowledgeIndexer`(Karpathy LLM Wiki)는 **태그가 붙은 문서를 검색하는** 도구다. 서로 별개로 동작하며, 하나의 파이프라인이 아니다.

| 항목 | 태깅 자동화 시스템 | Karpathy LLM Wiki (KnowledgeIndexer) |
|------|-------------------|--------------------------------------|
| **담당 파일** | `tag_linker.py`, `ontology_graph.py`, `cascade_engine.py`, `bio_memory_engine.py` (Semantic Keyword Edge) | `knowledge_indexer.py` (`HybridKnowledgeIndexer` 클래스) |
| **목적** | 문서 내용을 분석해 자동으로 키워드/태그를 제안·승인하고, 온톨로지 관계를 추적하며, 태그 변경 시 연쇄 업데이트 전파 | wiki/ 아래 모든 .md 파일을 스캔해 검색 가능한 인덱스(FTS5 + TF-IDF) 구축 |
| **동작 방식** | 반응적(on-demand) — `/ingest` 실행 시 LLM이 문서 내용을 분류하고 키워드를 추출하여 frontmatter tags에 자동 추가 | 능동적/정기적 — 주기적으로 wiki/ 폴더를 스캔하여 H2 헤딩 기준 청킹 후 SQLite FTS5에 인덱싱 |
| **트리거** | 문서 생성·이관(`/ingest`), 태그 제안·승인 콜백 (`propose_tag` / `approve_tag`) | fswatch 파일 변경 감지, `/ask` 검색 시점에 자동 조회 |
| **데이터 저장** | 문서 내부 frontmatter (`tags: [...]`) + 온톨로지 그래프 (OntologyGraph) + Semantic Keyword Edge (Bio-Memory) | SQLite FTS5 인덱스 (`wiki_knowledge` 테이블) + TF-IDF 벡터 |
| **검색 방식** | 태그 직접 매칭, 연관 태그 그래프 탐색 (CascadeEngine) | FTS5 전문 검색 + TF-IDF 코사인 유사도 + RRF 순위 융합 |
| **출력** | 문서 frontmatter 업데이트 (태그·설명·카테고리), 그래프 관계 갱신 | 검색 결과: 관련 문서 목록 (청크 단위, 점수 순) |
| **사용자 대상** | 시스템 내부 — 자동화 파이프라인 | 사용자 질의응답 — `/ask` 명령어에서 검색 백엔드로 사용 |

**왜 별도 시스템인가?**

초기 설계에서는 이 두 시스템이 같은 것이라고 오해하기 쉽다. 하지만:

1. **태깅은 문서 메타데이터를 풍부하게 만드는 것** — 문서 자체에 태그를 심어서 나중에 옵시디언에서 그래프 뷰로 탐색하거나, 연관 문서를 찾을 수 있게 한다.
2. **Karpathy LLM Wiki는 검색 인덱스를 만드는 것** — 문서 내용을 통째로 분석해서 "어느 문서에 이 내용이 있었지?"라는 질문에 빠르게 답하기 위한 도구다.
3. **두 시스템은 데이터도 별개** — 태깅은 문서 frontmatter + 온톨로지 DB를 쓰고, LLM Wiki는 SQLite FTS5 인덱스를 쓴다.

**둘의 관계**:
```
/ingest 실행
  ├── Clippings 이관 + 루트 파일 정리
  │     └── LLM 분류 → frontmatter tags 업데이트 (태깅 시스템)
  │
  └── fswatch 변경 감지 (백그라운드)
        └── KnowledgeIndexer 인덱스 갱신 (LLM Wiki)
```

각자 독립적으로 동작하며, `TagLinker`의 Pub-Sub 이벤트 버스를 통해 **연쇄 변경(Cascade)** 만 느슨하게 연결되어 있다.

**관련 항목**:
- [TagLinker](#-taglinker) — Pub-Sub 이벤트 버스 시스템의 중앙 허브
- [카파시 다이어트 철학](#-카파시-다이어트-철학) — LLM Wiki의 철학적 배경

---

### 📌 Ingest (지식 이관) — Clippings → 위키 자동 분류 파이프라인

> **한 줄 요약**: 텔레그램 `/ingest` 명령어 실행 시 **Clippings → 분류 → 위키** 3단계 파이프라인이 자동으로 동작하며, LLM 분류를 통해 6개 카테고리 중 하나로 파일을 분류·이관하고 태그를 추가한다.

**실행 위치**: `~/Applications/Mjauto/Scripts/modules/ingest_engine.py` — `IngestEngine` 클래스
**트리거 경로**: 텔레그램 `/ingest` → `handlers/_file.py` `cmd_ingest()` → `IngestEngine.process_all()`

**파이프라인 3단계 (IngestEngine.process_all 실행 순서)**:

| 단계 | 메서드 | 처리 대상 | 설명 |
| :--- | :--- | :--- | :--- |
| 1 | `_process_clippings()` | `Clippings/` 내 모든 파일 | 텔레그램에서 저장된 클리핑 파일 처리 |
| 2 | `_process_root_files()` | Mjobsidian 루트에 방치된 .md/.pdf 파일 | 루트에 쌓인 미분류 파일 처리 |
| 3 | `_process_inbox()` | `Clippings/Inbox/` 내 `*_pending.md` 파일 | 이전에 분류 실패한 파일 재분류 |

**각 단계별 상세 처리**:

**1. Clippings 처리 (`_process_clippings`)**
- `Clippings/` 디렉토리 내 모든 일반 파일을 스캔 (Archive 제외)
- LLM이 파일 내용을 분석해 category + title + description + keywords 생성
- 6개 허용 카테고리: `10_AI_Automation`, `20_Research`, `30_Journal`, `40_Thesis`, `50_Invest`, `Unsorted`
- 분류 성공 → 해당 카테고리 폴더로 이동 + frontmatter 업데이트 + TagLinker DB 동기화
- 분류 실패(Unsorted/JSON 파싱 실패) → Inbox로 deferral
- 원본은 `Clippings/Archive/`로 백업 이동

**2. 루트 파일 처리 (`_process_root_files`)**
- Mjobsidian 루트 디렉토리에 방치된 .md/.pdf 파일 처리
- Clippings와 동일한 분류 로직 사용
- 분류 성공 → 카테고리 폴더로 이동 (mtime 보존)
- 분류 실패 → Inbox로 deferral 후 원본 삭제

**3. Inbox 재분류 (`_process_inbox`)**
- `Clippings/Inbox/` 내 `*_pending.md` 파일을 다시 LLM 분류 시도
- 2차 시도 성공 → 정식 카테고리 폴더로 이동
- 2차 시도 실패 → Inbox 잔류 (다음 Ingest 라운드에서 재시도)

**전체 파일 구조**:

```
~/Applications/Mjobsidian/
├── Clippings/                    ← 텔레그램 클리핑 저장소
│   ├── (분류 전 파일들)          ← LLM 분류 대기 상태
│   ├── Archive/                  ← 처리 완료된 원본 백업
│   └── Inbox/                    ← 저신뢰 분류 파일 보관소
│       └── *_pending.md          ← Unsorted 판정된 파일 (재분류 대기)
│
├── 10_AI_Automation/             ← AI 자동화 카테고리
├── 20_Research/                  ← 연구 자료 카테고리
├── 30_Journal/                   ← 저널/기사 카테고리
├── 40_Thesis/                    ← 논문/학위 자료 카테고리
├── 50_Invest/                    ← 투자 자료 카테고리
└── (그 외 루트 파일들)           ← 다음 Ingest 시 처리 대상
```

**Unsorted 처리: 왜 Inbox인가?**

`Unsorted`는 **실제 폴더가 아니라 LLM 분류 실패 시의 fallback 트리거**입니다. `ALLOWED_CATEGORIES`에는 `"Unsorted"`가 등록되어 있지만, 코드에서 `category == "Unsorted"`인 경우는 **Inbox로 deferral**하도록 설계되었습니다. 즉 `Unsorted` 폴더는 생성되지 않으며, 대신 `Clippings/Inbox/파일명_pending.md` 형태로 보관됩니다.

이 설계의 이유:
- 분류 실패 파일을 강제로 특정 폴더에 넣어버리면 사용자가 발견하지 못하고 방치됨
- Inbox에 _pending 접미사로 모아두면 사용자가 직접 확인·분류하기 쉬움
- 다음 Ingest 실행 시 자동 재분류 시도 (반영구적 방치 방지)

**수동 관리 방법**: Inbox에 `_pending.md` 파일이 남았다면:
1. 파일 내용을 열어보고 직접 적절한 카테고리 판단
2. 수동으로 이동: `mv Inbox/파일명_pending.md 30_Journal/파일명.md`
3. 이동 후 frontmatter에 적절한 `tags: [...]` 추가
4. 또는 다음 `/ingest` 실행 시 자동 재분류를 기다림 (이미 2회 실패한 파일은 실패할 가능성 높음)

**파일명 생성 규칙**:
- LLM이 추출한 title을 기준으로 `.md` 파일 생성
- 특수문자 제거, 공백 유지
- Clippings 원본 파일명과 다른 경우가 일반적 (LLM이 내용 기반으로 새 제목 생성)

**TagLinker 동기화**:
- 처리 완료된 파일은 `TagLinker.sync_document()`를 통해 `~/.hermes/runtime/hermes_index.db`에 태그 DB 동기화
- 20_Research 카테고리 파일은 추가로 `index_db.add_paper()`로 논문 인덱싱

---

### 📌 Save vs Organize & Inbox Deferral

> **한 줄 요약**: `/save file` 명령어는 **순수 저장** 역할로, ingest engine은 **분류+이동** 역할로 명확히 분리해야 한다는 설계 원칙. 저신뢰 분류 파일은 Inbox에 deferral 후 재분류 라운드에서 처리.

**문제 정의 (Save vs Organize 분리)**
| 측면 | SAVE 태그 (harness_agent) | Ingest Engine |
| :--- | :--- | :--- |
| 역할 | 파일 내용을 특정 경로에 저장 | 문서 분류·태깅·정리 |
| 경로 결정 | LLM이 `[SAVE:/path]content[/SAVE]` 형식으로 직접 지정 | LLM 분류 결과에 따라 자동 결정 |
| 문제점 | 저장 경로를 LLM에 전적으로 의존 — 분류 오류 시 엉뚱한 위치에 저장 | 저신뢰(Unsorted) 분류 시에도 강제로 폴더 배정 |
| **해결** | PermissionBridge Tier 2 게이트로 분류 오류 방지 | Inbox Deferral로 저신뢰 파일 보류 |

**Inbox Deferral 메커니즘 (v9.2)**

| 단계 | 설명 |
| :--- | :--- |
| ① LLM 분류 | ingest 과정에서 LLM이 category + keywords 생성 |
| ② 저신뢰 판별 | category == "Unsorted" OR JSON 파싱 실패 → Inbox로 defer |
| ③ 파일 복사 | 원본 → Archive/백업 + Inbox/`*_pending.md` 복사본 생성 |
| ④ 태그/인덱싱 skip | frontmatter 업데이트, tag DB 동기화, 논문 인덱싱 모두 생략 |
| ⑤ 재분류 라운드 | `_process_inbox()`가 `_pending.md` 파일을 재분류 — 2차 실패 시 Inbox 잔류 |

**의사결정**:
- `_pending` 접미사 사용 (숨김파일/별도 DB보다 직관적)
- Inbox는 Clippings 소스 디렉토리 아래 (`source_dir/Inbox/`) — Archive와 동일 계층
- Archive 백업 후 원본 제거 — Inbox가 유일한 pending 사본
- 2회 연속 실패 시 Inbox 잔류 (파일 손실 방지) — 매 ingest 라운드마다 재시도

### 🔧 TagLinker 인자 오류 수정 (2026-06-03)

**오류**: `TagLinker.__init__() got an unexpected keyword argument 'vault_path'`

**원인**: `ingest_engine.py` Line 20에서 `TagLinker(vault_path=str(vault_path))`로 호출했으나,
`tag_linker.py` Line 30의 `__init__` 시그니처는 `def __init__(self, db_path: Optional[str] = None):`로,
`vault_path` 인자가 없고 `db_path`만 받음.

**수정 내용**:
- `vault_path` 변수 라인 제거 (vault_path = dest_dir.parent)
- `TagLinker(vault_path=str(vault_path))` → `TagLinker()`로 변경 (인자 없이 기본 DB 경로 사용)
- 기본 DB 경로: `~/.hermes/runtime/hermes_index.db` (TagLinker 기본값)
- `vault_path`가 디렉토리 경로를 전달하여 SQLite가 파일 경로를 기대하는 DB 연결과 충돌했던 문제 해결

**교훈**: TagLinker는 디렉토리 경로가 아닌 DB 파일 경로를 받으며, 인자 생략 시 기본 경로를 사용한다. ingest_engine에서 커스텀 DB 경로가 필요하지 않으므로 인자 없이 호출하는 것이 올바름.

---

## ⚡ 성능 최적화

---

### 📌 Context Hash Cache

> **한 줄 요약**: 같은 내용의 질문이 들어오면, LLM을 다시 호출하지 않고 이전 결과를 즉시 꺼내주는 캐시 시스템.

**파일 위치**: `modules/core_reducer.py` → `decision_cache` 테이블

**동작 원리**:
```
질문 입력
   │
   ▼
AgentContext → SHA256 해시 생성 (짧은 고유 ID)
   │
   ▼
decision_cache 테이블 조회 → 있고 TTL 만료 안됐으면?
   │                              │
  없음                           있음
   │                              │
   ▼                              ▼
LLM 호출 (1~3초)         캐시 반환 (0.001초) 💨
   │
   ▼
결과를 캐시에 저장
```

**효과**: 동일 질문 반복 시 응답 속도 **100배 향상**, 토큰 비용 **0원**

---

### 📌 KV 캐시 방어선

> **한 줄 요약**: 한 번에 LLM에 보내는 텍스트 양을 12,000자로 물리적으로 제한하여 로컬 모델(Gemma4)의 메모리 폭발을 막는 안전장치.

**설정값**: `MAX_SAFE_CHAR_SIZE = 12000`

**왜 필요한가?**  
LLM이 텍스트를 처리할 때, 이전에 본 모든 단어를 Key-Value 벡터로 메모리(KV 캐시)에 쌓아두는 구조다. 텍스트가 길어질수록 이 캐시가 기하급수적으로 커져 RAM이 폭발한다. 12,000자 제한은 약 3,000~4,000 토큰에 해당하는 안전 상한선이다.

---

### 📌 WAL 모드

> **한 줄 요약**: SQLite 데이터베이스를 여러 곳에서 동시에 읽고 쓸 때 데이터가 꼬이지 않도록 하는 안전 잠금 방식.

**WAL = Write-Ahead Logging**

**왜 중요한가?**  
봇이 텔레그램 메시지를 처리하면서 동시에 백그라운드에서 Dreaming을 돌리면 같은 DB 파일에 동시 접근이 발생한다. WAL 모드 없이는 데이터 손상이 일어날 수 있다.

**적용 코드**:
```python
conn.execute("PRAGMA journal_mode=WAL")
```

---

### 📌 TTL 기반 캐시 만료

> **한 줄 요약**: 캐시된 답변이 1시간이 지나면 자동으로 폐기하여 오래된 정보가 계속 사용되는 것을 막는 신선도 관리 장치.

**TTL = Time To Live** (생존 시간)

**동작 원리**:
```python
"SELECT ... WHERE (recorded_at + ttl_seconds) > 현재시각"
# → 저장된 시각 + 3600초 > 지금이면 유효, 아니면 무시
```

**정리 스케줄러**: 매 1시간마다 `cleanup_expired_cache()`가 자동 실행되어 만료된 캐시를 일괄 삭제

---

## 🔗 연결 시스템

---

### 📌 Pub-Sub 이벤트 버스

> **한 줄 요약**: 모듈들이 서로 직접 호출하지 않고, "신호를 방송하면 관심 있는 모듈이 알아서 구독"하는 느슨한 연결 구조.

**Pub-Sub = Publish-Subscribe** (발행-구독)

**비유**:
- **기존 방식**: A가 B에게 직접 전화 → B가 바쁘면 A도 대기
- **Pub-Sub 방식**: A가 게시판에 "태그 승인됨"이라고 붙여놓음 → B, C, D 각자 확인

**Hermes3 적용**:
```python
# 발행 (TagLinker)
TagLinker._dispatch("tag_approved", {"file": "note.md", "tag": "#AI"})

# 구독 (hermes_local.py)
TagLinker.subscribe("tag_approved", 캐스케이드_처리_함수)
```

**효과**: 새 기능 추가 시 기존 코드를 수정할 필요 없음 (Factor 7 충족)

---

### 📌 TagLinker

> **한 줄 요약**: Hermes3의 내부 이벤트 우편배달부. 모든 Pub-Sub 신호를 중앙에서 관리한다.

**파일 위치**: `modules/tag_linker.py`

**주요 이벤트**:
- `tag_approved`: 태그 승인됨
- `conversation_ended`: 대화 종료됨 → DreamingV2가 수집
- `error_occurred`: 오류 발생 → DreamingV2가 오류 기록
- `critical_error_detected`: 심각한 오류 → 관리자 알림

---

### 📌 AI Gateway (3-way Failover)

> **한 줄 요약**: LLM API가 먹통이 되어도 봇이 죽지 않도록, DeepSeek → NIM → 로컬 Gemma4 순서로 자동으로 갈아타는 자동 복구 시스템.

**Failover 체인**:
```
DeepSeek API (1순위, 최고 품질)
   │ 실패 (429 과금, 500 서버 에러)
   ▼
NIM API (2순위, 백업)
   │ 실패
   ▼
로컬 Gemma4 llama-server (3순위, 무조건 작동)
```

**지수 백오프 (Exponential Backoff)**:  
실패 시 1초 → 2초 → 4초 → 8초 간격으로 재시도하여 API 서버를 과부하시키지 않음

---

### 📌 Graphify (지식 그래프)

> **한 줄 요약**: `/vault graph` 명령어로 vault 문서 간 연결 구조를 추출·분석하는 on-demand 지식 그래프 엔진.

**pip 패키지**: `graphifyy` | **임포트**: `import graphify`

**명령어**: `/vault graph` — `handlers/_vault.py`의 `_vault_graph()` 함수

**동작 파이프라인**:
```
graphify.extract(files, parallel=False)  # 문서 간 관계 추출 (tree-sitter 기반)
     ↓
build_from_json(extraction, directed=True)  # NetworkX 방향 그래프 생성
     ↓
god_nodes(G, top_n=10)  # 허브 문서 식별 (연결이 가장 많은 핵심 문서)
surprising_connections(G, top_n=5)  # 예상치 못한 교차 연결 탐지
```

**특징**:
- on-demand 실행 (항상 실시간 추출, 캐시 미사용)
- `parallel=False` 필수 (Hermes Agent의 Python 3.11 spawn 제한 우회)
- 모든 `.md` 파일 스캔, 제외 디렉토리(`.obsidian`, `.trash` 등) 자동 필터
- 출력: 노드 수, 엣지 수, 고립 문서 수, 허브 노드 Top-N, 놀라운 연결

**의존성**: networkx (graphifyy가 자동 설치)

---

### 📌 adapters.py

> **한 줄 요약**: 텔레그램이든, 슬랙이든, 웹훅이든 어떤 채널로 들어온 메시지도 표준 AgentContext로 변환해주는 번역기 모듈.

**파일 위치**: `modules/adapters.py`

**지원 채널**:
```
Telegram 메시지  ──┐
Slack 메시지     ──┤──► AgentContext (표준 형식) ──► HermesCoreReducer
Webhook 요청     ──┤
크론(예약) 작업  ──┘
```

**핵심 가치**: 채널이 추가되어도 `reduce()` 함수는 단 한 줄도 수정할 필요 없다 (Factor 11)

---

### 🔄 switch-model (모델 전환 도구)

> **한 줄 요약**: GPT-OSS-120B(NVIDIA)와 DeepSeek Chat 사이에서 Hermes의 메인 모델을 전환하는 CLI 도구.

**배경**: NVIDIA의 got-oss-120b (무료) 모델이 DeepSeek Chat보다 저렴하고 성능이 우수한 경우가 있어, WebUI 드롭다운에서 수동으로 선택하는 대신 CLI 한 줄로 두 Hermes Home을 동시에 전환할 필요가 생김.

**파일 위치**: `~/Applications/venu/scripts/switch_model.sh`
**심링크**: `/usr/local/bin/switch-model`

**사용법**:
```
switch-model got       # 메인 모델을 GPT-OSS-120B(NVIDIA)로 전환
switch-model deepseek  # 메인 모델을 DeepSeek Chat으로 전환
```

**동작 방식**:
1. 두 Hermes Home의 `config.yaml`을 각각 읽음
2. `~/.hermes/config.yaml` — Gateway/WebUI 설정
3. `~/Applications/venu/.hermes2/config.yaml` — Telegram Bot 설정
4. 현재 선택된 모델에 주석 처리 (`# [SWITCHED to ...]`)
5. 대상 모델의 주석을 제거하여 활성화
6. (주의) 전환 후 `hermes gateway restart` 실행 필요

**핵심 원칙**:
- **파일 삭제 금지** — 전환된 쪽 설정은 `# [SWITCHED to ...]` 주석만 추가, 원본 보존
- **두 Hermes Home 동시 적용** — Gateway/WebUI + Telegram Bot 모두 일관성 유지
- **Gemma4 26B 무영향** — Gemma4는 별도 API 키를 사용하므로 모델 전환과 무관

---

## 📁 데이터 저장

---

### 📌 SQLite WAL 워크벤치

> **한 줄 요약**: 봇이 실시간으로 받는 모든 대화·오류 로그를 일단 저장해두는 임시 창고. DreamingV2가 주기적으로 이 창고를 비워 지식 파일로 정제한다.

**파일 위치**: `~/.hermes/runtime/dreaming_workbench.db`

**테이블 구조**:
| 테이블 | 역할 |
|--------|------|
| `raw_events` | 아직 증류되지 않은 원시 로그 (대화, 오류) |
| `rejected_edits` | 검증 실패한 패치 (오답 노트) |
| `pems_history` | PEMS 점수 변화 이력 |
| `decision_cache` | Context Hash 캐시 (v9.1) |

---

### 📌 hot.md (실시간 스트림)

> **한 줄 요약**: 봇이 대화를 처리할 때마다 핵심 요약본을 실시간으로 기록하는 "오늘의 일기장". 현재 맥락을 파악하는 데 사용된다.

**파일 위치**: `~/Applications/Mjobsidian/hot.md`

**기록 방식**: DreamingV2가 대화 요약을 `[v8.9 Stream] {요약}` 형식으로 append

---

### 📌 Mjobsidian 보관소

> **한 줄 요약**: 봇이 축적한 모든 지식이 마크다운 파일로 저장되는 장기 기억 창고. 옵시디언(Obsidian) 앱으로 시각화하고 편집할 수 있다.

**경로**: `~/Applications/Mjobsidian/`

**주요 하위 폴더**:
```
Mjobsidian/
├── wiki/00_Meta/        ← 시스템 메타 문서 (이 백과사전 포함)
├── Journal/             ← DreamingV2 증류 결과물
├── Memory/              ← 장기 지식 베이스
└── hot.md               ← 실시간 스트림
```

---

## 🚫 보류 기능

---

### 📌 Multi-Agent Orchestration (보류)

> **보류 이유**: 에이전트 간 통신을 위해 대용량 State를 메모리에 상시 유지해야 하므로 Stateless 철학과 충돌. 코드가 2,000줄 이상으로 재증가하고 LLM을 질문당 3~4회 호출하게 됨.
> **재검토 조건**: 전용 서버 확보 시

---

### 📌 Advanced RAG / sqlite-vec (보류)

> **보류 이유**: 모든 질문에 임베딩 연산이 강제되어 RAM 사용량이 상시 증가하고 부팅 시간 2.5초 원칙이 붕괴됨.
> **재검토 조건**: 옵시디언 보관소가 문서 10만 개를 초과하여 FTS5 검색이 느려질 때

---

### 📌 Auto-Refactoring / Self-Healing (보류)

> **보류 이유**: AI 환각(Hallucination)으로 정상 코드를 버그로 오인하면 무한 수리 루프에 빠져 API 과금 폭탄 및 시스템 불안정 유발.
> **재검토 조건**: Edit Budget(1일 3회 물리 제한) 및 롤백 메커니즘이 완벽히 설계된 후

---

## 📝 업데이트 이력

| 날짜 | 추가 항목 | 작성자 |
|------|-----------|--------|
|| 2026-06-02 | Graphify 연동 추가: `/vault graph` 명령어 + 백과사전 문서화 | Hermes Agent |
|| 2026-06-06 | switch-model (모델 전환 도구) 항목 신설 — GPT-OSS-120B ↔ DeepSeek Chat 전환 | Hermes Agent |
|| 2026-06-01 | v9.2 4개 Priority 추가: ArchitecturalJudgmentGate · SIA · MonitoringEngine · ModelLoadBalancer · Tag/Exec 보안 3중 필터 | MJ님 |
|| 2026-06-01 | /reduce 명령어 상세 설명 추가 + 목차 업데이트 | MJ님 |
|| 2026-05-31 | 초안 작성 (v8.5~v9.1 전체 기능) | Antigravity |

> **이 파일에 계속 추가하는 방법**: 새로운 기능에 대해 질문하거나 개발이 완료되면, 이 파일의 해당 섹션에 내용을 덧붙인다. 목차의 링크도 함께 업데이트할 것.

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
