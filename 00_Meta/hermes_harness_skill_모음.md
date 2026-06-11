# Hermes Harness Skill 모음

> 커스텀 스킬 목록 및 호출 방법 관리 문서  
> 최종 업데이트: 2026-06-10

---

## 이 파일의 정보 출처 (2곳)

이 파일은 세 곳에서 오는 정보가 합쳐집니다.

| 출처 | 경로 | 스킬 형태 |
|---|---|---|
| **Hermes 지식 스킬** | `~/.hermes/skills/<이름>/SKILL.md` | 자연어 프롬프트 기반. 텔레그램 봇에서 실행 |
| **Claude Code 스킬** | `~/.claude/skills/<이름>/SKILL.md` | Claude Code 세션에서 자동 로딩 |
| **모듈 스킬** | `02_스크립트 정보.md`에 등록된 Python 모듈 | 코드 실행 기반. `modules/` 폴더의 .py 파일 |
| **Claude Code 에이전트** | `~/.claude/agents/<이름>.md` | 서브에이전트 형태. Task 도구로 병렬 실행 |
| **MCP 서버** | `settings.json mcpServers` | Claude Code에서 도구로 직접 호출 가능 |

> 새 스킬이 생기면 **둘 중 어디에 속하는지** 확인 후 이 파일에 추가.  
> Python 모듈로 만든 것도 자연어로 부를 수 있으면 여기에 트리거 등록.

---

## 스킬 목록

### 1. meta-update — 메타 파일 자동 업데이트

**형태**: 지식 스킬  
**파일**: `~/.hermes/skills/meta-update/SKILL.md`  
**생성일**: 2026-06-09

**이렇게 부르면 됩니다**
- "메타 업데이트해줘"
- "작업 내용 저장해줘"
- "오늘 작업 저장해줘"
- "방금 한 거 메타에 반영해줘"
- "문서 업데이트해줘"

**실행 시 일어나는 일**
1. 현재 세션 대화 히스토리 분석 → 어떤 작업이 있었는지 파악
2. 메타 7종 중 관련된 파일만 선별 (없으면 건너뜀)
3. `00_Meta/` 하위 파일 중 직접 관련된 것도 함께 업데이트
4. 어떤 파일을 왜 업데이트했는지 완료 보고

**업데이트 대상 판단 기준**

| 파일 | 조건 |
|---|---|
| `05_시스템 상태.md` | 코드 변경, 새 모듈, 버그 수정 |
| `02_스크립트 정보.md` | 신규 모듈/함수, 카운트 변화 |
| `06_에이전트_오류_및_재발방지_보고서.md` | 버그 수정, 예외 처리 |
| `01_hot.md` | 작업 상태 변경, 완료 항목 |
| `03_시스템 인벤토리.md` | 패키지 설치, 환경 변경 |
| `00_Meta_지도.md` | 신규 문서 생성 |
| `claude_briefing.md` | 시스템 구조 대규모 변경 |

### 2. mj-meta-update — Claude Code 메타 업데이트 스킬

**형태**: Claude Code 스킬  
**파일**: `~/.claude/skills/mj-meta-update/SKILL.md`  
**생성일**: 2026-06-10

**이렇게 부르면 됩니다** (Claude Code 세션에서)
- "메타 업데이트해줘" (Hermes skill과 동일 트리거, Claude Code에서도 작동)
- "작업 내용 저장해줘"
- "문서 업데이트해줘"

**실행 시 일어나는 일**
1. 이 세션의 변경 파일 분석
2. 변경 유형에 따라 메타 7종 선택적 업데이트
3. `git -C wiki add -A && git commit` 자동 실행

**Hermes skill과의 차이**
- Hermes skill (`meta-update`): 텔레그램에서 호출 → Hermes 봇이 처리
- Claude Code skill (`mj-meta-update`): Claude Code 세션에서 호출 → Claude가 직접 파일 편집

---

### 3. mj-stock-analyze — V_FINAL 주식 분석 체크리스트

**형태**: Claude Code 스킬  
**파일**: `~/.claude/skills/mj-stock-analyze/SKILL.md`  
**생성일**: 2026-06-10

**이렇게 부르면 됩니다** (Claude Code 세션에서)
- "NVDA 분석해줘"
- "V_FINAL 기준으로 RDW 봐줘"
- "주식 분석해줘"

**실행 시 일어나는 일**
1. V_FINAL v1.4 전략 가이드 로드
2. 5레이어 체크리스트 적용 (SEPA/기관품질/펀더멘털/ALPHA_SCORE/매도조건)
3. 판정 결과 출력: FINAL_BUY / WATCH / STRONG_STRUCT / SKIP

**MCP stock-scanner와의 차이**
- MCP tool: 실시간 데이터 가져와서 자동 계산 (Claude Code에서 `analyze_stock` 도구 호출)
- Claude Code skill: 전략 가이드 문서를 분석 기준으로 로드 (수동 분석 보조)

---

### 4. /ship — 병렬 서브에이전트 코드 작성/리뷰/테스트

**형태**: Claude Code 슬래시 커맨드 + 에이전트 팀  
**파일**: `~/.claude/commands/ship.md` + `~/.claude/agents/{writer,reviewer,tester}.md`  
**생성일**: 2026-06-10

**이렇게 부르면 됩니다** (Claude Code 세션에서만)
- `/ship <작업 설명>`
- 예) `/ship harness_agent.py에 rate limiting 추가, 분당 10회 초과 시 차단`

**실행 시 일어나는 일**
1. Opus(오케스트레이터)가 브리핑 작성 (목표/범위/완료 조건/제외 범위)
2. Writer(Sonnet) + Tester(Sonnet) **병렬** 실행
3. Writer 완료 후 Reviewer(Sonnet) 실행
4. 최종 리포트 1개로 수렴 (Writer 구현 내용 + Tester 결과 + Reviewer 지적사항)
5. 커밋은 MJ님 승인 후에만

**사용 조건**
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 환경변수 필요 (`~/.zshrc`에 등록됨)
- 파일 2개 이상 수정 + 테스트 필요한 중간 규모 작업에 적합
- 단순 수정/1파일 변경은 일반 Claude Code가 빠름

---

## Claude Code 에이전트 (Sub-agents)

`~/.claude/agents/` 에 저장. `Task` 도구로 병렬 호출 가능.  
→ 상세 사용법: `wiki/00_Meta/자동화_시스템_사용법.md`

| 에이전트 | 파일 | 역할 | 호출 방법 |
|---|---|---|---|
| `meta-updater` | `~/.claude/agents/meta-updater.md` | 메타 7종 자동 분석·업데이트 | "메타 업데이트 에이전트 실행해줘" |
| `hermes-debugger` | `~/.claude/agents/hermes-debugger.md` | 봇 에러 로그 분석 → 원인·수정안 | "hermes 디버그해줘" |
| `writer` | `~/.claude/agents/writer.md` | 코드 구현 전담 | `/ship` 커맨드 내부에서 자동 호출 |
| `reviewer` | `~/.claude/agents/reviewer.md` | 코드 리뷰 전담 | `/ship` 커맨드 내부에서 자동 호출 |
| `tester` | `~/.claude/agents/tester.md` | 테스트 작성 전담 | `/ship` 커맨드 내부에서 자동 호출 |

---

## MCP 서버 (Layer 5 — Plugins)

`~/.claude/settings.json mcpServers` 에 등록. Claude Code에서 도구로 직접 호출.

| MCP 서버 | 파일 | 제공 도구 | 트리거 예시 |
|---|---|---|---|
| `hermes` | `/Users/bluesea/.local/bin/hermes mcp serve` | Hermes 봇 연동 | (자동) |
| `stock-scanner` ✅ NEW | `Scripts/stock_mcp_server.py` | `analyze_stock`, `run_scan`, `market_status`, `record_result`, `backtest_summary`, `watchlist` | "NVDA 실시간 분석해줘", "오늘 매수 후보 스캔해줘" |

**stock-scanner MCP 사용법** (Claude Code 세션에서):
```
"NVDA V_FINAL 분석해줘"        → mcp__stock-scanner__analyze_stock 자동 호출
"오늘 매수 후보 찾아줘"         → mcp__stock-scanner__run_scan 자동 호출
"현재 시장 상태 확인해줘"       → mcp__stock-scanner__market_status 자동 호출
"관심종목 목록 보여줘"          → mcp__stock-scanner__watchlist 자동 호출
```

---

## Claude Code 훅 (Hooks — Layer 3)

`~/.claude/settings.json hooks` 에 등록. 특정 이벤트에 자동 실행.  
→ 상세 사용법: `wiki/00_Meta/자동화_시스템_사용법.md`

| 훅 | 이벤트 | 실행 파일 | 동작 |
|---|---|---|---|
| SessionStart | 세션 시작 시 | `session_start_hook.sh` | `01_hot.md` + 최근 변경 → 컨텍스트 주입 |
| Stop | 세션 종료 시 | `hooks/stop_hook.py` | 미커밋 수 확인 + 메타 업데이트 체크리스트 표시 |
| PostToolUse (Write\|Edit) | 파일 수정 시 | `hooks/wiki_autostage.py` | wiki 경로 파일 → git 자동 스테이징 |

---

## 모듈 스킬 — 자연어 트리거 가능한 Python 모듈

`02_스크립트 정보.md`에 등록된 모듈 중 사용자가 자연어로 호출할 수 있는 것들.  
트리거 등록되면 `CLAUDE.md`에도 추가할 것.

| 모듈 | 기능 요약 | 자연어 트리거 예시 | 트리거 등록 |
|---|---|---|:---:|
| `ingest_engine.py` | 클리핑/PDF → Wiki 자동 이관 | "ingest해줘", "정원 가꿔줘", "노트 정리해줘" | ❌ 미등록 |
| `harness_verifier.py` | 시스템 구조 건강 진단 100점 | "하네스 점수 확인해줘", "시스템 진단해줘" | ❌ 미등록 |
| `curator.py` | 스킬/파일 감사 (미사용/대용량/bak 탐지) | "코드 감사해줘", "큐레이터 실행해줘" | ❌ 미등록 |
| `system_monitor.py` | 서비스 헬스체크 | "상태 확인해줘", "서비스 점검해줘" | ❌ 미등록 |
| `vault_deduplicator.py` | Obsidian 중복 문서 제거 | "vault 중복 제거해줘" | ❌ 미등록 |
| `knowledge_mesh_orchestrator.py` | 논문+노트 교차 분석 | "논문 분석해줘", "리서치 연결해줘" | ❌ 미등록 |
| `natural_language_cron.py` | 자연어로 크론잡 등록 | "매일 오전 9시에 ~해줘" | ❌ 미등록 |
| `web_agent_module.py` / `web_reader.py` | 웹 검색/읽기 | "이 URL 읽어줘", "웹 검색해줘" | ❌ 미등록 |
| `send_telegram_msg.py` | 텔레그램 알림 발송 | "나한테 알림 보내줘" | ❌ 미등록 |
| `dream_scheduler.py` | 메모리 드리밍(L3 성장) | "드리밍 실행해줘", "메모리 정제해줘" | ❌ 미등록 |
| `weakness_miner.py` | 반복 실패 패턴 감지 + 에러보고서 자동 기록 | "weakness 현황 보여줘", "에러 패턴 분석해줘" | ✅ 자동 (3회↑ 시 텔레그램 알림) |
| `command_router.py` | 명령어 라우팅 (내부 인프라) | — 내부 전용, 트리거 불필요 | —  |
| `response_handler.py` | LLM 응답 파이프라인 (내부 인프라) | — 내부 전용, 트리거 불필요 | — |
| `context_assembler.py` | 컨텍스트 조립 (내부 인프라) | — 내부 전용, 트리거 불필요 | — |
| `agentic_loop.py` | 에이전틱 루프 (내부 인프라) | — 내부 전용, 트리거 불필요 | — |

> **트리거 등록 우선순위**: ingest → harness_verifier → curator → system_monitor 순으로 정리 추천

---

## 스킬 추가 방법

새 스킬이 생기면 아래 형식으로 추가.

```
### N. 스킬이름 — 한 줄 설명

**형태**: 지식 스킬 / 모듈 스킬
**파일**: `~/.hermes/skills/<폴더>/SKILL.md` 또는 `Scripts/modules/<파일>.py`
**생성일**: YYYY-MM-DD

**이렇게 부르면 됩니다**
- (트리거 예시들)

**실행 시 일어나는 일**
(동작 설명)
```

---

## 트리거 작동 범위

| 환경 | 작동 여부 | 방식 |
|---|---|---|
| **Hermes 텔레그램 봇** | ✅ 자동 | skills/ 폴더 자동 로딩 |
| **Claude Code** | ✅ 작동 | CLAUDE.md에 트리거 등록돼 있어서 세션 시작 시 인식 |
| **다른 AI (ChatGPT 등)** | ❌ 불가 | skills/ 폴더 접근 권한 없음 |
