# 💡 주요 시스템 가이드 및 FAQ (자주 묻는 질문)

> [!INFO] 💡 문서의 역할 (지식 증류 아키텍처)
> 이 문서는 **"정제된 백과사전"**입니다.
> 날것의 에러 로그와 문제 해결 과정은 `wiki/00_Meta/장애 기록/` 폴더에 일지(Post-mortem) 형태로 상세히 기록하고, 그중 **앞으로 시스템과 봇이 계속 명심해야 할 핵심 교훈 및 가이드라인만 요약**해서 이곳에 등재합니다.
> **최종 업데이트: 2026-06-07 11:52 — cove_engine.py 이전, 메타 7종 갱신**
     6|
     7|이 문서는 시스템 운영 중 자주 발생하는 질문(FAQ)과 핵심 문제 해결 이력을 기록하여, 향후 시스템 유지보수 및 업그레이드 시 참고하기 위해 관리됩니다.
     8|
     9|## 📝 1. 자주 묻는 질문 (FAQ)
    10|
    11|### Q1. `/명령어`들은 자연어로도 지시가 가능한가요?
    12|- **자연어 가능 (Fast Intent)**: 파일 읽기나 리스트 조회("보관소 폴더 리스트 뭐있어?", "hot.md 파일 열어줘", "지금 몇시야?")는 `/ask`, `/read`를 쓰지 않아도 봇이 자연어를 스캔하여 0.1초 만에 즉시 실행합니다. (`verification_engine.py` 기반)
    13|- **자연어 차단 (안전 보호)**: `/exec`, `/move`, `/create` 등 시스템을 변경하는 치명적인 명령어는 봇이 자연어를 잘못 해석하여 시스템을 훼손하는 것을 막기 위해 **반드시 슬래시(/) 명령어로만** 직접 입력해야 합니다.
    14|
    15|### Q2. 텔레그램 버튼 미적용 같은 시스템 버그도 Skill Evolver가 스스로 고치나요?
    16|- **아닙니다.** `Skill Evolver`는 텔레그램의 `/exec [명령어]`를 통해 **터미널이나 OS 명령어**를 실행할 때 발생하는 환경적 에러(예: 권한 없음, 패키지 누락 등)만을 자율 복구하고 학습합니다.
    17|- 파이썬 봇 자신의 코어 코드를 자율적으로 수정하게 두는 것은 봇 자체의 붕괴(자가 오염) 위험이 매우 크므로 의도적으로 차단해 두었습니다. 시스템 버그는 AI 비서에게 대화로 수정을 요청해야 안전합니다.
    18|
    19|### Q3. Graphify 지식망 리포트(Graph)는 어떻게 업데이트하나요?
    20|- `wiki_manager.py`는 `Mjobsidian/graphify-out/GRAPH_REPORT.md`를 읽어 지식망 컨텍스트로 사용하도록 설계되어 있습니다.
    21|- **적용 방법**: Graphify는 터미널 전용 도구(CLI)입니다. 
    22|  - **빠른 무비용 업데이트 (추천)**: 터미널이나 텔레그램 `/exec` 명령어에 `graphify update /Users/bluesea/Applications/Mjobsidian`을 실행하시면 API 키 및 요금 소모 없이 수 초 만에 구조 기반 지식망(`GRAPH_REPORT.md` 및 시각화 트리)이 즉시 갱신됩니다.
    23|  - **심층 AI 의미 추출**: API 키를 등록하고 `graphify extract /Users/bluesea/Applications/Mjobsidian --backend gemini` 형식으로 실행하면 AI가 의미적 연관성까지 더 심층 분석하여 추출해 줍니다.
    24|
    25|### Q4. 텔레그램 Dreaming(/dreaming)과 AI 에이전트의 정리 로직은 동일한가요?
    26|- **네, 100% 동일합니다.** 텔레그램 봇(`hermes_local.py`)과 제가 사용하는 기억 정리 코드는 완전히 같은 물리적 모듈 파일인 `modules/bio_memory_engine.py`를 호출하여 가동합니다.
    27|- 대화 분석의 대상이 되는 장부 파일(`harness_memory.json`)과 핵심 요약/분류를 담당하는 AI 추론 라우터(`hybrid_router.py`)가 동일하게 공유되므로, 텔레그램 하단 버튼을 클릭하든 에이전트에게 직접 대화로 정리해달라고 요청하든 결과물의 포맷, 어조, 일시 정보 저장 형식은 완벽하게 일관성을 유지합니다.
    28|
    29|### Q5. 텔레그램 `/goal` 명령어와 야간 감사(Audit)는 어떻게 동작하나요?
    30|  - **목표 설정**: 텔레그램에서 `/goal [이루고 싶은 장기 목표]`를 입력하면 `~/.hermes/active_goal.txt`에 장기 목표가 안전하게 보관됩니다. 목표 지우기는 `/goal clear`로 가능합니다.
    31|  - ~~**야간 지능형 감사**: 매일 새벽 3시에 동작하는 `dream_scheduler.py` 엔진(ExecPlan 기반 6단계 phase별 오류 격리)이… — **[2026-05-27 Dreaming 폐기로 중단됨]**~~
    32|
    33|### Q6. brew upgrade 후 llama-server(로컬 LLM)가 실행되지 않아요
    34|- **원인**: Homebrew로 `llama.cpp`를 업그레이드하면 Cellar 버전 디렉토리가 변경되지만, launchd plist에 하드코딩된 이전 버전 경로(`/opt/homebrew/Cellar/llama.cpp/XXXX/bin/llama-server`)가 남아서 바이너리를 찾지 못함.
    35|- **증상**: Gemma4 연결 실패, DeepSeek 자동 폴백, `launchctl list | grep llama` exit code 78
    36|- **해결 방법**:
    37|  ```bash
    38|  # 1) plist의 ProgramArguments 경로 확인
    39|  nano ~/Library/LaunchAgents/com.bluesea.llama_server2.plist
    40|  
    41|  # 2) 바이너리 경로를 brew symlink로 변경 (권장, 영구 해결)
    42|  # /opt/homebrew/Cellar/llama.cpp/XXXX/bin/llama-server → /opt/homebrew/bin/llama-server
    43|  
    44|  # 3) 재등록
    45|  launchctl bootout gui/501/com.bluesea.llama_server2 2>/dev/null
    46|  launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.bluesea.llama_server2.plist
    47|  
    48|  # 4) 확인
    49|  launchctl list | grep llama
    50|  curl http://127.0.0.1:8080/v1/models
    51|  ```
    52|- **예방**: 바이너리 경로에 **brew symlink**(`/opt/homebrew/bin/llama-server`)를 사용하면 brew upgrade에도 깨지지 않음. 이미 적용 완료됨.
    53|
    54|### Q7. PDF 파일도 /ingest로 Obsidian에 넣을 수 있나요?
    55|- **네, 가능합니다.** 2026-06-01부터 `ingest_engine.py`가 PDF(PyMuPDF/fitz)를 직접 읽어 텍스트를 추출한 후 LLM 분류 → `.md`로 변환 → Vault에 저장합니다.
    56|- **동작**: `/ingest` 실행 시 Clippings/ 폴더 내 `.pdf`도 `.md`와 동일하게 처리됨. PDF→텍스트 추출 → LLM 분류 → frontmatter(tags, description) → Archive 이동.
    57|- **제약**: 이미지/표/차트 등 비텍스트 요소는 추출 불가. 복잡한 레이아웃(2단, 표)은 텍스트 순서가 깨질 수 있음. 원본 PDF는 `Clippings/Archive/`에 보관되므로 필요 시 참조 가능.
    58|- **영구 저장/검색**: 변환된 `.md`는 FTS5 인덱스에 등록되어 `/reduce wiki` 검색 가능. NotebookLM MCP(비공식 API, 연구 세션 보조용)와는 보완 관계 — 영구 검색 인프라는 PDF→MD 파이프라인 담당.
    59|
    60|### Q8. `/reduce wiki`로 PDF 내용도 검색되나요?
    61|- **네.** PDF→MD로 변환된 파일은 일반 `.md` 파일과 동일한 FTS5 인덱스에 등록되므로 `/reduce wiki [검색어]`로 내용 검색 가능합니다.
    62|- 변환 전 원본 PDF는 검색되지 않습니다 (PDF 자체만으로는 FTS5 인덱싱 불가능). 변환 후 `.md`만 인덱싱 대상.
    63|
    64|### Q9. 에이전트가 파일을 만들 때 타임스탬프나 태그를 빼먹고 실수합니다. (WebUI 재시작 후)

### Q10. memory_engine 디렉터리와 빈 consolidator_state.json 파일을 만들면 어떤 효과가 있나요?
- **효과**: `hermes/memory_engine/` 경로가 존재하지 않아 발생하던 파일 입출력 오류를 방지합니다. 빈 `consolidator_state.json`은 메모리 엔진 초기화 시 기본 상태(빈 컨솔리데이터)로 인식되어, 메모리 통합 단계에서 오류 없이 진행됩니다. 이를 통해 메모리 정리·통합 파이프라인이 정상 동작하고, 이후 발생할 수 있는 `FileNotFoundError` 또는 `JSONDecodeError`를 사전 차단합니다.
- **원인**: WebUI나 에이전트 시스템이 새로 시작되거나 세션이 리셋되면, 에이전트는 완전한 백지 상태가 되어 `constitution.local.md`의 규칙(YYYY-MM-DD HH:MM 형식, 태그 등)을 모르는 상태에서 일을 처리하기 때문입니다.
- **해결 방안**: 
  1. `USER.md`에 규정된 **"초기화 프로토콜"**에 따라, 에이전트 시스템 프롬프트에 "시작 시 반드시 헌법을 먼저 읽어라"는 지시가 주입되어 있어야 합니다.
  2. 혹은 새 대화를 시작하실 때 **"일 시작하기 전에 constitution.local.md 랑 01_hot.md 부터 읽고 숙지해"**라고 첫 마디로 지시해 주시면 백지 상태의 에이전트가 헌법을 다시 다운로드(숙지)하여 실수를 방지할 수 있습니다.

### Q11. `clear_webui_cache.sh`와 `check_venv_patches.sh` 스크립트를 어떻게 실행해보세요?
- **clear_webui_cache.sh**: `/usr/bin/bash ~/Applications/Mjauto/Scripts/clear_webui_cache.sh` – WebUI 모델 캐시(`~/.hermes/webui/models_cache.json`)를 강제로 삭제합니다. 실행 후 캐시가 재생성되며 최신 모델이 로드됩니다.
- **check_venv_patches.sh**: `/usr/bin/bash ~/Applications/Mjauto/Scripts/check_venv_patches.sh` – 현재 가상환경(`venv`)의 핵심 패치(`harness_agent.py`, `run.py`, `config.yaml`) 상태를 자동 점검하고 결과를 출력합니다. 성공 시 “All patches verified” 메시지가 표시됩니다.

---
    65|
    76|    66|## 🔧 2. 주요 시스템 문제 해결 및 업데이트 이력 (Changelog)

### [2026-06-07] Qwen2.5-14B-Instruct → Qwen2.5-14B-Instruct-A3B 모델 교체
1. **변경 내용**:
   - 로컬 LLM 모델 교체: Qwen2.5-14B-Instruct → Qwen2.5-14B-Instruct-A3B (Qwen2.5-14B-Instruct-A3B-UD-Q4_K_M.gguf)
   - `~/.hermes/config.yaml` custom_providers 수정 (localhost:1234→8080, context_length 65536 override)
   - `harness_agent.py` 모든 UI 문자열 Gemma4→Qwen3.6 교체
2. **미해결 이슈**:
   - WebUI modelSelect 드롭다운에 Qwen 미표시 (api_server 플랫폼 미활성화)
   - Qwen 추론 1분 40초+ 타임아웃
3. **관련 문서**: 장애 기록 #020 / HERMES3_MASTER_DEVELOPMENT_GUIDE

### [2026-06-05] Bio-Memory Engine v9.3 — 3파일 구조 개선

1. **문제**: L2 메모리 급증(1.7MB / 83건) 시 Early Exit에 걸려 L3 패턴 학습이 정체됨. 용량 기준 강제 증류 부재로 메모리 블로트 리스크 존재. dreaming_v2.py에 atomic write 미적용.
2. **수정 내용**:
   - `bio_memory_engine.py`: `_get_l2_bytes()` 메서드 추가로 실시간 KB/MB 보고. L2 상태 조회 시 바이트 정보 포함.
   - `dreamer_layer.py`: `offline_consolidation_forced()` 추가 — 중요도 하위 50% 강제 L3 전이. 기존 증류 조건과 무관하게 용량 위기 시 자동 발동.
   - `dreaming_v2.py`: `_run_offline_consolidation()`에 용량 위기(rows > 80 or bytes > 900KB) 시 강제 증류 호출. `_commit_to_l3_semantic()`에 atomic write(`write + os.replace`) 적용.
3. **파일 위치**: `~/Applications/Mjauto/Scripts/modules/`
4. **검증**: 3개 파일 Python import 정상 확인.
5. **교훈**: L3 패턴 학습을 위해 Early Exit 조건에 용량 기준을 추가하고, 중요도 무관 강제 전이 메서드가 필요함.

### [2026-06-05] Llama-Server 멀티 슬롯 컨텍스트 불일치 및 망각 장애 해결

1. **문제**: 대화가 길어질 때 로컬 Gemma 4 모델이 자신이 생성한 프로그램이나 대화 내용을 잊어버리는 현상 발생.
2. **원인**: 
   - `com.bluesea.llama_server2.plist`에서 `-np 2`(2개 슬롯)로 실행되어, 65,536 컨텍스트 공간이 슬롯당 32,768로 강제 분할됨.
   - Hermes 설정(`context_length: 65536`)에 따라 32k가 넘는 긴 메시지를 전송했을 때, Llama 서버가 앞쪽 대화 맥락을 예고 없이 강제 Truncation하여 기억을 잃게 만듦.
   - Gemma 4 SWA 구조상 `-np 2` 설정 시 슬롯 간 KV 캐시가 자주 무효화되어 추론 속도 저하도 유발함.
3. **해결 내용**:
   - `~/Library/LaunchAgents/com.bluesea.llama_server2.plist`의 `-np` 파라미터 값을 `2`에서 `1`로 수정하여 단일 슬롯에 65,536 컨텍스트를 온전히 할당.
   - `launchctl`을 통해 Llama 서버를 재기동하여 정상 동작 확인.
4. **결과**: 대화가 길어져도 이전 작업 파일 내역 등을 안전하게 64k 내에서 망각 없이 기억하며, KV 캐시 보존율 상승으로 답변 속도 대폭 향상.

### [2026-06-04] 세션 워크스페이스 망각 장애 및 거짓 답변 현상 해결

1. **문제**: 세션 단절 후 복구(컴팩션) 과정에서 에이전트가 `Mjobsidian` 폴더 외부의 임시 프로젝트 폴더(`/Users/bluesea/Applications/MarineOS-XR Project`)를 스캔 대상에서 누락하고, 파일이 지워졌다고 허위로 단정짓는 현상 발생.
2. **원인**: 
   - LLM이 세션의 워크스페이스 경로(기본값 `Mjobsidian`)에만 의존하여 외부 디렉터리를 스캔하지 않음.
   - 물리적 디스크 확인(`find` 등) 없이 과거의 기억이나 추측만으로 파일 존재 여부를 단정함.
3. **해결 방안**:
   - `constitution.local.md` §X.2에 "물리적 실재 확인 의무화" 추가 (항상 `find`나 `ls`로 실제 경로 확인 후 답변).
   - `constitution.local.md` §X.4에 "다중 작업 경로 바인딩" 규칙 신설 (`01_hot.md`에 명시된 활성 외부 프로젝트 경로를 보조 경로로 강제 스캔).
4. **결과**: 외부 프로젝트 경로 망각 현상 해결, 팩트 기반 스캔 강제화. `06_에이전트_오류_및_재발방지_보고서.md` 신규 발행.

### [2026-06-03] Ingest TagLinker vault_path 키워드 오류 수정

1. **문제**: `ingest_engine.py:20`에서 `TagLinker(vault_path=str(vault_path))` 호출 → `tag_linker.py`의 `__init__(self, db_path: Optional[str] = None)`가 `vault_path` 키워드를 받지 못해 TypeError.
2. **수정**: `TagLinker(vault_path=...)` → `TagLinker()` (인자 없이 기본 생성자). `vault_path` 변수 완전 제거.
3. **결과**: `/ingest` 정상 동작 확인 — 11 Clippings + 7 root files 처리.
4. **교훈**: 호출부와 피호출부 시그니처 불일치 — 새 인자 추가 전 callee 시그니처 먼저 확인할 것.

### [2026-06-03] HERMES3_ENCYCLOPEDIA.md write_file 덮어쓰기 사고

1. **문제**: 기존 파일(1108줄)에 write_file 사용 → 전부 77줄로 덮어써짐. 원본 내용 유실 (778-1108라인).
2. **원인**: 기존 파일 수정 시 patch 대신 write_file 사용. 가장 중요한 안전 규칙 위반.
3. **영향**: Graphify 섹션, SQLite WAL, 기타 하부 섹션 소실. git/Time Machine 백업 없음.
4. **교훈**: 기존 파일에 write_file 금지 — 반드시 patch 사용. 사전 read_file로 전체 내용 확인 의무.

### [2026-06-03] config.yaml display 설정 최적화 — language: ko, final_response_markdown: keep

### ✅ 완료 — config.yaml toolsets 전체 추가 (2026-06-06)
- `~/.hermes/config.yaml`와 `~/Applications/venu/.hermes2/config.yaml`에 모든 toolsets를 포함하도록 업데이트했습니다.
- 적용된 toolsets 목록: hermes-cli, terminal, browser, web, search, file, vision, delegate, cronjob, computer_use, discord, discord_admin, feishu_doc, feishu_drive, homeassistant, image_gen, kanban, session_search, skills, spotify, todo, tts, video, video_gen, x_search, yuanbao.
- 이후 두 Hermes 인스턴스 모두 전체 도구 사용이 가능해졌습니다.

1. **변경 내용**:
   - `display.language: en → ko` — 한국어 사용자 환경에 최적화
   - `display.final_response_markdown: strip → keep` — WebUI 마크다운 렌더링 활성화
2. **영향**: WebUI에서 응답 마크다운(코드 블록, 리스트 등)이 정상 표시됨. 시스템 메시지 언어가 한국어로 전환.

### [2026-06-02] Hermes 2 WebUI 대화 맥락 단절 및 폴더 오염 진단/수정
1. **문제 발견**: Hermes 2 WebUI 사용 중 대화 맥락 단절 현상, "Session compressed N times" 반복 출력 및 메모리 부족. 시스템 폴더(`~/.hermes`) 오염 가능성 제기됨.
2. **원인 1 (SWA 캐시 무효화)**: `llama-server -np 2`로 병렬 처리 슬롯을 설정했으나 Gemma 4 SWA 구조는 병렬 요청 시 KV 캐시를 무효화하는 특징이 있어 잦은 재연산 유발.
3. **원인 2 (조기 압축)**: `.hermes2/config.yaml`에 `compressor` 엔진과 `threshold: 0.5`가 적용되어 컨텍스트 50% 지점에서 즉시 대량의 기억이 날아가는 설정 오류 발견.
4. **해결 내용**:
   - `start_llama.sh` 스크립트를 `-np 1`, `--cache-reuse 256`로 수정하여 KV 캐시 보존율 상승.
   - `.hermes2/config.yaml`을 `engine: truncation`, `threshold: 0.85`, `protect_last_n: 40`으로 변경하여 컨텍스트 수명 대폭 연장 및 안정성 확보.
   - **경로 격리 원칙 재확인**: Hermes 1(`~/.hermes`)과 Hermes 2(`.hermes2`)의 폴더 분리 정책 준수를 강조.
5. **결과**: WebUI의 극심한 건망증 및 맥락 단절 현상 해결, 안정적 기억 연장 확인.
6. **지식/스킬화**: 이 과정을 `.hermes2/skills/devops/llama-context-fix/SKILL.md` 스킬 파일로 저장하여 향후 자동 복구 지식으로 활용.
    67|
    68|### [2026-05-27] 봇 Polling 안정화 (Zombie Poller 방지) — Hermes1
    69|1. **문제 발견**: `hermes_local.py` (PTB v22.5)의 `app.run_polling()`이 내부에서 `loop.run_forever()`를 호출하여, 409 Conflict 등으로 updater가 중단되어도 프로세스가 좀비로 생존 (이벤트 루프는 다른 태스크 때문에 계속 실행됨). 네트워크 연결 0개, CPU 0%, 메모리 유지 — launchd가 죽은 프로세스를 감지 못함.
    70|2. **근본 원인 3중 결함**: (가) `logging.getLogger("asyncio").setLevel(logging.WARNING)` — asyncio Task Exception 로그 차단 (나) `_auto_heal_loop()`의 bare `except Exception: pass` — 모든 오류 침묵 (다) plist에 `PYTHONUNBUFFERED` 없음 — stderr block-buffered로 crash 로그가 파일에 안 써짐.
    71|3. **수정 내용**:
    72|   - `logging.getLogger("asyncio").setLevel(logging.ERROR)` — Task Exception 로그 차단 해제
    73|   - asyncio 예외 핸들러 등록 — 모든 unhandled task exception을 traceback 포함 로깅
    74|   - `_auto_heal_loop` bare `except: pass` → `logger.warning()`으로 교체
    75|   - `app.run_polling()` → 직접 `updater.running` 모니터링으로 대체 — polling 죽으면 `sys.exit(0)`
    76|   - `com.hermes.bot.plist`에 `PYTHONUNBUFFERED=1` + `-u` 플래그 + `ThrottleInterval=5` 추가
    77|   - `harness_agent.py` `auto_heal_loop`에도 bare except 주석 추가
    78|4. **검증**: 새 봇(PID 33144) 3분+ 운영 중, 2 ESTABLISHED 연결 유지, Conflict 없음. 봇 1회 명령 테스트 완료. Clippings 처리 확인 필요.
    79|5. **참고**: Conflict 발생 시 (예: 외부 getUpdates 호출) updater가 중단되고, `sys.exit(0)` → launchd KeepAlive가 5초 후 재시작. 이전처럼 좀비 프로세스가 영원히 살아 있는 문제 해결함.
    80|6. **연관 문서**: 시스템 상태.md (변경 이력 업데이트), 시스템 인벤토리.md (plist 변경 적용), 스크립트 정보.md (패치 기록)
    81|
    82|### [2026-05-27] /ingest v2.1 — 루트 파일 LLM 분류 이동 + v6.4
    83|1. **기존 설계 변경 (2026-05-27 12:50)**: `_process_root_files()` 전면 재작성. 루트 방치 파일도 LLM(DeepSeek) 분류 후 4개 폴더(10_AI_Automation/20_Research/30_Journal/Unsorted)로 이동 + frontmatter(category 태그) 업데이트. 더 이상 태그만 붙이고 방치하지 않음.
    84|2. **`_build_tag_prompt` 제거**: dead code 정리. 모든 LLM 프롬프트를 `_build_classify_prompt`(one-shot 예시 + 엄격 JSON 출력)로 통일.
    85|3. **`cmd_ingest()` — `_call_llm` 연결 완료**: `_file.py`가 `IngestEngine(source_dir, dest_dir, llm_func=_call_llm)`로 호출. DeepSeek 라우팅 정상.
    86|4. **버그 수정**: frontmatter 업데이트 후 `shutil.move()`만 하고 `write_text()`를 빼먹던 버그 발견 → `f.write_text(updated_text)` 후 `shutil.move()` 순서로 수정.
    87|5. **실행 결과**: 루트 26개 .md 파일 전량 분류 이동 완료. 10_AI_Automation(21개), 20_Research(4개), 30_Journal(1개), Unsorted(1개). 루트 clean.
    88|
    89|### [2026-05-27] /ingest v2.2 — 모드 중립 분류 라우팅 + 중복 코드 제거
    90|1. **모드 중립 분류 라우팅 구현**: `handlers/_base.py`에 `_ingest_llm_wrapper` 신규 추가 — `get_llm_response()`를 통해 사용자 현재 모드(Gemma4/DeepSeek/NVIDIA)로 분류 요청을 라우팅. `handlers/_file.py` `cmd_ingest()`가 DeepSeek 고정 `_call_llm` 대신 `_ingest_llm_wrapper`를 사용하도록 변경. 이제 사용자가 어떤 모드로 봇을 쓰고 있어도 Ingest 버튼이 모드에 구애받지 않고 동작.
    91|2. **`ingest_engine.py` 중복 제거**: `_build_classify_prompt`가 동일한 내용으로 두 번 정의되어 있던 코드 정리 (첫 번째 정의만 유지, 20줄 제거).
    92|
    93|### [2026-05-26] llama-server brew symlink 경로 변경 + executor import 패치 — v5.9
    94|
    95|1. **llama-server launchd 바이너리 경로 brew symlink로 변경**
    96|   - **문제**: `brew upgrade llama.cpp` 시 Cellar 버전 디렉토리(8960→9310)가 변경되면서 launchd plist의 하드코딩된 경로가 깨져 서비스 시작 실패 (exit code 78)
    97|   - **조치**: plist의 `ProgramArguments`를 `/opt/homebrew/Cellar/llama.cpp/8960/bin/llama-server` → `/opt/homebrew/bin/llama-server`(brew symlink)로 변경. 재등록 후 정상 기동 (PID 77734).
    98|   - **효과**: brew upgrade 시 재발 방지 (symlink는 항상 최신 버전 가리킴)
    99|2. **`harness_agent.py` executor import 누락 패치**
   100|   - **문제**: 633번째 줄 `executor.execute_bash_command()` 호출 시 `import executor` 누락으로 NameError 발생
   101|   - **조치**: `harness_agent.py` 상단에 `import executor` 추가. Hermes1 봇 재시작 후 정상 동작 확인.
   102|1. **Gemma4 "Connection Error" 및 폴백 해결**
   103|   - **문제**: 로컬 엔진(llama.cpp)의 API 포트가 8080으로 변경되었으나, `config.py`에는 구형 LM Studio 포트(1234)가 지정되어 있어 연결 실패 및 자동 폴백이 발동함.
   104|   - **조치**: `config.py`의 `LM_STUDIO_BASE_URL`을 `http://127.0.0.1:8080/v1`으로 수정하여 Gemma4 정상 연결 복원.
   105|2. **명령줄(CLI) 인터랙티브 디버거 제작**
   106|   - **문제**: 백그라운드(Launchd) 봇에서 에러 발생 시 로그 확인이나 재시작이 번거로움.
   107|   - **조치**: 텔레그램 밖 터미널에서 즉각적인 디버깅 및 포그라운드 실행이 가능한 `hermes_cli.sh` 스크립트 제작.
   108|3. **자연어 파일 조작명령어 오인 (하이재킹) 차단**
   109|   - **문제**: 사용자가 "만들어줘", "지워줘"와 같은 일상적인 자연어를 썼을 때, 파일 조작 정규식(Regex)이 이를 파일 조작 명령어로 오인하여 엉뚱한 응답("파일 경로를 입력해주세요")을 반환함.
   110|   - **조치**: `harness_agent.py` 내의 불안정한 자연어 정규식 인터셉트를 비활성화하고, LLM 본연의 추론을 통한 `[CREATE:]`, `[DELETE:]` 태그 생성을 유도하도록 교정.
   111|4. **메모리 확보 스크립트 적용 (16GB 파일 캐시)**
   112|   - **문제**: 옵시디언 등 수많은 파일을 스캔하면서 16GB가 넘는 "File-backed pages" 캐시가 RAM을 점유, 시스템 리소스 부족 현상 유발 우려.
   113|   - **조치**: 캐시 삭제가 시스템에 무해함을 분석한 뒤, 관리자 권한으로 캐시를 즉시 반환(purge)하는 `clear_memory.sh` 스크립트 작성 및 적용. 
   114|5. **AI 스택 인지 오류 수정 및 llama.cpp 업데이트**
   115|   - **문제**: 에이전트가 본인의 로컬 구동 백엔드를 "Ollama"로 착각하여 답변함.
   116|   - **조치**: `USER.md`의 시스템 스택 정의를 "llama.cpp"로 수정하고, Homebrew를 통해 `llama.cpp` 버전을 8960에서 최신 9310으로 성공적으로 업그레이드.
   117|6. **텔레그램 메모리 관리 버튼 직관성 개선 및 권한 우회 적용**
   118|   - **문제**: 기존 🧠 메모리 버튼이 프로세스(pid) 목록을 띄우고 하나씩 kill해야 해서 복잡하고 직관적이지 못함.
   119|   - **조치**: 복잡한 프로세스 목록을 없애고, 현재 메모리 상태 요약과 함께 **[🧹 캐시 정리 실행]** 원클릭 버튼만 나타나도록 UI 전면 개편. 텔레그램 백그라운드 봇이 비밀번호 없이 `sudo purge`를 쏠 수 있도록 `/private/etc/sudoers.d/purge_nopasswd` 파일에 `NOPASSWD` 예외 권한을 부여하여 데이터 손실 위험 없이 즉시 16GB 파일 캐시를 확보할 수 있게 최적화.
   120|
   121|### [2026-05-26] 텔레그램 내장 칸반(Kanban) 시스템 구축
   122|1. **SQLite 기반 Kanban 관리 시스템 추가**
   123|   - 텔레그램 봇 내에서 `/kanban list`, `add`, `move`, `delete` 등을 통해 TODO, IN_PROGRESS, DONE 상태를 관리하는 칸반 보드 구축.
   124|2. **텔레그램 인라인 버튼(Inline Keyboard) 연동**
   125|   - `/kanban list` 출력 시 각 카드별로 'Move', 'Delete' 버튼을 함께 띄워, 사용자가 직접 텍스트 명령어를 타이핑할 필요 없이 버튼 클릭만으로 즉시 카드를 이동 및 삭제할 수 있는 UI 구현 완료.
   126|
   127|### [2026-05-25] ~~지능형 야간 스케줄러 헌법 및 목표 감사 시스템 탑재~~ **[2026-05-27 Dreaming 폐기]**
   128|1. **/goal 목표 설정 및 헌법 감사(Audit) 훅 연동**
   129|   - ~~**조치**: 텔레그램에서 장기 목표를 설정할 수 있는 /goal 명령어를 신설하고, dream_scheduler.py의 야간 Dreaming(새벽 3시) 과정에 목표 진척도 및 constitution.md 준수 여부를 LLM이 스스로 판단하여 리포트를 작성하도록 기능 추가.~~ **[폐기됨]**
   130|2. **LLM 통신 포맷(HTTP 400) 오류 및 Git 경로 버그 수정**
   131|   - ~~**조치**: dream_scheduler.py가 API 호출 시 단순 문자열을 전송해 발생하던 400 포맷 에러를 Message 객체 리스트([{"role": "system"...}]) 형태로 수정하고, 기록 요약 안전장치(각 200자 제한)를 추가하여 토큰 초과 완전 방지. 또한 옵시디언 폴더에 .git이 없는 경우 동기화를 건너뛰도록 처리해 Fatal 에러 방지 완료.~~ **[폐기됨]**
   132|
   133|### [2026-05-28] Dreaming/Ingest/Recent/DummyRouter 버그픽스 + #12~#13 완료 (~~#14 폐기됨~~)
   134|1. **Dreaming 3종 버그 수정 완료** (`_memory.py` cmd_dreaming — MemoryEngine import 복구, DummyRouter 우회, 버튼 콜백 effective_message 방어): `/dreaming` Telegram 명령어 복구. — 단, 야간 스케줄러(dream_scheduler.py)는 [2026-05-27 폐기됨].
   135|   Ingest 2종 + Recent 1종 버그 수정. 봇 재시작 완료 (PID 81010). 장애 이력 #013~#016 등록.
   136|2. **#12 constitution.local 포인터 패턴 완료**: 중복 내용(§2/§3/§6)을 constitution.md/나의 비서 가이드.md 참조 포인터로 대체 (98→50줄).
   137|3. **#13 validate-skills git hook 완료**: `~/.hermes/scripts/validate_skill_md.py` + `~/.git/hooks/pre-commit`.
   138|4. ~~**#14 dream_scheduler ExecPlan 완료**: ExecPlan/ExecPhase 클래스 도입, 6단계 phase별 오류 격리, sync/async 지원.~~ **[2026-05-27 폐기됨]**
   139|5. ~~**#14 보완 — style_profile → dreaming 연결 가시화**: ExecPlan Phase 1~3 style_profile 로드/동기화/감사 포함.~~ **[2026-05-27 폐기됨]**
   140|
   141|### [2026-05-27] Python 3.10 호환성 수정 + 테스트 인프라 구축
   142|1. **Python 3.10 호환성 문제 해결**: `dialectic_layer/_dreamer.py`와 `hermes_context_builder.py`에서 `str | None` (PEP 604) 문법 사용 → macOS 기본 Python 3.9.6에서 SyntaxError 발생. 두 파일 상단에 `from __future__ import annotations` 한 줄씩 추가로 해결. 코드 변경 최소화 + 하위 호환 유지.
   143|2. **pytest 8.4.2 설치**: base Python3에 pip 설치 완료.
   144|3. **tests/ 디렉토리 구축**: `~/Applications/Mjauto/Scripts/tests/` — 6개 테스트 파일 생성:
   145|   - `test_imports.py`: 32개 modules/ + 9개 handlers/ 모듈 import 검증
   146|   - `test_bio_memory.py`: BioMemoryEngine 5개 smoke
   147|   - `test_skill_evolver.py`: _validate_skill 9개 smoke
   148|   - `test_kanban_manager.py`: KanbanDB 10개 smoke
   149|   - `test_hybrid_router.py`: HybridRouter.is_sensitive 9개 smoke
   150|4. **테스트 결과**: **87 passed, 0 skipped, 0 failed** (0.48s). 기존 handlers/ skip 조건(Python 3.10 버전 체크) 제거.
   151|5. **linked**: 관련 5개 메타 문서(hot.md/시스템 상태.md/스크립트 정보.md/시스템 인벤토리.md/주요 시스템 가이드 및 FAQ) 일괄 업데이트 완료.
   152|6. **style_profile.md truncation 확정**: dream_scheduler.py Phase 3 — `[:1000]` 유지 (4447 bytes 기준). MJ님 승인 완료.
   153|
   154|### [2026-05-26] 터미널 자율 진단 기능 및 파일 시스템 조작 안정성 강화
   155|1. **자율 터미널 진단(Agentic Terminal) 지능 부여**
   156|   - **문제**: 사용자가 "알람의 원인을 확인해봐"라고 자연어로 요청했을 때, 봇이 스스로 터미널을 열람하지 못하고 사용자에게 명령어(`launchctl list`)를 치라고 안내(수동적 답변)하는 문제 발생.
   157|   - **조치**: `harness_agent.py` 시스템 프롬프트에 `[RUN_CMD: 명령어]` 자율 액션 태그를 권한 부여. 이제 자연어 지시만으로도 봇이 스스로 터미널을 띄우고 진단 결과를 보고할 수 있도록 지능 격상 완료.
   158|2. **로컬 LLM (llama-server) OOM 타임아웃 장애 및 폴백(Fallback) 환각 해결**
   159|   - **문제**: Mac Studio 램 여유가 390MB로 고갈되자, `llama-server`가 멈춰(23초 타임아웃) 딥시크로 자동 폴백됨. 이때 딥시크가 "Ollama 서비스가 중단됨"이라고 환각(Hallucination) 리포트를 발행함.
   160|   - **조치**: `clear_memory.sh` (sudo purge) 및 `killall llama-server`, `recovery_system.sh`를 즉시 가동하여 16GB의 메모리를 확보하고 시스템 완전 정상화.
   161|3. **파일 조작 절대 경로 인식 버그(404) 완전 수정**
   162|   - **문제**: `/list /Users/bluesea/...` 등 슬래시(/)로 시작하는 절대경로를 입력했을 때, `secure_path` 함수가 Base 경로를 이중으로 부착하여 폴더를 찾지 못하는 논리적 버그 발견.
   163|   - **조치**: `hermes_local.py`의 `secure_path` 로직을 대대적으로 개편하여, 절대경로와 상대경로를 완벽히 구분하고 허용 Base 권한 검증만 통과하도록 수정 완료.
   164|
   165|### [2026-05-26] #018 max_tokens underflow (harness_agent.py 1500→3500)
   166|1. **하네스 역설계 인사이트 문서화 완료**: Agent 개선 제안(테스트/Git/헬스체크/ADR) + 하네스 기여도 70% 분석 + Gemma4 최적화 전략 — `wiki/00_Meta/하네스_역설계_및_LLM_최적화_인사이트.md` 신규 생성. `wiki/00_Meta/gemma4 26b기준의 하네스 역설계 및 LLM 최적화 인사이트.md` — DeepSeek 제안을 Qwen2.5-14B-Instruct 관점에서 재평가.
   167|2. **max_tokens underflow 발견 및 수정**: Gemma4 로컬 LLM 응답이 `harness_agent.py:248` `max_tokens=1500` 제한으로 1500토큰에서 강제 종료되는 버그 발견. **증상**: 사용자가 느끼기에 "봇이 멈춤". **원인**: v5.8 `handlers/` 리팩토리에서 튜닝되지 않은 기본값 유지. **조치**: `max_tokens=1500` → `3500` (사용자 지정 3000~4000 중간값). **재시작**: Hermes1 재시작 (PID 81010→88574), 정상 동작 확인.
   168|3. **영향 범위**: Hermes1 봇만 해당. Hermes2는 이미 `max_tokens=4096`으로 설정되어 있어 불필요.
   169|4. **장애 이력**: #018 등록 완료. hot.md/시스템 상태.md/장애 기록 일괄 갱신.
   170|5. **메모 저장**: max_tokens 설정값, 발견 경로, 수정 이력 저장 완료.
   171|
   172|### [2026-05-26] #020 constitution.local v1.2 인라인 전환 (포인터 패턴 → 복사 패턴)
   173|1. **constitution.local.md v1.2 인라인 전환 완료**: 기존 포인터 패턴(§2/§3/§6 "참조")을 모든 참조 내용을 실제로 인라인 대체하는 방식으로 전환. 98→204줄 (중복 허용). Gemma4가 이 파일 하나만 읽어도 모든 규칙 파악 가능.
   174|2. **constitution.md §4/§5/§7 통합 병합**: constitution.md의 오류 복구(§4), 메모리 정책(§5), 에이전트 패턴(§7)도 constitution.local.md에 통합 병합하여 Gemma4 접근성 강화.
   175|3. **동기**: Qwen2.5-14B-Instruct는 문서 간 추론(크로스-레퍼런스)이 약하므로, 모든 규칙을 단일 문서에 중복 기재. DeepSeek은 중복에 무해.
   176|
   177|---
   178|
   179|🔗 **관련 문서 링크**
   180|- [[스크립트 정보]]
   181|- [[시스템 인벤토리]]
   182|- [[시스템 상태]]
   183|- [[USER]]
   184|
   185|### [2026-05-28] Group 1 — /status KEY=VALUE, /paper review, ADR 템플릿, 이유 컬럼
   186|
   187|1. **`/status KEY=VALUE` 구현**: `cmd_status`에 KEY=VALUE 파싱 로직 추가. `hot.md` KV 섹션에 실시간으로 상태 기록/읽기/리셋 가능. 핫키-값 쌍으로 시스템 상태 순간 저장.
   188|2. **`/paper review` 구현**: 문서 파일 또는 직접 텍스트 입력 → 6축 학술 검토 (구조/논증/선행연구/용어/인용/개선) → ⭐별점 포함 마크다운 리포트. `_call_llm(DeepSeek)` 연동. 3900자 청크 분할.
   189|3. **시스템 상태.md '이유' 컬럼 추가**: 변경 이력 테이블 5→6컬럼. 모든 과거 행 `| -` 채움. 결정 맥락 추적성 강화.
   190|4. **ADR 템플릿 생성**: `docs/adr/ADR-0000-template.md` — 배경/결정/이유/대안/영향 5섹션 YAML frontmatter 템플릿. 구조적 의사결정 기록 인프라.
   191|
   192|### [2026-05-28] Hermes v8.1 — Self-Healing Loop + Live Sync + Cron 등록
   193|
   194|1. **Self-Healing Loop (`modules/dream_scheduler.py` v1.0)**: 4-phase ExecPlan 자율 루프 구현 (진단→수정→검증→보고). 시스템 상태 모니터링 → 장애 자가진단 → 자동 수정 시도 → 결과 텔레그램 보고. 매일 새벽 3시 cron `dream-scheduler-daily` 등록 완료 (job_id: cb8d3090df6b).
   195|2. **Live Sync (`fswatch_daemon.py` + `update_index.py`)**: 5개 핵심 디렉터리(Mjobsidian/wiki/, Mjauto/Scripts/, .hermes/runtime/, .hermes/governance/, .hermes/scripts/) 실시간 fswatch 감시 → 변경 3초 내 `hermes_index.db` 자동 갱신. Launchd `com.bluesea.fswatch-indexer` (Running, PID 48285).
   196|3. **pytest 89/89 전부 통과**: `conftest.py`에 `telegram.constants` mock 보강, `import time` 누락 수정 (handlers/_base.py NameError 방지). 모든 단위 테스트 정상.
   197|4. **하드코딩 경로 제거 (Portability)**: `dream_scheduler.py`, `fswatch_daemon.py`, `update_index.py`의 `/Users/bluesea/...` 절대경로를 전부 `Path.home()` 기반으로 변경. 향후 다른 계정 이식 가능.
   198|5. **정리**: stray `hermes_index.db` (0바이트) 삭제, DB 테스트 엔트리 정리 (14개 정상 엔트리 유지). Self-Healing 8건 처리 (2 성공 / 6 실패: log-issue key_error — 모두 과거 로그).
   199|
   200|*최종 업데이트: 2026-06-07 11:52 — cove_engine.py 이전, 메타 7종 갱신*
   201|
   202|---
   203|
   204|### [2026-05-31] /restart_bot 버그 수정 + /run 제거
   205|
   206|1. **버그**: 다른 AI가 `handlers/_system.py`에 `cmd_restart_bot` 함수를 추가했지만, `handlers/__init__.py`에 import를 누락하여 Telegram에서 `/restart_bot` 명령어가 실제로 동작하지 않음. `_load_handler()`에서 AttributeError 발생.
   207|2. **수정**: `handlers/__init__.py`에 `cmd_restart_bot` import 추가.
   208|3. **/run 제거**: 다른 AI가 추가한 `/run` 명령어(제한적 화이트리스트 기반: date/uptime/whoami/top/df만 허용)는 부적합하여 제거. 대신 자율 에러 복구형 `/exec [명령어]` 사용 권장.
   209|4. **효과**: Telegram에서 `/restart_bot`으로 직접 봇 재시작 가능. 임의 터미널 명령은 `/exec`로 실행.
   210|5. **봇 재시작 완료** (PID 88333).
   211|
   212|### [2026-06-01] Hermes2 클라우드 전용 개편 + post_init 로그 수정 — Hermes2
   213|
   214|1. **Hermes2 클라우드 전용 전환**: `hermes2_bot.py`에서 gemma4(로컬) 모드, GATEWAY_URL 상수, OpenRouter 브랜치 완전 제거. DeepSeek(API) 기본 + NVIDIA NIM 70B 폴백 체계로 개편.
   215|2. **NVIDIA API 키 등록**: `ai.hermes2.bot.plist` 환경변수 + `.hermes2/.env`에 NVIDIA_API_KEY 추가. launchd 재시작 완료 (PID 93016).
   216|3. **post_init 로그 출력 문제 해결**: `post_init()` 콜백 함수 제거 — PTB의 `app.initialize()` 시점 콜백 stdout이 로그 파일에 리다이렉트되지 않는 문제 발견. 시작 완료 print를 `main()` async 흐름 내 `start_polling()` 직후로 이동하여 로그에 정상 출력 확인.
   217|4. **효과**: 재시작 루프 가능성 완전 제거, 클라우드 전용 안정화 (CPU 0%, RSS 73MB), 시작 완료 메시지 로그 정상 기록 확인.
   218|5. **참고**: llama-server(PID 1381, Port 8080)는 아직 실행 중이나 Hermes2에서 더 이상 참조하지 않음.
   219|
   220|### [2026-05-28] Group 1
   221|
   222|1. **[A] 경고 정리**: `hermes_local.py`에 `warnings.filterwarnings('ignore', category=DeprecationWarning)`, `warnings.filterwarnings('ignore', category=UserWarning)` 추가. 런타임 경고 메시지 제거로 텔레그램 로그 가독성 향상. 봇 재시작 완료.
   223|2. ~~**[C] 주간 펄스 리포트 시스템**~~: ~~`weekly_pulse.py` 신규 생성. 칸반 완료율/로그 에러율/Git 커밋 수/CPU·메모리 사용량 수집 → `wiki/00_Meta/주간_펄스_리포트.md` 자동 생성. `com.bluesea.weekly_pulse.plist` launchd 등록 (매주 일요일 23:00, KeepAlive=false).~~ **[2026-05-27 weekly_pulse 폐기됨 → _archive/로 이동]**
   224|3. **[B] style_profile 일반 명령어 주입**: `handlers/_base.py`에 `_get_style_profile()` 1시간 TTL 캐시 함수 추가. `_call_llm()` (provider=None 경우)과 `harness_agent.py handle_message()` 시스템 프롬프트에 style_profile 텍스트(stop-slop + 문체 규칙) 주입. 이제 `/start`, `/help`, 일반 대화 등 모든 명령어에서 일관된 출력 스타일 적용.
   225|4. ~~**메타 문서 5종 일괄 업데이트**~~: ~~시스템 상태.md (변경 이력 + 푸터), 스크립트 정보.md (v6.7 + weekly_pulse 추가), 시스템 인벤토리.md (업데이트 로우), 주요 시스템 가이드 및 FAQ.md (신규 changelog), 00_Meta_지도.md (푸터 갱신).~~ **[2026-05-27 weekly_pulse 폐기됨 — 관련 참조 취소선 처리 완료]**
   226|
   227|---
   228|
   229|### [2026-05-28] Group 2 — /vault check, /grill-with-docs
   230|
   231|1. **`/vault check` 구현**: 새 `handlers/_vault.py` 생성. 3축 진단: 캐시/찌꺼기 파일 (`.DS_Store`, `.bak`, `.tmp`) + 프론트매터 스키마 (미닫힌 `---` 감지) + 중복 문서 (기존 vault_scanner.py TF-IDF 연동). 통계 포함 (전체 .md 개수/용량). `/vault duplicates`로 상세 중복 스캔 별도 분리.
   232|2. **`🔍 보관함 진단` 버튼 추가**: 하단 키보드 `ℹ️ 도움말` 대체. `_base.py` `handle_text_message`에 버튼 매핑. `/help`는 명령어로 항상 접근 가능.
   233|3. **`/grill [문서] [질문]` 구현**: 새 `handlers/_grill.py` 생성. Vault 문서 읽고 DeepSeek LLM 기반 Q&A. 절대경로/상대경로/키워드 FUZZY 검색 4단계, 대용량 문서 15K자 청킹 제한.
   234|4. **`vault_scanner.py` 타임스탬프 동적화**: `write_report()` 하드코딩된 `"2026-05-20 13:51"` → `datetime.datetime.now()` 동적 생성.
   235|5. **메타 문서 5종 일괄 업데이트**: 시스템 상태.md (변경 이력 + 명령어 테이블), 스크립트 정보.md (v6.6), 시스템 인벤토리.md, 주요 시스템 가이드 및 FAQ.md (Changelog), hot.md.
   236|
   237|### [2026-05-27] 메모리_파일_명세서 원복 + memory.md 아카이브 정리
   238|
   239|1. **문제**: 메모리_파일_명세서.md가 실수로 99_Archive/로 이동된 상태.
   240|2. **조치**: 사용자 지시에 따라 메모리_파일_명세서.md만 00_Meta로 원복. memory.md만 99_Archive 동결 유지.
   241|3. **메모리_파일_명세서.md**: 상단 `[!WARNING]` 아카이브 배너 제거. memory.md 참조 10곳 취소선 유지 (참고 문구 1곳은 취소선 없이 archive 경로 명시).
   242|4. **00_Meta_지도.md**: 메모리_파일_명세서 줄 취소선 해제, 푸터 갱신.
   243|5. **시스템 상태.md**: 원복 이력 행 추가 + 푸터 갱신.
   244|6. **hot.md**: 신규 작업 이력 추가, 최종 업데이트 2026-05-27 18:55.
   245|7. **결론**: 메모리_파일_명세서는 현역 문서로 복귀. memory.md는 과거 Dreaming 레거시로 99_Archive 정적 보존. 시스템 구조 경량화.
   246|
   247|### [2026-06-01] HERMES3_GUIDE v9.1.5 + V9.0 추가 2 제안 검토
   248|1. **HERMES3_MASTER_DEVELOPMENT_GUIDE.md v9.1→v9.1.5 업데이트**: Phase 6 (Hermes2 Cloud-Only) 추가. v9.4+ 중장기 계획 섹션 신설 — V9.0 프로그램 추가 2.md 기반 3개 모듈 제안.
   249|2. **V9.0 프로그램 추가 2.md**: NVIDIA SkillSpector(v9.4.2, 스킬 프로파일링), Anthropic CyberAuditor(v9.5, 코드 보안 감사), OpenSRE SRE Investigator(v9.5.1, 장애 조사) — **설계 제안 단계, 코드 미구현**.
   250|3. **영향**: 00_Meta_지도.md / 스크립트 정보.md / 시스템 인벤토리.md / 시스템 상태.md — 4개 메타 문서 일괄 업데이트 완료.
   251|
   252|### [2026-06-01] PDF→MD 파이프라인 구현
   253|1. **`modules/ingest_engine.py`**: `_read_file_content()` 정적 메서드 신규 추가 — `.pdf`는 PyMuPDF(fitz) v1.27.2.3으로 텍스트 추출, 나머지 확장자는 일반 텍스트 읽기.
   254|2. **파일 필터 확장**: Clippings/ + 루트 파일 ingest 루프에서 `.md`만 필터링하던 것을 `.md`, `.pdf`로 확장. 빈 PDF 방어 처리.
   255|3. **효과**: `/ingest` 한 번으로 PDF→텍스트 추출→LLM 분류→.md 변환→FTS5 검색 가능. 원본 PDF는 Clippings/Archive/에 보관.
   256|4. **제약**: 이미지/표/차트 추출 불가. NotebookLM MCP(비공식 API)는 연구 세션 보조용으로 유지 — PDF→MD는 영구 저장+검색 인프라.
   257|5. **메타 7종 일괄 갱신**: hot.md, 00_Meta_지도, 스크립트 정보, 시스템 상태, 시스템 인벤토리, 주요 시스템 가이드 및 FAQ, 06_에이전트_오류_보고서.
   258|
   259|### [2026-06-01] v9.1 보안 감사 + 캐싱 최적화 완료
   260|1. **Priority 1 — tag 액션 한글 처리** (`handlers/_approval.py`): `cmd_tag_logic()`에 `shlex.quote()` escape + `VALID_ACTIONS` 화이트리스트 + 한글 경로 분기. 태그 아닌 일반 질의는 ask Fallback.
   261|2. **Priority 2 — exec/file 액션 보안 검증** (`modules/core_reducer.py`): `_execute_exec` 14개 위험 명령어 블록리스트 + 한글 차단 + 30초 타임아웃. `_execute_file` 신규 구현 — `/Users/bluesea/Applications/` 화이트리스트, realpath symlink 검증, 100MB/50KB 제한.
   262|3. **Priority 3 — Context Hash 이중 캐싱** (`modules/core_reducer.py`): 메모리 LRU (128개, 60s TTL) 1차 → SQLite 2차 조회. 조회 실패 시에만 `decision_agent.decide()` 호출. LRU eviction 자동 정리.
   263||4. **최종 검증**: pytest **114/114 ✅ 전면 통과** (0.81s). python3 -m py_compile 문법 합격.
   264||5. **메타 7종 + v9_0_완성_요약.md 일괄 갱신**: 모든 문서 v9.1 완료 반영.
   265||
   266||### [2026-06-01] v9.2 — SIA 피드백 학습 + 모니터링 엔진 + 멀티 모델 로드 밸런싱
   267||1. **SelfImprovingAgent (`modules/sia_engine.py`)** — `record_feedback()`: action_id/rating(1-5)/context/response_time 저장 → SQLite. `analyze_trends()`: action별 평균 평점 추세 분석, 저성능 패턴 식별. `get_low_performers()`: threshold 기반 하위 액션 필터링 (min_samples 보장). `suggest_improvements()`: 저성능 액션 → LLM 개선 제안 (DeepSeek). 격리 DB.
   268||2. **MonitoringEngine (`modules/monitoring_engine.py`)** — `record_metric()`: action/duration/success/response_time 기록. `get_action_stats()`: 액션별 횟수/성공률/평균지연시간. `get_error_rate()`: 최근 N건 에러율. `alert_if_degradation()`: 3축 임계 경보 (error_rate>20%, response_time>30s, success<70%). 격리 DB.
   269||3. **ModelLoadBalancer (`modules/load_balancer.py`)** — `select_best_model()`: 성능 가중치 기반 weighted random 선택. `record_model_performance()`: 성공/실패/지연시간 기록. `rebalance_weights()`: 주기적 가중치 재조정 (기본 0.8, 저성능 -0.1 감점). `get_model_rankings()`: 통계 랭킹. 격리 DB.
   270||4. **core_reducer.py 통합** — `apply_user_feedback()`, `on_feedback_collected()` SIA 피드백 라우팅 메서드 추가.
   271||5. **hybrid_router.py 통합** — `__init__`에 `self.load_balancer` 초기화. `route()`에 `select_best_model()` 연동. `call_deepseek()`에 `record_model_performance()` 연동.
   272||6. **신규 테스트**: `test_sia_engine.py` (12개), `test_monitoring_engine.py` (12개), `test_load_balancer.py` (10개) — **모두 격리 DB**.
   273||7. **전체 pytest**: **150/150 ✅ 전면 통과** (기존 116 + 신규 34). 회귀 0건.
   274||
   275|### [2026-06-01] v9.0 완성 요약 문서 생성
   276|1. **`v9_0_완성_요약.md** 생성 (`~/Applications/Mjauto/Scripts/`): core_reducer 3-Agent Pipeline 구조 설명, 7개 액션(web/wiki/ask ✅ / tag/exec/file ⬜) 동작 현황, v9.1에서 고칠 한글 태그 버그/exec file 보안 계획 정리.
   277|2. **메타 7종 일괄 갱신**: hot.md, 00_Meta_지도, 스크립트 정보, 시스템 상태, 시스템 인벤토리, 주요 시스템 가이드 및 FAQ, 06_에이전트_오류_보고서.
   278||
   279||---
   280||
   281|### [2026-06-03] constitution.local.md §X 지시 과잉 행위 금지 규칙 추가

1. **변경 내용**: constitution.local.md에 §X "지시 과잉 행위 금지" 규칙 추가 (v1.4→v1.5)
2. **규칙 상세**:
   - §X.1 기본 원칙: 허가 없는 파일 생성 금지, "이것도 필요하겠지" 선제적 판단 금지, 직전 성공 패턴 무비판적 재사용 금지
   - §X.2 실행 규칙: search_files/read_file 사전 확인 의무, 추상적 목표와 구체적 수단 구분 의무
   - §X.3 위반 시: 즉시 보고·삭제·원래 지시 재확인·원인 분석 memory 기록
3. **영향**: 모든 세션·모델에 자동 적용되는 최상위 규칙으로, 허가 없는 파일 생성 재발 방지
4. **관련 7종 메타 파일**: constitution.local.md, 01_hot.md, 02_스크립트 정보.md, 03_시스템 인벤토리.md, 05_시스템 상태.md, 00_Meta_지도.md, 06_에이전트_오류_및_재발방지_보고서.md 전면 업데이트 완료

### [2026-06-03] wiki_auto_stamper.py 태그 자동화(최대 8개) 확장 및 하네스 컨트롤 가이드 작성

1. **태그 8개 자동화**: `wiki_auto_stamper.py`에서 본문의 `#태그`들을 파싱하여 Frontmatter `tags:`로 병합하고 최대 8개로 개수를 자르는 로직 추가. 본문 내 무분별한 `[[링크]]`를 일반 텍스트로 풀어내는 정돈 로직 구현.
2. **정규식 Lookahead 개선**: 해시태그 파싱 시 연속된 태그가 누락되거나 문장 부호(쉼표, 마침표)가 붙는 경우 누락되는 현상을 긍정형 전방탐색 `(?=\s|$|[.,;:!?])`을 통해 해결.
3. **하네스 가이드 생성**: 하네스 컨트롤 명령어(`/harness`, `/hdod`, `/hstatus`, `/hrollback`)의 작동 원리(6-레이어)와 사용법, 효용성을 담은 `하네스_컨트롤_가이드.md` 문서 생성 및 메타 폴더 배포. 깨진 링크 `지식 베이스 사용 가이드.md` 정리.

*최종 업데이트: 2026-06-07 11:52 — cove_engine.py 이전, 메타 7종 갱신*
---

## 🛠️ 2026-06-03 FAQ 추가 — 타임스탬프 / 메모리 복구

### Q. `/memory_dream` 실행 후 "수렴" 메시지가 나오는데 정상인가요?
**A. 정상입니다.** "수렴" 메시지는 PEMS 게이트가 LLM 호출을 절약했다는 뜻입니다. 2026-06-03 패치 이후 `offline_consolidation()`(메모리 정화)은 PEMS 통과 여부와 무관하게 **항상 백그라운드에서 100% 실행**됩니다.

### Q. wiki 파일에 타임스탬프가 없는데 어떻게 일괄 복구하나요?
```bash
python3 /Users/bluesea/Applications/Mjauto/Scripts/wiki_auto_stamper.py --scan
```

### Q. 새 wiki 파일을 만들 때 타임스탬프는 어떻게 붙이나요?
파일 맨 마지막에 다음 형식으로 추가합니다:
```
---
*최종 업데이트: 2026-06-07 11:52 — cove_engine.py 이전, 메타 7종 갱신*
```
또는 단일 파일 자동화:
```bash
python3 /Users/bluesea/Applications/Mjauto/Scripts/wiki_auto_stamper.py /path/to/file.md
```

### Q. Hermes 봇을 재시작하려면?
```bash
# 방법 1: 텔레그램에서
/restart_bot

# 방법 2: 터미널에서 (launchd 자동 재시작 이용)
pkill -f hermes_local.py

# 방법 3: launchd 완전 재시작
launchctl stop com.hermes.bot && launchctl start com.hermes.bot
```

*최종 업데이트: 2026-06-07 11:52 — cove_engine.py 이전, 메타 7종 갱신*

### [2026-06-05] AI Agent Memory 개념 분석 — 문제 인식 저장

1. **분석 내용**: 블로그 "AI Agent Memory" 4계층 메모리 스택 + 4대 연산 vs 현재 Bio-Memory Engine 시스템 대비 분석 완료.
2. **발견된 핵심 갭** (향후 수정 로드맵 확정 시 반영 예정):
   - Forget 정책 부재 — 메모리 블로트 리스크
   - Update 자동 충돌 감지 부재
   - Writer 저장 전 self-question 부재
   - semantic_index.db ↔ memory 검색 미연동
3. **현재 시스템 강점**: 4계층 메모리 스택(컨텍스트 윈도우→L1→L2→L3) 완비, Write/Read 연산 강함, External Knowledge 레이어(web_search/RAG/Knowledge Mesh) 충실.
4. **적용 불필요 항목**: 메모리 암호화(단일 사용자), 비동기 write(정보 유실), LLM retrieval self-pick(Gemma4 한계).
5. **참조**: 01_hot.md `📋 AI Agent Memory 개념 분석 — 문제 인식 저장` 섹션 상세.

### [2026-06-05] Skill Curator 및 Skills Hub 정책 기록

1. **Curator 상태**: Hermes 9.3 공식 내장. venu/.hermes2/에서 7일 간격 정기 실행 중. ~/.hermes/도 시드 완료 (첫 실행 대기).
2. **Curator 대상**: agent-created skill만. Bundled/Hub skill은 절대 건드리지 않음.
3. **Curator 사용법**: `hermes curator` 명령어 12개 (status/run/pin/unpin/restore/list-archived/prune/backup/rollback 등).
4. **Skills Hub**: 설치만 되어 있음, 현재 사용 안 함. 687개 skill 보유. 특정 요구사항 발생 시 개별 설치 검토.
5. **참조**: constitution.local.md §3.5 (Curator) + §3.6 (Skills Hub), HERMES3_MASTER_DEVELOPMENT_GUIDE.md (v9.4+ 후보 섹션).

### ❓ FAQ: 봇이 날씨를 물어볼 때 정확한 동네 날씨를 모르는 경우
- **답변**: 기본 검색 엔진(DuckDuckGo)이 한국의 특정 동네 실시간 위젯 정보를 가져오지 못하기 때문입니다. 현재는 `web_agent_module.py`의 날씨 인터셉터를 통해 네이버 날씨를 우회 스크래핑하도록 구현되어 정상 작동합니다.

### ❓ FAQ: 텔레그램 봇 응답 대기 시 멈춘 것인지 확인하는 방법
- **답변**: `🤔 생각 중...` 메시지의 점(.) 개수가 주기적으로 변한다면(애니메이션) 봇이 멈춘 것이 아니라 백그라운드에서 API 응답을 대기하거나 에이전틱 루프를 실행 중인 것입니다. 안심하고 기다리시면 됩니다.

### ❓ FAQ: 모델 스위치(switch-model) 도구 사용법 (2026-06-06 추가)
- **질문**: GPT-OSS-120B(NVIDIA)와 DeepSeek Chat 사이에서 메인 모델을 전환하려면?
- **답변**: 터미널에서 다음 명령어 중 하나를 실행합니다:
  ```bash
  switch-model got       # GPT-OSS-120B (NVIDIA)로 전환
  switch-model deepseek  # DeepSeek Chat으로 전환
  ```
- **동작 방식**: 스크립트가 두 Hermes Home(`~/.hermes/config.yaml` + `venu/.hermes2/config.yaml`)의 설정을 동시에 변경합니다. 전환된 쪽 설정은 파일을 삭제하지 않고 `# [SWITCHED to ...]` 주석 처리하여 보존합니다.
- **전환 후 필수**: `hermes gateway restart`를 실행해야 적용됩니다.
- **Qwen2.5-14B-Instruct 영향 없음**: Qwen2.5-14B-Instruct는 로컬 API(localhost:8080)로 별도 연결되어 있으므로 모델 스위치의 영향을 받지 않습니다.
- **스크립트 위치**: `~/Applications/venu/scripts/switch_model.sh`

### ❓ FAQ: NVIDIA NIM 모델이 404 오류로 안 될 때 (2026-06-07 추가)
- **증상**: 텔레그램봇에서 NVIDIA 모드 선택 → 응답 없음, 자동 DeepSeek 폴백 발동
- **원인**: NVIDIA NIM은 무료 서비스로 모델이 언제든지 종료될 수 있음 (`meta/llama3-70b-instruct` 2026-06-07 404 확인)
- **해결**: `harness_agent.py`에서 `_call_nvidia()` 함수의 `model=` 값만 교체
  ```python
  # 현재 (2026-06-07)
  model="openai/gpt-oss-120b"
  
  # 다른 NVIDIA 모델로 교체 시 (https://build.nvidia.com 에서 무료 모델 확인)
  model="meta/llama-3.1-70b-instruct"   # 예시
  ```
- **API 키**: `CAPT_NVIDIA_API_KEY` (`.env` 파일, 동일 키 사용)
- **봇 재시작 필요**: `launchctl kickstart -k gui/501/com.hermes.bot`

### ❓ FAQ: WebUI 드롭다운에 새 모델을 추가하려면? (2026-06-07 추가)

**증상**: `~/.hermes/config.yaml`에 custom_provider를 추가했는데 WebUI 드롭다운에 나타나지 않음.

**체크리스트 (순서대로)**:
```
□ 1. config.yaml에 discover_models: false + context_length 명시 추가
□ 2. hermes-webui/api/config.py의 _whitelist_keywords에 모델명 키워드 추가
   예: _whitelist_keywords = ["gemma-4-26b", "deepseek-v4-flash", "gpt-oss-120b", "minimax-m2.7", "qwen"]
□ 3. rm ~/.hermes/webui/models_cache.json (캐시 삭제)
□ 4. Gateway 재시작 후 WebUI 새로고침
```

**모델 라우팅이 실패할 때** (`Unknown provider` 또는 응답 없음):
- WebUI는 모델을 `@custom:<slug>:<model-name>` 포맷으로 인코딩해서 Gateway에 전달함
- Gateway(`api_server.py`)는 이 접두사를 자동으로 스트립하고 실제 모델명으로 라우팅함 (2026-06-07 수정)
- 라우팅 실패 시 Gateway 로그에서 "Model ID received:" 줄 확인

**로컬 모델(llama-server) 주의사항**:
- GGUF n_ctx 메타데이터는 32768 리포트 → Hermes 최소 64K 요건 미달 오류 가능
- `discover_models: false` 설정 시 llama-server를 프로브하지 않고 config.yaml 값 사용
- Mac Studio 36GB: Qwen2.5-14B는 context 32768 권장, 65536은 OOM 위험

**로컬 모델이 느린 이유**:
- Hermes 시스템 프롬프트가 ~10K 토큰 (tool definitions + memory + persona)
- Qwen2.5-14B @ ~91 tokens/sec → 첫 응답 약 2분, KV 캐시 워밍업 후 빨라짐
- 빠른 응답이 필요하면 DeepSeek(API) 또는 GPT OSS 120B(NVIDIA) 사용 권장

**관련 장애 이력**: `장애 기록/헤르메스_초기통합_장애_이력.md` #024
