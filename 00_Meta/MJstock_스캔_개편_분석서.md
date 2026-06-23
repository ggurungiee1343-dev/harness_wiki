# MJstock 스캔 시스템 개편 분석서

> 작성일: 2026-06-21
> 목적: 문제점 분석 + 개편 내용 정리. 메타 7종 및 HTML 문서 업데이트 시 참조용.
> 관련 파일: `auto_scan_morning.py` / `auto_scan_intraday.py` / `send_scan_result.py` (수정)

---

## 1. 발견된 문제점 전체 목록

### 🔴 문제 1 — 텔레그램 차트 링크가 폰에서 안 열림 (핵심)

**파일**: `send_scan_result.py` → `run()` 함수

**기존 코드**:
```python
import socket as _sock
s = _sock.socket(_sock.AF_INET, _sock.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]   # → 192.168.0.10 같은 내부 IP

summary = (
    f"📱 차트 보기:\n"
    f"http://{local_ip}:8765"   # ← 이걸 텔레그램으로 전송
)
```

**문제 원인**:
- `192.168.x.x:8765` 는 공유기 내부 IP
- 집 WiFi에 연결된 상태에서만 접속 가능
- LTE/5G 또는 외부 네트워크에서는 **완전 차단**
- 게다가 `mobile_dashboard.py`(포트 8765)가 cron으로 자동 실행되지 않아
  링크가 있어도 서버 자체가 꺼져 있는 경우 많음

**해결책**:
```python
# 링크 전송 대신 HTML 파일 자체를 텔레그램 sendDocument API로 전송
url = f"https://api.telegram.org/bot{token}/sendDocument"
with open(chart_path, "rb") as f:
    resp = requests.post(
        url,
        data={"chat_id": chat_id, "caption": caption},
        files={"document": (filename, f, "text/html")},
    )
```

폰에서 파일을 탭하면 브라우저가 직접 HTML을 열음.
네트워크 무관, 서버 없이 동작, 시그널 포함 인터랙티브 차트 그대로 표시.

---

### 🔴 문제 2 — 장중 전용 검색기를 아침에 돌림

**파일**: `auto_scan_nasdaq500.py`

**기존 코드**:
```python
US_SCREENERS = [
    "uryangju",    # 일봉 기반 ← 아침 OK
    "judoju",      # 일봉 기반 ← 아침 OK
    "danta",       # 일봉 기반 ← 아침 OK
    "selyeok",     # 일봉 기반 ← 아침 OK
    "pochak",      # 장중 전용 ← ❌ 아침에 돌리면 의미없음
    "shooting",    # 장중 전용 ← ❌
    "chuddoli",    # 장중 전용 ← ❌
    "chowuryang",  # 일봉 기반 ← 아침 OK
]
# cron: 0 10 * * 1-5 → UTC 10시 = KST 오후 7시 (미국장 중간!)
```

**문제 원인**:
- `pochak`(세력포착), `shooting`(매수후바로슈팅), `chuddoli`(단타추돌이)는
  5분봉/30분봉 **실시간 데이터**가 핵심 조건
- 장 마감 후 일봉 확정 시점에 돌리면 5분봉/30분봉 데이터가
  전일 마지막 봉이라 조건 판정이 무의미
- 게다가 cron 시간이 `0 10 * * 1-5` = UTC 10:00 = KST 19:00
  → 미국장(KST 22:30~05:00) **4시간 전**에 돌리고 있었음

**해결책**:
```
아침 스캔 (KST 07:00)  → auto_scan_morning.py
  US: uryangju / judoju / danta / selyeok / chowuryang
  KR: uryangju_kr / judoju_kr / danta_kr / selyeok_kr / chowuryang_kr

장중 스캔 (KST 22:30)  → auto_scan_intraday.py --market us
  US: pochak / shooting / chuddoli

장중 스캔 (KST 09:10)  → auto_scan_intraday.py --market kr
  KR: pochak_kr / shooting_kr / chuddoli_kr
```

---

### 🟡 문제 3 — 일봉 데이터 중복 다운로드

**파일**: `auto_scan_nasdaq500.py` → `run_scan()` 함수

**기존 구조**:
```
우량주농사   → 종목 500개 × 일봉 다운로드 (0.35초/종목)
주도주단기   → 종목 500개 × 일봉 다운로드 (중복!)
단타의신     → 종목 500개 × 일봉 다운로드 (중복!)
세력주농사   → 종목 500개 × 일봉 다운로드 (중복!)
초우량주     → 종목 500개 × 일봉 다운로드 (중복!)
= 500 × 5 × 0.35초 = 약 14분 소요
```

**문제 원인**:
- `auto_scan_nasdaq500.py`가 `run_scan.py`를 subprocess로 5번 독립 실행
- 각 subprocess가 각자 500종목 일봉 데이터를 다운로드
- 동일 데이터를 5번 중복 요청

**현재 해결 수준**:
- 이번 개편에서 subprocess 구조는 유지 (run_scan.py 내부 로직 건드리지 않음)
- 근본 해결은 run_scan.py에 `--reuse-daily-cache` 옵션 추가 필요 (v2.0 과제)
- 현재는 시간대 분리로 부하 분산 (5개 검색기가 하루 종일 순차 실행되던 것을
  아침 1회로 집중 → 적어도 장중 3개 중복 제거)

---

### 🟡 문제 4 — health_check.py .env 로딩 경로 오류

**파일**: `health_check.py` → `send_telegram()` 함수

**기존 코드**:
```python
ROOT_DIR = Path(__file__).parent          # screener/ 폴더
load_dotenv(ROOT_DIR / "screener" / ".env")  # → screener/screener/.env ❌ 존재 안 함
load_dotenv(Path.home() / ".hermes" / ".env") # → ~/.hermes/.env ✅ 이게 살려줌
```

**실제 영향**: `~/.hermes/.env`에 `TELEGRAM_BOT_TOKEN`이 있어서 두 번째 줄이
구제하고 있음. 실제 발송 실패 원인은 아니었음.

**향후 수정**:
```python
# health_check.py가 screener/ 안에 있으므로
load_dotenv(Path(__file__).parent / ".env")  # screener/.env ← 올바른 경로
```

---

### 🟡 문제 5 — format_screener_result()에 차트 링크 없음

**파일**: `send_scan_result.py` → `format_screener_result()` 함수

**기존 코드**:
- `format_screener_result()` = 종목 점수/RSI/MACD만 텍스트로 전송
- 차트 링크 없음
- `run_scan.py`에서 `format_screener_result()`를 호출하고 있었으나
  차트 정보가 전혀 없는 텍스트만 전송됨

**해결책**:
- `format_screener_result()` 마지막에 `"📎 차트 파일 첨부 확인"` 안내 추가
- 실제 차트는 `send_document()`로 별도 첨부
- `get_chart_paths()` 함수 신규 추가 — farming/intraday 차트 경로 탐색

---

### 🟡 문제 6 — 텔레그램 요약에 종목명이 없음

**파일**: `auto_scan_nasdaq500.py` → `send_telegram_summary()` 함수

**기존 전송 내용**:
```
📊 MJstock 나스닥 500 자동 스캔
🕐 2026-06-21 07:00

✅ 검색식: 8/8
📈 총 통과: 15개 종목

✅ uryangju        8개
✅ judoju           2개
...
http://192.168.0.10:8765   ← 안 열림
```

**문제**: 어떤 종목이 통과했는지 전혀 알 수 없음.
차트 첨부 방식으로 전환하면 파일명에 티커가 포함되어 자동 해결됨.

---

## 2. 개편 후 파일 구조

```
Mjstock/
├── auto_scan_morning.py      ← 신규 (구 auto_scan_nasdaq500.py 대체)
├── auto_scan_intraday.py     ← 신규
├── screener/
│   └── send_scan_result.py  ← 수정 (send_document() 추가)
└── logs/
    ├── scan_morning.log      ← 신규
    ├── scan_intraday_us.log  ← 신규
    └── scan_intraday_kr.log  ← 신규
```

---

## 3. crontab 설정 (전체)

```bash
# 현재 crontab 확인
crontab -l

# 편집
crontab -e

# ── 추가할 내용 ──────────────────────────────────────────────────

# [아침] 미국+한국 일봉 스캔 (KST 07:00, 평일)
0 7 * * 1-5 cd /Users/bluesea/Applications/Mjstock && .venv/bin/python auto_scan_morning.py >> logs/scan_morning.log 2>&1

# [장중] 미국 장중 스캔 (KST 22:30, 평일 — 서머타임 기준)
30 22 * * 1-5 cd /Users/bluesea/Applications/Mjstock && .venv/bin/python auto_scan_intraday.py --market us >> logs/scan_intraday_us.log 2>&1

# [장중] 한국 장중 스캔 (KST 09:10, 평일)
10 9 * * 1-5 cd /Users/bluesea/Applications/Mjstock && .venv/bin/python auto_scan_intraday.py --market kr >> logs/scan_intraday_kr.log 2>&1

# [헬스체크] 평일 18:00 (기존 유지)
0 18 * * 1-5 cd /Users/bluesea/Applications/Mjstock/screener && .venv/bin/python health_check.py >> /Users/bluesea/Applications/Mjstock/logs/health_check.log 2>&1

# ── 기존 제거 대상 ────────────────────────────────────────────────
# 아래 줄 삭제 (auto_scan_nasdaq500.py → 더 이상 사용 안 함)
# 0 10 * * 1-5 cd /Users/bluesea/Applications/Mjstock && python3 auto_scan_nasdaq500.py
```

---

## 4. 텔레그램 수신 형식 변화

### 기존 (아침 7시)
```
📊 MJstock 나스닥 500 자동 스캔
🕐 2026-06-21 07:00

✅ 검색식: 8/8
📈 총 통과: 15개 종목

✅ uryangju        8개
❌ pochak           0개   ← 장중 검색기를 아침에 돌려서 항상 0
...

http://192.168.0.10:8765  ← LTE에서 안 열림
```

### 개편 후 — 아침 (KST 07:00)
```
📊 MJstock 미국 아침 스캔
🕐 2026-06-21 07:00

✅ 우량주농사: 8종목
✅ 주도주단기농사: 3종목
⚠️ 단타의신: 0종목
✅ 세력주농사: 2종목
✅ 초우량주: 1종목

📈 총 통과: 14종목
📎 아래 차트 파일 탭하면 바로 열림

--- (다음 메시지로) ---
📈 우량주농사 — AMAT (일봉)
[📎 AMAT_farming_20260621.html]   ← 탭하면 브라우저에서 바로 열림

📈 우량주농사 — KLAC (일봉)
[📎 KLAC_farming_20260621.html]

... (최대 5개)
```

### 개편 후 — 미국 장중 (KST 22:30)
```
⚡ MJstock 미국 장중 스캔
🕐 2026-06-21 22:35
🎯 대상: 세력포착 / 매수후바로슈팅 / 단타추돌이

✅ 세력포착: 3종목
✅ 매수후바로슈팅: 1종목
⚠️ 단타추돌이: 0종목

🔥 총 4종목 포착 — 즉시 차트 확인!

--- (다음 메시지로) ---
⚡ 세력포착 — NVDA (일봉)
[📎 NVDA_farming_20260621.html]

⚡ 세력포착 — NVDA (5분봉)
[📎 NVDA_intraday_20260621.html]
```

---

## 5. 검색기별 스캔 시간대 완전 정리

### 미국 (US)

| 검색기 | 스캔 파일 | KST 실행 시간 | 이유 |
|---|---|---|---|
| 우량주농사 | auto_scan_morning.py | 07:00 | 일봉 기반, 미국 장 마감 후 |
| 주도주단기농사 | auto_scan_morning.py | 07:00 | 일봉+30분봉 (전일 30분봉 유효) |
| 단타의신 | auto_scan_morning.py | 07:00 | 일봉+30분봉 |
| 세력주농사 | auto_scan_morning.py | 07:00 | 일봉 전용 |
| 초우량주 | auto_scan_morning.py | 07:00 | 일봉 전용 |
| 세력포착 | auto_scan_intraday.py | 22:30 | 갭업+5분봉+30분봉 실시간 필수 |
| 매수후바로슈팅 | auto_scan_intraday.py | 22:30 | 갭업+5분봉 실시간 필수 |
| 단타추돌이 | auto_scan_intraday.py | 22:30 | 5분봉+30분봉 실시간 필수 |

### 한국 (KR)

| 검색기 | 스캔 파일 | KST 실행 시간 | 이유 |
|---|---|---|---|
| 우량주농사(KR) | auto_scan_morning.py | 07:00 | 일봉 기반, 전일 마감 후 |
| 주도주단기농사(KR) | auto_scan_morning.py | 07:00 | 일봉+30분봉 |
| 단타의신(KR) | auto_scan_morning.py | 07:00 | 일봉 |
| 세력주농사(KR) | auto_scan_morning.py | 07:00 | 일봉 전용 |
| 초우량주(KR) | auto_scan_morning.py | 07:00 | 일봉 전용 |
| 세력포착(KR) | auto_scan_intraday.py | 09:10 | 갭업+5분봉 실시간 필수 |
| 매수후바로슈팅(KR) | auto_scan_intraday.py | 09:10 | 5분봉 실시간 필수 |
| 단타추돌이(KR) | auto_scan_intraday.py | 09:10 | 5분봉 실시간 필수 |

---

## 6. 적용 방법 (집에서 할 것)

```bash
# 1. 파일 복사
cp auto_scan_morning.py  /Users/bluesea/Applications/Mjstock/
cp auto_scan_intraday.py /Users/bluesea/Applications/Mjstock/
cp send_scan_result.py   /Users/bluesea/Applications/Mjstock/screener/

# 2. 기존 auto_scan_nasdaq500.py 백업 (삭제 아님)
mv /Users/bluesea/Applications/Mjstock/auto_scan_nasdaq500.py \
   /Users/bluesea/Applications/Mjstock/auto_scan_nasdaq500.py.bak

# 3. crontab 교체
crontab -e
# 기존 auto_scan_nasdaq500.py 줄 삭제
# 위 §3의 4줄 추가

# 4. 즉시 테스트 (아침 스캔)
cd /Users/bluesea/Applications/Mjstock
.venv/bin/python auto_scan_morning.py

# 5. 즉시 테스트 (장중 스캔 — 장중 시간에)
.venv/bin/python auto_scan_intraday.py --market us
.venv/bin/python auto_scan_intraday.py --market kr
```

---

## 7. 메타 7종 및 HTML 업데이트 대상

이 개편 내용을 반영해야 하는 문서 목록:

| 문서 | 업데이트 내용 |
|---|---|
| `MJstock_사용설명서.html` | §스캔 실행 시간 표 전면 교체, auto_scan 파일명 변경 |
| `signals_entry_points.html` | §12 스캔 결과 해석법 — 텔레그램 형식 변경 반영 |
| `quant_logic_analysis.html` | §10 퀀트 DB 목록 — screener 키 목록 변경 없음 (유지) |
| `01_hot.md` | MJstock 스캔 개편 완료 항목 추가 |
| `02_스크립트_정보.md` | auto_scan 파일 2개 신규 등록, send_scan_result 수정 기록 |
| `00_Meta_지도.md` | 주식 프로그램 섹션 업데이트 |
| `주식 프로그램 및 주식 스크립트와 연동계획.md` | 스캔 시간대 표 전면 교체 |

---

## 8. 미해결 / 향후 과제

| 항목 | 우선순위 | 설명 |
|---|---|---|
| 일봉 캐시 공유 | 중 | run_scan.py에 `--reuse-cache` 옵션 추가 → 검색기 간 일봉 재사용 |
| health_check.py .env 경로 수정 | 하 | `load_dotenv(ROOT_DIR / "screener" / ".env")` → `load_dotenv(Path(__file__).parent / ".env")` |
| 서머타임 자동 감지 | 하 | 미국 장중 스캔 시간 22:30 vs 23:30 자동 전환 |
| 차트 전송 실패 재시도 | 하 | send_document() 실패 시 3회 retry 로직 |
| 삼돌이/농사단타 추가 | 중 | screen_nongsa_danta_kr/us.py → crontab에 추가 필요 |

---

*작성: 2026-06-21 | MJstock 스캔 시스템 개편 세션*
