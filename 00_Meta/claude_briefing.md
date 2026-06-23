# Hermes Claude Briefing
생성일시: 2026-06-21 19:33
버전: Hermes v9.2

---

## 📌 참고
이 파일은 즉시 참조 용도입니다.
- **constitution.local.md** — 세션 시작 시 자동 스캔
- **01_hot.md** — 세션 시작 시 자동 스캔

## 🖥️ 현재 시스템 상태
#### 변경 내용

| 파일 | 변경 내용 |
|---|---|
| `app.py` | SCREENERS_KR dict 키 6개 `kr_X` → `X_kr` 형식으로 통일 (치명적) |
| `run_scan.py` | `run_one()` 함수에 `no_telegram: bool = False` 파라미터 추가, `args.no_telegram` NameError 수정 (치명적) |
| crontab | 07:30/17:30/18:00 작업 3개 `/usr/bin/python3` → `.venv/bin/python` 교체 (치명적) |
| `auto_scan_nasdaq500.py` | `sys.executable` → `PYTHON` 변수 (venv 우선, 없으면 sys.executable fallback) |
| `app.py:617` | `st.switch_tab("📊 차트 보기")` 제거 → 안내 메시지로 대체 (Streamlit 1.58 미지원) |
| `send_scan_result.py:52` | `load_latest_csv` 반환 타입 `pd.DataFrame | None` → `tuple | None` |

#### 버그 요약

| 번호 | 심각도 | 파일 | 증상 |
|---|---|---|---|
| BUG-1 | 치명적 | `app.py` | KR 검색식 키 불일치 → KR 스캔 argparse 검증 실패, 결과 폴더 미존재 경로 참조 |
| BUG-2 | 치명적 | `run_scan.py` | `run_one()`에서 `args` NameError — `args.no_telegram` 미전달 |
| BUG-3 | 치명적 | crontab | venv 미사용 → pandas/dotenv/requests/plotly import 실패 |
| BUG-4 | 경미 | `app.py` | `st.switch_tab` Streamlit 1.58 미지원 API 호출 오류 |
| BUG-5 | 경미 | `send_scan_result.py` | 반환 타입힌트 오류 (`DataFrame` → `tuple`) |

**에러 진단 포인트**:
- KR 스캔 argparse error → SCREENERS_KR 키 형식 확인 (`X_kr` 패턴)
- `run_one()` NameError → 호출부 3곳에 `no_telegram=args.no_telegram` 전달 여부 확인
- crontab 스캔 실패 시 `which python` → `.venv/bin/python` 확인

## 🚨 미해결 버그/장애
## 🔴 결함 #1: Zombie Poller (PTB run_polling 블로킹)
## 🔴 결함 #4: Telegram Markdown Parsing — 사용자 콘텐츠를 Markdown으로 전송
## ⚠️ 잠재적 구조적 리스크 (Potential Future Structural Risks)
**위험도:** 🔴 높음
**위험도:** 🔴 높음
- [ ] 모든 launchd 서비스가 `KeepAlive` + `ThrottleInterval` 설정?
- [ ] polling/수신 루프가 `run_forever()` 계열 사용? → 직접 모니터링으로 교체 필요?
- [ ] 프로세스 비정상 종료 시 로그가 남는가?
- [ ] `atexit` 등록된 모든 정리 함수가 SIGTERM에 실행되는가?
- [ ] 모든 `except:` 블록이 로깅 또는 재시도하는가?
- [ ] bare `except: pass`가 없거나 명시적 `# noqa` 주석이 있는가?
- [ ] asyncio logger 레벨이 WARNING 이하인가? (Task Exception 차단 위험)
- [ ] asyncio exception handler가 등록되어 있는가?
- [ ] stderr/stdout이 unbuffered 상태인가? (PYTHONUNBUFFERED / `-u`)
- [ ] 모든 LLM 백엔드(Gemma4, DeepSeek, NVIDIA)가 chat completions API에서 정상 응답?
- [ ] 빈 문자열, null, 에러 형식을 "성공"으로 오판하지 않는가?
- [ ] fallback 체인이 투명하게 로깅되는가?
- [ ] fallback 발생 시 사용자에게 통지되는가?
- [ ] 서로 다른 bot token을 사용하는 프로세스들이 각각 독립적인 env var를 읽는가? (공유 충돌 위험)
- [ ] thread-safe하지 않은 라이브러리(httpx, openai)가 스레드 간에 공유되지 않는가?
- [ ] 파일 기반 상태 공유(lock 파일, mode 파일)가 경쟁 조건 없이 동작하는가?
- [ ] 모든 예외 시나리오(네트워크 단절, API 타임아웃, 메모리 부족)에 대한 복구 경로가 있는가?
- [ ] launchd 재시작 후 이전 상태(예: 잠긴 lock 파일)가 복구에 지장을 주지 않는가?
- [ ] 연속 실패 시 에스컬레이션(알림, 서비스 중단) 경로가 있는가?
## 🔴 결함 #5: 메모리 명령어 누락 및 Dreaming 엔진 PEMS 고착화 문제
## 🔴 결함 #6: 문서 무결성 시스템(타임스탬프) 붕괴 — System Drift
| `constitution.md`에 문서 관리 규칙 섹션 없음 | 규칙 공백 | 🔴 높음 |
| AI 에이전트가 내용만 수정하고 타임스탬프 갱신 누락 반복 | 행동 패턴 | 🔴 높음 |

## 🧠 메모리 현황
아래 구조가 위 설계의 **L1~L3 저장소 계층**을 담당하며, 각각이 전담 모듈에 의해 관리됩니다.
| 1 | `memory.json` | *(구 L1)* | `Scripts/memory.json` | 구 HistoryManager 단기 버퍼 (harness_v2 시절) | **🪦 사망** |
| 2 | `harness_memory.json` | **L1 — 단기** | `Scripts/harness_memory.json` | 현재 활성 단기 대화 버퍼 | **✅ 활성** |
| 3 | `episodic_memory.json` | **L2 — 에피소딕** | `~/.hermes/runtime/memory/episodic_memory.json` | 중기 경험·사건 저장 | **✅ 활성** |
| 4 | `semantic_memory.json` | **L3 — 시맨틱** | `~/.hermes/runtime/memory/semantic_memory.json` | 장기 개념·패턴 저장 | **✅ 활성** |
hot.md (작업 캐시)  ← L1: harness_memory.json
memory.md (핵심 기억) ← L2: episodic_memory.json ~~— memory.md는 Dreaming 폐기로 정적화 (2026-05-27)~~
                        + L3: semantic_memory.json
#### 2-2. harness_memory.json ✅ L1 (단기 대화 버퍼)
| **역할** | **Hermes1 L1 단기 작업 기억 (Working Memory)**. 모든 에이전트가 공유하는 최근 대화 내역. 봇 재시작/스위칭 시에도 맥락 유지 |
| `modules/bio_memory_engine.py` | 118 | L1 경로 (`self.l1_path`) |
| `modules/deriver_layer.py` | 187 | L1 경로 (`self.l1_path`) |

## 🗺️ 개발 로드맵 (진행 중)
*이 문서는 Hermes3 프로젝트의 현재 상태(v9.2 완료 + Phase 1·2 구현)와 향후 로드맵(v9.4+)을 명확히 보여줍니다. 앞으로도 경량·Stateless 원칙을 유지하며 진행해 나가겠습니다.*
- [ ] **Gateway api_server 플랫폼 활성화 문제 진단 및 수정** — WebUI가 Gateway 없이도 자체 provider 목록 표시하게 하거나, Gateway가 api_server를 띄우도록 수정
- [ ] **llama-server `-c 65536`으로 재시작** — 실제 context 확장 (메모리 사용량 확인 후, -ngl 99 유지 시 RAM 사용량 20~25GB 추정)
- [ ] **Qwen 추론 타임아웃 조정** — harness_agent.py `_call_local()` timeout 60s → 120s+ (35B A3B 첫 추론 시간 고려)
- [ ] **Telegram 모드 버튼 Gemma4→Qwen3.6 실제 적용 확인** — Telegram 접속 시 모드 전환 버튼 문구 확인 필요
- [ ] Qwen3.6 vs Gemma4 26B 성능/품질 비교 평가 (추론 속도, 응답 품질, context 활용도)
- [ ] hermtes-webui plist 정리 — 중복 실행 방지, HERMES_HOME 일원화 최종 확인
- [ ] hybrid_router.py `call_gemma4()` dead code 정리 (provider="gemma4" 문자열 → Qwen)

---
*이 파일은 /claude_brief 명령어로 자동 생성됩니다.*
*Claude 새 대화 시작 시 이 파일을 첨부하세요.*