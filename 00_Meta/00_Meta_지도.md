---
tags: []
---
# 🗺️ 00_Meta 디렉터리 통합 지도 (Map of Content)

> [!INFO] 💡 문서의 역할 (지식 내비게이션)
> 이 문서는 `00_Meta` 폴더 내에 혼재된 40여 개의 핵심 설정 파일, 장부, 보고서, 가이드 문서들을 성격별로 분류해 놓은 **'내비게이션 지도(MOC)'**입니다. 
> ⚠️ **원칙**: 이 폴더에 새로운 문서를 생성할 경우, 에이전트는 반드시 이 지도 문서에도 해당 파일의 링크와 설명을 추가하여 지도를 최신 상태로 유지해야 합니다.

---

## ⚙️ 1. 코어 설정 파일 (Core Config)
시스템과 봇의 두뇌 역할을 하는 핵심 환경/설정 파일입니다.
- USER - 박사님(사용자)의 선호 AI 스택(llama.cpp 등)과 페르소나 설정
- ~~memory - 에이전트의 단기/장기 메모리 데이터~~ **[2026-05-27 archive/99_Archive/로 이관 — Dreaming 폐기로 정적화]**
- guardrails - 안전망 및 제한 규칙 설정
- INDEX - 메타 인덱스 관리 파일
- `semantic_index.db` - 로컬 RAG 검색을 위한 벡터 데이터베이스 파일
- CLAUDE - 🆕 2026-06-08: Claude Code 세션 초기화 포인터 파일 (`~/.claude/CLAUDE.md` 심볼릭 링크 연결). 세션 시작 시 읽을 문서 순서 지정. **Claude.ai 채팅용 `claude_briefing.md`와 쌍으로 운용.**

## 📜 2. 심볼릭 링크 헌법 (Symlinked Rules)
옵시디언에서 관리하지만 봇의 뇌(`~/.hermes/`)로 심볼릭 링크(거울)가 연결된 시스템 절대 규칙들입니다.
- constitution - 봇 시스템 전체 헌법
- constitution.local - 로컬 환경에 맞춰진 헌법 보완 파일
- HERMES - 에이전트 코드베이스 및 아키텍처 규칙
- _meta.py — `/claude_brief` (4대 메타 문서 브리핑 생성) · 🆕 `/save_wiki` (대화 분석 결과 wiki 저장) · 🆕 `/wiki_lint` (고아/오래된/깨진링크/빈 페이지 탐지)
- hermes_harness_skill_모음 - 🆕 2026-06-09: 커스텀 스킬 목록 + 호출 방법 + 동작 설명 관리 문서

## 📓 3. 시스템 운영 장부 (Meta Ledgers)
에이전트와 박사님이 실시간으로 시스템 상태를 기록하고 공유하는 메인 장부들입니다. **가장 자주 확인해야 하는 곳**입니다.
|- 01_hot - 현재 프로젝트 핫토픽 및 투두 리스트
|- 시스템_구조적_결함_분석 - 🆕 2026-05-27: 3종 구조적 결함 Post-Mortem + 잠재 리스크 — 다른 AI 분석용
|- 06_에이전트_오류_및_재발방지_보고서 - 🆕 2026-06-04: 세션 컨텍스트 이탈 및 추측성 답변 장애 원인 및 방지 대책
|- 05_시스템 상태 - 엔진 변경 이력과 현재 에이전트 작업 상황
||- HERMES3_MASTER_DEVELOPMENT_GUIDE - Hermes3 마스터 개발 로드맵 (v9.2 완료, v9.4+ 계획: LLM Distiller/Skills Hub 후보)
|- V9.0 프로그램 추가 2 -v9.4+ 외부 참조 제안서 (SkillSpector/CyberAuditor/SRE Investigators) **[설계 제안 단계, 미구현]**
|- Hermes_v8.1_종합_사용_설명서 - v8.1 Self-Healing Loop + Live Sync + Cron 통합 가이드
|- 03_시스템 인벤토리 - 설치된 런타임, 포트 및 환경 구성표
|- 02_스크립트 정보 - 전체 파이썬 스크립트 작동 원리 및 텔레그램 명령어 가이드. 🆕 2026-06-09: **루프 안전 시스템 빠른 진단 가이드 섹션 추가** (Circuit Breaker / Mayor / ToolResult / Context Compaction / 루프 자기검증 — 연결 구조도 + 증상별 진단표 + 상수 변경 가이드). **장애 발생 시 이 파일 하단부터 확인.**
|- 메모리_파일_명세서 - **모든 JSON/L 메모리/상태 파일의 위치·계층·코드 참조 전수 명세** (00_Meta 현역)
|||| 04_주요 시스템 가이드 및 FAQ - 시스템 문제 해결법 및 핵심 교훈 요약 백과사전
|- Hermes1_재시작_터미널_능력 - 🆕 2026-05-31: Hermes1 봇 /restart_bot 및 /exec 명령어 아키텍처 명세
|- 헤르메스2_텔레그램_터미널명령어_처리_이슈 - 🆕 2026-06-01: 텔레그램 raw 명령어가 LLM 채팅으로 처리되어 미실행되는 이슈 문서
|- 텔레그램_메모리_버튼_작동_원리_및_안전성_검증 - 🆕 2026-06-05: 텔레그램 메모리 정리 버튼 작동 원리, sync & purge 안전성 검증 및 로컬 LLM 램/VRAM 확보 가이드
|- AI Agent Memory 개념 분석 - 🆕 2026-06-05: 4계층 메모리 스택/4대 연산 비교 분석 결과 (01_hot.md 섹션 참조)
|- `switch_model.sh` — 🆕 2026-06-06: 모델 전환 자동화 스크립트 (`~/Applications/venu/scripts/switch_model.sh` → `/usr/local/bin/switch-model`). 사용법: `switch-model got` or `switch-model deepseek`.
|- WebUI_멀티모델_통합_장기화_원인분석_20260607 — 🆕 2026-06-07: WebUI Qwen/GPT OSS 120B/Minimax 3종 통합 장기화 5계층 원인 분석 + 미래 모델 추가 체크리스트 + 10K 토큰 시스템 프롬프트 분석
|- 자동화_시스템_사용법 — 🆕 2026-06-10 전면 재작성: **전체 하네스 통합 가이드**. Claude Code 5-Layer OS (L1~L5), Self-Harness 3단계 루프 (WeaknessMiner/ProposalValidator), 훅 3개 상세, 서브에이전트, MCP, Wiki+Scripts Git, 텔레그램 명령어 전체, 데이터 누적 로드맵, 문제 해결 빠른 참조. Self-Correction Loops 아티클 3제안 MJ 시스템 적용 분석 포함.
|- 주식 프로그램 및 주식 스크립트와 연동계획 — 🆕 2026-06-10: V_FINAL 전략 완전 가이드. 텔레그램 7개 명령어 상세 사용법, MCP 서버 사용법, Webull 연동 워크플로우, 개선 루프, 에러 진단 가이드 포함.
|- Phase1_Phase2_개선_설명서 — 🆕 2026-06-09: Phase 1(낙관적 응답) + Phase 2(세밀한 메모리) 시스템 개선 상세 설명. 구현 구조, 해결 갭 4개, 시너지 효과, 수치 기대 효과 포함. Phase 3 설계 참조 포인터.
|- ~~하네스_업그레이드_로드맵_20260611~~ — 2026-06-11 갭 진단 9건 전부 완료(2026-06-11 실행현황 확인). **2026-07-02 삭제** — 잔여 미해결 서브노트 1건은 `HERMES3_MASTER_DEVELOPMENT_GUIDE.md` "흩어진 미완료 항목 통합" 표로 이관.
|- skill_auditor — 🆕 2026-06-11: Runtime Skill Auditor. ~/.hermes/skills/ 전체 동적 감사. 위험 패턴 10종(시스템명령/외부HTTP/동적실행/역직렬화 등) 탐지. 3단계 위험도(CLEAN/REVIEW/SUSPICIOUS). 로그: skill_audit.log.
|- test_layer_harness — 🆕 2026-06-11: Layer-Isolated Evaluation Harness. LLM 없이 19개 결정론적 테스트, 1.31초. 4개 레이어(메모리정제/에이전틱루프/파일무결성/핸들러) 독립 검증.
|- HANDOFF — 🆕 2026-06-11: Architect Loop 상태 파일. Claude Code(Architect)↔DeepSeek(Builder) 핸드오프. 슬라이스 스펙·빌드 결과·미결 이견·결정 로그 포함. 작업마다 Builder가 업데이트, Architect가 판결.
|- verify_harness_report — 🆕 2026-06-09: `/verify_harness` 실행 시마다 자동 갱신. 현재 상태(전체 진단 결과) + 📈 이력 테이블(최근 20회 자동 보존). **시스템 점수 추이를 시간순으로 추적 가능. 구조 개선 전후 비교 기준점.**
- Claude_Code_Hermes_통합_아키텍처 — 🆕 2026-06-08: Claude Code ↔ Hermes 연결 구조, 시스템 성장 메커니즘 (L1/L2/L3), bio_memory_engine LLM 독립성, Dreaming 버튼 원리, 전체 성장 결론. **"어떤 도구로 작업해도 성장 + Dreaming = 모든 계층 성장"**
|- `HERMES_HOME 과 환경 변수의 진짜 물리적 지도 (Fact Check) 20260607` — 🆕 2026-06-07: 2-인스턴스 테이블, 포트맵, plist 목록, API Key, config.yaml 전체 구조, WebUI 아키텍처, venv 패치 경로, GGUF n_ctx, 10K 시스템 프롬프트 총정리

- **2026-06-10 업데이트 (Self-Harness 5-Layer 강화)**: Wiki Git 초기화(306개 문서), SessionStart/Stop/PostToolUse Hook 3개 추가, `weakness_miner.py` 신규(모듈 80개), Claude Code 에이전트 2개(meta-updater/hermes-debugger), Skills 2개(mj-meta-update/mj-stock-analyze), stock-scanner MCP 연결. 신규 문서: Wiki_Git_사용법, 자동화_시스템_사용법.
- **2026-06-10 업데이트 (주식 시스템 V_FINAL)**: 주식 분석 시스템 전체 구축 — `modules/stock_*.py` 4개 신규, `handlers/_stock.py` 7개 텔레그램 명령어(/stock /scan /market /watchlist /positions /result /backtest), `stock_mcp_server.py` Claude Code MCP 서버(✓Connected). V1.8→V3.0 전략 병합. modules 63개. handlers 18개. 문서: `wiki/주식 프로그램 및 주식 스크립트와 연동계획.md` 전면 재작성.
- **2026-06-09 업데이트 (Phase 2)**: 메모리 정제 엔진(`modules/memory_refinement.py`) 신규 — Forget 자동 정리/충돌 감지/저장 판단/hybrid recall(L2+FTS5 병합). `/memory forget`, `/memory health` 추가. modules 59개.
- **2026-06-09 업데이트 (Phase 1)**: 낙관적 응답 엔진(`modules/optimistic_response.py`) 신규 — Linear 아키텍처 패턴(즉시 피드백→백그라운드→편집). `/ingest` 3분기 통합, `/retry` 명령어 추가.
- **2026-06-09 업데이트**: `/verify_harness` 구조 진단 명령어 신규 구현 (`modules/harness_verifier.py` — 파일비대화/SRP/문서표류/서비스/메모리/임시파일 6항목 100점 측정). AgentForge 4패턴 + Stage 5 루프 가드레일 3종 완료 — Circuit Breaker, Prompt Injection 방어(ToolResult), Context Compaction, ToolResult 구조화, Mayor 에이전트(`modules/mayor_agent.py` 신규), 토큰 예산 가드레일, 루프 자기검증(CoVe Step5 자동). `/orchestrate mayor` 대시보드 추가.
- **2026-06-08 업데이트**: LLM 환각 방지 3계층 구현 (briefing 미사용 스택 명시 + harness_agent 자동 주입 + CoVe Step5 파일시스템 검증). curator.py 코드베이스 편집자로 확장. /help 전면 재작성.
- **2026-06-07 업데이트**: WebUI 3종 멀티모델 통합 완료. NIM 70B(meta/llama3-70b-instruct 서비스 종료) → GPT OSS 120B(openai/gpt-oss-120b) 전환. Skills 115개 + toolsets [browser, vision] 비활성화 → Qwen 첫 응답 77s로 개선.
- **2026-06-06 업데이트**: `~/.hermes/config.yaml`와 `~/Applications/venu/.hermes2/config.yaml`에 전체 toolsets를 포함하도록 적용.

||| 00_Meta_지도 - (현재 문서) 메타 폴더 내비게이션 파일
|| ~~주간_펄스_리포트 - 주간 시스템 펄스 리포트 (매주 일요일 23:00 자동 생성, weekly_pulse.py)~~ **[2026-05-27 weekly_pulse 폐기로 제거]**

## 📖 4. 시스템 운영 가이드 및 매뉴얼 (Manuals)
각종 에이전트와 스크립트의 상세 사용법을 정리한 설명서입니다.
- 헤르메스봇_가이드, 나의 비서 가이드, 에이전트 교육 및 핸드오버 매뉴얼
- Harness V2.5 가이드북, Hermes Codebase Harness 가이드, 하네스_컨트롤_가이드
- Hermes_서브에이전트_시스템_가이드 - 🆕 서브에이전트 위임(delegate_task) 아키텍처 설명 — DeepSeek/Gemma4/NVIDIA 병렬 작업
- Hermes_v8.1_종합_사용_설명서 - 🆕 v8.1 전체 아키텍처 구조도 + 9개 기능 상세 설명 + 실행 명령어 일람 + FAQ
|- Bio_Memory_Engine_가이드 — 🆕 v9.3: Hybrid Trigger 개수/1MB, 강제 증류, Atomic Write, Early Exit 우회
- hermes_kanban_guide
- 맥봇_상세_가이드
- 논문_워크플로우_가이드 - 🆕 2026-06-01: arXiv/논문 스킬 및 워크플로우 종합 가이드 (연구 작업용)
- 파일조작 명령어 가이드
- 하네스_기능_및_버튼_활용_정의
- 헤르메스_help_text_시스템_구조 — 🔄 **통합본** (파일조작 가이드 흡수, 33개 명령어 완전판 + Help Text 수정 구조)
- ~~파일조작 명령어 가이드~~ **[2026-06-03 삭제 — 헤르메스_help_text_시스템_구조.md로 통합]**
- runbook_launchd, runbook_recovery, runbook_telegram, runbook_upgrade (docs/ → 이관)
- `wiki_auto_stamper.py` — wiki 타임스탬프 자동 복구 도구 (`/Users/bluesea/Applications/Mjauto/Scripts/wiki_auto_stamper.py`)

## 📊 5. 일회성 분석 보고서 및 기획서 (Reports / Archive)
과거에 시스템 분석이나 기획을 위해 한시적으로 작성되었던 문서들입니다.
- **분석 보고서**: 보관소_유사도_분석보고서, 파일_디렉터리_구조_및_상호연결성_점검결과, 규칙_통합_결과보고서, 카파시_메모리_시스템_적용_점검
- **기획안**: 보관소_지식_Deduplication_계획서, 비서_시스템_메타_문서_비교_정의, 맥스튜디오_지능화_구상도
- **v8.1 관련**: v8.1_작업_결과_보고서_20260528 - 🆕 4일간 9/9 완료 결과보고서 + 딥시크_구현_지시문_v8.1 - 원본 구현 지시문
- **기타 목록**: 옵시디언_설치된_플러그인_목록, 추천_MCP_서버_목록, 홈디렉토리_정리_후보목록, llama_server_launchd_troubleshooting, 하네스 파일권한 상향, 헤르메스_이관_및_가족_공유_아키텍처_전략

## 📁 6. 하위 폴더 (Sub-Directories)
- `장애 기록/` - 날것의 에러 로그와 해결 과정을 기록하는 사건 현장 일지 (Post-mortem)
- `MacBot/` - MacBot 관련 데이터
- `skills/` - 에이전트 스킬 파일 폴더
- `archive/` - 내용이 통합·대체되어 보관된 레거시 문서들 (예: `(Hot.md파일관련)Memory_시스템_설계.md` → 메모리_파일_명세서로 통합)
- `memory_engine/` - Hermes 메모리 엔진 관련 스크립트 및 빈 consolidator_state.json 파일

---
🔗 **관련 문서 링크**
- 02_스크립트 정보
- 05_시스템 상태

|*최종 업데이트: 2026-07-02 15:06*
*추가: 2026-06-06 13:10 — switch_model.sh (모델 전환 스크립트) 참조 추가*
*추가: 2026-06-05 — AI Agent Memory 개념 분석 참조 항목 추가*
*작성자: 헤르메스 시스템 아키텍트*

## 신규 문서 — 2026-06-12

| 파일 | 설명 |
|---|---|
| `하네스_논문_기반_개선_로그.md` | 논문 11편 기반 하네스 개선 전체 기록 (Why/What/How + 미적용 후속 항목) |

*최종 업데이트: 2026-07-02 15:06*

## 신규 기능 — 2026-06-21

| 파일 | 변경 내용 |
|---|---|
| `modules/wiki_manager.py` | `write_wiki()` · `lint_wiki()` 메서드 2개 추가 — Karpathy LLM-Wiki 패턴 적용 |
| `handlers/_meta.py` | `/save_wiki` · `/wiki_lint` 핸들러 2개 추가 (`/claude_brief` 기존 유지) |

*최종 업데이트: 2026-07-02 15:06*

## 신규 문서 — 2026-06-28 (MJstock/MJcoin)

| 파일 | 설명 |
|---|---|
| `~/Applications/Mjstock/docs/MJcoin_사용설명서.html` | 빗썸 코인 스크리너 사용설명서 — 삼돌이 3조건·3축점수·BTC방향필터·스테이블코인필터 |
| `~/Applications/Mjstock/docs/quant_logic_analysis.html` | v1.1→v1.2 업데이트 — KIS 100봉 한계 원인·조치 전체 기록 (US/KR 모두) |
| `~/Applications/Mjstock/Coin/` | 코인 스크리너 폴더 신설 (bithumb_api/data_loader/screen_samdoli/auto_scan/config) |

*최종 업데이트: 2026-07-02 15:06*
