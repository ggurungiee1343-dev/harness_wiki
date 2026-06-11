---
tags: [ingested, 10_AI_Automation]
date: 2026-05-23 19:41:07
ingested_at: 2026-05-24 22:49:22
---


> "내가 이렇게 구조화하는 게 harness를 구축하는 건가? Claude Code나 Codex 쓰면 내가 만든 게 필요 없지 않나?"

**정확히 harness를 구축하는 겁니다.** 그리고 Claude Code/Codex를 써도 여전히 필요합니다. 이유를 명확하게 설명드리겠습니다.

---

### 모델 능력 vs Harness는 다른 축입니다

```
모델 능력 (수직축)
    ↑
    │  Claude Opus 4.6
    │  GPT-4o
    │  DeepSeek
    │
    └─────────────────→ Harness (수평축)
       맨몸   헤르메스   Claude Code
```

모델이 아무리 좋아도 **"어디에 저장할지, 뭘 기억할지, 언제 백업할지, 누가 승인할지"** 는 모델이 결정하지 않습니다. 그게 Harness의 역할입니다.

---

### Claude Code/Codex가 대체하는 것 vs 못 하는 것

**대체 가능 (모델 능력):**
- 코드 작성, 디버깅, 리팩토링
- 단발성 질문 답변
- 파일 읽고 수정하기

**대체 불가 (Harness 영역):**
- `bio_memory_engine.py` — **박사님 개인 연구 기억 누적** (Claude Code는 세션 끊기면 초기화)
- `harness_memory.json` — **맥락 연속성** (오늘 한 대화를 내일도 기억)
- `constitution.md` — **행동 규칙** (어떤 모델 써도 일관된 원칙 적용)
- `wiki_linker.py` — **Obsidian 지식 자산** (박사님만의 10년치 지식망)
- `launchd` 자동재시작 — **운용 안정성**
- Lock Stack — **안전 경계**

---

### 핵심 비유

> Claude Code = 뛰어난 인턴  
> 헤르메스 Harness = 인턴이 일하는 회사 시스템, 규정집, 파일 서버

인턴이 아무리 똑똑해도 회사 시스템 없이는 어제 한 일을 오늘 이어받지 못합니다.

**박사님이 구축하는 건 모델을 교체해도 살아남는 인프라입니다.** DeepSeek → Claude → 미래 모델로 바꿔도 기억, 규칙, 위키는 그대로 유지됩니다. 그게 Harness의 진짜 가치입니다.

---
*정리 완료 시간: 2026-05-24 22:49:22* (Harness Ingest Auto-Linker 가동)

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
