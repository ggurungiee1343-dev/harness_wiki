# Hermes 메모리 레이어 개선 분석서

> 작성일: 2026-06-21
> 근거: Rob Pike 5 Rules + TAOUP (Eric Raymond) 17 Rules + Exceeds AI 생산성 역설
> 대상: bio_memory_engine / context_assembler / consolidation 파이프라인

---

## 1. 두 글에서 Hermes에 적용한 핵심 원칙

### Exceeds AI — AI 코딩 에이전트 생산성 역설

> "Delayed failure — silent corruption that doesn't show up until much later"

| 글의 주장 | Hermes 현실 |
|---|---|
| AI 코드의 버그는 30~90일 후 터짐 | L2 episodic 54항목 미처리 → 지금은 조용함, 나중에 context 품질 저하 |
| 검증 오버헤드가 시니어를 19% 느리게 만듦 | context_assembler가 7개 소스 항상 조립 → LLM 응답 느려짐 |
| 측정 없는 AI 코드 = tech debt factory | assemble_context() 소요 시간 측정 없음 |

### TAOUP — Unix 철학 적용

| 규칙 | Hermes에 위반된 곳 | 개선 |
|---|---|---|
| **Rule of Representation** | L3 patterns[]가 카테고리 없이 누적 | SemanticMemory를 {category: []} dict로 |
| **Rule of Separation** | consolidation 정책(언제)과 메커니즘(어떻게)이 dreamer_layer에 혼재 | POLICY 상수 분리 |
| **Rule of Modularity** | bio_memory + cove + context_assembler + memory_refinement 상호 임포트 | 단방향 파이프라인 |
| **Rule of Simplicity** | context_assembler가 7개 소스 항상 전부 조립 | 3 필수 + 키워드 감지 시 선택 |
| **Rule of Robustness** | L2 파일 쓰기 중 crash 시 손상 위험 | Atomic write (os.replace) |
| **Rule of Transparency** | consolidation 결과를 볼 방법 없음 | health_check() + 단계별 로그 |

---

## 2. 실제 문제점 3개

### 문제 1 — L2→L3 증류 정지 (Delayed Failure)

```
현상:
  consolidator_state.json → 마지막 실행 시간 불명
  episodic_memory.json → 54항목 이상 미처리로 쌓임
  Dreaming 폐기(2026-05-27) 후 consolidation 경로 없음

원인:
  dreamer_layer.py + dreaming_v2.py + bio_memory_engine.py
  복잡한 상호 임포트 → Dreaming 폐기 시 통째로 고아(orphan)됨
  → "Bugs tend to collect in glue" (TAOUP)

결과:
  L2가 무한 성장 → hybrid_recall() 느려짐
  context window 낭비 → LLM 응답 품질 저하
  지금은 조용하지만 30~90일 후 체감 (Exceeds AI)
```

### 문제 2 — L3 카테고리 없는 무작위 누적

```
현상:
  semantic_memory.json의 patterns[] 배열에 무작위 누적
  카테고리 없음 → hybrid_recall()이 전체 탐색

원인:
  "Fold knowledge into data" 원칙 위반
  데이터 구조가 단순(list)해서 로직이 복잡해짐

결과:
  recall 쿼리마다 O(n) 전체 탐색
  해양법 쿼리에 주식 패턴이 섞여 들어옴
```

### 문제 3 — context_assembler 과부하

```
현상:
  assemble_context()가 항상 7개 소스 조립
  "날씨 알려줘" 질문에도 briefing.md + wiki + L2/L3 전부 실행

원인:
  Rule of Simplicity 위반
  Rule of Parsimony 위반 ("필요할 때만 크게")

결과:
  불필요한 소스 조립 → context 과부하 → LLM 느려짐
  소요 시간 측정 없음 → 병목 파악 불가 (Pike Rule 2 위반)
```

---

## 3. 개선 파일 3개

### `memory_schema.py` — 데이터 구조 재설계

**핵심: Rule of Representation — 지식을 데이터에 접어넣기**

```python
# 기존: 단순 dict 배열, 판단 로직이 함수에 분산
episodic = [{"content": "...", "importance": 3.0}, ...]

# 개선: EpisodicEntry 데이터클래스에 판단 기준 내장
@dataclass
class EpisodicEntry:
    importance: float = 3.0
    ttl_days:   int   = 30

    @property
    def is_worth_storing(self) -> bool:
        return (len(self.content) >= 30
                and self.importance >= 2.5
                and not self._is_ephemeral())

    @property
    def is_expired(self) -> bool:
        return datetime.now() > created + timedelta(days=self.ttl_days)
```

**SemanticMemory: list → {category: list}**

```python
# 기존: patterns[] 배열 (전체 탐색 O(n))
{"patterns": ["해양법 심판...", "주식 삼돌이...", ...]}

# 개선: 카테고리별 dict (카테고리 필터 탐색 O(n/k))
{
  "maritime_law": ["해양법 심판...", ...],
  "stock":        ["주식 삼돌이...", ...],
  "system":       ["하네스 config...", ...],
  "personal":     [...],
  "research":     [...],
  "general":      [...],
}
```

카테고리 자동 분류도 로직 대신 키워드 테이블로:
```python
CATEGORY_KEYWORDS = {
    "maritime_law": ["해양", "선박", "심판", "도선", ...],
    "stock":        ["주식", "삼돌이", "농사", "매수", ...],
    ...
}
# classify_category()는 이 테이블을 스캔하기만 함 — 로직 없음
```

### `memory_consolidator.py` — L2→L3 증류 파이프라인

**핵심: Rule of Separation — 정책과 메커니즘 분리**

```python
# 정책(Policy) — 한 곳에서만 수정
POLICY = {
    "promote_importance_min": 4.0,   # L3 승격 기준
    "drop_retention_below":   0.15,  # 삭제 기준
    "max_l2_items":           200,   # L2 상한
}

# 메커니즘(Mechanism) — 정책을 읽어서 실행만
def consolidate():
    # Step1. 만료 제거
    # Step2. 저보유율 제거
    # Step3. importance >= POLICY["promote_importance_min"] → L3
    # Step4. L2 다이어트
```

**단방향 파이프라인 (Rule of Modularity)**:
```
L2 로드 → 만료 제거 → 저보유율 제거
         → L3 승격 → L2 다이어트 → 상태 저장
```
기존 dreamer_layer ↔ bio_memory_engine ↔ dreaming_v2 3방향 순환 임포트 → 단방향으로

**crontab 추가 (Delayed Failure 방지)**:
```bash
# 매일 새벽 4시 자동 증류
0 4 * * * cd ~/Applications/Mjauto/Scripts && .venv/bin/python -m modules.memory_consolidator >> logs/consolidation.log 2>&1
```

### `context_assembler_v2.py` — 컨텍스트 조립 단순화

**핵심: Rule of Simplicity — 복잡성은 필요할 때만**

```
기존: 7블록 항상 전부
  sys_prompt + wiki + style + history15 + L2/L3 + Resolver + briefing + 날씨

개선: 3필수 + 키워드 감지 시 선택
  [항상] sys_prompt + L3(카테고리필터) + history10
  [system 키워드] briefing.md 추가
  [wiki 키워드]   wiki 검색 추가
  [날씨 키워드]   날씨 스크래핑 추가
```

**트리거도 데이터로 (Rule of Representation)**:
```python
TRIGGERS = {
    "weather": ["날씨", "기온", "weather", ...],
    "system":  ["하네스", "hermes", "시스템", ...],
    "stock":   ["주식", "스캔", "삼돌이", ...],
}
# 로직 없이 키워드 테이블 스캔만
```

**소요 시간 측정 추가 (Pike Rule 2)**:
```python
t0 = time.perf_counter()
# ... 조립 ...
elapsed = time.perf_counter() - t0
logger.info(f"[context_assembler_v2] {block_count}블록 | {elapsed*1000:.0f}ms")
```

**적용 방법 (1줄만)**:
```python
# harness_agent.py에서
from modules.context_assembler   import assemble_context  # 기존
from modules.context_assembler_v2 import assemble_context  # 변경
```

---

## 4. 집에서 적용하는 순서

```bash
# Step 1. 파일 복사
cp memory_schema.py       ~/Applications/Mjauto/Scripts/modules/
cp memory_consolidator.py ~/Applications/Mjauto/Scripts/modules/
cp context_assembler_v2.py ~/Applications/Mjauto/Scripts/modules/

# Step 2. 현재 상태 확인 (측정 먼저 — Pike Rule 2)
cd ~/Applications/Mjauto/Scripts
.venv/bin/python -m modules.memory_consolidator --health

# Step 3. L3 포맷 마이그레이션 (기존 patterns[] → {category: {}})
.venv/bin/python -m modules.memory_consolidator --migrate

# Step 4. 증류 dry-run (실제 저장 안 함)
.venv/bin/python -m modules.memory_consolidator --dry-run

# Step 5. 실제 증류 실행
.venv/bin/python -m modules.memory_consolidator

# Step 6. context_assembler 교체 (1줄)
# harness_agent.py 열고:
# from modules.context_assembler import assemble_context
# → from modules.context_assembler_v2 import assemble_context

# Step 7. crontab 추가
crontab -e
# 추가:
# 0 4 * * * cd ~/Applications/Mjauto/Scripts && .venv/bin/python -m modules.memory_consolidator >> logs/consolidation.log 2>&1
```

---

## 5. 기대 효과

| 항목 | 기존 | 개선 후 |
|---|---|---|
| L2 미처리 항목 | 54개+ (영원히 쌓임) | 매일 새벽 4시 자동 정리 |
| L3 탐색 속도 | O(n) 전체 탐색 | O(n/카테고리수) 필터 탐색 |
| context 블록 수 | 항상 7개 | 쿼리에 따라 3~7개 |
| 병목 파악 | 불가 | ms 단위 로그 |
| consolidation 상태 | 불투명 | health_check() 즉시 확인 |
| 데이터 손상 위험 | 쓰기 중 crash 위험 | Atomic write |

---

## 6. 메타 7종 업데이트 대상

| 문서 | 업데이트 내용 |
|---|---|
| `00_Meta_지도.md` | memory_schema.py / memory_consolidator.py / context_assembler_v2.py 신규 등록 |
| `02_스크립트_정보.md` | modules/ 3개 파일 설명 추가, consolidation crontab 추가 |
| `Bio_Memory_Engine_가이드.md` | L2→L3 새 파이프라인 설명 추가 |
| `메모리_파일_명세서.md` | SemanticMemory 카테고리 구조 반영 |
| `하네스_업그레이드_로드맵.md` | L3 증류 정지 해결 완료로 상태 변경 |
| `01_hot.md` | 이 개선 완료 항목 추가 |

---

*작성: 2026-06-21 | 근거: Rob Pike 5 Rules + TAOUP 17 Rules + Exceeds AI*
