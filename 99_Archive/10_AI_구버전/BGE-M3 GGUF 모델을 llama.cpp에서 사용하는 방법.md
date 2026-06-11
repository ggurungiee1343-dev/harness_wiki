---
tags: [ingested, 인공지능/머신러닝]
date: 1778786675.183
---

Using BGE-M3 GGUF in llama.cpp
llama.cpp supports the GGUF backend directly, allowing you to run embedding models on macOS.

Reddit
·r/LocalLLaMA
 +3
Search: On Hugging Face, search for lm-kit/bge-m3-gguf or bge-m3-gguf in the model repository.
Download: Select the GGUF version (e.g., Q4_K_M or Q8_0) suitable for your system.
Run: Use llama-server with the `--embedding` flag to load the model for embedding tasks, or use the embedding endpoint at `http://localhost:8080/v1/embeddings`.

Alternatives
MLX format: If you prefer the MLX format for Apple Silicon, models like mlx-community/bge-m3-mlx-4bit are available via mlx-lm.
Rerankers: bge-reranker-v2-m3 is also available for improving search results.

Hugging Face
 +1
Note: The GGUF version via llama.cpp is the recommended approach for the current system setup.

Reddit
·r/LocalLLaMA
 +3

---
*최종 업데이트: 2026-06-03 19:10 — 누락 타임스탬프 자동 복구*
