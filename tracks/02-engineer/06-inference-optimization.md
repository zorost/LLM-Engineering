# E6 · Inference optimization

## Why it exists

Decode is why the bill and the latency exist. Prefill reads
the prompt in parallel. Decode writes one token (or a small
draft block) at a time and is often **memory-bound**: you are
waiting on weight reads, not on FLOPs. This module is the
standard toolkit that serving engines use so a GPU is not
idle. Operator track (O1) is how you pick an engine. Here you
learn the mechanisms so those names mean something.

## The idea

### Prefill versus decode

**Prefill:** the full prompt, highly parallel, more
compute-bound. **Decode:** each new token attends to all
prior keys and values. Without a cache you recompute
attention over the growing prefix every step. That is the
naive picture. Lab `18_kv_cache.ipynb` makes the second
token cheaper on a toy sequence. [transformer-explainer](https://github.com/zorost/transformer-explainer)
is the visual companion.

F5 is the hardware literacy. Come back if VRAM versus
bandwidth is still mush.

### KV cache

After prefill, each layer stores **keys and values** for
tokens already seen. Decode appends one column (or a block)
instead of rebuilding the past. Memory grows with *layers ×
heads × sequence × d_head × batch × precision*. Long context
is a KV problem as much as a weight problem. Quantizing
weights does not shrink KV unless you also quantize or
evict cache.

**Prefix (prompt) cache.** Shared prefixes (system prompt,
few-shot block, tool schemas) can be reused across requests
when the bytes match. Hosted APIs call this prompt caching.
Local engines call it prefix cache. A system prompt that
changes every request throws the hit away. E9.

### Attention kernels and head grouping

**Flash Attention** (Dao et al.,
[arXiv:2205.14135](https://arxiv.org/abs/2205.14135),
[github.com/Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention)).
An IO-aware attention implementation: tile the softmax so
you do not materialize the full *n × n* matrix in HBM.
Same math, less memory traffic, longer context becomes
feasible. You almost never write it yourself. You require
an engine that uses it.

**MQA (multi-query attention).** Many query heads, one key
and one value head. KV cache shrinks a lot. Quality is the
trade.

**GQA (grouped-query attention).** Groups of query heads
share a KV head. The production compromise in Llama-class
and many peers. transformer-explainer shows the wiring.

Architecture (S1) chooses MQA/GQA. Serving just has to
allocate the smaller cache.

### Paged attention and continuous batching

**Paged attention** (vLLM, Kwon et al.,
[arXiv:2309.06180](https://arxiv.org/abs/2309.06180)).
KV cache in fixed-size pages, like virtual memory, so you
do not pre-allocate a giant contiguous tensor per sequence
and fragment the GPU. Variable-length requests stop wasting
VRAM.

**Continuous batching** (iteration-level scheduling; the
Orca line of work, Yu et al., OSDI 2022). Sequences join
and leave a batch as they finish. You do not wait for the
slowest prompt in a static batch of eight. Throughput at
load comes from this more than from a clever kernel at
batch 1.

Together: paged KV plus continuous batching is why vLLM and
peers beat a naive `generate()` loop. TGI and SGLang are
the same family of ideas with different extras (E7).

### Speculative decoding and EAGLE

The target model is expensive per token. A **draft** model
(or a head) proposes several tokens. The target **verifies**
them in one parallel pass. Accepted tokens are free relative
to serial decode; rejected tokens fall back. Correctness:
the output distribution matches the target if verification
is done right. Lab `16_speculative_decoding.ipynb` is a toy
alphabet. S10 is the scientist view (distillation, draft
training).

**EAGLE** (Li et al.,
[arXiv:2401.15077](https://arxiv.org/abs/2401.15077);
code [github.com/SafeAILab/EAGLE](https://github.com/SafeAILab/EAGLE))
drafts at the feature level (second-to-top layer) rather
than only with a small independent LM. EAGLE-2/3 add dynamic
draft trees. Engines expose "speculative" as a flag; EAGLE
is one strong method in that family. You care about
**acceptance rate**. Low acceptance means you paid for a
draft and still ran the target.

Medusa, lookahead, and native MTP (multi-token prediction)
heads are relatives. Same contract: draft, verify, measure
speedup on *your* traffic, not on a blog.

## The gap most roadmaps leave

They list "use vLLM" without **which bottleneck**:

| Symptom | First suspect |
|---|---|
| Batch 1 chat is slow | Decode memory bandwidth; quantization; speculative |
| High QPS, GPU idle gaps | Continuous batching not on; tiny batches |
| OOM at long context | KV cache; paged attention; GQA already in the weights? |
| Shared system prompt still costs full prefill | Prefix cache broken by a changing prefix |
| Speculative "on" but no speedup | Draft too weak; acceptance collapse |

If you cannot fill that table, you are swapping Docker images.

## Practice

1. Lab `18_kv_cache.ipynb`. Compute why token 2 is cheaper.
2. Lab `16_speculative_decoding.ipynb`. Change draft quality
   and watch accept rate.

Then, on paper (F5 / lab 13 numbers): KV bytes for 8k
context, batch 1, a 32-layer GQA model at fp16. No GPU
required.

Going further: read the vLLM paged-attention paper's
figures. Optional: transformer-explainer KV and GQA views.

## Watch and read

- Flash Attention, [arXiv:2205.14135](https://arxiv.org/abs/2205.14135)
- vLLM / paged attention, [arXiv:2309.06180](https://arxiv.org/abs/2309.06180)
  and [docs.vllm.ai](https://docs.vllm.ai/)
- Orca, [USENIX OSDI 2022](https://www.usenix.org/conference/osdi22/presentation/yu)
- EAGLE, [arXiv:2401.15077](https://arxiv.org/abs/2401.15077) ·
  [github.com/SafeAILab/EAGLE](https://github.com/SafeAILab/EAGLE)
- GQA, [arXiv:2305.13245](https://arxiv.org/abs/2305.13245)
- Dao-AILab, [flash-attention](https://github.com/Dao-AILab/flash-attention)
- [transformer-explainer](https://github.com/zorost/transformer-explainer)
- Stanford CS336, GPU / inference lectures
  ([2026 playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rMqXOcazWaTUHhq-yembLCV))

## Knowledge check

1. Why can decode be memory-bound while prefill is not?
2. What does GQA reduce in the serving budget?
3. What problem does paged attention solve that Flash
   Attention does not?
4. What must be true of a prefix for prompt caching to hit?
5. What does speculative decoding refuse to sacrifice if it
   is implemented correctly?

<details>
<summary>Answers</summary>

1. Decode streams large weights for a small amount of math
   per token. Prefill processes many prompt tokens in
   parallel, so arithmetic intensity is higher.
2. KV cache size (and KV bandwidth), by sharing KV heads
   across groups of query heads.
3. Fragmentation and over-reservation of KV memory across
   many variable-length sequences. Flash Attention speeds
   and shrinks the attention *kernel* for a given sequence.
4. Byte-identical cached prefix (system, tools, static
   few-shot). A per-request timestamp in the prefix misses.
5. The target model's output distribution. Verification
   rejects draft tokens that the target would not have
   sampled.

</details>
