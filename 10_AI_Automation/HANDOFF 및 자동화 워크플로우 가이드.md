---
description: 이 문서는 Claude Code와 DeepSeek WebUI를 활용한 HANDOFF 프로세스와 자동화 워크플로우를 정리한다.
  작업 완료 시 HANDOFF.md에 현재 슬라이스와 결과를 기록하고, 인덱스 및 변경 이력을 관리한다. 이를 통해 개발 가이드와 시스템 상태를
  일관되게 유지하며 효율적인 협업을 지원한다.
tags:
- 10_AI_Automation
- automation
- claude-code
- deepseek
- development-guide
- handoff
- scanned
- system-status
---
---

**완료 내역:**

|작업|파일|
|---|---|
|✅ HANDOFF.md 신규 생성|`wiki/00_Meta/HANDOFF.md`|
|✅ Architect Loop 워크플로우 문서화|`자동화_시스템_사용법.md` §13 신규|
|✅ 응답 품질 원칙 적용|`harness_agent.py` + `CLAUDE.md`|
|✅ 변경 이력 기록|`05_시스템 상태.md`|
|✅ 인덱스 등록|`00_Meta_지도.md`|
|✅ 현재 작업 상태|`01_hot.md`|
|✅ 개발 가이드 이력|`HERMES3_MASTER_DEVELOPMENT_GUIDE.md`|

---

**사용 방법 요약:**

1. **Claude Code에서** → HANDOFF.md "현재 슬라이스" 채우기 (목표·수락기준·범위 밖)
2. **DeepSeek WebUI에서** → `docs/HANDOFF.md를 읽어라` + `/goal` 프롬프트 붙여넣기 → 구현
3. **완료 후** → DeepSeek이 HANDOFF.md "마지막 빌드 결과" 업데이트
4. **Claude Code로 돌아와서** → 결과 판단 + 다음 슬라이스 작성

---
*최종 업데이트: 2026-06-23 22:30*
