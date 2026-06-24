---
brief: brief
description: Hermes v9.2는 최신 업그레이드로 모델 붕괴 차단과 ClawTrojan 방어 등 주요 보안 기능을 구현하였다. 그러나
  Forget 정책 부재와 Context offload 부재 등 핵심 메모리 관리 기능이 아직 미흡하여 적용에 제한이 있다. 따라서 TencentDB
  Agent Memory와의 연동은 제한적으로 권장되며, 추가 개선이 필요하다.
tags:
- 20_Research
- AI security
- Hermes
- TencentDB
- context-offload
- forget-policy
- ingested
- memory management
---
# TencentDB Agent Memory → Hermes v9.2 적용 가능성 재평가
**분석일시:** 2026-06-13  
**Hermes 버전:** v9.2 (2026-06-12 대규모 업그레이드 완료)  
**평가자:** Claude (수정됨)

---

## 🎯 핵심 결론: **제한적 적용 권장**

### 이전 분석과의 변경사항
Hermes v9.2는 **2026-06-12 논문 기반 대규모 업그레이드** 완료 후, 이미 다음을 구현했습니다:

| 기능 | 이전 상태 | 현재 상태 | TDAI 필요성 |
|------|---------|---------|-----------|
| Model Collapse 차단 | ❌ | ✅ LLM→L2 경로 완전 차단 | ↓ 낮음 |
| ClawTrojan 방어 | ❌ | ✅ wiki 오염 탐지 | ↓ 낮음 |
| 도구 궤적 기록 | ❌ 산발적 | ✅ trace_log.jsonl | 🟡 부분 활용 |
| 협업 규칙 구현 | ❌ | ✅ 7개 규칙 코드 적용 | ↓ 낮음 |
| Forget 정책 | ❌ | ⚠️ 여전히 부재 | ✅ 높음 |
| Context offload (symbolic) | ❌ | ❌ | ✅ 높음 |

---

## 📊 Hermes v9.2 메모리 현황 (최신)

### 구현된 것
```
L1: harness_memory.json (작업 캐시 ← hot.md)
    ├─ bio_memory_engine.py (118행) — 관리
    ├─ deriver_layer.py (187행) — 유도
    └─ ✅ 동작 중

L2: episodic_memory.json (중기 경험)
    └─ ⚠️ memory.md는 Dreaming 폐기로 정적화 (2026-05-27)

L3: semantic_memory.json (장기 개념)
    └─ ✅ 활성, 하지만 isolated

보안: ✅ Model Collapse 차단 (L2 ← LLM 경로 완전 폐쇄)
    ✅ ClawTrojan 방어 (wiki 오염 탐지)

도구 기록: ✅ trace_log.jsonl (전체 도구 궤적)
```

### 여전히 부재한 것
```
❌ Forget 정책 (메모리 블로트 리스크 동일)
❌ Symbolic short-term compression (Mermaid canvas)
❌ L0→L3 완전 드릴다운 체계
❌ 자동 Persona 생성 (Dreaming 비활성화 상태)
❌ Embedding-based semantic recall (BM25 없음)
```

---

## 🔄 Hermes v9.2 내 TDAI 적용의 "필요성" vs "효과"

### A. 긴급 필요도 (낮음 → 이미 해결)

❌ **Model Collapse** — 이미 L2 ← LLM 경로 차단  
❌ **ClawTrojan** — 이미 wiki 오염 탐지 구현  
❌ **협업 규칙 미흡** — 이미 7개 규칙 코드화 (history_manager, response_handler, skill_auditor 등)

### B. 중장기 필요도 (높음 → 여전히 미해결)

✅ **Forget 정책 부재**
- 현황: episodic/semantic 모두 append-only (누적)
- TDAI 기여: LTM 계층화로 자동 정리 파이프라인 제공
- 효과: 메모리 갱신 충돌 감지, retention policy 자동 적용

✅ **도구 로그 폭발 (현재 문제 심화)**
- 현황: trace_log.jsonl 기록하지만, harness_memory.json에는 여전히 verbose 저장
- TDAI 기여: Mermaid symbolic offload (refs/*.md 외부 저장)
- 효과: 현재 inference lag 개선, context 압박 완화
  - Gemma4 26B: 현재 context 포화도 높음 → Mermaid offload로 10~20% 개선 예상

✅ **Persona 자동 갱신 불가**
- 현황: memory.md 정적화 (Dreaming 폐기)
- TDAI 기여: L2 Scenario → L3 Persona 자동 생성 파이프라인
- 효과: 장기 사용 패턴 학습, /persona 명령어 유용성 복원

---

## 🛠️ 구체적 적용 시나리오

### 시나리오 1: 최소 개입 (1-2주, 추천)

**목표:** 도구 로그 폭발 해결만  
**구현:**

```python
# harness_memory.json 저장 로직 수정
# 변경 전:
{
  "tool_calls": [
    {
      "name": "search",
      "input": "...",
      "output": "...very long result... (수천 글자)"
    }
  ]
}

# 변경 후 (TDAI 영감):
{
  "tool_calls": [
    {
      "node_id": "tool_search_001",
      "name": "search",
      "input": "...",
      "output_ref": "refs/tool_search_001.md"  # 외부 저장
    }
  ]
}

# refs/tool_search_001.md (external)
# 풀 결과 저장 (지속성 보장)
```

**비용:**
- bio_memory_engine.py: +30행 (파일 오프로드 로직)
- deriver_layer.py: +20행 (node_id 추적)
- 기존 L1/L2/L3 구조 유지

**효과:**
- harness_memory.json 크기 50~70% 감소
- context window 압박 완화
- inference lag 10~15% 개선 (Gemma4 추정)

---

### 시나리오 2: 중간 개입 (3-4주)

**목표:** Forget 정책 + Persona 재활성화  
**구현:**

```python
# episodic_memory.json에 retention policy 추가
# 변경 후:
{
  "memories": [
    {
      "id": "epis_001",
      "content": "...",
      "created_at": "2026-06-01",
      "last_accessed_at": "2026-06-13",
      "access_count": 15,
      "ttl_days": 30,  # TDAI 영감: automatic expiry
      "score": 0.75
    }
  ],
  "persona": {
    "preferences": [...],
    "last_updated_at": "2026-06-12",
    "sources": ["scenario_001", "scenario_002"]  # drill-down link
  }
}
```

**비용:**
- episodic_memory.py (신규): 50~80행 (TTL 관리)
- semantic_memory.py (수정): +40행 (Persona 재활성화)
- retention worker: +60행 (주기적 정리)

**효과:**
- 메모리 블로트 원천 차단
- L2→L3 업데이트 충돌 감지 (벡터 거리 기반)
- /persona 명령어 복구

---

### 시나리오 3: 완전 도입 (6-8주, 비권장)

**목표:** 전체 L0~L3 계층화 + Embedding 통합  
**구현:**

```
기존 Hermes (L1~L3 JSON)
    ↓
+ TDAI 전체 스택 (SQLite + embedding)
    ↓
hybrid_router.py에 embedding recall 추가
    ↓
context_assembler에 retrieval 로직
```

**비용:**
- SQLite 도입 (새로운 의존성)
- embedding 모델 필요 (로컬 또는 API)
- 기존 JSON 마이그레이션 (데이터 손실 리스크)
- 통합 테스트 2-3주

**리스크:**
- 🔴 기존 trace_log.jsonl과의 중복/충돌
- 🔴 마이그레이션 중 메모리 손실 위험
- 🔴 새로운 의존성 추가 (유지보수 부담)

**권장하지 않는 이유:**
- Hermes v9.2는 이미 핵심 보안 & 협업 기능 구현 완료
- 남은 문제는 도구 로그 폭발 + Forget 정책 뿐
- 이 둘은 TDAI 전체 스택 없이 경량 수정으로 충분

---

## 📋 Hermes v9.2 기존 구조 vs TDAI

### 적용 가능성 매트릭스

| 기능 | Hermes 구현 | TDAI 제공 | 호환성 | 우선도 |
|------|-----------|---------|-------|-------|
| L0 Conversation 기록 | ✅ trace_log.jsonl | ✅ L0 raw logs | 🟢 완벽 | 낮음 |
| L1 단기 메모리 | ✅ harness_memory.json | ✅ (+ offload) | 🟢 완벽 | 🔴 높음 |
| L2 에피소딕 | ✅ episodic_memory.json | ✅ (+ TTL) | 🟡 부분 | 🟡 중간 |
| L3 시맨틱 | ✅ semantic_memory.json | ✅ (+ Persona) | 🟡 부분 | 🟡 중간 |
| Symbolic offload | ❌ | ✅ Mermaid refs/ | 🟢 신규 | 🔴 높음 |
| Forget 정책 | ❌ | ✅ TTL/LRU | 🟢 신규 | 🔴 높음 |
| Embedding recall | ❌ | ✅ sqlite-vec | 🟡 선택 | 낮음 |
| Persona auto-gen | ⚠️ 폐기됨 | ✅ L2→L3 | 🟢 복구 | 🟡 중간 |

---

## 🎯 최종 권장안: "TDAI 영감의 경량 수정"

### 이름: **Hermes Memory Refresh (v9.2.1)**

기존 Hermes v9.2 구조를 유지하되, TDAI의 **핵심 아이디어 3가지**를 도입:

#### 1️⃣ Symbolic Offload (refs/)
```
harness_memory.json (L1 경량화)
  ├─ node_id로 도구 호출 링크
  └─ refs/*.md에 풀 결과 저장 (지속성)
```
**영향:**
- 파일 2개 (+ 기존 구조)
- bio_memory_engine.py +30행
- **효과: context 50~70% 축소, inference lag 10~15% 개선**

#### 2️⃣ Retention Policy (TTL)
```
episodic_memory.json에 ttl_days 필드 추가
retention_worker.py (신규) — 주 1회 정리
  ├─ 30일 미접근 memories 아카이브
  └─ access_count 기반 scoring
```
**영향:**
- episodic_memory.py +40행
- 신규 worker 60행
- **효과: 메모리 크기 안정화, 갱신 충돌 제거**

#### 3️⃣ Persona Reactive (L2→L3)
```
semantic_memory.json.persona 자동 갱신
trigger: episodic_memory 변경 시
source: 최근 5개 에피소드 → Persona 요약
```
**영향:**
- semantic_memory.py +50행
- persona_synthesizer.py (신규) 80행
- **효과: /persona 복구, 장기 패턴 학습**

---

### 구현 로드맵

#### Phase 1 (주 1-2: 긴급)
```bash
# Symbolic Offload (도구 로그 폭발 해결)
- bio_memory_engine.py에 ref 저장 로직 추가
- test: refs/*.md 생성 확인
- test: context 크기 감소 측정
```

#### Phase 2 (주 2-3)
```bash
# Retention Policy
- episodic_memory.py에 TTL 필드 추가
- retention_worker.py 작성
- test: 만료된 record 아카이브 확인
```

#### Phase 3 (주 3-4)
```bash
# Persona Reactivation
- persona_synthesizer.py 작성 (기존 Dreaming 코드 참고)
- semantic_memory.py에 trigger 추가
- test: /persona 명령어 정상 작동 확인
```

---

## ⚠️ 주의사항 & 리스크

### 회피할 사항 (현재 상황에서)
- ❌ SQLite 도입 (trace_log.jsonl과 중복)
- ❌ Embedding 모델 추가 (현재 inference lag가 더 긴급)
- ❌ 전체 JSON→DB 마이그레이션 (데이터 손실 리스크)

### 모니터링 포인트
- ✅ refs/*.md 크기 폭증 감시 → 자동 정리 필요 시 주기 조정
- ✅ retention_worker 실행 시간 → 매월 1GB+ 메모리 정리 예상
- ✅ persona_synthesizer 응답 시간 → LLM 호출 비용 고려

---

## 📈 기대 효과 (정량)

| 지표 | 현재 | Phase 1 이후 | Phase 1+2+3 이후 |
|------|------|------------|----------------|
| harness_memory.json 크기 | ~2-3MB | ~0.5-1MB | 0.3-0.8MB |
| episodic_memory.json 크기 | ~5MB (증가 중) | ~5MB (안정화) | ~3-4MB |
| context 점유율 (%) | 70-80% | 50-60% | 40-50% |
| inference lag (초) | 3-5s | 2.5-4s | 2-3s |
| /persona 명령어 | ❌ 작동 불가 | ⚠️ 정적 | ✅ 동적 갱신 |
| Forget 정책 | ❌ | ⚠️ 부분 | ✅ 완전 자동 |

---

## 🎬 결론

### "TDAI 전체 도입" vs "경량 수정"
| 항목 | TDAI 전체 | 경량 수정 (권장) |
|------|----------|--------------|
| 구현 시간 | 6-8주 | 3-4주 |
| 의존성 증가 | 높음 (SQLite, embedding) | 낮음 (Python stdlib) |
| 기존 코드 영향 | 높음 (마이그레이션) | 낮음 (+200행 정도) |
| 즉시 효과 | 61% 토큰 감소 (논문 벤치) | 50-70% context 축소 |
| 리스크 | 중간 (마이그레이션) | 낮음 (덧셈식) |
| Hermes 철학 부합 | 🟡 부분 (DB 도입) | 🟢 완벽 (경량 stateless) |

### 최종 권장
**"TDAI 영감의 경량 수정" (Hermes Memory Refresh v9.2.1)**
- Symbolic offload + Retention + Persona reactivation
- 3-4주 구현, 기존 철학 유지, 즉시 효과
- v9.4 로드맵에 통합 가능

**만약 중장기 (3-6개월)에 여유가 생기면:**
- 그때 TDAI 전체 스택 평가 고려
- 현재는 "빌드업" 단계

---

*분석자 주: Hermes v9.2는 이미 상당히 진화했습니다. TDAI의 가치는 "보안 & 협업" 이 아니라 "메모리 효율성 & 자동화"에 있습니다. 따라서 아이디어만 차용하는 경량 접근이 가장 현실적입니다.*

---
*최종 업데이트: 2026-06-23 22:30*
