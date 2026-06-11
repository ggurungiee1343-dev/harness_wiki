---
tags: [scanned, 50_Invest, stock-analysis, swing-trading, investment, yfinance, claude-code, webull, automation]
description: "MJ 주식 분석 시스템은 일봉 기반 스윙 트레이딩을 목표로 고확신 종목을 선별한다. yfinance와 SQLite를 활용해 데이터 수집·지표 계산을 자동화하고, Claude Code와 Webull을 연동해 결과를 검증한다. 최종 신호는 사람(MJ)이 확인 후 수동 주문으로 진행한다."
---

# MJ 주식 분석 시스템 — V_FINAL 전략 완전 가이드

> 최종 업데이트: 2026-06-10 (v1.4 — ADX 추세 강도 ALPHA_SCORE 반영 + 4티어 스캔)
> 작성: Claude Code 세션 (V1.8→V2.0→V2.3→V3.0 전략 병합 + 시스템 구축)

### 변경 이력
| 버전 | 날짜 | 내용 |
|:---:|---|---|
| v1.4 | 2026-06-10 | **ADX 점수 추가** — ADX≥60:+0.5 / ADX≥40:+0.25. **4티어 스캔** — /scan buy/watch/strong/sepa |
| v1.3 | 2026-06-10 | **5가지 전략 개선** — REVERSAL 부분점수화, 펀더멘털 필터, 실적발표 필터, 트레일링 스탑, 섹터 RS 보너스 |
| v1.2 | 2026-06-10 | **전략 완화** — IS_TIGHT 필수게이트 제거, IS_LEADER 임계값 0.97→0.90, SCORE 4.5→3.0 |
| v1.1 | 2026-06-10 | `/scan sepa` 서브커맨드 추가. `stock_scanner.py`에 `sepa_list` 필드 추가 |
| v1.0 | 2026-06-10 | 최초 구축. 텔레그램 7개 명령어, MCP 서버, V_FINAL 전략 완성 |

---

## 1. 시스템 개요

### 설계 철학
- **초단타 NO** — 일봉 기준 스윙 트레이딩 (며칠~몇 주)
- **고확신 종목만** — 최대 8.5점 중 3.0점 이상 + 5레이어 다중 조건 통과
- **15분 지연 OK** — yfinance 일봉, 장 마감 후 스캔이 오히려 정확
- **자동 주문 절대 없음** — 신호 제시 → 사람(MJ) 확인 → 수동 주문

### 사용 패턴 (2가지)

```
출장 중 (어디서나)          집 데스크탑
     텔레그램                Claude Code + Webull
         ↓                         ↓
  /scan → 후보 발굴        MCP → V_FINAL 수치 분석
  /stock CRWD → 상세       Webull 차트 → 시각 확인
  /result → 결과 기록      두 정보 교차 검증 → 판단
```

---

## 2. 구성 파일 목록

### Scripts/modules/ (4개 핵심 모듈)

| 파일 | 기능 | 비고 |
|---|---|---|
| `stock_fetcher.py` | yfinance 데이터 수집, SQLite DB, 유니버스 관리, **펀더멘털 캐시**, **트레일링 스탑** | v1.3: get_fundamentals / update_trailing_stop 추가 |
| `stock_indicators.py` | 45개 지표 계산 (순수 pandas/numpy) | pandas-ta 미사용 |
| `stock_signal_engine.py` | V_FINAL 신호 엔진 (**5레이어** 판단 구조) | v1.3: REVERSAL 분리, 펀더멘털/섹터/트레일링 적용 |
| `stock_scanner.py` | NASDAQ 유니버스 스캔 오케스트레이터, **섹터 RS 순위** | v1.3: _get_top_sectors 추가 |

### Scripts/handlers/

| 파일 | 기능 |
|---|---|
| `_stock.py` | 텔레그램 명령어 7개 + 차트 사진 분석 (~500줄) |

### Scripts/ (루트)

| 파일 | 기능 |
|---|---|
| `stock_mcp_server.py` | Claude Code 전용 MCP 서버 (6개 도구) |

### 데이터베이스

```
Scripts/data/stock_cache.db  (SQLite)
├── positions           — 열린 포지션 (entry/stop/shares/max_price/trailing_stop)
├── watchlist           — 관심종목
├── scan_log            — 스캔 이력
├── trade_results       — 매매 결과 피드백 (개선용)
└── fundamentals_cache  — EPS/매출/이익률/실적발표일/섹터 (7일 TTL) [v1.3 신규]
```

---

## 3. V_FINAL 전략 구조

### 전략 계보
```
V1.8 (EMA 기반 기초)
  + V2.0 (EMA200 추세 강화)
  + V2.3 (SEPA 트렌드 템플릿 + AI Extreme)
  + V3.0 (Alpha Master — IS_TIGHT, IS_LEADER, ALPHA_SCORE)
  = V_FINAL (병합 + MJ 수정 + 개선)
```

### 5레이어 판단 구조 (v1.3 최신 기준)

```
┌──────────────────────────────────────────────────────────────────┐
│ Layer 1: SEPA 트렌드 템플릿  ← 필수 게이트 (Stage 2 확인)       │
│                                                                  │
│   ① 이평선 정배열: 종가 > EMA50 > EMA150 > EMA200               │
│   ② EMA200 우상향: EMA200_현재 > EMA200[20일전]                  │
│   ③ 52주 범위:     종가 ≥ 52W저가×1.30  (저가 탈출)             │
│                   종가 ≥ 52W고가×0.75  (고점 근처 위치)          │
│                                                                  │
│   → 3개 모두 True = SEPA_FULL  (Layer 1 통과)                   │
├──────────────────────────────────────────────────────────────────┤
│ Layer 2A: 기관 품질 지표  ← 일부 필수                            │
│                                                                  │
│   IS_TIGHT  ★점수전용(+1.5)★  ← 필수아님                        │
│     조건: ATR10 < ATR30 × 0.85                                  │
│           AND BB_WIDTH < BB_WIDTH_MA50 × 0.80                   │
│     의미: 기관 물량 조용히 응축 중 → 폭발 직전                   │
│                                                                  │
│   IS_LEADER  ← 필수 게이트                                       │
│     조건: RS_LINE ≥ RS_52W_HIGH × 0.90   [v1.2: 0.97→0.90]     │
│           AND RS_LINE_MA50 > RS_LINE_MA50[20일전]                │
│     의미: NASDAQ 대비 상대강도 주도주 여부                         │
│                                                                  │
│   FRESH_TREND  ★점수전용(+1.0)★  ← 필수아님                     │
│     조건: EMA200 > EMA200[60일전]                                │
│           AND EMA200 > EMA200[120일전]                           │
│     의미: 장기 추세 신선도 (이미 너무 오래된 추세 제외)            │
│                                                                  │
│   SAFE_MARGIN  ← 필수 게이트                                     │
│     조건: 종가 < 3년저가 × 8.0                                   │
│     의미: 8배 이상 폭등 버블 차단                                  │
├──────────────────────────────────────────────────────────────────┤
│ Layer 2B: 펀더멘털 + 실적발표 필터  ← 필수 게이트 [v1.3 신규]   │
│                                                                  │
│   FUNDAMENTAL_OK                                                 │
│     조건: EPS 성장률 > 15%    (earningsGrowth)                   │
│           AND 매출 성장률 > 10% (revenueGrowth)                  │
│           AND 순이익률 > 0%     (profitMargins)                  │
│     예외: 데이터 없으면 통과 (yfinance 미제공 종목 보호)           │
│     캐시: SQLite 7일 TTL (fundamentals_cache 테이블)             │
│                                                                  │
│   EARNINGS_SAFE                                                  │
│     조건: 실적발표까지 > 10일  (yfinance .calendar)              │
│     이유: 실적 발표 전후 급등락 리스크 제거                        │
│           이미 발표 완료된 경우(days<0)는 OK                      │
├──────────────────────────────────────────────────────────────────┤
│ Layer 3: ALPHA_SCORE 타이밍 점수  (최대 8.5점) [v1.3 업데이트]  │
│                                                                  │
│  ① IS_TIGHT      +1.5   ATR10/ATR30 < 0.85 + BB_WIDTH압축      │
│  ② IS_LEADER     +1.5   RS_LINE ≥ 52W_HIGH×0.90 + MA상승        │
│  ③ FRESH_TREND   +1.0   EMA200 > 60일전 AND 120일전             │
│                                                                  │
│  ④ REVERSAL 부분점수 (v1.3) — 최대 1.5점:                       │
│     MACD_CROSS:  +0.75  MACD 골든크로스 (이전봉 이하→이번봉 돌파) │
│     EMA_CROSS:   +0.50  EMA3 또는 EMA15 상향 돌파               │
│     RSI_ZONE:    +0.25  RSI 45~68 + 종가 > VWAP50              │
│     ※ 이전(v1.2): 5조건 동시 충족 → 1.5(거의 0점 → 분리 개선)   │
│                                                                  │
│  ⑤ VOLUME        +1.5   달러거래대금 > MA20×1.8 + 갭업≥0.5%     │
│                  +0.75  달러거래대금 > MA20×1.8 (갭업 없음)       │
│  ⑥ OBV           +0.5   OBV > OBV_EMA20                        │
│  ⑦ SECTOR_BONUS  +0.5   상위 4개 섹터 소속 (섹터ETF RS 기준)    │
│  ⑧ ADX_BONUS     +0.5   ADX ≥ 60 (극강 추세)           [v1.4]  │
│                  +0.25   ADX ≥ 40 (강한 추세)                   │
│     ADX 기준: <20 횡보 / 20~40 보통 / 40~60 강함 / ≥60 극강     │
│                                                                  │
│   → 합계 = ALPHA_SCORE  (최대 9.0점, v1.4)                      │
├──────────────────────────────────────────────────────────────────┤
│ Layer 4: FINAL_BUY — 최종 매수 신호  (v1.3)                     │
│                                                                  │
│   SEPA_FULL        ← Layer 1 통과                               │
│   AND IS_LEADER    ← 필수 (상대강도 주도주)                       │
│   AND SAFE_MARGIN  ← 필수 (버블 과열 차단)                       │
│   AND FUNDAMENTAL_OK ← 필수 (EPS/매출/흑자)  [v1.3 신규]       │
│   AND EARNINGS_SAFE  ← 필수 (발표 10일전 제외)[v1.3 신규]       │
│   AND ALPHA_SCORE ≥ 3.0  (v1.2: 4.5→3.0)                      │
│                                                                  │
│   ※ IS_TIGHT: 필수 제외 → 점수(+1.5)만 기여 [v1.2 결정]        │
│     이유: 변동장에서 TIGHT 구조적 0% → 전체 신호 전멸 방지       │
├──────────────────────────────────────────────────────────────────┤
│ Layer 5: 매도 조건 — 5개 독립 게이트 + 트레일링 스탑  [v1.3]   │
│                                                                  │
│   trend_ema50:  종가 < EMA50×0.99        (추세 훼손)            │
│   profit_rsi:   RSI > 80                  (과매수 익절)          │
│   profit_bb:    종가 > BB상단×1.05        (과열 익절)            │
│   chop_vol:     CHOP>65 AND 거래량<MA20×0.8 (모멘텀 소멸)       │
│   macd_dead:    MACD 데드크로스            (방향 전환)           │
│   trailing_stop: 종가 < 트레일링스탑가   [v1.3 신규]            │
│                                                                  │
│   트레일링 스탑 계산:                                             │
│     진입 후 매 스캔마다: max_price = max(max_price, 현재가)       │
│     trailing_stop = max_price - (진입가 - 원래손절가)            │
│     → 스탑은 위로만 이동 (한번 올린 스탑은 내리지 않음)           │
└──────────────────────────────────────────────────────────────────┘
```

### 전략 진화 이력 — 파라미터 변경 요약

> **v1.2** (2026-06-10) — 실데이터 진단: TIGHT=0%, LEADER 3종목 → 6종목으로 완화

| 파라미터 | v1.0 | v1.2 | v1.3 |
|---|:---:|:---:|:---:|
| IS_TIGHT 필수게이트 | ✅ | ❌ 제거 | ❌ (점수만) |
| IS_LEADER 임계값 | RS≥97% | RS≥90% | RS≥90% |
| ALPHA_SCORE 임계값 | ≥4.5 | ≥3.0 | ≥3.0 |
| 펀더멘털 필터 | ❌ | ❌ | ✅ 추가 |
| 실적발표 필터 | ❌ | ❌ | ✅ 추가 |
| REVERSAL 방식 | 5조건 일괄(1.5) | 5조건 일괄(1.5) | 3개 독립(최대1.5) |
| 섹터 RS 보너스 | ❌ | ❌ | +0.5 추가 |
| 트레일링 스탑 | ❌ | ❌ | ✅ ATR기반 |
| 최대 점수 | 7.5 | 7.5 | **8.5** |

> **수정 위치**: `Scripts/modules/stock_signal_engine.py`
> - IS_LEADER: `rs_52w_high * 0.90`
> - FINAL_BUY: `alpha_score >= 3.0`
> - 펀더멘털: `fundamentals` 파라미터로 전달
> - REVERSAL: `score["macd_cross"]`, `score["ema_cross"]`, `score["rsi_zone"]` 분리

### ALPHA_SCORE 점수 구성표 (v1.4)

```
구성요소         최대점수   조건
──────────────────────────────────────────────────────────
IS_TIGHT          +1.5    ATR10/ATR30<0.85 AND BB압축<0.80
IS_LEADER         +1.5    RS_LINE≥52W고점×0.90 AND MA상승
FRESH_TREND       +1.0    EMA200 > 60d AND 120d 이전 수준
MACD_CROSS        +0.75   MACD 골든크로스 발생
EMA_CROSS         +0.50   EMA3 OR EMA15 상향 돌파
RSI_ZONE          +0.25   RSI 45~68 + 종가>VWAP50
VOLUME            +1.5    달러거래대금>MA20×1.8 + 갭업≥0.5%
                  +0.75   달러거래대금>MA20×1.8만 (갭없음)
OBV               +0.5    OBV > OBV_EMA20
SECTOR_BONUS      +0.5    섹터ETF RS 상위 4개 섹터 소속
ADX_BONUS  [v1.4] +0.5    ADX ≥ 60 (극강 추세)
                  +0.25   ADX ≥ 40 (강한 추세)
──────────────────────────────────────────────────────────
최대 합계          9.0점  (v1.4: 8.5→9.0)
매수 최솟값        3.0점  ← LEADER+FRESH+OBV 기본조합
```

> **ADX란?** Average Directional Index — 추세의 *방향*이 아닌 *강도*를 측정
> - ADX < 20: 추세 없음 (횡보, 노이즈)
> - ADX 20~40: 보통 추세 (진입 준비)
> - ADX 40~60: 강한 추세 (모멘텀 살아있음)
> - ADX ≥ 60: 극강 추세 (진입 후 지속 확률 높음) ← RDW 71.8 해당

### 실전 점수 시나리오 (v1.4)

```
9.0점  — 완벽 셋업 (TIGHT+LEADER+FRESH+MACD+EMA+RSI+VOLUME갭업+OBV+섹터+ADX극강)
7.5점  — TIGHT+LEADER+FRESH+MACD+VOLUME+OBV+ADX강
5.5점  — LEADER+FRESH+MACD+EMA+VOLUME+OBV+섹터
4.5점  — LEADER+FRESH+MACD+EMA+RSI+OBV
3.5점  — LEADER+FRESH+OBV+거래량부분+섹터
3.0pt  — LEADER+FRESH+OBV  ← 매수 최솟값
2.7pt  — FRESH+OBV+ADX극강  (LEADER 미달 예: RDW 타입 → 🔵구조강함 티어)
2.5pt  — LEADER+OBV (FRESH 미충족)
```

### 4티어 스캔 결과 분류 (v1.4 신규)

```
/scan            → 4티어 요약 (각 티어 개수 + 상위 5개 미리보기)
/scan buy        → 🟢 Tier1: FINAL_BUY 전체
/scan watch      → 🟡 Tier2: SEPA+LEADER+점수≥2.0 (타이밍 대기)
/scan strong     → 🔵 Tier3: 정배열+EMA우상향+ADX≥40 (52W 미달이어도 포함)
/scan sepa       → ⬜ Tier4: SEPA 통과 전체
```

| 티어 | 조건 | 활용 |
|---|---|---|
| 🟢 매수 | FINAL_BUY | 지금 당장 진입 검토 |
| 🟡 대기 | SEPA+LEADER+점수≥2.0 | 알림 걸고 타이밍 기다림 |
| 🔵 구조강함 | 정배열+EMA우상향+**ADX≥40** | RDW타입 — 추세 강하지만 52W/LEADER 미달 |
| ⬜ SEPA | sepa_full=True | 전통적 SEPA 통과 참고 |

> Tier3 🔵는 FINAL_BUY가 아니므로 직접 진입보다는 **Webull 차트 확인 후 판단** 권장.
> 매수 신호 없는 날 `/scan strong`으로 RDW 같은 잠재 종목 발굴 가능.

### 3중 시장 필터 (스캔 전 선행 체크)
```
Gate 1: NASDAQ > EMA50        (추세 확인)
Gate 2: VIX < 28              (공포 지수)
Gate 3: 11개 섹터 중 6개 이상 EMA200 위 (시장 폭)

→ 3개 모두 통과해야 스캔 진행. 실패 시 "매매 보류"
```

### 포지션 사이징 (ATR 기반)
```
SHARES = (계좌금액 × 리스크%) ÷ (ATR14 × VIX_배수)

VIX_배수:
  VIX < 20  → 1.5배 (저변동, 작은 스탑)
  VIX < 25  → 2.0배 (중간)
  VIX ≥ 25  → 2.5배 (고변동, 큰 스탑)

기본값: 계좌 $100,000, 종목당 리스크 1%
```

### 매도 조건 (6개 독립 게이트, v1.3)
| 조건 | 수식 | 의미 |
|---|---|---|
| `trend_ema50` | 종가 < EMA50 × 0.99 | 추세 훼손 — 즉시 검토 |
| `profit_rsi` | RSI > 80 | 과매수 → 분할 익절 |
| `profit_bb` | 종가 > BB상단 × 1.05 | 과열 → 즉시 익절 |
| `chop_vol` | CHOP > 65 AND 거래량 < MA20×0.8 | 모멘텀 소멸 |
| `macd_dead` | MACD 골든 → 데드크로스 | 방향 전환 확인 |
| `trailing_stop` ⭐ | 종가 < 트레일링스탑가 | 고점 추적 손절 [v1.3] |

> **트레일링 스탑 공식**:
> - `max_price` = 진입 후 매 스캔마다 고점 갱신 (DB 저장)
> - `trailing_stop` = max_price − (진입가 − 원래 손절가)
> - 스탑은 **위로만** 이동 — 한번 올라간 스탑은 내리지 않음
> - 진입가=$100, 손절가=$96(ATR=4) → 고점$110 도달 시 트레일링=$106

---

### 명령어 동작 테스트 결과 (2026-06-10 v1.3)

| 명령어 | 테스트 결과 | 비고 |
|---|:---:|---|
| `/market` | ✅ | NASDAQ/VIX/섹터 정상 출력 |
| `/scan` | ✅ | SEPA목록 자동 포함, 이중개행 수정 |
| `/scan sepa` | ✅ | 전체 목록 페이지 분할 |
| `/scan AMAT` | ✅ | `/stock AMAT` 으로 자동 리다이렉트 |
| `/stock AMAT` | ✅ | 4레이어 분석 + 포지션 사이징 |
| `/watchlist add/rm/list` | ✅ | SQLite 정상 |
| `/positions` | ✅ | 열린 포지션 조회 |
| `/result` | ✅ | SQLite 기록 정상 |
| `/backtest` | ✅ | 승률/RR 통계 정상 |
| 차트 사진 전송 | ✅ | 핸들러 등록됨 (LLM 연결 시 작동) |
| MCP 서버 임포트 | ✅ | 6개 도구 정상 |

---

## 4. 텔레그램 명령어 상세 사용법

### `/market` — 시장 상태 확인
```
사용: /market
출력: NASDAQ / VIX / 11개 섹터 EMA200 위치
용도: 매매 시작 전 첫 번째로 확인

예시 결과:
  🌐 시장 필터 현황
  종합: ✅ 매매 가능
  ① NASDAQ 19,234  EMA50 18,900  ✅
  ② VIX 18.5  기준 <28  ✅
  ③ 섹터 브레드스 8/11  ✅
```

---

### `/scan` — NASDAQ 전체 스캔
```
사용: /scan
소요: 1~3분 (100종목 일괄 분석)
출력: 시장 필터 + 매수 후보 + SEPA 통과 상위 15개 (알파점수 내림차순)

예시 결과 (매수신호 있을 때):
  ✅ 스캔 완료  스캔 105종목 | SEPA통과 36개 | 매수신호 3개
  시장: NASDAQ ✅  VIX 18.5 ✅  섹터 8/11 ✅

  🟢 매수 신호 종목 (상위 10개)
  • CRWD  $619  6.5점 🔒🚀🌱
  • PANW  $251  5.5점 🔒🚀
  • PLTR  $28   4.8점 🔒

  📈 SEPA 통과 (매수조건 미달 33개, 상위 15개)
  • NVDA  $200  3.5pt  T:🔒 L:☐
  • MSFT  $420  3.0pt  T:☐  L:🚀
  ...

예시 결과 (매수신호 없을 때):
  ✅ 스캔 완료  스캔 105종목 | SEPA통과 36개 | 매수신호 0개

  📈 SEPA 통과 (매수조건 미달 36개, 상위 15개)
  • CRWD  $619  3.5pt  T:🔒 L:☐
  (+21개 더 있음 — /scan sepa 전체 확인)

용도: 매일 장 마감 후 실행 추천
      매수신호 없어도 SEPA 목록으로 관심종목 파악 가능
```

---

### `/scan sepa` — SEPA 통과 전체 목록 ⭐ 신규
```
사용: /scan sepa
소요: /scan과 동일 (1~3분, 같은 스캔 재활용)
출력: SEPA 통과 전체 종목 알파점수 순 (페이지 분할 자동)

예시 결과:
  ✅ 스캔 완료  스캔 105종목 | SEPA통과 36개 | 매수신호 0개

  📈 SEPA 통과 종목 36개 (알파점수 순)
  🟢 CRWD  $619  6.5점  🔒🚀🌱   ← 🟢=매수신호까지 통과
  ⬜ PANW  $251  3.5점  🔒🚀     ← ⬜=SEPA만 통과
  ⬜ NVDA  $200  3.0점  🔒
  ...

  🔒=TIGHT  🚀=LEADER  🌱=FRESH  🟢=매수신호

용도: 매수신호 0개일 때 SEPA 36개 전부 확인
      Layer 2~3 조건 아슬아슬하게 미달한 종목 발굴
      Webull에서 차트 확인할 후보 리스트 추출
```

---

### `/stock TICKER [계좌금액] [리스크비율]` — 단일 종목 상세 분석
```
사용 예:
  /stock NVDA              (기본값: $100,000 계좌, 1% 리스크)
  /stock CRWD 50000        ($50,000 계좌 기준 포지션 계산)
  /stock AAPL 100000 0.02  (2% 리스크)

출력:
  [Layer 1] SEPA: 정배열✅ EMA200우상향✅ 52W위치✅
  [Layer 2] TIGHT✅ LEADER✅ FRESH✅ SAFE✅
  [Layer 3] 점수: TIGHT1.5 LEADER1.5 FRESH1.0 REVERSAL0 VOLUME1.5 OBV0.5 = 6.0/7.5
  [포지션]  진입$619 손절$601 → 5주 / 투자금$3,095 / 리스크$90
  [지표]    RSI 58.2 | ADX 32.1 | CHOP 42.3 | 거래량비율 2.1x
  [매도경보] trend_ema50 (해당 없음)

용도: /scan 후보 중 관심 종목 깊이 확인
      Webull 차트와 교차 검증
```

---

### `/watchlist` — 관심종목 관리
```
/watchlist                → 목록 조회 (= /watchlist list)
/watchlist add CRWD       → 추가
/watchlist add CRWD SEPA진입예정  → 메모와 함께 추가
/watchlist rm CRWD        → 삭제
/watchlist scan           → 관심종목만 빠르게 스캔

용도: /scan에서 마음에 든 종목 임시 저장
      다음날 /watchlist scan으로 빠른 재확인
```

---

### `/positions` — 열린 포지션 확인
```
사용: /positions
출력: 보유 중인 포지션 목록 (진입가/손절가/수량/날짜)

참고: 이 시스템은 "주문 실행" 기능 없음
      실제 주문은 Webull에서 직접 → 이후 수동 기록 필요
      (현재 자동 연동 미구현)
```

---

### `/result` — 매매 결과 기록 ⭐ 핵심 기능
```
형식: /result TICKER 매수가 매도가 [수량] [메모]

사용 예:
  /result CRWD 580 635           (수량/메모 없이 수익률만)
  /result CRWD 580 635 5         (5주)
  /result CRWD 580 635 5 SEPA진입_목표가도달
  /result NVDA 200 185 10 손절_EMA50이탈

출력:
  🟢 CRWD 결과 기록 완료
  진입 $580.00 → 매도 $635.00
  수익률: +9.48% ($275)
  메모: SEPA진입_목표가도달

용도: 매매할 때마다 바로 기록
      데이터가 쌓여야 /backtest로 수식 개선 가능
```

---

### `/backtest` — 누적 성과 통계
```
사용: /backtest
출력:
  📊 V_FINAL 매매 성과 (12건)
  승률: 75.0% (9승 3패)
  평균 수익률: +8.3%
  평균 이익: +12.1% | 평균 손실: -5.8%
  리스크:리워드 = 1 : 2.09
  최고: CRWD +18.2%
  최악: NVDA -9.3%
  최근 5건: ...

용도: 월 1회 확인 → 수식 어디를 개선할지 근거 마련
      "LEADER 조건 없이도 잘 맞았나?" 같은 질문 검증
```

---

### 차트 사진 전송 — V_FINAL 기준 차트 분석
```
방법: Webull에서 차트 캡처 → 텔레그램에 사진 전송
      캡션에 종목명 추가 권장 (예: "CRWD 일봉")

출력: V_FINAL 기준 차트 분석
  - Stage 1/2/3/4 판별
  - SEPA 정배열 시각 확인
  - 볼린저밴드 압축(TIGHT) 여부
  - 거래량 패턴
  - 매수/관망/매도 종합 의견

용도: 지표(/stock)로 OK 나온 종목의 차트 패턴 최종 확인
      "지표 OK + 차트 패턴 OK" → 진입 확신
```

---

## 5. Claude Code MCP 서버 사용법

### 등록 상태
```bash
# 이미 등록 완료 (2026-06-10)
claude mcp list
# stock-scanner: python3 .../stock_mcp_server.py ✓ Connected
```

### Claude Code에서 사용 방법

**자연어로 바로 질문:**
```
"NVDA 지금 분석해줘"
→ MCP가 analyze_stock("NVDA") 자동 호출

"오늘 매수 후보 찾아줘"
→ MCP가 run_scan() 자동 호출 (1~3분)

"지금 시장 괜찮아?"
→ MCP가 market_status() 자동 호출

"CRWD 관심종목에 추가해줘"
→ MCP가 watchlist(action="add", symbol="CRWD") 호출

"CRWD 580에 사서 635에 팔았어, 5주"
→ MCP가 record_result() 자동 호출

"지금까지 성과 어때?"
→ MCP가 backtest_summary() 자동 호출
```

### MCP 도구 목록 (6개)
| 도구 | 파라미터 | 설명 |
|---|---|---|
| `analyze_stock` | symbol, account=100000, risk_pct=0.01 | 단일 종목 V_FINAL 분석 |
| `run_scan` | symbols=None, account=100000 | 전체/선택 유니버스 스캔 |
| `market_status` | (없음) | 3중 시장 필터 현황 |
| `record_result` | symbol, entry, exit, shares, notes | 매매 결과 기록 |
| `backtest_summary` | (없음) | 누적 성과 통계 |
| `watchlist` | action, symbol, notes | 관심종목 관리 |

### Hermes 봇과의 관계
```
Hermes 텔레그램 봇          MCP 서버
(hermes_local.py)          (stock_mcp_server.py)
       ↑                          ↑
  텔레그램 메시지 시만        Claude Code 대화 시만
  실행 (항상 켜짐)           실행 (온디맨드)

→ 완전히 독립된 프로세스
→ Hermes 성능에 0% 영향
→ 같은 SQLite DB 공유 (데이터 동기화)
```

---

## 6. Webull 연동 방법 (현재: 차트 분석만)

### 현재 구현된 방법
```
Webull 앱 (차트 시각화)
    ↓  스크린샷
텔레그램에 사진 전송  →  V_FINAL 차트 분석
    또는
Claude Code에 이미지 붙여넣기  →  MCP + 비전 교차 분석
```

### 추천 워크플로우 (집 데스크탑)
```
1. /scan 또는 Claude Code "후보 찾아줘"
   → V_FINAL 조건 통과 종목 목록

2. Webull에서 해당 종목 차트 열기
   → 눈으로 Stage 2 확인, 지지선 파악

3. Claude Code "CRWD 분석해줘" (MCP)
   → 수치 지표 확인

4. 차트 스크린샷 → Claude Code에 붙여넣기
   → "지표 OK + 차트 패턴 OK" 더블 확인

5. 확신 생기면 Webull에서 직접 주문
   → 주문 후 /result로 진입가 기록
```

### 미래 연동 옵션 (미구현)
- **Webull API**: 실시간 데이터 소스 (현재 yfinance로 충분)
- **자동 주문**: 설계상 금지 (신호 → 사람 확인 → 수동 주문 원칙)

---

## 7. 개선 루프 (수식 발전 방법)

```
① 장 마감 후 /scan (또는 Claude Code "후보 찾아줘")
   ↓
② Webull에서 차트 확인 + /stock TICKER 지표 확인
   ↓
③ 마음에 들면 /watchlist add TICKER
   ↓
④ 실제 매수 (Webull에서 직접)
   ↓
⑤ 매도 후 즉시 → /result TICKER 매수가 매도가 수량 메모
   ↓
⑥ 데이터 10~20건 쌓이면 /backtest
   ↓
⑦ "LEADER 없어도 이겼다면?" → Claude Code에 물어보기
   "ALPHA_SCORE 4.0으로 낮춰도 되나?" 등
   ↓
⑧ V_FINAL 파라미터 조정 (stock_signal_engine.py 수정)
```

---

## 8. 기술 결정 사항 (Why)

| 결정 | 이유 |
|---|---|
| yfinance 유지 | 일봉 스윙 트레이딩에 15분 지연 충분. Webull API는 실시간 필요 시 추후 추가 가능 |
| pandas-ta 미사용 | Python 3.14에서 numba 컴파일 실패. 순수 pandas/numpy가 더 안정적 |
| SQLite 선택 | 포지션/관심종목/결과 기록에 충분. PostgreSQL 불필요 |
| 자동 주문 없음 | 신호 → 사람 확인 → 수동 주문 원칙. 오작동 시 금전 손실 방지 |
| 일봉 기준 | 초단타 제외, 확실한 종목만. 소음 제거 |
| MCP 서버 방식 | stdio, 포트 없음. Hermes 완전 독립. Claude Code 대화 시만 실행 |

---

## 9. 에러 진단 가이드

### 텔레그램 명령어 안 될 때
```bash
# 1. 봇 재시작 필요 여부 확인
# handlers/_stock.py 수정 후 반드시 봇 재시작

# 2. 핸들러 로드 실패 확인
# hermes_local.py 로그에서:
# "✅ 주식 분석 핸들러 등록 완료 (V_FINAL + 피드백 루프)" 확인

# 3. 모듈 단독 테스트
cd ~/Applications/Mjauto/Scripts
python3 -c "
from modules.stock_scanner import StockScanner
s = StockScanner()
print(s.analyze_single('AAPL'))
"
```

### MCP 서버 안 될 때
```bash
# 1. 연결 상태 확인
claude mcp list | grep stock

# 2. 서버 단독 실행 테스트
python3 ~/Applications/Mjauto/Scripts/stock_mcp_server.py

# 3. 재등록
claude mcp remove stock-scanner
claude mcp add stock-scanner -- python3 /Users/bluesea/Applications/Mjauto/Scripts/stock_mcp_server.py
```

### 데이터 이상할 때
```bash
# yfinance 네트워크 문제
python3 -c "import yfinance as yf; print(yf.Ticker('AAPL').history(period='5d'))"

# DB 상태 확인
sqlite3 ~/Applications/Mjauto/Scripts/data/stock_cache.db ".tables"
sqlite3 ~/Applications/Mjauto/Scripts/data/stock_cache.db "SELECT * FROM trade_results ORDER BY recorded_at DESC LIMIT 5;"
```

---

## 10. 현재 유니버스 (약 100종목)

### 포함 기준
- NASDAQ 상장 대형 기술주 + 성장주
- 일 달러 거래대금 충분한 종목 (유동성)
- 섹터 다양성 고려

### 주요 섹터별 포함 종목 (예시)
```
반도체/AI: NVDA, AMD, AVGO, QCOM, MRVL, ARM
소프트웨어: MSFT, GOOGL, META, AAPL, CRM, NOW
사이버보안: CRWD, PANW, ZS, FTNT, S
헬스케어:  LLY, ABBV, UNH, TMO
핀테크:    MA, V, PYPL, SQ, COIN
기타 성장: TSLA, AMZN, NFLX, SPOT, UBER
```

### 유니버스 수정 방법
```python
# modules/stock_fetcher.py 상단 CORE_UNIVERSE 리스트 수정
CORE_UNIVERSE = ["NVDA", "AMD", ...]  # 원하는 종목 추가/삭제
```

---

## 11. 향후 개선 아이디어

**v1.3에서 구현 완료:**
- [x] ~~**REVERSAL 부분 점수화**: MACD(0.75)+EMA교차(0.50)+RSI구간(0.25) 독립 분리~~
- [x] ~~**펀더멘털 필터**: EPS>15% / 매출>10% / 흑자 (yfinance, 7일 캐시)~~
- [x] ~~**실적발표 필터**: 발표 10일 이내 종목 매수 보류~~
- [x] ~~**트레일링 스탑**: ATR 기반 고점 추적 손절 (SQLite 저장)~~
- [x] ~~**섹터 RS 보너스**: 상위 4개 섹터 소속 종목 +0.5점~~

**다음 개선 후보:**
- [ ] **주간 자동 스캔 알림**: 매주 월요일 장 시작 전 자동 /scan → 텔레그램 발송
- [ ] **유니버스 확장**: S&P500 전체로 확장 (현재 ~100종목)
- [ ] **분봉 지원**: 일봉 외 4시간봉 추가 (진입 타이밍 정밀화)
- [ ] **수익률 차트**: /backtest 결과를 그래프로 시각화
- [ ] **파라미터 최적화**: 백테스트 데이터 기반 ALPHA_SCORE 임계값 자동 조정
- [ ] **펀더멘털 스코어링**: 현재 hard gate → 부분 점수화 (데이터 축적 후 검토)

---

*관련 파일: `Scripts/modules/stock_*.py`, `Scripts/handlers/_stock.py`, `Scripts/stock_mcp_server.py`*
*DB: `Scripts/data/stock_cache.db`*
*메타: `wiki/00_Meta/05_시스템 상태.md`, `wiki/00_Meta/02_스크립트 정보.md`*
