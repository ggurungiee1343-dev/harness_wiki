---
tags: [ingested, 10_AI_Automation, automation, meta-update, claude-brief, hook-system, keyword-matching, workflow, integration]
description: "작업 완료 후 메타 6종 문서 업데이트 여부를 자동으로 확인하는 후크 시스템을 구현한다. 6대 메타 문서에서 Claude 대화용 브리핑 파일을 자동 생성하는 기능을 통합한다. 키워드 매칭 기반의 간단한 트리거 로직으로 LLM 호출 없이 동작한다."
brief: "brief"
---

# `meta_update_guard` + `/claude_brief` 통합 구현 요청

## 목적
1. **meta_update_guard**: 작업 완료 후 메타 6종 문서 업데이트 여부를
   텔레그램/WebUI에서 자동으로 물어보는 후크 시스템
2. **`/claude_brief`**: 6대 메타 문서에서 Claude 대화용 브리핑 파일
   자동 생성

---

## Part 1. meta_update_guard

### 1-1. 새 모듈 생성
경로: `modules/meta_update_guard.py`

#### 트리거 조건
다음 작업이 완료된 직후 자동 감지:
```python
TRIGGER_KEYWORDS = [
    # 파일 변경
    "파일 생성", "파일 수정", "파일 삭제", "저장",
    # 코드 변경
    "모듈 수정", "핸들러 수정", "스크립트 변경",
    "버그 수정", "오류 수정", "패치",
    # 기능 변경
    "명령어 추가", "기능 추가", "설정 변경",
    "업그레이드", "리팩토링", "구현 완료",
    # 영문
    "fixed", "updated", "created", "modified", "added",
]
```

#### 판단 로직
```python
def should_ask_meta_update(action_result: str) -> bool:
    """
    작업 결과 텍스트에 트리거 키워드 포함 여부 확인.
    LLM 호출 없음 — 단순 키워드 매칭.
    """
    text = action_result.lower()
    return any(kw in text for kw in TRIGGER_KEYWORDS)
```

#### 관련 파일 추론 로직
```python
def infer_related_meta_files(action_result: str) -> list:
    """
    작업 내용 기반으로 업데이트가 필요한 메타 파일 추론.
    항상 01_hot.md는 포함 (변경 이력).
    """
    files = ["01_hot.md"]  # 항상 포함

    if any(kw in action_result for kw in ["모듈", "스크립트", "핸들러", "명령어"]):
        files.append("02_스크립트_정보.md")

    if any(kw in action_result for kw in ["상태", "버전", "업그레이드", "엔진"]):
        files.append("05_시스템_상태.md")

    if any(kw in action_result for kw in ["설치", "포트", "런타임", "패키지"]):
        files.append("03_시스템_인벤토리.md")

    if any(kw in action_result for kw in ["오류", "버그", "장애", "수정"]):
        files.append("시스템_구조적_결함_분석.md")

    return files
```

#### 텔레그램 메시지 형식
```
✅ 작업 완료

📝 메타 문서 업데이트가 필요할 수 있습니다.
관련 파일:
• 01_hot.md — 변경 이력
• 05_시스템_상태.md — 현재 상태  ← 해당 시에만 표시

업데이트할까요?
[✅ 예] [❌ 아니오] [⏰ 나중에]
```

#### 인라인 버튼 콜백 처리
```
[✅ 예] 클릭 시:
  → 변경 내용 요약 자동 생성
  → 관련 메타 파일에 append
  → "✅ 메타 문서 업데이트 완료" 응답

[❌ 아니오] 클릭 시:
  → 메시지 삭제
  → 별도 동작 없음

[⏰ 나중에] 클릭 시:
  → "알겠습니다. /meta_update 로 나중에 업데이트하세요." 응답
  → pending_updates 큐에 저장
```

#### append 형식 (01_hot.md 기준)
```markdown
## YYYY-MM-DD HH:MM — [작업 제목]
- [변경 내용 1줄 요약]
- 관련 파일: [파일명]
```

---

### 1-2. 기존 핸들러 후크 추가
다음 핸들러들의 작업 완료 응답 직후에 후크 삽입:

```python
# 각 핸들러 작업 완료 후 공통 패턴
from modules.meta_update_guard import should_ask_meta_update, ask_meta_update

async def cmd_xxx(update, context):
    # ... 기존 작업 로직 ...
    result_text = "작업 완료 메시지"
    await update.message.reply_text(result_text)

    # 후크 — 2줄 추가
    if should_ask_meta_update(result_text):
        await ask_meta_update(update, context, result_text)
```

후크 추가 대상 핸들러:
- `handlers/_file.py` — 파일 생성/수정
- `handlers/_exec.py` — 명령어 실행
- `handlers/_research.py` — 연구/논문 작업
- `handlers/_memory.py` — 메모리 작업
- `handlers/_ingest.py` — 인제스트 작업

---

### 1-3. `/meta_update` 명령어 (나중에 수동 실행용)
```
/meta_update
```
→ pending_updates 큐 확인 후 처리
→ 큐 없으면 "현재 대기 중인 업데이트 없음" 응답

---

## Part 2. `/claude_brief` 명령어

### 2-1. 핸들러 추가
기존 적절한 핸들러에 `cmd_claude_brief` 함수 추가.

### 2-2. 소스 파일 및 추출 규칙

| 소스 파일 | 추출 내용 | 최대 줄 수 |
|---|---|---|
| `constitution.local.md` | §1.1 경로구조, §1.2 금지사항, §2.1 라우팅, §2.2 Fallback, Lock Stack | 40줄 |
| `01_hot.md` | `[ ]` 미완료 항목 + 최근 7일 changelog | 30줄 |
| `05_시스템 상태.md` | 파일 하단 최신 30줄 (tail) | 30줄 |
| `시스템_구조적_결함_분석.md` | `미해결`, `⚠️`, `🔴`, `[ ]` 포함 라인 | 20줄 |
| `메모리_파일_명세서.md` | `L1`, `L2`, `L3` 포함 라인 | 15줄 |
| `HERMES3_MASTER_DEVELOPMENT_GUIDE.md` | 현재 버전 + `진행 중`, `미완료`, `[ ]` 라인 | 20줄 |

### 2-3. 출력 파일
경로: `wiki/00_Meta/claude_briefing.md`

```markdown
# Hermes Claude Briefing
생성일시: YYYY-MM-DD HH:MM
버전: Hermes v9.2.6

---

## 🖥️ 시스템 스펙 & 경로
[constitution.local.md §1.1 추출]

## 🔒 Lock Stack (수정 금지)
- modules/bio_memory_engine.py
- modules/cove_engine.py
- modules/semantic_engine.py
- modules/deriver_layer.py
- modules/dreamer_layer.py

## 🔀 LLM 라우팅
[constitution.local.md §2.1, §2.2 추출]

## 📋 진행 중 작업 (TODO)
[01_hot.md 미완료 항목]

## 📅 최근 변경 (7일)
[01_hot.md 최근 changelog]

## 🖥️ 현재 시스템 상태
[05_시스템_상태.md 최신 30줄]

## 🚨 미해결 버그/장애
[시스템_구조적_결함_분석.md 미해결 항목]

## 🧠 메모리 현황
[메모리_파일_명세서.md L1/L2/L3]

## 🗺️ 개발 로드맵 (진행 중)
[HERMES3_MASTER_DEVELOPMENT_GUIDE.md 진행 중 항목]

---
*이 파일은 /claude_brief 명령어로 자동 생성됩니다.*
*Claude 새 대화 시작 시 이 파일 하나만 첨부하세요.*
```

### 2-4. 텔레그램 응답
```
# 성공 시
📄 Claude 브리핑 생성 완료
• 소스: 6대 메타 문서
• 출력: wiki/00_Meta/claude_briefing.md
• 크기: NKB
Claude 새 대화 시작 시 위 파일만 첨부하세요.

# 일부 누락 시
⚠️ Claude 브리핑 생성 완료 (일부 누락)
• 정상: N개 / 누락: [파일명]
• 출력: wiki/00_Meta/claude_briefing.md
```

---

## 공통 주의사항

1. **한글 파일명**: glob 대신 `Path` 직접 경로 지정
2. **LLM 호출 금지**: meta_update_guard 판단 로직은 키워드 매칭만 사용
3. **6대 문서 읽기 전용**: 소스 파일 절대 수정 금지
4. **Lock Stack 모듈 수정 금지**:
   `bio_memory_engine.py`, `cove_engine.py`, `semantic_engine.py`,
   `deriver_layer.py`, `dreamer_layer.py`
5. **배치 크기 32 이하** (OOM 방지)
6. **단일 인스턴스**: 중복 실행 방지
7. **파일 크기 제한**: `claude_briefing.md` 50KB 초과 시 각 섹션 자동 축소

---

## 첨부 파일 (AI에게 전달 시)
- 후크 추가할 핸들러들:
  `handlers/_file.py`, `handlers/_exec.py`,
  `handlers/_research.py`, `handlers/_memory.py`
- `wiki/00_Meta/constitution.local.md`
- `wiki/00_Meta/01_hot.md`
- `wiki/00_Meta/05_시스템 상태.md`
