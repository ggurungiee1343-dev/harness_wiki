---
tags: []
---
## ⚖️ 최근 감사 결과 (Dreaming)
**[목표 진척도]**
사용자의 기술적 문제(명령어 오류, 메모리 구조화)에 대해 구체적인 해결책과 설계안을 제시함으로써 '유용성' 측면에서 높은 진척도를 보이고 있습니다. 요청된 데이터 구조화 및 관리 설계 작업을 즉각 수행하며 장기 목표를 충실히 이행 중입니다.

**[헌법 준수 감사]**
결론을 먼저 제시하는 역피라미드 구조와 전문 용어를 활용하여 MJ님의 스타일 프로필을 충실히 준수하고 있습니다. 불필요한 수식어나 메타 해설을 지양함으로써 'AI 냄새'를 효과적으로 제거하고 시스템의 핵심 가치인 신뢰성을 유지하고 있습니다.

# 📝 프로젝트 핫토픽

**최종 업데이트: 2026-06-30 19:38*

## 📠 실시간 상태 (KV — /status 명령어로 설정)
- **Active External Project**: `/Users/bluesea/Applications/Mjstock` (자동 스캔 시스템 구축 완료)
- **Current Model (Telegram)**: GPT OSS 120B (기본, NVIDIA API) / DeepSeek API (폴백) / Qwen2.5-14B 로컬 (선택 가능)
- **Current Model (WebUI)**: Qwen2.5-14B (로컬) / GPT OSS 120B (NVIDIA) / Minimax M2.7 (NVIDIA) — 3종 멀티모델 통합 완료
- **Hermes1 PID**: 18639 (2026-06-29 기준)
- **hermes_stock_bot.py PID**: 36986 (2026-06-29 재활성화 — com.hermes.stockbot)
- **llama-server**: 종료 가능 (Telegram GPT OSS 120B 모드 + WebUI 비-Qwen 선택 시 영향 없음)

## 💡 Lessons Learned

> **목적**: 버그가 아니어도, 채팅이 닫히기 전에 기록해야 할 패턴·발견·판단 근거를 실시간으로 쌓는 곳.
> **06번 보고서와 차이**: 06번 = 버그 원인·재발방지(무거운 형식). 여기 = 작업 중 발견한 판단 근거·패턴·비직관적 사실(가벼운 형식).
> **작성 트리거**: "나중에 이걸 왜 이렇게 했지?" 라는 질문이 생길 것 같은 모든 순간.
>
> **정리 정책 (2026-06-23 확정)**: 자동화 없음 — 로직 자체가 관리 부담. **30줄 초과 시 Claude가 세션 시작 시 "Lessons Learned 정리할까요?" 제안.**
> 정리 기준: ① 모든 세션 필수 지식 → CLAUDE.md 승격 후 삭제 ② 06번 보고서에 이미 있는 버그 패턴 → 삭제 ③ 3개월 이상 경과 + 더 이상 관련 없음 → 삭제 ④ 여전히 실수할 것 같은 패턴 → 유지

| 날짜 | 분야 | 교훈 |
|---|---|---|
| 2026-06-30 | 스캔 이중 실행 충돌 | `RC!=0 + stderr 비어있음 + stdout 비어있음` = 조용한 이중 실행 충돌 시그니처. Traceback 없음에 속지 말것. 1차 진단: `pgrep -f auto_scan \| wc -l` (2이상이면 이중 실행). 이전 스캔 완료 전 수동 실행 금지. 06번 SCAN-007 참조. |
| 2026-06-30 | date_str CSV glob 매칭 | `date_str` 형식 `%Y%m%d`는 여러 타임스탬프 충돌 가능 → `%Y%m%d_%H%M%S` 로 변경해야 특정 스캔 시각의 CSV를 정확히 glob 매칭. 형식 변경 시 텔레그램 콜백 파싱쪽(`_handle_mjstock_scan_list`)도 동일 형식 사용하는지 함께 확인. |
| 2026-06-30 | 코인 버튼 레이블 UX | Coin 스캔 결과 버튼 레이블 `(N종)` 만으로는 "클릭하면 무슨 일이 생기는지" 불명확. `검색(N종)` 접미로 동작을 명시하는 것이 모바일 UX 기준. 버튼 레이블은 항상 동사/동작 포함 여부 검토. |
| 2026-06-30 | Streamlit 블로킹 | `while proc.poll() is None: time.sleep(1)` 패턴은 Streamlit 전체를 블로킹 → 스캔 중 탭 전환 불가. `session_state` 기반 polling + `st.rerun()` 패턴으로 교체해야 첫 번째 검색기 완료 직후 차트탭 접근 가능. Streamlit에서 서브프로세스 대기는 항상 비동기 방식. |
| 2026-06-30 | Telegram InlineKeyboard | REST API에서 `reply_markup`을 JSON으로 전달. `mjstock_scan_list:{key}:{ts}` 형식 callback_data로 스캔 결과 → 종목 목록 → 차트 → Back 드릴다운 UX 구현 가능. 버튼 레이블은 `{검색기명}(N종)` 형식이 모바일 가독성 최적. |
| 2026-06-30 | mjstock 콜백 라우팅 | `mjstock_scan_list:` prefix는 `^mjstock[_:]` 패턴에 매칭 → `callback_mjstock()` 자동 라우팅. 신규 `mjstock_*` prefix 추가 시 별도 핸들러 등록 불필요, `callback_mjstock()` 내부 분기만 추가. `mjstock_chart:` 4-part 파싱(ticker/screener_key/date_str)도 동일 라우터에서 처리. |
| 2026-06-30 | macOS 스케줄러 | macOS에서 crontab은 Full Disk Access 제한으로 Claude Code 셸에서 타임아웃 발생 → launchd plist가 macOS 표준 스케줄러 대안. `~/Library/LaunchAgents/` 에 plist 작성 후 `launchctl load` 로 등록. 신규 배치 스크립트 스케줄링은 crontab 대신 launchd plist 사용. |
| 2026-06-30 | Streamlit 차트 인라인 표시 | 차트 외부 열기(`subprocess.Popen(["open", chart_path])`)는 Streamlit UI 내부에 표시되지 않음. `st.components.v1.html(f.read(), height=1200, scrolling=True)` 패턴이 인라인 표시 정답. 외부 앱 열기 방식은 Streamlit 웹 UI에서 사용자 경험 단절 발생. |
| 2026-06-30 | Python SyntaxError 전파 | `signal_tracker.py` `record_scan()`에 `sector_map` 파라미터가 중복 정의되어 SyntaxError → 모듈 import 자체 실패 → 해당 모듈을 쓰는 모든 스캔 결과 전송 불가. 함수 파라미터 추가 후 단독 import 테스트 필수: `python3 -c "import 모듈명"`. 06번 SCAN-006 참조. |
| 2026-06-30 | EMA45 이격도 퀀트 저장 | ema45_dist_pct를 signal_log.csv에 안 넣으면 "몇 % 이격 시 진입했나"를 소급 분석 불가. 삼돌이 핵심 지표(EMA45 돌파)는 퀀트 DB에서 이격도 형태로 반드시 보존. sector도 업종별 승률 분석 필수. 새 검색기 만들 때 핵심 지표는 signal_log.csv 컬럼으로 등록 세트. |
| 2026-06-30 | app.py 차트탭 자동갱신 패턴 | 탭 재진입 시마다 최신 스캔 결과 auto-detect 하려면 `session_state` mtime 비교 패턴 필수. mtime이 바뀌었을 때만 `chart_sel` 업데이트 → 중복 갱신 방지. 스캔 완료 후 탭 전환 UX에 항상 이 패턴 적용. |
| 2026-06-30 | 퀀트 DB 아침/장중 중복 억제 버그 | signal_tracker.record_scan()의 "이미 active" 체크가 scan_type 구분 없이 동작 → 아침 후보로 기록된 종목의 장중 실제 타점이 영구 누락됨. scan_type 컬럼 추가 + 중복체크에 scan_type 반영으로 해결. morning/intraday 별개 행 기록됨. |
| 2026-06-30 | 두 개의 수익률 시스템 | 개별 scan_*.csv → ret_5d/10d/20d (batch_fill_returns.py 담당). signal_log.csv → return_10d/20d/30d (signal_tracker.update_returns() 담당). 두 시스템 별개 운영 중. 분석 시 signal_log.csv 기준으로 통일. 다른 AI가 이 둘을 혼동해 "batch 미실행 추정" 오진단. |
| 2026-06-30 | handlers SRP 분할 | 대형 핸들러 분할 시 `safe_reply`/`safe_edit`를 각 신규 파일에 로컬 정의해야 순환 import 방지. `_base.py` import 시 handlers 패키지 전체가 로드되므로 분리 파일은 독립성 유지 필수. |
| 2026-06-30 | _paper.py dispatch 패턴 | 538줄 단일 함수를 9개 `_handle_*` 서브함수 + dispatch dict 라우터로 분리하면 유지보수성 수직 상승. 새 subcmd 추가 시 함수 1개 + dict 1줄만 추가. |
| 2026-06-30 | 퀀트 DB 수동조회 누락 | `/stock`, `/mjstock` 수동 조회는 signal_tracker에 저장 안 되고 있었음. 자동 스캔만 저장 중이었으므로 `record_manual_lookup()` 신설 필수. 신규 텔레그램 명령어 구현 시 퀀트 DB 저장 여부 항상 체크. |
| 2026-06-30 | Streamlit 차트 높이 제한 패턴 | `height=720` 고정이면 차트 아래 매수/매도 분석 섹션이 잘림. 차트 + 분석 섹션을 함께 보여줄 때는 `height=1200` + `scrolling=True` 세트로 설정. 높이 부족은 사용자가 내용 짤림으로 인지 → 리포트 안 올라옴 → 나중에야 발견 패턴. |
| 2026-06-30 | 배치 채우기 스크립트 crontab 미등록 재발 패턴 | 스크립트 작성 완료 후 crontab 등록을 잊는 패턴 반복. `batch_fill_returns_coin.py` 작성 완료했으나 crontab 미등록. 신규 배치 스크립트 완성 시 반드시 즉시 crontab 등록 확인. (`crontab -l | grep <파일명>` 으로 검증) |
| 2026-06-30 | 코인 수익률 데이터 축적 특성 | 3d/7d 수익률 채움은 신호 발생 후 3일/7일이 실제로 경과해야 의미있는 데이터 생성. 스크립트 실행 즉시 결과가 안 보이는 것이 정상. 데이터 축적 단계에서는 "비어있는 수익률 컬럼" = 아직 경과 안 됨을 의미. 채움 실패와 혼동 금지. |
| 2026-06-30 | MJstock 텔레그램 버튼 | BUG-4에서 버튼→sendDocument로 전환했지만 hermes_stock_bot.py에 `callback_mjstock_results` 핸들러가 등록되어 있으면 버튼 방식이 정상 작동함. gateway 경유 여부가 핵심 — gateway 우회 봇(hermes_stock_bot.py)은 자체 prefix 제한 없음. 버튼 방식 가능 여부는 콜백 핸들러 등록 여부로 판단. |
| 2026-06-30 | MJstock 전송 방식 설계 | 인라인 버튼(요약 메시지 + 버튼) vs sendDocument(HTML 직접 첨부) 선택 기준: 다수 파일 → 버튼(파일폭탄 방지). 단일 결과 → sendDocument도 무방. 2열 버튼 배치(InlineKeyboardButton 2개씩 row)가 모바일 UX 최적. |
| 2026-06-29 | MJstock 아침 스캔 | subprocess TimeoutExpired를 run_screener() 레벨에서 catch 안 하면 main() 전체 종료 → 이후 검색기 전부 미실행. catch 필수. |
| 2026-06-29 | MJstock selyeok 성능 | yfinance 루프 내 개별 호출(500종목×1~3초=1500초) vs group_by="ticker" 배치(1회 10~30초). 검색기 루프에 API 호출 넣기 전 배치 여부 먼저 검토. |
| 2026-06-29 | MJstock 텔레그램 콜백 | `[결과 보기]` 버튼 무응답 = hermes_stock_bot.py 미실행이 단일 원인. mjstock_callback_bot.py는 send-only(설계 의도) — 콜백 수신 역할 아님. 혼동 금지. |
| 2026-06-29 | MJstock 콜백 봇 구조 | 버튼 발송 토큰과 콜백 수신 봇 토큰이 같아야(8740948695) Telegram이 콜백 라우팅. 봇 토큰 다르면 콜백 영구 미수신. |
| 2026-06-29 | MJstock gateway 우회 | gateway 설치 패키지(`venu/venv/lib/.../gateway/platforms/telegram.py`) 수정 불가 — 자체 prefix(mp:/ea:/sc:/cl:)만 처리. `mjstock_results__` prefix 핸들러 없으므로 버튼 콜백 방식 자체가 구조적 불가. 버튼 제거 → HTML `sendDocument` 직접 전송이 유일한 해법. |
| 2026-06-28 | MJcoin signal_tracker_coin 고도화 | score_delta는 직전 스캔 기록 없으면 항상 0 — 첫 실행 정상. ATR 포지션 사이징: stop=ATR×3, 계좌 1% 리스크 기준. star_type/circle_type은 BUY_SIGNALS 리스트 기반 자동 추출 — 리스트 누락 시 빈 칸. |
| 2026-06-28 | MJstock chart.py 분석카드 | `_inject_analysis_card()`는 save 함수 끝에서 HTML에 카드 삽입. 세 save 함수(save_chart/save_farming_chart/save_chowuryang_chart) 모두에 추가해야 일관성 유지. 하나라도 누락 시 해당 검색기 차트에만 카드 미표시. |
| 2026-06-28 | MJcoin signal_tracker | 코인 tracker CSV는 `Coin/tracker/signal_log.csv`. `batch_fill_returns_coin.py`가 루트만 탐색하는 버그 → `_collect_csv_files()` 재귀 탐색으로 수정. 서브폴더 samdoli/uryangju 등 모두 커버. |
| 2026-06-28 | MJcoin vs MJstock 격차 | 코인에 없는 것: score_delta(모멘텀), ATR 포지션 사이징. 주식에 없는 것: 히스토리컬 ★ tracker 저장, 흰 배경 분석카드. 교차비교표 양쪽 HTML에 추가(섹션 14/18). |
| 2026-06-28 | MJcoin 명령어 | /coin scan → /coin all 리네임. "all"이 전체 스캔 의미로 더 직관적. 기존 scan도 호환 유지(sub in 조건). HELP_TEXT + 사용설명서 HTML도 함께 교체해야 일관성 유지. |
| 2026-06-28 | MJcoin 텔레그램 콜백 | callback_coin 핸들러 미등록이 /coin 명령 전체 무응답의 단일 원인. 신규 봇 모듈 추가 시 hermes_stock_bot.py CallbackQueryHandler 등록까지 세트로 확인. |
| 2026-06-28 | MJcoin 보조지표 | 검색기 prep_fn은 자기 검색기 지표만 계산. 차트 핸들러에서 여러 검색기 결과 합산하면 지표 누락 → "—". 차트 핸들러는 항상 직접 계산. |
| 2026-06-28 | Plotly showlegend | grep 으로 `"showlegend": true`(공백 포함) 검색 시 0 결과 — Plotly JSON은 공백 없이 `"showlegend":true` 출력. 공백 없이 검색해야 정확함. |
| 2026-06-28 | MJstock KR 데이터 | KIS API 국내 일봉도 100봉 제한 — `.KS`/`.KQ` yfinance 우선 필수. 삼성전자 300봉, 에코프로 485봉 실측. get_domestic_daily_ohlcv() 수정 완료. |
| 2026-06-28 | MJcoin | 코인 스크리너 indicators.py 공유 재사용(sys.path). 스테이블코인 필터(`_STABLECOINS` 셋) 없으면 USDT/USDC/USD1 등 다수 통과 오탐. |
| 2026-06-28 | MJstock 데이터 | KIS API 해외 일봉 최대 100봉 제한 — judoju(210봉), chowuryang(420봉) 필요 검색기는 KIS 단독으로는 영구 0개. yfinance 병용(500봉) 필수. |
| 2026-06-28 | MJstock selyeok | selyeok은 prepare_daily + df_weekly 둘 다 필요. 하나라도 빠지면 RVOL/BB=NaN 또는 F조건 항상 False → 결과 0개. run_scan.py 추가 시 두 인수 세트 확인 필수. |
| 2026-06-28 | MJstock 유니버스 | S&P600(소형주)은 russell2000.csv로 관리. Wikipedia 자동 수집(_update_russell2000). 대형주 universe와 별개로 auto_scan_morning.py에서 별도 selyeok 실행 블록 유지. |
| 2026-06-28 | Telegram | PTB 봇이 active일 때 curl getUpdates 직접 호출 → 409 Conflict 발생. 진단 목적이라도 절대 금지. 진단은 `launchctl print` + `pgrep` 로만. |
| 2026-06-28 | NVIDIA API | GPT OSS 120B는 reasoning model — max_tokens≥2048 필수. content=None이면 `choices[0].message.reasoning_content` fallback 시도. max_tokens=100 설정은 응답 생성 불가. |
| 2026-06-28 | signal_tracker | star_signal_date는 BUY_SIGNALS 8종(BUY_URYANGJU/BUY_SELYEOK/NONGSSA/RAPID_ACCUM/GONGJOONG/NAKPOK/REVERSAL_EARLY/MACD_BB_BUY) 기준. SCAN_PASS는 ★ 아님. |
| 2026-06-28 | signal_tracker | exit_price는 price_map에 없음(탈락 종목이므로) → 마지막 기록된 close_price 사용. price_map 조회 실패를 기본 동작으로 처리하면 안 됨. |
| 2026-06-28 | JSON 파싱 | signal_tracker가 stdout에 [Tracker] 라인 출력 → json.loads 전 `next((l for l in lines if l.strip().startswith('{')), '')` 패턴 필수. stdout에 로그 섞이는 모든 subprocess 호출에 동일 적용. |
| 2026-06-28 | Hermes1 토큰 | TELEGRAM_BOT_TOKEN 공유 → Hermes1/Hermes2/screener 모두 같은 토큰으로 getUpdates → Conflict. 봇별 토큰 분리(HERMES1_BOT_TOKEN) 필수. |
| 2026-06-24 | Hermes1 봇 재시작 (BOT-001) | 봇 "자주 뻑감"의 근본 원인 = **재시작 이중화**. botwatch의 nohup 폴백이 launchd 바깥 유령 프로세스 생성 → KeepAlive가 또 하나 띄움 → 두 봇이 getUpdates Conflict로 상호 사망. 봇 재시작은 **반드시 launchd 경로**(`launchctl enable` → `kickstart -k`)로만. 수동 nohup 금지. 진단: `pgrep -f "Scripts/hermes_local.py" \| wc -l`(=1이어야 정상), `launchctl print gui/$(id -u)/com.hermes.bot \| grep state`. 구버전 `com.bluesea.hermes_local.plist.disabled`(~/hermes/ 경로) 절대 enable 금지. 상세: 06번 BOT-001. |
| 2026-06-24 | 검증층 | 압축 시 안전 규칙 증발(Governance Decay, arXiv 2606.22528). history_manager compact_and_save + get_history_for_llm 양쪽에 GOVERNANCE_ANCHOR 삽입으로 방어. 압축 후 LLM 컨텍스트 맨 앞에 Lock Stack 4개 항상 살아있어야 함. |
| 2026-06-24 | 검증층 | 메모리 오염(Memory Contagion, arXiv 2606.23195): 편향 평가가 L2/L3 메모리 통해 누적 전파. bio_memory_engine L2 promote 시 confidence + observation_count + provenance 필드로 불확실 기억(confidence < 0.6) 격리. |
| 2026-06-24 | 검증층 | 스킬 커버리지 측정은 weakness_miner.get_skill_coverage()로. ~/.hermes/skills + ~/.claude/skills 전체 스캔 → 호출률 반환. /status 명령어에서 미호출 스킬 목록 확인 가능. 스킬 추가 후 반드시 한 번은 실제 호출해야 coverage에 잡힘. |
| 2026-06-24 | MJstock 차트 iframe 방식 | results HTML에서 Plotly 데이터 추출+재조립 방식은 실패 경로. 원본 chart HTML에서 4.8MB Plotly 번들만 CDN 태그로 교체(→75KB) → base64 data URI → iframe lazy load. 원본이 잘 작동하면 건드리지 말고 그대로 임베드할 것. |
| 2026-06-24 | 4.8MB JS 인라인 HEAD | 대용량 JS를 `<head>`에 동기 인라인 번들하면 모바일 브라우저에서 onclick 바인딩 자체가 실패. bdata 변환·layout null·divId 등 세부 문제보다 이게 근본 원인이었음. JS가 4MB+ 넘으면 무조건 CDN 또는 defer. |
| 2026-06-24 | MJstock 차트 x축 누락 | Plotly layout에서 y축 autorange만 적용하면 x축 range는 그대로 남아 히스토리가 잘림. x축도 `layout["xaxis*"].pop("range")` + `autorange=True` 세트로 처리해야 전체 히스토리 표시. y축 단독 처리 금지. |
| 2026-06-24 | MJstock 차트 모달 vs 인라인 | 인라인 차트(행 아래 펼침)는 모바일에서 테이블 레이아웃 붕괴 + 스크롤 이탈 발생. position:fixed 전체화면 모달이 모바일/데스크탑 모두 안정적. 차트 있는 테이블은 처음부터 모달 방식으로 설계할 것. |
| 2026-06-24 | MJstock 텔레그램 HTML | 텔레그램 원격 접속 시 로컬 IP 링크 전송 불가 → 자기완결형 HTML 파일로 `send_document` 전송이 정답. CDN Plotly.js + data만 추출하면 4.9MB → 1.4MB로 절감. |
| 2026-06-24 | MJstock 콜백 봇 | 두 봇이 같은 토큰으로 getUpdates 폴링 → 409 Conflict → 양쪽 사망. 독립 콜백 봇 대신 기존 Hermes 봇에 콜백 핸들러(`mjstock_results__` prefix) 추가하는 방식이 정답. |
| 2026-06-24 | NASDAQ API | NASDAQ Screener API `marketCap` 필드는 T/B/M suffix 없는 순수 달러 숫자 문자열. `_parse_cap()`에서 suffix 처리 로직 불필요. |
| 2026-06-24 | pandas column 타입 | DataFrame 컬럼명이 integer일 수 있음 → `c.lower()` AttributeError. 반드시 `str(c).lower()` 변환 후 메서드 호출. CSV 로드 시 컬럼명 타입 확인 필수. |
| 2026-06-23 | 봇 핸들러 오타 | `history_mgr.get_saturation()` → 실제 메서드명 `get_context_pressure()`. 오타 하나가 봇 전체 무응답. 신규 기능 추가 후 반드시 단독 import 테스트: `python3 -c "from handlers._base import add_to_history; print('OK')"`  |
| 2026-06-23 | launchctl 신뢰성 | 이 환경에서 `launchctl unload/load`는 Exit code 5로 실패 가능. 봇 재시작은 항상 Popen(start_new_session=True) — 새 프로세스 먼저 띄우고 기존 SIGTERM 순서 |
| 2026-06-23 | botwatch 등록 | plist 파일 존재 != launchd 등록. 재부팅 후 반드시 `launchctl list com.hermes.botwatch`로 PID 확인. `-` 이면 bootstrap 재등록 필요 |
| 2026-06-23 | MJstock 삼돌이/농사단타 | 삼돌이 OBV 조건 = `OBV < Signal` (반전 직전). 농사단타 OBV 조건 = `OBV > Signal` (순매수 완료). 방향이 반대 — 혼동 주의. |
| 2026-06-23 | MJstock US import | screen_nongsa_danta_us.py 함수명은 `prepare_daily_us()` / `prepare_5min_us()` — `_us` 접미사 필수. `prepare_30min` 없음 → needs_30min: False 등록 필수. |
| 2026-06-23 | subagent 권한 | 메인 세션의 Edit/Bash 권한이 subagent에 상속되지 않음. 메타 업데이트·파일 수정은 항상 메인 세션에서 직접 실행. |
| 2026-06-23 | SRP 분할 | bio_memory_engine.py 분할 시 ImportanceScorer/ForgettingCurve 중복 정의를 제거하고 deriver_layer에서 import — Lock Stack 파일에서 가져오는 것이므로 경로/클래스명 변경 없이 유지. |
| 2026-06-23 | pip 패키지 호환성 | `executor` 패키지가 Python 3.14에서 `cmd.async` SyntaxError — `async`는 3.5부터 예약어. 단일 import 실패가 handlers 패키지 전체(16개)를 무너뜨림. pip 패키지 추가 시 반드시 `python3 -c "import 패키지명"` 으로 3.14 호환 검증. |
| 2026-06-23 | /restart_bot 순서 | NEW 먼저 → OLD 종료 순서는 Telegram 409 Conflict → 양쪽 사망. 반드시 OLD 즉시 종료 → sleep 1 → NEW 시작 순서. |
| 2026-06-23 | 폴더 구조 리팩토링 | Scripts 루트 32개 + modules 83개 파일. 폴더 재구성 시 sys.path, launchd plist, 하드코딩 경로 전수 수정 필요 — 리스크 대비 이득이 적음. 보류. |
| 2026-06-23 | Dreaming 트리거 | random.random() 기반 조기 종료는 절대 금지. 트리거 조건은 실측 가능한 값(이벤트 수, 경과 시간, 용량)으로만 결정. |
| 2026-06-23 | hot.md 경로 | dreaming_v2.py의 _append_to_hot_md 경로는 `wiki/00_Meta/01_hot.md` — `Mjobsidian/hot.md` 루트에 쓰면 stamper 감지 안 됨. |
| 2026-06-23 | 메타 파일명 | 메타 파일 경로 참조 시 공백 아닌 언더스코어 표준 — `02_스크립트_정보.md` (O), `02_스크립트 정보.md` (X). |
| 2026-06-23 | MJstock KIS API | `get_exchange_code()` 단독 사용 금지. CSV 기반 `resolve_ticker_universe()` → 빈 DataFrame 시 NAS/NYS/AMS 순차 재시도 패턴이 표준. |
| 2026-06-23 | MJstock 빈 DataFrame | KIS API는 top-n 500에서 일부 종목 빈 DataFrame 반환. `prep_daily_fn` 호출 전에도 가드 필요. 순서: fetch → 빈 가드 → prep_daily → 빈 가드 → check_fn(try/except). |
| 2026-06-23 | pandas groupby 충돌 | `df.index.name = "date"`인 상태에서 `df["date"] = df.index...` 후 `groupby("date")` → 오류. 해결: `df.index.name = None` 먼저 클리어 후 column 추가. |
| 2026-06-23 | 퀀트 60컬럼 | stoch_rsi는 indicators.py 함수 없음 — RSI_14 시리즈에서 인라인 계산. obv_slope_5d = polyfit(x, OBV[-5:], 1)[0]. dd_dist_pct는 samdoli 검색기만 채워짐(DD 컬럼 존재 시). |
| 2026-06-23 | history_manager | 파일 저장 메시지 수(N)와 COMPACT_THRESHOLD(T) 관계: N/T < 0.5 유지. 현재 10/60=16.7%. 이 비율 깨지면 세션 시작 즉시 포화. |
| 2026-06-23 | permission_bridge | 개인 봇에서 bash 자동 승인은 INTERNAL_TOOLS 분류. 단, 결제·삭제·외부 민감 API는 EXTERNAL 유지 — 이 경계선 흐리지 말 것. |
| 2026-06-23 | 봇재시작 | /restart_bot: NEW 먼저 시작 → Conflict 양쪽 사망. OLD 먼저 종료 후 sleep 1 && NEW 순서가 정답. Telegram은 단일 인스턴스 — 두 프로세스 동시 폴링 절대 금지. |
| 2026-06-23 | 패키지 | executor 패키지 Python 3.14 호환 불가(async 예약어 SyntaxError). _base.py 한 줄이 핸들러 16개 전체 먹통의 단일 원인. pip 패키지 추가 시 `python3 -c "import <패키지>"` 테스트 필수. executor 재설치 금지. |
| 2026-06-23 | vault | /vault graph: Vault 노드 5000개 초과 시 graphify 기본 제한 초과 오류. `GRAPHIFY_VIZ_NODE_LIMIT=10000` 환경변수 필요. Vault 규모 커질수록 이 설정 유지 확인. |
| 2026-06-23 | EMA 조건 구현 | 검색식 조건 부등호는 PDF 원본 그대로. `EMA_단기 > EMA_장기` = 상승배열. 헷갈리면 반드시 PDF 재확인. |
| 2026-06-09 | 루프 아키텍처 | 루프 = 크론 + 루프 본체 의사결정자. 마법은 루프 안의 피드백. CoVe + ToolResult + Circuit Breaker = 피드백 품질 체계. |
| 2026-06-24 | 스킬 구조 | ~/.claude/skills/는 Claude Code 전용. 범용 스킬은 ~/.hermes/skills/에 두어야 AI 교체 시에도 유지됨. → 일원화 완료. |
| 2026-06-24 | 스킬 병합 | 같은 역할 스킬 2개 존재 시 더 완성된 쪽을 살리고 구버전만 삭제. mj-meta-update vs meta-update 비교 → hermes 쪽이 5단계 절차 완비 → hermes 유지, claude 버전 삭제. |
| 2026-06-03 | 파일 수정 | 기존 파일 수정 시 write_file(전체 덮어쓰기) 절대 금지 → Edit(patch)만. write_file = 기존 내용 소실 위험. |

---

## 📌 현재 진행 중인 작업

### ✅ 완료 — MJstock + Coin 텔레그램 봇 UX 개선 (2026-06-30)
- `handlers/_stock_coin.py`: `/coin all` 버튼 레이블 `검색(N종)` 형식으로 변경 (cmd_coin, _handle_coin_scan_back 2곳)
- `Mjstock/app.py`: `send_scan_result_telegram()` 시그니처 확장 + InlineKeyboard 버튼 포함 전송 + 스캔 루프 session_state 비동기 전환 (블로킹 제거)
- `handlers/_stock_mjstock.py`: `_MJSTOCK_SCREENER_NAMES` 딕셔너리, `_handle_mjstock_scan_list()` 신규, `_handle_mjstock_chart()` date_str 파라미터 추가, `callback_mjstock()` 4-part 파싱 지원

### ✅ 완료 — MJstock 주식봇 AI 채팅 + quant CSV 저장 + signal_tracker 개선 (2026-06-28)
- Hermes1 HERMES1_BOT_TOKEN 분리 → getUpdates Conflict 해결
- Hermes2 API minimax-m2.7 → openai/gpt-oss-120b 전환
- hermes_stock_bot.py AI 채팅 기능(`_call_gpt_oss`, `_history`, `handle_text`) 추가
- signal_tracker.py BUY_SIGNALS/SELL_SIGNALS 상수, star_signal_date/circle_date/exited 로직 개선
- scan_all_ticker.py + run_scan.py quant CSV 저장 연동
- tracker/signal_log.csv 신규 생성
- **⚠️ 후속 과제**: `docs/quant_logic_analysis.html` 업데이트 필요 (star_signal_date/circle_date/return_30d 반영)

### ✅ 완료 — Claude Code 스킬 정리 + ~/.hermes/skills/ 일원화 (2026-06-24)
- `~/.claude/skills/` 15개 전체 삭제 (13개 빈 껍데기 + mj-meta-update 구버전 + mj-stock-analyze)
- `mj-stock-analyze` → `~/.hermes/skills/mj-stock-analyze/`로 이전
- `mj-meta-update` → hermes `meta-update/`가 더 완성본 → 구버전만 삭제
- `hermes_harness_skill_모음.md` 통합 완료 상태로 갱신

### ✅ 완료 — arXiv 6편 논문 하네스 적용 + 봇 안정화 (2026-06-24)

**arXiv 논문 하네스 (6편)**:
- `history_manager.py`: `GOVERNANCE_ANCHOR` 상수 추가 — 압축(`compact_and_save`) + 컨텍스트 조립(`get_history_for_llm`) 양쪽 적용. 압축 후 안전 규칙 59% 사라지는 문제(Governance Decay, 2606.22528) 방어.
- `verification_engine.py`: `verify_file_changed()` / `verify_db_row_exists()` / `snapshot_file_hash()` + `detect_sycophancy_risk()` 추가 (GroundEval 2606.22737, Sycophancy 2606.20718)
- `weakness_miner.py`: `record_skill_invocation()` / `get_skill_coverage()` / `skill_invocations` DB 테이블 + `validate_skill_safety()` 추가 (Skill Coverage 2606.20659, SkillHarness 2606.20636)
- `bio_memory_engine.py`: L2 에피소드 `confidence` / `observation_count` / `provenance` 필드, L3 `confidence` / `success_count` 추가 (Memory Contagion 2606.23195)

**봇 안정화**:
- `handlers/_base.py`: `executor` Python 3.14 SyntaxError 제거 → `asyncio.create_subprocess_shell` 교체 (모든 명령어 먹통 근본 원인)
- `handlers/_system_ops.py`: `/restart_bot` 레이스 컨디션 수정 — OLD 먼저 SIGTERM, 1초 후 NEW 시작
- `handlers/_vault.py`: `/vault graph` 노드 오버플로우 graceful degradation

**신규 스킬**: `grill-me`, `grilling`, `diagnosing-bugs` (3개, `~/.hermes/skills/`)

### ✅ 완료 — MJstock results HTML 차트 iframe 방식 전환 (2026-06-24)
- **generate_results_html.py**: Plotly 데이터 추출+JS 재렌더링 방식 폐기 → `_load_chart_iframe()` 신규. 원본 chart HTML에서 4.8MB Plotly 번들 → CDN 태그 교체(75KB) → base64 data URI → `<iframe data-src="...">` lazy load. 파일 크기 6MB → 1.8MB. `toggleChart()`도 iframe.src 설정으로 단순화.
- **docs/MJstock_사용설명서.html**: "4. 차트 보는 법" 섹션 — iframe 방식 설명 + 재발방지 warn 박스 추가.

### ✅ 완료 — MJstock 차트 전체화면 모달 전환 + position_monitor_guide 이동 (2026-06-24)
- **generate_results_html.py**: 차트 인라인 토글 → 전체화면 모달(position:fixed). `#modal-toolbar` + ESC 닫기. x축 range 누락 버그 수정(`xaxis*` autorange). height 반응형(`calc(100vh - 56px)`). Plotly responsive+scrollZoom 추가.
- **sellstock/position_monitor_guide.html** (이동): `docs/` → `sellstock/`. /mjbuy, /mjsell, /mjpositions 상세 문서 + 퀀트 매도 시그널 논리 추가 (v2.0).
- **docs/MJstock_사용설명서.html**: 차트 사용법 설명 모달 방식으로 업데이트.

### ✅ 완료 — MJstock HTML 결과 리포터 + 텔레그램 콜백 + NASDAQ 1000 + app.py Tab 2 (2026-06-24)
- **generate_results_html.py** (NEW): 스캔 결과 자기완결형 HTML. CDN Plotly.js 2.27.0. 시그널 상단 정렬. 종목 행 클릭 → 차트 인라인 토글. Output: `results/_html/results_{screener_key}_{date}.html`
- **auto_scan_morning.py**: `run_screener()` 반환값 구조화. 스캔 후 HTML 자동 생성. `send_results()` + `_send_telegram_with_buttons()` 신규. 기존 차트 첨부 방식 완전 제거.
- **handlers/_callbacks.py + _stock.py**: `mjstock_results__` prefix 콜백 라우팅. `callback_mjstock_results()` 신규 — HTML send_document 전송.
- **mjstock_callback_bot.py** (NEW, inactive): 409 충돌로 미사용. Hermes 봇이 콜백 처리.
- **screener/data_loader.py**: NASDAQ Screener API 전환. 시총 상위 1000개. `str(c).lower()` integer column 버그 수정.
- **app.py Tab 2**: selectbox → checkbox 그리드(2열). `st.empty()` 진행 표시. 선택 검색기만 실행.
- **docs/MJstock_사용설명서.html**: 새 텔레그램 포맷 + 버튼 동작 설명 추가.

### ✅ 완료 — MJstock 삼돌이/농사단타 현지화 + HTML 5종 통합 (2026-06-23)
- **screen_samdoli_kr/us.py**: KR/US 현지화. US = 시총 $1B↑, 거래량변화 150%↑, SMA200 추가
- **screen_nongsa_danta_kr/us.py**: 삼돌이 후보 대상 3박자(50억봉+3매수+OBV) 단타. US는 30분봉 미사용
- **run_scan.py**: 4개 검색기 레지스트리 등록 + 임포트 검증 성공
- **docs/ 파일**: 8개→5개 (samdoli_guide / nongsa_danta_guide / nongsa_signal_board 삭제, 내용 흡수)
- **사용설명서**: 6대→10대 검색식, 카드/타이밍표/파라미터표/선택가이드 업데이트
- **signals_entry_points**: 섹션13 삼돌이/농사단타 Phase 가이드 추가
- **korean_original_formulas**: S9(삼돌이KR), S10(농사단타KR) 수식 추가
- **kr_to_us_conversion**: S8(삼돌이US), S9(농사단타US) 변환표 추가

### ✅ 완료 — MJstock screener 개선 v3 (2026-06-23)
- **signal_tracker.py**: `score_delta` / `reversal_early` 컬럼 추가. `record_scan()` 파라미터 `score_delta_map` 추가
- **batch_fill_returns.py**: `_trading_days_elapsed()` 도입 — 거래일 기준 수익률 채움 (캘린더일 → 영업일)
- **future_screeners/** 신규 폴더: 삼돌이/농사단타 미적용 검색기 코드 4개 파일 보관
- **docs/ HTML 2종 업데이트**: quant_logic_analysis.html (22컬럼), signals_entry_points.html (신규 컬럼 설명)
- **20260620_1_개선사항 폴더**: 모든 기능 반영 완료 확인 → 삭제 예정 (MJ 직접 삭제)

### ✅ 완료 — bio_memory_engine.py SRP 분할 + 핵심 버그 수정 5종 (2026-06-23)
- **bio_memory_engine.py**: 955줄 → 627줄 (SRP 분할). 벡터 계층 → vector_engine.py 분리. ImportanceScorer/ForgettingCurve 중복 제거
- **vector_engine.py**: 신규 생성 — TurboVecLight, VectorIndexManager, get_vector_backend 등 벡터 인덱스 계층 전담
- **dreaming_v2.py**: 결함 #5(PEMS 고착화) 수정. random.random() 기반 조기 종료 제거 → 이벤트 수 + 1시간 간격 체크로 교체. hot.md 경로 버그 동시 수정
- **hermes_local.py**: PID 충돌 자동복구 추가 (Conflict 에러 감지 → launchctl kickstart 자동 실행)
- **handlers/_base.py**: 메모리 포화도 자동 압축 추가 (add_to_history()에서 포화 감지 → compact_and_save() 자동 호출)
- **modules/harness_verifier.py**: 파일명 버그 수정 (`02_스크립트 정보.md` 공백 → `02_스크립트_정보.md` 언더스코어)

### ✅ 완료 — Hermes1 버그 수정 3종 (2026-06-23)
- **scan_single.py**: `get_exchange_code()` → `resolve_ticker_universe()` 교체. 빈 DataFrame 재시도(NAS/NYS/AMS). AAOI 등 나스닥 종목 `'close'` KeyError 해결
- **history_manager.py**: `COMPACT_THRESHOLD` 30→60, `KEEP_RECENT` 10→15, 파일 저장 최근 20→10개. 세션 시작 직후 67% 포화 문제 해결
- **permission_bridge.py**: `RUN_CMD` EXTERNAL_TOOLS → INTERNAL_TOOLS 이동. bash 실행 120초 타임아웃 "권한 없음" 오류 해결
- **헤르메스 봇 재시작**: PID 71365

### ✅ 완료 — MJstock 스캔 유니버스 전면 확장 (2026-06-23)
- **auto_scan_morning.py**: 나스닥500 + 러셀500 + 코스피500 + 코스닥500 각각 별도 실행. 총 20스캔 / 07:00 KST
- **auto_scan_intraday.py**: 동일 4유니버스 각각 별도 실행. 타임아웃 300s→600s. 총 12스캔 / 시간대별
- **텔레그램**: 유니버스별 별도 메시지 수신 (8종 레이블). 연결 테스트 완료 ✅

### ✅ 완료 — MJstock 시간대별 자동 스캔 + 퀀트 DB 확장 + 차트 외부 접속 + HTML 초보자 설명 (2026-06-23)
- **auto_scan_morning.py**: 미국 morning 스캔(07:00 KST)만 활성화. KR 블록 주석 처리. `--scan-type morning` 인자 추가
- **auto_scan_intraday.py**: 미국 intraday 스캔(22:30 KST)만 활성화. KR `return 0` 즉시 종료. `--scan-type intraday` 인자 추가
- **run_scan.py**: `compute_quant_snapshot()` — ret_30d/60d/90d 추가. `compute_intraday_signal_snapshot()` 신규 (7컬럼, US/KR 자동 구분). `--scan-type` CLI 인자, `run_one(scan_type)` 파라미터 추가
- **batch_fill_returns.py**: `[5,10,20]` → `[5,10,20,30,60,90]` 확장. 종목별 현재가 1회 호출 최적화
- **handlers/_stock.py `_handle_mjstock_chart()`**: 로컬 IP URL → `bot.send_document()` HTML 첨부 방식 전환 (외부망 접근 가능)
- **docs/ 5종 HTML**: nongsa_danta/samdoli/nongsa_signal_board/korean_original_formulas/kr_to_us_conversion — 초보자 설명박스 + SVG 비유 차트 신규 추가

### ✅ 완료 — MJstock HTML 문서 업데이트 (2026-06-23)
- **korean_original_formulas.html**: 5개 전략 섹션에 "HTS 원본 전략식 (사진 직접 독해)" div 블록 추가
- **kr_to_us_conversion.html**: 5개 전략 섹션에 HTS 원본 전략식 pre 블록 추가
- **signals_entry_points.html**: "초보자 빠른 이해" 섹션 신규 추가 (농사단타 3단계 흐름, SVG 5분봉 타점 차트, 손절/익절 카드)
- **quant_logic_analysis.html**: "초보자 빠른 이해" 섹션 신규 추가 (전체 흐름 SVG, S/A/B/PASS 등급 카드)
- **미완료**: `MJstock_사용설명서.html` 업데이트 (다음 세션 과제)

### ✅ 완료 — MJstock 검색기 개선 v2 (2026-06-23)
- **ticker_analyze.py**: 분석 결과 텔레그램 메시지 하단에 Claude 인지편향 체크 프롬프트 템플릿 자동 첨부 ("위 종목 {ticker} 점수 {score}점 나왔는데 인지편향 체크리스트랑 청산 조건 잡아줘")
- **screen_selyeok_pochak.py BUG FIX**: `c_ema` 조건 역방향(EMA_9 > EMA_5) → 정방향(EMA_5 > EMA_9) 수정. 이 버그로 하락 배열 종목이 통과되고 상승 배열이 필터링되던 문제 해결
- **screen_uryangju_nongsaju.py 강화**: EMA45 추가, 30분봉 Ichimoku 구름대 추가, K 조건 EMA 기준 오류 수정(EMA_200→EMA_45), J 조건(30분봉 구름대 위) 신규 추가
- **nongsa_danta_guide.html / nongsa_signal_board.html**: v2.0 업데이트 (이전 세션)

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
- **요약**: `wiki_auto_stamper.py`를 확장하여 실시간 저장 시 태그 8개 자동 조율 및 링크 텍스트화 적용. 하네스 컨트롤(harness, hdod, hstatus, hrollback)의 상세 분석 가이드 생성 및 깨진 링크 정리.
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
- **태그 기반 전환 유지**: 링크 ❌, `위키 링크` 미생성. tags=[scanned, 카테고리]로 분류
- **관련**: 스크립트 정보, 시스템 상태, 주요 시스템 가이드 및 FAQ, 시스템 인벤토리

### ✅ 완료 — Python 3.10 호환성 문제 해결 (2026-05-27)
- **문제**: `dialectic_layer/_dreamer.py` (line 202)와 `hermes_context_builder.py` (line 43)에서 `str | None` (PEP 604) 문법 사용 → macOS 기본 Python 3.9.6에서 SyntaxError 발생
- **해결**: 두 파일 상단에 `from __future__ import annotations` 한 줄씩 추가
- **결과**: handlers/ 9개 서브모듈 전부 Python 3.9.6에서 import 성공
- **관련**: 시스템 상태, 주요 시스템 가이드 및 FAQ, 시스템 인벤토리

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
- **관련**: 스크립트 정보, 시스템 인벤토리, 시스템 상태

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
- 00_Meta_지도 — 메타 폴더 내비게이션
- 시스템 상태 — 전체 변경 이력
- 스크립트 정보 — 모듈 및 명령어 가이드
- 주요 시스템 가이드 및 FAQ — 문제 해결 및 Changelog
- 시스템 인벤토리 — 설치 환경 정보
- [2026-06-03] 메모리 누락 명령어(/memory) 복구 및 Dreaming v2 PEMS 엔진 고착화(수렴 버그) 수정 완료. (offline_consolidation 흐름 정상화)
gemma4 launchctl unload ~/Library/LaunchAgents/com.bluesea.llama_server2.plist
        launchctl load ~/Library/LaunchAgents/com.bluesea.llama_server2.plist
---

## 2026-06-05 Bio-Memory Engine v9.3 개선 — 3파일 구조 개선 완료

- ✅ **bio_memory_engine.py**: `_get_l2_bytes()` 메서드 추가(402-405행), `get_memory_status()`에 KB/MB 실시간 표시
- ✅ **dreamer_layer.py**: `offline_consolidation_forced()` 메서드 추가(270-296행) — 중요도 하위 50% 강제 L3 전이 (1MB 초과 시 자동 발동)
- ✅ **dreaming_v2.py**: `_run_offline_consolidation()`에 용량 위기 시 강제 증류 호출(124-128행) + `_commit_to_l3_semantic()` atomic write 적용(230-274행)
- ✅ **import 검증**: 3개 파일 전부 Python import 정상 확인
- **연관**: 03_시스템 인벤토리, 05_시스템 상태, 04_주요 시스템 가이드 및 FAQ, 00_Meta_지도, 06_에이전트_오류_및_재발방지_보고서, constitution.local

## 2026-06-03 작업 완료 목록

- ✅ `/claude_brief` 핸들러 추가 — `handlers/_meta.py` 신규, 6대 메타 문서 → claude_briefing.md 브리핑 생성
- ✅ Dreaming V2 PEMS 고착화 버그 수정 (`offline_consolidation` 항상 실행)
- ✅ Hermes 봇 재시작 (pkill → launchd 자동 재시작)
- ✅ HELP_TEXT 완전판 업데이트 (33개 명령어)
- ✅ wiki 전체 59개 파일 타임스탬프 일괄 복구
- ✅ `constitution.md` §9 타임스탬프 의무 갱신 규칙 신설
- ✅ `wiki_auto_stamper.py` 기능 확장 (태그 최대 8개 병합, 링크 텍스트화 및 긍정형 전방탐색 파싱)
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


|*최종 업데이트: 2026-06-30 19:38*

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
- **연관**: 00_Meta_지도, 03_시스템 인벤토리, 02_스크립트 정보

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

---

### ✅ 완료 — MJstock 스캔 시스템 개편 v2.0 (2026-06-23)

**프로젝트**: `/Users/bluesea/Applications/Mjstock`

**완료 항목**:
- `auto_scan_morning.py` — 신규. 아침 일봉 스캔 전용 (KST 07:00). 미국 5종 + 한국 5종 (uryangju/judoju/danta/selyeok/chowuryang) 실행
- `auto_scan_intraday.py` — 신규. 장중 스캔 전용. `--market us` (KST 22:30) / `--market kr` (KST 09:10). pochak/shooting/chuddoli 3종
- `screener/send_scan_result.py` — 수정. 텔레그램 로컬 IP 링크 → HTML 파일 직접 sendDocument 전송. `get_chart_paths()` 신규. 폰 LTE에서 바로 탭하여 열림
- `auto_scan_nasdaq500.py` — `.bak`으로 백업 (더 이상 사용 안 함)
- crontab — 기존 `0 7 auto_scan_nasdaq500.py` 제거. 신규 3개 등록:
  - `0 7 * * 1-5` auto_scan_morning.py → logs/scan_morning.log
  - `30 22 * * 1-5` auto_scan_intraday.py --market us → logs/scan_intraday_us.log
  - `10 9 * * 1-5` auto_scan_intraday.py --market kr → logs/scan_intraday_kr.log
- `docs/` 5개 HTML 교체 (Jun 18 → Jun 21 버전): MJstock_사용설명서, signals_entry_points, quant_logic_analysis, korean_original_formulas, kr_to_us_conversion

**해결된 문제**:
- 텔레그램 차트 링크 폰에서 안 열림 (LTE/5G 환경 차단) → HTML 직접 첨부로 해결
- 장중 전용 검색기(pochak/shooting/chuddoli)를 아침에 실행하던 오류 → 시간대 분리
- 장 4시간 전에 스캔하던 cron 타이밍 오류 → 올바른 시간대로 수정

**미해결 후속과제**:
- `run_scan.py --reuse-cache` 옵션 추가 (일봉 중복 다운로드 근본 해결)
- `health_check.py` `.env` 경로 수정 (`screener/screener/.env` → `screener/.env`)
- 서머타임 자동 감지 (미국 장중 22:30 vs 23:30)

---

### ✅ 완료 — Hermes 메모리 레이어 개선 + MJstock 티커 분析기 (2026-06-23)

**프로젝트**: Hermes + `/Users/bluesea/Applications/Mjstock`

**완료 항목**:
- `modules/memory_schema.py` — 신규. L2 EpisodicEntry 데이터클래스 (is_worth_storing/is_expired/retention_score), L3 SemanticMemory (카테고리 dict 구조), CATEGORY_KEYWORDS 자동 분류 테이블
- `modules/memory_consolidator_v2.py` — 신규. L2→L3 증류 파이프라인. Dreaming 폐기 후 고아된 경로 복구. 실측 경로(`~/.hermes/memory/`) 기반. `--dry-run` / `--health` 플래그 지원
- `modules/context_assembler_v2.py` — 신규. 기존 7블록 → 키워드 감지 시 3~7블록 (Rule of Simplicity). history 15턴 → 10턴. ms 측정 로그 추가
- `screener/ticker_analyze.py` — 신규. `/mjstock AAPL` 명령어 개선판. KIS API 1회 다운로드 → 모든 검색기 동시 적용 → 점수 순위표 + 1등 시그널 텔레그램 전송. `include_intraday=True` 옵션으로 5분봉 장중 검색기 포함
- crontab — 매일 04:00 `memory_consolidator_v2` 자동 실행 등록

**해결된 문제**:
- L2→L3 증류 경로 끊김 (Dreaming 폐기 후 고아 상태) → memory_consolidator_v2로 복구
- L3 패턴 카테고리 없이 무작위 누적 → SemanticMemory 카테고리 dict 구조로 개선
- context_assembler 7블록 항상 전부 조립 → 키워드 감지 시 선택적 조립으로 경량화
- /mjstock 단일 검색식만 → 전체 검색기 동시 비교 + 점수 순위표

**추가 완료 (2026-06-23)**:
- `harness_agent.py:255` — `context_assembler` → `context_assembler_v2` 전환 완료
- `screener/screen_nongsa_danta_kr.py` — 신규 설치 (농사단타 한국)
- `screener/screen_nongsa_danta_us.py` — 신규 설치 (농사단타 미국)
- `screener/screen_samdoli_kr.py` — 업데이트 설치 (HTS 이미지 확인 기반 파라미터 전면 수정)
- `docs/nongsa_danta_guide.html`, `docs/nongsa_signal_board.html`, `docs/samdoli_guide.html` — 신규 가이드 HTML

**미완료**:
- ticker_analyze.py 텔레그램 핸들러 등록 (`_stock.py`의 CommandHandler("mjstock") 교체)
