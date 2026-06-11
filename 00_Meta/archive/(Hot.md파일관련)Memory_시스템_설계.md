# Memory 시스템 설계 문서

> hot.md, memory.md, Journal의 역할과 정보 흐름을 정의합니다.
> Harness Agent의 Dreaming 작업의 기준 문서입니다.

---

## 문제 정의

**기존 문제점:**
- hot.md는 "한 일 목록"에 가까움 (작업 로그)
- 이 로그를 그대로 memory.md에 압축 저장하는 것은 의미 없음
- memory.md는 "실수를 방지하기 위한 핵심 정보"를 담아야 함

---

## 3단계 Memory 구조

### 1단계: hot.md (작업 캐시)
**역할:** 현재 진행 중인 작업의 모든 기록 (무제한 용량)

**저장 위치:** `wiki/00_Meta/hot.md`

**저장 대상:**
| 섹션 | 내용 |
|------|------|
| **Harness 내부 작업** | Harness가 직접 수행한 작업 (진행 중 + 완료) |
| **외부업무** | Antigravity Bot 작업 또는 MJ님이 수동 추가한 내용 |

**갱신:** 매 작업 후 증량 추가

**Dreaming 시:**
- 완료 항목 → Journal로 이동
- 핵심 요약 → memory.md에 추가
- 진행 중 항목 → 유지

---

### 2단계: memory.md (핵심 기억)
**역할:** Harness가 실수를 방지하고 연속성을 유지하기 위한 핵심 정보

**저장 위치:** `~/.hermes/memories/MEMORY.md`

**용량 제한:** 있음 (최대 2200chars 권장)

**저장 대상:**

#### A. 사용자 선호도 (Preferences)
```
- MJ님이 요청하는 방식의 변화
- "이제는 ~这种方式 선호"
- "~은 더 이상 하지 않기로 함"
```

#### B. 시스템 설정/변경 사항
```
- 위키 폴더 구조 변경
- 새로운 에이전트/봇 추가
- 경로 변경 (Obsidian Vault 경로 등)
```

#### C. 진행 중인 프로젝트 현황
```
- 프로젝트명, 현재 단계, 목표
- 주요 결정 사항
- 다음 행동 요약
```

#### D. 에러 및 해결 기록
```
- 발생한 에러와 해결 방법
- "이런 상황에서 이런 에러가 발생하면 이렇게 해결"
```

#### E. 반복 패턴 (Anti-patterns)
```
- "MJ님이 항상 이렇게 요청함"
- "이 방법은 피해야 함"
- "과거에 이로 인해 실수가 있었음"
```

**NOT 저장 대상 (삭제 대상):**
```
- 단순 작업 목록 (이미 Journal에 있음)
- 일회성 대화 내용
- 임시想法
- 이미 처리 완료된 작업의 세부 내용
```

---

### 3단계: Journal (완전한 기록)
**역할:** 일별 완전한 작업 기록

**저장 위치:** `wiki/30_Journal/{날짜}_업무일지.md`

**저장 대상:**
```
- 매일의 모든 작업 상세 내용
- Harness + Antigravity 작업 통합
- 대화의 전체 맥락
- 결론과 근거
```

**중복 처리:**
- Harness와 Antigravity가 같은 작업을 각각 기록하더라도
- Journal 작성 시 중복 항목은 1개로 합침

**갱신 주기:** 매일 밤 Dreaming 후 또는 프로젝트 완료 시

---

## Dreaming 프로세스

**실행:** 매일 밤 11시 (Cronjob)

**Dreaming 시 Telegram 제안 방식:**

```
1. Cronjob 실행
   ↓
2. hot.md 백업 생성 (hot.md.bak.{timestamp})
   ↓
3. hot.md 분석
   ↓
4. 처리草案 작성:
   - Journal에 추가할 완료 작업
   - memory.md에 추가할 핵심 요약
   - hot.md에서 삭제할 완료 항목
   ↓
5. Telegram으로 MJ님께 제안:
   """
   🌙 Dreaming 결과 (2026.05.08)

   다음 작업을 하려고 합니다:

   📝 Journal 추가:
   - Clippings 자동 분류 시스템 구축
   - Memory 시스템 재설계
   - Gemma4 파일 ingest (3개)

   💾 memory.md 갱신:
   - Memory 시스템 규칙 추가
   - 경로 설정 유지

   🗑️ hot.md에서 삭제:
   - 완료된 작업 5개 항목

   [실행] [수정] [취소]
   """
   ↓
6. MJ님 승인/수정/취소
   ↓
7. 승인 시:
   - Journal 작성 (중복 제거)
   - memory.md 갱신
   - hot.md 정리
   ↓
8. 오류 시:
   - hot.md.bak로 복원
   - MJ님께 알림
```

---

## 정보 흐름

```
Clippings에 파일 추가
    ↓
Harness가 처리 (분류, 이동, INDEX 갱신)
    ↓
hot.md에 기록 (Harness 내부 작업)
    ↓
Antigravity 작업 → hot.md (외부업무) 또는 MJ님이 수동 추가
    ↓
 Dreaming (매일 밤)
    ↓
 Telegram으로 처리 제안
    ↓
 MJ님 승인
    ↓
┌─────────────────────────────┐
│ Journal: 완료 작업 통합     │
│ memory.md: 핵심 요약 추가    │
│ hot.md: 완료 항목 삭제       │
└─────────────────────────────┘
```

---

## memory.md 템플릿

```markdown
# MJ님의 영구 메모리 (Harness 행동규범)

## 사용자 선호도 (Latest: YYYY-MM-DD)
- 응답 스타일: 간결하게, 장황한 설명 지양
- 언어: 한국어 only, 한자 사용 금지
- 승인 필요: 파일 생성/삭제, 시스템 변경 작업 전

## 시스템 설정 (Latest: YYYY-MM-DD)
- Obsidian Vault: /Users/bluesea/Applications/Mjobsidian/wiki/
- Clippings 경로: /Users/bluesea/Applications/Mjobsidian/Clippings/
- Wiki 폴더: 00_Meta, 10_AI_Automation, 20_Research, 30_Journal

## 진행 중인 프로젝트
- [[프로젝트명]]: 현재 단계 및 목표

## 에러 기록 (Anti-patterns)
- NVIDIA NIM DEGRADED 에러 → Gemini로 전환
- Harness 응답 없음 → gateway.pid 삭제 후 재시작

## 반복 패턴
- MJ님은 긴 대화 후 요약 선호
- 파일 경로 항상 확인 필요
```

---

## 핵심 원칙

> **memory.md는 "실수를 방지하기 위한 것"이다.**
> - "내가 기억해야 할 것"이 아니라 "내가 틀리기 쉬운 것"
> - 매번 다시 설명할 필요 없는 것은 memory에 넣지 않음
> - Journal과 hot.md에 있는 상세 내용은 그대로 두되, memory.md에는 압축 요약만

---

## Dreaming 안전장치

| 안전장치 | 설명 |
|----------|------|
| **사전 백업** | 처리 전 hot.md 복사본 생성 |
| **Telegram 제안** | 처리 전 MJ님께 확인 요청 |
| **복원 스크립트** | 오류 시 hot.md.bak로 복원 |

---

*최종 업데이트: 2026-05-08*
*Dreaming 프로세스 및 Telegram 제안 방식 추가됨*
*Cronjob 관리: [[Cronjob_관리]] 문서 참조*

---

## 🧠 하네스 v2.2 메모리 아키텍처 요약 (추가)

시스템이 고도화됨에 따라 메모리의 역할이 다음과 같이 이원화되었습니다.

### 1. `memory.json` vs `memory_engine.py` 차이
| 구분 | `memory.json` | `memory_engine.py` (및 memory.md) |
| :--- | :--- | :--- |
| **명칭** | **단기 대화 버퍼 (Short-term Buffer)** | **장기 지식 엔진 (Long-term Engine)** |
| **저장 데이터** | 최근 10~15턴의 원문 대화 내역 | 추출된 사실, 규칙, 업무일지 요약 |
| **유효 기간** | 일시적 (새로운 대화가 오면 밀려남) | 영구적 (위키에 기록됨) |
| **해결책** | 재부팅 후에도 "아까 하던 말"을 기억함 | 시간이 흘러도 "나의 취향"을 기억함 |

### 2. 하이브리드 메모리 운용 (해결책)
박사님의 지시와 시스템의 안정성을 위해 두 가지를 모두 사용합니다:
1.  **실시간 기록**: 모든 대화는 `HistoryManager`를 통해 `memory.json`에 즉시 기록되어 대화의 맥락을 유지합니다.
2.  **지능형 추출**: 대화 중 중요 정보는 `@기억` 명령을 통해 `memory_engine.py`가 `memory.md`에 영구 기록합니다.
3.  **정기 정리 (Dreaming)**: 매일 새벽 03:00에 `hot.md`를 분석하여 파편화된 정보를 `Journal`과 `memory.md`로 통합하여 지식을 선순환시킵니다.

*최종 업데이트: 2026-05-12 23:10 (Harness v2.2 하이브리드 메모리 아키텍처 반영)*