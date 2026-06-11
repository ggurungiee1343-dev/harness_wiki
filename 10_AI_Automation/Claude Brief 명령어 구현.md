---
tags: [ingested, 10_AI_Automation, claude-brief, meta-documents, automation, telegram, command-handler, briefing]
description: "6대 메타 문서에서 필요한 정보만 추출하여 claude_briefing.md 파일을 자동 생성한다. 생성된 파일은 텔레그램으로 전송된다. 핸들러는 handlers/_meta.py에 구현하며 명령어는 /claude_brief를 사용한다."
brief: "brief"
---

# `/claude_brief` 명령어 구현 요청

## 목적
6대 메타 문서에서 Claude와의 대화에 필요한 정보만 추출하여
`claude_briefing.md` 파일 하나로 자동 생성 후 텔레그램으로 전송.

---

## 구현 위치
- 핸들러: `handlers/_meta.py` (또는 적절한 기존 핸들러에 추가)
- 출력 파일: `/Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/claude_briefing.md`
- 명령어: `/claude_brief`

---

## 소스 파일 및 추출 규칙

### 1. constitution.local.md
경로: `wiki/00_Meta/constitution.local.md`
추출 내용:
- §1.1 경로 구조 (전체)
- §1.2 로컬 금지 사항 (전체)
- §2.1 라우팅 현황 (전체)
- §2.2 하네스 Fallback 체인 (전체)
- Lock Stack 항목 (전체)

### 2. 01_hot.md
경로: `wiki/00_Meta/01_hot.md`
추출 규칙:
- `[ ]` 또는 `TODO` 포함 라인 (미완료 항목 전체)
- 최근 7일 이내 날짜가 포함된 changelog 라인
- 최대 30줄 제한 (초과 시 최신순 30줄)

### 3. 05_시스템_상태.md
경로: `wiki/00_Meta/05_시스템 상태.md`
추출 규칙:
- 파일 전체에서 최신 30줄만 추출
- (파일 하단이 가장 최신이므로 tail 방식)

### 4. 시스템_구조적_결함_분석.md
경로: `wiki/00_Meta/시스템_구조적_결함_분석.md`
추출 규칙:
- `미해결`, `⚠️`, `🔴`, `TODO`, `[ ]` 포함 라인만 추출
- 없으면 "미해결 항목 없음" 출력

### 5. 메모리_파일_명세서.md
경로: `wiki/00_Meta/메모리_파일_명세서.md`
추출 규칙:
- `L1`, `L2`, `L3` 포함 라인만 추출
- 파일 크기/상태 관련 라인 포함
- 최대 15줄 제한

### 6. HERMES3_MASTER_DEVELOPMENT_GUIDE.md
경로: `wiki/00_Meta/HERMES3_MASTER_DEVELOPMENT_GUIDE.md`
추출 규칙:
- 현재 버전 번호 포함 라인
- `진행 중`, `예정`, `미완료`, `[ ]` 포함 라인
- 최대 20줄 제한

---

## 출력 파일 형식 (claude_briefing.md)

```markdown
# Hermes Claude Briefing
생성일시: YYYY-MM-DD HH:MM
버전: Hermes v9.2.6

---

## 🖥️ 시스템 스펙
[constitution.local.md §1.1 추출 내용]

## 🔒 Lock Stack (수정 금지)
[constitution.local.md Lock Stack 추출 내용]

## 🔀 LLM 라우팅
[constitution.local.md §2.1, §2.2 추출 내용]

## 📋 진행 중 작업 (TODO)
[01_hot.md 미완료 항목]

## 📅 최근 변경 (7일)
[01_hot.md 최근 changelog]

## 🖥️ 현재 시스템 상태
[05_시스템_상태.md 최신 30줄]

## 🚨 미해결 버그/장애
[시스템_구조적_결함_분석.md 미해결 항목]
없으면: "미해결 항목 없음"

## 🧠 메모리 현황
[메모리_파일_명세서.md L1/L2/L3 상태]

## 🗺️ 개발 로드맵 (진행 중)
[HERMES3_MASTER_DEVELOPMENT_GUIDE.md 진행 중 항목]

---
*이 파일은 /claude_brief 명령어로 자동 생성됩니다.*
*Claude 대화 시작 시 이 파일 하나만 첨부하세요.*
```

---

## 텔레그램 응답

### 성공 시
```
📄 Claude 브리핑 파일 생성 완료

• 소스: 6대 메타 문서
• 출력: wiki/00_Meta/claude_briefing.md
• 크기: NKB

Claude 새 대화 시작 시 위 파일 하나만 첨부하세요.
```

### 실패 시 (특정 소스 파일 없을 때)
```
⚠️ Claude 브리핑 생성 완료 (일부 누락)

• 정상 추출: N개 파일
• 누락: [파일명] — 파일 없음
• 출력: wiki/00_Meta/claude_briefing.md
```

---

## 구현 주의사항

1. **한글 파일명 처리**
   - `05_시스템 상태.md` 등 공백 포함 파일명 주의
   - `Path` 객체로 처리, glob 대신 직접 경로 지정

2. **파일 없을 때**
   - 소스 파일 하나가 없어도 나머지로 생성 계속
   - 누락된 파일명은 브리핑에 `[누락]` 표시

3. **Lock Stack 항목**
   - constitution.local.md에 명시적 Lock Stack 섹션이 없으면
     `bio_memory_engine.py`, `cove_engine.py`, `semantic_engine.py`,
     `deriver_layer.py`, `dreamer_layer.py` 하드코딩으로 포함

4. **파일 크기 제한**
   - 전체 출력 파일 50KB 초과 시 각 섹션 추출량 자동 축소
   - Claude 컨텍스트 효율을 위해 간결하게 유지

5. **기존 파일 덮어쓰기**
   - `claude_briefing.md` 기존 파일 있으면 덮어쓰기
   - 백업 불필요 (매번 새로 생성하는 파일)

6. **6대 문서 수정 금지**
   - 소스 파일(6대 문서)은 읽기 전용으로만 접근
   - 절대 수정하지 않음

---

## 첨부 파일
- `handlers/_meta.py` (또는 명령어를 추가할 핸들러 파일)
- `wiki/00_Meta/constitution.local.md`
- `wiki/00_Meta/01_hot.md`
- `wiki/00_Meta/05_시스템 상태.md`
