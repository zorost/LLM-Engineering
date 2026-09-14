# O1 · Serving engines

## Why it exists

A weights file is not a service. The engine is the process that turns
a prompt into tokens at a stated concurrency, with a tokenizer that
matches the card, and an HTTP contract other teams can call. Pick the
engine for the workload, not for the blog post you saw last week.

## The idea

Inference has two phases. **Prefill** reads the prompt and fills the KV
cache. It is relatively compute-heavy. **Decode** emits one token (or a
small block) at a time. It is often memory-bound: you reread a large
weight tensor for a small amount of math. Batching raises GPU
utilization in decode. Continuous batching lets new requests join a
running batch as others finish, instead of waiting for a static pack.

The KV cache is the other budget. It grows with sequence length, batch,
and the number of KV heads. Grouped-query attention (GQA) shrinks it.
Paged allocation (the idea behind vLLM's PagedAttention) stops you from
reserving a giant contiguous block per request. Prefix caching reuses
KV for a shared system prompt or a repeated RAG preamble. Speculative
decoding uses a cheaper draft to propose tokens that the main model
verifies; see S10 and lab 16.

An **OpenAI-compatible** HTTP surface (`/v1/chat/completions`, streaming
via SSE) is the practical contract in 2025 to 2026. Lab 15 is one client
against many backends. If the engine cannot speak that dialect, your
application code forks.

### The engines this course will name

Use current docs for flags. The job here is the decision.

**vLLM.** A high-throughput GPU server. Continuous batching, paged KV,
prefix caching, tensor parallel across GPUs, LoRA adapters as a serving
feature, speculative decoding on supported stacks. Default choice when
you have NVIDIA (or other supported) GPUs and a chat or completion
workload that must absorb concurrent users. It is not a laptop toy.

**SGLang.** A serving stack that treats the **radix tree of prefixes**
as a first-class cache, and treats **constrained decoding** as a
first-class path. Multi-turn agents, JSON schemas, and shared system
prompts hit the cache more often than a naive FIFO batcher expects.
If your product is a tool loop with a fat preamble, measure SGLang
before you assume vLLM is the ceiling. Throughput numbers without a
prefix-hit rate are incomplete.

**TGI (Text Generation Inference).** Hugging Face's production server.
Flash Attention, tensor parallelism, streaming, and a Hub-native
workflow. Teams already living in the Hugging Face serving and model
catalog often land here. Compare it to vLLM on *your* model, *your*
sequence lengths, and *your* batch mix. Do not compare them on a
screenshot from a different year.

**llama.cpp.** GGUF weights, aggressive quantization, CPU, Apple
silicon, and CUDA backends. The honest engine for edge, laptops, and
"this must run without a datacenter GPU." `llama-server` now speaks a
usable OpenAI-shaped API. You trade peak tokens per second on a fat GPU
for portability and a quantization zoo. Tokenizer and chat-template
mismatches are the usual production bug, not the C++ kernel.

**MLX.** Apple's array framework on unified memory, plus `mlx-lm` for
language models. The right local path when the team is on Mac and the
model fits in unified RAM. It is a development and on-device engine,
not a multi-tenant GPU cluster. Do not pretend a Mac Studio is a
fleet.

**Ollama** sits next to llama.cpp as a developer experience layer:
model pull, a local daemon, a simple API. Fine for a laptop demo and
for Engineer E1. It is usually the wrong long-term process for a
shared production SLA. If you outgrow it, you outgrow it toward
llama.cpp directly, vLLM, or SGLang, not toward more wrappers.

### A choice procedure

Write the workload in one paragraph before you clone an engine:

1. Hardware: NVIDIA GPU, Apple unified memory, CPU-only, or mixed.
2. Model: dense 7B to 70B, MoE, multimodal, embedding-only.
3. Traffic: QPS, tokens in, tokens out, p95 latency target, how much
   of the prompt is a repeated prefix.
4. Features: structured output, LoRA hot-swap, vision, tool calls,
   multi-LoRA.
5. Contract: OpenAI-compatible or not.

Then run **one** model card through two engines with the same tokenizer,
same `max_tokens`, and the same prompt set. Record TTFT, inter-token
latency, tokens per second, GPU memory, and prefix-cache hit rate.
The winner is the one that hits the SLO at the lower dollar, not the
one with the louder README.

MoE serving is a different job from dense serving: expert placement,
routing, and memory overcommit. If the card says Mixtral-class or a
sparse 100B+, read the engine's MoE notes before you buy another GPU.
Lab 17 is the routing idea, not the cluster.

## The gap most roadmaps leave

They say "run Llama in Docker" and stop. They do not mention that
**chat templates**, **BOS/EOS**, and **tokenizer versions** are part of
the serving contract. A model served with the wrong template looks like
a dumb model. They also skip prefix caching, which is often a larger
win than a new kernel once your system prompt is two thousand tokens.

They treat Ollama, vLLM, and a vendor API as interchangeable. They are
not. The application should speak one client. The operator should know
which process is behind it.

## Practice

1. Lab `15_openai_compatible_client.ipynb`: one client, fake or local
   backend, identical request shape.
2. Lab `18_kv_cache.ipynb`: feel why the second token is cheaper.
3. Optional, if you have a GPU or a Mac: serve the *same* small model
   with two of {vLLM, SGLang, llama.cpp, MLX}. Write a half page:
   hardware, TTFT, tokens/s, memory, and which feature you could not
   turn on. Do not publish weights you are not licensed to serve.

Going further (optional, paid or local GPU): read the vLLM and SGLang
metrics endpoints and sketch which gauges you would put on a dashboard
in O4.

## Watch and read

- Engine docs, current version: [vLLM](https://docs.vllm.ai/),
  [SGLang](https://docs.sglang.ai/),
  [TGI](https://huggingface.co/docs/text-generation-inference),
  [llama.cpp](https://github.com/ggml-org/llama.cpp),
  [MLX LM](https://github.com/ml-explore/mlx-lm)
- Kwon et al., Efficient Memory Management for Large Language Model
  Serving with PagedAttention (vLLM), 2023,
  [arXiv:2309.06135](https://arxiv.org/abs/2309.06135)
- Stanford CS25, serving lectures when posted (see
  [YOUTUBE.md](../../reference/YOUTUBE.md))
- GPU Mode lectures on kernels and profiling
- [TOOLS.md](../../reference/TOOLS.md) for the short compare table

## Knowledge check

1. Why does continuous batching raise decode throughput compared with
   a static batch that waits to fill?
2. Which engine family is the default when the box has no datacenter
   GPU and the weights are GGUF?
3. Why can SGLang beat a generic server on an agent workload even if
   raw kernel speed is similar?
4. What serving bug looks exactly like "the model got worse" after a
   migration?
5. Name two numbers you must record when you A/B two engines.

<details>
<summary>Answers</summary>

1. Decode is often memory-bound. Filling the GPU with in-flight
   sequences amortizes the weight read. Continuous batching lets new
   sequences occupy slots as others hit EOS, so the GPU stays busy
   without waiting for a full aligned batch.
2. llama.cpp (Ollama is a convenience layer on that family). MLX is
   the Apple-unified-memory analogue when you are not on GGUF.
3. Radix prefix caching and constrained decoding. Agents reuse long
   prefixes and often need valid JSON. Cache hits and grammar-guided
   decoding cut both latency and invalid outputs.
4. Wrong chat template, wrong tokenizer, or stripped special tokens.
   The weights did not change. The string-to-id map did.
5. Any two of: TTFT, inter-token time or tokens/s at a stated
   concurrency, GPU memory, prefix-cache hit rate, error rate under
   the same prompt set.

</details>
