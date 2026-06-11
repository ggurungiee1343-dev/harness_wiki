---
title: Wiki Git 사용법
tags: [meta, git, wiki, 버전관리]
created: 2026-06-10
updated: 2026-06-10
---

# Wiki Git 사용법

> Wiki 버전 관리 시스템. 문서 실수 복구 + GitHub 백업용.
> 초기화 완료: 2026-06-10 (306개 파일 첫 커밋)

---

## 기본 워크플로우

### 1. 변경 사항 저장 (커밋)

문서 작성/수정 후 주기적으로 커밋하면 실수로 삭제해도 복구 가능.

```bash
# 변경된 파일 확인
git -C ~/Applications/Mjobsidian/wiki status

# 전체 변경 사항 커밋
git -C ~/Applications/Mjobsidian/wiki add -A
git -C ~/Applications/Mjobsidian/wiki commit -m "docs: 오늘 작업 내용 요약"

# 특정 폴더만 커밋
git -C ~/Applications/Mjobsidian/wiki add 50_Invest/
git -C ~/Applications/Mjobsidian/wiki commit -m "docs: 주식 분석 업데이트"
```

### 2. 변경 내역 확인

```bash
# 최근 커밋 목록
git -C ~/Applications/Mjobsidian/wiki log --oneline -10

# 특정 파일 변경 이력
git -C ~/Applications/Mjobsidian/wiki log --oneline -- "00_Meta/01_hot.md"

# 어제와 비교
git -C ~/Applications/Mjobsidian/wiki diff HEAD~1 HEAD
```

### 3. 실수 복구

```bash
# 특정 파일 마지막 커밋 상태로 복원
git -C ~/Applications/Mjobsidian/wiki checkout HEAD -- "50_Invest/삭제된파일.md"

# 3일 전 상태의 파일 꺼내기
git -C ~/Applications/Mjobsidian/wiki log --oneline  # 커밋 ID 확인
git -C ~/Applications/Mjobsidian/wiki show abc1234:"00_Meta/01_hot.md" > /tmp/복구본.md
```

---

## GitHub Private Repo 연결 (1회만 설정)

### 설정 단계

1. GitHub → New Repository → **Private** → 이름: `mjwiki` (또는 원하는 이름)
2. 아래 명령어 실행:

```bash
# Remote 연결
git -C ~/Applications/Mjobsidian/wiki remote add origin https://github.com/[계정명]/mjwiki.git

# 최초 Push
git -C ~/Applications/Mjobsidian/wiki push -u origin main
```

### 연결 확인

```bash
git -C ~/Applications/Mjobsidian/wiki remote -v
# origin  https://github.com/[계정]/mjwiki.git (fetch)
# origin  https://github.com/[계정]/mjwiki.git (push)
```

### 이후 Push (변경 사항 GitHub에 올리기)

```bash
git -C ~/Applications/Mjobsidian/wiki push
```

---

## 자동 커밋 설정 (선택)

매일 자정 자동 커밋하려면 `~/.hermes/launchd/` 에 plist 추가.
현재는 수동 커밋 방식으로 운영 중 (Claude Code가 작업 후 커밋).

---

## .gitignore 규칙

현재 제외 항목:
- `.DS_Store` — macOS 메타데이터
- `*.bak`, `*_old.md`, `*_test.md` — 임시 파일
- `.obsidian/workspace*.json` — Obsidian 개인 설정
- `*.env`, `*secret*`, `*password*` — 민감 정보

---

## 일일 lint 자동화와 연동

매일 새벽 3:17 자동 실행되는 Wiki lint 스케줄이 미커밋 파일이 20개 초과 시 텔레그램 알림을 발송합니다.
알림 받으면 커밋 진행 권장.

---

## 연관 문서
- [[session_start_hook.sh]] — 세션 시작 시 wiki 상태 자동 주입
- [[05_시스템 상태]] — 전체 변경 이력
