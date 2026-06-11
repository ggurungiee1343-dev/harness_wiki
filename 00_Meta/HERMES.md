# 🤖 HERMES.md — modules/ 디렉토리 아키텍처 규칙 (v3.9.1)

이 파일은 `hermes_context_builder.py`에 의해 헤르메스 에이전트가 이 폴더를 탐색하거나 파일을 읽을 때 **자동으로 로드되는 가이드라인**입니다.  
이 파일의 규칙은 헤르메스의 **구조적 장기기억(Architectural Long-term Memory)**으로 기능합니다.

---

## 📌 이 디렉토리의 역할

`modules/`는 `harness_agent.py`가 에이전틱 루프를 실행할 때 호출하는 **전문 기능 모듈들의 모음**입니다.  
모든 모듈은 독립적인 클래스(Class) 단위로 설계되어 있으며, `harness_agent.py`에서 인스턴스화하여 사용합니다.

---

## 📋 현재 등록된 모듈 목록 (2026-05-21 기준)

| 모듈 파일 | 역할 |
|:---|:---|
| `wiki_manager.py` | 위키 컨텍스트 로딩 및 LLM 제공 |
| `history_manager.py` | 대화 이력 (`harness_memory.json`) 관리 |
| `file_manager.py` | 파일 생성/읽기/이동/삭제 |
| `bio_memory_engine.py` | L1/L2/L3 인지 메모리 엔진 (에빙하우스 망각+연상망) |
| `ingest_engine.py` | Clippings → 위키 자동 분류 이관 |
| `system_monitor.py` | 하드웨어 감시 및 자가 치유 |
| `news_engine.py` | 뉴스 수집 |
| `git_manager.py` | Git 저장소 관리 (Add/Commit/Push/Pull) |
| `executor.py` | Bash 실행 + 자율 에러 복구 + Skill 캐싱 |
| `cognitive_engine.py` | 고수준 추론 보조 |
| `web_reader.py` | URL 본문 추출 및 요약 |
| `audit_engine.py` | 작업 감사 로그 |
| `model_scanner.py` | LLM 모델 상태 스캔 |
| `hermes_context_builder.py` | 코드베이스 컨텍스트 하네스 (비대화 방지 알고리즘 탑재) |

---

## 🏛️ 코딩 규칙 (Coding Rules)

### 규칙 1: 반드시 Class 기반으로 작성할 것
```python
# ✅ 올바른 방식
class NewModule:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root

# ❌ 금지: 전역 함수만으로 구성된 모듈
def some_function():
    pass
```

### 규칙 2: `__init__`에는 반드시 `workspace_root` 인자를 받을 것
- 헤르메스의 작업 공간 경로를 모듈에 주입하여, 모듈이 스스로 올바른 경로를 찾을 수 있어야 합니다.

### 규칙 3: 신규 모듈 추가 시 `harness_agent.py` 임포트 구역에 등록할 것
```python
from modules import (
    ...,
    new_module_name   # ← 여기에 추가
)
```

### 규칙 4: 파일명은 `snake_case`로, 확장자는 `.py`로 고정
- 예: `web_agent_module.py`, `hermes_context_builder.py`

### 규칙 5: HERMES.md 비대화 방지 및 슬림화 가이드
- `hermes_context_builder.py`가 `_slim_context()` 필터로 핵심 리스트 및 헤더만 4000자 이내로 파싱하여 LLM에 전달합니다. 규칙은 반드시 `-` 또는 `*` 리스트 기호로 시작하도록 정형화하십시오.

### 규칙 6: 버전 관리는 `git_manager.py`에 위임할 것
- 변경 사항 커밋/동기화 시 하드코딩된 subprocess 대신 반드시 `GitManager`를 호출하십시오.

### 규칙 7: 에이전틱 루프 설계 및 파일 쓰기(SAVE) 가이드
- 에이전틱 루프는 최대 3회로 통제하며, `[SAVE]` 태그 처리 시 절대 경로(Scripts 등)인지 상대 경로(inbox, wiki 등)인지 명확히 판별하십시오.

### 규칙 8: 카파시(Karpathy)의 4대 AI 개발 가이드라인 준수
- **1. Ask, don't assume**: 불명확한 지시는 2~3가지 안을 제시하여 승인 후 진행.
- **2. Simplest solution first**: 요청받지 않은 추상화 금지. 가장 단순한 코드 우선.
- **3. Don't touch unrelated code**: 범위 밖 파일 리팩토링/포맷팅 금지.
- **4. Flag uncertainty**: 확신 없으면 지어내지 말고 불확실함을 명시.

### 규칙 9: 불필요한 미사여구 배제 (Kill the filler)
- "물론입니다!", "좋은 질문입니다!", "확인해 드리겠습니다!" 등 filler 문구 금지. 바로 결과로 진입.

---

## 🧠 기억 시스템 통합 구조 요약

```
Bio-Memory (bio_memory_engine.py)
  L1: 최근 대화 (harness_memory.json 상위 15개)  → 수 시간
  L2: 연상망 (벡터+그래프)                        → 수 주
  L3: 절차기억 (Bash 스킬 캐시)                  → 반영구

Codebase Harness (hermes_context_builder.py)
  구조기억: HERMES.md                            → 영구 (슬림 요약 필터 적용)
  노이즈차단: .hermesignore                       → 영구
  맵핑: Codebase Map (런타임 자동생성)            → 즉시

→ 두 시스템이 합쳐져야 "경험+원칙"을 동시에 기억하는 완전한 AI
```

---

*변경이력 → `wiki/00_Meta/hot.md` 참조*  
*다음 업데이트 트리거: 새 모듈 추가 또는 아키텍처 변경 시*

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
