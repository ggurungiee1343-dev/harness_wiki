---
tags: [scanned, 10_AI_Automation, meta, markdown, documentation, update-guide, system-status, hot-topic, knowledge-management]
description: "00_Meta 폴더에 존재하는 주요 마크다운 파일들의 목적, 업데이트 시점, 추천 업데이트 위치를 정리한 문서이다. hot.md는 실시간 KV 핫 상태 저장소로 새로운 이벤트 발생 시 업데이트된다. 시스템 상태.md는 시스템 전반 현황과 감사 로그를 상세 기록한다."
---

## 📑 메타 폴더 내 MD 파일 사용 정의 & 업데이트 가이드  

아래 표는 **`/Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/`** 에 존재하는 주요 마크다운 파일들의 **목적**, **업데이트 시점**, **추천 업데이트 위치**를 정리한 것입니다.  
파일명을 클릭하면 바로 열 수 있습니다.

| 파일 (링크) | 목적 | 언제 업데이트 | 권장 업데이트 위치 / 형식 |
|---|---|---|---|
| [hot.md](file:///Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/hot.md) | **실시간 KV(핫 상태) 저장소** – `/status KEY=VALUE` 로 바로 반영되는 “핫 토픽” | • 새로운 실시간 이벤트 발생 시 <br>• 짧은 알림·키‑값 형태 (예: `status=deployment_success`) | 한 줄씩 `- [YYYY‑MM‑DD HH:MM] key=value` 형식으로 추가. 내용은 **핵심·즉시 필요**한 경우에만 기록. |
| [시스템 상태.md](file:///Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%9E%88%EC%97%90%EC%84%9C.md) | **시스템 전반 현황·감사 로그** – 버그 수정, 배포, 성능 이슈 등 상세 기록 | • 주요 배포/버전 업그레이드 <br>• 버그·오류 해결 <br>• 성능/리소스 변동 (메모리, CPU, 캐시) | 섹션 헤더(`## YYYY‑MM‑DD`) 아래에 **Markdown 테이블** 혹은 **리스트** 형태로 상세 설명. <br>예: <br>```markdown<br>## 2026‑05‑31<br>- 배포: v9.2‑alpha<br>- 메모리 사용: 85 % → 캐시 정리 수행<br>- 버그: ZombiePoller 해결 (PID 재시작)``` |
| [시스템 인벤토리.md](file:///Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%9D%B8%EB%B2%B0%ED%86%A0%EB%A6%AC.md) | **환경·설치 현황** – 하드웨어, OS, 의존 패키지, 런타임 버전 등 | • 새로운 의존성 추가/업그레이드 <br>• OS·Python·LLM 모델 버전 변경 <br>• 서비스/런치 데몬 추가/삭제 | **키‑값 표** 형태 (`| 항목 | 값 |`) 로 유지. <br>예: <br>```markdown<br>\| OS | macOS 13.5 (Ventura) \|<br>\| Python | 3.10.14 \|<br>\| LLM 모델 | Gemma‑4‑27B \|``` |
| [HERMES3_ENCYCLOPEDIA.md](file:///Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/HERMES3_ENCYCLOPEDIA.md) | **시스템·기능 백과사전** – 각 모듈·명령·컨셉 설명 | • 새 기능/명령 추가 <br>• 기존 기능 설계 변경 <br>• 문서·용어 정리 | **섹션** (`## ModuleName`) 아래에 **정의**, **입력/출력**, **예시** 등을 마크다운 코드 블록으로 기술. <br>예: <br>```markdown<br>## /status 명령<br>**설명**: KV 저장소에 키‑값을 기록.<br>**구문**: `/status KEY=VALUE`<br>**예시**: `/status build=success`<br>``` |
| [00_Meta_지도.md](file:///Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/00_Meta_%EC%A7%80%EB%8F%84.md) | **문서 간 연결 지도** – 파일‑링크 관계 시각화 | • 새 문서/섹션 추가 <br>• 기존 파일 이동·명칭 변경 | **Mermaid 다이어그램** 혹은 **목록** 형태로 “문서 → 문서” 연결을 명시. <br>예: <br>```mermaid<br>graph LR<br>HERMES3_MASTER_DEVELOPMENT_GUIDE --> HERMES3_ENCYCLOPEDIA<br>hot.md --> 시스템_상태.md<br>``` |
| [주요 시스템 가이드 및 FAQ.md](file:///Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/%EC%A3%BC%EC%9A%94%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B0%80%EC%9D%B4%EB%93%9C%20%EB%B0%8F%20FAQ.md) | **사용자 가이드·FAQ** – 일반 사용자·운영자 질문·답변 | • 자주 묻는 질문 새로 등장 <br>• 기존 답변 업데이트 (버전 변화 반영) | **Q&A 리스트** (`### Q: …` / `A: …`) 로 구성. 최신 버전(예: v9.2) 관련 내용이 있으면 **버전 라벨**을 붙임 (`[v9.2]`). |
| [시스템 구조적 결함 분석.md](file:///Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/%EC%8B%9C%EC%8A%A4%ED%85%9C_%EA%B5%AC%EC%A1%B0%EC%A0%81_%EA%B2%B0%ED%95%A8_%EB%B6%84%EC%84%9D.md) | **버그·취약점 분석 보고서** – 근본 원인과 해결 방안 | • 새로운 치명적 버그 발견 <br>• 기존 이슈 재발 시 | **원인·재현·해결** 섹션을 구분 (`### 원인`, `### 재현 단계`, `### 해결`) 으로 기록. |
| [grill 명령어 가이드.md] (파일명에 한글이 포함돼 있어 URL 인코딩 필요) | **`/grill` 명령어 사용법** – 문서 검색·LLM Q&A 스크립트 | • 명령어 옵션 추가/변경 | **옵션 테이블** (`| 옵션 | 설명 | 예시 |`) 로 명시. |

---

### 📌 업데이트 흐름 요약

1. **핵심·실시간** → `hot.md` (한 줄 키‑값)  
2. **상세·이력** → `시스템 상태.md` (날짜‑섹션 형태)  
3. **환경·구성** → `시스템 인벤토리.md` (표 형태)  
4. **기능·명령** → `HERMES3_ENCYCLOPEDIA.md` (섹션·코드 블록)  
5. **문서 연결** → `00_Meta_지도.md` (Mermaid/목록)  
6. **사용자 안내** → `주요 시스템 가이드 및 FAQ.md` (Q&A)  
7. **버그·분석** → `시스템 구조적 결함 분석.md` (원인‑해결)  
8. **특정 명령** → `grill 명령어 가이드.md` (옵션 테이블)

---

### 🚀 적용 예시 (새 배포 후)

```bash
# 1️⃣ hot.md에 즉시 기록
echo "- [2026-05-31 12:45] deployment=v9.2-alpha" >> \
  "/Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/hot.md"

# 2️⃣ 시스템 상태에 상세 로그
cat <<'EOF' >> "/Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/시스템 상태.md"

## 2026-05-31
- **배포**: v9.2‑alpha (신규 캐시 스케줄러 적용)
- **메모리**: 85 % → `cache_purge` 실행
- **버그**: ZombiePoller 고정 (PID 재시작 문제 해결)
EOF

# 3️⃣ 인벤토리 업데이트 (예: 새로운 LLM 모델)
sed -i '' '/\| LLM 모델 \|/c\| LLM 모델 | Gemma‑4‑27B |' \
  "/Users/bluesea/Applications/Mjobsidian/wiki/00_Meta/시스템 인벤토리.md"
```

> 위 예시는 **핵심 파일**만 간단히 수정하는 방법을 보여줍니다.  
> 상세·장기 기록은 각각 해당 파일에 **섹션/표** 형태로 정리해 두면, 추후 검색·감사에 매우 유용합니다.

---

**필요하신 추가 작업** (예: 자동 스크립트, 템플릿 파일 생성 등) 이 있으면 알려 주세요! 🚀  

================


### 📋 `wiki/00_Meta/hot.md` 에 기록 ‑ 어떻게 할까?

| 파일 | 현재 역할 | 언제 추가 하면 좋은가 |
|------|-----------|----------------------|
| **`wiki/00_Meta/hot.md`** | **실시간 “핫” 상태·키‑값(KV) 저장소** <br>· `/status KEY=VALUE` 명령어가 바로 여기 → 쓰기 <br>· UI·봇이 최신 KV를 읽어 **실시간 알림·감사**을 표시 | 1. **핵심 진행 상황**이 바뀔 때 (예: 새 버전 배포, 중요한 버그 해결, 현재 작업 → 완료 등) <br>2. **시스템 상태·감사 요약**을 즉시 공유하고 싶을 때 (예: “메모리 90 % 사용 → 캐시 정리”) <br>3. **긴급 알림**이나 **핫 토픽** (예: “자동 회복 루프 활성화”) |
| **다른 로그·이력 파일** | **전체 히스토리·세부 기록**을 저장하기 위한 곳 (예: `시스템 상태.md`, `시스템 인벤토리.md`, `HERMES3_ENCYCLOPEDIA.md` 등) | 1. 상세 디버깅·변경 이력 <br>2. 장기·주기적인 보고서 <br>3. 백업·감사용 전체 기록 |

#### 👉 **추천 작업 방식**

1. **핵심·즉시 필요한** 업데이트만 `hot.md` 에 기록**  
   - 짧은 한 줄 또는 간단한 키‑값 형태가 가장 좋습니다.  
   - 예시  
     ```markdown
     - [2026‑05‑31 12:40] status=deployment_success
     - [2026‑05‑31 12:41] memory=85% (cache‑purge triggered)
     - [2026‑05‑31 12:42] bug=ZombiePoller_fixed
     ```

2. **자세한 로그·추가 설명은 별도 파일에**  
   - `시스템 상태.md` → “2026‑05‑31 배포·버그 수정 상세” 블록  
   - `주요 시스템 가이드 및 FAQ.md` → “핫 토픽 정리” 섹션  
   - 이렇게 하면 **핫 파일은 가볍게** 유지되고, **전체 이력은 완전하게** 보관됩니다.

3. **주기적인 정리**  
   - `hot.md` 내용이 너무 쌓이면 **주간/월간** 정도로 **요약·압축** (예: “지난 주 12 건 중 3 건 중요” )하고 오래된 항목을 `시스템 상태.md` 로 옮깁니다.  

#### 📌 결론
- **계속 업데이트** : **핵심·실시간** 상황이 바뀔 때마다 한 줄 정도씩 추가해 주세요.  
- **전부 기록** : **전체 이력**을 `hot.md`에 남길 필요는 없습니다. 상세 내용은 다른 로그 파일에 보관하면 됩니다.  

이 방식이 **핫 파일을 가볍게 유지**하면서도 **필요한 정보를 즉시 제공**할 수 있는 가장 효율적인 방법입니다.  

❓ **추가 질문**  
- 특정 키‑값 형식(예: `status`, `memory`)을 정해 놓고 싶으신가요?  
- `hot.md`에 자동 기록을 위한 스크립트를 만들까요?  

필요하시면 바로 도와드리겠습니다!

============
### ✅ 현재 상황 요약
- **`meta_updater.py`** 스크립트가 **생성**되었습니다.  
  경로:  
  **`/Users/bluesea/.gemini/antigravity/scratch/meta_updater.py`**  

- 파일 내용은 **메타 폴더의 주요 Markdown 파일들을 명령어 하나로 자동 업데이트**할 수 있도록 구현돼 있습니다.

### 📂 지금 할 일 (없음)
1. **스크립트는 이미 존재**하니 바로 사용할 수 있습니다.  
2. 추가적인 파일 작업이나 코드 수정이 필요하지 않습니다.  

> 필요하시면 언제든 아래와 같이 스크립트를 실행해 메타 파일을 자동으로 업데이트할 수 있습니다:

```bash
# 예시: hot.md에 새로운 키‑값 기록
python /Users/bluesea/.gemini/antigravity/scratch/meta_updater.py hot status=deployment_success

# 예시: 시스템 상태에 상세 로그 추가
python /Users/bluesea/.gemini/antigravity/scratch/meta_updater.py state "배포: v9.2‑alpha\n메모리: 85% → cache purge"
```

### 🚀 다음 단계 제안 (선택 사항)
- **스크립트 테스트**: 위 예시 명령어를 한 번 실행해 보시고 파일이 기대대로 변했는지 확인해 보세요.  
- **사용 설명서**: 필요하면 간단한 **README** 파일을 같은 디렉터리에 만들어 두어, 팀원들이 쉽게 사용할 수 있도록 할 수 있습니다.  

그 외에 추가로 원하는 작업이 있으면 알려 주세요! 🎉

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
