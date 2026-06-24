---
tags: []
---
# CLAUDE.md — Claude Code 세션 초기화 규칙
> 이 파일은 Claude Code 세션 시작 시 자동으로 읽힙니다.
> 관리 위치: `/Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/CLAUDE.md`
> 최종 업데이트: 2026-06-08

---

## 1. 세션 시작 시 필독 파일 (순서대로)

1. **`claude_briefing.md`** (현재 파일과 같은 폴더) — 시스템 전체 상태, 최근 변경, 미해결 버그
2. **`~/.hermes/constitution.local.md`** — 행동 규칙 전문 (경로 규칙, 금지 사항, 검증 루프)
3. **`guardrails.md`** (현재 파일과 같은 폴더) — 3대 관제 원칙, 금지 행동
4. **`USER.md`** (현재 파일과 같은 폴더) — MJ님 프로필, 선호도, 기술 스택
5. **`01_hot.md`** (현재 파일과 같은 폴더) — 현재 진행 중인 작업, 실시간 상태

---

## 2. 핵심 경로 (암기)

```
~/Applications/
├── Mjauto/Scripts/          ← 모든 Python 스크립트 (작업 루트)
│   ├── handlers/            ← 17개 텔레그램 명령어 핸들러
│   ├── modules/             ← 57개 전문 모듈
│   ├── hermes_local.py      ← Hermes1 봇 메인
│   ├── harness_agent.py     ← LLM 하네스 관제탑
│   └── send_telegram_msg.py ← 텔레그램 알림 발송
├── Mjobsidian/wiki/         ← Obsidian Vault (문서 저장소)
│   └── 00_Meta/             ← 시스템 메타 문서 (이 파일 위치)
└── venu/                    ← Hermes2/WebUI/Gateway 환경
```

---

## 3. 절대 수정 금지 (Lock Stack)

아래 파일은 **허락 없이 절대 수정하지 말 것**:
- `modules/cove_engine.py` (위치: `Scripts/cove_engine.py`)
- `modules/deriver_layer.py`
- `modules/dreamer_layer.py`
- `~/.hermes/constitution.local.md`

> **2026-06-23 Lock Stack 변경**: `bio_memory_engine.py` 잠금 해제 — SRP 분할 및 Dreaming 결함 #5 수정 완료. 분할 후 신규 파일(`vector_engine.py`)은 리팩토링 완료 시까지 잠금 불필요.

---

## 4. Claude Code 행동 원칙

### 수정 전 반드시
- 파일 전체 구조 파악 후 수정 (800줄 제한 인지, 분할 Read 사용)
- 수정 범위와 방법을 먼저 설명하고 **허락받은 후** 실행
- 기존 파일 덮어쓰기 전 내용 전체 확인

### 편집자 원칙 (Taste — 2026-06-08 추가)
- 기능 추가 전 **제거할 수 있는 것이 없는지 먼저 검토** ("No"가 먼저)
- `.bak` / `_old` / `_test` 임시 파일은 작업 완료 후 **즉시 삭제**
- 300줄 초과 파일 수정 시 **전체 구조 파악 후 Edit(부분 수정)만** 허용 — Write(전체 덮어쓰기) 금지
- 새 문서/스크립트 생성 전 동일 기능이 이미 있는지 확인

### 작업 완료 시 — 반드시 메타 7종 업데이트
- **`wiki/00_Meta/05_시스템 상태.md`** — 모든 코드 변경 이력 기록 (날짜/파일명/변경 내용/연결 구조/에러 진단 포인트)
- **`wiki/00_Meta/02_스크립트 정보.md`** — 신규 모듈·함수 추가 시 모듈 설명 + 에러 진단 포인트 추가, 모듈 카운트 업데이트
- 중요 결정은 `wiki/00_Meta/` 에 문서로 저장
- 알림 필요 시 `send_telegram_msg.py` 호출

### 메타 7종 업데이트 기준
| 파일 | 업데이트 트리거 |
|---|---|
| `05_시스템 상태.md` | 모든 코드 변경, 버그 수정, 새 기능 |
| `02_스크립트 정보.md` | 신규 모듈/함수, 모듈 개수 변화, 흐름 구조도 변경 |
| `06_에이전트_오류_및_재발방지_보고서.md` | 버그 수정, 예외 처리 추가 |
| `01_hot.md` | 진행 중 작업 상태 변경, **Lessons Learned 실시간 추가** |
| `03_시스템 인벤토리.md` | 새 패키지 설치, 환경 변경 |
| `00_Meta_지도.md` | 신규 문서 생성 |
| `claude_briefing.md` | 시스템 구조 대규모 변경 (자동: `/claude_brief`) |

### Lessons Learned 라우팅 규칙 (2026-06-23 추가)

"나중에 이걸 왜 이렇게 했지?" 라는 질문이 생길 것 같은 순간 → **즉시 01_hot.md Lessons Learned 테이블에 한 줄 추가**

| 상황 | 어디에 쓰나 | 형식 |
|---|---|---|
| 버그 원인 파악 + 재발방지 패턴 필요 | `06_에이전트_오류_및_재발방지_보고서.md` | 무거운 형식 (증상·원인·수정·재발방지) |
| 작업 중 발견한 비직관적 패턴·판단 근거·설계 이유 | `01_hot.md` → `## 💡 Lessons Learned` 테이블 | 한 줄 형식 (날짜 \| 분야 \| 교훈) |
| 아키텍처·모듈 설계 결정 | `06_에이전트_오류_및_재발방지_보고서.md` + Lessons Learned 양쪽 | 크로스 참조 |

**작성 원칙**: 채팅이 닫히기 전에 쓴다. Lessons Learned는 버그가 아니어도 쓴다. 나중에 같은 질문을 반복하지 않기 위해 쓴다.

### Lessons Learned vs 06번 보고서 — 역할 분리 원칙 (2026-06-23 확정)

두 시스템은 경쟁하지 않는다. **Lessons Learned는 06번의 요약 인덱스**다.

| | Lessons Learned (`01_hot.md`) | 06번 보고서 |
|---|---|---|
| **목적** | 빠른 캡처 — "나중에 왜 이렇게 했지?" 방지 | 깊은 기록 — 버그 재발방지 정식 문서 |
| **형식** | 한 줄 (날짜·분야·교훈) | 증상·원인·수정코드·재발방지 전체 |
| **타이밍** | 작업 중 즉석에서 | 버그 수정 완료 후 |
| **참조 시점** | 매 세션 자동 로드 → 즉시 참조 | "이 버그 왜 생겼지?" 코드 레벨 파볼 때 |
| **도구 연동** | Claude Code 세션 컨텍스트 | `/verify_harness` 등 진단 도구 참조 |

**흐름**: 버그 발생 → Lessons Learned 한 줄(즉시) → 06번 보고서 상세 기록(무겁게)

> 06번이 없으면 "왜 이렇게 고쳤는지" 코드 수준 근거가 사라진다.  
> Lessons Learned가 없으면 세션 시작마다 같은 실수를 반복한다.  
> **둘 다 영구 유지.**

### Lessons Learned 정리 정책 (2026-06-23 확정)

자동화 없음 — 로직 자체가 관리 부담이 됨.

**트리거**: `01_hot.md` Lessons Learned 테이블이 **30줄 초과 시** Claude가 세션 시작 때 "정리할까요?" 먼저 제안.

**정리 기준**:
| 조건 | 처리 |
|---|---|
| 모든 세션에서 반드시 알아야 하는 패턴 | CLAUDE.md로 승격 후 삭제 |
| 06번 보고서에 이미 상세 기록된 버그 패턴 | 삭제 |
| 3개월 이상 경과 + 더 이상 관련 없음 | 삭제 |
| 여전히 실수할 것 같은 패턴 | 유지 |

### 커스텀 스킬 (자연어 트리거)

| 사용자 발화 | 실행 스킬 | 동작 |
|---|---|---|
| "메타 업데이트해줘", "작업 내용 저장해줘", "문서 업데이트해줘" | `~/.hermes/skills/meta-update/SKILL.md` | 세션 작업 분석 → 관련 메타 7종 + 00_Meta 하위 파일 업데이트 |

> 새 스킬 추가 시 `wiki/00_Meta/hermes_harness_skill_모음.md`에도 함께 등록할 것.

### 응답 품질 원칙 (2026-06-11 추가)
- **핵심 먼저**: 첫 문장은 "무슨 일이 있었나 / 무엇을 발견했나"로 시작. 배경·옵션·계획은 핵심 이후에 배치
- **증거 기반 보고**: 완료 여부는 실제 툴 실행 결과로만 보고. 미확인 내용은 "아직 미확인"으로 명시
- **질문·사고 중엔 분석만**: MJ가 질문하거나 생각을 말할 때(실행 요청 없을 때)는 분석 결과만 보고. 수정·실행은 명시적 요청 후
- **이미 결정된 것 재논의 금지**: 대화에서 확정된 사실·결정을 다시 도출하거나 재검토하지 말 것

### 금지 행동
- `~/Applications/` 밖에 파일 생성/설치 금지
- Hermes1(`~/.hermes`)과 Hermes2(`~/.hermes2`) 경로 혼용 금지
- 추측성 답변 금지 — 파일 존재 여부는 반드시 직접 확인
- **Hermes1 봇을 `nohup`/수동 `python hermes_local.py`로 직접 실행 금지** (이중 인스턴스 → getUpdates Conflict → 상호 사망). 재시작은 launchd 경로만
- **`com.bluesea.hermes_local.plist.disabled` enable 금지** — 구버전(`~/hermes/` 경로). 정식은 `com.hermes.bot`(`Scripts/hermes_local.py`)

### Hermes1 봇 재시작 표준 절차 (2026-06-24 BOT-001 확정)
봇이 안 뜨거나 "이미 실행 중" 반복 시 — **반드시 이 순서로만**:
```bash
launchctl enable gui/$(id -u)/com.hermes.bot       # disabled 드리프트 해제
launchctl kickstart -k gui/$(id -u)/com.hermes.bot # 정식 재시작
pgrep -f "Scripts/hermes_local.py" | wc -l          # 1이어야 정상(이중 인스턴스 아님)
```
- 진단: `launchctl print gui/$(id -u)/com.hermes.bot | grep state`
- botwatch(`check_bot_alive.sh`)가 5분마다 자동 복구. `botwatch.log`에 `nohup 직접 실행` 보이면 수정 되돌려진 것 → 06번 BOT-001 참조

---

## 5. 주요 스크립트 활용 가이드

| 목적 | 사용 스크립트 |
|---|---|
| 서비스 상태 점검 | `Scripts/check_services.sh` |
| Hermes1 봇 재시작 | `launchctl enable gui/$(id -u)/com.hermes.bot && launchctl kickstart -k gui/$(id -u)/com.hermes.bot` |
| API 엔드포인트 확인 | `Scripts/model_endpoint_check.sh` |
| WebUI 캐시 삭제 | `Scripts/clear_webui_cache.sh` |
| venv 패치 확인 | `Scripts/check_venv_patches.sh` |
| 텔레그램 알림 발송 | `python3 Scripts/send_telegram_msg.py "메시지"` |
| Obsidian 타임스탬프 복구 | `python3 Scripts/wiki_auto_stamper.py` |
| 모델 전환 | `switch-model got` / `switch-model deepseek` |

---

## 6. 시스템 성장 원칙 (2026-06-08 확정)

> **이 창(Claude Code)에서 작업하면 시스템은 성장한다.**  
> Scripts/wiki 수정 → 코드·지식 성장 / 텔레그램 대화 → L1/L2 성장 / Dreaming 버튼 → L3 성장  
> 세 가지를 모두 활용하면 모든 계층이 성장한다.

- `bio_memory_engine.dream()`은 로컬 LLM 없이 **NVIDIA/DeepSeek API**로 작동
- WebUI 하단 모델 버튼(Hermes2)과 텔레그램 LLM 모드(`llm_mode.txt`)는 **완전 별개**
- 상세 구조: `Claude_Code_Hermes_통합_아키텍처.md` 참조

---

## 7. 이 파일 자동 업데이트

`/claude_brief` 텔레그램 명령어 실행 시 `claude_briefing.md`가 갱신됩니다.
`CLAUDE.md` 자체는 시스템 구조가 바뀔 때만 수정합니다.

---
*관리: `/Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/CLAUDE.md`*
*연관: `claude_briefing.md`, `constitution.local.md`, `guardrails.md`, `USER.md`*

---
*최종 업데이트: 2026-06-24 22:42*
