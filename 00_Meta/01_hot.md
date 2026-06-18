## ⚖️ 최근 감사 결과 (Dreaming)
**[목표 진척도]**
사용자의 기술적 문제(명령어 오류, 메모리 구조화)에 대해 구체적인 해결책과 설계안을 제시함으로써 '유용성' 측면에서 높은 진척도를 보이고 있습니다. 요청된 데이터 구조화 및 관리 설계 작업을 즉각 수행하며 장기 목표를 충실히 이행 중입니다.

**[헌법 준수 감사]**
결론을 먼저 제시하는 역피라미드 구조와 전문 용어를 활용하여 MJ님의 스타일 프로필을 충실히 준수하고 있습니다. 불필요한 수식어나 메타 해설을 지양함으로써 'AI 냄새'를 효과적으로 제거하고 시스템의 핵심 가치인 신뢰성을 유지하고 있습니다.

# 📝 프로젝트 핫토픽

**최종 업데이트:** 2026-06-09 21:00

## 📠 실시간 상태 (KV — /status 명령어로 설정)
- **Active External Project**: `/Users/bluesea/Applications/MarineOS-XR Project` (우선 스캔 경로)
- **Current Model (Telegram)**: GPT OSS 120B (기본, NVIDIA API) / DeepSeek API (폴백) / Qwen2.5-14B 로컬 (선택 가능)
- **Current Model (WebUI)**: Qwen2.5-14B (로컬) / GPT OSS 120B (NVIDIA) / Minimax M2.7 (NVIDIA) — 3종 멀티모델 통합 완료
- **llama-server**: 종료 가능 (Telegram GPT OSS 120B 모드 + WebUI 비-Qwen 선택 시 영향 없음)

## 📌 현재 진행 중인 작업

### ✅ 완료 — MJstock /mjstock 텔레그램 온디맨드 분석 (2026-06-18)
- **`scan_single.py` 신규**: 단일 종목 × 검색식 → 점수 계산 + 차트 즉시 생성 (시간 제한 없음)
- **`_stock.py` `cmd_mjstock` / `callback_mjstock` 추가**: 인라인 버튼으로 검색식 선택 → 결과+차트URL 회신
- **`_callbacks.py`**: `mjstock:` 콜백 라우팅 추가
- **`hermes_local.py`**: `/mjstock` CommandHandler 등록

### ✅ 완료 — MJstock 헬스체크 + 설정 탭 + 사용설명서 (2026-06-18)
- **`health_check.py` 신규**: 평일 18:00 crontab 자동 실행. 스캔 실행 여부/로그 에러/수익률 채움/퀀트 누적 현황 체크 → 텔레그램 일일 리포트
- **`app.py` 설정 탭(tabs[5]) 신규**: 텔레그램 봇 토큰/채팅 ID 입력·저장, 채팅 ID 자동 조회, 테스트 발송, 연동 상태 요약 — 가족 배포용 자기 계정 알림 설정
- **`MJstock_사용설명서.html` 업데이트**: 설정 탭 사용법(텔레그램 연동) + 모바일 대시보드 접속 방법 섹션 추가

### ✅ 완료 — MJstock 더블 발송 버그 수정 + 모바일 대시보드 (2026-06-18)
- **더블 발송 버그 수정**: `auto_scan_nasdaq500.py`가 `run_scan.py` × 8 호출 → 각각 텔레그램 발송 = 8+1건 → `--no-telegram` 플래그로 차단, 요약 1건만 발송
- **`mobile_dashboard.py` 신규**: Python 내장 http.server, 포트 8765, 같은 WiFi 폰 접속, 검색식 카드 + 종목 점수바 + 5분 자동 새로고침

### ✅ 완료 — MJstock 유니버스 확장 + 티커 검색 + UI 개편 (2026-06-18)
- **유니버스 전면 확장**: 나스닥1000 / 코스피946 / 코스닥1000 실 데이터 CSV 생성 (FinanceDataReader + NASDAQ FTP)
  - `data/nasdaq1000.csv` — 나스닥 상장 시총 상위 1000종목
  - `data/kospi_full.csv` — 코스피 전체 946종목 (시총 정렬)
  - `data/kosdaq_full.csv` — 코스닥 전체 시총 상위 1000종목
  - `data/dow30.csv`, `data/russell1000.csv` — 기존 유지
- **슬라이더 0~1000 통일**: 0=전체, 오른쪽으로 밀면 상위 N개 (소형주 제외용)
- **유니버스별 자체 1000개**: 보완 로직 제거, 각 CSV가 독립적으로 최대 1000개 보유
- **스캐너 탭 UI**: 미국/한국 선택 → 유니버스 버튼(4개/2개) → 슬라이더 → 검색식 카드형 박스
- **차트 탭 티커 직접 검색**: 티커/종목코드 입력 → `--single-chart` 모드로 차트 즉시 생성
- **FRESH_TREND 버그 수정**: KIS API 100봉 제한 대응 — EMA200 조건 불가 시 EMA50 기울기로 fallback
- **공중★ 하락 해석**: `signals_entry_points.html` GONGJOONG 설명에 "급등 말미 = 에너지 소진 경고" 추가
- **`data_loader.py`**: `get_us_universe_tickers()`, `get_kr_universe_tickers()` 신규 함수 추가
- **`run_scan.py`**: `--universe`, `--top-n`, `--single-chart` 파라미터 추가

### ✅ 완료 — MJstock UI 개선 + 실험 필터 시스템 (2026-06-18)
- **스캐너 탭 중복 제거**: 스캔 결과 차트 버튼 그리드 제거 → 통과 종목 수 안내 + "차트 보기 탭으로 이동" 메시지로 교체
- **차트 탭 점수 정렬**: `run_scan.py`에서 farming signals + `compute_score()` 직접 계산 → CSV `score` 컬럼 → 차트탭 내림차순 정렬 + 버튼에 "N점" 표시
- **실험 필터 토글**: `compute_exp_filters()` 함수 신설 (run_scan.py) — FRESH_TREND/IS_LEADER/IS_TIGHT 3종, US+KR 12개 검색식 통합 적용
- **Best Signal 문구**: `*(수동 설정값 — 스캔 데이터 30일 누적 후 실제 승률로 자동 변경됩니다)*` 추가
- **문서 업데이트**: `MJstock_사용설명서.html` (Step 5/6, 탭 설명), `quant_logic_analysis.html` (§9 실험 필터), `signals_entry_points.html` (§9 보조지표 독법, §10 과거이력), `korean_original_formulas.html` (SEPA/GROK 아카이브)

### ✅ 완료 — 메타인지 Faithful Uncertainty 룰 적용 (2026-06-18)
- `harness_agent.py` `_FIXED_SYS_PROMPT` Rule 12 신설: `[확실]`/`[추론]`/`[불확실]` 3단계 접두어, 사실·정보 질문에만 적용
- 기대 효과: 불필요한 [SEARCH] 감소 + 환각(확신에 찬 오류) 감소
- 출처: Google 논문 "Hallucinations Undermine Trust; Metacognition is a Way Forward"

### ✅ 완료 — 텔레그램 봇 장애 전체 해결 (2026-06-17)
- ISP 차단은 공유기 재부팅으로 해결됨
- 워치독 오탐(메시지 없는 조용한 상태를 행으로 오판) 수정: 하트비트 파일 기반으로 전환, 텔레그램 알람 제거
- `hermes_local.py` 폴링 루프에 `_HEARTBEAT.touch()` 추가 (15초 주기, `~/.hermes/runtime/bot_heartbeat`)
- `check_bot_alive.sh` 최종: 하트비트 mtime 3분 정지 기준, 내부 동작만(알람 없음), SIGTERM 우선

### 🚨 미해결 — 텔레그램 SNI 차단으로 Hermes1 무응답 (2026-06-17)
- **진짜 원인**: 코드/프로세스 문제 아님. **ISP가 api.telegram.org에 대한 TLS SNI 차단** 중 — 일반 인터넷(Google 등)은 정상, 텔레그램 IP 일부는 TCP는 열려도 TLS 핸드셰이크에서 멈춤(`curl` `000`). 그동안의 "행"·"크래시 루프"·"Conflict" 증상은 전부 이 네트워크 차단으로 인한 재연결 시도의 부작용이었음
- **확인 방법**: `curl --max-time 6 https://api.telegram.org` → `000` 이면 차단 상태. `curl https://www.google.com`은 정상(`200`) — 도메인 특정 차단 확인 포인트
- **현재 이 Mac에 활성 VPN 없음**
- **해결책**: VPN 연결 또는 다른 네트워크(핫스팟) 전환, 혹은 ISP 차단이 풀릴 때까지 대기. 봇 프로세스 자체는 정상 대기 상태이므로 네트워크만 풀리면 자동 복구됨
- **부수 효과**: 디버깅 중 `hermes_local.py`의 `except Exception: pass`(폴링 종료 시 원인 완전 삼킴)를 발견 → `logger.error(f"[Polling 종료 원인] ...")`로 수정해 향후 같은 문제 빠르게 진단 가능해짐

### ✅ 완료 — Hermes1 행(hang) 워치독 도입 + 크래시 루프 추가 수정 (2026-06-17)
- **1차 장애**: 텔레그램 API 네트워크 오류(`httpx.ReadError`) 폭주 후 폴링 루프가 죽지도 않고 멈춤(행) → launchd `KeepAlive`는 프로세스 종료시만 재시작하므로 무인 감지 안 됨 (3시간 30분간 무응답)
- **1차 조치**: `check_bot_alive.sh` 신규 — 로그 mtime 10분 이상 정지 시 강제 재시작 + 텔레그램 알림. `com.hermes.botwatch` LaunchAgent로 5분마다 자동 실행
- **2차 장애 (워치독의 부작용)**: 워치독이 `kill -9`로 죽이자 텔레그램 서버측 getUpdates long-poll 연결이 즉시 안 끊김 → 5초 만에 뜬 새 인스턴스가 `telegram.error.Conflict: terminated by other getUpdates request`로 즉시 충돌·종료 → `ThrottleInterval=5` 재시작 → 또 충돌, 무한 크래시 루프 (실제 발생, MJ 신고로 발견)
- **2차 조치**: `launchctl unload` → `pkill`로 완전 정지 후 60초 대기(서버측 연결 만료) → `launchctl load`로 1회 정상 기동 확인(Conflict 재발 없음). `check_bot_alive.sh`를 SIGTERM 우선(최대 5초 대기) → 그래도 살아있으면 SIGKILL 방식으로 수정, kickstart 전 대기를 2초→5초로 늘림
- **잔여 검토**: `hermes_local.py` 폴링 루프에 httpx 타임아웃 명시 + 하트비트 파일 기록 (근본 원인 완화, 코드 수정 필요해 보류 중)

### ✅ 완료 — 논문 5편 기반 Hermes 강화 v9.3.2 (2026-06-11)
- **Goal-Autopilot** `agentic_loop.py` — `_verify_gate()` 추가, RUN_CMD/CREATE 거짓 완료 보고 구조적 차단
- **Sycophancy Filter** `memory_refinement.py` — 아첨 패턴(80자 미만 동의) L2 저장 차단
- **HORMA 계층 검색** `memory_refinement.py` — context_tags 클러스터 기반 hybrid_recall() 효율화
- **Layer-Isolated Harness** `tests/test_layer_harness.py` 신규 — 19개 결정론적 테스트, 1.31초
- **Runtime Skill Audit** `modules/skill_auditor.py` 신규 — 10종 위험 패턴, 3단계 분류

### ✅ 완료 — Architect Loop 워크플로우 도입 (2026-06-11)
- `wiki/00_Meta/HANDOFF.md` 신규 생성 — Architect↔Builder 상태 공유 파일
- `harness_agent.py` + `CLAUDE.md` 응답 품질 원칙 4개 추가 (핵심 먼저·증거 기반·질문 시 분석만·재논의 금지)
- `자동화_시스템_사용법.md` §13 Architect Loop 섹션 신규
- 역할: Claude Code(Architect) + DeepSeek WebUI(Builder) + Gemini(Reviewer) + Perplexity(Research)

### ✅ 완료 — 봇 이중 기동 근본 해결 + /claude_brief 수정 (2026-06-11)
- `hermes_local.py` — `fcntl.flock` → PID 파일 자동 교체 방식으로 변경. 출장 중 무인 운영 안정화
- `handlers/_meta.py` — `safe_reply` import 누락으로 `/claude_brief` 미동작 수정

### ✅ 완료 — P2-④ semantic_index ↔ memory 연동 + _stock.py safe_reply 완전 적용 (2026-06-11)
- `hybrid_recall()` 3소스 통합: L2 + knowledge_indexer FTS5 + **semantic_index.db FTS5** (신규)
- `_stock.py` 잔여 28곳 safe wrapper 적용 완료 (전체 핸들러 255개 적용)
- **잔존 P2**: GitHub Remote(URL 필요) / P3: /harness_report 월간 대시보드

### ✅ 완료 — 하네스 업그레이드 로드맵 P1 전체 실행 (2026-06-11)
- **① L3 자동 증류**: `auto_dream_trigger.py` + launchd `com.hermes.autodream.plist` (일요일 03:30)
- **② 문서 표류 보정**: `claude_briefing.md` 갭 섹션 3개 항목 ✅ 보정
- **③ safe_reply/safe_edit 전체 적용**: 핸들러 14개 파일 219곳 — `BadRequest` Markdown 크래시 방어 완료
- **⑤ 모듈 분할**: `ingest_text_utils.py`, `indexer_text_utils.py` 신규 분리
- **⑦ yf.download + 일별 캐시**: `/scan` rate limit 장애 해소, 하루 1회 캐시
- **Hermes1 재시작**: PID 95296 (변경 활성화 완료)
- **잔존 P2**: semantic_index↔memory 연동 / GitHub Remote(URL 필요) / 월간 harness_report

### ✅ 완료 — /verify_harness 95/100 S등급 달성 (2026-06-09)
- harness_agent.py 887→319줄 3차 분할 완료 효과 반영
- 잔존 경고: bio_memory_engine.py(877줄·Lock Stack), ingest_engine.py(642줄), knowledge_indexer.py(631줄)
- `_archive/hermes_handlers_backup_20260526.py` — 이미 보관됨, 무시 가능
- **다음 세션 과제**: ingest_engine.py / knowledge_indexer.py 분할 (Lock Stack 아님)

### ✅ 완료 — V_FINAL v1.4 — ADX 점수 + 4티어 스캔 (2026-06-10)
- ADX 추세 강도 점수 추가: ADX≥60:+0.5 / ADX≥40:+0.25 → 최대 점수 9.0pt
- 4티어 스캔: /scan buy/watch/strong/sepa — strong 티어가 RDW 타입 포착
- 다음: 봇 재시작 후 /scan 결과 4티어로 확인

### ✅ 완료 — 주식 전략 V_FINAL v1.3 — 5가지 개선 적용 (2026-06-10)
- **REVERSAL 부분점수화**: macd_cross(0.75)+ema_cross(0.50)+rsi_zone(0.25) 3개 독립 → 이전 5조건 일괄 대비 점수 활용률 대폭 개선
- **펀더멘털 필터**: EPS>15% / 매출>10% / 흑자. yfinance `.info` 7일 캐시 (fundamentals_cache 테이블 신설)
- **실적발표 필터**: `days_to_earnings > 10` (yfinance `.calendar`). 발표 10일 이내 매수 보류
- **트레일링 스탑**: ATR 기반. `max_price` 추적 → `trailing_stop = max_price - 원래손절폭`. 스탑은 위로만 이동
- **섹터 RS 보너스**: 11개 섹터 ETF RS 순위 계산 → 상위 4개 소속 종목 +0.5점. 최대 점수 7.5→8.5
- **문서**: 위키 5레이어 구조도 전면 갱신 (수식 완전 정리)
- **다음 과제**: 봇 재시작 후 실데이터 스캔으로 v1.3 결과 확인

### ✅ 완료 — Self-Correction Loops 아티클 + Self-Harness 전체 구현 완성 (2026-06-10)
- **Self-Correction Loops 아티클 3제안 분석** 완료 — MJ 시스템 장단점 및 개선안 문서화
- **Proposal Validator** (`modules/proposal_validator.py`) 구현 — Self-Harness 3단계 완성
- **WeaknessMiner 전 핸들러 확장** — 3→6핸들러, 3→14포인트
- **Claude Code 5-Layer OS 전체 완성** — L1~L5 모두 운영 중
- **자동화_시스템_사용법.md 전면 재작성** — 구조도 병합, 아티클 분석, 전체 사용법 통합
- **핵심 미완**: GitHub Remote (URL 필요) / `/harness_report` 월간 대시보드

### ✅ 완료 — 아티클 3종 분석 + Loop Engineering 적용 결론 (2026-06-10)

**분석 대상**:
1. Loop Engineering (addyosmani) — 5 Pillars
2. The AI Agent Stack the Creator of Claude Code Uses (Av1dlive) — Boris Cherny HIVE 3티어
3. How to Build a Hermes Agent... (gkisokay) — Buildroom / Auto-think / Auto-build

**결론 — 이미 구현된 것 (85%)**:
| Pillar | Hermes 대응 |
|---|---|
| Automations | `natural_language_cron.py` + CronCreate + `/loop` ✅ |
| Skills | `~/.hermes/skills/` 34카테고리 ✅ |
| External Memory | wiki vault + episodic/semantic + `01_hot.md` ✅ |
| Sub-agents | `/ship` (Writer/Reviewer/Tester) ✅ |
| Buildroom roles | Research/Dreamer/Main/Coder/QA 모두 기존 모듈에 대응 ✅ |

**미적용 결정 (불필요)**:
- Buildroom JSON 스키마 계약 체인 → 솔로 운영자에게 과도한 ceremony
- `ant` CLI → Python 기반 Hermes가 동일 역할
- 수천 에이전트 swarm → 개발팀용 패턴, MJ 시스템 불필요

**적용 권장 (미실행)**:
- CLAUDE.md 자동 증류 루프 — CronCreate로 세션 내 등록 (영구화 불필요 결정)
- 검증 스킬 트리거 등록 (harness_verifier, curator 등) — 다음 세션 과제

### ✅ 완료 — /ship 병렬 서브에이전트 팀 (2026-06-10)
- `~/.claude/agents/` writer/reviewer/tester 3개 + `/ship` 슬래시 커맨드
- `source ~/.zshrc` 후 즉시 사용 가능
- **사용 조건**: 파일 2개+ 수정, 테스트 필요한 중간 규모 작업에만 사용 (단순 수정은 오버헤드)
- 토큰: 병렬이 순차보다 총량 적음 (각 에이전트 격리 컨텍스트), 단 시간당 한도 소진은 3배 빠름

### ✅ 완료 — Hermes Harness Skill 체계 수립 (2026-06-09)
- `~/.hermes/skills/meta-update/SKILL.md` 생성 — "메타 업데이트해줘" 자연어 트리거
- `wiki/00_Meta/hermes_harness_skill_모음.md` 생성 — 스킬 인덱스 + 모듈 스킬 트리거 미등록 목록
- `CLAUDE.md` 커스텀 스킬 트리거 섹션 추가 — Claude Code에서도 자연어 인식
- 자연어 스킬 라우팅 시스템 설계 → `HERMES3_MASTER_DEVELOPMENT_GUIDE.md` v9.4+ 후보 등록
- **미등록 모듈 스킬**: ingest, harness_verifier, curator, system_monitor 등 — 필요 시 순차 등록

### ✅ 완료 — harness_agent.py 3차 분할 (2026-06-09)
- `modules/command_router.py` (135줄): /confirm, /cancel, 모드전환, @단축어, Logic Engine
- `modules/response_handler.py` (130줄): LLM 파이프라인, SAVE 태그, 응답 전송
- harness_agent.py: 494 → 319줄 (handle_message 35줄 글루로 완성)

### ✅ 완료 — Phase 2 세밀한 메모리 (2026-06-09)
- **신규**: `modules/memory_refinement.py` — 4대 갭 해결 (Forget/충돌감지/self-question/hybrid recall)
- **적용**: `/memory forget`, `/memory health`, harness LLM 컨텍스트 hybrid_recall 자동 주입
- **01_hot.md 갭 분석 4항목 전부 해결**

### ✅ 완료 — Phase 1 낙관적 응답 엔진 (2026-06-09)
- **신규**: `modules/optimistic_response.py` — Linear 아키텍처 즉시 피드백 패턴
- **적용**: `/ingest` 3분기(기본/scan/interrogate) + `/retry` 명령어

### ✅ 완료 — harness_agent.py + skill_evolver.py 책임 분할 (2026-06-09)
- **배경**: `/verify_harness` 진단으로 B등급(60/100) 도출 → 파일 비대화 🔴 문제 지적
- **목표**: 점수 75+ (A등급) 달성
- **완료**:
  - harness_agent.py: 1243줄 → 882줄 (-361줄) ✅
  - skill_evolver.py: 918줄 → 351줄 (-567줄) ✅
  - 신규 3개 모듈: llm_engines.py(267줄), file_ops_agent.py(126줄), skill_curator_ext.py(564줄) ✅
  - `/verify_harness` 명령어에 InlineKeyboard 버튼 추가 (진단 실행/취소) ✅
  - `02_스크립트 정보.md` 업데이트 ✅
- **다음**: `/verify_harness` 재실행 → 점수 개선 확인 (목표 75+)

### ✅ 완료 — AgentForge 4패턴 + 루프 설계 아키텍처 적용 (2026-06-09)

#### 구현 완료
1. **Circuit Breaker** (`harness_agent.py`): 엔진 3회 연속 실패 → 60초 차단. 폴백 체인도 CB 확인
2. **Prompt Injection 방어** (`harness_agent.py` + `modules/tool_result.py`): 외부 도구 출력 샌드박스 태그 감쌈
3. **Context Compaction** (`modules/history_manager.py`): 30턴 초과 시 오래된 대화 자동 요약 압축
4. **ToolResult 구조화** (`modules/tool_result.py` 신규): ok/artifacts/recovery_hint/next_actions 구조

#### 📋 "루프 설계" 트렌드 분석 결론 (Boris Cherny / steipete 2.2M 조회수 논쟁)

**핵심 인사이트**: "프롬프트 치는 사람이 되지 말고 루프를 쓰는 사람이 돼라"
→ Hermes 관점: **이미 루프 시스템. 텔레그램이 루프 인프라, 스킬이 재사용 단위.**

**5단계 사다리 Hermes 매핑**:
| 단계 | 내용 | Hermes 상태 |
|---|---|---|
| Stage 1 | ReAct while-loop (도구→결과→반복) | ✅ `harness_agent.py` 에이전틱 루프 3회 |
| Stage 2 | AutoGPT식 자기 프롬프트 | ✅ `/kanban` + `/handoff` + `/delegate` |
| Stage 3 | ralph loop (고정 앵커 파일 반복) | ✅ `/loop` 명령어 (CronCreate 기반) |
| Stage 4 | /goal (validator 확인 시까지 반복) | ✅ `/caveman` 계획→실행 모드 |
| Stage 5 | 루프가 루프를 감독 (멀티루프 오케스트레이션) | ⚠️ `/orchestrate` 병렬은 있으나 **루프-인-루프 스케줄링 미구현** |

**비용 관리 3대 가드레일** (모든 루프에 적용 권장):
- `max_iterations`: 루프 최대 반복 수 — 에이전틱 루프 `range(3)` 충분
- `no-progress 감지`: `executor.py`의 `detect_stagnation()` 이미 구현
- `토큰/비용 예산`: 미구현 → v9.4 로드맵 후보

**핵심 교훈** — "루프 = 크론 + 루프 본체의 의사결정자. 마법은 루프 안의 **피드백**이다."
→ CoVe + ToolResult + Circuit Breaker = 피드백 품질 향상 체계 완비

**루프 아키텍처 가드레일 — 구현 완료** (2026-06-09):
- ✅ Stage 5: `modules/mayor_agent.py` Mayor 에이전트 구현. `/orchestrate mayor` 대시보드
- ✅ 토큰/비용 예산: `harness_agent.py` 에이전틱 루프 Mayor.tick() 연결, 12,000토큰/루프 기본 예산
- ✅ 루프 자기검증: 에이전틱 루프 break 직전 CoVe `_filesystem_grounding()` 자동 실행

### ✅ 완료 — Qwen2.5-14B-Instruct → Qwen2.5-14B-Instruct-A3B 모델 교체 (2026-06-07 03:39)
- **변경**: 로컬 LLM 모델 교체 (Qwen2.5-14B-Instruct → Qwen2.5-14B-Instruct-A3B UD-Q4_K_M.gguf)
- **config**: custom_providers Gemma→Qwen, context_length 65536, 포트 8080
- **harness_agent.py**: 모든 UI 문자열 Gemma4→Qwen3.6 변경
- **미해결**: WebUI 드롭다운에 Qwen 미표시, Qwen 추론 1분40초+ 타임아웃
- **상세**: 장애 기록 #020 참조

### ✅ 완료 — Gemma4 internal token fallback 및 컨텍스트 환각 해결 (#021, #022) + Qwen→Gemma4 복귀 (2026-06-07)
- **문제**: Qwen→Gemma4 모델 복귀 후 Gemma4 모드가 항상 DeepSeek으로 fallback
- **원인**: `_call_local()` 함수가 Qwen3.6 기준 `<start_of_turn>` 포맷 사용. Gemma4가 이해하나 응답에 `<|channel>` internal token 포함되어 fallback 발동
- **조치**: `_call_local()`에 Gemma4 internal token 제거 로직(re.sub) 추가. 모든 "Qwen3.6" 문자열 "Gemma4"로 복원 (8곳). llama-server gemma-4-26B 재기동
- **상세**: 장애 기록 #021 참조, `qwen-gemma4-switch` 스킬 등록

### ✅ 완료 — Llama-Server 멀티 슬롯 컨텍스트 불일치 및 망각 장애 해결 (2026-06-05)
- **원인**: `com.bluesea.llama_server2.plist`가 `-np 2`로 기동되어 65,536 컨텍스트를 슬롯당 32,768로 분할. Hermes 설정(`context_length: 65536`)에 맞춰 32k가 넘는 긴 컨텍스트를 보냈을 때 Llama 서버단에서 앞부분이 예고 없이 잘려 나감. SWA 캐시 충돌로 속도도 저하됨.
- **조치**: Plist의 `-np 2` 설정을 `-np 1`로 변경하여 단일 슬롯에 65,536 컨텍스트를 온전히 할당하고 서버 재시작 완료.

### ✅ 완료 — 에이전트 세션 초기화 프로토콜(Initialization Protocol) 규정 (2026-06-04)
- **문제**: WebUI 재시작 시 에이전트가 백지 상태로 타임스탬프/태그 등 헌법 규칙을 무시하고 파일 생성.
- **조치**: `USER.md` 및 `06_에이전트_오류_및_재발방지_보고서.md`에 모든 에이전트가 첫 턴에 `constitution.local.md`와 `01_hot.md`를 필수 스캔하도록 초기화 프로토콜 신설.

### ✅ 완료 — 세션 워크스페이스 망각 장애 해결 및 다중 경로 바인딩 적용 (2026-06-04)
- **문제**: 세션 컴팩션 시 워크스페이스 경로(`Mjobsidian`) 밖의 임시 외부 프로젝트(`MarineOS-XR Project`)를 스캔하지 않고 파일이 지워졌다고 허위 추측 답변을 하는 장애 발생.
- **조치 1**: 중복 생성된 `Script/` 디렉토리 삭제 및 `MarineOS-XR Project` 내 레이어별 코드 물리적 대조/검증 완료.
- **조치 2**: `constitution.local.md`에 §X.2(물리적 실재 확인 의무화) 및 §X.4(다중 작업 경로 바인딩) 추가.
- **조치 3**: `01_hot.md`에 활성 외부 프로젝트 경로 등록. `06_에이전트_오류_및_재발방지_보고서.md` 발행 완료.

### ✅ 완료 — 태그 자동화(최대 8개) 확장 및 하네스 컨트롤 가이드 작성 (2026-06-03)
- **요약**: `wiki_auto_stamper.py`를 확장하여 실시간 저장 시 태그 8개 자동 조율 및 [[링크]] 텍스트화 적용. 하네스 컨트롤(harness, hdod, hstatus, hrollback)의 상세 분석 가이드 생성 및 깨진 링크 정리.
- **연관 파일**: `wiki_auto_stamper.py`, `하네스_컨트롤_가이드.md`, `00_Meta_지도.md`, `INDEX.md`

### ❌ 진행 중 — HERMES3_ENCYCLOPEDIA.md write_file 덮어쓰기 사고 (2026-06-03)
- **문제**: AI가 write_file로 기존 파일 수정 시도 → 전체 파일이 77줄로 덮어써짐 (원본 1108줄)
- **원인**: 기존 파일 수정에 patch 대신 write_file 사용. 가장 중요한 안전 규칙 위반.
- **영향**: HERMES3_ENCYCLOPEDIA.md의 원본 778-1108줄 내용 소실 (Graphify 섹션, SQLite WAL, 나머지 섹션)
- **조치**: constitution.local.md에 write_file 사용 전 read_file 의무화 규칙 추가 예정
- **교훈**: CRITICAL — 기존 파일 수정은 write_file 금지, patch만 사용. 본 사고를 재발 방지 교훈으로 memory 등록 완료.

### ✅ 완료 — Ingest TagLinker vault_path 오류 수정 (2026-06-03)
- **문제**: `ingest_engine.py:20`에서 `TagLinker(vault_path=str(vault_path))` 호출 → `tag_linker.py`의 `__init__`는 `db_path` 파라미터만 받아서 TypeError
- **수정**: `TagLinker(vault_path=...)` → `TagLinker()` (인자 없음, 기본 DB_PATH 사용). vault_path 변수 완전 제거.
- **결과**: Ingest 정상 동작 확인 — 11 Clippings + 7 root files + 1 Inbox deferral 처리됨
- **연관 파일**: `modules/ingest_engine.py`

### ✅ 완료 — PKM_2 Knowledge Mesh 구현 완료 (2026-06-03)

**Private Knowledge Mesh 2차 설계 전면 구현** — 연구 시간 90% 단축 목표.

| 모듈 | 파일 | 내용 |
|------|------|------|
| 🧠 중앙 제어기 | `modules/knowledge_mesh_orchestrator.py` | JSON 레시피 기반 파이프라인 오케스트레이터 — web_search_multi(arXiv/Semantic Scholar), local_semantic_search, merge_timeline, cross_reference, summarize_insights |
| 📅 타임라인 | `modules/timeline_builder.py` | 단일/다중 소스 타임라인 병합, 날짜 파싱, 중복 제거 |
| 🔗 교차 분석 | `modules/cross_reference_analyzer.py` | TF-IDF 코사인 유사도 기반 노트↔웹 페이퍼 교차 분석, 시간 감쇠 가중치, predict-and-realize 탐지 |
| 🏷 주제 분류 | `modules/auto_topic_manager.py` | 템플릿 기반 주제 분류, 신뢰도 점수, 새 주제 후보 탐지, 키워드 매칭 |
| 🔍 인덱서 확장 | `modules/knowledge_indexer.py` | `search_similar()` 메서드 추가 — 구조화된 dict 리스트 반환 (Orchestrator 통합용) |
| 📓 번들 확장 | `modules/paper_bundle_manager.py` | `get_bundle_papers()`에 `formal_date` 필드 지원 |
| 🤖 핸들러 | `handlers/_research.py` | `cmd_research` 전면 재작성 — `/research`, `/research local/tl/xref`, `/research topics/classify/classifyall/recluster/stats` |
| **결과** | pytest | **69/69 ✅ 전부 통과** (신규 모듈 4개 import 포함) |

**특징**: LanceDB 불필요 — 기존 TF-IDF 벡터 검색 확장. arXiv API + Semantic Scholar API 동시 검색. JSON 레시피(coffee recipe) 방식 파이프라인 구성.

**약 250~300줄 순수 신규 코드** (4개 모듈) + 기존 파일 3개 소폭 수정.

## 📠 실시간 상태 (KV — /status 명령어로 설정)

## 📌 현재 진행 중인 작업

### ✅ 완료 — constitution.local.md §X 지시 과잉 행위 금지 규칙 추가 + 메타 7종 업데이트 (2026-06-03)

**constitution.local.md에 지시 과잉 행위 금지 규칙 추가**:
- §X.1 기본 원칙: 허가 없는 파일 생성 금지, 선제적 판단 금지, 직전 패턴 무비판적 재사용 금지
- §X.2 실행 규칙: search_files/read_file 사전 확인 의무, 목표와 수단 구분 의무
- §X.3 위반 시: 즉시 보고·삭제·원래 지시 재확인·원인 기록
- constitution.local.md 버전 1.4 → 1.5

**관련 7종 메타 파일 업데이트 완료**:
- constitution.local.md (변경 이력 + §X 본문)
- 01_hot.md (핫토픽 업데이트)
- 02_스크립트 정보.md (변경 이력)
- 03_시스템 인벤토리.md (변경 이력)
- 04_주요 시스템 가이드 및 FAQ.md (Changelog)
- 05_시스템 상태.md (작업 이력)
- 00_Meta_지도.md (최종 업데이트)

### ✅ 완료 — config.yaml display 설정 최적화 (2026-06-03)

### ✅ 완료 — config.yaml toolsets 전체 추가 (2026-06-06)
### ✅ 완료 — memory_engine 디렉터리 및 빈 consolidator_state.json 파일 생성 (2026-06-06)
- `~/.hermes/config.yaml` 와 `~/Applications/venu/.hermes2/config.yaml` 에 모든 toolsets 를 포함하도록 업데이트했습니다.
- 적용된 toolsets 목록: hermes-cli, terminal, browser, web, search, file, vision, delegate, cronjob, computer_use, discord, discord_admin, feishu_doc, feishu_drive, homeassistant, image_gen, kanban, session_search, skills, spotify, todo, tts, video, video_gen, x_search, yuanbao.
- 이후 두 Hermes 인스턴스 모두 전체 도구 사용이 가능해졌습니다.

**config.yaml display 섹션 언어/마크다운 설정 변경**:
- `language: en → ko` — 한국어 사용자 환경에 최적화
- `final_response_markdown: strip → keep` — WebUI 마크다운 렌더링 활성화

| 항목 | 변경 전 | 변경 후 |
|------|--------|--------|
| display.language | en | ko |
| display.final_response_markdown | strip | keep |

### ✅ 완료 — Hermes 2 대화 맥락 단절 및 폴더 오염 진단/수정 (2026-06-02)

**Hermes 2 대화 맥락 단절 원인 및 수정**:
- **문제**: WebUI 사용 중 대화 맥락 단절, "Session compressed N times" 반복.
- **원인 1**: `llama-server -np 2` 병렬 처리 시 Gemma 4 SWA 캐시 무효화. → `~/.hermes/start_llama.sh`를 `-np 1`, `--cache-reuse 256`으로 수정.
- **원인 2**: `compressor` 엔진 조기 압축 및 손실. → `.hermes2/config.yaml`의 `engine`을 `truncation`으로 변경, `threshold` 0.85 상향.

**Hermes 1 vs Hermes 2 경로 격리 재확인**:
- **문제**: 환경변수 누락 시 시스템 및 AI가 `~/.hermes`를 잘못 참조하는 혼선 발생.
- **결론**: Hermes 1(`hermes_local.py`)은 설계대로 `~/.hermes` 전용 사용 유지. Hermes 2(Gateway/WebUI)는 `.hermes2` 전용으로 독립 유지. 두 시스템의 폴더 혼용 불가 원칙 재확인.
- **스킬**: `.hermes2/skills/devops/llama-context-fix/SKILL.md` 스킬 파일 등록 완료.

### ✅ 완료 — v9.2 SIA 피드백 학습 + 모니터링 엔진 + 멀티 모델 로드 밸런싱 (2026-06-01)

**v9.2 업그레이드**: SelfImprovingAgent(SIA) 피드백 학습 → MonitoringEngine 모니터링 → ModelLoadBalancer 멀티 모델 로드 밸런싱 3축 구현.

| 항목 | 파일 | 내용 |
|------|------|------|
| 🤖 SIA | `modules/sia_engine.py` | `SelfImprovingAgent` 클래스 — `record_feedback()` 평점/맥락 저장, `analyze_trends()` 저성능 식별, `suggest_improvements()` LLM 개선 제안 |
| 📊 모니터링 | `modules/monitoring_engine.py` | `MonitoringEngine` 클래스 — `record_metric()` 액션/지연시간/성공 기록, `get_error_rate()`/`get_performance_trend()` 추세 분석, `alert_if_degradation()` 임계 경보 |
| ⚖️ 로드밸런서 | `modules/load_balancer.py` | `ModelLoadBalancer` 클래스 — `select_best_model()` 성능 기반 weighted 라우팅, `rebalance_weights()` 주기적 가중치 재조정, 히스토리/에러 추적 |
| 🔗 통합 | `modules/core_reducer.py` | `HermesCoreReducer`에 SIA/Monitoring 통합 — `apply_user_feedback()`, `on_feedback_collected()` |
| 🔗 통합 | `hybrid_router.py` | `route()`/`call_deepseek()`에 로드밸런서 연동 — `select_best_model()` + `record_model_performance()` |
| ✅ 테스트 | 3개 테스트 파일 | `test_sia_engine.py` (12개) + `test_monitoring_engine.py` (12개) + `test_load_balancer.py` (10개) = **34/34 ✅** |
| **결과** | 전체 pytest | **150/150 ✅ 전면 통과** — 기존 116 + 신규 34 |
| **스킬** | — | v9.2 통합 내용은 `adr-management` 스킬 ADR 템플릿 참조

### ✅ 완료 — PDF→MD 파이프라인 (2026-06-01)

**PDF 파일을 Obsidian에 ingest 가능**: `ingest_engine.py`에 `_read_file_content()` 메서드 추가. PDF는 PyMuPDF(fitz)로 텍스트 추출, 나머지는 일반 텍스트 읽기. Clippings/ + 루트 파일 모두 `.pdf` 지원.

| 항목 | 내용 |
|------|------|
| 도구 | PyMuPDF (fitz) v1.27.2.3 |
| 변경 파일 | `ingest_engine.py` — `_read_file_content()` 신규, `_process_clippings()` + `_process_root_files()` 확장자 분기 |
| 동작 | `/ingest` 실행 시 `.pdf` → 텍스트 추출 → LLM 분류 → `.md` 저장 → Archive 이동 |
| 제약 | 이미지/테이블 추출은 불가 (순수 텍스트만). 표/그래프는 원본 PDF 참조 필요 |
| 검색 | 변환된 `.md`는 FTS5 검색(`/reduce wiki`) 가능 |
| 관계 | NotebookLM MCP(연구 세션용)와는 보완 관계 — 영구 저장+검색 인프라

### ✅ 완료 — /restart_bot 버그 수정 + /run 제거 (2026-05-31)

**버그**: 다른 AI가 추가한 `cmd_restart_bot`이 `handlers/__init__.py`에 import되지 않아 `/restart_bot` 명령어가 Telegram에서 동작 안 함. `@bot.run`은 제한적 화이트리스트 기반이라 사용자 요구사항(임의 터미널 명령 실행)에 부적합.

**수정**:
1. `handlers/__init__.py` — `cmd_restart_bot` import 추가 → Telegram에서 `/restart_bot` 직접 봇 재시작 가능
2. `handlers/_system.py` — `cmd_run_cmd` + `ALLOWED_CMDS` 화이트리스트 제거
3. `hermes_local.py` — `/run` CommandHandler 등록 제거
4. 봇 재시작 완료 (PID 88333)
5. **사용**: `⚠️ /run` 대신 `⚙️ /exec [명령어]` 사용 — AI 자율 에러 복구형 Bash 실행

### ✅ 완료 — 구조적 결함 3종 수정 + 재발 방지 인프라 (2026-05-27)

**문제 1 — Zombie Poller (Hermes1 봇 7분 주기 좀비화)**:
- **증상**: 봇 프로세스는 살아있지만 (PID 존재, 메모리 점유) Telegram API 연결 0개, CPU 0%. 7분마다 launchd가 재시작해도 동일 패턴 반복. 3회 재현 확인 (PID 31208→32176→32956).
- **근본 원인**: PTB v22.5 `app.run_polling()`이 내부에서 `loop.run_forever()` 호출 → polling coroutine이 409 Conflict 등으로 죽어도 이벤트 루프가 계속 실행되며 프로세스가 좀비로 생존. launchd가 감지 못함 (exit code 발생 안 함).
- **수정**: `app.run_polling()` → 직접 `updater.running` 모니터링 + `sys.exit(0)` → launchd KeepAlive 재시작 (5초 ThrottleInterval). asyncio 예외 핸들러 등록. logging 레벨 ERROR 격상.
- **연관 파일**: `hermes_local.py` (run_polling 대체 + watchdog 60s + asyncio handler), `harness_agent.py` (auto_heal_loop bare except → 로깅), `com.hermes.bot.plist` (PYTHONUNBUFFERED + `-u` + ThrottleInterval=5)

**문제 2 — 에러 침묵 구조 (3중 차단)**:
- **증상**: 봇이 죽는데 로그가 전혀 없음. asyncio Task Exception, httpx 타임아웃, polling 실패 모두 silent.
- **근본 원인**: (가) `logging.getLogger("asyncio").setLevel(logging.WARNING)` — "Task was destroyed" 같은 fatal 로그 차단 (나) `_auto_heal_loop()`의 bare `except Exception: pass` — 5분마다 실행되는데 모든 오류 침묵 (다) `com.hermes.bot.plist`에 PYTHONUNBUFFERED 없음 → stderr block-buffered (8KB) → crash 로그가 파일에 안 써짐.
- **수정**: asyncio 로거 ERROR 격상, bare except→로깅 교체, plist PYTHONUNBUFFERED=1 + `-u` 플래그, asyncio 예외 핸들러(traceback 포함) 등록.
- **연관 파일**: `hermes_local.py` (asyncio handler + logging 레벨 + auto_heal 로깅), `com.hermes.bot.plist` (PYTHONUNBUFFERED)

**문제 3 — Gemma4 GGUF Chat Template 버그**:
- **증상**: Gemma4 모드에서 ingest/ask 등 모든 LLM 호출이 빈 문자열 반환. 사용자 모드(Gemma4)가 선택되어 있어도 실질적으로 항상 DeepSeek 폴백.
- **근본 원인**: `llama-server`가 GGUF 내장 Jinja chat template으로 메시지 포맷 시 `chat.completions.create()`가 항상 빈 문자열(`""`) 반환. 모델 파일 자체의 메타데이터 결함. `completions.create()`(raw prompt)는 정상 동작.
- **수정**: `_call_local()` 함수 전면 교체. `chat.completions.create()` → `completions.create()` + 수동 `<start_of_turn>user/model<end_of_turn>` 포맷. stop 토큰 `<end_of_turn>` 설정.
- **연관 파일**: `harness_agent.py` (_call_local 함수 완전 교체)

**스킬 반영**: `systematic-debugging` → `references/hermes-bot-silent-running.md` (7단계 fix 패키지 + Gemma4 template 우회 포함)

### ✅ 완료 — 메모리_파일_명세서 원복 + memory.md 아카이브 정리 (2026-05-27)

1. **메모리_파일_명세서.md 99_Archive→00_Meta 원복**: 사용자 지시로 메모리_파일_명세서.md는 살리고 memory.md만 archive 보냄.
2. **상단 아카이브 배너→참고 문구 변경**: `[!WARNING]` 배너 대신 memory.md만 archive된 참고 문구로 교체.
3. **memory.md 참조 10곳 취소선 유지**: 메모리_파일_명세서 내 memory.md 관련 참조는 그대로 취소선 처리.
4. **00_Meta_지도.md 취소선 해제**: 메모리_파일_명세서 줄 취소선 제거 + archive 주석 → 현역 표기.
5. **시스템 상태.md 원복 이력 추가**: 변경 이력 행 + 푸터 갱신.
6. **memory.md 파일**: wiki/99_Archive/ 유지 (아카이브 배너 정적 보존).

### ✅ 완료 — [Group 2] Vault 진단 + Grill (2026-05-28)

1. **`/vault check`** — `_vault.py` 신규. 3축 진단: 캐시/찌꺼기 파일(DS_Store), 프론트매터, 중복(TF-IDF, vault_scanner 연동).
2. **`🔍 보관함 진단` 버튼** — 하단 키보드 추가 (ℹ️ 도움말 대체). `_base.py` 버튼 매핑 완료.
3. **`/grill [문서] [질문]`** — `_grill.py` 신규. Vault 문서 → LLM Q&A. FUZZY 검색 4단계, 15K자 청킹.
4. **vault_scanner.py 타임스탬프 동적화** — 하드코딩 → `datetime.now()`.
5. **handlers/ 9개 서브모듈** (`_vault`, `_grill` 추가).

### ✅ 완료 — [Group 1] 4개 구현 (2026-05-28)

1. **`/status KEY=VALUE`** — `cmd_status`에 KEY=VALUE 파싱 + hot.md KV 섹션 즉시 쓰기. `reset` 키워드로 초기화. 핫키-값 순간 저장.
2. **시스템 상태.md 이유 컬럼** — 변경 이력 테이블 5→6컬럼. 결정 맥락 추적성 향상.
3. **`/paper review`** — 문서/텍스트 → 구조·논증·선행연구·용어·인용·개선 6축 학술 검토. ⭐별점 보고서.
4. **ADR 템플릿** — `docs/adr/ADR-0000-template.md` 생성. 배경/결정/이유/대안/영향 구조적 의사결정 기록 인프라.

### ✅ 완료 — /ingest v2.1 루트 파일 LLM 분류 이동 (2026-05-27)
- **루트 방치 파일 → LLM 분류 이동**: 26개 .md 파일 전량 처리. 10_AI_Automation(21개), 20_Research(4개), 30_Journal(1개), Unsorted(1개)
- **`_process_root_files()` 전면 재작성**: LLM(DeepSeek) 분류 → frontmatter(category 태그) 업데이트 → 4개 폴더로 이동
- **`_build_tag_prompt` 제거**: dead code 정리. `_build_classify_prompt`(one-shot 예시 + 엄격 JSON)로 통일
- **`cmd_ingest()` — `_call_llm` 연결**: IngestEngine(source_dir, dest_dir, llm_func=_call_llm) 호출
- **버그 수정**: frontmatter 업데이트 후 `write_text()` 누락 → `f.write_text(updated_text)` → `shutil.move` 순서로 수정
- **태그 기반 전환 유지**: 링크 ❌, `[[위키 링크]]` 미생성. tags=[scanned, 카테고리]로 분류
- **관련**: [[스크립트 정보]], [[시스템 상태]], [[주요 시스템 가이드 및 FAQ]], [[시스템 인벤토리]]

### ✅ 완료 — Python 3.10 호환성 문제 해결 (2026-05-27)
- **문제**: `dialectic_layer/_dreamer.py` (line 202)와 `hermes_context_builder.py` (line 43)에서 `str | None` (PEP 604) 문법 사용 → macOS 기본 Python 3.9.6에서 SyntaxError 발생
- **해결**: 두 파일 상단에 `from __future__ import annotations` 한 줄씩 추가
- **결과**: handlers/ 9개 서브모듈 전부 Python 3.9.6에서 import 성공
- **관련**: [[시스템 상태]], [[주요 시스템 가이드 및 FAQ]], [[시스템 인벤토리]]

### ✅ 완료 — 테스트 인프라 구축 (2026-05-27)
- **pytest 8.4.2** 설치 완료 (base Python3)
- **tests/ 디렉토리**: `~/Applications/Mjauto/Scripts/tests/` 생성
- **6개 테스트 파일**:
  - `test_imports.py` — 32개 modules/ + 9개 handlers/ 모듈 import 검증
  - `test_bio_memory.py` — BioMemoryEngine.pre_query_context 5개 smoke
  - `test_skill_evolver.py` — _validate_skill 9개 smoke
  - `test_kanban_manager.py` — KanbanDB 10개 smoke
  - `test_hybrid_router.py` — HybridRouter.is_sensitive 9개 smoke
- **결과**: **87 passed, 0 skipped, 0 failed** (0.48s)
- **참고**: 기존 handler import skip 조건 제거 (Python 3.10 버전 체크 삭제)
- **관련**: [[스크립트 정보]], [[시스템 인벤토리]], [[시스템 상태]]

### 📌 style_profile 읽기 길이 — 1000자 유지 확정
- dream_scheduler.py Phase 3: style_profile.md(4447 bytes) `[:1000]`로 truncation
- MJ님 승인 완료 — 300자는 너무 짧고 Gemma4 컨텍스트도 충분

### ✅ 완료 — Hermes v8.1 Self-Healing Loop + Live Sync (2026-05-28)

1. **Self-Healing Loop (`dream_scheduler.py` v1.0)**: 4-phase ExecPlan (진단→수정→검증→보고). 매일 새벽 3시 cron 등록.
2. **Live Sync (`fswatch_daemon.py` + `update_index.py`)**: 5개 핵심 디렉터리 실시간 감시 → `hermes_index.db` 3초 내 갱신.
3. **pytest 89/89 전부 통과**: conftest mock 보강, handlers 9개 (+_vault, +_grill) 전부 통과.
4. **메타 5종 현행화**: 00_Meta_지도, 스크립트 정보, 시스템 상태, 시스템 인벤토리, 주요 시스템 가이드 및 FAQ 전부 v8.1 기준 업데이트.

### ✅ 완료 — `/reduce` 보안 감사 + 3계층 방어 체계 (2026-06-01)

**범위**: `_approval.py` `cmd_tag_logic` + `core_reducer.py` `_execute_exec`/`_execute_file` + 캐싱 최적화

**변경 요약** (3개 파일):
| 계층 | 파일 | 내용 |
|------|------|------|
| 🔒 태그 보안 | `handlers/_approval.py` | `cmd_tag_logic` — `shlex.quote()` escape, action 키워드 화이트리스트, 한글 경로 검증 |
| 🔒 실행 보안 | `modules/core_reducer.py` | `_execute_exec` — 14개 위험 명령어 블록리스트(`rm -rf /`, `mkfs`, `dd if=`, `fdisk`, `shutdown`, fork bomb, wget\|curl 파이프 등). 한글 쿼리 차단. 30초 타임아웃 |
| 🔒 파일 읽기 | `modules/core_reducer.py` | `_execute_file` 신규 — 허용 경로 `/Users/bluesea/Applications/` 제한, symlink `os.path.realpath` 검증, `/` 시작/`.` 시작 파일 차단, 100MB 제한, 50KB 출력 제한 |
| ⚡ 캐싱 | `modules/core_reducer.py` | 메모리 캐시 레이어 추가 (Dict, 최대 128개, 60s TTL) — Context Hash로 1차 조회, SQLite 폴백 |
| ✅ 테스트 | `tests/test_core_reducer.py` | `test_hermes_core_reducer_pipeline` 격리 DB(`tempfile.mktemp`) 사용으로 캐시 오염 방지 |
| 📄 문서 | `v9_0_완성_요약.md` | v9.0 개요/액션 현황/v9.1 계획 정리 (스크립트 디렉터리 위치) |
|| **결과** | 전체 pytest | **114/114 ✅ 전부 통과** |
||| **v9.1 완료** | 전체 파이프라인 | **Priority 1-3 전부 완료**: tag 한글/액션 검증(_approval.py), exec 14개 위험명령어+한글+30s 차단, file 화이트리스트+symlink+100MB 제한, 메모리LRU+SQLite 이중 캐싱, 128개 LRU eviction |
||- Hermes1/Hermes2 Telegram Token 분리 (#002)
|- #006/#007 경고 정리 (운영 안정화)

### ✅ 완료 — Ingest Unsorted 경고 알림 + Graphify Vault 그래프 분석 (2026-06-02)

| 항목 | 파일 | 내용 |
|------|------|------|
| ⚠️ Unsorted 경고 | `handlers/_file.py` | `/ingest` 3개 경로(기본/scan/interrogate) 실행 시 Unsorted 비율 30% 초과 시 Telegram 경고 메시지 표시 |
| 🕸️ Graphify 그래프 | `handlers/_vault.py` | `/vault graph` 명령어 — graphifyy(v0.8.28) 패키지 연동, 문서 간 연결 추출 → NetworkX 방향 그래프 → 허브 노드/고립 문서/놀라운 연결 분석 리포트 |
| 📚 ENCYCLOPEDIA.md | Graphify 항목 신설 | 한 줄 요약, 파이프라인 다이어그램, 특징, 의존성 상세 기록 |
| 📋 GUIDE.md | 항목 ✅ 마킹 | 해야할일 표에서 Graphify LOW → ✅ 완료 (2026-06-02) 전환 |

**참고**: `parallel=False` 필수 (Hermes Agent Python 3.11 spawn spawn 제한 우회)

| 항목 | 파일 | 내용 |
|------|------|------|
| 🔐 PermissionBridge | `modules/permission_bridge.py` | 2-tier 도구 권한 게이트웨이 — Internal(자동 승인) vs External(Tier 2, 승인 필요) |
| 🔗 통합 | `harness_agent.py` | RUN_CMD/SAVE/파일작업(DELETE/MOVE/COPY/RENAME) — 모두 PermissionBridge 승인 경유 |
| 🔗 콜백 | `handlers/_base.py` | `perm_approve:` 인라인 키보드 콜백 라우팅 추가 |
| 📥 Inbox Deferral | `ingest_engine.py` | 저신뢰(Unsorted)/파싱 실패 시 Inbox/`*_pending.md` deferral, `_process_inbox()` 재분류 라운드 |
| 📚 ENCYCLOPEDIA.md | 2개 항목 추가 | PermissionBridge + Save vs Organize & Inbox Deferral |
| 📋 GUIDE.md | 9.2 해야할일 | 미완료 항목 7개 Priority 표 등록 (HERMES.md 템플릿/AutoVault/인터랙티브 등)

---

🔗 **관련 문서**
- [[00_Meta_지도]] — 메타 폴더 내비게이션
- [[시스템 상태]] — 전체 변경 이력
- [[스크립트 정보]] — 모듈 및 명령어 가이드
- [[주요 시스템 가이드 및 FAQ]] — 문제 해결 및 Changelog
- [[시스템 인벤토리]] — 설치 환경 정보
- [2026-06-03] 메모리 누락 명령어(/memory) 복구 및 Dreaming v2 PEMS 엔진 고착화(수렴 버그) 수정 완료. (offline_consolidation 흐름 정상화)
gemma4 launchctl unload ~/Library/LaunchAgents/com.bluesea.llama_server2.plist
        launchctl load ~/Library/LaunchAgents/com.bluesea.llama_server2.plist
---

## 2026-06-05 Bio-Memory Engine v9.3 개선 — 3파일 구조 개선 완료

- ✅ **bio_memory_engine.py**: `_get_l2_bytes()` 메서드 추가(402-405행), `get_memory_status()`에 KB/MB 실시간 표시
- ✅ **dreamer_layer.py**: `offline_consolidation_forced()` 메서드 추가(270-296행) — 중요도 하위 50% 강제 L3 전이 (1MB 초과 시 자동 발동)
- ✅ **dreaming_v2.py**: `_run_offline_consolidation()`에 용량 위기 시 강제 증류 호출(124-128행) + `_commit_to_l3_semantic()` atomic write 적용(230-274행)
- ✅ **import 검증**: 3개 파일 전부 Python import 정상 확인
- **연관**: [[03_시스템 인벤토리]], [[05_시스템 상태]], [[04_주요 시스템 가이드 및 FAQ]], [[00_Meta_지도]], [[06_에이전트_오류_및_재발방지_보고서]], [[constitution.local]]

## 2026-06-03 작업 완료 목록

- ✅ `/claude_brief` 핸들러 추가 — `handlers/_meta.py` 신규, 6대 메타 문서 → claude_briefing.md 브리핑 생성
- ✅ Dreaming V2 PEMS 고착화 버그 수정 (`offline_consolidation` 항상 실행)
- ✅ Hermes 봇 재시작 (pkill → launchd 자동 재시작)
- ✅ HELP_TEXT 완전판 업데이트 (33개 명령어)
- ✅ wiki 전체 59개 파일 타임스탬프 일괄 복구
- ✅ `constitution.md` §9 타임스탬프 의무 갱신 규칙 신설
- ✅ `wiki_auto_stamper.py` 기능 확장 (태그 최대 8개 병합, [[링크]] 텍스트화 및 긍정형 전방탐색 파싱)
- ✅ `지식 베이스 사용 가이드.md` 링크 정리 (00_Meta_지도.md, INDEX.md 깨진 링크 제거)
- ✅ `하네스_컨트롤_가이드.md` 상세 분석서 작성 및 메타폴더 하부 저장
- ✅ `Bio_Memory_Engine_가이드.md` 전면 현행화
- ✅ `규칙_통합_결과보고서.md` Rule 6 추가
- ✅ 7종 메타 문서 동시 업데이트

### ✅ 완료 — WebUI 멀티모델 통합 + NIM→GPT OSS 120B 마이그레이션 (2026-06-07)
- **WebUI 3종 모델 통합**: Qwen-14B / GPT OSS 120B / Minimax M2.7 WebUI 드롭다운 및 라우팅 완전 동작
- **Root Cause 5계층**: `_whitelist_keywords` 누락 → `@custom:` prefix 미제거 → context_length TypeError → 디스크 캐시 → skills 스냅샷 캐시
- **핵심 패치**: `api/config.py` whitelist 확장, `api_server.py` prefix strip + context_length pop, `run.py` provider 해석
- **NIM 70B → GPT OSS 120B**: `harness_agent.py` + `llm_mode.txt` 마이그레이션 완료 (`openai/gpt-oss-120b`)
- **Skills 115개 비활성화**: `disabled_toolsets: [browser, vision]` + `skills.disabled` 115개 → Qwen 첫 응답 120s→77s
- **M4/36GB 스펙 확정**: M4 Mac Studio 36GB RAM (이전 문서의 M2 Max/Ultra 오기 정정 완료)
- **신규 문서**: `HERMES_HOME 과 환경 변수의 진짜 물리적 지도 (Fact Check) 20260607.md`, `WebUI_멀티모델_통합_장기화_원인분석_20260607.md`
- **상세**: 장애 기록 #024 참조

### ✅ 완료 — cove_engine.py Scripts/로 이전 + 참조 정리 (2026-06-07)
- **작업**: `cove_engine.py`를 `~/.hermes/governance/skills/brain/cognitive/scripts/` → `Scripts/cove_engine.py`로 이동
- **수정 파일**:
  - `Scripts/cove_engine.py` (신규 복사): 내부 `sys.path.append` 하드코딩 2줄 제거, `wiki_manager` import를 `modules.wiki_manager`로 상대경로 변경
  - `handlers/_base.py`: import 주석 위치 표기 추가 (코드 수정 없음)
- **영향 범위**: `cove_engine`을 간접 참조하는 7개 handlers 모듈 모두 영향 없음 (모두 `_base.py` 경유)
- **백업**: `Scripts/_archive/cove_engine.py.bak`
- **원본 삭제**: `~/.hermes/governance/.../cove_engine.py` (백업 후 삭제 완료)

## 🔴 현재 미해결 / 모니터링 필요
- ⚠️ `wiki_auto_stamper.py` fswatch 연동 미설정 (수동 실행만 가능)
- ⚠️ `meta_updater.py` 비활성화 상태 유지 중 (필요시 재활성화)


|*최종 업데이트: 2026-06-07 22:00 — WebUI 멀티모델 통합, NIM→GPT OSS 120B, Skills 115개 비활성화, 메타 7종 갱신*

---

## 📋 AI Agent Memory 개념 분석 — 문제 인식 저장 (2026-06-05)

**참조**: 블로그 "AI Agent Memory" 4계층 메모리 스택 + 4대 연산 vs 현재 시스템 비교 분석

### 우리 시스템 대비 블로그 갭 (향후 수정 로드맵 확정 시 반영 예정)

| 항목 | 블로그 제안 | 우리 시스템 현황 | 개선 필요 |
|------|-----------|----------------|----------|
| **Forget 정책 부재** | 명시적 forget/pruning 연산 필요 | ✅ `memory_refinement.auto_forget()` — 보유율 15% 미만 + 7일 경과 자동 정리 | ✅ 해결 |
| **Update 자동 충돌감지** | 쓰기 전 기존 메모리와 충돌 검증 | ✅ `memory_refinement.check_conflict()` — L2/L3 키워드 충돌 검사 | ✅ 해결 |
| **Writer self-question** | "다음 세션에도 쓸모있을까?" 저장 전 자가 질문 | ✅ `memory_refinement.should_store()` — 중요도/일시적 표현/중복 자동 판단 | ✅ 해결 |
| **Retrieval 품질** | 후보 다수 확보→LLM 선택 | ✅ `memory_refinement.hybrid_recall()` — L2+FTS5 병합, harness 자동 주입 | ✅ 해결 |

### 적용 불필요 항목

- 메모리 암호화 (단일 사용자 환경)
- 비동기 write (정보 유실 리스크)
- LLM이 retrieval 후보 직접 선택 (Gemma4 문서 간 추론 약함)

### 현재 시스템 강점 (블로그 대비 우위)

- 4계층 메모리 스택 완비: Context Window→L1(harness_memory.json)→L2(episodic_memory)→L3(semantic_core)
- Write/Read 연산 강함 (memory tool, session_search)
- External Knowledge: web_search, RAG(FTS5+knowledge_indexer), Knowledge Mesh
- checkpoint + session_search + wiki가 Long-Term Memory + External Knowledge 역할 수행 중
- "Store what matters next week" 원칙 이미 이해하고 memory에 규정되어 있음

## 📋 2026-06-06 업데이트 내역: switch_model.sh 생성 — 모델 전환 스크립트
- **신규 스크립트**: `~/Applications/venu/scripts/switch_model.sh` — 모델/프로바이더 전환 자동화
- **심링크**: `/usr/local/bin/switch-model` (터미널에서 바로 실행 가능)
- **사용법**: `switch-model got` → GPT-OSS-120B (NVIDIA) 로 전환 / `switch-model deepseek` → DeepSeek Chat 으로 전환
- **적용 범위**: 두 Hermes Home 모두 적용 (`~/.hermes/config.yaml` + `venu/.hermes2/config.yaml`)
- **특징**: 기존 설정 삭제 안 함. `# [SWITCHED to ...]` 주석으로 전환 상태 표시. 전환 후 `hermes gateway restart` 필요.
- **연관**: [[00_Meta_지도]], [[03_시스템 인벤토리]], [[02_스크립트 정보]]

## 📋 2026-06-06 업데이트 내역: 텔레그램 UX 개선 및 NVIDIA/날씨 오류 패치

### 🛠️ 최근 장애 복구 요약
- 장애 현상: 서브 봇 날씨 API 키 누락, WebUI 단기 기억 오염
- 근본 원인: 환경 변수 누락, `harness_memory.json` 공유
- 조치: `.env`에 `ANTIGRAVITY_NVIDIA_API_KEY` 추가, `harness_memory.json` 삭제, 게이트웨이 재시작
- 결과: Hermes WebUI 정상 작동, 텔레그램 봇 응답 일치

### 📑 마스터 플랜 (추후 작업)
- L1 단기 기억 파일 격리를 위해 `HERMES_HOME` 활용 또는 `harness_memory_webui.json`/`harness_memory_telegram.json` 도입
- `bio_memory_engine.py`와 `deriver_layer.py` 잠금 해제 필요 시 최소 패치 설계
- ~~테스트 스위트 추가~~ → ✅ 2026-06-11 완료: `tests/test_bio_memory.py` 6→19개 확장 + 운영 기억 오염 차단(`_make_engine` 격리). CI 연동은 추후
- ✅ 2026-06-11: 비대화 감시 `check_file_sizes.sh` + `com.hermes.sizewatch` (매주 월 09:00) 가동
- 상세 내용은 `@wiki/00_Meta/HERMES3_MASTER_DEVELOPMENT_GUIDE.md`에 기록 예정
- **NVIDIA NIM 70B 모델명 수정**: `harness_agent.py` 내 `openai/gpt-oss-120b` → `meta/llama3-70b-instruct` 로 수정하여 폴백 오류 해결.
- **실시간 날씨 인터셉터**: `web_agent_module.py`에 네이버 날씨 웹 스크래퍼를 추가하여 DeepSeek/DuckDuckGo 검색 시 동네 날씨(예: 명륜동)가 표출되지 않던 한계 극복.
- **텔레그램 대기 UX 개선**: 무거운 LLM API 호출 시 '🤔 생각 중...'이 멈춰있지 않고 움직이는 비동기 애니메이션 태스크를 `harness_agent.py`에 적용.
- **파일 절단 사고 복구**: 이전 에이전트가 `view_file` 800줄 제한을 모른 채 코드를 작성해 파일이 망가졌던 것을 구조 분석을 통해 완벽히 복구함.

### ✅ 완료 — 논문 기반 하네스 대규모 업그레이드 v9.4 (2026-06-12)

**분석 논문**: 11편 (Model Collapse, SAGE, Code as Harness, ClawTrojan, COLLEAGUE.SKILL, TraceGraph, AdaCoM, MIT Self-Revising, Aging Agents, Bi-Temporal Memory, OpenAI Engineering)

**적용 완료**:
- `bio_memory_engine.py` — Model Collapse 방어 (assistant 점수 상한), 임베딩 인라인 제거 (2.3MB→~150KB), eviction while 수정, source 태깅
- `memory_refinement.py` — SAGE 신선도 게이트 4개 함수 (novelty_score, is_novel_enough, diversity_check, get_diversity_report)
- `context_assembler.py` — ClawTrojan 방어 (_sanitize_wiki_content, 7개 regex 패턴)
- `skill_auditor.py` — SkillLifecycle 클래스 (lifecycle DB, stale 탐지, 보고서)
- `agentic_loop.py` — TraceGraph 궤적 로깅 (_trace, trace_log.jsonl 롤링 200엔트리)

**미적용 후속**:
- AdaCoM context hot/cold 분리 (context_assembler 리팩 필요)
- Governed Harness Mutation (skill_evolver.py 분석 필요)
- Deep Telemetry 파이프라인

**상세 기록**: `wiki/00_Meta/하네스_논문_기반_개선_로그.md`

---

### ✅ 완료 — MJstock 실험 필터 토글 시스템 v1.0 (2026-06-18)

**프로젝트**: `/Users/bluesea/Applications/Mjstock`

**완료 항목**:
- `screener/run_scan.py` — 실험 필터 토글 3개 (`EXP_USE_FRESH_TREND`, `EXP_USE_IS_LEADER`, `EXP_USE_IS_TIGHT`) + `compute_exp_filters()` 함수 신설. US/KR 스캔 양쪽 적용. CSV에 exp_* 컬럼 상시 기록
- `screener/signal_tracker.py` — `_calc_position_size()` ATR 기반 포지션 사이징 추가. `record_scan()` 파라미터 확장 (atr14, suggested_shares, exp_* 3종)
- `app.py` — exp_* 컬럼 감지 시 실험 필터 체크박스 자동 표시. 재스캔 없이 즉시 필터링 + 필터된 종목 수 캡션
- `screener/screen_uryangju_nongsaju.py` — 중복 실험 필터 코드 제거
- `docs/` 4개 문서 업데이트 (signals_entry_points, quant_logic_analysis, korean_original_formulas, MJstock_사용설명서)

**다음 작업 후보**:
- `EXP_USE_*` 토글을 app.py UI에서 직접 제어하는 설정 패널 추가
- `suggested_shares` 컬럼을 차트 탭에 표시

---

### ✅ 완료 — MJstock 퀀트 DB 기초공사 + 자동 축적 시스템 (2026-06-18)

**프로젝트**: `/Users/bluesea/Applications/Mjstock`

**완료 항목**:
- `screener/run_scan.py` — `compute_quant_snapshot()` 신설. 스캔 통과 종목마다 17개 퀀트 컬럼(진입가·ATR·RSI·MACD·BB·EMA이격도·52주고가·거래량비율·미래수익률 자리) 자동 저장. US/KR 공통 적용
- `screener/batch_fill_returns.py` — 신규. 매일 17:30 cron 자동 실행. ret_5d/10d/20d 자동 채움 + `health_check()` 함수로 적재 상태 반환. `results/fill_returns.log` 기록
- `app.py` 탭4 — "최근 결과" → "퀀트 로그" 전면 개편. 검색식별 서브탭 + 요약 지표 + 6종 차트(점수/RSI/거래량비율/EMA이격도/MACD/52주고가) 체크박스 토글 + "데이터 적재 상태 확인" 헬스체크 섹션 + CSV 다운로드
- crontab — 매주 월~금 17:30 `batch_fill_returns.py` 자동 실행 등록 완료
- 유니버스 버튼 레이블 간소화, 슬라이더 눈금, CSV 업데이트 섹션 추가
- score 계산 수정 (항상 0 → bool 조건 컬럼 기반), 차트 탭 순위 번호 추가

**퀀트 DB 이력관리 방향 (확정)**:
- 스캔마다 → `scan_*.csv`에 17개 퀀트 스냅샷 자동 저장
- 매일 17:30 → `batch_fill_returns.py`가 ret_5d/10d/20d 자동 채움
- 퀀트 로그 탭 헬스체크로 적재 누락 즉시 감지
- 데이터 수천 건 쌓이면 → 논문/전략 시뮬레이션으로 진입타이밍 최적화 가능

**다음 작업 후보**:
- `batch_fill_returns.py` 실제 KIS API 연동 테스트 (스캔 5일 후)
- 퀀트 로그 탭에 수익률 분포 차트 추가 (ret_5d/10d/20d 히스토그램)
- 논문 기반 새 지표 시뮬레이션 — MJ가 논문 던져주면 Claude가 백테스트
