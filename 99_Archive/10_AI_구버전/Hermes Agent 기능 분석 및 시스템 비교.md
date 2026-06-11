---
tags: [ingested, 10_AI_Automation, hermes-agent, ai-automation, system-comparison, memory-management, skill-evolution, session-search, progressive-disclosure]
description: "공식 Hermes Agent의 기능을 소개하고 우리 시스템과의 중복 여부를 분석한다. MEMORY.md, Session search, SOUL.md, Self-evolving skills 등 주요 기능을 constitution.local.md와 실제 파일 기준으로 비교한다. 기존 시스템에 이미 존재하는 기능과 새로 적용 가능한 기능을 체계적으로 분류한다."
brief: "summary"
---

이 글은 공식 Hermes Agent (Hermes2 v9.3?)의 기능 소개 + 튜토리얼입니다. 현재 MJ님 시스템이 이미 Hermes 기반이므로, **우리 시스템에서 이미 있는 것 / 없는 것 / 적용 가능한 것**을 constitution.local.md + 실제 파일 기준으로 분석합니다.

---

## 1. 우리 시스템에 이미 있는 것 (중복)

| 기능 | Hermes 공식 문서 | 우리 시스템 대응 |
|------|-----------------|----------------|
| **MEMORY.md / USER.md** | T1 메모리, ~2.2K / ~1.4K chars | memory.md + memory tool. USER.md는 memory(user)로 대체 |
| **Session search** | SQLite FTS5 | state.db 동일. session_search tool로 사용 중 |
| **SOUL.md** | identity layer | constitution.local.md §4.1 (나의 비서 가이드)가 동일 역할 |
| **Self-evolving skills** | agent가 create/patch/edit | 동일. skill_manage tool로 사용 중 (constitution §X.3) |
| **Progressive disclosure** | 이름만 → 전체 로드 | 동일. skill_view(name) → 필요 시 file_path |
| **Profiles** | 완전 격리 인스턴스 | 우리는 dual hermes home (~/.hermes + ~/Applications/venu/.hermes2/)으로 2개만 있음 |
| **Cron (영어 스케줄)** | "every weekday at 8am" | cronjob tool 동일. 우리도 사용 중 |
| **Gateway (Telegram)** | 텔레그램 봇 | com.hermes.bot (launchd), com.hermes.webui 운영 중 |
| **Config / .env 분리** | config.yaml + .env | 동일 구조 |

## 2. 우리 시스템에 없는 것 (갭)

| 기능 | 설명 | 우리 상태 |
|------|------|----------|
| **GEPA (offline skill optimization)** | 실행 trace 기반 진화, PR 생성 | 없음. Lock Stack에 dreaming이 유사 기능이나 GEPA 수준 아님 |
| **Curator (자동 skill 정리)** | 7일 idle 감지 → 오래된 skill 정리 | 없음. 수동 관리만 |
| **Multi-profile: 3개 이상** | designer/programmer/researcher 완전 격리 | 2개만 있음. 3번째 프로필 없음 |
| **External memory providers (8종)** | Mem0, Memobase, Zep 등 플러그인 | 우리는 Bio-Memory Engine (L1/L2/L3) 자체 구현 |
| **Claude Code 위임** | Hermes가 Claude Code CLI 호출 | 없음. DeepSeek API 직접 호출 |
| **Skills Hub (687개)** | 공식 저장소 | 우리는 직접 작성한 custom skills만 있음 |
| **acp_command (subagent 전송)** | subagent를 다른 CLI로 실행 | 없음. Hermes subagent만 |
| **Skins / Plugins 시스템** | CLI 테마, 플러그인 | 없음 |

## 3. 우리 시스템이 더 잘하는 것 (우위)

| 항목 | Hermes 공식 | 우리 시스템 |
|------|-----------|-----------|
| **메모리 계층 깊이** | T1(Tiny md) → T2(FTS5) → T3(외부) | L1(JSON working) → L2(episodic+associations+embedding) → L3(semantic+procedural) — 훨씬 정교 |
| **Spreading Activation** | 없음 | 1-Hop 활성화 확산 (line 364-374) |
| **Forgetting Curve** | 없음 | 에빙하우스 망각 곡선 적용 (line 91-108) |
| **벡터 검색** | FTS5만 | SemanticEngine + 코사인 유사도 + RRF |
| **Dreaming / offline consolidation** | 없음 | Dreaming V2 (PEMS+SKILLOPT) |
| **SIA 피드백 학습** | 없음 | sia_engine.py + monitoring_engine.py + load_balancer.py (v9.2) |
| **로컬 LLM 라우팅** | API 전용 | hybrid_router.py + Gemma4 + DeepSeek + NIM 3단 fallback |
| **Lock Stack (변경 금지 보호)** | 없음 | 5개 핵심 엔진 Lock Stack 규칙 |

## 4. 도입 가능 / 추천하는 요소

### 추천 — 도입

1. **Curator (auto skill pruning)**: 지금도 skill이 쌓이고 있음. 7일 idle 감지 + 30일 미사용 stale → archival 로직은 별도 스크립트로 cronjob 등록 가능. Lock Stack 비침범.

2. **3번째 프로필 추가**: 지금 Hermes1 (텔레그램 봇, com.hermes.bot) + Hermes2 (WebUI, Telegram bot 2) = 2개. 3번째 isolated 프로필을 추가하면 designer 전용 또는 researcher 전용 봇 분리 가능.

3. **Skills Hub 활용**: 공식 hub의 87개 built-in + 79 optional skill 중 우리에게 유용한 게 있을 수 있음. 검토 후 필요한 것만 install.

### 비추천 — 도입 불필요

1. **GEPA**: ICLR 2026 논문 레벨이지만, 우리는 이미 Lock Stack 엔진(bio_memory_engine, dreaming)이 유사 역할을 함. 게다가 GEPA는 PR 생성 방식이라 운영 비용 대비 효용 낮음.

2. **External memory providers (Mem0 등)**: 우리 Bio-Memory Engine이 L1/L2/L3를 전담하고 있고 Lock Stack이라 교체 불가. 외부 provider 추가는 경쟁 상태 유발.

3. **Claude Code 위임**: 우리 시스템은 DeepSeek API 전용이고, Claude Code는 Claude Max 구독 필요. 환경이 다름.

### 판단 보류 — 검토 필요

1. **acp_command (subagent 전송)**: 다른 CLI(GitHub Copilot 등)로 subagent 실행. 우리는 Hermes subagent만으로 충분한지, 다른 CLI의 이점이 있는지 검토 필요.

2. **Skins / Plugins**: 현재 CLI 사용성이 나쁘지 않음. 필요성을 느낄 때 도입.

## 5. 종합 평가

| 항목 | 판정 |
|------|------|
| 이미 대부분 구현됨 | 10/18 항목 이미 보유 |
| 우리가 더 잘하는 영역 | 8개 (메모리 계층, 검색, 학습, 라우팅) |
| **도입 추천** | **Curator (자동 skill 정리)** — 효과 확실, 비용 낮음 |
| 추가 검토 | 3번째 프로필, Skills Hub |
| 도입 불필요 | GEPA, External memory, Claude Code 위임 |

**결론**: 이 글이 소개하는 Hermes 공식 기능의 80%는 우리 시스템이 이미 갖고 있거나 더 잘 구현함. 유일하게 실질적 갭은 **Curator (자동 skill 정리)** — 이건 도입하면 즉시 효과 볼 수 있음. 나머지는 지금 상태 유지해도 무방.