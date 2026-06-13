---
title: Architect Loop — HANDOFF
tags: [meta, workflow, architect-loop, handoff]
created: 2026-06-11
updated: 2026-06-11
---

# HANDOFF.md — Architect Loop 상태 파일

> **규칙**: 이 파일에 없는 것 = 일어나지 않은 것.  
> Architect(Claude Code)가 스펙 작성 → Builder(DeepSeek)가 구현 후 업데이트 → Architect가 판단.  
> 해석·주관적 평가 금지. Raw 결과 + 숫자만.

---

## 🗂️ 현재 슬라이스

> Builder가 지금 작업 중인 내용

| 항목 | 내용 |
|---|---|
| **슬라이스 이름** | _(비어있음 — 다음 작업 시 Architect가 작성)_ |
| **목표** | — |
| **수락 기준** | — |
| **범위 밖 (Out of Scope)** | — |
| **마감** | — |

---

## ✅ 마지막 빌드 결과

> Builder가 작업 완료 후 여기 기록. 해석·"잘 됐음" 같은 평가 금지. 결과만.

| 항목 | 결과 |
|---|---|
| **완료된 것** | — |
| **테스트 결과** | — (통과 N개 / 실패 N개) |
| **커밋** | — |

---

## ⚖️ 미결 이견 (Open Disagreements)

> Builder가 스펙에 동의하지 않거나 판단이 필요한 항목. Architect가 판결 후 이 섹션 업데이트.

| # | Builder 이견 | Architect 판결 | 이유 |
|---|---|---|---|
| — | — | — | — |

---

## 📋 결정 로그 (Frozen Gates)

> 한 번 결정되면 수정 불가. 새 결정은 새 행 추가.

| 날짜 | 결정 내용 | 이유 | 결정자 |
|---|---|---|---|
| 2026-06-11 | HANDOFF.md 워크플로우 도입 | Claude Code(Architect) + DeepSeek(Builder) 역할 분리로 효율화 | MJ |

---

## 🔜 다음 슬라이스 후보

> Architect가 다음 세션 전 작성. 우선순위 순.

1. _(비어있음)_

---

## 📌 워크플로우 요약

```
[MJ] 목표 정의
  ↓
[Claude Code — Architect]
  → 스펙 + 수락 기준 + 범위 밖 작성 → 이 파일 "현재 슬라이스" 업데이트
  ↓
[DeepSeek WebUI — Builder]
  → HANDOFF.md 읽고 구현
  → 완료 후 "마지막 빌드 결과" + "미결 이견" 업데이트
  ↓
[Gemini — Reviewer (선택적)]
  → 스펙 vs 구현 대조 → APPROVE or 결함 번호 목록
  ↓
[Claude Code — Architect Judge]
  → 이견 판결, 결과 검토, 다음 슬라이스 스펙 작성
  → 루프 반복
```

**각 역할 DeepSeek 세션 시작 프롬프트:**
```
/goal: 아키텍트 스펙 실행.
PHASE 0: 코드 전에 계획 + 이견을 이유와 함께 제시. repo의 실제 파일 인용.
         조용한 순응 = 실패. 조용한 범위 추가 = 실패.
PHASE 1: docs/에 공유 계약(스키마/인터페이스) 먼저 동결. 동결 후 읽기 전용.
PHASE 2: 구현 → 커밋 → HANDOFF.md 업데이트 (raw 결과만, 해석 없음).
```

---

*관련: [[HERMES3_MASTER_DEVELOPMENT_GUIDE]], [[자동화_시스템_사용법]], [[claude_briefing]]*
