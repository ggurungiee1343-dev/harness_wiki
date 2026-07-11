---
tags: []
---
## ⚖️ 최근 감사 결과 (Dreaming)
**[목표 진척도]**
사용자의 기술적 문제(명령어 오류, 메모리 구조화)에 대해 구체적인 해결책과 설계안을 제시함으로써 '유용성' 측면에서 높은 진척도를 보이고 있습니다. 요청된 데이터 구조화 및 관리 설계 작업을 즉각 수행하며 장기 목표를 충실히 이행 중입니다.

**[헌법 준수 감사]**
결론을 먼저 제시하는 역피라미드 구조와 전문 용어를 활용하여 MJ님의 스타일 프로필을 충실히 준수하고 있습니다. 불필요한 수식어나 메타 해설을 지양함으로써 'AI 냄새'를 효과적으로 제거하고 시스템의 핵심 가치인 신뢰성을 유지하고 있습니다.

# 📝 프로젝트 핫토픽

**최종 업데이트: 2026-07-11 22:35*

## 📠 실시간 상태 (KV — /status 명령어로 설정)
- **Active External Project**: `/Users/bluesea/Applications/Mjstock` (자동 스캔 시스템 구축 완료)
- **Current Model (Telegram)**: GPT OSS 120B (기본, NVIDIA API) / DeepSeek API (폴백) / Qwen2.5-14B 로컬 (선택 가능)
- **Current Model (WebUI)**: Qwen2.5-14B (로컬) / GPT OSS 120B (NVIDIA) / Minimax M2.7 (NVIDIA) — 3종 멀티모델 통합 완료
- **Hermes1 PID**: 66385 (2026-06-30 기준)
- **hermes_stock_bot.py PID**: 68065 (2026-06-30 재시작 — com.hermes.stockbot, BOT-002 버그 수정 후)
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
| 2026-07-11 | 0건 진단 순서 고정 | MJstock 장중 검색기 5종 0건 재발(BUG-MJS-030) — 처음엔 RVOL 임계값 문제로 보였으나 실제 최우선 원인은 `US_SCREENERS["pochak"]` prepare_* 배선 자체가 안 돼 있던 것과 KIS 30분봉 120봉 페이지네이션 한계로 156기간 지표가 영구 NaN이던 것이었음. 0건 진단할 땐 임계값 의심 전에 항상 ① prepare_*/딕셔너리 배선 등록 여부 ② 지표 계산에 필요한 원천 데이터 길이 확보 여부부터 확인하고, 그 다음에야 임계값 실측 대조로 넘어갈 것. |
| 2026-07-09 | pandas `df.copy()` 재할당의 침묵 실패 패턴 | `save_scan_result()`가 `matched = matched.copy()`로 지역 복사본에만 컬럼을 추가하고, 호출부는 원본 `matched`를 계속 재사용 — CSV엔 정상 저장되니 겉보기엔 멀쩡한데 DB insert만 매번 조용히 0행. "함수에 df 넘기고 그 함수가 컬럼 추가했다"고 가정하지 말고, 함수가 `.copy()`를 쓰는지 반드시 확인할 것 — 쓴다면 그 결과를 호출부가 돌려받아 재할당해야 함. |
| 2026-07-09 | 신규 외부 API 연동은 실제 운영 규모로 타이밍 테스트 필수 | LS API(1회/초 제한) 연동 시 소규모(150종목) ad-hoc 스크립트로만 검증하고 실제 운영 유니버스(코스피500 등 500종목) 크론 파이프라인으로는 테스트 안 함 — 실제 배포 후 900초 타임아웃으로 검색기 8개가 스캔 실패나는 사고로 이어짐(05번 2026-07-09 (5) 참조). 속도 제약 있는 신규 데이터소스를 붙일 땐 "종목당 호출횟수 × 전체 유니버스 크기 ÷ 처리속도"를 미리 계산하거나, 최소한 운영 규모에 가까운 샘플로 타이밍까지 재봐야 함 — 기능적으로 동작하는지만 보고 끝내면 안 됨. |
| 2026-07-09 | "docs 먼저 확인" 원칙의 재발 사례 | judoju_kr의 O/P/X/Y/Z~c를 "원본 HTS 사진이 없어 구현 불가"라고 답했다가 MJ님이 "내가 이미 줬는데?"라고 지적 — 실제로 `docs/원본문서(참고용)/검색식 원본/주도주단기농사/`에 9장이 있었음. 기존 CLAUDE.md 원칙("새 도구 제안 전 docs 폴더 HTML부터 확인")이 `docs/*.html`만 명시했는데, **원본 사진 폴더도 동일하게 먼저 검색 대상**임을 놓침 — "자료가 없다"고 결론 내리기 전엔 `docs/`와 `원본문서(참고용)/` 두 곳 다 먼저 뒤질 것. |
| 2026-07-09 | HTS 원본식 독해 | 조건 토글이 ON이어도 실제 "조건식"(A and B and...) 문자열에 그 알파벳이 없으면 미사용 정의일 뿐. uryangju_kr의 L(EMA1≥200)이 이 케이스 — 토글은 켜져 있었지만 실제 조건식엔 없었음. 원본 대조 시 토글 상태만 보지 말고 조건식 문자열까지 끝까지 확인할 것. |
| 2026-07-09 | 반사실 검증 설계 | MFE처럼 "이상적 최고점"을 벤치마크로 쓰는 분석은, 그 최고점 관측이 검증 대상인 청산규칙 자체에 의해 끊기지 않는지 먼저 의심할 것 — 우량주농사 "매도문제 34%"가 실은 이 순환논리 함정이었고, "청산 안 하고 계속 보유했다면?" 반사실로 재검증하니 3.2%로 정정됨(05번 2026-07-09 항목). |
| 2026-07-09 | 가짜 프록시의 위험성 | "API 미지원"이라 가정하고 넣은 대체 기술지표(OBV/CMF/MFI)가 실제로는 API가 지원하는 진짜 데이터(개인/외국인/기관 순매수)를 흉내만 내며 방향까지 반대로 가 있었음(chowuryang_kr). 조건을 아예 안 넣은 uryangju(US, 매수문제 0%)보다 가짜로 채운 kr판(매수문제 54.5%)이 더 나빴음 — 없느니만 못한 프록시는 적극적으로 해악. |
| 2026-07-07 | 진단 도구 자체의 오탐 의심 | `/vault check` "닫히지 않은 프론트매터 22개"는 파일 문제 아니라 진단이 첫 512바이트만 읽어 긴 프론트매터를 오탐한 것(8192로 늘리니 0). "재실행해도 같은 결과"면 도구 로직부터 의심. 06번 BUG-MJS-025 인접. |
| 2026-07-07 | "검색기 전부 0"이 항상 에러는 아님 | 로그의 `점수/시그널 [1-9]` 이력으로 "진짜 신호 없는 날(정상)"과 "크래시(returncode=1)/데이터 0"을 구분. 07-06 US 전부 0은 정상(07-01 chuddoli 러셀 12신호 등 최근 실신호 있었음). 크래시는 요약만 보면 안 잡히고 로그를 열어야 잡히는 침묵 실패. |
| 2026-07-04 | 좀비 데몬은 launchd KeepAlive가 되살린다 | `mjstock_callback_bot.py`는 과거 getUpdates 충돌 후 폴링을 코드에서 껐지만(전송 전용 주석) launchd `KeepAlive`가 빈 sleep 루프 프로세스를 계속 유지 — "봇 2개 떠 있음" 혼동의 근원. 기능을 다른 봇으로 이관했으면 **launchd job도 함께 bootout+plist .disabled** 처리할 것. 버튼 콜백은 `handlers/_stock_mjstock.py:callback_mjstock_results`가 유일 처리자. 05번 2026-07-04 항목 참조. |
| 2026-07-04 | 봇 프로세스 재시작 직후 즉시 클릭 요청 금지 | 코드 수정은 봇 프로세스(`com.hermes.stockbot`) 재시작 전까진 반영 안 됨. 재시작 직후 Hermes 하네스 초기화(ActionRealization/FTS 인덱싱 등, 몇 초 소요) 중 도착한 클릭은 "Query is too old" 에러로 유실 가능 — 재시작 후 몇 초 대기 후 테스트 요청할 것. |
| 2026-07-03 | MJstock 검색기/신호 역할 분리 | 20개 검색기 전수 조사 결과: 대부분(우량주농사/주도주단기/단타의신/세력포착/매수후바로슈팅 등)은 이미 우상향 중인 종목을 잡는 지속형 필터고, 반전 타이밍 감지는 `signals_farming.py`의 ★신호 레이어가 전담(삼돌이/농사단타 계열만 검색기 자체에 반전 로직 내장). 신규 검색기 설계 시 "이게 지속형인지 반전형인지" 먼저 분류하고 반전 감지는 signals_farming으로 위임할 것. |
| 2026-07-03 | 종료조건과 이정표는 분리 설계 | +5% 도달을 매도 규칙(익절 기준)이자 동시에 신호 검증 추적의 종료 기준으로 같이 쓰면, 신호가 실제로 얼마나 더 갈 수 있었는지(진짜 잠재력)가 데이터에서 잘려나감. 매도 실행 기준과 추적용 데이터 수집 기준은 별도 필드(예: `reached_5pct_date`는 이정표, `close_reason`은 실제 종료)로 분리해서 기록할 것. |
| 2026-07-02 | quant.db cron 체인 | cron→auto_scan→run_scan→quant.db 체인 완성. 별도 저장 트리거 불필요. 수동 실행도 동일하게 저장됨. 주식 3회/일(07:00·09:10·22:30) + 코인 1회/일(08:00) + 수익률 동기화 17:30 양쪽. |
| 2026-07-02 | MJcoin quant.db 통합 | 코인/주식 동일 quant.db 통합 시 `market='coin'` 컬럼으로 구분. BTC 강도 컬럼은 `spy_*` 재사용 — DB 스키마 변경 없이 즉시 적용, `market='coin'` 필터로 조회 시 혼동 없음. 새 자산군 추가 시 별도 DB 신설보다 market 컬럼 구분이 교차분석 쿼리 측면에서 유리. |
| 2026-07-02 | MJcoin BTC 강도 컬럼 설계 | BTC 강도를 spy_* 컬럼으로 재사용한 이유: ①DB 스키마 변경 없이 즉시 적용 ②`market='coin'` 필터 사용 시 spy_* = BTC 강도임을 맥락으로 파악 가능 ③향후 코인 전용 컬럼 추가 시 마이그레이션 없이 오버라이드 가능. 단점: spy_* 컬럼명이 BTC 의미와 다르므로 쿼리 시 주석 필수. |
| 2026-07-02 | MJstock quant.db 설계 | CSV만으로는 검색기 간 교차분석/시계열 쿼리 불가 → SQLite 중앙 DB 도입. UNIQUE(scan_datetime, screener, ticker) 제약으로 중복 삽입 방지. CSV는 휴먼 리더블 백업, DB는 쿼리용 주 저장소로 역할 분리. |
| 2026-07-02 | MJstock 시장강도 컬럼 | 개별 종목 결과만 보면 시장 환경 파악 불가 → 스캔 시점의 SPY/KOSPI 상태(MA위치·수익률)를 모든 행에 스탬프로 박음. 나중에 "약세장 스캔 결과"와 "강세장 스캔 결과"를 분리 분석 가능. |
| 2026-07-02 | 하네스 문서 파편화 | "미완료 항목"을 여러 메타 문서에 각자 만들면 어느 게 최신인지 알 수 없게 됨(GitHub Remote가 이미 완료됐는데 다른 문서엔 여전히 미완료로 남아있던 사례). 미완료 항목은 `HERMES3_MASTER_DEVELOPMENT_GUIDE.md` 한 곳(흩어진 미완료 항목 통합 표)으로만 추적하고, 완료된 항목을 담은 로드맵 문서는 완료 확인 즉시 삭제(git 히스토리로 복구 가능). |
| 2026-07-02 | book-to-skill 자동화 한계 | PDF→구조화 변환 도구가 "API 키 불필요, 로컬 처리"라고 홍보해도, 실제로는 Claude Code 등 LLM 에이전트가 세션 안에서 직접 읽고 합성하는 "Agent Skill" 방식일 수 있음(book-to-skill이 그 케이스) — `scripts/extract.py`는 raw 텍스트 추출만 하고 챕터/프레임워크 구조화는 에이전트 몫이라 완전 무인 launchd 자동화 불가. 도구 도입 전 "핵심 로직이 결정론적 스크립트인지 LLM-in-the-loop인지" 반드시 구분할 것. |
| 2026-07-02 | arXiv ID 검증 없이 조사 착수 금지 | 스크린샷에 적힌 arXiv ID("2607.01871")가 실제로는 존재하지 않는 논문(404)이었음 — 다이제스트 생성 과정의 오류인지 원인 불명. 논문 기반 개선 작업 착수 전 `arxiv.org/abs/<id>` 응답 코드부터 확인할 것. 다행히 에이전트가 스스로 원논문(코드가 실제 인용 중인 2606.10949)으로 우회 검증해서 조사 자체는 무산되지 않았음 — "이 논문 못 찾겠다"에서 멈추지 말고 "그럼 실제로 참조된 원본이 뭔가"로 한 단계 더 파고드는 게 유용했음. |
| 2026-07-02 | 사이코팬시 필터 길이 게이트의 함정 | "80자 미만만 차단" 같은 길이 기반 휴리스틱은 공격/실패 유형이 짧은 문구에 국한된다는 암묵적 가정을 깔고 있음 — 실제 논문(2606.10949)이 측정한 위험은 정반대로 "길고 확신에 찬 응답 안에 숨은 오류 동조"였음. 길이 대신 "정정/반박 신호의 유무"로 판단 기준을 바꾸니 실제 실패 유형을 잡음. 휴리스틱 설계 시 "이 필터가 막으려는 실제 사례가 뭐였지"를 원논문에서 재확인할 것 — 초기 구현 당시의 가정이 논문 취지와 어긋나 있을 수 있음. |
| 2026-06-30 | fetch_fundamentals KR 자동갱신 wrapper | plist에서 단일 universe 실행 → 여러 universe 실행 전환 시 `run_fetch_fundamentals.sh` wrapper 패턴 사용. plist는 wrapper만 참조, 내부 로직은 sh에서 관리. |
| 2026-06-30 | fetch_fundamentals plist KR 미반영 | plist는 `nasdaq1000`만 실행. KR 유니버스(kospi200/kosdaq150) 추가했으나 plist 미갱신 → 토요일 자동 실행 시 KR 재무 미갱신. KR 재무는 수동 실행 필요. 향후 plist 업데이트 또는 KR 전용 plist 신설 과제. |
| 2026-06-30 | 코인 콜백 4-part 파싱 | `coin_all:{symbol}` → `coin_all:{symbol}:{ts_key}:{screener_key}` 로 변경. 뒤로가기 연결 위해 ts_key + screener_key 필요. 기존 2-part 파싱 코드가 있으면 split 개수 체크 추가 필수. |
| 2026-06-30 | date_str CSV glob 매칭 | `date_str` 형식 `%Y%m%d`는 여러 타임스탬프 충돌 가능 → `%Y%m%d_%H%M%S` 로 변경해야 특정 스캔 시각의 CSV를 정확히 glob 매칭. 형식 변경 시 텔레그램 콜백 파싱쪽(`_handle_mjstock_scan_list`)도 동일 형식 사용하는지 함께 확인. |
| 2026-06-30 | 코인 버튼 레이블 UX | Coin 스캔 결과 버튼 레이블 `(N종)` 만으로는 "클릭하면 무슨 일이 생기는지" 불명확. `검색(N종)` 접미로 동작을 명시하는 것이 모바일 UX 기준. 버튼 레이블은 항상 동사/동작 포함 여부 검토. |
| 2026-06-30 | Streamlit 블로킹 | `while proc.poll() is None: time.sleep(1)` 패턴은 Streamlit 전체를 블로킹 → 스캔 중 탭 전환 불가. `session_state` 기반 polling + `st.rerun()` 패턴으로 교체해야 첫 번째 검색기 완료 직후 차트탭 접근 가능. Streamlit에서 서브프로세스 대기는 항상 비동기 방식. |
| 2026-06-30 | Telegram InlineKeyboard | REST API에서 `reply_markup`을 JSON으로 전달. `mjstock_scan_list:{key}:{ts}` 형식 callback_data로 스캔 결과 → 종목 목록 → 차트 → Back 드릴다운 UX 구현 가능. 버튼 레이블은 `{검색기명}(N종)` 형식이 모바일 가독성 최적. |
| 2026-06-30 | mjstock 콜백 라우팅 | `mjstock_scan_list:` prefix는 `^mjstock[_:]` 패턴에 매칭 → `callback_mjstock()` 자동 라우팅. 신규 `mjstock_*` prefix 추가 시 별도 핸들러 등록 불필요, `callback_mjstock()` 내부 분기만 추가. `mjstock_chart:` 4-part 파싱(ticker/screener_key/date_str)도 동일 라우터에서 처리. |
| 2026-06-30 | macOS 스케줄러 | macOS에서 crontab은 Full Disk Access 제한으로 Claude Code 셸에서 타임아웃 발생 → launchd plist가 macOS 표준 스케줄러 대안. `~/Library/LaunchAgents/` 에 plist 작성 후 `launchctl load` 로 등록. 신규 배치 스크립트 스케줄링은 crontab 대신 launchd plist 사용. |
| 2026-06-30 | Streamlit 차트 인라인 표시 | 차트 외부 열기(`subprocess.Popen(["open", chart_path])`)는 Streamlit UI 내부에 표시되지 않음. `st.components.v1.html(f.read(), height=1200, scrolling=True)` 패턴이 인라인 표시 정답. 외부 앱 열기 방식은 Streamlit 웹 UI에서 사용자 경험 단절 발생. |
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
| 2026-07-04 | 동명 문서 삭제 전 계층구조 확인 | `Scripts/HERMES.md`·`Scripts/modules/HERMES.md`·`wiki/00_Meta/HERMES.md` 3개 동명 파일 발견 시 "중복"으로 단정하지 않고 `hermes_context_builder.py`의 `context_files = ["HERMES.md", "README.md"]` 계층 수집 로직부터 확인 — 폴더별 HERMES.md는 각기 다른 스코프 설명이 정상 설계. 실제 중복(vault 사본, 봇이 안 읽음, 구버전)만 삭제. 동명 문서 정리 요청 시 항상 로딩 코드 먼저 grep할 것. |
| 2026-07-04 | 평문 시크릿 파일은 삭제 전 실사용처 대조 | `Deepseek_API_Keys.md`의 4개 키 중 1개만 `.env`에 있었고 나머지 3개(가족 계정)는 그 문서가 유일 저장소였음 — "정리 대상"으로 보였지만 삭제하면 복구 불가능한 데이터 파괴였음. 시크릿/키 파일 삭제 지시 시 grep으로 각 값이 다른 곳에도 있는지 먼저 대조하고, 유일 저장소인 값이 있으면 삭제 대신 사용자에게 판단 요청. |
| 2026-07-04 | 로그 경로 이전 시 스크립트 내부 하드코딩 확인 | plist의 StandardOutPath만 바꾸면 될 줄 알았으나 `fswatch-indexer.sh:19`가 `LOGFILE` 변수를 자체 하드코딩하고 있어 plist와 스크립트 양쪽 다 고쳐야 했음. launchd 서비스 로그 경로 변경 시 실행 스크립트 자체에도 로그 경로 하드코딩이 있는지 항상 먼저 grep할 것. |
| 2026-07-04 | launchctl bootstrap 1회 실패는 즉시 재시도 | `com.hermes.stockbot` bootout 직후 bootstrap이 `Input/output error`로 실패 — 재시도 없이 포기했으면 봇이 다운된 채로 방치될 뻔했음. bootout 직후 즉시 bootstrap이 일시적으로 실패하는 경우가 있으므로, 실패 시 `launchctl print`로 깊이 파기 전에 먼저 1회 재시도. 재시도 성공 여부와 무관하게 반드시 pgrep으로 최종 생존 확인. |
| 2026-07-04 | 봇 토큰의 숫자 ID만 노출은 낮은 위험 | 텔레그램 봇 토큰은 `{숫자ID}:{시크릿문자열}` 구조 — 앞의 숫자 ID만 문서 프로즈에 노출되고 콜론 뒤 시크릿이 없으면 API 호출 자체가 불가능해 실질 위험은 낮음. "토큰 노출" 우려 시 전체 문자열(콜론+시크릿 포함)이 있는지부터 구분해서 심각도 판단할 것 — 숫자ID만이면 낮음, 전체 문자열이면 즉시 재발급 필요. |
| 2026-07-04 | "동일 복사본" 판단은 시간 지나면 재검증 | 이전 세션에서 `future_screeners/`의 3개 파일이 `screener/` 원본과 "완전 동일"이라 진단했는데, 실행 시점엔 그중 2개가 1줄 차이(pandas index 버그 수정)로 이미 갈라져 있었음 — 다행히 구버전 쪽이 죽은 파일이라 삭제는 맞았지만, diff 재확인 없이 예전 진단만 믿고 지웠으면 사일런트하게 최신 수정을 놓칠 뻔했음. 과거 진단에서 "중복/동일"이라 기록된 파일도 실제 삭제 직전엔 반드시 `diff` 재실행할 것. |
| 2026-07-04 | .env에 값 넣어도 코드가 다른 변수명을 찾으면 무용 | `Coin/run_scan_coin.py`/`auto_scan_coin.py`가 `os.environ.get("TELEGRAM_TOKEN")`/`"TELEGRAM_CHAT_ID"`를 참조했는데 프로젝트 표준은 `TELEGRAM_BOT_TOKEN`/`TELEGRAM_ALLOWED_USERS` — 게다가 `load_dotenv()` 호출 자체가 없어 `.env` 파일이 있어도 안 읽힘. "토큰을 .env로 옮겼다"고 끝내지 말고, 실제로 그 변수명 그대로 코드가 조회하는지 + dotenv 로드 호출이 있는지 둘 다 확인할 것. |

---

## 📌 현재 진행 중인 작업

### 🔄 진행 중 — MJstock 장중 검색기 5종 0건 지속 수정 후 관찰 대기 (BUG-MJS-030, 2026-07-11)
- shooting/chuddoli/samdoli/nongsa_danta/pochak(US) + samdoli_kr/nongsa_danta_kr "0건 지속" 원인 3종(pochak 배선 누락, 30분봉 120봉 페이지네이션 한계, RVOL 임계값 미스매치) 진단·수정 완료. 통합검증(`auto_scan_intraday.py`)에서 한국 12/12 검색기 성공, 미국 shooting/chuddoli 1~3개 신호 확인.
- **미해결**: samdoli의 6개 게이트 동시 AND 체인은 수정 후에도 30종목 샘플에서 0건 — confluence 전략 설계 특성으로 추정되나 버그 아닌지 며칠 더 관찰 필요.
- **미커밋**: `run_scan.py`/`data_loader.py`/`screen_samdoli_us.py`/`screen_samdoli_kr.py`/`screen_nongsa_danta_us.py`/`screen_nongsa_danta_kr.py` 전부 워킹트리 uncommitted.
- **다음 세션 할 일**: 07-12~07-14 `logs/scan_intraday_us.log`·`logs/scan_intraday_kr.log`로 samdoli/nongsa_danta 실제 신호 발생 여부 확인 → MJ님과 커밋 여부 결정.
- 상세: 05번(2026-07-11 항목) + 06번 BUG-MJS-030 참조

### ✅ 완료 — 매수→매도 시그널 추적 시스템 fd 고갈 복구 (BUG-MJS-029, 2026-07-08)
- `screener/batch_fill_returns.py`가 fd 고갈로 매일 크래시 → `signal_tracker.update_positions()` 미도달 → `tracker/signal_log.csv` 전량 status=active로 방치돼 있던 것 발견·수정
- `run_scan.py`(07-07 적용)와 동일 `resource.setrlimit` fix 이식, 실행 검증(3,071건 갱신, `last_checked_date` 0→2,056건, 매도신호 49건 감지)
- **미결정**: 정지 기간(6/29~7/7) 코호트의 circle_date 소급 재계산 여부 — MJ님 결정 대기, 미착수
- 상세: 05번(2026-07-08 (2) 항목) + 06번 BUG-MJS-029 참조

### ✅ 완료 — MJstock/MJcoin 텔레그램 인라인 버튼 네비게이션 왕복경로 버그 8종 수정 (2026-07-03/04)
- `screener/send_scan_result.py`(수동 발송)를 프로덕션 방식(`mjstock_scan_list:` 콜백)과 통일하는 작업 중 잠복 버그 6개(BUG-MJS-015~019, BUG-COIN-001) 발견 — "검색기 2개 이상 조합+뒤로가기+KR종목+에러상황" 왕복 테스트가 처음이라 드러남
- 잠복 버그: 뒤로가기 버튼 소실(date_str 정확일치 매칭), KR 종목코드 앞자리 0 소실(dtype 미지정), 버튼 표시개수↔실제 목록개수 불일치, 차트 조회 subprocess 동기호출로 콜백 타임아웃, 에러/빈결과 화면 키보드 소실("막다른 화면"), 코인 6검색기 화면 왕복 시 버튼 소실
- Claude 자기귀책 회귀 2건: 시간창(±30분) 근사 매칭 도입 → 무관한 검색기 혼입(BUG-MJS-020), batch_id 15자 타임스탬프 → 콜백데이터 64바이트 초과로 무반응(BUG-MJS-021)
- 최종 설계: 배치 매니페스트(`results/_batch/{batch_id}.json`, 8자 hex id) 방식으로 정확한 검색기 집합 복원
- 재발방지 도구 신규: `Mjauto/Scripts/test_mjstock_navigation.py` — mock(FakeQuery) 기반 왕복경로 자동 회귀 테스트(콜백데이터 64바이트 검증 포함)
- 최종 검증: 사용자 텔레그램 실클릭 확인 완료, 프로덕션 auto_scan_morning.py 25/25 검색기 정상 완료 확인
- 상세: 06번 BUG-MJS-015~021 + BUG-COIN-001 참조

### ✅ 완료 — `modules/code_graph.py` 신규 (경량 코드베이스 지식그래프) (2026-07-03)
- 외부 MCP 도구(`codebase-memory-mcp`) 대안 — `~/Applications/` 밖 캐시 경로 문제 + 158개 언어 과스펙 판단 후 자체 구현
- Python 표준 `ast`+`sqlite3`만 사용(신규 의존성 0개), MCP 아닌 CLI 스크립트, 인덱스는 `Scripts/.hermes_code_graph.db`
- 168개 파일 0.25초 인덱싱, `find_callers`/`find_importers` 결과가 수동 grep과 일치 확인
- **완전 수동 트리거** — 코드 변경 후 `--rebuild` 직접 실행해야 함, 자동 갱신 없음
- 사용법: `python3 modules/code_graph.py --rebuild|--callers 함수명|--importers 모듈명|--file 경로`

### ✅ 완료 — MJstock 시그널 생애주기 추적 시스템 버그 3종 수정 + 종료 조건 재설계 (2026-07-03)
- MJ님과 20개 검색기(US 10 + KR 10) 전수 조사 — 대부분 지속형 필터, 반전 감지는 `signals_farming.py` ★신호 레이어 전담 구조 확인. 조사 중 `signal_tracker.py`/`signal_log.csv`의 실질 고장 발견
- **버그 1**(`run_scan.py`): `_signal_map`이 "BUY_"로 시작하는 컬럼을 찾았으나 실제론 `has_buy_signal`/`buy_signal_type` 컬럼 사용 → 신호 매칭 2242건 중 2241건 실패("SCAN_PASS" 플레이스홀더만 기록). 컬럼 직접 참조로 수정
- **버그 2**(`signal_tracker.py` `record_scan()`): 재스캔 미매칭만으로 근거 없이 "exited" 처리 → 2242건 중 1617건(72%) 오판정. 해당 블록 삭제, 기존 1617건 "active"로 마이그레이션
- **버그 3**(코드 결함 아님, 재확인): `update_returns()`는 크론에 이미 연결돼 있었으나 데이터 축적 시작이 최근(6/28~)이라 10일 경과 행이 아직 없어 미실행 — 스케줄 문제로 오인했다가 정정
- **설계 변경**: 고정 10/20/30일 창 → 이벤트 기반 즉시 종료(`update_positions()` 신설). SELL_CONFIRMED(매도신호+3거래일 후 -2%↓)/SELL_FALSE(매도신호+반등재돌파)/TRAILING_GIVEBACK(MFE 대비 -3%p 되돌림, 고점 2%↑ 시만)/TIMEOUT(60거래일). +5% 도달은 종료조건 아닌 이정표(`reached_5pct_date`)로만 기록
- 문서 3종 갱신: `docs/korean_original_formulas.html`, `docs/quant_logic_analysis.html`(2곳), `docs/signals_entry_points.html`(20종 분류표)
- 테스트: mock으로 4개 분기 개별 검증 + py_compile 통과. **실 라이브 검증 미실시** — 오늘 17:30 크론이 첫 실행
- **미결정**: 하락 손절 기준(-10% 등 강제 종료 여부) — 현재 타임아웃(60거래일)까지 보유하는 기본값. MJ님 미정
- 상세: 05번(변경이력) + 06번 BUG-MJS-011/BUG-MJS-012 참조

### 🔄 초기화 — MJstock `experiments/` 삭제 + 문서 정리 (2026-07-03)
- MJ님이 다른 세션에서 `experiments/`(백테스트 엔진, 789종목 검증 완료 상태였음) 삭제 지시 → 확인 완료, 본체 영향 없음
- `MJstock_사용설명서.html` v1.8 상세 섹션 → "초기화됨" 짧은 안내로 교체, `loop_review/README.md` 3번 항목 상태 되돌림
- **재착수 여부는 MJ님 지시 대기 중**


### 🚨 미해결(추정 해소) — 텔레그램 SNI 차단으로 Hermes1 무응답 (2026-06-17)
> **2026-07-04 갱신**: 이번 세션에서 hermes_stock_bot·Hermes1 봇 응답 정상 확인(사용자 실클릭 확인 포함) — 네트워크 차단은 현재 해소된 것으로 보이나, ISP 차단이므로 재발 가능. 재발 시 아래 진단법 그대로 사용.
- **진짜 원인**: 코드/프로세스 문제 아님. **ISP가 api.telegram.org에 대한 TLS SNI 차단** 중 — 일반 인터넷(Google 등)은 정상, 텔레그램 IP 일부는 TCP는 열려도 TLS 핸드셰이크에서 멈춤(`curl` `000`). 그동안의 "행"·"크래시 루프"·"Conflict" 증상은 전부 이 네트워크 차단으로 인한 재연결 시도의 부작용이었음
- **확인 방법**: `curl --max-time 6 https://api.telegram.org` → `000` 이면 차단 상태. `curl https://www.google.com`은 정상(`200`) — 도메인 특정 차단 확인 포인트
- **현재 이 Mac에 활성 VPN 없음**
- **해결책**: VPN 연결 또는 다른 네트워크(핫스팟) 전환, 혹은 ISP 차단이 풀릴 때까지 대기. 봇 프로세스 자체는 정상 대기 상태이므로 네트워크만 풀리면 자동 복구됨
- **부수 효과**: 디버깅 중 `hermes_local.py`의 `except Exception: pass`(폴링 종료 시 원인 완전 삼킴)를 발견 → `logger.error(f"[Polling 종료 원인] ...")`로 수정해 향후 같은 문제 빠르게 진단 가능해짐

### 🚨 미해결 — KIS API(openapi.koreainvestment.com) 접속 차단 (2026-07-04 신규 발견)
- **증상**: `/mjstock nas`(나스닥 상위500 일괄 스캔) 실행 시 우량주농사·주도주단기 검색기 둘 다 KIS API 개별 종목 조회 단계에서 무한 대기. `sample`로 스택 확인 결과 `sock_connect→internal_select`에서 멈춤(HTTP 요청 이전, TCP 핸드셰이크 단계) — `lsof`로 `210.107.75.32:https`(KIS 서버) 연결이 `SYN_SENT` 상태로 굳어있음 확인
- **타임라인으로 신규 발생 확인**: 2026-07-03 22:30~23:54 장중 자동스캔은 KIS로 10/10 검색기 전부 정상 성공(검색기당 7~9분 소요) — **어젯밤까진 멀쩡했고 그 이후 오늘 사이에 새로 발생**. 텔레그램 SNI 차단(6/17)과 같은 유형이지만 별개 사건(도메인이 다름, 발생일도 다름)
- **rate-limit(호출과다)이 아니라 접속 차단으로 판단한 근거**: rate-limit이면 TCP 연결은 성공한 뒤 서버가 에러 응답(KIS `EGW00201` 등)을 줬어야 함. 지금은 TCP 연결 자체가 안 되고 있어 요청이 서버에 도달조차 못 함 — 두 검색기(우량주농사/주도주단기)에서 동일 IP·동일 증상 재현되어 일회성 아님을 확인
- **확인 방법**: `curl --max-time 8 https://openapi.koreainvestment.com` → 타임아웃이면 차단 상태. `curl https://www.google.com`은 정상 — 도메인 특정 차단 확인 포인트. `lsof -a -p <PID> -i`로 `SYN_SENT` 여부 확인
- **해결책**: VPN 또는 다른 네트워크(핫스팟) 전환, 혹은 ISP 차단이 풀릴 때까지 대기(MJ님 결정: 나중에 재시도)
- **관련 코드는 문제 없음**: `/mjstock nas`/`kos`(2026-07-04 신규), `run_scan.py --exclude-screen` 전부 정상 동작 확인 — 네트워크만 풀리면 그대로 작동함

## 🔴 현재 미해결 / 모니터링 필요
- ⚠️ `wiki_auto_stamper.py` fswatch 연동 미설정 (수동 실행만 가능)
- ⚠️ `meta_updater.py` 비활성화 상태 유지 중 (필요시 재활성화)
- 🔄 **핸들러 분할 확정 보류**: `handlers/_stock_mjstock.py` 분할(→ `_stock_mjstock_extra.py`, 2026-07-04) 아직 git commit 안 함 — MJ님이 며칠간 직접 텔레그램 테스트 후 확정/롤백 결정 예정. 스케줄 작업이 2026-07-07 11:00에 자동으로 확정 여부 재문의.


---

🔗 **관련 문서**
- 00_Meta_지도 — 메타 폴더 내비게이션
- 05_시스템 상태.md — 전체 변경 이력 (2026-06-23 이전 완료 작업 아카이브 포함)
- 02_스크립트 정보.md — 모듈 및 명령어 가이드
- 06_에이전트_오류_및_재발방지_보고서.md — 버그 재발방지 상세 기록

---
*최종 업데이트: 2026-07-11 22:35*
