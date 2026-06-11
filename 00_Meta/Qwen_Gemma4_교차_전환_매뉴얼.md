# Qwen ↔ Gemma4 교차 전환 매뉴얼

> **Version**: 1.2 (2026-06-07 15:57)
> **적용 대상**: Hermes1 텔레그램 봇 (@MJ_CAPT_BOT) + Hermes WebUI — 로컬 LLM 엔진 교체

---

## 변경해야 할 파일 (4개)

| # | 파일 | 역할 |
|---|------|------|
| ① | **`harness_agent.py`** | Hermes1 봇 LLM 호출 엔진 — `[Qwen ALT]` 8곳 swap |
| ② | **`~/.hermes/config.yaml`** | Hermes1 로컬 설정 custom_providers 정의 |
| ③ | **`~/.hermes2/config.yaml`** | Hermes WebUI/Gateway custom_providers 정의 (**WebUI 하단 버튼에 표시되는 모델 목록**) |
| ④ | **`com.bluesea.llama_server2.plist`** | llama-server 데몬이 로딩하는 GGUF 모델 파일 경로 |

---

## 파일 경로

| 파일 | 절대 경로 |
|------|----------|
| `harness_agent.py` | `/Users/bluesea/Applications/Mjauto/Scripts/harness_agent.py` |
| `config.yaml` | `/Users/bluesea/.hermes/config.yaml` |
| `com.bluesea.llama_server2.plist` | `/Users/bluesea/Library/LaunchAgents/com.bluesea.llama_server2.plist` |

---

## 모델 파일 경로

| 모델 | GGUF 파일 경로 |
|------|---------------|
| **Gemma4 26B** | `/Users/bluesea/Applications/Mjauto/unsloth/gemma-4-26B-A4B-it-GGUF/gemma-4-26B-A4B-it-UD-Q4_K_S.gguf` |
| **Qwen2.5-14B-Instruct** | `/Users/bluesea/Applications/Mjauto/unsloth/Qwen2.5-14B-Instruct/Qwen2.5-14B-Instruct-Q4_K_M.gguf` |

---

## 현재 상태 (2026-06-07 15:57 기준)

| 항목 | 값 |
|------|-----|
| 활성 로컬 모델 | **Qwen2.5-14B-Instruct** ✅ |
| harness_agent.py | `MODE_QWEN14B = "Qwen-14B"` (활성) / Gemma4 관련 코드 주석 보존 |
| ~/.hermes/config.yaml | Qwen-14B 블록 `[ACTIVE]`, Gemma4 블록 `# [DISABLED]` |
| ~/.hermes2/config.yaml | Qwen-14B custom_providers 추가됨 (WebUI 하단 버튼용) |
| llama-server | Qwen2.5-14B-Instruct-Q4_K_M.gguf, `-c 32768`, 8080 포트 |
| llm_mode.txt | `Qwen-14B` |

---

## ⏩ Gemma4 → Qwen2.5 14B 전환 (Qwen을 다시 쓸 때)

### Step 1 — `harness_agent.py` `[Qwen ALT]` 8곳 swap

파일 내 `[Qwen ALT]` 태그 **8개**를 검색해서, 각 위치에서:

1. **Gemma4 활성 라인** → 주석 처리 (`#` 추가)
2. 바로 아래의 **`# [Qwen ALT]` 주석 라인** → 주석 해제 (`# ` 제거)

#### 8곳 상세

| # | 위치 (근사 행) | Gemma4 라인 (→ 주석) | Qwen ALT 라인 (→ 활성) |
|---|-------------|-------------------|---------------------|
| 1 | ~187행 | `MODE_GEMMA4 = "Gemma4"` | `MODE_GEMMA4 = "Qwen2.5 14B"` |
| 2 | ~202행 | `MODE_GEMMA4: "🟢 Gemma4 (로컬)"` | `MODE_GEMMA4: "🟢 Qwen2.5 14B (로컬)"` |
| 3 | ~270행 | `"""Gemma4 (llama-server) completions API — 수동 포맷..."` | `"""Qwen2.5 14B (llama-server) completions API — 수동 포맷..."` |
| 4 | ~288행 | `💻 [Engine] Gemma4 (로컬) 호출 중...` | `💻 [Engine] Qwen2.5 14B (로컬) 호출 중...` |
| 5 | ~298행 | `return text, "Gemma4 (로컬)"` | `return text, "Qwen2.5 14B (로컬)"` |
| 6 | ~314행 | `_ENGINE_MAP: MODE_GEMMA4: ("Gemma4 (로컬)", _call_local)` | `_ENGINE_MAP: MODE_GEMMA4: ("Qwen2.5 14B (로컬)", _call_local)` |
| 7 | ~320행 | `_FALLBACK_ORDER: ("Gemma4", _call_local)` | `_FALLBACK_ORDER: ("Qwen2.5 14B", _call_local)` |
| 8 | ~381행 | `"모든 엔진(Gemma4, DeepSeek, NVIDIA 70B)이 응답하지 않습니다..."` | `"모든 엔진(Qwen2.5 14B, DeepSeek, NVIDIA 70B)이 응답하지 않습니다..."` |

### Step 2 — `~/.hermes/config.yaml` Qwen custom_providers 활성화

```yaml
# 변경 전 (Gemma4 — 주석 처리)
custom_providers:
# [DISABLED 2026-06-07] Qwen2.5-14B-Instruct → Gemma4 26B로 복귀
# - api_mode: chat_completions
#   base_url: http://localhost:8080/v1
#   model: qwen2.5-14b-instruct-q4_k_m.gguf
#   models:
#     qwen2.5-14b-instruct-q4_k_m.gguf:
#       context_length: 32768
#   name: Qwen-14B

# 변경 후 (Qwen 활성 — 주석 해제)
custom_providers:
- api_mode: chat_completions
  base_url: http://localhost:8080/v1
  model: qwen2.5-14b-instruct-q4_k_m.gguf
  models:
    qwen2.5-14b-instruct-q4_k_m.gguf:
      context_length: 32768
  name: Qwen-14B
```

### Step 3 — `~/.hermes2/config.yaml` Qwen custom_providers 추가 (WebUI 하단 버튼)

> [!IMPORTANT]
> WebUI 하단 모델 선택 버튼은 **Gateway가 읽는 `.hermes2/config.yaml`** 기준으로 표시됨.
> `.hermes/config.yaml`과 별개이므로 반드시 양쪽 모두 수정해야 한다.

`.hermes2/config.yaml`의 `custom_providers` 섹션에 추가:
```yaml
custom_providers:
- api_mode: chat_completions
  base_url: http://localhost:8080/v1
  model: qwen2.5-14b-instruct-q4_k_m.gguf
  models:
    qwen2.5-14b-instruct-q4_k_m.gguf:
      context_length: 32768
  name: Qwen-14B
```

### Step 4 — llama-server plist GGUF 경로 교체

`~/Library/LaunchAgents/com.bluesea.llama_server2.plist` 의 `-m` 경로와 `-c` 값을 변경:

```diff
- /Users/bluesea/Applications/Mjauto/unsloth/gemma-4-26B-A4B-it-GGUF/gemma-4-26B-A4B-it-UD-Q4_K_S.gguf
+ /Users/bluesea/Applications/Mjauto/unsloth/Qwen2.5-14B-Instruct/Qwen2.5-14B-Instruct-Q4_K_M.gguf
```
컨텍스트: `-c 65536` → `-c 32768` (14B 모델에 65536은 메모리 부족 OOM 유발)

### Step 5 — 재시작

```bash
# llama-server 강제 재시작 (-k 필수! 없으면 기존 프로세스 유지됨)
launchctl kickstart -k gui/501/com.bluesea.llama_server2

# 모델 확인 (로딩 완료까지 30초~1분 소요)
curl http://127.0.0.1:8080/v1/models | python3 -c "import sys,json;print(json.load(sys.stdin)['data'][0]['id'])"

# Hermes1 봇 재시작
launchctl kickstart -k gui/501/com.hermes.bot
```

> [!WARNING]
> `launchctl kickstart`에 **`-k` 옵션 필수**. 없으면 기존 프로세스가 RAM에 계속 살아있어 기억 파일 재오염 등 부작용 발생 (#022 참조)

---

## ⏪ Qwen2.5 14B → Gemma4 전환 (Qwen에서 Gemma4로 복귀)

위 Gemma4→Qwen 순서의 **정확히 역방향**입니다.

### Step 1 — `harness_agent.py` `[Qwen ALT]` 8곳을 주석 처리 + Gemma4 라인 활성화

`[Qwen ALT]` 8곳 검색 → 각 위치에서:

1. **`# [Qwen ALT]` 라인** → 주석 처리 (`# ` 추가)
2. 바로 위의 **Gemma4 활성 라인** → 주석 해제 (`#` 제거)

### Step 2 — `~/.hermes/config.yaml` Qwen 블록 주석 처리

위 Step 2의 역방향 — Qwen custom_providers 블록을 `#` 주석 처리하고 `# [DISABLED ...]` 메모 추가.

### Step 3 — plist GGUF 경로 gemma-4-26B로 변경

위 Step 3의 역방향.

### Step 4 — 재시작 (동일)

---

## ⚡ 퀵 레퍼런스

| 전환 방향 | harness_agent.py | config.yaml | plist |
|-----------|-----------------|-------------|-------|
| **Gemma4 → Qwen** | `[Qwen ALT]` 8곳 활성화 + Gemma4 라인 8곳 주석 | Qwen 주석 해제 | GGUF → Qwen 경로 |
| **Qwen → Gemma4** | `[Qwen ALT]` 8곳 주석 + Gemma4 라인 8곳 활성화 | Qwen 주석 처리 | GGUF → Gemma4 경로 |

> 전환 소요 시간: 약 **2~3분** (파일 3개 편집 + 재시작 2회)
> `switch-model` 스크립트는 DeepSeek↔NVIDIA 전환 전용이므로, Qwen/Gemma4 교체는 본 매뉴얼에 따라 수동으로 진행.

---

## 참고 — 전환 시 주의사항

- **llama-server context_length**: Qwen2.5-14B는 `-c 32768`로 실행. `-c 65536`은 Mac Studio 36GB에서 OOM 발생 확인 (#023). config.yaml의 `context_length`도 32768로 맞춰야 함.
- **Qwen2.5-14B GGUF 실제 max context**: 131,072 — 32768로도 일반 업무 충분.
- **Gemma4 GGUF chat template 버그**: `chat.completions.create()`가 빈 문자열 반환 → `completions.create()` + 수동 `<start_of_turn>user/model<end_of_turn>` 포맷으로 우회. Qwen도 동일한 수동 포맷 사용 가능.
- **`_call_local()` timeout**: 현재 120초. Qwen2.5-14B 일반 질문은 10~30초, 긴 문서 작업은 60초 내외.
- **복수 AI 동시 작업 주의**: 두 AI가 동시에 llama-server를 재시작하면 이전 모델 프로세스가 좀비로 남을 수 있음. 전환 후 `ps aux | grep llama-server`로 중복 프로세스 없는지 반드시 확인.
- **Gateway config 분리**: WebUI 하단 버튼은 `.hermes2/config.yaml`(HERMES_HOME=`~/Applications/venu/.hermes2`)을 기준으로 표시됨. `.hermes/config.yaml`만 수정하면 WebUI에 반영 안 됨.

---

## 🔧 Hermes Agent 스킬 연동

이 매뉴얼을 기반으로 `qwen-gemma4-switch` 스킬이 등록되어 있습니다. 스킬을 통해 AI 에이전트가 직접 전환 절차를 수행할 수 있습니다.

| 항목 | 내용 |
|------|------|
| **스킬명** | `qwen-gemma4-switch` |
| **카테고리** | `devops/` |
| **파일 위치** | `~/.hermes/skills/devops/qwen-gemma4-switch/SKILL.md` |
| **호출 방법** | `skill_view(name='qwen-gemma4-switch')` |

### 스킬 활용

MJ님께서 **"Qwen으로 바꿔줘"** 또는 **"Gemma4로 복귀"** 라고 말씀하시면, AI 에이전트가 이 스킬을 로드하여 3개 파일 변경 + 서비스 재시작까지 자동으로 수행합니다.

### 스킬 생성 경위

1. MJ님이 기존 Qwen—Gemma4 교차 전환 매뉴얼(`Qwen_Gemma4_교차_전환_매뉴얼.md`)을 스킬화 요청
2. 매뉴얼 내용을 YAML frontmatter + 마크다운 본문 형식의 SKILL.md로 변환
3. `skill_manage(action='create')`로 `devops/qwen-gemma4-switch` 스킬 등록
4. 향후 `skill_view()`로 불러와서 즉시 전환 실행 가능

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-06-07 11:00 | 1.0 | 최초 작성 — Qwen3.6-35B ↔ Gemma4 `[Qwen ALT]` 주석 방식 매뉴얼 |
| 2026-06-07 | 1.1 | Hermes Agent 스킬(`qwen-gemma4-switch`) 연동 정보 추가 |
| 2026-06-07 | 1.2 | **Qwen2.5-14B-Instruct로 완전 전환** — 모델 경로/context 수정, `.hermes2/config.yaml` Step 추가, 좀비 프로세스 주의사항 추가, `-k` 옵션 경고 추가 |

---

*최종 업데이트: 2026-06-07 15:57 — Qwen2.5-14B-Instruct 전환 완료 기준으로 전면 개정*
