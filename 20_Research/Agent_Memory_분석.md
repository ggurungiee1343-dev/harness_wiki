# Agent-Memory 분석

> 출처: https://agent-memory.dev
> 저장일: 2026-05-08
> 태그: #memory #agent #hot-mdhots.md와 비교

---

## 개요

**Agent-Memory:** AI 코딩 에이전트를 위한 영구 메모리 레이어
**GitHub:** 2,436 stars
**벤치마크:** 95.2% R@5 (LongMemEval-S)

**핵심 슬로건:**
"CAPTURE EVERY SESSION. RECALL IN MILLISECONDS. RUN ANYWHERE."

---

## 핵심 기능

| 기능 | 설명 |
|------|------|
| **Triple-stream 검색** | BM25 + Vector + Knowledge Graph |
| **12 Auto-hooks** | Tool call, Prompt, Stop 등 자동 캡처 |
| **Hourly Consolidation** | 중복 병합, 정체 행 제거 |
| **Knowledge Graph** | 엔티티/관계 자동 추출 |
| **JSONL Session Import** | 세션 Replay |
| **P2P Sync** | 다중 에이전트 메모리 공유 |
| **Obsidian Export** | Markdown으로 내보내기 |
| **MCP Support** | 51개 MCP tools |
| **Zero External DB** | 단일 프로세스 |

---

## Agent-Memory vs hot.md 비교

| 항목 | Agent-Memory | 우리 hot.md |
|------|-------------|-------------|
| **저장 방식** | Triple-stream (BM25 + Vector + Knowledge Graph) | 단순 텍스트 파일 |
| **검색 속도** | P50 < 20ms | 파일 읽기 (느림) |
| **자동 캡처** | 12개 Auto-hooks | 수동 기록 |
| **자동 정리** | Hourly sweep | 수동 (Dreaming) |
| **지식 그래프** | 엔티티/관계 자동 추출 | 없음 |
| **복원력** | 세션 Replay (JSONL) | 없음 |
| **외장 DB** | 없음 | 없음 |
| **MCP 지원** | 51개 | 없음 |

---

## 우리 시스템 강점 (hot.md)

- ✅ 단순함 — 텍스트 파일로 즉시 사용
- ✅ Harness 통합 — MEMORY.md와 연동
- ✅ Obsidian 호환 — wiki에서 직접 편집/검색
- ✅ Dreaming 연동 — Cronjob + Telegram 제안
- ✅ 외부업무 섹션 — Harness/Antigravity 작업 분리

---

## 설치 장단점

### 장점 ⭐

1. **실시간 메모리 캡처** — 작업 중 자동 기록
2. **的高速 검색** — 토큰 비용 절감 (92% 감소)
3. **Knowledge Graph** — 노트 간 숨겨진 연결 자동 발견
4. **Obsidian 연동** — 메모리를 vault로 내보내기
5. **다중 에이전트** — 여러 AI 간 메모리 공유

### 단점 ⚠️

1. **추가 의존성** — Node.js 런타임 필요
2. **복잡성 증가** — 현재 단순架构에서 탈피
3. **학습 곡선** — III Engine, Hooks, Workers 개념 필요
4. **중복 기능** — hot.md + Dreaming + Clippings로 일부 구현됨
5. **리소스 사용** — 백그라운드 서버 실행

---

## 우리 시스템과의 차이

```
우리 시스템                    Agent-Memory
─────────────────────────────────────────────────
hot.md (수동/반자동)    ←→     자동 캡처 (12 hooks)
MEMORY.md (핵심 요약)   ←→     자동 압축 (Hourly sweep)
Journal (일별 기록)     ←→     JSONL Session Replay
Connector (수동 연결)   ←→     Knowledge Graph 자동 추출
```

---

## 결론

| 상황 | 추천 |
|------|------|
| **현재架构 유지** | hot.md + Dreaming으로 충분 |
| **향후 확장** | Agent-Memory 도입 고려 |
| **단순нача** | Obsidian PDF++ Plugin 먼저 |

**현재는 hot.md로 충분. 나중에 다중 에이전트 운영하거나 검색 성능이 문제가 되면 Agent-Memory 도입 검토.**

---

## 관련 문서

- [[Memory_시스템_설계]]
- [[hot]]
- [[멀티에이전트_구축_계획]]

---

*최종 업데이트: 2026-05-08*
*저장 이유: 추후 Agent-Memory 도입 시 참조*