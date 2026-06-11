# Claude Code ↔ Hermes 통합 아키텍처 및 시스템 성장 구조

**작성일:** 2026-06-08  
**작성 배경:** Claude Code 세션에서 도출된 핵심 결론 — 어떤 도구로 작업해도 하네스 시스템이 성장하는 메커니즘 정리  
**핵심 결론:** Claude Code 포함 어떤 작업을 해도 시스템은 성장한다. 여기에 주기적 Dreaming을 더하면 모든 계층이 성장한다.

---

## 1. 전체 시스템 성장 구조도

```
┌─────────────────────────────────────────────────────────┐
│                   작업 입력 경로                          │
│                                                         │
│  텔레그램 Hermes ──→ harness_agent.py                   │
│  WebUI (Hermes2) ──→ hermes-webui + gateway             │
│  Claude Code CLI ──→ 파일시스템 직접 접근                │
└──────────────┬──────────────────────┬───────────────────┘
               │                      │
               ▼                      ▼
┌─────────────────────┐   ┌──────────────────────────────┐
│  런타임 메모리 계층  │   │     파일 기반 지식 계층        │
│                     │   │                              │
│  L1 단기 캐시       │   │  Scripts/*.py  ← 코드 개선   │
│  L2 에피소딕        │   │  wiki/00_Meta/ ← 문서 축적   │
│  L3 장기 의미론     │   │  skills/*.md   ← 스킬 성장   │
│  hot.md 실시간 상태 │   │  soul.md       ← 정체성      │
└──────────┬──────────┘   └──────────────────────────────┘
           │
           ▼ (🌙 Dreaming 버튼)
    dream(llm_func=현재API)
    → L1/L2/L3 통합 압축
    → hot.md 갱신
```

---

## 2. Claude Code가 시스템을 성장시키는 경로

### ✅ 성장하는 것 (파일로 남는 것)

| 작업 유형 | 성장 경로 | 영속성 |
|---|---|---|
| Scripts 수정/생성 | 하네스 코드 자체 개선 | 영구 |
| wiki/00_Meta 문서 업데이트 | 시스템 지식 누적 | 영구 |
| 버그 발견 및 수정 | 다음 실행부터 반영 | 영구 |
| CLAUDE.md → claude_briefing.md | 다음 세션에서 인식 | 세션 간 |

### ❌ Claude Code가 직접 닿지 않는 것

| 항목 | 이유 |
|---|---|
| Hermes 런타임 메모리 (L1/L2/L3) | 텔레그램 대화에서만 축적됨 |
| bio_memory_engine 실시간 학습 | harness_agent.py 통해서만 업데이트 |
| 대화 컨텍스트 히스토리 | Hermes 세션 내부에서만 관리 |

**→ 두 경로는 파일시스템을 통해서만 연결된다.**

---

## 3. bio_memory_engine 성장 메커니즘

### LLM 의존성 — 로컬 LLM 불필요

```python
# harness_agent.py 613번 줄
res = await memory.dream(history.history, llm_func=get_llm_response)

# get_llm_response = 현재 활성 모드 자동 선택
# ~/.hermes/llm_mode.txt 값에 따라 결정
# 현재: "GPT OSS 120B" (NVIDIA API)
```

**로컬 LLM(Qwen)이 꺼져도 DeepSeek 또는 NVIDIA API로 dream() 작동.**

### 계층별 성장 조건

| 계층 | 성장 조건 | LLM 필요 여부 |
|---|---|---|
| L1 단기 캐시 | 대화 발생 시 자동 | ❌ 불필요 |
| L2 에피소딕 | 중요도 점수 3.0 이상 시 자동 승격 | ❌ 불필요 |
| L3 장기 의미론 | dream() 실행 시 | ✅ 필요 (현재 NVIDIA) |
| hot.md | dream() 실행 시 갱신 | ✅ 필요 |

### LLM 모드 선택 기준

```
WebUI 하단 모델 선택 버튼
    → ~/.hermes2/ 설정 (Hermes2 전용)
    → Claude Code, 텔레그램에 무관

텔레그램 Hermes + dream()
    → ~/.hermes/llm_mode.txt 파일만 읽음
    → 텔레그램 /mode 버튼으로만 변경
    → 현재: GPT OSS 120B (NVIDIA)
```

**WebUI 버튼 ≠ 텔레그램 LLM 모드. 완전히 별개.**

---

## 4. Dreaming 버튼 = L3 성장의 핵심 트리거

```
텔레그램 🌙 Dreaming 버튼
    ↓
handlers/_base.py → confirm_dreaming 승인
    ↓
handlers/_memory.py → cmd_dreaming()
    ↓
bio_memory_engine.dream(history, llm_func=get_llm_response)
    ↓
L1/L2 망각곡선 정리 + L3 승격 + hot.md 갱신
```

**수동 트리거가 자동 스케줄보다 품질이 높다.**  
대화가 충분히 쌓인 시점에 누르는 것이 최적. 새벽 자동 실행은 빈 히스토리 낭비 가능성 있어 미채택.

---

## 5. 옵시디언 메타 폴더 내 Soul/Skill 등 성장

```
wiki/00_Meta/
├── soul.md (SOUL.md)         ← 정체성/페르소나 — 수동 편집으로 성장
├── skills/*.md               ← 스킬 정의 — Claude Code 또는 수동으로 개선
├── constitution.local.md     ← 행동 헌법 — 신중하게 수동 업데이트
├── USER.md                   ← 사용자 프로필 — 환경 변화 시 업데이트
├── 01_hot.md                 ← 실시간 상태 — dream() + 수동으로 갱신
└── claude_briefing.md        ← 시스템 브리핑 — /claude_brief 명령으로 생성
```

이 파일들은 Hermes 런타임과 Claude Code 세션이 공유하는 **공통 지식 베이스**다.  
Claude Code가 이 파일들을 읽고 수정하면 → 다음 Hermes 세션도 그 변경을 인식한다.

---

## 6. 전체 성장 결론

```
어떤 작업 경로를 쓰든:

Claude Code로 작업
    → Scripts 코드 개선 ✅
    → wiki 문서 축적 ✅
    → 다음 Claude Code 세션 인식 (CLAUDE.md → briefing) ✅

텔레그램 Hermes로 대화
    → L1/L2 자동 성장 ✅
    → 스킬/soul/핸들러 활용 ✅

🌙 Dreaming 버튼 주기적으로 누름
    → L3 장기 기억 성장 ✅
    → hot.md 갱신 ✅

= 모든 계층 완전 성장
```

**권장 루틴:**
- 일상 대화/자동화: Hermes WebUI 또는 텔레그램
- 코드 개선/분석: Claude Code
- 기억 압축: Dreaming 버튼 (대화 많이 쌓인 시점)
- 시스템 브리핑 갱신: `/claude_brief` 텔레그램 명령

---

## 7. Claude Code ↔ Hermes 연결 방법 (미래 구현 후보)

현재는 **파일시스템만 공유**하는 구조. 향후 필요 시 구현 가능한 연동:

| 방법 | 구현 위치 | 비고 |
|---|---|---|
| 텔레그램 자연어 트리거 | `natural_language_router.py` | "클로드야 해줘" → `claude -p` 서브프로세스 |
| llm_interface.py MODE_CLAUDE | `llm_interface.py` | `subprocess.run(["claude", "-p", prompt])` |
| hybrid_router.py 코딩/분석 라우팅 | `hybrid_router.py` | 작업 유형 판단 후 Claude Code 위임 |

**현재는 불필요.** Claude Pro 할당량 소모, 2-5초 오버헤드, 스트리밍 미지원 등 제약 있음.  
지금 이 창(Claude Code)에서 직접 작업하는 것이 가장 효율적.

---

*작성: Claude Code 세션 (2026-06-08)*  
*관련 파일: `CLAUDE.md`, `claude_briefing.md`, `bio_memory_engine.py`, `harness_agent.py`*  
*연관 메타: `비서_시스템_메타_문서_비교_정의.md`, `00_Meta_지도.md`, `05_시스템 상태.md`*
