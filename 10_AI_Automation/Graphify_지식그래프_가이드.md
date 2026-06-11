# 🧠 Graphify 지식 그래프 가이드

이 문서는 하네스 시스템에 적용된 **Graphify 지식 그래프 도구**의 작동 원리, 결과물 사용법, 그리고 `audit_engine.py` / `cron_manager.py`와의 통합 계획을 설명합니다.

---

## 1. Graphify란?

폴더 안의 파일들(코드, 문서, 노트 등)을 분석하여 **지식 그래프(Knowledge Graph)**로 만들어주는 도구입니다.

### 하네스 시스템에 적용하면 얻을 수 있는 것
- 하네스 스크립트들 간의 **의존관계 시각화** (`harness_v2.py` → `audit_engine.py` 등)
- 위키 문서들 간의 **개념 연결 지도**
- `graph.html` — 브라우저에서 바로 열 수 있는 **인터랙티브 그래프**
- `GRAPH_REPORT.md` — 핵심 노드 및 숨겨진 연결 감사 보고서

---

## 2. 설치 및 환경

- **패키지**: `graphifyy` (pip 설치)
- **실행 환경**: `/Users/bluesea/Applications/Mjauto/Scripts/venv` (하네스 가상환경)
- **결과물 위치**: `/Users/bluesea/Applications/Mjauto/graphify-out/`

---

## 3. 분석 결과 (2026-05-13 기준)

| 항목 | 값 |
| :--- | :--- |
| **분석 대상** | Mjauto 스크립트 + Mjobsidian 위키 전체 |
| **총 파일** | 64개 (코드 12 + 문서 52) |
| **총 단어** | 약 22,061개 |
| **노드** | 125개 |
| **엣지** | 177개 |
| **커뮤니티** | 26개 |

### 🏆 핵심 허브 노드 (God Nodes)

| 순위 | 노드 | 연결 수 | 의미 |
| :--- | :--- | :--- | :--- |
| 1 | `HistoryManager` | 7 | 대화 기록 관리 — 가장 많이 참조되는 모듈 |
| 2 | `file_manager.resolve` | 7 | 파일 경로 처리 — 핵심 유틸리티 |
| 3 | `CronManager` | 5 | 스케줄 관리 허브 |
| 4 | `MemoryEngine` | 5 | 기억 처리 허브 |
| 5 | `assistant_guide` | 5 | 비서 지침 문서 — 에이전트 행동의 근거 |

---

## 4. 결과물 사용법

### 📂 파일 위치
```
/Users/bluesea/Applications/Mjauto/graphify-out/
├── graph.html        ← 인터랙티브 지식 그래프 (브라우저로 열기)
├── GRAPH_REPORT.md   ← 감사 보고서
└── graph.json        ← 전체 그래프 데이터 (GraphRAG용)
```

### 🖥️ graph.html 여는 법

```bash
# 터미널에서
open ~/Applications/Mjauto/graphify-out/graph.html
```

또는 Antigravity에게 **"그래프 열어줘"** 라고 요청하면 됩니다.

### 🕸️ 그래프 읽는 법

| 요소 | 의미 |
| :--- | :--- |
| **노드(원)** | 각 개념·함수·문서 하나 |
| **색상** | 같은 색 = 같은 커뮤니티 (밀접하게 연결된 그룹) |
| **크기** | 클수록 더 많이 연결된 허브 노드 (= 핵심 파일) |
| **실선 엣지** | 명시적으로 확인된 관계 |
| **점선 엣지** | 추론된 관계 |

**조작 방법:**
- 마우스 드래그 → 노드 이동
- 스크롤 → 줌인/아웃
- 노드 클릭 → 연결된 관계 강조 표시

---

## 5. 실행 방법 (Antigravity에게 요청)

```
# 전체 재분석 (최초 실행 또는 대규모 변경 후)
"전체 그래프 재분석해줘"

# 증분 업데이트 (새 파일 추가 또는 수정 후)
"그래프 업데이트해줘"
```

---

## 6. audit_engine + cron_manager 통합 계획

> **핵심 아이디어**: 별도 스크립트 없이 기존 Dreaming 파이프라인에 흡수하여 문서도 깔끔하고 운영도 단순하게.

### 통합 흐름도

```
Dreaming (매일 03:00)
  │
  ├── memory_engine.py
  │       └→ hot.md 요약 → 업무일지 생성
  │
  ├── audit_engine.py
  │       ├→ 끊긴 링크 감사 (기존)
  │       ├→ 타임스탬프 불일치 감지 (기존)
  │       └→ graphify --update 호출 (신규)
  │               └→ 고립 노드 탐지 → 리포트 병합
  │
  └── Telegram 아침 리포트
          ├→ 감사 결과 (링크, 타임스탬프)
          └→ 지식 그래프 변경 요약 (신규)
```

### 구현 계획

| 단계 | 작업 | 담당 |
| :--- | :--- | :--- |
| 1단계 | `audit_engine.py`에 `run_graphify_update()` 메서드 추가 | Antigravity |
| 2단계 | `cron_manager.py` Dreaming 작업에서 위 메서드 호출 | Antigravity |
| 3단계 | 고립 노드 목록을 Telegram 리포트 메시지에 포함 | Antigravity |

### 장점
- **문서 깔끔**: 별도 graphify 스크립트 파일 불필요
- **자동화 완성**: 매일 아침 그래프 자동 갱신
- **운영 단순**: 기존 Dreaming 흐름에 자연스럽게 통합

---

## 7. 커뮤니티 구조 (26개)

| 커뮤니티 | 대표 노드 | 의미 |
| :--- | :--- | :--- |
| 0 | Antigravity Bot, NVIDIA NIM | AI 에이전트 & Telegram 봇 설정 |
| 1 | audit_engine, cron_manager | 감사 & 크론잡 자동화 |
| 2 | assistant_guide, agent_memory | 에이전트 행동 지침 & 메모리 |
| 3 | file_manager 함수들 | 파일 관리자 모듈 |
| 4 | INDEX.md, handover_manual | 지식 베이스 & 핸드오버 |
| 5 | HistoryManager 메서드들 | 대화 기록 관리자 |
| 6 | MemoryEngine 메서드들 | Memory 엔진 (Dreaming) |
| 7 | CronManager 메서드들 | Cron 스케줄러 모듈 |
| 8 | antigravity_bot_v2.py | Antigravity 봇 코어 |
| 9 | AuditEngine 메서드들 | 감사 엔진 모듈 |
| 10 | WikiManager 메서드들 | Wiki 컨텍스트 로더 |
| 11 | IngestEngine 메서드들 | Ingest 엔진 모듈 |
| 12 | Clippings, ingest_engine | Clippings 인제스트 시스템 |
| 13 | executor 함수들 | Executor 실행 모듈 |
| 14 | [SAVE], [LIST] 태그 | 하네스 에이전트 태그 시스템 |
| 15 | 스크립트 정보, 명령어 | 스크립트 & 명령어 문서 |
| 16 | web_reader 함수들 | 웹 리더 모듈 |
| 17 | AI 편향, 마크다운 연구 | AI 연구 (편향/마크다운) |

---

*최종 업데이트: 2026-05-13 01:32*
*작성자: Antigravity AI*
