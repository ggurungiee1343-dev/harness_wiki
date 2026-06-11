# 🔧 Mac Studio 유령 정리 & 최종 재설정 가이드

**작성:** Claude (NVIDIA 70B)  
**대상:** MJ 박사님의 Mac Studio  
**목표:** 메모리 50-60% 확보 & 안정화  

---

## 📋 발견된 문제점 (당신의 터미널 출력 기반)

### ✅ **확인된 유령 파일**
```
1. ❌ /Users/bluesea/Applications/Mjauto/Scripts/harness_v2.py (16614 bytes)
2. ❌ /Users/bluesea/Applications/Mjauto/Scripts/antigravity_bot_v2.py (7839 bytes)
3. ⚠️  __pycache__ 폴더 3개 발견
```

### ✅ **현재 상태 (양호)**
```
✓ LaunchAgent: com.bluesea.harness_agent.plist (현재 버전만 등록됨) ✅
✓ Port 1234: LM Studio 정상 LISTEN 중 ✅
✓ 실행 중인 Python 프로세스: 현재 상태 미표시 (재부팅 필요)
```

---

## 🚀 3단계 정리 절차

### **Step 1: 스크립트 실행 (자동 정리)**

**다운로드한 `cleanup_ghosts.sh` 파일을 실행:**

```bash
# 터미널에서:
cd ~/Downloads  # 또는 파일이 있는 폴더

# 스크립트 실행
bash cleanup_ghosts.sh

# 또는 (절대 경로 사용)
bash ~/Downloads/cleanup_ghosts.sh
```

**이 스크립트가 자동으로 처리할 것:**
- ✅ 유령 프로세스 강제 종료 (harness_v2, antigravity_bot 등)
- ✅ 과거 버전 스크립트 파일 삭제 (백업 생성)
- ✅ __pycache__ 폴더 제거
- ✅ .pyc 파일 제거
- ✅ 불필요한 LaunchAgent .plist 파일 제거
- ✅ Obsidian 캐시 정리
- ✅ 모든 변경사항 `/Users/bluesea/Applications/Mjauto/.backup_YYYYMMDD_HHMMSS/` 폴더에 백업

---

### **Step 2: Mac 재부팅**

**스크립트 실행 후 즉시 재부팅:**

```bash
# 터미널에서:
sudo reboot

# 또는 메뉴 > 재부팅
```

**재부팅이 중요한 이유:**
- LaunchAgent 변경사항 적용
- 메모리 캐시 초기화
- 좀비 프로세스 완벽 제거

---

### **Step 3: 메모리 상태 확인**

**재부팅 후, 터미널에서:**

```bash
# 1. 현재 메모리 상태 확인
top -l 1 -n 0 | grep PhysMem

# 기대 출력:
# PhysMem: 4.2G used (약 3G 이상 여유 있어야 함)

# 2. 현재 실행 중인 Python 프로세스 확인
ps aux | grep python | grep -v grep

# 기대: harness_agent.py 1개만 나와야 함

# 3. 하네스 에이전트 정상 작동 확인
ps aux | grep harness_agent

# 기대: 1줄 나와야 함 (PID, CPU%, MEM% 등)

# 4. LM Studio 정상 작동 확인
lsof -i :1234

# 기대: LM Studio LISTEN 상태
```

---

## ⚠️ 주의사항

### **🔴 DO NOT (하지 말 것)**
- ❌ 스크립트 없이 수동으로 파일 삭제하기 (백업 없음)
- ❌ 현재 하네스 에이전트 파일 삭제
- ❌ /Applications/ 폴더의 앱 강제 삭제
- ❌ Git 저장소(.git) 무삭제 삭제

### **✅ DO (할 것)**
- ✅ 스크립트 실행 후 백업 폴더 확인
- ✅ 재부팅 전에 중요 작업 저장
- ✅ 메모리 상태 확인 스크린샷 찍기
- ✅ 문제 발생 시 백업 폴더의 파일들 복구

---

## 📊 예상 개선 효과

### **정리 전**
```
Harness v2.0 (유령) ........................ ~800MB
Harness v3.6 (현재) ....................... ~1.2GB
Antigravity Bot (유령) .................... ~500MB
__pycache__ 폐기물 ........................ ~300MB
LaunchAgent 부하 ......................... ~200MB
기타 좀비 ................................ ~500MB
─────────────────────────────────────
총 메모리 사용: ~4.3GB (여유: 1-2GB)
```

### **정리 후 (기대값)**
```
Harness v3.6 (정상) ....................... ~1.2GB
Obsidian + 플러그인 ....................... ~600MB
시스템 베이스 ............................. ~1.5GB
─────────────────────────────────────
총 메모리 사용: ~2.0GB (여유: 6-8GB) 🚀
```

**예상 개선율: 50-60% 메모리 확보**

---

## 🔄 장기 안정성 유지 방법

### **향후 유령 프로세스 예방**

**주 1회 점검 (자동화 권장):**

```bash
# Mac의 LaunchAgent 확인
ls ~/Library/LaunchAgents/ | grep -iE "bot|agent|harness"

# 예상: com.bluesea.harness_agent.plist만 나와야 함
# 다른 것이 있으면 즉시 제거
```

**월 1회 정리 (권장):**

```bash
# __pycache__ 폐기물 정리
find /Users/bluesea/Applications/Mjauto -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# .pyc 파일 정리
find /Users/bluesea/Applications/Mjauto -type f -name "*.pyc" -delete 2>/dev/null
```

**반년 1회 정책:**

```bash
# Git 저장소 최적화 (경량화)
cd /Users/bluesea/Applications/Mjauto
git gc --aggressive --prune=all

cd /Users/bluesea/Applications/Mjobsidian
git gc --aggressive --prune=all
```

---

## 🆘 문제 발생 시 대응

### **문제 1: 스크립트 실행 중 오류 발생**

```bash
# 오류 메시지 저장
bash cleanup_ghosts.sh > cleanup.log 2>&1

# 로그 확인
cat cleanup.log

# 문제가 있으면 백업 폴더에서 파일 복구
cp -r ~/.backup_[날짜]/[파일명] [원본 경로]/
```

### **문제 2: 재부팅 후 하네스 에이전트 안 켜짐**

```bash
# 상태 확인
launchctl list | grep harness

# 없으면 로드
launchctl load ~/Library/LaunchAgents/com.bluesea.harness_agent.plist

# 로그 확인
log show --predicate 'process == "harness_agent"' --last 1h
```

### **문제 3: 메모리가 여전히 부족**

```bash
# 1. Obsidian 플러그인 비활성화 (큰 효과)
# Obsidian > 설정 > 플러그인 > 불필요한 것 비활성화

# 2. LM Studio 메모리 설정 조정
# LM Studio > 설정 > GPU 할당 메모리 조정

# 3. 최후의 수단: 로컬 LLM 대신 NVIDIA NIM만 사용
# harness_agent.py의 local_client 사용 중단
```

---

## ✅ 최종 체크리스트

정리 후 이 항목들을 모두 확인하세요:

- [ ] `cleanup_ghosts.sh` 실행 완료
- [ ] 백업 폴더 생성 확인 (`.backup_YYYYMMDD_HHMMSS/`)
- [ ] Mac 재부팅 완료
- [ ] `top` 명령어로 메모리 여유 확인 (6GB 이상)
- [ ] `ps aux | grep harness_agent` 결과 1줄만 나옴
- [ ] LM Studio Port 1234 정상 (lsof -i :1234)
- [ ] Telegram에서 하네스 에이전트 응답 확인
- [ ] Obsidian 정상 작동 확인

---

## 📞 추가 도움이 필요하면

**다음 정보를 준비하고 문제 보고:**

```
1. 스크립트 실행 결과 (cleanup.log)
2. 메모리 현황 (top -l 1 -n 0 | grep PhysMem)
3. 실행 중인 프로세스 (ps aux | grep -E "python|harness")
4. 에러 메시지 (터미널 복사/붙여넣기)
```

---

*최종 가이드: 2026-05-15 / Claude (NVIDIA 70B)*
