---
tags: [ingested, 10_AI_Automation, webui, network-refresh, automation, bash-script, session-management, process-kill, gateway-restart]
description: "주석을 배제하여 zsh 구문 오류를 원천 차단한 100% 실행 가능한 순수 명령어 세트를 제공한다. 터미널에 복사하여 붙여넣기만 하면 WebUI 세션과 네트워크 무결성을 리프레시할 수 있다. 해당 프로토콜은 포트 킬, 프로세스 종료, 게이트웨이 재시작, WebUI 서버 실행의 자동화된 워크플로우를 포함한다."
brief: "웹UI 세션 충돌과 네트워크 불안정을 해결하기 위해, 기존 프로세스를 강제 종료하고 락 파일을 삭제한 뒤 새로운 서버 인스턴스를 8787 포트에 재바인딩하는 명령어 세트다. 정상 작동 여부는 로그 파일의 마지막 15줄을 확인하여 검증할 수 있다."
---

## WebUI 세션 및 네트워크 무결성 리프레시 프로토콜

주석을 배제하여 zsh 구문 오류를 원천 차단한 100% 실행 가능한 순수 명령어 세트입니다. 아래 텍스트 박스 내용을 **전체 복사하여 터미널에 붙여넣고 엔터**를 쳐주십시오.

Bash

```
kill -9 $(lsof -t -i:8787) 2>/dev/null
pkill -9 -f "server.py"
pkill -9 -f "hermes-webui"
rm -f /Users/bluesea/.hermes/runtime/webui/*.lock 2>/dev/null
export HERMES_HOME="/Users/bluesea/.hermes"
/Users/bluesea/.hermes/hermes-agent/venv/bin/hermes gateway stop 2>/dev/null
HERMES_PLATFORMS="api_server" nohup /Users/bluesea/.hermes/hermes-agent/venv/bin/hermes gateway run --replace > ~/gateway_net.log 2>&1 &
sleep 1.5
cd /Users/bluesea/Applications/hermes-webui/
nohup /Users/bluesea/Applications/venu/venv/bin/python /Users/bluesea/Applications/hermes-webui/server.py > webui_launchd.log 2>&1 &
sleep 1.5
ps aux | grep server.py | grep -v grep
```

## 🔍 정상 가동 여부 실시간 팩트 체크

위 명령어를 가동하면 내부 락 파일들이 소멸되고 깨끗한 단일 `server.py` 인스턴스가 8787 포트를 다시 점유하게 됩니다. 정상 바인딩 상태를 보려면 아래 명령어를 실행하십시오.

Bash

```
cat /Users/bluesea/Applications/hermes-webui/webui_launchd.log | tail -n 15
```