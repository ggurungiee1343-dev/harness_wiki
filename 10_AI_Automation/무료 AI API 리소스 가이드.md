# 무료 AI API 리소스 가이드

## 요약
에이전트 개발 및 AI 활용 시 비용 부담 없이 사용할 수 있는 주요 클라우드 API 리소스 모음입니다. 하나의 서비스가 장애가 나거나 한도에 도달했을 때 즉시 교체하여 사용할 수 있도록 정리되었습니다.

## 🚀 추천 TOP 3
1. **Google Gemini:** 가장 스마트하고 다재다능함 (에이전트용 최적)
2. **Groq:** 압도적인 속도 (실시간 대화용 최적)
3. **OpenRouter:** 수십 개의 모델을 하나의 API로 교체 가능 (유연성 최적)

---

## 💎 주요 무료 리소스 목록 (9선)

### 1. OpenRouter (오픈라우터)
- **특징:** 약 29개의 완전 무료 모델 제공. 모델 자동 순환에 최적.
- **모델:** Gemma 2, Llama 3, Qwen 등
- **가입:** https://openrouter.ai/keys

### 2. Google Gemini API
- **특징:** 1M+ 컨텍스트, 멀티모달 능력이 가장 강력함.
- **모델:** Gemini 1.5 Pro / Flash 시리즈
- **가입:** https://aistudio.google.com/app/apikey

### 3. NVIDIA NIM
- **특징:** 최적화된 고성능 오픈 모델, 높은 RPM(40회/분).
- **모델:** Llama 3.3 70B, Qwen 235B 등
- **가입:** https://build.nvidia.com/explore/discover

### 4. Groq Cloud
- **특징:** 번개처럼 빠른 추론 속도. 실시간 에이전트에 필수.
- **모델:** Llama 3.3 70B, Qwen 32B 등
- **가입:** https://console.groq.com/keys

### 5. Cerebras Cloud
- **특징:** 대형 모델에 대한 매우 관대한 무료 한도.
- **가입:** https://cloud.cerebras.ai

### 6. Mistral La Plateforme
- **특징:** 코딩 및 다국어 작업에 강력함.
- **모델:** Mistral Large 3, Small 3.1 등
- **가입:** https://console.mistral.ai/api-keys

### 7. Cohere
- **특징:** 검색 증강 생성(RAG) 및 에이전트 작업에 특화.
- **가입:** https://dashboard.cohere.com/api-keys

### 8. GitHub Models
- **특징:** GitHub 계정으로 즉시 사용 가능, 안정적인 성능.
- **가입:** https://github.com/marketplace/models

### 9. Cloudflare Workers AI
- **특징:** 가볍고 견고한 에이전트 구축용.
- **가입:** https://dash.cloudflare.com/profile/api-tokens

---

## 💡 개발자를 위한 팁
- **호환성:** 대부분 OpenAI SDK와 호환되므로 `base_url`과 `api_key`만 바꾸면 바로 교체 사용 가능합니다.
- **전략:** Gemini를 메인으로 쓰고, 속도가 필요하면 Groq, 모델 테스트는 OpenRouter를 활용하세요.

---
*최종 업데이트: 2026-05-05 01:55*
