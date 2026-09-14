# F5 · Scaling, information, and hardware

## Why it exists

This is the module the 2024 public roadmaps almost never had, and the
one that saves real money. If you cannot estimate tokens, FLOPs, and
VRAM, you are shopping, not engineering.

## The idea

### Information

A token is not a word. English often lands around 3 to 4 characters per
token, but code, other languages, and numbers move that number. Context
windows are counted in tokens. Bills are counted in tokens. Fertility
(tokens per word) is why a "multilingual" model can be worse than its
English scores suggest. See S1 and S11.

### Scaling laws

Loss falls as a power of compute, data, and parameters, in a range, not
forever. Chinchilla-style results said: for a compute budget, smaller
models with more data can beat larger starved models. That statement has
caveats (data quality, synthetic data, sparse MoE, inference cost). Read
the plots. Do not quote the slogan.

Lab 19 is a toy curve so the shape is in your hands.

### Hardware literacy

You need working numbers, not a vendor SKU list:

- **VRAM** holds weights, KV cache, activations, optimizer states
  (training). Inference of a dense 7B in fp16 is roughly 14 GB for
  weights alone, before KV. Quantization cuts the weight term. Long
  context grows the KV term. See lab 13 and E6.
- **FLOPs** are math. Memory bandwidth is often the bottleneck for
  decode (one token at a time is memory-bound). Prefill (the prompt) is
  more compute-bound.
- **Arithmetic intensity** is FLOPs per byte. CS336 lecture 2 exists
  for this.
- **Batching** raises utilization. Unbatched chat is an expensive hobby.

Unified memory on Apple silicon (MLX, llama.cpp) changes the shopping
list. It does not repeal the math.

## The gap most roadmaps leave

They jump to "run Llama in Colab" with no budget. Then the engineer
learns VRAM from CUDA OOM. We teach the estimate first, the OOM second.

## Practice

Labs `13_vram_and_cost.ipynb` and `19_scaling_laws.ipynb`. Then pick a
public 8B model card and write, on one page: weights in GB at fp16,
at Q4, KV cache for 8k context at batch 1, and a ballpark token price
if you served 10 requests/second.

## Watch and read

- Stanford CS336, lectures on PyTorch / resource accounting, GPUs, and
  scaling laws ([2026 playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rMqXOcazWaTUHhq-yembLCV))
- Hugging Face, GPU inference docs
- Databricks, LLM inference performance notes
- Karpathy, Deep Dive into LLMs (the tokenizer and compute sections)

## Knowledge check

1. Why can decode be memory-bound while prefill is not?
2. What grows with sequence length at inference even if weights are
   quantized?
3. What did Chinchilla argue, and what is a valid caveat?
4. Why is tokens-per-word a product metric?
5. Name two optimizer-state reasons training uses more memory than
   inference.

<details>
<summary>Answers</summary>

1. Decode generates one (or a few) tokens with a large weight read per
   token. Prefill processes the whole prompt in parallel, so compute
   per byte is higher.
2. The KV cache (and some activations).
3. Allocate more tokens to smaller models for a training-compute
   budget. Caveats: data quality, inference-compute optimality, MoE,
   overtrained small models in 2024 to 2026 practice.
4. It drives cost, latency, and quality for non-English and code.
5. Adam keeps extra moments per parameter (often 2× fp32); gradients
   and (if not sharded) a full copy of weights in the optimizer.

</details>
