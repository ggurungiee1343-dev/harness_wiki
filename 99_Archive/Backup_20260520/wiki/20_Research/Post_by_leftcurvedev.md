---
title: "Post by @leftcurvedev_ on X"
source: "https://x.com/leftcurvedev_/status/2052812387955151062"
author:
  - "[[@leftcurvedev_]]"
published: 2026-05-08
created: 2026-05-10
description: "8GB 또는 12GB VRAM 설정을 사용하는 모든 사람은 llama.cpp에서 성능을 향상시키는 핵심 플래그가 \"-ncmoe\"라는 점을 이해해야 합니다. Qwen3.6 35B A3B에 대한 제 결과입니다. 8GB RTX 3070Ti에서 64k q8"
tags:
  - "clippings"
aliases: [Post by @leftcurvedev_ on X 1]
---
8GB 또는 12GB VRAM 설정을 사용하는 모든 사람은 llama.cpp에서 성능을 향상시키는 핵심 플래그가 "-ncmoe"라는 점을 이해해야 합니다.

Qwen3.6 35B A3B에 대한 제 결과입니다. 8GB RTX 3070Ti에서 64k q8\_0 컨텍스트로:

⚪️ 플래그 없음 → 8.7 tok/s

RAM: 13.6GB & VRAM: 7.8GB

🔴 -ncmoe 35 → 27.5 tok/s

RAM: 12.1GB & VRAM: 4.3GB

🟢 -ncmoe 30 → 32.5 tok/s

RAM: 12GB & VRAM: 5.6GB

🔵 -ncmoe 25 → 40.9 tok/s

RAM: 12GB & VRAM: 6.9GB

여기서 보이는 RAM과 VRAM 사용량은 모델이 실행 중인 Windows PC의 총 사용량임을 유의하세요. 제 친구의 설정: 8GB VRAM과 16GB RAM. Linux로 전환하면 성능을 향상시킬 수 있습니다. 그냥 염두에 두세요.

기본적으로, 이 플래그는 MoE 전문가들을 처음 X 레이어에 CPU + RAM에 유지하여 VRAM을 즉시 모두 소모하는 대신 처리합니다. 이는 OOM 없이 더 큰 모델을 실행할 수 있게 해주면서 나머지는 GPU에 유지하여 속도를 내는 스마트한 하이브리드 오프로드 방식입니다.

데이터에서 보듯이, 최적의 지점이 있습니다. 35에서 25로 낮추면 속도가 +50% 증가하는데, 이는 GPU에 더 많은 레이어가 올라가기 때문입니다 (VRAM 사용량을 보세요). 핵심은 숫자를 실험하며 VRAM에 최대한 맞추는 것이고, 스트레스를 피하기 위해 1GB/800MB 여유 공간을 목표로 하세요.

↓ 서버 플래그는 아래

> **left curve dev @leftcurvedev\_** · 2026-05-08
> 
> 오늘 저는 RTX 3070 Ti로 약간의 테스트를 해보고 있습니다. 8GB VRAM에 얼마나 많은 것을 담을 수 있는지 확인해보죠. 이걸 두 부분으로 나눠보겠습니다:
> 
> 1) 기본 llama.cpp에서 최대 속도를 위한 -ncmoe 매개변수의 적정점을 찾기
> 
> 2) Turboquant, DFlash 및 MTP 통합을 시도하여 더 많은 x.com/leftcurvedev_/…