# 시스템 업그레이드 (Runbook)

## Python 버전 업그레이드

현재: Python 3.14.4 (Homebrew)
관련 경로:
- `/opt/homebrew/bin/python3`
- `/opt/homebrew/lib/python3.14/site-packages/`

## 패키지 업데이트

```bash
cd ~/Applications/Mjauto/Scripts
pip3 install --upgrade -r requirements.txt
```

## Hermes Agent 업그레이드

```bash
pip3 install --upgrade hermes-agent
```

## Launchd 재시작 (업그레이드 후)

```bash
for svc in bot webui; do
  launchctl stop com.hermes.$svc
  sleep 1
  launchctl start com.hermes.$svc
done
```

## 롤백 절차

1. GitHub에 커밋된 이전 버전 확인
2. 필요 시 `git revert` 또는 `git checkout` 사용
3. plist 수정 시 `launchctl unload` → 수정 → `launchctl load`

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*

---

## 2026-06-03 업그레이드 체크리스트 추가

### 봇 업데이트 후 필수 확인
- [ ] HELP_TEXT 명령어 목록 최신화 (`hermes_local.py`)
- [ ] wiki 타임스탬프 전수 확인 (`wiki_auto_stamper.py --scan`)
- [ ] constitution.md §9 타임스탬프 규칙 준수 여부 확인
- [ ] Bio-Memory L1/L2/L3 파일 정상 여부 (`/memory`)

*최종 업데이트: 2026-06-03 19:05 — 업그레이드 체크리스트 현행화*
