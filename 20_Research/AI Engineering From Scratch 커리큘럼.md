---
tags: [ingested, 20_Research]
date: 2026-05-23 20:04:29
ingested_at: 2026-05-24 22:49:20
---

https://github.com/rohitg00/ai-engineering-from-scratch

확인하겠습니다.

**헤르메스 구조화와 직접 연관은 없지만, 박사님께 개인적으로 가치 있는 레포입니다.**

---

## 무엇인가

수학 기초부터 자율 에이전트 스웜까지 20개 Phase, 230개 이상 실습 레슨으로 구성된 AI 엔지니어링 커리큘럼입니다. Python, TypeScript, Rust, Julia를 다루며, 매 레슨마다 프롬프트/스킬/에이전트/MCP 서버 같은 재사용 가능한 결과물을 산출합니다. [github](https://github.com/rohitg00/ai-engineering-from-scratch)

---

## 헤르메스와의 관련성

커리큘럼 결과물 구조가 `outputs/prompts/`, `outputs/skills/`, `outputs/agents/`, `outputs/mcp-servers/`로 구성되며, SkillKit으로 설치해 Claude Code나 Cursor에 바로 플러그인할 수 있습니다. [github](https://github.com/rohitg00/ai-engineering-from-scratch)

즉 이 커리큘럼을 따라가면서 만든 결과물이 **그대로 헤르메스 `~/.hermes/skills/`에 추가 가능**합니다.

---

## 박사님께 특히 유용한 Phase

| Phase | 내용 | 헤르메스 연관 |
|---|---|---|
| **Phase 14** | Agent Loop, Memory, Context 압축, Hooks, Self-Healing | `bio_memory_engine.py` 고도화 직접 참고 |
| **Phase 15** | 자율 시스템, 비용 인식, 안전 경계 | Lock Stack 설계 원칙 |
| **Phase 11** | RAG, 고급 청킹, 리랭킹 | `semantic_engine.py` 개선 참고 |
| **Phase 13** | MCP 서버/클라이언트 빌드 | 26일 이후 MCP 확장 시 |

---

## 결론

**설치 불필요, 참고 커리큘럼으로 보존.**

헤르메스 모듈을 더 깊이 이해하고 개선하고 싶을 때, 특히 `bio_memory_engine.py`나 `semantic_engine.py` 리팩토링 시 **Phase 14 Agent Engineering** 섹션이 직접적인 참고 자료가 됩니다. Obsidian 위키에 북마크해 두시길 권합니다.

---
*정리 완료 시간: 2026-05-24 22:49:20* (Harness Ingest Auto-Linker 가동)

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
