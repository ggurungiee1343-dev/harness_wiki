# 장애 복구 (Runbook)

## 봇 응답 없음

```bash
# 1. 프로세스 확인
launchctl list | grep hermes

# 2. 로그 확인
tail -50 ~/Applications/Mjauto/Scripts/hermes_launchd.log

# 3. 재시작
launchctl stop com.hermes.bot && sleep 2 && launchctl start com.hermes.bot

# 4. 10초 후 응답 확인
```

## Launchd 서비스 미실행

```bash
# 1. 로드 확인
launchctl list | grep com.hermes

# 2. 언로드 후 재로드
launchctl unload ~/Library/LaunchAgents/com.hermes.bot.plist
launchctl load ~/Library/LaunchAgents/com.hermes.bot.plist

# 3. plist 오류 확인
plutil ~/Library/LaunchAgents/com.hermes.bot.plist
```

## 디스크 부족

```bash
# 1. 디스크 사용량 확인
df -h

# 2. 큰 파일 찾기
du -sh ~/.hermes/logs/* | sort -rh | head -5
du -sh ~/.hermes/skills/*   | sort -rh | head -5

# 3. 로그 정리
# 7일 이상 로그 자동 정리
find ~/.hermes/logs -name "*.log" -mtime +7 -delete
```

## 메모리 부족

```bash
# 1. 메모리 확인
vm_stat | head -10

# 2. 큰 프로세스 확인
ps aux --sort=-%mem | head -10

# 3. 봇 재시작 (메모리 해제)
launchctl stop com.hermes.bot
sleep 2
launchctl start com.hermes.bot
```

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*

---

## 2026-06-03 복구 절차 추가

### Bio-Memory 복구 (맥락 이해 저하 시)
```bash
# 1. 메모리 상태 확인
# 텔레그램: /memory

# 2. Dreaming 강제 실행
# 텔레그램: /memory_dream

# 3. episodic_memory.json 백업 확인
ls ~/.hermes/runtime/memory/backups/

# 4. 봇 재시작
pkill -f hermes_local.py
```

### wiki 타임스탬프 누락 복구
```bash
python3 /Users/bluesea/Applications/Mjauto/Scripts/wiki_auto_stamper.py --scan
```

*최종 업데이트: 2026-06-03 19:05 — Bio-Memory 복구 절차 추가*
