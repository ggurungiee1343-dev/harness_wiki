# semantic_index.db 이력

> 생성일: 2026-06-05
> 위치: `wiki/00_Meta/semantic_index.db` (~1.3MB, SQLite + FTS5)
> 관리 모듈: `modules/semantic_engine.py`
> 최종 수정: 2026-06-03 (~~_이력.md 작성 시점 기준)

---

## 1. 개요

`semantic_index.db`는 **sentence-transformers 기반 벡터 검색 + FTS5 전문 검색**을 결합한 로컬 RAG 인덱스 DB. `FastEmbed`(`sentence-transformers/paraphrase-multilingual-mpnet-base-v2` 모델)로 임베딩을 생성하며, NPU 가속이 가능한 구조.

원래 **MacBot 전용**으로 설계되어 Hermes 시스템과 연동되었으나, 현재는 사실상 방치 상태에 가까움.

---

## 2. 현재 상태 (2026-06-05 기준)

### DB 상태
| 항목 | 값 |
|------|-----|
| 파일 크기 | ~1.3MB (SQLite) |
| 인덱싱된 문서 | 82개 |
| 마지막 인덱싱 | 2026-05-15 |
| 마지막 업데이트 (자동) | 2026-06-03 (수동 재인덱싱) |
| 00_Meta 폴더 인덱싱 | 제외됨 (`semantic_engine.py` line 67) |

### 구조
- **Dense 검색:** sentence-transformers 임베딩 (NPU 가속 가능)
- **Sparse 검색:** FTS5 전문 검색
- **결합:** RRF (Reciprocal Rank Fusion) — Dense + Sparse 점수 통합
- **벡터 차원:** 768차원 (paraphrase-multilingual-mpnet-base-v2)

### 연동 대상
| 컴포넌트 | 상태 |
|----------|------|
| `harness_agent.py` (line 166-170) | import 시도 → 실패 시 silent fallback |
| `bio_memory_engine.py` `recall()` (line 325-341) | SemanticEngine 호출 → 오류 시 키워드 fallback |
| `bio_memory_engine.py` `_promote_to_l2()` (line 216-222) | 모든 L1→L2 승격마다 임베딩 생성 호출 |
| `index_vault()` 자동 호출 | 주석 처리 (line 139) → 자동 재인덱싱 중단됨 |

---

## 3. 이슈 및 문제점

### 3.1 무음 실패 구조 (Silent Fallback)
- `harness_agent.py`에서 SemanticEngine import 실패 시 에러 로그 없이 무시
- 20일 이상 DB 업데이트가 없어도 사용자는 인지 불가
- `offline_consolidation` 등 주기적 작업도 DB에 반영 안 됨

### 3.2 리소스 부담
- `_promote_to_l2()`가 호출될 때마다 (memory write마다) 임베딩 생성 시도
- sentence-transformers 모델 상주 → 메모리 점유 (수백 MB 추정)
- wiki 문서 82개 인덱싱에 ~1.3MB → 문서 수 증가 시 급속 확장 가능

### 3.3 인덱스 방치
- 21일간 인덱스 업데이트 없음 (수동 재인덱싱 제외)
- `index_vault()` 주석 처리로 자동 인덱싱 완전 중단
- 새 문서/수정된 문서가 인덱스에 반영되지 않음

### 3.4 모델 의존성
- HuggingFace 모델 다운로드 필요 (paraphrase-multilingual-mpnet-base-v2)
- 모델 다운로드 실패 시 `semantic_engine.py` 전체가 동작 불능
- NPU 가속이 가능하나, MacBot 환경에서 실제 가속 여부 미검증

---

## 4. 장점 평가

### 4.1 최신 문서 검색 커버리지 (개선 시)
- RRF 기반 검색으로 Dense + Sparse 장점 결합
- 의미론적 검색 (키워드 불일치 시에도 유사 문서 검색 가능)
- FTS5로 정확한 키워드 매칭도 유지

### 4.2 기존 인프라 활용
- SQLite 기반 → 별도 DB 서버 불필요
- FastEmbed로 NPU 가속 가능 (설정만 하면)
- 이미 Hermes 시스템에 연동 코드 존재

### 4.3 Bio-Memory Engine 보완
- 키워드 기반 `recall()`만으로 부족한 의미론적 검색을 커버
- `_promote_to_l2()`에서 자동 임베딩 → L2 에피소드 간 관계 발견 가능

---

## 5. 평가 결론 (장점 vs 단점)

**단점이 장점을 상회**한다고 평가됨.

현재 시스템(Gemma4 + llama-server, 로컬 inference)에서 sentence-transformers 모델을 상주시키는 것은 리소스 대비 효용이 낮음. 특히:
1. 단 82개 문서를 위해 수백 MB 메모리 사용
2. 무음 실패 구조로 유지보수성이 낮음
3. 자동 재인덱싱 중단으로 실질적 가치 없음

### 추천 방향
| 옵션 | 설명 | 우선순위 |
|------|------|----------|
| **유지 포기** | semantic_index.db 및 SemanticEngine 연동 제거 | ★ 높음 |
| **키워드 기반 전환** | `recall()`을 순수 키워드/TF-IDF 기반으로 변경 | ★ 높음 |
| **Knowledge Mesh 대체** | `cross_reference_analyzer` (TF-IDF 기반)를 활용 | ★ 중간 |
| **개선 유지** | index_vault() 복구, silent fallback 제거, NPU 가속 설정 | ☆ 낮음 |

---

## 6. 참고: 이전 논의 세션 (2026-06-05 이전)

### 6.1 TagLinker 오류 수정 세션 (2026-06-03)
- `ingest_engine.py`에서 `TagLinker(vault_path=...)` 호출이 `tag_linker.py`의 `__init__` 시그니처와 불일치
- `TagLinker()` 인자 없이 호출하도록 수정 → 기본 `DB_PATH` (`~/.hermes/runtime/hermes_index.db`) 사용
- **semantic_index.db는 이 세션에서 언급되지 않음** — 수정 대상은 `hermes_index.db`

### 6.2 Memory Engine 분석 세션 (2026-06-03~04)
- Bio-Memory Engine L3 (`semantic_memory.json`)가 비어 있는 원인 분석
- L2→L3 승격 조건이 순수 개수 기반(`> 200`) → Hybrid Trigger(`> 100 OR > 1MB`)로 개선 제안
- `offline_consolidation`이 pruning만 하고 L3로 증류하지 않는 문제 발견
- 이 세션에서 `semantic_index.db`는 **본격적으로 논의되지 않음** — `semantic_memory.json`이 주제

### 6.3 Bio-Memory Engine 개선 지침서 분석 세션 (2026-06-05, 이 세션)
- "Bio-Memory Engine 메모리 계층 분석 지침서" 코드 대비 분석
- 지침서 내용 대부분 이미 구현되어 있음을 확인
- **유일한 누락:** `dreaming_v2.py` line 244 `procedural` 초기화 타입 불일치 (`[]` vs `{}`)
- `semantic_index.db`의 실질적 활용 가치에 대한 장단점 평가 본격 진행
- **최종 평가:** 유지 포기 또는 키워드 기반 전환 권장 (단점 > 장점)
- 결과물: `wiki/00_Meta/semantic_index.db_이력.md` (이 파일)

---

## 7. 관련 파일

| 파일 | 설명 |
|------|------|
| `wiki/00_Meta/semantic_index.db` | 실제 벡터 DB (SQLite) |
| `modules/semantic_engine.py` | SemanticEngine 클래스 (임베딩 + 검색) |
| `modules/bio_memory_engine.py` | Bio-Memory Engine (recall → SemanticEngine 연동) |
| `modules/dreaming_v2.py` | 실시간 캡처, L3 직접 누적 |
| `~/.hermes/runtime/memory/semantic_memory.json` | L3 메모리 (semantic patterns) |
| `~/.hermes/runtime/memory/episodic_memory.json` | L2 메모리 (83 entries, 1.7MB) |
| `~/.hermes/runtime/hermes_index.db` | TagLinker 기본 DB (ingest engine용) |

---

## 8. 결정 사항 (2026-06-05 기준)

- [ ] **유지 포기** — `semantic_index.db` 연동 제거
- [ ] **키워드 기반 전환** — `recall()` 순수 키워드/TF-IDF로 변경
- [ ] **Knowledge Mesh 대체** — `cross_reference_analyzer` 활용
- [ ] **개선 유지** — 현 상태 유지, 필요 시 재평가

> 현재 결정 대기 중. MJ님이 "안하는걸로"라고 한 상태이나, 평가 완료 후 추가 결정 필요.
