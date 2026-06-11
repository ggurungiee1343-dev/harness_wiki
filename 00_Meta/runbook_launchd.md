# Launchd 서비스 관리 (Runbook)

## 서비스 목록

| 서비스 | Plist | 상태 | 용도 |
|--------|-------|------|------|
| `hermes_bot` | `~/Library/LaunchAgents/com.hermes.bot.plist` | 🟢 | 텔레그램 봇 (hermes_local.py) |
| `hermes_webui` | `~/Library/LaunchAgents/com.hermes.webui.plist` | 🟢 | Hermes WebUI |

## 상태 확인

```bash
launchctl list | grep hermes
# PID가 있는지 확인
```

## 로그 확인

```bash
# 봇 로그
tail -f ~/Applications/Mjauto/Scripts/hermes_launchd.log

# 에러 로그
tail -f ~/Applications/Mjauto/Scripts/hermes_launchd.error.log

# Hermes WebUI 로그
tail -f ~/Applications/hermes-webui/hermes_webui.log
```

## 재시작

```bash
# 봇 재시작
launchctl stop com.hermes.bot
sleep 2
launchctl start com.hermes.bot

# WebUI 재시작
launchctl stop com.hermes.webui
sleep 2
launchctl start com.hermes.webui

# 둘 다 재시작
for svc in bot webui; do
  launchctl stop com.hermes.$svc
  sleep 1
  launchctl start com.hermes.$svc
done
```

## Plist 경로

- `~/Library/LaunchAgents/com.hermes.bot.plist`
- `~/Library/LaunchAgents/com.hermes.webui.plist`

## KeepAlive 설정

두 서비스 모두 `KeepAlive: SuccessfulExit` — 크래시 시 자동 재시작.

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*

---

## 2026-06-03 업데이트

### 봇 프로세스 목록 (현행)
| 서비스 | PID 확인 | 역할 |
|--------|----------|------|
| `com.hermes.bot` | `pgrep -f hermes_local.py` | Hermes1 텔레그램 봇 |
| `com.hermes.webui` | `pgrep -f server.py` | Hermes WebUI |
| `hermes2_bot.py` | `pgrep -f hermes2_bot.py` | Hermes2 게이트웨이 |

### 주의사항 (2026-06-03)
- `pkill -f hermes_local.py` 사용 시 launchd KeepAlive가 5초 내 자동 재시작
- `launchctl bootout` 사용 시 수동으로 `launchctl bootstrap` 필요

*최종 업데이트: 2026-06-03 19:05 — 프로세스 목록 현행화*
