# 📋 Hermes Agent Kanban (칸반) 다중 에이전트 협업 가이드

Hermes Agent `v0.12.0` 버전부터 탑재되어 `v0.14.0`까지 지속 개발된 **Kanban**은 로컬 SQLite 데이터베이스를 기반으로 작동하는 강력한 **다중 에이전트 협업 시스템**입니다. 

여러 개의 에이전트 프로필(Profiles)을 생성하여 각각 전문 분야를 부여하고, 칸반 보드를 통해 병렬로 태스크를 처리하거나, 자동으로 태스크를 분석/분할하여 협업하도록 할 수 있습니다.

---

## 1. ⚙️ 칸반 기본 개념 및 구조

Hermes Kanban은 다음과 같은 요소들로 구성됩니다:
* **보드 (Board)**: 프로젝트나 워크스트림별 개별 칸반 보드 (기본값: `default` 보드, SQLite DB 파일로 관리됨).
* **태스크 (Task)**: 할 일, 데이터, 의존성 관계, 할당 프로필, 진행 상황 로그를 담은 개체.
* **프로필 (Profile)**: 작업을 실제로 수행하는 주체 (예: `analyst`, `trader`, `verifier` 등 각각 다른 LLM 및 설정을 가짐).
* **작업공간 (Workspace)**: 각 태스크가 격리되어 실행되는 디렉터리 경로.

---

## 2. 🛠️ 칸반 핵심 명령어 가이드

### 2.1. 초기화 및 보드 관리
칸반 데이터베이스를 만들고 관리합니다 (최초 1회 실행 필요).
```bash
# 칸반 데이터베이스 생성 (idempotent, 기존 데이터가 있으면 안전하게 유지됨)
hermes kanban init

# 생성된 보드 목록 확인
hermes kanban boards list

# 새 칸반 보드 생성
hermes kanban boards create my_project

# 활성화할 칸반 보드 전환
hermes kanban boards switch my_project
```

### 2.2. 태스크 관리
보드 내에서 할 일(Task)을 생성, 조회, 수정합니다.
```bash
# 1. 새 태스크 생성
hermes kanban create "백테스트 코드 디버깅" --body "V2.2 코드의 지표 계산 로직 오류 점검"

# 2. 태스크 목록 확인 (Todo, In Progress, Done 등 상태별 시각화)
hermes kanban list
# 또는 축약형
hermes kanban ls

# 3. 특정 태스크 상세 조회 (진행 로그, 댓글, 의존성 포함)
hermes kanban show <TASK_ID>

# 4. 태스크 강제 완료 처리
hermes kanban complete <TASK_ID>

# 5. 태스크 보관(Archive) 및 정리
hermes kanban archive <TASK_ID>
```

### 2.3. 태스크 연결 및 의존성 (Dependency) 설정
특정 태스크가 완료된 후에만 다음 태스크가 실행되도록 의존성 그래프를 생성합니다.
```bash
# parent_task가 완료되어야 child_task가 활성화(Ready)되도록 링크 연결
hermes kanban link <PARENT_TASK_ID> <CHILD_TASK_ID>

# 의존성 해제
hermes kanban unlink <PARENT_TASK_ID> <CHILD_TASK_ID>
```

---

## 3. 🤖 다중 에이전트(Multi-Profile) 협업 환경 구축 및 실습

칸반의 핵심은 **프로필(Profile)**을 통한 역할 분담입니다. 각기 다른 강점을 가진 AI 에이전트들이 알아서 일감을 가져가 처리하는 방식입니다.

### 단계 1: 다중 프로필 생성
예를 들어 분석 전담 에이전트(`analyst`)와 실행 전담 에이전트(`trader`) 프로필을 생성합니다.
```bash
# 1. 분석가 프로필 생성 (Claude-3.5-Sonnet 등 분석 모델 지정 가능)
hermes profile create analyst
# 2. 트레이더 프로필 생성
hermes profile create trader
```

### 단계 2: 태스크 할당 (Assign)
특정 에이전트에게 일을 지정하거나, 에이전트가 알아서 가져가게 할 수 있습니다.
```bash
# analyst 프로필에게 특정 태스크 수동 할당
hermes kanban assign <TASK_ID> analyst

# 할당 해제 (다시 공용 풀로 되돌리기)
hermes kanban reclaim <TASK_ID>
```

### 단계 3: 백그라운드 디스패처(Dispatcher) 및 데몬 구동
게이트웨이가 구동 중이면 백그라운드에서 에이전트들이 자동으로 칸반 보드의 태스크들을 스캔하고 가져가 병렬로 실행합니다.
```bash
# Hermes 게이트웨이 데몬 시작 (에이전트 스케줄러가 포함됨)
hermes gateway start
```
* 활성화된 에이전트들이 `Ready` 상태의 일감을 하나씩 원자적으로 클레임(`claim`)하여 격리된 작업공간에서 코딩, 분석, 리포트 작성 등의 작업을 동시에 수행합니다.

---

## 4. 🔥 고급 기능: Swarm (에이전트 스웜) 자동 생성

Hermes Agent는 여러 에이전트가 한 번에 모여 하나의 거대한 문제(예: 복잡한 코드 작성 또는 리포트 작성)를 협업하여 푸는 **스웜(Swarm)** 기능을 지원합니다.

```bash
# 스웜 그래프 자동 생성
hermes kanban swarm --workers 3 --prompt "나스닥 우량주 30개 종목의 단기/중기 백테스트 데이터 분석 보고서 작성 및 교차 검증"
```
위 명령어를 실행하면 칸반 보드 내부에 아래와 같은 다중 에이전트 작업 파이프라인 그래프가 자동으로 그려지고 실행됩니다.
1. **Parallel Workers (3명)**: 작업 내용을 3개로 분할하여 동시에 실행 및 분석.
2. **Verifier (검증 에이전트)**: 3명의 작업자가 낸 결과를 교차 검토하고 논리적 오류 검출.
3. **Synthesizer (종합 에이전트)**: 최종 검증된 내용을 하나로 종합하여 고품질의 완성형 결과물 도출.

---

## 5. 🔍 칸반 모니터링 및 진단
실시간으로 진행 상황을 관찰하고 디버깅할 수 있습니다.
```bash
# 보드의 태스크 현황 및 담당자별 업무 로드 통계 조회
hermes kanban stats

# 실시간 태스크 이벤트 및 에이전트 작업 실시간 스트리밍 관찰
hermes kanban watch

# 특정 태스크의 에이전트 실행 로그 확인
hermes kanban log <TASK_ID>

# 오래된 아카이브 작업공간 및 임시 파일 정리 (용량 확보)
hermes kanban gc
```

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
