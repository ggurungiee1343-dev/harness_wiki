---
tags: [ingested, 10_AI_Automation, hermes, environment-variable, config-path, webui, port-mapping, routing, launchd]
description: "두 개의 Hermes 인스턴스(Hermes 1 메인, Hermes 2 울산)가 존재하며 경로와 사용처가 완전히 다르므로 절대 혼용해서는 안 된다. Hermes WebUI는 반드시 ~/.hermes 환경을 바라봐야 하며 경로 혼용 시 모든 모델 라우팅이 실패한다. 8787 포트는 Hermes WebUI 프론트엔드 서비스가 담당하며 launchd plist로 관리된다."
brief: "brief"
---

### `HERMES_HOME`과 환경 변수의 진짜 물리적 지도 (Fact Check)

> 최초 작성: 2026-06-07 / 최종 업데이트: 2026-06-07 (WebUI 멀티모델 통합 세션 반영)

---

## 1. 두 Hermes 인스턴스 — 절대 혼용 금지

| 항목 | Hermes 1 (메인) | Hermes 2 (울산) |
|---|---|---|
| HOME 경로 | `~/.hermes` | `/Users/bluesea/Applications/venu/.hermes2` |
| config.yaml 경로 | `~/.hermes/config.yaml` | `venu/.hermes2/config.yaml` |
| 사용처 | 텔레그램 메인봇 + **WebUI 백엔드** + API Server | `@Ulsan_Antigravity_bot` 전용 |
| 라우팅 모델 | DeepSeek / GPT-OSS-120B / Qwen-14B (로컬) / Minimax | 독자 API (DeepSeek 미사용) |
| switch-model 대상 | ✅ 해당됨 | ❌ 별도 관리 |

**⚠️ 황금 규칙**: Hermes WebUI는 `venu/.hermes2`가 **아니라** `~/.hermes` 환경을 바라봐야 정상 동작함. 경로 혼용 시 모든 모델 라우팅 실패.

---

## 2. 포트 & 서비스 맵

| 포트 | 서비스 | launchd plist | 프로세스 |
|------|--------|---------------|----------|
| **8787** | Hermes WebUI (프론트엔드) | `com.bluesea.hermes-webui.plist` | Node.js (Next.js) |
| **8642** | Hermes Gateway (라우팅 엔진) | `ai.hermes.gateway.plist` | Python (venu venv) |
| **8000** | Hermes API Server | (Gateway 내부 설정) | Python (Gateway와 동일 프로세스) |
| **8080** | llama-server (로컬 LLM) | `com.bluesea.llama_server2.plist` | llama.cpp llama-server |

**WebUI 요청 흐름**:  
브라우저 → `localhost:8787` (WebUI) → `localhost:8642` (Gateway) → 외부 API 또는 `localhost:8080` (llama-server)

---

## 3. launchd plist 파일 목록 (실제 경로)

| plist 파일명 | 위치 | HERMES_HOME | 역할 |
|---|---|---|---|
| `ai.hermes.gateway.plist` | `~/Library/LaunchAgents/` | `~/.hermes` | Hermes Gateway (포트 8642) |
| `com.bluesea.hermes-webui.plist` | `~/Library/LaunchAgents/` | — | Hermes WebUI (포트 8787, Node.js) |
| `com.bluesea.llama_server2.plist` | `~/Library/LaunchAgents/` | — | llama-server (포트 8080, Qwen-14B 서빙) |
| `com.bluesea.hermes2.plist` | `~/Library/LaunchAgents/` | `venu/.hermes2` | Hermes 2 텔레그램봇 (울산) |
| `com.bluesea.fswatch-indexer.plist` | `~/Library/LaunchAgents/` | — | fswatch 인덱서 |

**⚠️ PID 안정성**: macOS launchd는 재시작 시마다 PID를 새로 부여함. 스크립트에서 PID를 하드코딩하면 안 됨.  
현재 PID 확인: `launchctl list | grep <서비스명>`  
정확한 PID: `launchctl print gui/501/<label> | grep pid`

---

## 4. API 키 환경 변수 — 실제 이름과 위치

| 환경변수명 | 서비스 | 설정 위치 |
|---|---|---|
| `DEEPSEEK_API_KEY` | DeepSeek Chat API | `ai.hermes.gateway.plist` EnvironmentVariables |
| `NVIDIA_GPT_API_KEY` | NVIDIA API (GPT OSS 120B) | `ai.hermes.gateway.plist` EnvironmentVariables |
| `NVIDIA_MINIMAX_API_KEY` | NVIDIA API (Minimax M2.7) | `ai.hermes.gateway.plist` EnvironmentVariables |
| `TELEGRAM_BOT_TOKEN` | 텔레그램 메인봇 | `ai.hermes.gateway.plist` EnvironmentVariables |

> 🔑 plist 파일을 직접 열지 말고: `launchctl print gui/501/ai.hermes.gateway | grep -A2 "environment"`

---

## 5. `~/.hermes/config.yaml` — custom_providers 구조 (실제 상태)

```yaml
custom_providers:
  # [DISABLED 2026-06-07] Gemma4 26B — 메모리 부족으로 비활성화
  # - api_mode: chat_completions
  #   base_url: http://127.0.0.1:8080/v1
  #   model: gemma-4-26B-A4B-it-UD-Q4_K_S.gguf
  #   name: Gemma4

  # [ACTIVE 2026-06-07] Qwen2.5 14B — 로컬 llama-server
  - api_mode: chat_completions
    base_url: http://127.0.0.1:8080/v1
    api_key: local
    model: Qwen2.5-14B-Instruct-Q4_K_M.gguf
    context_length: 65536        # llama-server는 -c 65536로 기동하지만 실제 서빙은 32768
    discover_models: false       # 라이브 /v1/models 프로브 스킵 (로컬 모델 등록용)
    models:
      Qwen2.5-14B-Instruct-Q4_K_M.gguf:
        context_length: 65536
    name: Qwen-14B

  # NVIDIA GPT OSS 120B
  - api_mode: chat_completions
    base_url: https://integrate.api.nvidia.com/v1
    api_key_env: NVIDIA_GPT_API_KEY
    model: openai/gpt-oss-120b
    context_length: 131072
    name: GPT OSS 120B (NVIDIA)

  # Minimax M2.7
  - api_mode: chat_completions
    base_url: https://integrate.api.nvidia.com/v1
    api_key_env: NVIDIA_MINIMAX_API_KEY
    model: minimaxai/minimax-m2.7
    context_length: 65536
    name: Minimax M2.7
```

---

## 6. Hermes WebUI 아키텍처 (2026-06-07 확인)

### 설치 경로
- **WebUI 소스**: `/Users/bluesea/Applications/hermes-webui/`
- **핵심 설정 파일**: `/Users/bluesea/Applications/hermes-webui/api/config.py`
- **디스크 캐시**: `~/.hermes/webui/models_cache.json` ← 문제 원인이었음

### 모델 ID 포맷
WebUI는 custom_providers 모델을 다음 형식으로 인코딩함:
```
@custom:<slug>:<model-name>
예: @custom:qwen-14b:Qwen2.5-14B-Instruct-Q4_K_M.gguf
    @custom:gpt-oss-120b-nvidia:openai/gpt-oss-120b
    @custom:minimax-m2.7:minimaxai/minimax-m2.7
```

Gateway는 이 `@custom:` 접두사를 이해하지 못함. 따라서 `api_server.py`에서 접두사를 스트립한 뒤 라우팅해야 함 (2026-06-07 수정 완료).

### 하드코딩된 화이트리스트 (발견 및 수정)
`api/config.py` 안에 드롭다운에 표시할 모델을 필터링하는 키워드 목록이 있음:
```python
_whitelist_keywords = ["gemma-4-26b", "deepseek-v4-flash", "gpt-oss-120b", "minimax-m2.7", "qwen"]
```
이 목록에 없는 모델은 드롭다운에 표시되지 않음. Qwen이 안 보였던 진짜 이유.

### 캐시 무효화 방법
```bash
rm ~/.hermes/webui/models_cache.json
# 이후 WebUI 재시작 또는 브라우저 새로고침
```

---

## 7. Hermes Gateway 패키지 경로

Gateway는 venv에 설치된 패키지로 동작함 (소스 코드가 아님):
```
/Users/bluesea/Applications/venu/venv/lib/python3.11/site-packages/gateway/
  ├── run.py              ← custom_provider 라우팅 해석 (_resolve_custom_provider_by_model)
  ├── platforms/
  │   └── api_server.py   ← @custom: 접두사 스트립 로직 (2026-06-07 수정)
  └── ...
```

**⚠️ 주의**: `pip install` 또는 `pip upgrade`로 패키지를 업데이트하면 위 수정 사항이 **덮어써짐**. 버전 업그레이드 전 반드시 패치 내용 백업/재확인 필요.

---

## 8. Qwen-14B GGUF n_ctx 주의사항

- llama-server 기동 시 `-c 65536` 옵션을 줘도 GGUF 메타데이터의 `n_ctx`는 `32768`을 리포트함
- Hermes Gateway는 `GET /v1/models`로 이 값을 읽고 "컨텍스트 부족" 오류 발생 가능
- 해결: `discover_models: false` + `context_length: 65536` 명시적 설정
- **실제 서빙 컨텍스트**: Mac Studio 36GB에서 Qwen2.5-14B + context 32768이 안전. 65536은 OOM 가능.

---

## 9. Hermes 시스템 프롬프트 (~10,000 토큰)

Hermes Agent가 요청마다 전송하는 시스템 프롬프트는 약 10,000 토큰 이상:
- **Tool definitions**: 20개 이상의 도구 스키마 (각 100~300토큰)
- **Memory context**: 사용자 기억, 페르소나, 프로젝트 상태
- **Soul/Persona**: Hermes 행동 지침
- **Skills**: 로드된 스킬 목록

이 프롬프트를 로컬 14B 모델로 처리할 경우:
- 첫 요청: 약 91 tokens/sec → 10,000 토큰 처리 = **약 110초 (2분)**
- 이후 요청: KV 캐시 히트로 빠름
- 결론: 로컬 소형 모델에 Hermes Agent를 붙이는 것은 속도 면에서 비효율적

---

## 10. 분산된 설정 파일 전체 목록

| 파일 | 경로 | 용도 |
|---|---|---|
| `config.yaml` (Hermes 1) | `~/.hermes/config.yaml` | Hermes 메인 설정 (모델, custom_providers, agent 설정 등) |
| `config.yaml` (Hermes 2) | `venu/.hermes2/config.yaml` | 울산봇 전용 설정 |
| `api/config.py` | `/Users/bluesea/Applications/hermes-webui/api/config.py` | WebUI 모델 필터링 로직 (whitelist 포함) |
| `models_cache.json` | `~/.hermes/webui/models_cache.json` | WebUI 모델 목록 디스크 캐시 (TTL 있음, 수동 삭제 가능) |
| `ai.hermes.gateway.plist` | `~/Library/LaunchAgents/` | Gateway API 키 환경변수, HERMES_HOME 설정 |
| `com.bluesea.llama_server2.plist` | `~/Library/LaunchAgents/` | llama-server 기동 옵션 (-c, 모델 경로 등) |
| `harness_config.py` | `/Users/bluesea/Applications/Mjauto/Scripts/` | 하네스 에이전트 설정 |

> **`.env` 파일**: 현재 Hermes1/2 시스템에서는 별도 `.env` 파일을 사용하지 않음. 환경변수는 모두 plist의 `EnvironmentVariables` 섹션에서 주입됨.

---

*이 문서는 2026-06-07 WebUI 멀티모델 통합 작업 세션 중 실제 코드/설정 탐색을 통해 확인된 정보만 포함함.*
