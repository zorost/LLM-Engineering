# O3 · Cost and capacity

## Why it exists

LLM bills are token bills plus GPU-time bills plus people-time bills.
If you cannot estimate them, you cannot choose an engine, a context
length, or a "we should fine-tune" meeting. This module is arithmetic
with consequences.

## The idea

### Token economics

Vendors price **prompt (input) tokens** and **completion (output)
tokens** separately. Output is usually more expensive because decode
occupies the GPU longer per token. Cached prompt prefixes, when the
vendor or engine supports them, are cheaper on the input side. Your
unit of product thought is **cost per successful task**, not cost per
1k tokens in a vacuum. A cheap model that needs three retries can lose
to a dearer model that finishes once.

Count tokens with the **same tokenizer the model uses**. A word is not
a token. Code, CJK text, and numbers have different fertility. Lab 01
and F5 exist so this sentence is not a surprise. If you log dollars
from a different tokenizer than the bill, you will argue with finance
forever.

Self-hosted cost is not free. Convert GPU-hours, electricity, reserved
instances, idle time, and engineer on-call into a per-token or
per-request number, then compare to the API. Idle GPUs are the usual
hidden line. A box at 15% utilization is a luxury good.

### Prefill, decode, and why output dominates GPU time

Prefill scales with prompt length and can be batched across tokens in
the prompt. Decode is serial in the output length (except for
speculative or block methods). For interactive chat, **output length
caps** (`max_tokens`, stop sequences, a summarizer on old turns) are
cost controls. For RAG, **chunk count and preamble size** are cost
controls. A 20k-token system prompt you never measured is a tax.

### Capacity is memory before it is FLOPs

At serving time, VRAM (or unified memory) holds:

- Weights (cut by quantization; see S7 and lab 07)
- KV cache (grows with batch × sequence × layers × KV heads × dtype)
- Activations and engine overhead
- Sometimes extra adapters (LoRA)

The request you cannot admit is the one whose KV does not fit. Long
context is a capacity feature. Raising max context from 8k to 128k
without shrinking batch is how a GPU starts 429ing. GQA, quantization
of KV, sliding windows, and prefix caching are capacity moves, not
only quality moves.

A back-of-envelope that operators actually use:

- Weights GB ≈ `parameter_count × bytes_per_param` (fp16 is 2 bytes,
  Q4 is about 0.5 plus overhead).
- KV GB is in lab 13. If you cannot sketch it, do not buy the card
  for "long context."

Throughput capacity is **tokens per second at a latency SLO**, not
peak tokens per second on a single stream. Always quote concurrency
and sequence length next to tokens/s.

### Levers, cheapest first

Before you rent another GPU:

1. **Stop generating.** Templates, extractive answers, or a classifier
   for the easy cases.
2. **Shorten the prompt.** Less RAG, better ranking, prompt cache,
   smaller history.
3. **Cap output.** Most products do not need 2k tokens.
4. **Batch and cache.** Continuous batching, prefix cache, HTTP cache
   for identical deterministic asks.
5. **Smaller or quantized model** that still passes the eval.
6. **Speculative decoding** if the engine supports it and the draft
   is honest (lab 16).
7. **More hardware** or a larger reserved instance.

Fine-tuning is not a cost-reduction strategy unless it lets you serve
a smaller model at the same eval. It has its own GPU bill (S4). RAG
is a cost strategy when it lets a small model cite instead of a large
model guess. It has its own retrieval bill.

### Planning QPS

You need an arrival rate (requests per second), a prompt-length
distribution, an output-length distribution, and a latency SLO.
Little's law still applies: concurrency ≈ arrival rate × residency
time. Residency time is TTFT plus tokens_out × time_per_token, plus
queue. If the math says you need 12 in-flight generations and the
KV for 12 × 32k does not fit, you do not have a kernel problem. You
have a product problem (shorter context) or a hardware problem.

Reserved capacity versus on-demand: reserved is cheaper if you
actually use it. Burst to an API fallback rather than owning a second
idle cluster for a once-a-quarter spike, unless data residency forbids
it. That is an L1 decision with an O3 number attached.

## The gap most roadmaps leave

They quote a vendor's per-1k price and ignore **output length**,
**retry inflation**, **idle GPUs**, and **tokenizer mismatch**. They
never make the student compute KV memory, so "just use 128k context"
survives until the first outage. They treat self-hosting as morally
cheaper. Sometimes it is. Measure.

## Practice

Labs `13_vram_and_cost.ipynb` and `19_scaling_laws.ipynb`.

Then, on one page, for a product you care about:

1. Tokens in, tokens out, requests per day.
2. API bill at list prices, and a self-host estimate at 40% GPU
   utilization.
3. KV memory at your advertised max context and target concurrency.
4. The first lever you would pull if the bill doubled.

Optional: price the same workload at 4-bit versus fp16 on one GPU
generation using public memory numbers only.

## Watch and read

- F5 in this course, then CS336 resource-accounting lectures
  ([2026 playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rMqXOcazWaTUHhq-yembLCV))
- Chip Huyen, *AI Engineering*, on inference optimization and cost
- Databricks and cloud vendor LLM inference pricing notes (they rot;
  read the date)
- [BOOKS.md](../../reference/BOOKS.md) for the leadership treatment of
  the same arithmetic

## Knowledge check

1. Why are output tokens often dearer than input tokens on a price
   list, and on a GPU?
2. What grows with context length even after you quantize the
   weights?
3. When is fine-tuning a cost win?
4. Why is "tokens per second" without concurrency and sequence length
   a vanity metric?
5. Name three cheaper levers than buying another GPU.

<details>
<summary>Answers</summary>

1. Price lists reflect that decode occupies scarce GPU time per
   emitted token. Prefill processes many prompt tokens in parallel.
   Decode is typically memory-bound and serial in output length.
2. The KV cache (and admission of concurrent requests).
3. When it lets you serve a smaller or cheaper model at the same
   eval, or when it cuts prompt length (for example, by baking in
   format). Not when it is a ritual on the same 70B you already
   serve.
4. Because a single stream on an empty GPU looks fast, and a loaded
   GPU at 32k context looks like a different machine.
5. Any three of: cap output, shrink prompts, cache prefixes, batch,
   quantize or downsize the model, speculative decode, refuse easy
   cases without a model.

</details>
