---
tags: [scanned, 20_Research]
---


조사 완료했습니다. 결과를 정리해드립니다.

---

## Hermes1 vs Hermes2 리소스 공유 분석(2026.05.25 10:15)

### ✅ 이미 공유 중인 것
| 항목 | 경로 | 상태 |
|------|------|------|
| **LLM 모드 상태** | `~/.hermes/llm_mode.txt` | ✅ 양쪽 봇이 읽고 씀 |
| **Obsidian Vault** | `/Users/bluesea/Applications/Mjobsidian/` | ✅ 양쪽 접근 가능 |
| **Scripts 경로** | `/Users/bluesea/Applications/Mjauto/Scripts/` | ✅ Hermes2 config에 `extra_paths` 등록됨 |

### ❌ 아직 공유 안 되는 핵심 항목 (공유해야 할 것)

#### 1️⃣ **SOUL.md / Constitution / 성격 파일** ← **가장 중요**
- Hermes1: `~/.hermes/memory/SOUL.md` — 봇의 정체성/영혼
- Hermes2: **이 파일을 전혀 참조하지 않음**
- → Hermes2가 같은 성격/규칙으로 동작하게 하려면 반드시 필요

#### 2️⃣ **Bio-Memory 시스템 (L1~L3)**
| 파일 | 경로 | 용도 |
|------|------|------|
| `bio_memory_config.json` | `~/.hermes/memory/bio_memory_config.json` | 중요도 규칙, 감정 패턴 |
| `episodic_memory.json` | `~/.hermes/memory/episodic_memory.json` | L2 경험 기억 (487KB) |
| `semantic_memory.json` | `~/.hermes/memory/semantic_memory.json` | L3 의미 기억 |

- Hermes1: 3계층 Bio-Memory 엔진으로 읽고 씀
- Hermes2: Gateway 내장 메모리를 사용 → 완전히 **별도 메모리 공간**
- → **두 봇이 같은 기억을 공유하지 못함.** Hermes1이 Dreaming으로 정리한 내용이 Hermes2에 반영 안 됨

#### 3️⃣ **Hot Topics / 상태 정보**
| 파일 | 경로 |
|------|------|
| `memory.md` | `Applications/Mjobsidian/wiki/00_Meta/memory.md` |
| `hot.md` | `Applications/Mjobsidian/wiki/00_Meta/hot.md` |
| `시스템 상태.md` | `Applications/Mjobsidian/wiki/00_Meta/시스템 상태.md` |

- Hermes1: Dreaming으로 주기적 업데이트
- Hermes2: **전혀 읽지 않음**

#### 4️⃣ **end.sh 훅 (세션 종료 처리)**
- `~/.hermes/hooks/end.sh` — 세션 종료 시 `open-loops.md` 업데이트 + Telegram 알림
- 현재 **Hermes1만** `atexit`으로 등록되어 있음
- Hermes2가 종료될 때 이 훅이 실행 안 됨 → **Open-Loops 기록 누락**

#### 5️⃣ **Configuration 공유**
| 항목 | Hermes1 | Hermes2 |
|------|---------|---------|
| `.env` (토큰) | `~/.hermes/.env` | `~/.hermes2/.env` (별도) |
| 허용 사용자 ID | `config.py`에 하드코딩 | `.env`에서 로드 |
| API 키 (DeepSeek/OpenRouter) | 각각 별도 환경변수 | 각각 별도 환경변수 |

#### 6️⃣ **로그 통합**
- Hermes1: `Scripts/hermes_launchd.log`, `hermes_launchd.error.log`
- Hermes2: `.hermes2/logs/bot.log`, `.hermes2/logs/gateway.log`
- → 문제 발생 시 **어디 로그를 봐야 할지 분산됨**

---

### 📋 공유 권장 우선순위

| 순위 | 항목 | 공유 방법 제안 | 영향 |
|------|------|---------------|------|
| ⭐⭐⭐ | **SOUL.md + Constitution** | Hermes2 Gateway context/system prompt에 주입 | 두 봇 동일 성격/규칙 |
| ⭐⭐⭐ | **Bio-Memory (L1~L3)** | Hermes2가 `~/.hermes/memory/` 공유 참조 | 두 봇 같은 기억 공유 |
| ⭐⭐ | **Hot topics / 상태** | Hermes2 시작 시 Obsidian 상태 파일 로드 | 현재 상황 인식 |
| ⭐⭐ | **end.sh 훅** | Hermes2 launchd `ExitCoded` 훅으로 등록 | Open-Loops 완전성 |
| ⭐ | **로그 경로 통일** | 둘 다 `~/.hermes/logs/` 아래 통합 | 디버깅 편의 |
| ⭐ | **공유 .env** | 민감 정보는 각자, 공유용은 `~/.hermes/` | 중복 관리 해소 |

---

**결론:** SKILL.md 외에 **메모리 시스템 공유**와 **SOUL.md/Constitution 공유**가 가장 중요합니다. 특히 Bio-Memory는 Hermes1이 지금까지 쌓아온 487KB의 경험 기억과 3계층 메모리 구조인데, Hermes2가 이걸 몰라서 같은 질문에 다른 답을 할 가능성이 큽니다.

어떤 항목을 우선 처리할까요? 위 리스트에서 골라주시면 구체적 구현 방안을 바로 제시하겠습니다.

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
