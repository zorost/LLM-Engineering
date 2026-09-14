# S7 · Quantization

## Why it exists

Weights in fp16 are often the reason a model does not fit. Quantization
is a compression of those numbers. It is not a free lunch: you trade
bits for error, and the winning format depends on whether you train,
serve on a GPU, or serve on a laptop CPU.

## The idea

### The formats, as numbers

| Format | What it is | Where you meet it |
|---|---|---|
| **fp32** | 32-bit float | master weights, Adam states (S2, S4) |
| **fp16** | 16-bit float, small exponent | older mixed precision, some GPUs |
| **bf16** | 16-bit, fp32 exponent | training and GPU serve default |
| **int8** | 8-bit integer + scale | SmoothQuant, some on-the-fly casts |
| **int4 / NF4** | 4-bit integer or normal-float | QLoRA, GPTQ, AWQ, GGUF Q4 |

A 7B dense model is roughly 14 GB in fp16/bf16 weights alone, 7 GB
in int8, 3.5 to 4.5 GB in 4-bit depending on metadata and extras.
KV cache is **not** in that number unless you quantize it separately
(E6, lab 13, lab 18).

### Absmax and zero-point

Two schoolbook maps from float vectors to integers (lab 07):

- **Absmax (symmetric)**: scale = max|x| / qmax. Zero stays zero.
  Simple. Wastes range if the tensor is not symmetric.
- **Zero-point (asymmetric)**: map min..max onto the integer grid
  with a scale and an offset. Better when activations are shifted.

Per-tensor scales are cheap and crude. **Per-channel** (per output
feature) is the usual weight recipe. **Groups** of 32 or 128 values
sharing a scale (GPTQ/AWQ/GGUF k-quants) are the 4-bit compromise:
more scales, less error, a bit more metadata.

The error you care about is **downstream tokens**, not MSE on W.
A layer that looks fine in MSE can still ruin a rare name.

### GGUF and llama.cpp

**[llama.cpp](https://github.com/ggerganov/llama.cpp)** is the CPU
(and Metal/CUDA) runtime people actually ship on laptops.
**GGUF** is its file format: tensors plus tokenizer plus metadata
in one file. Quant types are a family (`Q4_K_M`, `Q5_K_S`, `Q8_0`,
IQ quants, …), not a single "int4."

GGUF wins when:

- The box is a laptop, a Mac, or a small server without a Python
  inference stack.
- You want one file and a stable CLI.
- You are willing to convert from Hugging Face (and to accept that
  conversion is a one-way product artifact).

GGUF is the wrong default for QLoRA training (use bitsandbytes / NF4)
and a weak default for high-QPS GPU serving (use AWQ/GPTQ/FP8 on
vLLM or SGLang; O1).

### GPTQ, EXL2, AWQ

GPU weight-only methods, offline:

- **GPTQ** ([paper](https://arxiv.org/abs/2210.17323)): layer-wise
  4-bit (or 3-bit) with Hessian-aware rounding, calibration data.
  Mature, widely served. Quality depends on the calibration set.
- **AWQ** ([paper](https://arxiv.org/abs/2306.00978)): find weight
  channels that matter for activations, **scale them up** before
  quantizing so they keep more resolution. Often gentler on
  instruction models than a careless GPTQ. vLLM and TGI speak it.
- **EXL2** ([ExLlamaV2](https://github.com/turboderp/exllamav2)):
  variable bits per tensor, packed for that kernel family. Excellent
  speed on NVIDIA if you are in the ExLlama serving path. Less
  portable than GGUF or AWQ in vLLM.

All three need a **calibration** pass on real text. Garbage
calibration, garbage 4-bit. Do not calibrate on a single Wikipedia
article and ship.

### SmoothQuant and activation-aware tricks

Weight-only quant is easy because weights are static. **Activations**
have outliers (a few channels with huge values). **SmoothQuant**
([paper](https://arxiv.org/abs/2211.10438)) migrates difficulty from
activations to weights by a per-channel smooth factor, then quantizes
both, which is how **int8 matrix multiply** becomes realistic.

You meet this when someone wants **W8A8** for Tensor Core int8, not
when you want a 4-bit laptop file. If the blog says SmoothQuant and
then dumps a GGUF, they mixed families.

### bitsandbytes

**[bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes)**
is the training-time library: 8-bit Adam, 8-bit and 4-bit (NF4)
**on-the-fly** quant for frozen bases (QLoRA). NF4 is a 4-bit code
matched to a normal distribution, not a GGUF k-quant.

Use bitsandbytes when you **train**. Export a serving artifact
afterward (merge LoRA, then AWQ or GGUF). Loading a QLoRA adapter
in bitsandbytes in production is a research convenience, not a
serving plan.

Hugging Face `transformers` quantization docs glue these together.
Read which path is **load-time** (BnB, GPTQ, AWQ) vs **convert-once**
(GGUF, EXL2).

### When each format wins

| Constraint | Format |
|---|---|
| Train LoRA on one 24 GB GPU | QLoRA, bitsandbytes NF4 |
| Train full FT on a GPU node | bf16 (fp8 recipes exist; not your first move) |
| Serve 7B on a Mac / CPU laptop | GGUF `Q4_K_M` or `Q5_K_M` in llama.cpp / MLX-related flows |
| Serve high QPS on NVIDIA | AWQ or GPTQ (or fp8) in vLLM / SGLang; EXL2 if that is your engine |
| Debug numerics / match a paper | bf16 or fp32, no quant |
| KV-heavy long context | quant weights **and** think about KV quant (E6); GQA/MLA first (S1) |

Measure with **your** eval suite (S6), not with "perplexity went
up 0.1 so we ship." 4-bit often keeps chat. It drops rare entities,
code, and multilingual scripts first. If the product is those, spend
the extra bit.

## The gap most roadmaps leave

They say "use 4-bit" as if it were one file. Missing:

- Absmax vs zero-point, per-channel vs grouped, so lab 07 is not
  a toy.
- GGUF as a runtime+format pair, not a synonym for GPTQ.
- Calibration data as part of the artifact.
- Train format (BnB) vs serve format (AWQ/GGUF).
- KV cache still in higher precision unless you opted in.

## Practice

Lab `notebooks/07_quantization.ipynb`. Quantize a toy vector with
absmax and with zero-point. Change the outlier. Then, on paper,
pick a 8B card and write: fp16 GB, Q4 GB, whether you would serve
GGUF or AWQ on the hardware you actually have (F5, lab 13).

Going further: convert a small public Apache checkpoint to GGUF
with llama.cpp and compare five prompts at Q8 vs Q4. Do not start
from a restricted or non-commercial weight.

## Watch and read

- Hugging Face, [quantization docs](https://huggingface.co/docs/transformers/quantization), [LLM course](https://huggingface.co/learn/llm-course)
- [llama.cpp](https://github.com/ggerganov/llama.cpp) GGUF readme
- Frantar et al., [GPTQ](https://arxiv.org/abs/2210.17323); Lin et al., [AWQ](https://arxiv.org/abs/2306.00978); Xiao et al., [SmoothQuant](https://arxiv.org/abs/2211.10438)
- [ExLlamaV2 / EXL2](https://github.com/turboderp/exllamav2), [bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes)
- Sebastian Raschka, quantization notes on his magazine; *Build a Large Language Model (From Scratch)*
- Stanford CS336, inference / precision lectures
- Karpathy, Deep Dive (compute and precision remarks)

## Knowledge check

1. Why is a 7B "14 GB" number not the VRAM you need to serve it?
2. What does a zero-point buy you that absmax does not?
3. When do you choose GGUF over AWQ?
4. What is bitsandbytes NF4 for, if not laptop serving?
5. Why does calibration data belong in the model card for GPTQ/AWQ?

<details>
<summary>Answers</summary>

1. That 14 GB is fp16 **weights**. KV cache, activations, CUDA
   context, and batch grow the number. Quantizing weights leaves
   the cache term.
2. An offset so a shifted min..max range uses the integer grid
   instead of wasting codes on unused negative or positive span.
3. CPU/Mac/local one-file serving with llama.cpp. AWQ when the
   production engine is a GPU server (vLLM/TGI) that already
   loads AWQ.
4. Training-time 4-bit bases (QLoRA) and 8-bit optimizers. Export
   a serving format after training.
5. The rounding solved for those weights on that data. A different
   calibration domain (code vs chat) changes error on the tasks
   you care about.

</details>
