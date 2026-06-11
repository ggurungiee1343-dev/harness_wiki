---
title: "Claude × Obsidian에서 \"멋지게 자라는 두 번째 두뇌\"를 구축하는 모든 절차"
source: "https://x.com/obsidianstudio9/status/2045856830191243473"
author:
  - "[[@obsidianstudio9]]"
published: 2026-04-19
created: 2026-05-05
description: "\"메모는 많이 모이는데 결국 어디에 무엇을 썼는지 모른다\"「링크를 붙이는 것이 귀찮아, 노트끼리가 엉망인 채」「Obsidian을 사용하고 있는데, 그냥 메모장이 되고 있다」\"AI를 활용하고 싶지만 매번 컨텍스트를 처음부터 설명하는 것이 번거로움\"이런 ..."
tags:
  - "clippings"
aliases: [Claude_Obsidian_세컨드_브레인_구축]
---
![이미지](https://pbs.twimg.com/media/HGP0vVHakAA_CGS?format=jpg&name=large)

"메모는 많이 모이는데 결국 어디에 무엇을 썼는지 모른다"

「링크를 붙이는 것이 귀찮아, 노트끼리가 엉망인 채」

「Obsidian을 사용하고 있는데, 그냥 메모장이 되고 있다」

"AI를 활용하고 싶지만 매번 컨텍스트를 처음부터 설명하는 것이 번거로움"

![이미지](https://pbs.twimg.com/media/HGRTzTIbwAEzTy_?format=jpg&name=large)

이런 고민, 없습니까?

해외에서[@defileo](https://x.com/@defileo)씨가 투고한 「Claude + Obsidian | How to use your second brain」이라는 해설이 99만뷰를 넘는 큰 버즈중 😳

![이미지](https://pbs.twimg.com/media/HGRKiDpbsAAhMK6?format=jpg&name=large)

Obsidian × Claude Code로 「멋대로 자라는 제 2의 뇌」를 구축하는 방법을, 스텝 바이 스텝으로 해설한 내용입니다.

이번에는 그 내용을 철저히 씹어 일본어로 해설하겠습니다 👇

전 포스트는 이쪽：[https://x.com/defileo/status/2043762213597397179](https://x.com/defileo/status/2043762213597397179)

■ 𝗰𝗹𝗮𝘂𝗱𝗲-𝗼𝗯𝘀𝗶𝗱𝗶𝗮𝗻이란 무엇인가?

![이미지](https://pbs.twimg.com/media/HGRS9McaQAAgf5F?format=jpg&name=large)

claude-obsidian은 GitHub에 공개된 오픈 소스 Claude Code 플러그인입니다(MIT License, GitHub: AgriciDaniel/claude-obsidian, 1.9k 스타).

Andrej Karpathy씨(OpenAI 창설 멤버, 전 Tesla AI 부문 디렉터)가 제창한 「LLM Wiki」패턴을 실장한 것으로, 한마디로 말하면 「지식이 복리로 늘어나는 Obsidian Vault」를 만드는 툴입니다.

기존의 AI × 노트 도구의 문제점은 매번 세션이 끊어지면 컨텍스트가 재설정된다는 것입니다. claude-obsidian은 이 문제를 근본적으로 해결합니다.

소스를 던지면, Claude가 그것을 읽어들여, 엔티티와 개념을 추출해, 상호 참조를 갱신해, 구조화된 Obsidian Vault에 자동적으로 파일링한다. 하나의 기사를 넣으면 8-15개의 상호 링크된 위키 페이지가 생성됩니다.

즉, 사용하면 사용할수록 Vault가 현명해진다. 지식이 「복리」로 쌓아 가는 구조입니다.

![이미지](https://pbs.twimg.com/media/HGRWzuraMAAxWfb?format=jpg&name=large)

■ 𝗰𝗹𝗮𝘂𝗱𝗲-𝗼𝗯𝘀𝗶𝗱𝗶𝗮𝗻 시작하는 방법

![이미지](https://pbs.twimg.com/media/HGRTnFlboAAaV8t?format=jpg&name=large)

필요한 것:

・Obsidian(데스크탑판)

• Node.js 버전 18 이상

· Claude Code (CLI 또는 데스크톱 앱)

설치에는 세 가지 방법이 있습니다.

![이미지](https://pbs.twimg.com/media/HGRWrfKaUAEr5ko?format=jpg&name=large)

【방법 1】Vault Clone(권장·2분에 완료)

\`\`\`

git clone[https://github.com/AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)

cd 클로드-옵시디언

bash bin/setup-vault.sh

\`\`\`

복제된 폴더를 Obsidian에서 열기만 하면 됩니다. 이것은 가장 간단합니다.

【방법 2】클라우드 코드 플러그인으로 추가

\`\`\`

클로드 플러그인 마켓플레이스에 AgriciDaniel/claude-obsidian을 추가하세요

클로드 플러그인 설치 claude-obsidian@claude-obsidian-marketplace

\`\`\`

【방법 3】 기존 Vault에 도입

GitHub 리포지토리에서 \`WIKI.md\`를 복사하여 자신의 Vault에 넣고 Claude에게 설정을 지시합니다.

어떠한 방법에서도, 최초로 \`/wiki\` 명령을 실행하면 Vault의 기본 구조가 스캐폴드 됩니다.

■ /𝘄𝗶𝗸𝗶 커맨드── Vault의 골격을 일발 구축

![이미지](https://pbs.twimg.com/media/HGRVnpUbcAAu82X?format=jpg&name=large)

\`/wiki\` 는 최초로 실행하는 커멘드입니다.

이것을 치면 Claude는 다음 구조를 자동으로 생성합니다.

· \`wiki/index.md\` — 마스터 카탈로그 (모든 페이지의 목차)

· \`wiki/hot.md\` — 핫 캐시 (최근 컨텍스트 유지)

· 도메인별 하위 색인

·\`.raw/\` 폴더 — 가져온 원문의 보관 장소

특히 중요한 것이 \`hot.md\`와 \`index.md\`의 2 파일.

![이미지](https://pbs.twimg.com/media/HGRVujebwAAz9Vu?format=jpg&name=large)

\`hot.md\` (은)는 세션간의 문맥을 자동으로 보관 유지하는 파일입니다. 통상의 AI 채팅에서는 대화가 끊어지면 전부 잊습니다만, claude-obsidian에서는 \`hot.md\`에 최근의 작업 내용이 자동 캐쉬되기 때문에, 다음의 세션에서도 「아까의 계속」부터 시작됩니다.

\`index.md\`는 Vault 전체의 마스터 카탈로그입니다. Claude는 먼저이 파일을 읽고 어떤 페이지에 무엇이 쓰여 있는지 파악합니다. 모든 페이지를 매번 로드하는 대신 인덱스에서 필요한 페이지만 선택적으로 로드하므로 토큰 비용을 크게 절약할 수 있습니다.

■ 𝟯코어 커맨드── /𝘀𝗮𝘃𝗲 /𝗮𝘂𝘁𝗼𝗿𝗲𝘀𝗲𝗮𝗿𝗰𝗵 /𝗰𝗮𝗻𝘃

![이미지](https://pbs.twimg.com/media/HGRWCzTaUAA1Hbs?format=jpg&name=large)

claude-obsidian의 일상적인 조작은 주로 세 가지 명령으로 돌아갑니다.

【/save】 대화를 위키 노트로 변환

![이미지](https://pbs.twimg.com/media/HGRVYXabkAEnvTc?format=jpg&name=large)

Claude와의 대화에서 가치있는 정보가 나오면 \`/save\`를 치는 것만. Claude는 전체 대화를 읽고, 키 아이디어를 추출하고, 잘 포맷된 Wiki 페이지를 작성하고, 기존 페이지에 대한 Wikilink를 자동 생성하고, index.md를 업데이트합니다.

\`/save 프롬프트 엔지니어링\`과 같이 이름을 지정할 수도 있습니다.

【/autoresearch】자율 리서치 루프

![이미지](https://pbs.twimg.com/media/HGRVc-WaUAAOWeE?format=jpg&name=large)

\`/autoresearch \[topic\]\`을 실행하면 Claude는 해당 주제에 대해 자율적으로 연구하고 결과를 위키 페이지로 볼트에 축적합니다.

예를 들어 \`/autoresearch RAG 최신 방법\`이라고 치면, RAG에 대한 지식이 Vault에 체계적으로 추가되어 갑니다.

【/canvas】 비주얼 지식지도

![이미지](https://pbs.twimg.com/media/HGRVh8absAAN-Zj?format=jpg&name=large)

Obsidian의 캔버스 기능과 협력하여 지식을 시각적으로 매핑합니다. 12개의 비주얼 템플릿과 6개의 레이아웃 알고리즘이 제공되어 프레젠테이션, 플로우차트, 지식 그래프 등을 자동으로 생성할 수 있습니다.

■ 매일 인제스트 루프── .𝗿𝗮𝘄/ 폴더 사용법

![이미지](https://pbs.twimg.com/media/HGRUbJ8bEAARh3k?format=jpg&name=large)

claude-obsidian의 진가는 "일상적인 정보 캡처"에 있습니다.

방법은 간단합니다 :

1\. 신경이 쓰인 기사, 논문, 메모를 \`.raw/\` 폴더에 넣기

2\. \`ingest \[파일 이름\]\`명령 실행

3\. Claude가 자동으로 로드, 요약, 개념을 추출하고 기존 Wiki 페이지와 상호 링크

복수 파일을 일괄 처리하고 싶은 경우는 \`ingest all of these\` 로 일괄 캡처가 가능. 이 때 파일 간의 상호 참조도 자동으로 생성됩니다.

보다 편리한 것이 \`lint the wiki\` 명령. 이것은 Vault 전체의 상태 확인을 수행하고 다음을 감지합니다.

・깨진 링크(데드 링크)

· 고립된 페이지(어디에서나 링크되지 않은 노트)

・지식의 갭

· 오래된 기술

![이미지](https://pbs.twimg.com/media/HGRUl50acAA1Yep?format=jpg&name=large)

즉, Vault의 "유지 보수"까지 AI가 자동으로 해주는 것입니다.

■ 비용 효율적인 설계 - 왜 토큰을 낭비하지 않는지

![이미지](https://pbs.twimg.com/media/HGRWKCibsAA6S6Z?format=jpg&name=large)

"AI × 노트 도구"로 많은 사람들이 걱정하는 것이 API 비용입니다.

claude-obsidian은 여기도 능숙하게 설계되었습니다.

작동 방식은 3가지:

·\`hot.md\` — 최근의 문맥만을 캐쉬해, 매회 전체 히스토리를 읽지 않는다

· \`index.md\` — 마스터 카탈로그에서 필요한 페이지 만 선택적으로로드

· 도메인별 하위 색인 - 관련 영역의 페이지에만 액세스 제한

예를 들어 프로그래밍에 대해 질문하면 Claude는 index.md를보고 "programming"관련 하위 인덱스 만 읽고 거기에서 더 필요한 페이지 만 엽니 다. Vault 전체가 1000페이지라도 실제로 로드하는 것은 10~20페이지 정도로 끝납니다.

![이미지](https://pbs.twimg.com/media/HGRWOSVaUAAlaFp?format=jpg&name=large)

이에 따라 Vault가 거대화해도 토큰 비용이 선형으로 증가하지 않는 설계가 되었습니다.

■ 𝟭개월 후의 그래프 뷰── 지식이 「보이는」순간

![이미지](https://pbs.twimg.com/media/HGRU1fAbYAEMJLk?format=jpg&name=large)

[@defileo](https://x.com/@defileo)씨의 투고에서 가장 반향이 있었던 것이, 1개월간 운용한 후의 Obsidian 그래프 뷰의 스크린 샷입니다.

노드 (개념)가 색으로 구분되어 각각이 서로 링크로 연결되어 있습니다. 수동으로 절대로 만들 수없는 밀도가 높은 지식 그래프가 자동으로 형성됩니다.

이것이 "지식이 복리로 증가한다"의 의미입니다.

처음 1주일은 페이지수도 적고, 링크도 드문드문. 하지만 2주, 3주간 계속되면서 새롭게 넣은 정보가 기존 지식과 자동적으로 연결되어 네트워크 효과가 가속된다. 4주째에는 「자신이 무엇을 알고 있는가」가 그래프로 일망할 수 있는 상태가 됩니다.

■ 실제 활용 장면

![이미지](https://pbs.twimg.com/media/HGRU-CgbgAAiVS3?format=jpg&name=large)

claude-obsidian은 다음과 같은 장면에서 특히 위력을 발휘합니다.

· 논문과 기술 기사를 일상적으로 읽는 연구자 · 엔지니어

→ 읽은 내용이 자동으로 체계화되어 나중에 「그 논문의 그 개념」을 바로 당길 수 있다

· 여러 프로젝트를 병렬로 진행하는 관리자

→ 프로젝트 간의 지식이 교차 참조되고 의사 결정의 질이 향상됩니다.

· 학습중인 주제를 깊이 파고 싶은 사람

→ /autoresearch에서 자율적으로 리서치, 지식의 구멍을 자동 검출

・Obsidian을 사용하고 있지만 「메모가 흩어지는 문제」를 안고 있는 사람

→ AI가 자동으로 링크를 하고 정리해 주기 때문에 수동 유지보수가 불필요하게

중요한 것은, 이것이 Obsidian의 로컬 파일(Markdown)로 움직이고 있는 점. 모든 데이터는 자신의 컴퓨터에 남아 있으며 클라우드에 의존하지 않습니다.

![이미지](https://pbs.twimg.com/media/HGRWWqgbcAABT8Q?format=jpg&name=large)

■ 멀티 모델 대응── Claude 이외에서도 움직인다

claude-obsidian이라는 이름이지만 사실은 Claude 이외의 모델에서도 작동합니다.

대응 모델:

・Claude(권장)

・쌍둥이자리

·사본

·커서

윈드서핑

프로바이더에 묶이지 않는 설계 때문에, 장래에 모델을 바꾸어도 축적한 지식은 그대로 사용할 수 있습니다.

■ 정리── 「메모를 모으는 것만」을 졸업한다

![이미지](https://pbs.twimg.com/media/HGRVK3ZakAAeaY0?format=jpg&name=large)

claude-obsidian이 해결하는 문제는 분명합니다.

전통적인 Obsidian 운영:

메모 쓰기 → 링크를 수동으로 붙이기 → 번거롭게 계속되지 않는다 → 노트가 흩어진다 → 결국 검색 요청

claude-obsidian 도입 후 :

소스를 .raw/ 에 넣는다 → ingest한다 → 자동으로 Wiki 페이지 생성·상호 링크·인덱스 갱신 → 사용할수록 현명해지는 Vault가 자랍니다

게다가 오픈 소스(MIT License)로 무료. GitHub 스타 1.9k에서 알 수 있듯이 해외 Obsidian 커뮤니티에서는 이미 클래식 도구가되고 있습니다.

AI 세컨드 뇌를 시작하고 싶다면 가장 장애물이 낮고 가장 큰 수익률이 가장 큰 옵션 중 하나입니다.

지금 시도하는 단계:

![이미지](https://pbs.twimg.com/media/HGRWiJibYAE-fXb?format=jpg&name=large)

1.[https://github.com/AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)복제

2\. \`bash bin/setup-vault.sh\` 실행

3\. Obsidian에서 폴더 열기

4\. \`/wiki\`로 Vault 초기화

5\. 좋아하는 기사를 \`.raw/\` 에 넣어 \`ingest\` 한다

5분 안에 시작됩니다.

어땠어?

기사를 쓰는 동안 스스로도 이렇게 하면, 잘 돌릴 수 있고 코스트도 삭감할 수 있을까 엄청 공부가 되었습니다.

자동화 레벨까지 운용을 다루는 것은 어렵지만, 극한 사람을 참고로 할 수 있기 때문에 점점 배워 가고 싶습니다!

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
