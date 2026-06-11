# Llama Server Launchd 트러블슈팅 및 해결 보고서

**날짜:** 2026-05-21
**대상:** `com.bluesea.llama_server.plist` (macOS LaunchAgent)

## 📌 증상
`llama-server` (Gemma-4-26B 모델 구동용)의 자동 실행을 위해 작성한 `~/Library/LaunchAgents/com.bluesea.llama_server.plist` 파일을 `launchctl bootstrap gui/$(id -u)` 로 로드하려 할 때 지속적으로 다음 에러 발생:
```text
Bootstrap failed: 5: Input/output error
```

## 🔍 원인 분석 및 배제 과정
1. **플리스트 문법 검사:** `plutil -lint` 결과 정상(OK).
2. **파일 소유권 및 권한:** `chmod 644` 및 `chown bluesea:staff` 모두 정상 적용 확인.
3. **바이너리 파일 정상 동작 여부:** 터미널에서 바이너리를 직접 실행(`llama-server -m ...`)했을 때는 포트 8080에서 정상적으로 작동함을 확인.
4. **macOS Quarantine 및 Provenance 속성:**
    - 플리스트 파일과 실행 바이너리에 붙어 있는 확장 속성 (`com.apple.provenance`, `com.apple.quarantine`)이 launchd에서 실행을 차단할 수 있다고 가정함.
    - `xattr -c`로 삭제를 시도했으나, 시스템에 의해 `com.apple.provenance`가 계속 자동 재생성되는 현상 발견.
5. **단순화된 테스트 (Simple Plist):**
    - `-c 65536` 등 옵션을 다 빼고 가장 기본적인 옵션(`--port 8080 --host 127.0.0.1`)만 넣은 새 플리스트 `com.bluesea.llama_server_simple.plist`를 생성해 로드해본 결과 **성공**함.
    - 이에 따라, 에러의 근본 원인은 파일 권한이나 `xattr` 속성이 아님이 판명됨.

## 🎯 근본 원인 및 최종 해결
- **원인:** macOS `launchd` 시스템의 내부 캐시 데이터베이스에서 기존 Label인 `com.bluesea.llama_server`가 오염/블로킹된 상태로 꼬여 있었습니다.
- **해결 방안:** 플리스트의 내부 `<key>Label</key>` 값을 **`com.bluesea.llama_server2`** 로 새로 변경하고 적용했습니다. 또한 심볼릭 링크 대신 실제 바이너리 절대 경로를 명시했습니다.
- **결과:** Label 변경 직후 `launchctl bootstrap`이 성공(SUCCESS)하였으며, `llama-server`가 백그라운드 프로세스(PID 할당)로 정상 구동되어 모델을 로드하고 `http://127.0.0.1:8080/health` 에 올바르게 응답하는 것을 확인했습니다.

## 🛠 현재 상태
- **서비스명:** `com.bluesea.llama_server2`
- **로그 경로:** `~/.hermes/llama_server_stdout.log`, `~/.hermes/llama_server_stderr.log`
- **서버 주소:** `http://127.0.0.1:8080`
- 백그라운드에서 LaunchAgent를 통해 macOS 로그인 시 자동 구동되며, Hermes 등 다른 로컬 애플리케이션에서 즉시 호출 가능합니다.

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
