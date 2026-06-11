---
tags: [ingested, 10_AI_Automation]
date: 2026-05-23 13:01:37
ingested_at: 2026-05-24 22:49:30
---

충분히 파악했습니다. 분석드립니다.

---

## learn-harness-engineering 핵심 개념

모델이 아무리 강력해도 주변 환경(하네스)을 제대로 구축하지 않으면 실제 엔지니어링 작업에서 실패한다는 것이 이 레포의 핵심 전제 [GitHub](https://github.com/FrancyJGLisboa/agent-skill-creator) 입니다.

하네스는 5개 서브시스템으로 구성됩니다 — Instructions(무엇을 어떤 순서로), State(진행 상황 추적), Verification(테스트 통과만이 완료 증거), Scope(한 번에 기능 하나), Session Lifecycle(시작/종료 루틴) [GitHub](https://github.com/FrancyJGLisboa/agent-skill-creator)

---

## 헤르메스 적용 여지 분석

### ✅ 이미 갖춘 것 (강점)

| 하네스 요소 | 헤르메스 현재 |
|---|---|
| Instructions | `hermes_context_v*.md` ✅ |
| State (일부) | `bio_memory_engine` ✅ |
| Scope | Karpathy 규칙 A5 "Stay in scope" ✅ (어제 적용) |

---

### ❌ 없는 것 (개선 여지)

**1. Verification 서브시스템**

에이전트는 테스트, lint, 타입 체크, 스모크 런을 통과하지 않으면 완료를 선언할 수 없다 — 검증 통과만이 완료의 증거 [GitHub](https://github.com/FrancyJGLisboa/agent-skill-creator)

헤르메스는 현재 "구현했다"고 하면 완료입니다. 실제로 동작하는지 검증하는 루틴이 없습니다.

**2. Session Lifecycle**

세션 시작 시 `init.sh` 실행, 세션 종료 시 clean-state 체크리스트, 다음 세션을 위한 핸드오프 노트 — 이 구조 덕분에 다음 세션이 이전 세션이 끊긴 정확한 지점에서 재개됩니다 [GitHub](https://github.com/FrancyJGLisboa/agent-skill-creator)

헤르메스는 세션마다 컨텍스트를 새로 로드하는데, **어디서 끊겼는지 정확한 재개 지점**이 없습니다. 어제 만든 `STATE.md` 계획과 직결됩니다.

**3. progress.md (State 심화)**

without harness: 세션 2에서 에이전트가 새로 시작해 이전에 무슨 일이 있었는지 기억 없이 작업을 다시 하거나 엉뚱한 걸 함 / with harness: 세션 2에서 에이전트가 progress log를 읽고 정확히 중단된 지점을 이어받음 [GitHub](https://github.com/FrancyJGLisboa/agent-skill-creator)

---

## 결론: 개선 여지 있음 — 단 범위를 좁혀서

전체 12강 커리큘럼을 적용할 필요는 없고, **헤르메스에 빠진 2가지만 가져오면 됩니다:**

```
1순위 — Session Lifecycle
   hermes_session_start.sh  (세션 시작 루틴)
   hermes_session_end.md    (종료 시 체크리스트 + 핸드오프 노트)

2순위 — Verification 루틴
   새 기능 구현 후 /hermes.verify 명령어
   "동작 확인 없이 완료 선언 금지" 규칙
```

이 두 가지는 어제 만든 Phase 2 (GSD의 STATE.md)와 합쳐서 한번에 만들 수 있습니다.

**만들어드릴까요?**

---
*정리 완료 시간: 2026-05-24 22:49:30* (Harness Ingest Auto-Linker 가동)

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
