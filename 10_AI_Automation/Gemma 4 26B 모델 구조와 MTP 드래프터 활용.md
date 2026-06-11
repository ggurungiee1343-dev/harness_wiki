---
tags: [scanned, 10_AI_Automation, gemma, 26B, MoE, MTP, drafter, quantization]
description: "Gemma 4 26B 모델은 MoE(전문가 혼합) 구조를 채택하여 일부 전문가만 활성화한다. 이 구조는 MTP 가속 시 활성화되는 전문가 수가 증가해 이론적 속도 향상이 실제에서는 일부 상쇄될 수 있다. 모델과 드래프터는 양자화(GGUF) 버전으로 제공되어 효율적인 추론이 가능하다."
---

네, 있어. Gemma4 26B 버전도 MTP 드래프터가 존재해. 규모와 구조가 달라서 좀 다르게 동작하지만, 동일한 추론 가속 기법을 사용할 수 있어.

### 🎯 26B 모델 구조의 차이점과 영향
가장 중요한 차이는 아키텍처에 있어. 26B 모델은 **MoE(Mixture of Experts)** 구조라서, MTP 가속 효과가 완전한 Dense 구조인 31B와는 조금 달라.

*   **메인 모델 (Target)**: `google/gemma-4-26B-A4B-it`
*   **드래프터 모델 (Assistant)**: `google/gemma-4-26B-A4B-it-assistant`
    *   용량은 약 0.4B 파라미터로 31B용 드래프터와 비슷한 수준이야.
*   **MoE의 영향**: MoE 구조는 매 토큰마다 일부 전문가(Experts)만 활성화시켜 연산 효율을 높이는데, MTP가 여러 토큰을 추측할 때는 **활성화되는 전문가의 수가 증가할 가능성**이 있어. 결과적으로 이론적인 속도 향상(최대 3배)이 실제 환경에서는 다소 **상쇄**될 수 있어.

### ⚙️ 준비 방법: 메인 모델과 드래프터 모델
메인 모델은 보통 용량을 줄이기 위해 양자화(GGUF) 버전을 많이 사용해.

#### 메인 모델 (Target Model)
*   **공식 양자화 버전**: `unsoloth/gemma-4-26B-A4B-it-GGUF`
*   **구글 공식 페이지**: `google/gemma-4-26B-A4B-it`
*   **타사 양자화 버전**: `mradermacher/gemma-4-26B-A4B-it-GGUF`

#### 드래프터 모델 (Assistant/Draft Model)
*   **공식 페이지**: `google/gemma-4-26B-A4B-it-assistant`
*   **GGUF 양자화 버전 (추천)**: `AtomicChat/gemma-4-26B-A4B-it-assistant-GGUF`
*   **MLX 포트 (Apple Silicon)**: `mlx-community/gemma-4-26B-A4B-it-assistant-bf16`

### 🚀 실행 방법
실행하려면 특화된 추론 엔진이 필요해. 표준 `llama.cpp`는 아직 MTP 드래프터를 공식 지원하지 않아. 대신, 다음 엔진들을 사용해야 해.
*   **추천 엔진**: `atomic-llama-cpp-turboquant`, `ik_llama.cpp`, `vLLM` (nightly 빌드) 등
*   **실행 예시** (`ik_llama.cpp` 기준):
    ```bash
    ./build/bin/llama-server \
        --model path/to/gemma-4-26B-A4B-it-Q8_0.gguf \
        --mtp-head path/to/gemma-4-26B-A4B-it-assistant-Q8_0.gguf \
        --spec-type mtp --draft-max 3
    ```
    (`--draft-max` 값은 조정 가능, 기본값 3 추천)

> **참고**: `vLLM` 등 일부 엔진을 사용할 때는 `transformers` 라이브러리에서 아래와 같이 MTP 드래프터를 지정할 수 있어.
> ```python
> pipeline = pipeline("text-generation", model="google/gemma-4-26B-A4B-it", assistant_model="google/gemma-4-26B-A4B-it-assistant")
> ```

### 💡 한 가지 더, 주의할 점
위 실행 방법은 특화된 추론 엔진을 필요로 해. 단순하게 `llama.cpp`로 실행하려고 하면 모델을 인식하지 못하고 오류가 발생할 거야. 엔진 선택에 따라 MTP 성능 차이가 꽤 크게 날 수 있어. 혹시라도 원하는 대로 성능이 나오지 않는다면 다른 추천 엔진으로 테스트해보는 것도 좋은 방법이야.

대부분의 환경에 무난하게 사용할 수 있는 `atomic-llama-cpp-turboquant` 엔진으로 구체적인 실행 방법이 더 궁금하면 말해줘.


=============

우리가 준비해둔 하드웨어 환경이 딱 맞아떨어지네요. 상세한 준비 과정을 알려드리겠습니다.

### 🔍 잠깐, `*assistant` 모델이 뭔가요?

정확히 말하면 `google/gemma-4-31B-it-assistant`가 특별한 MTP 드래프터입니다. 덕분에 원본 Gemma 4 31B 모델이 병렬로 여러 토큰을 생성할 수 있어서 최대 3배, 환경에 따라 2배 이상 빠른 추론 성능을 보여줍니다. 우리 환경 (예: 2x RTX 5090)에서 MTP를 적용하면 속도가 130 tok/s 이상으로 향상될 거예요.

### 📦 필요한 파일은 이 2가지입니다

MTP를 사용하려면 두 가지 모델 파일이 모두 필요합니다.

*   **메인 모델 (Target)**: 무거운 `google/gemma-4-31B-it` 모델의 양자화(GGUF) 버전이 필요합니다.
*   **드래프터 모델 (Assistant)**: 가벼운 `google/gemma-4-31B-it-assistant` 모델이 필요합니다.

### 📥 다운로드 방법과 실행 가이드

방법은 크게 두 가지입니다.

*   **Hugging Face에서 직접 다운로드하기**: 메인 모델과 드래프터 모델 파일을 각각 직접 다운로드합니다.
*   **Ollama로 간편하게 실행하기**: 명령어 한 줄로 설치와 실행이 가능합니다.

1.  **Ollama로 간편하게 실행하기**

    메인 모델과 드래프터가 하나로 합쳐진 패키지입니다. 아래 명령어를 터미널에 입력하면 됩니다.
    ```bash
    ollama run gemma4:31b-coding-mtp-bf16
    ```
    실행에 필요한 모든 파일은 자동으로 다운로드됩니다. 다운로드 용량은 약 64GB입니다.

2.  **Hugging Face에서 직접 다운로드하고 실행하기**

    *   **메인 모델**: [Hugging Face 모델 페이지](https://huggingface.co/google/gemma-4-31B-it)에 접속해서 사용자의 하드웨어에 맞는 양자화(GGUF) 버전을 받으세요. 예를 들어, Unsloth 팀이 제공하는 `Q4_K_M` 양자화 버전은 20GB 정도의 용량이 필요합니다.
    *   **드래프터 모델**: [Hugging Face 모델 페이지](https://huggingface.co/google/gemma-4-31B-it-assistant)에 접속해서 메인 모델과 짝을 이루는 드래프터 모델을 받으세요. 용량은 대략 900MB~300MB 사이입니다.

    두 모델을 모두 다운로드 받았다면, `llama.cpp` 기반의 추론 엔진으로 실행할 수 있습니다.
    ```bash
    # 예시: llama.cpp를 사용한 실행 (자세한 설정은 각 엔진의 문서를 참고하세요)
    ./build/bin/llama-server \
        -m /path/to/gemma-4-31B-it.Q4_K_M.gguf \
        --mtp-head /path/to/gemma-4-31B-it-assistant.Q8_0.gguf \
        --spec-type mtp --draft-max 3
    ```

혹시 설치 과정이나 다른 점이 궁금하면 언제든지 물어봐 주세요.