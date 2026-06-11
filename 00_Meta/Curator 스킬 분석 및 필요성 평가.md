---
tags: [ingested, 20_Research, curator, skill-management, hermes, agent-created, archive, usage-analysis, automation]
description: "현재 Hermes 시스템의 Curator 기능이 실제로 필요한지 분석한다. ~/.hermes/와 venu/.hermes2/ 디렉토리의 SKILL.md 파일 현황을 비교하여 사용률과 중복 여부를 평가한다. 10개의 스킬 중 대부분이 지속 사용 중이어서 Curator의 아카이브 기능이 실질적 효용이 낮음을 확인한다."
brief: "brief"
---



---

## Curator, 우리한테 필요한가?

**현재 skill 현황 (실제 데이터 기준)**:

| 항목 | ~/.hermes/ | venu/.hermes2/ |
|------|-----------|----------------|
| 디렉토리 수 | 30개 | 7개 |
| 실제 SKILL.md 파일 | **0개** | **10개** |
| Curator backup | 없음 | 있음 (1회, 06-01) |
| Curator run | 0회 (시드만) | 4회 |

**~/.hermes/**는 30개 디렉토리가 있지만 SKILL.md가 0개입니다. brains, diagramming, gardening 등 카테고리 디렉토리만 있고 내용물이 없음 = hub에서 install만 하고 agent-created는 아예 없음.

**venu/.hermes2/**는 10개 SKILL.md 중 `obsidian` skill이 2개(중복), 나머지는 각 1개씩. 총 9개 unique skill. 이 중 Curator가 대상으로 삼는 `agent-created` skill은 우리가 직접 만든 것들인데, 사실 대부분 hub에서 내려받거나 edit-existing-files처럼 필수적인 것들.

**Curator가 할 일**: 10개 중 30일/90일 미사용 찾아서 archive. 근데 이 skill들은 계속 사용 중임 (오늘도 software-development-lifecycle, obsidian 로드함).

---

## 판단

| 항목 | 평가 |
|------|------|
| **규모** | 10개 skill. 수동으로 관리 가능. |
| **정리할 대상** | `obsidian` 중복 1개 — 근데 이것도 직접 삭제 가능 |
| **미사용 skill** | 전부 최근 7일 내 사용. archive 대상 없음 |
| **백업 필요성** | 이미 git으로 vault 관리 중 |
| **자동화 필요성** | 지금 규모에서는 오버헤드 |

**도입 불필요.**

이유:
1. skill이 10개뿐이라 수동 관리로 충분
2. Curator가 자동으로 정리해도 archive할 대상이 없음
3. Curator fork는 agent idle 2시간 후에 백그라운드에서 돌아가는데, 우리 시스템은 항상 active할 가능성 높음. fork가 잘 안 뜰 수 있음
4. Curator backup은 zip 스냅샷인데, 우리는 git으로 파일 관리 중이므로 git이 이미 backup 역할

**필요해질 조건**: skill이 50개 이상으로 불어나고, 30일 이상 안 쓴 skill이 10개 이상 쌓일 때. 지금은 아님.

---

추가로, ENCYCLOPEDIA.md에는 넣지 않는 게 낫습니다. 보류 기능 목록에 넣자니 적극적으로 미는 기능이 아니고, 사용법만 기록하자니 우리가 안 쓰는 기능 설명이 문서만 비대하게 만듦. 필요해질 때 추가해도 늦지 않음.