# USER Profile (MJ님 지식 저장소)
이 파일은 MJ님(bluesea)에 대한 심층적인 정보를 저장하여, 에이전트가 개인 맞춤형 비서로서 동작하도록 돕습니다.

## 👤 기본 정보
- **호칭**: MJ님
- **직업/역할**: 법학 및 공학 융합 연구자, IT 자동화 전문가.
- **주요 워크스페이스**: Mac Studio (Main), Obsidian (`Mjobsidian`), Telegram.

## 🎯 선호도 및 스타일
- **커뮤니케이션**: 간결하고 정확한 결과 보고 선호. 리소스(토큰) 절약을 위해 불필요한 설명 지양.
- **기술 스택**: Python, Shell Scripts, Launchd, Docker, Local LLM 
- **관심사**: 맥 스튜디오 자동화, AI 에이전트 협업 시스템, 제2의 뇌(Second Brain) 구축.

## 🛠️ 상세 환경 및 기술 컨텍스트 (Environment)
- **OS**: macOS (Mac Studio)
- **Primary Paths**:
    - Vault: `/Users/bluesea/Applications/Mjobsidian`
    - Scripts: `/Users/bluesea/Applications/Mjauto/Scripts`
- **Preferred AI Stack**: llama.cpp (Gemma4 26B), NVIDIA NIM, Gemini.

## 🌟 개인적 선호 (Personal Preferences)
- **언어**: 한국어 중심 (영문 기술 용어 혼용 가능)
- **보고 형식**: "결론 -> 근거 -> 다음 단계" 순의 역피라미드 구조 선호.
- **자동화 철학**: "반복되는 일은 반드시 자동화한다."
- **업무 시간**: 주로 저녁~새벽 시간에 집중적인 연구 및 자동화 작업 수행.

## 🛑 AI 에이전트 필수 초기화 프로토콜 (Initialization Protocol)
- **최우선 행동 강령**: 어떤 AI 에이전트(WebUI, Telegram Bot 등)든 새 세션을 시작하거나 첫 지시를 받을 때, 사용자의 요구를 수행하기에 앞서 반드시 다음 두 파일을 `read_file` 또는 `view_file` 도구로 읽고 내용을 숙지해야 합니다.
  1. `/Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/constitution.local.md` (시스템 절대 규칙)
  2. `/Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/01_hot.md` (현재 진행 중인 프로젝트 경로 및 상태)
- 이 초기화 스캔 과정 없이는 파일 생성, 수정, 삭제 등의 물리적 시스템 조작을 절대 금지합니다.

---
*최종 업데이트: 2026-06-04 22:18 (에이전트 필수 초기화 프로토콜 추가)*
