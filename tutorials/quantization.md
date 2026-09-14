# Tutorial · Quantization

## Why it exists

Quantization is how a model that "needs 40 GB" runs in 8 GB, and
how a careless 4-bit conversion becomes a mysterious quality drop.
Lab 07 is the arithmetic. This note is how to talk about it without
magic.

## The idea

Weights (and sometimes activations and KV) are normally stored in
fp16 or bf16 (2 bytes per parameter). **Quantization** stores them
in fewer bits (int8, int4, and various float8 schemes) with a
**scale** (and often a **zero-point**) so you can dequantize for
math or use integer kernels directly.

**Absmax** scaling: divide by the maximum absolute value in a
group, map to the integer range. Symmetric, simple, what lab 07
starts with. **Zero-point** (asymmetric) maps min and max to the
integer range so the range need not be symmetric around zero.
**Grouping** (per-tensor, per-channel, per-group of N weights)
is the quality lever: smaller groups cost more metadata and
usually hurt less.

Methods you will see on cards:

- **bitsandbytes** NF4 / FP4: on-the-fly for training and light
  serving (QLoRA).
- **GPTQ:** post-training, uses calibration data, common for GPU
  serving of 4-bit weights.
- **AWQ:** activation-aware; protects salient weights. Also a
  4-bit serving citizen.
- **GGUF / llama.cpp:** many k-quants (Q4_K_M and friends) for
  CPU and Apple paths (O1).

None of these is "lossless." You measure the drop on **your** eval,
not on the packager's tweet. Perplexity on a generic crawl is a
weak proxy for a legal-clause extraction task.

Quantizing **KV cache** is a serving capacity move (O3). Quantizing
**weights** is a fit-in-memory move. Mixing them without measuring
TTFT and quality is how you get a fast, wrong system.

## The gap most tutorials leave

They run `.quantize()` and print "it works." They never make you
compute error on a known tensor. They never say that **calibration
data** for GPTQ/AWQ is a dataset decision with contamination risk.
They confuse "4-bit" as one thing. Q4_K_M, GPTQ 4-bit, and NF4
are different objects.

## How the lab should feel

Lab 07 should feel like a spreadsheet: a small float vector, a
scale, integers, a reconstruction, an error. Then a slightly worse
grouping. If you finish without computing an error number, redo it.
Lab 13 then places those bytes next to KV so you see which term
dominates at long context.

## Practice

1. `07_quantization.ipynb`, then the memory half of
   `13_vram_and_cost.ipynb`.
2. Pick a public 7B or 8B card. Write weights GB at fp16 and at
   Q4, then guess whether 8k context at batch 8 fits on a 24 GB
   GPU. Check yourself against lab 13's formulas.
3. Optional GPU: compare two 4-bit methods on a **tiny** prompt
   set you own. Record eval drop and tokens/s. Do not publish a
   ranking as universal.

## Watch and read

- GPTQ, Frantar et al., 2022, [arXiv:2210.17323](https://arxiv.org/abs/2210.17323)
- AWQ, Lin et al., 2023, [arXiv:2306.00978](https://arxiv.org/abs/2306.00978)
- QLoRA (for NF4 in training), [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)
- llama.cpp quant docs; Hugging Face `transformers` quantization
  docs
- S7 in this course

## Knowledge check

1. What is a scale doing in absmax quantization?
2. Why does grouping (per-channel or per-group) often beat a
   single tensor-wide scale?
3. Why is "4-bit" not enough to specify a serving stack?
4. When does KV quantization matter more than weight
   quantization?
5. Why must calibration sets for GPTQ be treated like training
   data?

<details>
<summary>Answers</summary>

1. It maps the float range onto the integer grid. Dequantization
   multiplies integers by that scale (and adds a zero-point if
   used).
2. Different channels have different magnitudes. One global max
   wastes the integer range on a few outliers.
3. Format, group size, whether embeddings and lm_head stay in
   higher precision, kernel support, and the engine (vLLM vs
   llama.cpp vs bitsandbytes) all change quality and speed.
4. At long context and high concurrency, KV dominates memory.
   Weight-only 4-bit will not admit the batch.
5. They touch the weights. Leakage, license, and "it was
   calibrated on the benchmark" are real failure modes.

</details>
