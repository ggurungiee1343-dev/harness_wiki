# 🧪 `/reduce` 명령어 사용 가이드 (v9.1.4)

**최종 업데이트**: 2026-06-01 08:00

---

## 📋 목차

1. [개요: 왜 만들었는가](#-개요-왜-만들었는가)
2. [정의: `/reduce`란?](#-정의-reduce란)
3. [사용법](#-사용법)
4. [전체 파이프라인 구조](#-전체-파이프라인-구조)
5. [DecisionAgent — 액션 자동 분류](#-decisionagent--액션-자동-분류)
6. [액션별 상세 동작](#-액션별-상세-동작)
   - [🌐 web — 웹 검색](#-web--웹-검색)
   - [📖 wiki — 위키 검색](#-wiki--위키-검색)
   - [💬 ask — 일반 QA](#-ask--일반-qa)
   - [🏷️ tag — 태깅](#️-tag--태깅)
   - [⚡ exec — 명령어 실행](#-exec--명령어-실행)
7. [에러 처리 체계](#-에러-처리-체계)
8. [구현 파일 및 구조](#-구현-파일-및-구조)
9. [버전 히스토리](#-버전-히스토리)

---

## 1. 📌 개요: 왜 만들었는가

### 문제 상황

Hermes 시스템이 발전하면서 Telegram에서 다양한 작업을 처리해야 했다:

- **웹 검색**: "오늘 날씨 어때?", "최신 AI 뉴스"
- **위키 검색**: "HMM이 뭐야?", "시스템 아키텍처 설명해줘"
- **일반 질문**: "파이썬의 철학은?", "삶이란 무엇인가"
- **태깅**: "이거 태그 추가해줘"
- **명령어 실행**: 디렉토리 확인, 파일 검색 등

처음에는 **각 작업마다 별도의 Telegram 명령어**(`/web`, `/wiki`, `/ask`, `/exec`...)가 존재했다. 이 방식은 다음과 같은 문제가 있었다:

1. **사용자 부담**: 어떤 명령어를 써야 하는지 기억해야 함
2. **확장성 부족**: 새로운 액션 추가 시마다 명령어 증가
3. **자동화 한계**: "오늘 날씨 어때?"는 `/weather`인가 `/web`인가?

### 해결 방안

**모든 질문을 하나의 명령어로 → `/reduce <질문>`**

명령어를 통합하고, **내부에서 DecisionAgent가 질문 의도를 자동 분류**하도록 설계했다. 사용자는 "/reduce" 하나만 외우면 된다.

### 철학

> *"사용자가 '무엇을 원하는지'만 말하면, 시스템이 '어떻게 처리할지'를 결정한다."*

전통적인 명령어 인터페이스(Command Interface)에서 **의도 기반 인터페이스(Intent-Based Interface)** 로의 전환. 이것이 HermesCoreReducer의 핵심 설계 철학이다.

---

## 2. 🔍 정의: `/reduce`란?

**`/reduce`**는 Hermes3 시스템의 **통합 쿼리 처리 명령어**다.

- **입력**: 단일 텍스트 쿼리 (자연어 질문, 명령어, 검색어 등)
- **내부 처리**: 3단계 Agent Pipeline (Decision → Execution → Knowledge)
- **출력**: 액션별 맞춤형 응답 (웹 검색 결과, 위키 문서 요약, LLM 답변 등)

### 공식 정의

> `/reduce`는 HermesCoreReducer 파이프라인을 구동하는 진입점이다.
> DecisionAgent가 쿼리 의도를 분석해 액션(web/wiki/ask/tag/exec)을 결정하고,
> ExecutionAgent가 해당 액션을 실행하며, KnowledgeAgent가 결과를 정제한다.

---

## 3. 📖 사용법

### 기본 문법

```
/reduce <질문|명령어|검색어>
```

### 실제 예시

| 입력 예시 | 전체 타이핑 |
|-----------|------------|
| 오늘 날씨 | `/reduce 오늘 날씨 어때?` |
| 뉴스 요약 | `/reduce 최신 AI 뉴스 요약해줘` |
| 개념 질문 | `/reduce HMM 모델이 뭐야?` |
| 태그 추가 | `/reduce 태그 추가 중요 urgent` |
| 명령 실행 | `/reduce ls -la ~/Applications` |
| 일반 질문 | `/reduce 파이썬의 철학은?` |

### 팁

- **질문은 자연어로 자유롭게**: 어떤 형식이든 DecisionAgent가 분류
- **검색 의도가 확실하면**: `검색 ...` 접두사 추천 (`/reduce 검색 하이브리드 라우팅`)
- **날씨/뉴스/주가**: 별도 설정 없이 자동 웹검색
- **명령어 실행**: 일반 질문과 구분되어 `exec` 액션으로만 특수 실행

---

## 4. ⚙️ 전체 파이프라인 구조

```
Telegram: /reduce 오늘 날씨 어때?
   │
   ▼
① cmd_reduce (handlers/_memory.py)
   ├─ check_user() → 권한 확인
   ├─ AgentContext 생성 (message_id, user_id, query)
   └─ reduce() 호출 [HermesCoreReducer]
        │
        ▼
② DecisionAgent.decide() — **무엇을 할지 결정**
   ├─ 키워드 매칭 (룰 기반 우선)
   │   web 키워드: "날씨", "뉴스", "주가", "검색 ", "http"
   │   tag 키워드: "태그", "tag"
   │   ask 키워드: 나머지 (기본값)
   ├─ (선택) LLM 보조 판단
   └─ action 결정 → {action, query, metadata}
        │
        ▼
③ ExecutionAgent.execute(action, query) — **실행**
   ├─ web  → duckduckgo_search 웹 검색 → 결과 포맷
   ├─ wiki → HybridKnowledgeIndexer (FTS5+TF-IDF+RRF) → LLM 정제
   ├─ tag  → handlers._approval.cmd_tag_logic
   ├─ ask  → handlers._memory.cmd_ask_logic (CoVe 팩트체크) 
   └─ exec → modules.executor.execute_bash_command
        │
        ▼
④ KnowledgeAgent.refine() — **정제 및 기록**
   ├─ ask/wiki 액션 + LLM 있음 → _refine_result()로 LLM 재가공
   ├─ hot_context 업데이트
   └─ pems_score 조정 (PEMS 에이전트 평가)
        │
        ▼
⑤ 응답 텍스트 → Telegram reply_text()
```

---

## 5. 🧠 DecisionAgent — 액션 자동 분류

### 분류 방식: 하이브리드 (룰 우선 + LLM 보조)

**1차: 키워드 매칭** (0-1ms, 지연 없음)
- 쿼리 내 특정 키워드 포함 여부를 확인
- 매칭되면 즉시 해당 액션 반환 (LLM 호출 없음)
- 우선순위: web → tag → exec → ask (기본값)

**2차: LLM 보조 판단** (키워드 매칭 실패 시)
- 키워드가 없으면 LLM의 이해에 의존
- LLM 호출 실패 시 기본값 `ask` 반환

### 액션 분류 표

| 액션 | 결정 방식 | 실행 결과 | 사용 예 |
|------|----------|---------|--------|
| `web` | 키워드 매칭 1순위 | 웹 검색 결과 요약 | 날씨/뉴스/주가/검색 |
| `wiki` | LLM 판단 (키워드 미매칭 시) | 위키 검색 → LLM 정제 | 개념 문의/문서 검색 |
| `ask` | 기본값 (모든 액션 미매칭) | LLM 직접 답변 | 일반 QA/잡담/철학 |
| `tag` | "태그"/"tag" 키워드 | 태깅 엔진 실행 | 태그 추가/관리 |
| `exec` | 특수 패턴 (옵션) | 시스템 명령어 실행 | 파일 조작/디렉토리 확인 |

### 키워드 목록 (core_reducer.py:110-113)

```python
# web 키워드 (확장 가능)
"날씨", "뉴스", "주가", "검색 ", "http"

# tag 키워드
"태그", "tag"
```

> **참고**: 키워드는 소스 코드 `core_reducer.py`의 `WEB_KEYWORDS` / `TAG_KEYWORDS` 상수에서 관리한다. 새 키워드 추가 시 DecisionAgent의 분류 정확도가 즉시 향상된다.

---

## 6. 🔧 액션별 상세 동작

### 🌐 web — 웹 검색

**v9.1.4 기준**: `duckduckgo_search`(DDGS) 라이브러리 직접 호출

```python
# 의사 코드
from duckduckgo_search import DDGS
with DDGS() as ddgs:
    results = list(ddgs.text(query, max_results=5))
```

**출력 예시**:
```
🌐 웹 검색: 오늘 날씨
1. 기상청 날씨누리
   기상청 날씨누리에서 최신 기상 정보를 확인하고...
   [https://www.weather.go.kr](https://www.weather.go.kr)
2. 네이버 날씨
   ...
```

**동작 흐름**:
1. 키워드 매칭 → web 액션
2. DDGS.text()로 실시간 검색
3. 결과 5개 추출 (제목 + 본문 200자 + 링크)
4. 깔끔한 마크다운 포맷팅
5. 검색 실패 시 위키 fallback

**fallback 체인**:
```
DDGS 실패 → _execute_wiki() fallback → "📖 위키 검색: ..."
```

---

### 📖 wiki — 위키 검색

**엔진**: HybridKnowledgeIndexer (SQLite FTS5 + TF-IDF 벡터 + RRF 병합)

**버전 히스토리**:
- v9.0: 기본 FTS5 검색 (원시 결과 반환)
- v9.1: TF-IDF + RRF 병합 (순위 정확도 향상)
- v9.1.3: **LLM 정제** 추가 (원시 검색 결과 → 자연어 답변)

**동작 흐름**:
1. FTS5 검색 실행 (전문(full-text) 검색)
2. TF-IDF 유사도 점수 계산
3. RRF(Reciprocal Rank Fusion)로 결과 병합
4. LLM으로 검색 결과 재가공 (v9.1.3+)
5. 정제된 답변 반환

**LLM 정제 과정** (`_refine_result`):
```
원시 검색 결과 (단순 문서 리스트)
    │
    ▼
LLM 프롬프트: "다음 검색 결과를 바탕으로 질문에 자연스럽게 답변해줘"
    │
    ▼
정제된 답변 (자연어, 읽기 쉬움)
```

---

### 💬 ask — 일반 QA

**실행 엔진**: `handlers._memory.cmd_ask_logic`

**동작**:
1. `cmd_ask_logic(question)` 호출
2. CoVe(구문 검증기) 우선: `verifier.process_query()` 
3. CoVe 빈 결과 시: `_call_llm()` 직접 호출
4. LLM 응답 반환

**에러 fallback**:
```python
try:
    from handlers._memory import cmd_ask_logic
    result = await cmd_ask_logic(query)
    return result if result else f"✅ {query}에 대한 응답을 준비 중입니다."
except Exception:  # ImportError 포함 모든 예외 처리
    return f"✅ 질문: {query}\n(LLM 응답 준비 중입니다)"
```

---

### 🏷️ tag — 태깅

**실행 엔진**: `handlers._approval.cmd_tag_logic`

- `/reduce 태그 추가 중요` → 태그 엔진에 `중요` 태그 추가 요청
- 키워드 "태그" 또는 "tag"로 시작하는 쿼리만 매칭
- 태깅 엔진 응답을 그대로 반환

---

### ⚡ exec — 명령어 실행

**실행 엔진**: `modules.executor.execute_bash_command`

- 특수 패턴 매칭 (보안 제한 있음)
- 신뢰된 사용자만 실행 가능
- Trajectory Regulation 적용 (명령어 이력 관리)

---

## 7. 🛡️ 에러 처리 체계

### 에러 유형별 대응

| 상황 | 대응 | 결과 메시지 |
|------|------|------------|
| 권한 없음 | `check_user()` 실패 | silent return (무응답) |
| 웹 검색 실패 | 자동 wiki fallback | 📖 위키 검색 결과 |
| wiki 검색 실패 | 빈 결과 방어 | ❌ 결과 없음 |
| LLM 호출 실패 | raw 결과 fallback | 원시 검색 결과 반환 |
| ask 모듈 예외 | except Exception | ✅ 질문에 대한 응답 준비 중... |
| 완전 빈 결과 | `if not result:` | 🤷 /reduce 결과가 비어 있습니다 |
| f-string 문법 오류 | pre-import 구문 검사 | crash 방지 |

### 캐시 시스템 (Context Hash Cache)

- 동일 쿼리 5분 내 재요청 → LLM 호출 없이 캐시 반환
- 캐시 키: `(message_id, user_id, query)` 해시
- Stateless 설계에도 자주 묻는 질문은 빠르게 응답 가능

---

## 8. 📁 구현 파일 및 구조

### 파일 목록

| 파일 | 역할 | 주요 함수/클래스 |
|------|------|----------------|
| `handlers/_memory.py` | Telegram handler 진입점 | `cmd_reduce()`, `cmd_ask_logic()` |
| `modules/core_reducer.py` | Reducer 파이프라인 코어 | `HermesCoreReducer`, `DecisionAgent`, `ExecutionAgent`, `KnowledgeAgent` |
| `modules/executor.py` | Bash 명령어 실행 | `execute_bash_command()` |
| `handlers/_approval.py` | 태깅 엔진 | `cmd_tag_logic()` |
| `modules/hybrid_router.py` | LLM 라우팅 | `send_completion()` — DeepSeek/로컬 라우팅 |

### 클래스 관계

```
HermesCoreReducer
 ├── DecisionAgent.decide(query) → action
 ├── ExecutionAgent.execute(decision) → result
 └── KnowledgeAgent.refine(action, result) → refined
```

### Pipeline 호출 순서 (core_reducer.py)

```
reduce()
  ├─ AgentContext 생성 (frozen dataclass)
  ├─ 캐시 확인 (5분 TTL)
  ├─ decision_agent.decide(query) → action + metadata
  ├─ execution_agent.execute(decision) → result dict
  ├─ knowledge_agent.refine(action, result_text) → 정제
  ├─ 캐시 저장
  └─ 최종 응답 텍스트 반환
```

---

## 9. 📜 버전 히스토리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v9.0 | 2026-05-26 | 최초 도입: 3-Agent Pipeline, FTS5 wiki, subprocess web 검색 |
| v9.1 | 2026-05-28 | HybridKnowledgeIndexer TF-IDF+RRF 추가, LLM 정제(v9.1.3) |
| v9.1.3 | 2026-05-31 | wiki 액션 LLM 정제, 키워드 확장(날씨/뉴스/주가/검색) |
| **v9.1.4** | **2026-06-01** | **웹 검색 DDGS 전환, `_execute_ask` 예외처리 강화, 데드코드 제거** |

### v9.1.4 변경 상세 (2026-06-01)

1. **`_execute_web`**: `hermes_web_search_plus` CLI (미설치) → `duckduckgo_search`(DDGS) 직접 호출
   - API 키 불필요 (무료, rate limit 있음)
   - subprocess 오버헤드 제거
   - 5개 결과 + 제목/본문/링크 포맷팅
   - DuckDuckGo 결과 → 마크다운 변환

2. **`_execute_ask`**: `except ImportError` → `except Exception`
   - `cmd_ask_logic` 내부 예외(`AttributeError`, `TypeError` 등)도 안전 처리
   - 모든 예외 상황에서 fallback 메시지 반환 보장

3. **데드코드 제거**: `_WEB_SEARCH_ENV`(SERPER/BRAVE/TAVILY/EXA API 키 변수), `WEB_CACHE_TTL` 제거

---

> **참고**: `/reduce`는 시스템 메인 명령어다. 문제 발생 시 `modules/core_reducer.py`와 `handlers/_memory.py`를 먼저 확인.

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
