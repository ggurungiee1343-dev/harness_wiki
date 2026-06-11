# GROK_2025_ULTIMATE_V4.1 (Alpha Master) — 주식 스캔 수식

## 분류
[[Stock Analysis]] | [[Alpha Master]]

## 원본
[[Clippings/Archive/2025_ULTIMATE_V4.1 (Alpha Master).md]]

---

## 수식 요약

### 점수 체계 (합격: 4.0+ / 6.5점)

| 조건 | 점수 | 기준 |
|------|------|------|
| IS_TIGHT | 1.5 | ATR10 < ATR30×0.85 AND BB축소 중 |
| IS_LEADER | 1.5 | RS_LINE 50일 신고가 AND RS_MA 상승 중 |
| FRESH_TREND | 1.5 | EMA200 > 3개월전 AND > 6개월전 |
| VOL_SURGE | 1.0 | 거래량 1.5배 + 3M株 이상 |
| RSI_NEUTRAL | 1.0 | RSI 40~70 구간 |

### 매수 조건
```
SAFE_MARGIN + SEPA_FULL + IS_TIGHT + IS_LEADER + FRESH_TREND + VOL_SURGE + RSI_NEUTRAL + MARKET_CAP_OK
```

### 매도 조건
- SELL_LOSS: 종가 < 매수가 × 0.92 (-8% 하드 스탑)
- SELL_TRAIL: 종가 < EMA50 이탈
- SELL_RSIHIGH: RSI > 80 (과매수 분할 매도)
- SELL_CHOP: BB_WIDTH > 1.20×20일전 (변동성 급등)

---

## 관련 문서
- [[ultra_swing_v3_스크립트_문서]] — ultra_swing_v3.py 스크립트 설명
- [[ULTRA_SWING_V3_작업_요약]] — V3.0 작업 기록

## 태그
#stock #alpha-master #screening-formula

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
