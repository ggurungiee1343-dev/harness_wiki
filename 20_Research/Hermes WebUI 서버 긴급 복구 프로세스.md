---
tags: [ingested, 20_Research, hermes-webui, server-recovery, python-path, process-conflict, background-fork, telegram-bot, system-diagnosis]
description: "Hermes 2 텔레그램 봇 기동 과정에서 자원 경합으로 종료된 hermes-webui 인프라의 최종 진단 결과와 백그라운드 영구 안착을 위한 복구 트랙을 요약한다. 시스템 전역 파이썬 경로 파손과 프로세스 명칭 혼선이 주요 장애 원인으로 분석된다. 표준 복구 절차를 통해 기존 웹 스택 자원을 소멸시키고 정적 에셋 포트와 백엔드 엔진을 독립된 백그라운드 트랙으로 격리한다."
brief: "summary"
---

## 🖥️ Hermes WebUI 서버 긴급 복구 프로세스 요약

Hermes 2 텔레그램 봇(`@Ulsan_Antigravity_bot`) 기동 과정에서 자원 경합으로 인해 종료되었던 **차기 웹 UI(hermes-webui)** 인프라의 최종 진단 결과와 백그라운드 영구 안착을 위한 복구 트랙 요약입니다.

### 1. 장애 원인 분석 (Root Cause)

- **시스템 전역 파이썬 경로 파손**: 전역 경로인 `/usr/local/bin/python3`가 디바이스 상에서 유실되거나 파손되어 표준 명령어 구동 시 `zsh: no such file or directory` 에러를 냈습니다.
    
- **프로세스 명칭 혼선**: `server.py`라는 동일한 실행 파일명이 **Hermes 2 텔레그램 봇**과 **WebUI 백엔드** 양측에 모두 존재하여, 프로세스 강제 종료 및 자원 할당 단계에서 인지 왜곡과 포트 충돌이 발생했습니다.
    

### 2. 표준 복구 절차 (Standard Operating Procedure)

기존에 꼬여있던 웹 스택 자원을 완전히 소멸시키고, 정적 에셋 포트(8000)와 백엔드 엔진을 상호 독립된 백그라운드 트랙으로 격리 포크(Fork)하는 명령어 세트입니다.

#### [1단계] 기존 웹 UI 잔여 프로세스 완전 소멸

메모리에 엉겨 붙어 있는 레거시 인스턴스의 잔해를 SIGKILL(-9) 플래그로 완전히 청소합니다.

Bash

```
pkill -9 -f "hermes-webui"
```

#### [2단계] 작업 디렉터리 이동 및 백업 네트워크 포트 기동

차기 UI 프로그램이 실재하는 전용 디렉터리로 이동한 뒤, 정적 리소스 바인딩을 위한 http 스택을 8000번 포트에 독립 상주 시킵니다.

Bash

```
cd /Users/bluesea/Applications/hermes-webui/
nohup python3 -m http.server 8000 > webui_net.log 2>&1 &
```

#### [3단계] 전용 가상환경(venv) 기반 백엔드 구동 (자동 연동 트랙)

전역 파이썬 파손 우회를 위해 검증된 전용 가상환경 런타임(`/Users/bluesea/Applications/venu/venv/bin/python`)을 접두어로 지정하여 메인 웹 서버를 안전하게 깨웁니다.

Bash

```
nohup /Users/bluesea/Applications/venu/venv/bin/python /Users/bluesea/Applications/hermes-webui/server.py > webui_launchd.log 2> webui_launchd.error.log &
```

### 3. 복구 상태 최종 검증 및 모니터링

정적 서버와 백엔드 엔진이 커널 메모리에 정상 안착했는지 팩트 체크하는 도구입니다.

- **웹 UI 런타임 상주 맵 확인**:
    
    Bash
    
    ```
    ps aux | grep -E "http.server|hermes-webui" | grep -v grep
    ```
    
- **기동 성공 메트릭 (Fact)**:
    
    - 정적 에셋 서버: **`PID 89086`** ── `state = SN` (대기 상태 안착)
        
    - 웹 UI 백엔드: **`PID 89088`** ── 가상환경 런타임 바인딩 및 상주 성공
        
## 진짜 Hermes WebUI 서버 긴급 기동 프로토콜

`hermes-webui` 패키지는 `~/Applications/hermes-webui/`에 실재하며, 웹 서비스의 표준 엔트리포인트를 주입해야 합니다. 아래 명령어를 통째로 복사하여 터미널에 실행해 주십시오.

Bash

```
pkill -9 -f "hermes-webui"
cd /Users/bluesea/Applications/hermes-webui/
nohup python3 -m http.server 8000 > webui_net.log 2>&1 &
sleep 1
ps aux | grep -E "http.server|hermes-webui" | grep -v grep
```

_(※ 만약 hermes-webui 디렉터리 내부에 고유한 Node.js 기반 구동 스펙(`npm run dev`)이나 파이썬 벡엔드 파일이 실재한다면, 실행 후 `cat webui_net.log`를 통해 드러나는 인터페이스를 보고 즉각 2차 조율하겠습니다.)_

====================
### 완벽하게 교정된 다중 에너 가동 인벤토리 맵 (Final Core Map)

현재 박사님의 Mac Studio 커널 메모리 상에 상호 충돌 없이 완벽한 독립 트랙으로 격리 구동 중인 3대 에이전트 인스턴스의 최종 물리 장부입니다.

| **인스턴스 명칭**      | **상주 PID**  | **인터페이스 / 봇**                   | **매핑 모델**             | **홈 경로 및 런타임**                 |
| ---------------- | ----------- | ------------------------------- | --------------------- | ------------------------------ |
| **Hermes 1**     | **`88993`** | 텔레그램 (메인 봇)                     | gpt-oss-120b (NVIDIA) | `~/.hermes` / 전역 Python3       |
| **Hermes 2**     | **`89037`** | 텔레그램 (`@Ulsan_Antigravity_bot`) | MiniMax-M2.7 (독자 API) | `~/.hermes2` / `venu/venv` 파이썬 |
| **Hermes WebUI** | **`89088`** | 차기 웹 브라우저 UI                    | 하이브리드 라우터             |                                |


======> 최종 정리

## 🖥️ Hermes WebUI 서버 최종 복구 절차 요약

Hermes 1/2 텔레그램 봇 기동 과정에서 포트 및 자원 충돌로 인해 크래시(`FATAL: Another server is already responding`)가 발생했던 **차기 웹 UI(hermes-webui)** 인프라의 최종 복구 가이드입니다.

### 1. 핵심 장애 원인 (Root Cause)

- **8787 네트워크 포트 충돌**: 기존에 완전히 종료되지 않은 `server.py` 인스턴스 또는 백그라운드 프로세스가 WebUI의 표준 포트인 **`8787` 포트를 독점 점유**하고 있어 중복 바인딩 실패 에러가 발생했습니다.
    
- **환경 설정 경로(HERMES_HOME) 혼선**: WebUI는 텔레그램 2호기(`.hermes2`)가 아닌, 딥시크(DeepSeek) API 추론 설정이 활성화된 `~/.hermes` 공간의 `config.yaml`을 바라보고 구동되어야 정상 작동합니다.
    

### 2. 표준 복구 절차 (Standard Operating Procedure)

점유된 소켓 포트를 즉각 강제 해제하고, DeepSeek API 컨필레이션을 동기화하여 단일 백엔드 런타임을 안착시키는 순수 명령어 세트입니다.

#### [1단계] 8787 포트 점유 프로세스 및 잔해 완전 소멸

터미널에서 8787 포트를 쥐고 있는 좀비 소켓의 PID를 찾아 커널 레벨에서 강제 파괴(-9)하고 파이썬 실행 잔해를 청소합니다.

Bash

```
kill -9 $(lsof -t -i:8787) 2>/dev/null
pkill -9 -f "server.py"
pkill -9 -f "hermes-webui"
```

#### [2단계] 글로벌 모델 설정 동기화 (DeepSeek Chat 모드)

글로벌 모델 스위처를 가동하여 WebUI의 타깃 경로인 `~/.hermes/config.yaml` 장부를 DeepSeek 궤도로 일괄 전환합니다.

Bash

```
/Users/bluesea/Applications/venu/scripts/switch_model.sh deepseek
```

#### [3단계] 독립형 격리 환경 변수 주입 및 백엔드 포크

작업 디렉터리로 이동한 뒤, `HERMES_HOME`을 메인 경로(`~/.hermes`)로 명확히 바인딩하고 전용 가상환경 런타임으로 웹 서버를 클린 포크합니다.

Bash

```
cd /Users/bluesea/Applications/hermes-webui/
export HERMES_HOME="/Users/bluesea/.hermes"
nohup /Users/bluesea/Applications/venu/venv/bin/python /Users/bluesea/Applications/hermes-webui/server.py > webui_launchd.log 2>&1 &
```

### 3. 복구 상태 최종 검증 (Fact Check)

- **백엔드 리스닝 상태 확인**: `cat /Users/bluesea/Applications/hermes-webui/webui_launchd.log`
    
    Plaintext
    
    ```
    Hermes Web UI listening on http://127.0.0.1:8787  [ok]
    ```
    
- **단일 프로세스 상주 팩트 체크**: `ps aux | grep server.py | grep -v grep`
    
    - 최종 안착 완료된 단일 상주 프로세스: **`PID 89258`**
        

### 📅 장부 기록 및 폐쇄 완료 (헌법 §3.2 준수)

- **장부 현행화**: 헌법 수렴 정책에 따라 `01_hot.md` 및 `05_시스템 상태.md`에 **`Hermes WebUI = ✅ ACTIVE (PID: 89258 — DeepSeek 연동 완결)`** 상태 장부 기록을 최종 완료했습니다.
    
- **접속 재개**: 이제 크롬 브라우저를 통해 `http://127.0.0.1:8787`에 접속하시면 DeepSeek API 기반의 초고속 추론 인터페이스를 바로 이용하실 수 있습니다.