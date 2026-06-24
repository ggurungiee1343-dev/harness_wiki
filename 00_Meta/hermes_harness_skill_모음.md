---
tags: []
---
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

### 4. writing-pro — 글쓰기 스킬

**형태**: 지식 스킬  
**파일**: `~/.hermes/skills/writing-pro/SKILL.md`  
**생성일**: 2026-06-11

**이렇게 부르면 됩니다**
- "글 써줘", "에세이 써줘", "칼럼 초안 잡아줘"
- "이 글 다듬어줘", "퇴고해줘"
- "글 비평해줘"

**실행 시 일어나는 일**
1. 독자·요지·형식 3가지 확정 후 초안 작성
2. AI 글쓰기 패턴 제거 체크리스트 적용 (회피성 마무리, 3개 나열, 양시론 결론 등)
3. 독자 보상 4채널(몰입/신뢰/새로움/감정) 비평 루프 후 최종본 1개만 산출

### 5. book-writing — 책 집필 + 원고 정합성 검토

**형태**: 지식 스킬  
**파일**: `~/.hermes/skills/book-writing/SKILL.md`  
**생성일**: 2026-06-11

**이렇게 부르면 됩니다**
- "책 집필 시작하자", "3장 써줘", "목차 잡아줘"
- "원고 정합성 검토해줘", "원고 전체 점검해줘"

**실행 시 일어나는 일**
1. `wiki/Books/<책제목>/` 표준 구조 생성 (기획/목차/바이블/chapters/작업로그)
2. 장 집필 시: 바이블 선독 → 집필 → 바이블·목차·로그 갱신 (세션 간 연속성 확보)
3. 정합성 검토 시: 용어 혼용·사실 충돌·중복·논조 일탈·구조 불일치 5종 검사 후 보고서 작성

### 6. legal-paper — 법학논문 (박사학위논문 + 학회 소논문)

**형태**: 지식 스킬  
**파일**: `~/.hermes/skills/legal-paper/SKILL.md`  
**생성일**: 2026-06-11

**이렇게 부르면 됩니다**
- "법학논문 시작하자", "학위논문 작업 이어서 하자"
- "소논문 써줘", "학회 투고 논문 잡아줘"
- "인용 검증해줘", "각주 점검해줘"

**실행 시 일어나는 일**

**[모드 A: 학위논문]** — 국립한국해양대학교 대학원 학위논문 작성 지침(개정 2024.10.30) 적용
- 체계 순서: 외표지 → 간지 → 속표지 → 인준지 → 목차 → 영문초록 → 본문 → 참고문헌 → 국문초록 → 감사의 글
- 편집 규격: A4, 여백 위30/좌우30/아래15mm, 본문 10~11pt 줄간격 160~200%, 각주 9pt, 서체 휴먼명조
- 목차 체계: `제 X 장 → 제X절 → Ⅰ. → 1.` / 쪽번호 i ii iii (중앙)
- 초록: 영문 제목 20pt, 성명·학교 13pt, 본문 11pt, Keywords 6개 이내
- 참고문헌: 국내(단행본 『』/논문 「」) → 국외(이탤릭·쉼표 방식) 구분
- 박사 제출: 4부 + PDF 온라인 선제출 / 심사위원 5인 (지도교수는 위원, 위원장 불가)

**[모드 B: 소논문]** — 한국해사법학회 「해사법연구」 투고 기준
- 인용 형식: `홍길동, "논문 제목", 「해사법연구」 제○○권 제○○호, 한국해사법학회, 2021.00, ○○면.`
- 투고카드: 논문 접수번호·소속·학술대회 발표 여부·연락처·별쇄본 수령 주소 작성
- 투고 전 체크리스트: 국문초록·주제어(5개)/Abstract·Keywords, 연구윤리, 익명심사 대비

**[공통]** 모든 법령·판례 인용은 korean-law MCP(`search_law`, `search_decisions`, `verify_citations`, `chain_amendment_track`)로 실재 확인 후 기재 — 전거 미확인 인용 절대 금지. 법학 문체(사견 구분, 양시론 금지, 법문/판례/학설 근거 명시) 적용.

**[참고 규격 원본]** `~/Downloads/` 내 투고양식.hwp, 투고카드-1.hwp, 학위논문 작성 지침.hwpx

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

---

## mattpocock/skills 접목 스킬 (2026-06-24 추가)

> 출처: https://github.com/mattpocock/skills — "Skills for Real Engineers"  
> 원본을 Hermes 환경(Python 3.14, 텔레그램 봇, L1/L2/L3 메모리)에 맞게 한국어 적용

### grill-me — 작업 시작 전 요구사항 인터뷰

**형태**: 지식 스킬  
**파일**: `~/.hermes/skills/grill-me/SKILL.md`  
**생성일**: 2026-06-24

**이렇게 부르면 됩니다**
- "grill해줘", "파고들어", "요구사항 먼저 정리하자", "grilling"

**실행 시 일어나는 일**
복잡한 구현 요청 전에 Claude가 설계 트리를 따라 질문 하나씩 — 추천 답변과 함께. 공유된 이해에 도달하면 구현 시작. 의도 불일치로 인한 재작업 방지.

---

### grilling — 집요한 인터뷰 루프 (grill-me의 실행 엔진)

**형태**: 지식 스킬  
**파일**: `~/.hermes/skills/grilling/SKILL.md`  
**생성일**: 2026-06-24

**이렇게 부르면 됩니다**
- grill-me 스킬이 내부 호출 / "grilling 시작"

**실행 시 일어나는 일**
설계 트리 각 분기를 걸어 내려가며 결정 간 의존성 해소. Hermes 특화 체크리스트(Lock Stack, Python 3.14 호환, import chain) 포함.

---

### diagnosing-bugs — 구조화된 버그 진단 6단계 루프

**형태**: 지식 스킬  
**파일**: `~/.hermes/skills/diagnosing-bugs/SKILL.md`  
**생성일**: 2026-06-24

**이렇게 부르면 됩니다**
- "버그 찾아줘", "왜 안되지", "diagnose", "먹통 원인", "에러 원인 파봐"

**실행 시 일어나는 일**
Phase 1(피드백 루프 구축) → Phase 2(재현+최소화) → Phase 3(가설 3~5개) → Phase 4(계측) → Phase 5(수정+회귀테스트) → Phase 6(정리+06번 보고서 기록). 피드백 루프 없이 코드 읽어서 가설 세우는 것 금지.

---

### claude/hermes 스킬 통합 계획 (보류 중 — 2026-06-24)

- `~/.claude/skills/` 15개 중 실제 내용 있는 것: `mj-meta-update`, `mj-stock-analyze` 2개. 나머지 13개 빈 껍데기.
- Claude Code를 쓰지 않게 되면 claude 스킬은 무용지물 → 의미 있는 스킬은 `~/.hermes/skills/`로 통합 예정.
- **보류 항목**: `mj-meta-update` → hermes meta-update에 내용 병합 / `mj-stock-analyze` → hermes stock-analyze로 복사 / 빈 껍데기 13개 삭제.
- MJ님 승인 후 진행.

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

---
*최종 업데이트: 2026-06-24 21:00*
