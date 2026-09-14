# S2 · Pre-training

## Why it exists

Pre-training is the only stage that creates a general next-token model
from unlabeled text. If you cannot say what data went in, how the
batch was split across devices, and which scalar says the run is dying,
you are watching a progress bar.

## The idea

### The job

Minimize token-level cross-entropy of the next token under a huge
corpus. Teacher forcing: the model sees the true prefix, not its own
samples. The checkpoint you download as "base" or "pretrained" is the
result of this loop, sometimes followed by a lighter **mid-training**
pass on math, code, or long documents.

You will almost never run this at frontier scale. You still need the
map, because every later stage inherits the tokenizer, the context
length, the data mixture, and the failure modes of this run.

### Data, not "the internet"

Public mixtures you can actually name:

- **FineWeb** ([HuggingFaceFW/fineweb](https://huggingface.co/datasets/HuggingFaceFW/fineweb)):
  Common Crawl, cleaned and deduplicated, on the order of 15T+ English
  tokens, ODC-By. FineWeb-Edu is the educational slice. FineWeb-2
  extends the recipe past English. The processing code is
  [datatrove](https://github.com/huggingface/datatrove).
- **RedPajama**: Together's open attempt to match a Llama-era mixture
  (Common Crawl, C4, GitHub, books, arXiv, Wikipedia, StackExchange).
  Useful as a documented recipe, not as a 2026 default dump.
- **Dolma** ([allenai/dolma](https://huggingface.co/datasets/allenai/dolma)):
  Allen AI's documented mix (web, code, papers, books, encyclopedic).
  The point is the **datasheet**, not the brand.
- **OLMo** ([allenai.org/olmo](https://allenai.org/olmo)): a fully
  open stack (data, code, intermediate checkpoints, evals). Use it
  when you need to see a real training log, not a marketing card.

Curation is filtering plus mixing. Language ID, quality classifiers,
PII scrubs, min-length, stopword heuristics, and **deduplication**
decide the loss more than the optimizer. Exact hash catches copies.
**MinHash / LSH** catches near-duplicates across crawls. Semantic
near-dup (embeddings, see also S3's semhash) catches paraphrases that
would otherwise dominate a domain.

Dedup is not optional. A duplicated Wikipedia dump looks like a
better model on Wikipedia evals and a worse model everywhere else.
Decontamination against **eval sets** belongs here and in S11. If
MMLU items sit in the crawl, S6 is theater.

### Parallelism

One GPU does not hold a 70B AdamW state. Three axes, used together
as **3D parallel**:

- **Data parallel**: each rank sees a different micro-batch, gradients
  all-reduce. ZeRO (S4) shards optimizer state on this axis. This is
  the first knob you turn.
- **Tensor parallel**: split a single matmul (column/row of `W`) across
  GPUs in a node. High communication, NVLink-friendly. Attention and
  MLP both split.
- **Pipeline parallel**: split layers into stages. Micro-batches fill
  the pipeline. Bubble time is the tax. Too few micro-batches and the
  GPUs wait.

**Context / sequence parallel** shards the sequence dimension when
activation memory at long context explodes. **Expert parallel** shards
MoE experts across ranks (S1). The Ultrascale Playbook
([nanotron space](https://huggingface.co/spaces/nanotron/ultrascale-playbook))
is the public picture of how these compose.

[nanotron](https://github.com/huggingface/nanotron) is Hugging Face's
minimal 3D-parallel trainer. Read a tiny Llama config there before you
open Megatron. **LLM360** (Amber, CrystalCoder, K2; org moving to
[IFM](https://huggingface.co/IFM)) published weights, data, code, and
intermediate checkpoints so a run is inspectable. That transparency is
the lesson. Do not treat a closed lab's blog as a substitute.

### Optimizers and the boring knobs that save runs

**AdamW** is the default: Adam with **decoupled weight decay**. The
decay hits the weights, not the Adam moments. Learning rate is a
schedule, not a constant:

1. **Warmup** from near-zero for a few thousand steps so the first
   batches do not explode an unnormalized residual stream.
2. Cosine or linear **decay** toward a floor.
3. Optional cooldown / WSD-style schedules in 2024 to 2026 recipes.

**Gradient clipping** (global L2, often 1.0) caps a bad batch. Spikes
still happen. Clip keeps one spike from NaN-ing the run. It does not
fix bad data.

**Mixed precision**: forward and backward in **bf16** (or fp16 with a
loss scaler). Master weights and Adam moments stay fp32. bf16 is the
GPU default when the chip has it: same exponent range as fp32, no
scaler dance. fp16 needs dynamic loss scaling. fp32-only training is
a debug mode. See S7 for what these formats *mean*.

**Gradient accumulation** fakes a larger batch when VRAM does not
allow it. The optimizer step sees the summed grads. Token batch size
(tokens per optimizer step) is the number you log, not "batch=8."

### Monitoring

A pre-training dashboard that is not lying tracks at least:

| Scalar | What a healthy run does |
|---|---|
| Train loss | down, with noise; sudden up is data or LR |
| Eval loss on a frozen holdout | down, then flat; up is overfit or shift |
| Grad norm | bounded; a spike with a clip count is a warning |
| Tokens/s and TFLOPs/s | flat; a drop is a hang, a straggler, or I/O |
| Learning rate | matches the schedule you think you launched |
| Remaining NaNs / skipped steps | zero, or you are already in incident mode |

Log the **data source mix** per step if you up-sample domains. A silent
mixture change looks like a capability regression two weeks later.

Karpathy's [nanoGPT](https://github.com/karpathy/nanoGPT) is the
readable single-node version of this loop. CS336 is the resource-
accounting version (F5). Neither replaces a cluster. Both replace
mythology.

## The gap most roadmaps leave

They say "train on a large corpus with Adam" and link a Colab that
fine-tunes. The missing work is **operational**:

- Which crawl, which dedup, which eval leaked into train.
- Which parallel axis you are on, and why the tokens/s number moved.
- Warmup, clip, bf16, and the master-weight copy.
- Intermediate checkpoints you can actually load (OLMo, LLM360),
  not a single final dump.

If you cannot write a one-page run card (data, tokens, parallel plan,
LR, precision, evals), you are not ready to spend GPU money.

## Practice

Lab `notebooks/19_scaling_laws.ipynb` for the shape of loss vs
compute. Then, on paper, pick a public 7B card (OLMo 2 or an Apache
checkpoint) and fill:

1. Pre-training tokens claimed, and whether the dataset is named.
2. Context length at pre-train vs the "128k" infer flag.
3. Parallelism you would need on 8×80 GB, in one sentence.
4. What you would plot besides train loss.

Optional: skim a [nanotron](https://github.com/huggingface/nanotron)
tiny-Llama config. Do not launch it until F5's VRAM estimate is on
that page.

## Watch and read

- Stanford CS336, data, parallelism, and scaling-law lectures ([course](https://cs336.stanford.edu/), [2026 playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rMqXOcazWaTUHhq-yembLCV))
- Karpathy, [nanoGPT](https://github.com/karpathy/nanoGPT) and the Deep Dive tokenizer/data sections
- Hugging Face, [FineWeb paper](https://arxiv.org/abs/2406.17557), [datatrove](https://github.com/huggingface/datatrove), [nanotron](https://github.com/huggingface/nanotron), [Ultrascale Playbook](https://huggingface.co/spaces/nanotron/ultrascale-playbook)
- Allen AI, [Dolma](https://huggingface.co/datasets/allenai/dolma), [OLMo](https://allenai.org/olmo)
- Together, [RedPajama-Data](https://github.com/togethercomputer/RedPajama-Data)
- LLM360 / IFM, [project paper](https://arxiv.org/abs/2312.06550) and [IFM org](https://huggingface.co/IFM)
- Loshchilov and Hutter, [AdamW](https://arxiv.org/abs/1711.05101)
- Lilian Weng, [Transformer family](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/) (training notes)
- Sebastian Raschka, pre-training chapters in *Build a Large Language Model (From Scratch)*

## Knowledge check

1. What does pre-training optimize, in one sentence?
2. Why does near-duplicate web text distort both loss and evals?
3. What is the difference between tensor parallel and pipeline parallel?
4. Why keep Adam moments in fp32 while the forward pass is bf16?
5. Name three scalars you would page on at 3 a.m.

<details>
<summary>Answers</summary>

1. Expected next-token cross-entropy on the pre-training mixture
   (with whatever packing and masking the trainer uses).
2. Repeated documents overweight those domains, so the model looks
   strong on leaked evals and weak on fresh text. Dedup is quality
   control, not tidiness.
3. Tensor parallel splits a layer's matmuls across GPUs (heavy intra-
   layer comms). Pipeline parallel splits layers into stages (bubble
   time, less all-reduce inside a layer).
4. Small-exponent fp16/bf16 noise in the moments accumulates. The
   master copy and optimizer state stay wide so updates do not vanish
   or explode.
5. Grad norm / clip rate, eval loss on a frozen holdout, tokens/s
   (hangs), NaN count. Train loss alone is not enough.

</details>
