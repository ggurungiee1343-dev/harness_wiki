# 🕸️ Graphify 사용 가이드

Graphify는 옵시디언 플러그인이 아닌, 맥(Mac) 시스템에 설치된 **독립적인 터미널 전용 AI 지식망 추출 도구(CLI)**입니다. 

이 도구는 지정한 폴더 내의 마크다운 파일(위키 문서)을 스캔하고 LLM(Gemini, Claude 등)을 활용해 문서 간의 숨겨진 맥락과 연결 고리를 분석하여 전체적인 **지식 그래프(Semantic Graph)**를 구축합니다.

---

## 1. 헤르메스 봇과의 연동 구조

헤르메스 봇 내부의 `wiki_manager.py` 스크립트는 답변을 생성할 때 이 Graphify가 만들어둔 **지식망 리포트**를 참조하여 보다 입체적인 답변을 제공합니다.

- **봇이 참조하는 파일 경로**: `/Users/bluesea/Applications/Mjobsidian/graphify-out/GRAPH_REPORT.md`
- **문제점**: 이 파일은 저절로 생성되지 않으며, 터미널에서 Graphify 추출 명령을 주기적으로 돌려주어야 최신화됩니다. 파일이 없으면 봇은 지식망 정보 없이 기본 검색(RAG)에만 의존하게 됩니다.

---

## 2. Graphify 지식망 구축 방법 (Update vs Extract)

상황에 맞게 두 가지 명령어 중 하나를 선택하여 사용할 수 있습니다.

### ⚡ 방법 A: 빠른 구조 추출 (API 키 불필요)
마크다운 파일들의 제목, 태그, 내부 링크 구조(AST)만 1초 만에 빠르게 읽어서 지식망을 만드는 방식입니다. 
AI 요약은 빠지지만, `wiki_manager.py`가 리포트를 참조하기에는 충분합니다.
```bash
graphify update /Users/bluesea/Applications/Mjobsidian
```
- **장점**: API 키가 필요 없고, 수 초 내에 즉시 `GRAPH_REPORT.md`가 생성됩니다.
- **언제 쓰나요?**: 평소 위키 문서들을 대량으로 이관(Ingest)한 직후 빠르게 지식망을 동기화할 때.

### 🧠 방법 B: 심층 의미 추출 (API 키 필수)
문서의 의미(Semantic)를 AI가 깊게 읽고 요약하여 더욱 입체적인 지식망을 구축하는 풀(Full) 추출 방식입니다.
```bash
export GEMINI_API_KEY="실제_구글_API_키"
graphify extract /Users/bluesea/Applications/Mjobsidian --backend gemini
```
- **특이사항**: Graphify 내부 구조상 로컬 LLM(llama.cpp 등)을 지원하지 않으므로, 반드시 공식 구글 Gemini, OpenAI, Claude 중 하나의 진짜 API 키를 주입해야 작동합니다.
- **언제 쓰나요?**: 문서가 크게 개편되었거나, 시간적 여유가 있을 때 AI에게 더 정밀한 지식 연결망 구축을 맡기고 싶을 때.

---

## 3. 유용한 Graphify 추가 명령어들

옵시디언 내의 지식들을 터미널 환경에서 다룰 때 유용한 명령어들입니다.

### 🔄 지식망 강제 업데이트 (Update)
문서를 대량으로 이동/삭제했을 때, 기존 캐시를 무시하고 뼈대를 재구축합니다.
```bash
graphify update /Users/bluesea/Applications/Mjobsidian --force
```

### ❓ 터미널에서 지식망에 직접 질문하기 (Query)
봇을 통하지 않고 Graphify 자체 엔진을 통해 질문할 수 있습니다.
```bash
graphify query "에이전트 메모리 시스템 설계에 대해 요약해줘" --graph /Users/bluesea/Applications/Mjobsidian/graphify-out/graph.json
```

### 🌳 시각화 리포트 생성 (Tree)
현재 지식망 구조를 웹 브라우저에서 볼 수 있는 상호작용형 HTML D3 트리맵으로 뽑아냅니다.
```bash
graphify tree --root /Users/bluesea/Applications/Mjobsidian --output /Users/bluesea/Applications/Mjobsidian/graphify-out/GRAPH_TREE.html
```

---

## 4. 요약 및 권장 사항

Graphify는 강력한 도구지만 백그라운드에서 자동으로 도는 것이 아니라 수동(CLI) 트리거가 필요합니다.
새로운 위키 문서(`Clippings` 등)를 대량으로 Ingest(이관)한 날에는, 잠들기 전이나 여유 시간에 **`graphify update`** 명령어를 한 번씩 돌려주시는 것을 권장합니다. (굳이 매번 무거운 `extract`를 돌릴 필요는 없습니다.)

---
*최종 업데이트: 2026-05-20 08:02*
*작성자: Antigravity AI*
