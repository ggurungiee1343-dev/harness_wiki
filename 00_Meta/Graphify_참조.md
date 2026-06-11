# Graphify 전체 정보

> `graphifyy==0.8.28` 패키지를 기반으로 하는 vault 지식 그래프 엔진.  
> ENCYCLOPEDIA.md에 통합된 동일 내용을 별도 참조용으로 정리함.

---

## 1. 패키지 정보

- pip: `graphifyy==0.8.28`, import: `import graphify`
- 의존성: networkx (자동 설치)
- 설치 위치: `/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages/graphify/`
- 필수 제약: `parallel=False` — Hermes Agent 환경(Python 3.11 spawn 제한) 때문

## 2. API 함수 & 호출 파이프라인

| 단계 | 함수 | 설명 |
|------|------|------|
| 1 | `collect_files(vault_path)` | vault 내 .md 파일 수집 |
| 2 | `extract(files, parallel=False)` | 문서 간 관계 추출 (tree-sitter) |
| 3 | `build_from_json(extraction, directed=True)` | NetworkX 방향 그래프 생성 |
| 4 | `god_nodes(G, top_n=10)` | 연결 가장 많은 허브 문서 |
| 5 | `surprising_connections(G, top_n=5)` | 예상치 못한 교차 연결 |
| 6 | `cluster(G)` | 커뮤니티 클러스터링 |
| 7 | `to_html(G, communities, html_path)` | 시각화 HTML |

파이프라인 순서: `collect_files -> extract -> build_from_json -> god_nodes + surprising_connections + cluster -> to_html`

## 3. 텔레그램 연동 (`/vault graph`)

| 항목 | 내용 |
|------|------|
| 핸들러 | `handlers/_vault.py` → `_vault_graph()` (270-374라인) |
| 명령어 | `/vault graph` |
| 동작 | 모든 .md 수집 → extract → build → god_nodes(10개) → 고립노드 → cluster → to_html → surprising_connections(5개) → 리포트 전송 |
| graph.html | `/Users/bluesea/Applications/Mjobsidian/graph.html` (vault 루트) |
| 오류 처리 | ImportError → 패키지 미설치 메시지, 기타 예외 → traceback |

보고되는 항목: 노드/엣지/커뮤니티/고립 문서/허브 노드 8개/놀라운 연결 5개

## 4. graph.html 생성

`graphify.to_html(G, communities, str(html_path))` 한 줄로 생성. vault 루트에 graph.html 파일 생성. Python 3.11+의 spawn 제약으로 `parallel=False` 필수. graph.html은 plotly 기반 인터랙티브 시각화.

## 5. output 파일들

| 파일 | 위치 |
|------|------|
| `graph.html` | vault 루트 (`~/Applications/Mjobsidian/graph.html`) |
| `GRAPH_REPORT.md` | `graphify-out/` (서브디렉토리 이관 완료) |
| `graph.json` | vault 루트 |
| `.graphify_*` / `_graphify_chunk_*` | vault 루트 (미삭제 잔여물) |

## 6. 다른 프로그램과의 연결성

| 연결 대상 | 방식 |
|-----------|------|
| wiki_manager.py | `graphify-out/GRAPH_REPORT.md` 읽어서 지식망 컨텍스트로 사용 |
| constitution.local.md | §3.4 Graphify 규칙 (v1.3, 2026-06-02) |
| ENCYCLOPEDIA.md | Graphify 섹션 문서화 완료 |
| GUIDE.md | Graphify LOW 할일 → 완료 전환 |
| vault_scanner.py | 같은 vault 분석 계열 (직접 그래프 연동 없음) |
| hermes_index.db (FTS5) | 별도 시스템 — graphify와 무관 |
| start_llama.sh | graphify와 무관 (LLM 서버) |

## 7. CLI 수동 실행

- 빠른 구조 분석: `graphify update /Users/bluesea/Applications/Mjobsidian`
- AI 심층 분석: `graphify extract /Users/bluesea/Applications/Mjobsidian --backend gemini`
- 둘 다 API 키/요금 소모 없음 (tree-sitter 기반)

## 8. 기존 테스트 스크립트

- `_run_fulltest_graphify.py`: 62줄, 순수 graphify 독립 테스트 (collect → extract → build → cluster → to_html → god_nodes + 요약 json 출력)
- `_test_graphify.py`, `_check_graphify.py`: 이미 삭제 완료

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
