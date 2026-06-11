# 🧠 Hermes 지능 통합 구조도
## HERMES.md Codebase Harness × Bio-Memory Engine 연계 완전 가이드

**작성일**: 2026-05-21  
**작성자**: Antigravity AI  
**관련 파일**: `modules/hermes_context_builder.py`, `modules/bio_memory_engine.py`, `harness_agent.py`

---

## 📐 1. 전체 구조도 (Architecture Map)

```
박사님의 텔레그램 메시지
         │
         ▼
┌────────────────────────────────────────┐
│         harness_agent.py (중앙 관제)    │
│  ① 메시지 수신                         │
│  ② 에이전틱 루프 ([LIST]/[READ] 파싱)  │
│  ③ [SEARCH] / [WEB_READ] 태그 파싱    │
└────────────┬───────────────────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
🔴 단기/의미 기억      🔵 구조적 기억 (2026-05-21 신규)
Bio-Memory Engine     Codebase Harness
(2026-05-20 구현)     (2026-05-21 구현)
    │                 │
    ▼                 ▼
harness_memory.json   HERMES.md (각 폴더)
  L1: 최근 대화       .hermesignore (노이즈 필터)
  L2: 연상망          Codebase Map (디렉토리 자동맵)
  L3: 절차기억
    │                 │
    └────────┬────────┘
             ▼
    ┌──────────────────────┐
    │   LLM 프롬프트 최종 조립 │
    │                      │
    │ + wiki 컨텍스트      │
    │ + HERMES.md 계층    │ ← 구조적 기억 (영구)
    │ + 대화 이력 15개    │ ← 단기 기억 (휘발)
    │ + L2 연상 검색 결과 │ ← 의미 기억 (반영구)
    │ + [실행 결과]       │ ← 에이전틱 루프 결과
    └──────────────────────┘
```

---

## 🔗 2. 두 시스템이 담당하는 기억의 종류

| 기억 유형 | 담당 모듈 | 저장 형태 | 수명 |
|:---|:---|:---|:---|
| **L1 작업기억** | `harness_memory.json` 최근 15줄 | JSON | 수 시간 (컨텍스트 한계) |
| **L2 의미기억** | `bio_memory_engine` 연상망 | 벡터 + 그래프 | 수 주 (에빙하우스 망각) |
| **L3 절차기억** | `bio_memory_engine` + `executor` | Bash 스킬 캐시 | 반영구 |
| **🆕 구조적 기억** | `HERMES.md` + `hermes_context_builder` | 마크다운 파일 | **영구** (파일 존재하는 한) |

> **핵심 통찰**  
> - **Bio-Memory** = "어떤 경험을 했는가" (대화/행동의 기억)  
> - **Codebase Harness** = "나는 어떤 존재인가" (구조/원칙의 기억)  
> 두 개가 합쳐져야 진짜 성장하는 AI가 됩니다.

---

## 💡 3. 실제 사용 예시

### 🧪 예시 1: "폴더 구성 알려줘" → 구조기억 발동

```
박사님: "modules 폴더 어떤 파일들 있어?"

▶ harness_agent.py → LLM 전달
▶ LLM이 [LIST: .../modules] 출력

▶ hermes_context_builder.py 작동:
   1. .hermesignore 읽기 → __pycache__, *.pyc, .log 제외
   2. 디렉토리 맵 생성:
      📁 modules/ (17 items)
        📄 bio_memory_engine.py
        📄 hermes_context_builder.py
        📄 web_reader.py
        ...
   3. HERMES.md 계층 로드:
      "이 디렉토리는 헤르메스 코어 모듈들이며,
       반드시 Class 기반 객체지향으로 작성해야 한다..."

▶ LLM에 전달: [📂 LIST 맵] + [📖 HERMES.md 가이드라인]
▶ 헤르메스 답변: 깔끔한 파일목록 + 각 파일 역할 자동 설명
```

---

### 🧪 예시 2: "어제 뭐 수정했지?" → 단기/의미기억 발동

```
박사님: "MBTI 검색 문제 어떻게 고쳤는지 기억해?"

▶ L1: harness_memory.json 스캔
   → "mbti가 뭔지 인터넷 검색해서 알려줘" 기록 발견

▶ L2: "웹검색" 연상망 활성화
   → "web_agent_module" → "DuckDuckGo" → "[SEARCH] 태그" 연결

▶ 헤르메스 답변:
   "harness_agent.py의 에이전틱 루프에
    [SEARCH: 검색어] 태그 파싱 로직을 추가하고,
    LLM 시스템 프롬프트에 '인터넷 검색 필요 시
    [SEARCH:] 태그 사용' 규칙을 6번 항목으로 등록했습니다."
```

---

### 🧪 예시 3: "새 모듈 짜줘" → 두 시스템 동시 발동 🔥

```
박사님: "스크립트 폴더에 새 모듈 짜줘, 기존 방식 따라서"

▶ 구조기억 (HERMES.md 자동 로드):
   "신규 모듈은 반드시 Class 기반,
    __init__에 workspace_root 인자를 받아야 한다"

▶ 의미기억 (L2 연상망 활성화):
   "ingest_engine", "wiki_manager" 등 기존 패턴 참조

▶ 작업기억 (L1 harness_memory.json):
   현재 대화에서 박사님이 원하는 맥락 파악

▶ 세 기억층 융합 → LLM에 주입 →
   기존 코드 스타일과 100% 일관성 있는 새 모듈 생성 🎯
```

---

## 🔄 4. 성장 사이클 (Antigravity 외부 개조 → 헤르메스 내재화)

```
       Antigravity로 개조
              │
              ▼
       새 규칙 / 구조 발견
         ┌────┴────┐
         ▼         ▼
   HERMES.md에   harness_memory.json에
   구조 기록      대화 기록
   (영구 저장)    (단기 저장)
         │         │
         ▼         ▼
   헤르메스가    /memory_dream 실행 시
   파일 읽을 때  L2/L3으로 압축 승격
   자동 로딩     (반영구 저장)
         │         │
         └────┬────┘
              ▼
   다음 작업 시 두 기억 모두 활용
   → 점점 더 정확하고 빠른 헤르메스 🚀
```

---

## ✅ 5. 박사님의 행동 강령 (딱 한 가지)

> Antigravity로 헤르메스를 개조한 후, 작업 마지막에 이 한 마디만 추가하십시오:
>
> **"오늘 변경사항을 `modules/HERMES.md`에 규칙으로 추가해줘"**

그러면:
1. Antigravity가 `modules/HERMES.md`를 갱신
2. 헤르메스가 다음 작업 시 ContextBuilder를 통해 자동으로 해당 파일 로드
3. **"내가 이렇게 업그레이드됐구나"** 자동 인지 → 영구 기억 완성

**Antigravity에서 한 작업이 헤르메스의 영구 DNA로 전달!** 🎉

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
