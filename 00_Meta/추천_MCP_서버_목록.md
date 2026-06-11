# 🔌 추천 MCP(Model Context Protocol) 서버 목록

박사님의 하네스/헤르메스 비서 시스템을 API 위주 개발에서 표준화된 AI 툴 연동 방식으로 고도화하고, 미래 가족 공유(이관)를 용이하게 만들기 위해 추천하는 핵심 MCP 서버 목록입니다.

---

## 🛠️ 1. 필수 연동 추천 MCP 서버 5선

| MCP 서버 이름 | 패키지 경로 / 링크 | 주요 역할 | 활용 시너지 및 로직 대체 방안 |
| :--- | :--- | :--- | :--- |
| **Brave Search** | [`@modelcontextprotocol/server-brave-search`](https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search) | Brave Search API를 이용한 실시간 웹 검색 및 웹페이지 스크랩 | **실시간 정보 탐색**: 과거 학습 데이터에만 의존하는 LLM의 한계를 해결하기 위해, 질문을 받았을 때 자동으로 최신 뉴스와 실시간 세무/법률 정보를 구글링하여 정확한 답변을 유도합니다. |
| **Filesystem** | [`@modelcontextprotocol/server-filesystem`](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | AI가 지정한 로컬 디렉토리 내에서 안전하게 파일을 읽고 쓰는 표준 입출력 제공 | **파일 관리 안전 격리**: `/Users/bluesea/Applications/Mjobsidian` 폴더만 접근 가능하도록 설정하여, 비서 에이전트가 다른 시스템 경로를 건드리지 못하게 원천 차단하고 안전하게 노트를 관리합니다. |
| **Fetch** | [`@modelcontextprotocol/server-fetch`](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | 입력된 URL 웹페이지의 HTML을 읽어 깔끔한 마크다운 텍스트로 변환 및 요약 | **웹 리더 대체**: 기존의 웹 텍스트 추출 커스텀 모듈(`web_reader.py`)을 완벽히 대체하며, 복잡한 웹 페이지 레이아웃도 깔끔한 본문 텍스트로 전환하여 요약할 수 있게 돕습니다. |
| **SQLite** | [`@modelcontextprotocol/server-sqlite`](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite) | 로컬 SQLite 데이터베이스 파일 생성, 스키마 정의 및 SQL 질의(Query) 실행 | **구조화된 메모리/칸반 제어**: 단순히 마크다운 파일만 읽는 방식에서 벗어나, 업무 상태(할 일, 진행 중, 완료) 및 단기 메모리 로그를 관계형 데이터베이스로 정교하게 관리 및 정렬합니다. |
| **GitHub** | [`@modelcontextprotocol/server-github`](https://github.com/modelcontextprotocol/servers/tree/main/src/github) | 깃허브 저장소(Repo) 생성, 커밋, 이슈(Issue), PR 생성 및 승인 | **협업 및 버전 관리**: 가족용 배포 패키지의 코드 형상 관리나, 에이전트가 개발 도중 발견한 버그 트래킹(칸반 대용)을 깃허브 이슈와 연결하여 실시간으로 보고하게 만듭니다. |

---

## ⚙️ 2. MCP의 구조 및 비서 엔진 연동 로드맵

```text
  ┌────────────────────────────────────────────────────────┐
  │                   옵시디언 / 텔레그램 봇                 │
  └──────────────────────────┬─────────────────────────────┘
                             │ (인터페이스 요청)
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │                 Harness 에이전트 (Client)              │
  └──────────────────────────┬─────────────────────────────┘
                             │ (JSON-RPC 표준 프로토콜)
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │                    MCP 호스트 / 라우터                  │
  └──────┬───────────────────┼─────────────────────┬───────┘
         │                   │                     │
         ▼                   ▼                     ▼
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │  Filesystem  │   │ Brave Search │   │    SQLite    │  ... (MCP Servers)
  │  (로컬 노트) │   │ (실시간 웹)  │   │  (구조 메모리)│
  └──────────────┘   └──────────────┘   └──────────────┘
```

### 1단계: 로컬 MCP 호스트 세팅
*   맥 스튜디오에 Node.js 또는 Python 기반의 MCP 서버들을 설치하고 백그라운드로 실행합니다.
*   예: `npx -y @modelcontextprotocol/server-filesystem /Users/bluesea/Applications/Mjobsidian`

### 2단계: 헤르메스 봇의 MCP 클라이언트화
*   `hermes_local.py` 또는 `harness_agent.py`가 API 호출을 생성할 때, 직접 API 코드를 타는 것이 아니라 로컬 MCP 라우터에 요청을 쏘도록 통일합니다.
*   이 방식이 탑재되면, 가족들에게 비서를 공유해 줄 때 복잡한 파이썬 모듈 수정 없이 **"Brave Search API 키" 하나와 "MCP 파일 시스템 서버" 하나만 켜두면 동일하게 작동**하게 됩니다.

---
*최종 업데이트: 2026-05-20 08:41:00*
*작성자: Antigravity AI (박사님을 위한 추천 MCP 서버 목록 및 고도화 아키텍처 가이드라인 신설 완료)*
