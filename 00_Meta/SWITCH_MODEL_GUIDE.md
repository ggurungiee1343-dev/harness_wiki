# 🔄 switch-model — 모델 전환 도구 사용 가이드

> **목적**: Hermes 시스템의 메인 모델을 GPT-OSS-120B(NVIDIA)와 DeepSeek Chat 사이에서 전환
> **최초 작성**: 2026-06-06
> **버전**: 1.0

---

## 개요

WebUI 하단의 모델 선택 드롭다운에서 수동으로 전환하는 대신, CLI 명령어 한 줄로 **두 Hermes Home**을 동시에 전환할 수 있습니다.

- Gateway/WebUI (`~/.hermes/config.yaml`)
- Telegram Bot (`venu/.hermes2/config.yaml`)

---

## 설치 (1회)

심링크 생성 (sudo 필요):

```bash
sudo ln -s ~/Applications/venu/scripts/switch_model.sh /usr/local/bin/switch-model
```

이제 어디서든 `switch-model` 명령어를 사용할 수 있습니다.

---

## 사용법

### GPT-OSS-120B(NVIDIA)로 전환

```bash
switch-model got
```

출력 예시:
```
>>> Switching to: GPT-OSS-120B (NVIDIA)
  [OK] /Users/bluesea/.hermes/config.yaml updated
  [OK] /Users/bluesea/Applications/venu/.hermes2/config.yaml updated
Done! Restart the gateway for changes to take effect:
  hermes gateway restart
```

### DeepSeek Chat으로 전환

```bash
switch-model deepseek
```

출력 예시:
```
>>> Switching to: DeepSeek Chat
  [OK] /Users/bluesea/.hermes/config.yaml updated
  [OK] /Users/bluesea/Applications/venu/.hermes2/config.yaml updated
Done! Restart the gateway for changes to take effect:
  hermes gateway restart
```

### 단축 인자

| 인자 | 대상 모델 | 설명 |
|------|-----------|------|
| `got`, `gpt-oss`, `oss`, `gpt` | GPT-OSS-120B (NVIDIA) | 무료 모델 전환 |
| `deepseek`, `ds` | DeepSeek Chat | 유료 모델 전환 |

---

## 전환 후 필수 작업

Gateway를 재시작해야 변경사항이 적용됩니다:

```bash
hermes gateway restart
```

---

## 동작 원리

### 파일 삭제 금지 원칙

이 스크립트는 **파일을 절대 삭제하지 않습니다**. 전환되는 쪽 설정은 `# [SWITCHED to ...]` 주석으로 처리되어 원본이 그대로 보존됩니다.

예시 (config.yaml 내부):
```yaml
# active model section
  default: openai/gpt-oss-120b           # ← 활성 상태
  # [SWITCHED to GPT-OSS] default: deepseek-chat  # ← 비활성 (보존)
```

DeepSeek으로 전환하면 반대로 GPT-OSS 설정이 주석 처리되고 DeepSeek 설정이 복원됩니다.

### 적용 대상

| Hermes Home | config.yaml 경로 | 용도 |
|-------------|-----------------|------|
| Home 1 (Gateway/WebUI) | `~/.hermes/config.yaml` | WebUI 브라우저 접속, Hermes Gateway |
| Home 2 (Telegram Bot) | `venu/.hermes2/config.yaml` | 텔레그램 봇 (harness_agent.py) |

### Gemma4 26B는 영향 없음

Gemma4 26B는 **별도의 API 키**와 별도 provider 설정을 사용하므로, 이 스크립트의 전환 작업에 전혀 영향을 받지 않습니다.

---

## 문제 해결

### "command not found: switch-model"

심링크가 생성되지 않은 경우:
```bash
# 직접 스크립트 실행
~/Applications/venu/scripts/switch_model.sh got
```

또는 심링크 생성:
```bash
sudo ln -s ~/Applications/venu/scripts/switch_model.sh /usr/local/bin/switch-model
```

### 전환 후에도 예전 모델이 보임

Gateway 재시작을 잊은 경우:
```bash
hermes gateway restart
```

### config 파일이 꼬인 경우

직접 config.yaml을 열어서 `# [SWITCHED to ...]` 주석을 제거하고 원하는 설정을 활성화하세요.
어떤 설정이 주석 처리되어도 원본 데이터는 모두 보존됩니다.

---

## 스크립트 위치

- **스크립트**: `~/Applications/venu/scripts/switch_model.sh`
- **심링크**: `/usr/local/bin/switch-model`

---

## 관련 문서

- [02_스크립트 정보.md](02_스크립트%20정보.md) — switch_model.sh 항목
- [03_시스템 인벤토리.md](03_시스템%20인벤토리.md) — 모델 전환 도구 항목
- [04_주요 시스템 가이드 및 FAQ.md](04_주요%20시스템%20가이드%20및%20FAQ.md) — FAQ
- [HERMES3_MASTER_DEVELOPMENT_GUIDE.md](HERMES3_MASTER_DEVELOPMENT_GUIDE.md) — 업데이트 이력
- [HERMES3_ENCYCLOPEDIA.md](HERMES3_ENCYCLOPEDIA.md) — switch-model 백과사전 항목

---

*최종 업데이트: 2026-06-06*
