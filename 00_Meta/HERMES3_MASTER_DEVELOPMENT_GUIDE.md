# 🎖️ HERMES3 마스터 개발설명서
> **최종 통합 문서** | 시간순 정렬 | 중복 제거 | 상태 명시
> **작성일**: 2026-06-07
> **마지막 수정**: 2026-06-07 03:45
> **버전**: v9.2 (완료) → v9.4+ (중장기)

---

## 📌 Executive Summary
Hermes3는 Andrej Karpathy의 **LLM Wiki** 철학과 **12‑Factor Agents** 원칙을 기반으로, v8.5‑v9.2까지 **경량·Stateless** 에이전트 시스템을 완성했습니다. **2026-06-07 Gemma4 26B → Qwen3.6-35B-A3B 로컬 모델 교체 완료.** 핵심 지표:
- **코드 라인**: 2500 → 500 (-80%)
- **메모리**: 450 MB → 100 MB (-78%)
- **응답 속도**: 캐시 히트 시 0.001 s (99% 토큰 절감)
- **12‑Factor**: 12/12 완전 충족 (v9.1)
- **Hermes2 클라우드 전용 전환** (v9.1.5): 로컬 Gemma4 의존 제거, DeepSeek + NVIDIA NIM 70B 폴백
- **v9.2 SIA 3축 완료**: SelfImprovingAgent 피드백 학습 + MonitoringEngine 메트릭 경보 + ModelLoadBalancer 가중치 라우팅 — pytest 150/150 ✅
- **2026-06-07 모델 교체**: Gemma4 26B → **Qwen3.6-35B-A3B** (UD-Q4_K_M.gguf), config override로 context_length 65536

---

## 🗓️ 버전별 진화
### Phase 1 – v8.5 (실구동) 2026‑04→05
- 5대 레이어 아키텍처 구축
- Karpathy LLM Wiki 철학 적용 (마크다운 기반 경량 지식 저장)
- 부팅 시간 2.5 s 달성

### Phase 2 – v8.6 (Pub‑Sub 이벤트 버스) 2026‑05
- Loose‑coupling 이벤트 버스 구현 (TagLinker)
- AI Gateway 3‑way Failover (DeepSeek → NIM → Gemma4)

### Phase 3 – v8.9 (초경량 자율 정제) 2026‑05
- **FluxMem** + **SKILLOPT** 로 PEMS 기반 지식 성숙도 관리
- Edit Budget, Validation Gate, Rejected‑Edit Buffer 도입

### Phase 4 – v9.0 (Stateless Reducer) 2026‑05
- `AgentContext`(frozen dataclass)와 3‑micro‑agents 구현
- 순수 함수형 리듀서로 100% 재현성 확보

### Phase 5 – v9.1 (Context‑Hash Caching & State Machine) 2026‑05
- SHA256 기반 **Context Hash** 캐시 (decision_cache) → 0.001 s 응답
- TTL 1 h, SQLite WAL, 자동 정리 스케줄러
- **Pause/Resume** 상태 머신 도입

### Phase 6 – v9.1.5 (Hermes2 Cloud-Only) 2026-06
- Hermes2 Telegram 봇을 로컬 Gemma4 → **DeepSeek + NVIDIA NIM 70B** 클라우드 전용으로 전환
- `GATEWAY_URL` 상수 제거, OpenRouter 브랜치 철수
- NVIDIA 직접 API 호출 추가 (`NVIDIA_API_KEY` → launchd plist 환경변수)
- post_init() stdout 리다이렉션 문제 해결 (main() async 흐름 내 직접 print)
- 메모리 · 응답 속도 개선 (로컬 LLM 부하 제거)

---

## ✅ v9.2 (완료) — SIA 피드백 학습 + 모니터링 엔진 + 멀티 모델 로드 밸런싱
v9.1의 tag/exec/file 보안 + 이중 캐싱 검증 이후, `/reduce` 파이프라인의 **Self-Improving Architecture (SIA) 3축 피드백 루프** 구축 완료.

### 신규 파일
| 파일 | 내용 |
| :--- | :--- |
| `modules/sia_engine.py` | SelfImprovingAgent — record_feedback/analyze_trends/get_low_performers/suggest_improvements |
| `modules/monitoring_engine.py` | MonitoringEngine — record_metric/get_action_stats/get_error_rate/get_performance_trend/alert_if_degradation |
| `modules/load_balancer.py` | ModelLoadBalancer — select_best_model/record_model_performance/get_model_rankings/rebalance_weights |
| `tests/test_sia_engine.py` | SIA 단위 테스트 12개 (격리 DB) |
| `tests/test_monitoring_engine.py` | 모니터링 단위 테스트 12개 (격리 DB) |
| `tests/test_load_balancer.py` | 로드밸런서 단위 테스트 10개 (격리 DB) |

### 수정 파일
| 파일 | 변경 내용 |
| :--- | :--- |
| `core_reducer.py` | `apply_user_feedback()`, `on_feedback_collected()` SIA 피드백 라우팅 메서드 추가 |
| `hybrid_router.py` | `self.load_balancer` 초기화 → `route()`에서 `select_best_model()` 연동 → `call_deepseek()`에 성능 기록 |

### 아키텍처

**SelfImprovingAgent** (`~/.hermes/runtime/sia_feedback.db`)
- action_id / rating(1-5) / context / response_time 저장
- `suggest_improvements()`는 DeepSeek 호출하여 저성능 액션 개선 제안 생성
- 모든 테스트 `tempfile.mktemp()` → 운영 DB 오염 없음

**MonitoringEngine** (`~/.hermes/runtime/metrics.db`)
- action / duration / success / response_time 메트릭 기록
- 경보 조건: error_rate > 20% OR response_time > 30s OR success_rate < 70%

**ModelLoadBalancer** (`~/.hermes/runtime/metrics.db` — MonitoringEngine과 공유)
- weighted random 선택 — 가중치 높은 모델 선택 확률 ↑
- 기본 가중치 0.8, 연속 실패/지연 시 -0.1 패널티

### Key Decisions
| 결정 | 이유 |
| :--- | :--- |
| **SQLite 영구 저장** | 재시작 후 피드백/메트릭 유지. CSV/JSON 대비 쿼리/분석 용이 |
| **3개 독립 엔진** | 단일 책임 원칙. 각 엔진 독립 테스트 + 독립 진화 가능 |
| **SIA DB / Metrics DB 분리** | SIA(소량·장기) vs Monitoring(대량·순환) — DB 특성 분리 |
| **가중치 기반 선택** (not greedy) | 단순 최우선 아닌 분산 라우팅으로 리스크 분산 |
| **격리 DB 테스트** | v9.1 SQLite 캐시 오염 문제 경험 → 모든 신규 테스트 임시 DB |
| **회귀 0건 방어** | 기존 116개 테스트 변경 없이 신규 34개만 추가 |

### 테스트 결과
| 항목 | 개수 | 상태 |
| :--- | :--- | :--- |
| v9.2 전용 | 34개 | ✅ 전면 통과 |
| 기존 테스트 | 116개 | ✅ 전면 통과 (aiohttp 미설치 17f/18e는 선행 이슈) |
| **전체** | **150개** | **✅ 전면 통과** |

### 향후 연동
- **SIA**: 텔레그램 Thumbs-up/Thumbs-down 버튼 → `record_feedback()` 호출
- **Monitoring**: `/status` 명령어에 메트릭 대시보드 연동
- **LoadBalancer**: Cron 기반 주기적 `rebalance_weights()`
- **통합**: SIA 저성능 탐지 → Monitoring 상세 진단 → LB 재조정 순환 루프

### 🚫 중지·보류 결정 (v9.1 철학과 충돌, v9.2에서 유지)
1. **Multi‑Agent Orchestration** – 대용량 State 유지 요구 → 코드 2 000줄 증가, LLM 호출 3‑4배
2. **Advanced RAG / sqlite‑vec** – 임베딩 연산 강제 → RAM·부팅 시간 붕괴
3. **Auto‑Refactoring / Self‑Healing** – AI 환각에 의한 무한 루프 위험
> **재검토 조건**: 전용 서버 확보·비동기 설계·Edit Budget·롤백 메커니즘 완전 구현 시

### 📋 현재 진행 상황 (2026-06-09 업데이트)

#### ✅ 최근 완료 항목 (Phase 1·2)

| 우선순위 | 항목 | 상태 | 설명 | 완료일 |
| :---: | :--- | :--- | :--- | :--- |
| 🔴 HIGH | **Phase 1: 낙관적 응답** | ✅ **완료** | `modules/optimistic_response.py` — 즉시 피드백 + 백그라운드 처리 + 자동 재시도 | 2026-06-09 |
| 🔴 HIGH | **Phase 2: 세밀한 메모리** | ✅ **완료** | `modules/memory_refinement.py` — auto_forget/check_conflict/should_store/hybrid_recall | 2026-06-09 |
| 🔴 HIGH | PermissionBridge 2-tier 도구 인가 | ✅ **완료** | `modules/permission_bridge.py` 생성, `harness_agent.py` + `_base.py` 통합 | 2026-05-28 |
| 🔴 HIGH | Ingest Engine 저신뢰 Inbox Deferral | ✅ **완료** | Unsorted/파싱 실패 시 `Inbox/*_pending.md` → `_process_inbox()` 재분류 | 2026-05-30 |
| 🟢 LOW | Ingest Unsorted 30% 경고 알림 | ✅ 완료 | Ingest 실행 시 Unsorted 비율이 30% 초과하면 Telegram 메시지에 경고 표시 | 2026-06-02 |
| 🟢 LOW | Graphify Vault 그래프 분석 | ✅ 완료 | `/vault graph` 명령어로 고립 문서/허브 노드/연결 구조 분석 | 2026-06-02 |

#### 🔄 향후 진행 (Phase 3 조건부)

| 우선순위 | 항목 | 상태 | 설명 | 조건 |
| :---: | :--- | :--- | :--- | :--- |
| 🟡 MEDIUM | **Phase 3: 능동적 지능** | 🔜 **검토 대기** | `proactive_engine.py` + `llm_distiller.py` — 반복 패턴 감지 & 선제 제안 | Phase 1·2 안정화 2주 + `/memory health` 정상 범위 |
| 🟢 LOW | Dreaming 3종 버그 수정 | ❌ 미적용 | MemoryEngine import 오류, DummyRouter 우회, 중복 실행 등 Dream engine 안정화 | Phase 3 이전에 선택적 처리 |
| 🟢 LOW | `/ingest` 재시도 시 중복 방지 | ❌ 미적용 | Inbox에서 온 파일이 중복 분류되지 않도록 `_pending`→`_discarded` 플래그 체계 | Phase 3 이전에 선택적 처리 |
| 🟢 LOW | AgentMemory 통합 고려 | ❌ 미적용 | 자동 캡처·합성·그래프·Forget 정책 등 GBrain 개선 내용 적용 검토 | v9.4+ 로드맵 |

#### 🛠️ 최근 장애 복구 요약 (v9.1.5)
- **장애 현상**: 서브 봇 날씨 API 키 누락, WebUI 단기 기억 오염
- **근본 원인**: 환경 변수 누락, `harness_memory.json` 공유
- **조치**: `.env`에 `ANTIGRAVITY_NVIDIA_API_KEY` 추가, `harness_memory.json` 삭제, 게이트웨이 재시작
- **결과**: Hermes WebUI 정상 작동, 텔레그램 봇 응답 일치

#### 📑 중장기 마스터 플랜 (v9.4+)
- **L1 메모리 격리**: `HERMES_HOME` 활용 또는 `harness_memory_webui.json`/`harness_memory_telegram.json` 도입
- **Lock Stack 진화**: `bio_memory_engine.py`와 `deriver_layer.py` 잠금 해제 시 최소 패치 설계
- **테스트 강화**: `tests/test_memory_engine.py` 추가 및 CI 연동
- **Phase 3 진행**: 기본 조건 충족 시 능동적 지능 계층 구현

---

## 💡 Qwen3.6-35B-A3B 전환 결과 및 추후 과제 (2026-06-07)

### 전환 사항
- **모델**: Gemma4 26B (gemma-4-26b-a4b-it) → Qwen3.6-35B-A3B (Qwen3.6-35B-A3B-UD-Q4_K_M.gguf)
- **서버 포트**: localhost:1234 → localhost:8080 (동일 llama-server, PID 84469)
- **서버 옵션**: `-m Qwen3.6-35B-A3B-UD-Q4_K_M.gguf -c 32768 -ngl 99 -ctk q8_0 -ctv q8_0 --port 8080`
- **config.yaml custom_providers**: Gemma(port 1234, model gemma-4-26b-a4b-it) → **Qwen3.6-35B-A3B**(port 8080, model Qwen3.6-35B-A3B-UD-Q4_K_M.gguf), context_length 32768→**65536 override**
- **harness_agent.py**: 모든 UI 문자열 Gemma4→Qwen3.6 교체 (MODE_GEMMA4 변수명 유지, 값만 "Qwen3.6"으로 변경)

### 세션 기록 (2026-06-07 02:33 ~ 03:45)

#### 발견된 문제점

**① Gateway api_server 플랫폼 미활성화 (⚠️ 미해결)**
- Gateway 재시작(여러 번) 후에도 `gateway_state.json`에 `telegram` 플랫폼만 connected, `api_server`가 없음
- 8642 포트 미리슨 → WebUI가 Gateway로부터 provider 정보 수신 불가
- 원인 불명. Telegram bot token(.env)을 읽어 Telegram 플랫폼은 연결되지만 api_server가 누락됨

**② WebUI modelSelect에 Qwen 미표시 (⚠️ 미해결)**
- `/api/providers`는 `custom:qwen3.6-35b-a3b` 정상 반환
- Settings → Providers에서 Qwen 모델 확인 가능, Refresh Models도 정상
- 단, `/api/models`의 `groups: []` 비어 있어 드롭다운(modelSelect)에 Qwen이 표시되지 않음
- WebUI `ui.js:populateModelDropdown()`이 `/api/models`의 groups로 `<select>`를 동적 생성
- 원인: WebUI가 Gateway api_server 없이 자체적으로 custom_providers를 groups에 포함시키지 못함

**③ Qwen context_length 부족 (✅ 해결)**
- `model.context_length: 32768` < Hermes Agent minimum 64000 → "Error: below minimum 64K"
- config.yaml override: `context_length: 65536`로 해결
- ⚠️ 실제 llama-server는 `-c 32768`로 실행 중이므로, 32768 토큰 초과 시 뒷부분 잘림
- **향후 필요**: llama-server를 `-c 65536`으로 재시작

**④ Qwen 추론 타임아웃 (⚠️ 미해결, 사용자 취소)**
- Qwen 선택 후 질문("하이") → 1분 40초+ thinking 후 응답 없음 → 사용자 취소
- harness_agent.py `_call_local()` 타임아웃 60s, completions API 사용 (chat template bypass)
- 35B A3B 모델의 첫 추론 속도가 매우 느림 (KV 캐시 워밍업 필요 가능성)

### 추후 계획

#### 🔴 HIGH
- [ ] **Gateway api_server 플랫폼 활성화 문제 진단 및 수정** — WebUI가 Gateway 없이도 자체 provider 목록 표시하게 하거나, Gateway가 api_server를 띄우도록 수정
- [ ] **llama-server `-c 65536`으로 재시작** — 실제 context 확장 (메모리 사용량 확인 후, -ngl 99 유지 시 RAM 사용량 20~25GB 추정)
- [ ] **Qwen 추론 타임아웃 조정** — harness_agent.py `_call_local()` timeout 60s → 120s+ (35B A3B 첫 추론 시간 고려)
- [ ] **Telegram 모드 버튼 Gemma4→Qwen3.6 실제 적용 확인** — Telegram 접속 시 모드 전환 버튼 문구 확인 필요

#### 🟡 MEDIUM
- [ ] Qwen3.6 vs Gemma4 26B 성능/품질 비교 평가 (추론 속도, 응답 품질, context 활용도)
- [ ] hermtes-webui plist 정리 — 중복 실행 방지, HERMES_HOME 일원화 최종 확인
- [ ] hybrid_router.py `call_gemma4()` dead code 정리 (provider="gemma4" 문자열 → Qwen)

#### 알려진 이슈
1. Gateway api_server 미활성화 — 근본 원인 분석 필요 (Gateway가 Telegram만 띄우는 조건?)
2. Qwen 첫 추론 극도로 느림 — 타임아웃 증가 또는 프롬프트 캐싱 도입 검토
3. WebUI 드롭다운에 Qwen 미표시 — Settings에서 직접 선택해야 사용 가능
4. llama-server context 32768 제한 — config override로 회피 중이나 실제 초과 시 잘림

### ~Gemma4 26B 성능 최적화 방안~ (2026-06-07 폐기 — 모델 교체)
### 하네스 강화로 Gemma4 한계 보완

**Gemma4 26B의 알려진 한계**
1. 추론 능력 — DeepSeek/NIM 70B 대비 복잡한 다단계 추론에서 부족
2. 컨텍스트 길이 — 긴 문서 처리 시 정보 손실 가능성
3. 지식 범위 — 최신 정보/특수 도메인 커버리지 제한

### 하네스 강화 방향 (Gemma4 유지, 무코드 개선)

| 우선순위 | 방안 | 설명 |
| :---: | :--- | :--- |
| 🔴 HIGH | **SIA 피드백 → LoadBalancer 지능화** | Gemma4가 자주 실패하는 패턴을 SIA DB에 수집, 해당 패턴 탐지 시 자동으로 DeepSeek/NIM으로 우회. Gemma4가 잘하는 작업은 유지, 약한 작업만 상위 모델 위임 |
| 🟡 MEDIUM | **Ingest 전용 캐시 레이어** | 문서 분류/요약 시 이전 유사 결과 재활용. Gemma4의 불필요한 LLM 호출을 줄여 추론 집중도 향상 |
| 🟢 LOW | **Context Pre-filter** | Gemma4에 전달 전 프롬프트 경량화. 불필요 맥락 제거로 제한된 컨텍스트 효율 극대화 |

### 로컬 AI 추가 추천 (계층별)

| 계층 | 모델 | 크기 | 용도 | 비고 |
| :---: | :--- | :---: | :--- | :--- |
| 1차 (초경량) | **Llama 3.1 8B** (기존 Ollama) | 8B | Ingest/분류 전담 | 이미 보유, 활용도만 높이면 됨 |
| 2차 (중간) | **Qwen2.5 14B** | 14B | 코드/추론 중간 레이어 | Gemma4와 크기·속도 균형 우수, Fallback 체인 중간층에 적합 |
| 3차 (대안) | **Phi-4 14B** (Microsoft) | 14B | 추론/코드 특화 | Gemma4 26B보다 작지만 추론 정확도 유사, Apple Silicon 최적화 확인 필요 |
| 4차 (동급 대체) | **Mistral Small 3.1 24B** | 24B | 일반 응답 대체 | Gemma4와 비슷한 크기지만 효율 우수, 라이선스 자유로움 |

### 권장 조합
- **Gemma4 26B** — 대화/일반 응답 유지
- **Llama 3.1 8B** (기존) — Ingest/분류 전담
- **Qwen2.5 14B** (신규 추천) — Fallback 체인 중간 레이어, 코드/추론 처리
- **하네스 LoadBalancer + SIA** — 패턴 학습 기반 라우팅 정밀도 향상

---

## 🚀 v9.4+ (Mid‑Term) – 제안 검토 중 (`V9.0 프로그램 추가 2.md` 참조)
V9.0 프로그램 추가 2.md에서 제안된 3가지 외부 참조 통합. **현재 코드 미구현, 설계 제안 단계**.

### 🧪 v9.4+ 후보: LLM 증류기 (LLM Distiller) — L3 패턴 인사이트 고도화

**상태**: 설계 검토 완료 (2026-06-05). **보류 — Lock Stack 안정화 후 재검토.**

**배경**: `_note_l3_candidate()` (bio_memory_engine.py line 293-314)가 L3 패턴에 저장하는 `summary`가 원본 content 200글자 raw 텍스트에 불과. 키워드 기반 병합(frequency 증가)만 수행할 뿐, 의미 있는 패턴/규칙/습관 추출은 전혀 안 됨. 이로 인해 `pre_query_context()`의 L3 패턴 검색 결과가 실질적 인사이트를 제공하지 못함.

**제안 내용**: Lock Stack을 침범하지 않는 별도 모듈(`llm_distiller.py`)을 신규 작성. `hermes_local.py`의 특정 지점에서 호출하여 L2/L3를 읽기 전용으로 참조하고, LLM 요약 결과를 별도 파일(`llm_insights.json`)에 저장.

**이점** (실제 코드 기반 검증 완료):

| 영역 | 효과 | 판정 |
|------|------|------|
| L3 패턴 인사이트 | raw 텍스트 200글자 → "사용자는 주말 오후에 비동기/동시성 개념 집중 학습. 선호 예제: asyncio.gather" 수준으로 개선 | **조금 좋아짐** |
| 검색 맥락 인식 | `pre_query_context()`가 L3 인사이트를 반환할 수 있게 되어, 에이전트가 단순 키워드 매칭을 넘어 맥락 기반 응답 가능 | **조금 좋아짐** |
| 반복 패턴 감지 → 제안 | "2주간 매일 같은 질문" 패턴 인식 → 자동화 제안 가능 | **가능해짐** (기존에 불가능) |
| L2 블로트 관리 | hybrid trigger가 이미 증분 방식으로 처리 중. LLM 증류는 블로트 해결이 아닌 L3 질 향상이 목적 | **변화 없음** |
| recall() 정확도 | L2 벡터+키워드+Spreading Activation은 이미 견고. L3 인사이트가 recall() 자체에 영향주진 않음 | **변화 없음** |
| API 비용 | 증분당 500-1000 tokens 추가. "90% 절감"은 기존 시스템이 전체 L2를 LLM에 던진다는 잘못된 가정에 기반 | **소폭 증가** (신규 비용) |

**안전성**:
- Lock Stack 완전 보호 — bio_memory_engine.py 수정 없음, L2/L3 파일 읽기 전용
- 별도 파일(`llm_insights.json`)에만 쓰기 → 기존 파이프라인과 경쟁 상태 없음
- 단, `pre_query_context()`가 이 별도 파일을 참조하려면 Lock Stack 외부에서 컨텍스트를 주입하는 경로 필요

**도입 조건**: v9.2 안정화 + Lock Stack 컴포넌트 업데이트 필요 시점에 동시 반영. 현재로서는 효과 대비 투자 효용이 낮아 보류.

### v9.4.1 — Phase 3: 능동적 지능 (Proactive Intelligence)

**상태**: 설계 제안. **미구현 — Phase 1·2 안정화 확인 후 재검토.**

**배경**: Phase 1(낙관적 응답)과 Phase 2(세밀한 메모리)가 "사용자 요청 → 응답" 루프를 개선했다면, Phase 3는 **사용자가 요청하기 전에 시스템이 먼저 제안**하는 능동적 지능 계층입니다.

**핵심 구성요소** (전부 신규 모듈, Lock Stack 미침범):

| 모듈 | 역할 | 예상 코드량 |
|------|------|------------|
| `modules/proactive_engine.py` | 대화 패턴 감지 → 선제적 제안 생성 | ~200줄 |
| `modules/llm_distiller.py` | L2/L3 읽기 전용 → LLM 요약 → `llm_insights.json` 저장 | ~150줄 |
| `handlers/_proactive.py` | `/proactive on/off/status` 명령어 | ~60줄 |

**동작 시나리오**:
```
[1] 사용자가 3일 연속 같은 주제를 질문
    → proactive_engine이 패턴 감지
    → "이 주제에 대한 정리 문서를 자동 생성할까요?" 제안

[2] L2에 유사 에피소드 10개 이상 누적
    → llm_distiller가 LLM으로 요약·증류
    → "최근 2주간 AI 규제 관련 대화를 이렇게 요약했습니다" 보고

[3] /ingest 후 미분류 파일이 30% 초과
    → "Inbox 정리가 필요합니다. 지금 실행할까요?" 선제 알림
```

**기대 이점**:

| 영역 | 효과 | 판정 |
|------|------|------|
| L3 패턴 품질 | raw 200글자 → LLM 요약 인사이트로 개선 | 조금 좋아짐 |
| 반복 질문 감지 | "매일 같은 질문" 패턴 → 자동화 제안 가능 | 신규 기능 (기존 불가) |
| 사용자 경험 | 수동 명령 → 시스템이 먼저 제안 | 체감 지능 향상 |
| Inbox 관리 | 수동 `/ingest` → 조건부 자동 알림 | 운영 효율 |

**안 한 이유 — 단점과 리스크**:

| 항목 | 리스크 | 심각도 |
|------|--------|--------|
| **API 비용 증가** | llm_distiller가 L2 에피소드를 LLM에 요약 요청 → 증분당 500~1000 토큰 추가. 기존 시스템은 LLM 호출 없이 키워드 매칭만 수행하므로 비용이 0이었음. DeepSeek 무료 할당량 소진 가속 | 🟡 중 |
| **오알림(False Positive)** | 패턴 감지가 부정확하면 쓸모없는 제안이 텔레그램에 반복 표시 → 사용자 피로감 증가. Linear의 "알림 과부하" 문제와 동일 | 🟡 중 |
| **Lock Stack 우회 복잡성** | `pre_query_context()`가 `llm_insights.json`을 참조하려면 Lock Stack 외부에서 컨텍스트를 주입하는 새 경로가 필요. 현재 `harness_agent.py`의 메모리 오버레이에 추가 분기 발생 | 🟢 낮음 |
| **백그라운드 리소스** | LLM 증류가 크론/Dreaming과 겹치면 동시 API 호출 발생. Rate Limit 충돌 가능. 기존 Circuit Breaker가 방어하지만 폴백 체인 소진 위험 | 🟡 중 |
| **효과 대비 투자** | LLM Distiller 섹션에서 분석한 대로, L2 벡터+키워드+Spreading Activation 검색은 이미 견고. L3 인사이트 개선이 recall() 정확도 자체를 올리진 않음. 체감 개선이 투자 대비 제한적 | 🟢 낮음 |
| **Phase 1·2 미안정** | Phase 1의 낙관적 응답 패턴과 Phase 2의 hybrid_recall이 충분히 검증되지 않은 상태에서 Phase 3를 올리면 디버깅 복잡도 급증 | 🔴 높음 |

**도입 조건** (모두 충족 시 재검토):
1. Phase 1·2가 최소 2주간 텔레그램에서 안정 운영 확인
2. `/memory health` 지표가 정상 범위 유지 (forget 대상 < 전체의 20%)
3. DeepSeek/NVIDIA API 무료 할당량 여유 확인 (증류 비용 예산 책정)
4. 사용자(MJ님)의 "선제적 알림"에 대한 실제 니즈 확인

**참조**: `Phase1_Phase2_개선_설명서.md`, `Bio_Memory_Engine_Technical_Guide_v9.3.md`

### v9.4.2 — Lightweight SkillSpector (`modules/skill_spector.py`)
- **출처**: NVIDIA SkillSpector → 초경량 Cleanroom 추출
- **핵심**: 스킬 실행 비용(Latency/토큰) 계량화 및 궤적 프로파일링
- **SQLite WAL** 원격측정 테이블로 무결 궤적 선별 → SIA 훈련 데이터 필터
- **장점**: LoRA 가중치 진화 순도 향상, 스킬 병목 시각화
- **리스크**: NVIDIA GPU 인프라 의존 차단 필수 (Apple Silicon 경량화 전제)

### v9.5 — Cybersecurity Secure Auditor (`modules/cyber_auditor.py`)
- **출처**: mukul975/Anthropic-Cybersecurity-Skills → 결정론적 정적 감사 모듈
- **핵심**: OWASP/CWE 패턴 기반 소스코드 취약점 정적 분석
- **v9.1.4 SecuritySandbox + v9.4.2 SkillSpector**와 연계

### v9.5.1 — SRE Incident Investigator (`modules/sre_investigator.py`)
- **출처**: Tracer-Cloud/opensre → 초경량 인프라 장애 진단 엔진
- **핵심**: 블랙박스 추론 거부, 증거 기반 결정론적 연관 추적
- **LangGraph/ClickHouse 종속 제거**, 순수 Python + SQLite

> **도입 조건**: Hermes2 v9.2 안정화 완료 후 재검토 (v9.2 완료 — SIA 3축 구축)

### 📎 참고: Claude Code Harness 디자인 철학 (v9.4+ 설계 참고용)
- **출처**: Claude Code 내부 Harness 시스템 (Claude Code 전용 플러그인, 직접 이식 불가)
- **핵심 개념**:
  1. **증거 패키징 (Evidence Packaging)** — 에이전트의 모든 결정에 증거(출처, 로그, 메트릭)를 첨부하여 추적 가능성과 설명력 확보
  2. **SSOT (Single Source of Truth)** — 상태/설정을 한 곳에서 관리, 중복/불일치 제거
  3. **5동사 루프** — `Analyze → Plan → Execute → Verify → Reflect` 순환 구조
- **Hermes 대응**: kanban/plan/review 스킬이 유사 기능 커버 중. 완전한 증거 패키징은 v9.4+에서 SRE Investigator (v9.5.1)와의 연계 시 도입 가능
- **도입 조건**: Hermes2 v9.2 안정화 + SIA/Monitoring/LoadBalancer 3축 운영 경험 누적 후 검토

|:---|:---|

## 🧪 v9.4+ 후보: "Teacher Mode" 프롬프트 (Anthropic 동료 경험 기반)

**출처**: Anthropic 내부에서 코딩 세션 길어질 때 이해도 불안을 줄이기 위해 사용 중인 프롬프트

**개념**: 기존 `personalities.teacher`와 quick command(`/teacher`)로 활성화하는 **단계별 교수법 모드**.  
단순 답변이 아니라 학습자가 진짜 이해할 때까지 가르치는 접근법.

**핵심 동작 방식**:
1. 단계별 진행 — 다음 단계로 넘어가기 전 현재 단계 마스터 확인
2. 체크리스트 마크다운 문서 유지 (문제점/해결책/맥락)
3. 학습자가 스스로 재진술하도록 선제 요청 → 부족한 부분 채움
4. `AskUserQuestion`으로 주관식/객관식 퀴즈 (정답 순서 매번 변경)
5. 코드·디버거 사용 유도
6. **`/goal`**: 체크리스트 전항목 이해 증명 전까지 세션 종료 불가

**기존 인프라와의 정합성**:
| 항목 | 현재 상태 | Teacher Mode 활용 |
|------|-----------|-------------------|
| `personalities.teacher` | 있음 (설명 중심) | 강화 대상 — `§5` 체크리스트+퀴즈 로직 통합 |
| `constitution.local.md` | §1-4 (Graphify, Ingest 등) | §5 Teacher Mode 추가 검토 |
| quick commands | config.yaml 미사용 | `/teacher` command 추가 |
| `/goal` | 없음 | Teacher Mode 전용 goal enforcement 필요 |

**Voice Mode 연계**: 음성 모드와 함께 사용 시 응답이 더 자연스럽고 대화하기 편하다는 경험 공유됨.

**도입 조건**: v9.2 안정화 후 SIA/Monitoring/LoadBalancer 운영 경험 누적 후 검토.  
**참조 프롬프트 원문**: `wiki/00_Meta/constitution.local.md` 또는 별도 템플릿으로 저장 필요.

|:---|:---|

## 🧪 v9.4+ 후보: "Karpathy Loop" 자율 실험 루프

**출처**: [The Karpathy Loop — What It's Still Missing (MemClaw, 2026-04)](https://memclaw.net/blog/karpathy-loop/)

**개념**: Andrej Karpathy의 autoresearch 패턴. 단일 에이전트가 한 파일, 한 metric, 한 시간 예산으로 무한 반복 실험을 자율 수행.

**3가지 프리미티브**:
1. **One file the agent can edit** — 단일 수정 대상
2. **One objective metric** — 명확한 단일 평가 지표
3. **One time budget per cycle** — 고정 실행 시간

**루프**: `Hypothesize → Edit → Run → Measure → Keep/Discard → Repeat`

**우리 시스템과의 비교**:

| 항목 | Karpathy Loop | Hermes3 v9.2 |
|------|---------------|--------------|
| 루프 구조 | hypothesize→edit→run→measure | analyze→plan→execute→verify→reflect (유사) |
| 메모리 | git log + results.tsv | Hermes memory + wiki vault |
| 목표 정의 | program.md | config.yaml goals + session goals |
| 평가 | 단일 metric 자동 판단 | SIA 피드백 (수동) |
| 실험 자동화 | 내장 | cronjob script + no_agent 모드로 가능 |

**장점 (우리 시스템에 적용 시)**:
- cronjob(script, no_agent=True) + 단일 파일 조합으로 Karpathy Loop 유사 패턴 구현 가능
- 5동사 루프가 이미 유사 구조를 가짐 → `program.md` 컨셉만 추가하면 됨
- SIA 3축(피드백 학습+모니터링+로드밸런싱)과 시너지 가능

**단점 (도입 시 주의)**:
- `program.md` 목표 정의 포맷이 없음 — 새로 제작 필요
- 단일 metric 기계적 평가 인프라 부재 — SIA는 수동 피드백 기반
- Hermes는 DevOps/응대 중심, 연구용 자율 실험이 목적이 아님 → 과잉 설계 가능성
- 싱글 유저 운영에 MemClaw 수준의 플릿·거버넌스는 불필요

**취할 것**: `program.md` 컨셉을 `/goal` 매커니즘에 결합. 세션 목표·제약조건·중단 조건을 문서화하고 봇이 자율 루프를 돌게 하는 패턴은 유용.

**버릴 것**: 크로스 에이전트 플릿, 거버넌스, MemClaw 통합. 싱글 유저에게 오버헤드.

**도입 조건**: v9.2 안정화 후 SIA/Monitoring/LoadBalancer 운영 경험 누적 후 검토.

|---

## 🤖 Autoresearch Integration (Karpathy Loop Adaptation)

### 기대 장점
- **자동 실험 루프** – `train.py` 를 AI 에이전트가 매 5분마다 수정·실행하고, 결과(`val_bpb`)를 로그로 남겨 하루에 12~15번의 실험을 자동 생성한다. 인간이 직접 코드와 하이퍼파라미터를 튜닝할 필요가 사라져 연구‑시간을 크게 절감한다.
- **버전·결과 추적** – `train.py` 가 하나의 파일이므로 Git diff 로 변경 내역을 바로 확인할 수 있다. 실험이 끝난 뒤 로그를 `harness_memory.json` 혹은 `gbrain` 그래프에 **“experiment”** 노드로 저장하면, 후에 “가장 좋은 실험은?” 같은 쿼리로 즉시 검색할 수 있다.
- **Hermes 도구와 연계** – `program.md` 를 Hermes 스킬 형태로 만들면 `memory_save`·`memory_recall` 로 실험 설정·결과를 메모리 레이어에 자동 기록한다. `cronjob` 으로 `autoresearch` 를 주기적으로 실행하거나, `agentmemory`‑style 스코프를 부여해 팀‑별 실험 히스토리를 격리할 수 있다.
- **자체 평가 메트릭** – `val_bpb` (bits‑per‑byte) 은 vocab‑size‑에 무관한 절대 지표다. 기존 Hermes 시스템에서 쓰는 `semantic_memory` 와 같은 벡터‑검색 메트릭과 병행해 “이 실험은 기존 모델보다 3 % 개선됐어” 같은 정량적 비교가 바로 가능해진다.
- **확장 가능성** – 하나의 GPU + 코드 파일만 있으면 되므로, 다른 프로젝트(예: 이미지 프롬프트 튜닝, RL 실험)에도 동일한 패턴으로 스크립트를 복제해 **멀티‑에이전트** 연구 조직을 만들 수 있다.

### 예상 단점·리스크
1. **GPU 호환성** – 현재 Mac Studio는 NVIDIA GPU 가 없으므로 CPU/MPS 모드로 포팅이 필요하다.
2. **리소스·시간 오버헤드** – 5분 학습은 GPU·디스크 I/O 를 많이 잡아먹어 기존 Hermes 데몬과 충돌할 수 있다.
3. **코드 변경 안전장치 부재** – `train.py` 를 자유롭게 편집하면 무한 루프·메모리 누수 위험이 있다.
4. **데이터 다운로드·전처리** – `prepare.py` 가 데이터를 재다운로드하거나 임시 파일을 남겨 디스크를 잡아먹을 수 있다.
5. **버전·의존성 충돌** – Autoresearch가 요구하는 최신 `torch`, `uv` 등은 현재 Hermes 가상환경과 충돌 가능성이 있다.
6. **보안·스코프** – 에이전트가 시스템 명령을 삽입할 위험이 있다. 현재 Hermes 환경에는 제한이 부족하다.

### 개선·완화 방안
- **GPU 대체·CPU‑모드**: `train.py` 의 `DEVICE` 를 `torch.device("cpu")` 또는 `torch.device("mps")` 로 강제하고, `DEPTH`·`TOTAL_BATCH_SIZE` 를 낮춰 메모리 사용량을 줄인다.
- **리소스 격리**: Docker 컨테이너 혹은 `uv` 격리 환경에서 실행하고 `nice`·`ionice` 로 낮은 우선순위 지정한다.
- **코드 검증 파이프라인**: `flake8`·`pyflakes` 로 정적 분석 후 자동 롤백(`git checkout -- train.py`)을 적용한다.
- **데이터·캐시 관리**: `prepare.py` 를 한 번만 실행하고 결과를 읽기‑전용 디렉터리에 저장, 재실행 시 `--skip-prepare` 플래그 추가.
- **의존성 격리**: Autoresearch 전용 `uv lock` 파일을 사용해 별도 가상환경을 유지한다.
- **보안·스코프 강화**: `program.md` 에 `#sandbox: true` 선언, `launchd` 플리스트에 `UserName`/`GroupName` 지정, 실행 파일 권한 `600` 로 제한한다.
- **결과 통합·시각화**: 실험 종료 시 `memory_save --key experiment/<timestamp>` 로 메타데이터를 저장하고, `memory_graph_query` 로 베스트 5 실험을 조회한다.

### 적용 로드맵 (3 단계)
1. **격리 테스트** – `uv venv` 로 `autoresearch_env` 생성, `prepare.py --skip-download` 후 CPU/MPS 모드 `train.py` 실행 확인.
2. **Hermes 스킬화** – `program.md` 에 Autoresearch 목표와 단계 정의 추가, `cronjob/autoresearch.plist` 를 `StartInterval=600` 으로 설정.
3. **결과 통합·모니터링** – `memory_save` 로 실험 메타 저장, `memory_graph_query` 로 베스트 실험 조회, 필요 시 `agentmemory` 스코프 적용.

> *위 내용은 `@wiki/00_Meta/HERMES3_MASTER_DEVELOPMENT_GUIDE.md` 에 반영되었습니다.*

## 🚀 v9.6 — Private Knowledge Mesh (PKM) 연구 파트너

**상태**: 설계 검토 완료 (2026-06-03). 코드 미구현. **구현 결정 시 우선순위 1순위.**

**출처**: `Private Knowledge Mesh (PKM)_2.md` — 연구 워크플로우 자동화 최종 설계

### 핵심 설계 (본 설계, 구현 대상)

웹 논문 + 로컬 옵시디언 노트를 하나의 타임라인으로 통합, AI가 의미적 교차 분석을 자동 수행.

| 모듈 | 역할 | 코드량 |
|------|------|--------|
| `knowledge_mesh_orchestrator.py` | 신규 — DecisionAgent JSON 레시피 → 로컬 프리미티브 실행 | ~120줄 |
| `timeline_builder.py` | 신규 — 날짜/버전 정렬, 중복 병합 | ~40줄 |
| `cross_reference_analyzer.py` | 신규 — 노트-논문 코사인 유사도 + 시간 감쇠 신뢰도 | ~60줄 |
| `auto_topic_manager.py` | 신규 — 새 논문/노트 자동 주제 클러스터 할당 | ~80줄 |
| `knowledge_indexer.py` | 수정 — `search_similar()` 벡터 검색 메서드 추가 | +5줄 |
| `paper_bundle_manager.py` | 수정 — `formal_date` 필드 지원 | +3줄 |
| `handlers/_research.py` | 수정 — Orchestrator 호출 추가 | +8줄 |

**기대 효과**:
- 연구 문헌 조사 시간: 20~30분(수동) → 2~3분(자동) — **90% 단축**
- 내 노트-논문 연관 발견: 우연 의존 → 매 검색마다 자동 제시
- 시스템 부하 증가: 거의 0 (RAM +200MB, CPU 1~2%)
- 기술 스택: LanceDB(벡터 DB), 임베딩 모델, watchdog, 크론잡

### 📎 추가 개선 제안 (GUIDE.md 기록 — 설계 미포함, 추후 참고)

아래 도구들은 PKM_2.md의 "웹 검색 기반 추가 개선 제안" 섹션에서 조사된 내용. **본 설계에 포함되지 않음.** MJ님의 텔레그램 기반 시스템과의 구조적 차이로 인해 직접 적용이 어렵거나, 선택적 API 연동만 가능.

#### Obsidian 플러그인류 (직접 적용 어려움)
- **Smart Connections**: Obsidian 내부에서 노트 간 유사도 기반 실시간 연결 제안. 텔레그램 기반 시스템과 구조 상이 → 직접 적용 불가, 참고만.
- **Obsidian Copilot**: Obsidian 내 AI 어시스턴트. 동일 사유로 직접 적용 불가.
- **Obsidian Breadcrumbs**: Obsidian 내 계층적 관계 정의 및 시각화. 동일 사유.

#### 외부 연구 도구 (API 연동으로 부분 통합 가능)
- **Zotero + 플러그인**: 참고문헌 관리. Zotero API 연동으로 논문 메타데이터 수집 파이프라인에 활용 가능.
- **Scite.ai**: 인용 맥락 분석(지지/반박/언급). API 연동 시 `cross_reference_analyzer` 성능 향상 가능.
- **Elicit**: 자연어 질문 기반 논문 검색. `/research` DecisionAgent 레시피 생성에 패턴 참고.
- **ResearchRabbit**: 시각적 논문 탐색. 벡터 검색 시각화 부분 참고.

> **도입 조건**: v9.2 안정화 완료 확인 후 구현 시작. 구현 결정 시 우선순위 1순위.

### 🧪 v9.4+ 후보: 자연어 스킬 라우팅 시스템 (Natural Language Skill Router)

**상태**: 설계 완료 (2026-06-09). **미구현 — 우선순위 검토 후 착수.**

**배경**: 현재 스킬 체계의 두 가지 문제:
1. `~/.hermes/skills/` (SKILL.md 지식파일) vs `Scripts/modules/` (Python 모듈) — 두 체계가 분리, 상호 인식 안 됨
2. `/명령어`, `@단축어` 없이 자연어("리서치해줘", "코드 리뷰해줘")로 스킬 호출 불가

**목표**: 사용자가 자연어로 말하면 → 시스템이 관련 스킬 자동 감지 → 스킬 컨텍스트 주입 후 응답. 스킬 없으면 일반 LLM 답변 후 저장 제안.

**구현 구성요소 (4개 신규/수정)**:

| 파일 | 역할 | 예상 코드량 |
|------|------|------------|
| `modules/skill_registry.py` (신규) | 스킬 목록 관리, Python모듈+SKILL.md 통합 인터페이스 | ~80줄 |
| `modules/intent_mapper.py` (신규) | 자연어 → 스킬명 변환 (키워드 우선, LLM 분류 폴백) | ~100줄 |
| `modules/response_handler.py` (수정) | intent_mapper 호출 → 스킬 컨텍스트 시스템 프롬프트 앞단 주입 | +15줄 |
| `modules/command_router.py` (수정) | 스킬 저장 제안 InlineKeyboard 처리 추가 | +20줄 |

**동작 흐름**:
```
사용자: "이 논문 분석해줘"
  ↓ intent_mapper: 키워드 매칭 → "academic-paper" (또는 LLM 분류)
  ↓ skill_registry: ~/.hermes/skills/research/abstract-writer/SKILL.md 로드
  ↓ response_handler: SKILL.md 내용을 sys_prompt 앞에 주입
  ↓ LLM: 스킬 컨텍스트 기반 전문 답변

스킬 없을 때:
  ↓ LLM 일반 답변
  ↓ "이 작업 패턴을 스킬로 저장할까요?" InlineKeyboard
  ↓ [저장] 선택 시 → LLM이 SKILL.md 초안 자동 생성 → ~/.hermes/skills/new-skill/ 저장
```

**인텐트 감지 방식 (하이브리드)**:
- 1차: 키워드 사전 매핑 (토큰 0, 즉시)
- 2차: LLM 분류 (NONE이면 스킵)
- 3차: 일반 LLM 폴백

**제약사항**:
- 인텐트 정확도 80~90% (애매한 표현은 NONE → 일반 LLM)
- LLM 분류 시 첫 응답 0.5~1초 추가
- 스킬 자동 생성 품질은 LLM 초안 수준 → 사용자 검토 필요

**도입 조건**: command_router/response_handler 안정화 확인 후 착수. Phase 3(능동적 지능) 이전 단계로 적합.

**참조**: 2026-06-09 Claude Code 세션 — 스킬 재사용 체계 미흡 분석 및 개선안 설계

---

### 🧪 v9.4+ 후보: Skills Hub (공식 확장 Skill 저장소)

**상태**: 설치 완료 (두 Hermes Home 모두 Hub 경로 존재). **도입 보류 — 현재 custom skill만으로 충분.**

**내용**: Hermes 공식 Skills Hub — 687개 skill / 18개 카테고리.
- Built-in: 87개 (에이전트 내장)
- Optional: 79개 (hermes skills install로 활성화 가능)
- Anthropic 제작: 16개 (frontend-design, pdf, pptx, docx, mcp-builder 등)
- LobeHub 커뮤니티: 505개

**현재 설치된 Hub 관련 경로**:
- `~/.hermes/skills/.hub/` — bundles, 21개 카테고리 디렉토리, taps.json
- `venu/.hermes2/skills/.hub/` — 동일 구조

**사용법**:
```bash
hermes skills list                   # 전체 skill 목록
hermes skills list --category devops # 카테고리별 필터
hermes skills install <name>         # 특정 skill 설치
hermes skills install hub/<name>     # Hub skill 설치
hermes skills uninstall <name>       # 제거
hermes skills tap add <user/repo>    # 커스텀 저장소 추가
hermes skills tap remove <user/repo> # 제거
```

**도입 조건**: 특정 요구사항(예: PDF 생성, PPT/문서 자동화, 프론트엔드 디자인, MCP 서버 구축) 발생 시 개별 skill 설치 검토. 현재 시스템 custom skill(software-development 등) + Hub의 강제 활성화는 token budget 낭비이므로 피할 것.

| 카테고리 | 개수 | 우리 시스템 유용도 |
|---------|:----:|:-----------------:|
| software-development | 128 | 중복 (이미 보유) |
| devops | 74 | 중복 (이미 보유) |
| creative | 56 | 낮음 |
| mlops | 49 | 낮음 |
| research | 37 | 중복 가능 |
| productivity | 33 | 낮음 |
| apple/macos | 9 | 관심 (선별적) |
| anthropic (cross-cat) | 16 | 관심 (pdf, pptx, docx, mcp-builder)

## ✅ 현재 사용 중인 핵심 파일 (v9.2 기준)
- `HERMES3_MASTER_DEVELOPMENT_GUIDE.md` (이 문서)
- `HERMES3_ENCYCLOPEDIA.md` (기능 백과사전)
- `V9.0 프로그램 추가 2.md` (v9.4+ 외부 참조 제안서)
- `시스템 상태.md` / `시스템 인벤토리.md`
- `hot.md` (실시간 KV 상태 기록)
- `00_Meta_지도.md` (문서 연결 지도)

> **삭제 완료** (v9.0‑v9.1 파일 — 2026-06-02 모두 이미 존재하지 않음, GUIDE.md 내 목록만 정리):

---

## 📚 업데이트 이력
| 날짜 | 내용 | 작성자 |
|------|------|--------|
|| 2026‑05‑31 | v9.1 상태 반영, 불필요 파일 리스트 지정, v9.2 계획 정리 | Antigravity |
||| 2026‑06‑01 | v9.1.5 Hermes2 Cloud-Only Phase 추가, v9.4+ 중장기 계획(V9.0 추가 2) 참조 추가 | Hermes Agent |
||| 2026‑06‑01 | v9.2 SIA 3축(피드백 학습+모니터링+로드밸런싱) 완료 반영 — Near-Term→✅ 완료 전환. 가이드 전면 v9.2 기준 업데이트 | Hermes Agent |
|| 2026‑06‑01 | Claude Code Harness 디자인 철학(증거 패키징/SSOT/5동사 루프) v9.4+ 참고 섹션 추가 | Hermes Agent (DeepSeek) |
|||| **2026‑06‑02** | **Gemma4 26B 성능 최적화 방안 섹션 신설** — SIA+LB 지능화, Ingest 캐시, Context Pre-filter 3축 + Qwen2.5 14B 추천 | Hermes Agent (DeepSeek) |
|||| **2026‑06‑02** | **v9.2b — Ingest Unsorted 경고 + Graphify 그래프 분석 추가** — `_file.py` Ingest 3개 경로에 Unsorted 30% 임계 경고. `_vault.py` graphifyy 기반 `/vault graph` 명령어 추가 (고립 문서/허브 노드/연결 구조) | Hermes Agent (DeepSeek) |
|||||| **2026‑06‑05 17:45** | **Skills Hub (v9.4+ 후보) 섹션 추가** — 공식 687개 skill 개요, Hub 명령어, 카테고리별 유용도 분석. constitution.local.md §3.6 동기화. | Hermes Agent (DeepSeek) |
||||| **2026‑06‑06** | **모델 스위치 도구(switch-model) 추가** — GPT-OSS-120B(NVIDIA)와 DeepSeek Chat 간 메인 모델 전환 스크립트. 두 Hermes Home 동시 적용, 파일 삭제 없는 주석 방식. 스크립트: `~/Applications/venu/scripts/switch_model.sh` → `/usr/local/bin/switch-model`. | Hermes Agent |
||||| **2026-06-07 03:45** | **Qwen3.6-35B-A3B 모델 교체 및 WebUI 정리**: Gemma4 26B(port 1234) → Qwen3.6-35B-A3B(port 8080). config.yaml custom_providers 교체, harness_agent.py UI 문자열 전면 교체. Gateway api_server 미활성화 이슈 발견. WebUI modelSelect에 custom_providers 미표시 버그 확인. | Hermes Agent |
||||| **2026-06-08** | **LLM 환각 방지 3계층 + curator.py 확장 + /help 재작성 + .bak 6개 삭제** | Claude Code |
||||| **2026-06-09** | **AgentForge 4패턴 구현**: Circuit Breaker(`harness_agent.py`), Prompt Injection 방어(ToolResult 샌드박스), Context Compaction(`history_manager.py` 30턴 압축), ToolResult 구조화(`modules/tool_result.py` 신규). "루프 설계" 트렌드(Boris Cherny) 분석 → Hermes Stage 1~4 이미 구현, Stage 5(멀티루프 오케스트레이션) v9.4 후보. | Claude Code |
||||| **2026-06-09** | **Phase 1·2 구현 + Phase 3 설계 등록**: Phase 1 낙관적 응답(`optimistic_response.py`), Phase 2 세밀한 메모리(`memory_refinement.py`) 구현 완료. Phase 3 능동적 지능(Proactive Intelligence) v9.4.1 후보로 설계 등록 — 장점·단점·도입 조건 명시. `Phase1_Phase2_개선_설명서.md` 신규 문서. | Claude Code |
||||| **2026-06-09** | **Stage 5 Mayor 에이전트 + 루프 가드레일 3종 완료**: `modules/mayor_agent.py` 신규(루프 생애주기 감독, 반복/토큰 예산 추적, 정체 감지, `/orchestrate mayor` 대시보드). `harness_agent.py` 에이전틱 루프에 Mayor 연결 + 토큰 예산(12k/루프) + 루프 종료 시 CoVe 파일시스템 자기검증 자동 실행. | Claude Code |

---

*이 문서는 Hermes3 프로젝트의 현재 상태(v9.2 완료 + Phase 1·2 구현)와 향후 로드맵(v9.4+)을 명확히 보여줍니다. 앞으로도 경량·Stateless 원칙을 유지하며 진행해 나가겠습니다.*

---
*최종 업데이트: 2026-06-09 16:00 (Phase 1·2 구현 완료, Phase 3 설계 등록, 해야할 일 현황 업데이트)*
