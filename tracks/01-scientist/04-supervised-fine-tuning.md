# S4 · Supervised fine-tuning

## Why it exists

SFT is how a base model learns the assistant pattern in your template,
on your tasks, with a loss you can still explain. Preference methods
(S5) sit on top of a model that already completes a turn. If SFT is
wrong, DPO will polish the wrong dialect.

## The idea

### Full fine-tune vs LoRA vs QLoRA

**Full fine-tune** updates every parameter. Highest ceiling, highest
VRAM (weights, grads, Adam moments: often ~16 bytes/param with AdamW
in mixed precision, before activations). Use it when you have the
GPUs, the data volume, and a domain shift that adapters underfit
(new language, heavy code style, a tokenizer you actually changed).

**LoRA** freezes the base and learns a pair of thin matrices
`A` (`r × d_in`) and `B` (`d_out × r`) whose product is added to a
weight, scaled by `α / r`. Trainable parameter count is
`r × (d_in + d_out)` per target. You store a small adapter. You merge
it for serving if you want a single file.

**QLoRA** keeps the base in 4-bit (typically NF4 via bitsandbytes)
and trains LoRA in 16-bit on top. That is how 7B SFT landed on a
single 24 GB card. The 4-bit base is a memory trick. The adapter is
still the thing you learn. See S7 for why NF4 is not GGUF.

Pick in this order: QLoRA if you are VRAM-poor and the task is
instruction-style; LoRA in bf16 if you have the memory and care about
adapter quality; full FT if adapters plateau and you can pay.

### Rank, alpha, targets

- **Rank `r`**: capacity of the adapter. 8 and 16 are the boring
  defaults for chat. 64+ is for harder domain shift. Doubling `r`
  roughly doubles adapter params, not quality.
- **Alpha `α`**: scale. A common convention is `α = 2r` so the
  multiplier `α / r` is 2, or `α = r` for a multiplier of 1. Mixing
  conventions across tools is a silent bug. Write the multiplier in
  the run card, not only `r`.
- **Targets**: which modules get A/B. Attention `q_proj`/`v_proj` is
  the historical minimum. Adding `k_proj`, `o_proj`, and the MLP
  (`gate_proj`, `up_proj`, `down_proj`) is the 2025 default for
  serious SFT. Targeting only `q` and `v` underfits code and math
  more often than people admit. Embedding / `lm_head` LoRA is for
  tokenizer or vocabulary shifts; skip it until you have that problem.

Dropout on LoRA layers is optional. **NEFTune** adds noise to
embeddings during SFT (paper: [2310.05914](https://arxiv.org/abs/2310.05914)).
Small lift on some instruction sets, free to try, not a substitute
for data.

Lab 05 is shapes and parameter counts. Compute them before you rent.

### Trainers

You do not need a new framework. You need one you can read.

- **TRL** (`SFTTrainer`) is the Hugging Face default: datasets,
  packing, completion-only loss, PEFT. Start here.
- **Unsloth** patches kernels and loaders for faster LoRA/QLoRA on
  supported models. Use it when the model is on their list and wall
  clock is the bottleneck. It is not a different algorithm.
- **Axolotl** is YAML-first: many community recipes, many knobs.
  Good when you want a documented config others can rerun. Bad when
  you cannot explain a flag you copied.

[PEFT](https://huggingface.co/docs/peft) is the adapter library TRL
sits on. Read `LoraConfig` once.

### Memory beyond LoRA: ZeRO and FSDP

When LoRA is not enough, or you full-FT:

- **DeepSpeed ZeRO-1** shards optimizer state. **ZeRO-2** also shards
  gradients. **ZeRO-3** shards parameters (fetch on use). Stage 3
  is how large full FTs fit; communication cost rises.
- **FSDP** (PyTorch) is the native cousin: wrap units, shard params,
  optional CPU offload. Hugging Face Trainers speak both.

These are data-parallel cousins of S2's 3D plan. For 7B LoRA you
often need neither. For 70B full FT you need both a plan and a
cluster. Activation checkpointing (recompute backward) trades FLOPs
for activation RAM. Turn it on before you turn on offload.

### Packing and loss masking

**Packing** concatenates short conversations into the context window
so you do not pad a 40-token turn to 4096. Cross-contamination
between packed docs is a real bug if you forget attention masks /
position resets. TRL packing is not "set true and walk away." Check
one packed batch.

**Loss masking** (completion-only / train-on-responses): zero the
loss on bos, system, and user tokens. The model should not learn to
predict the user's question. If you skip this, the run still drives
loss down. It just learns to parrot the prompt distribution.

Masking is template-dependent. That is why S3 comes first.

### Monitoring spikes

SFT dies in ordinary ways:

| Symptom | Usual cause |
|---|---|
| Loss NaN at step 1 to 20 | LR too high, fp16 without a scaler, bad ids |
| Loss spike mid-run | a packed batch with huge tokens, a corrupt row, clip too loose |
| Loss near zero, val garbage | masking inverted, or eval template mismatch |
| Endless decode after train | eos never in the targets (S3) |
| Adapter does nothing | `r` tiny, wrong targets, or you evaluated the base |

Log: train loss, eval loss on a frozen set, grad norm, tokens/s,
learning rate, a **qualitative sample** every N steps with the
production template. A 0.01 loss drop with worse samples is the
run telling you the metric is wrong.

Gradient clip still applies. Warmup still applies. A cosine decay
from 2e-4 (full) or 1e-4 to 2e-4 (LoRA) is a starting point, not a
law. If the first 50 steps explode, lower LR before you change rank.

## The gap most roadmaps leave

They screenshot a QLoRA Colab and call it SFT. The missing knobs
are the ones that decide whether the adapter is loadable in your
server:

- `r`, `α/r`, and target modules, written down.
- Completion-only loss and packing masks.
- The same chat template at train and serve.
- ZeRO/FSDP as memory math, not as a cargo-cult flag.
- Spike response: clip, skip, inspect the batch, do not "resume
  from latest" blindly onto a corrupted optimizer state.

## Practice

Lab `notebooks/05_lora_shapes.ipynb`. Compute trainable params for
`r=8` vs `r=64` on a toy attention map. Then write a one-page SFT
card for a 7B you might actually tune: full vs LoRA vs QLoRA, `r`,
`α`, targets, packing, mask, LR, and whether ZeRO is required on
the GPU you have (F5 / lab 13).

Going further, on a machine you pay for: TRL `SFTTrainer` + PEFT on
a small public instruct mix you decontaminated (S3). Unsloth or
Axolotl only after that loop works.

## Watch and read

- Hugging Face, [TRL SFT](https://huggingface.co/docs/trl/sft_trainer), [PEFT LoRA](https://huggingface.co/docs/peft), [LLM course](https://huggingface.co/learn/llm-course)
- Hu et al., [LoRA](https://arxiv.org/abs/2106.09685); Dettmers et al., [QLoRA](https://arxiv.org/abs/2305.14314)
- Jain et al., [NEFTune](https://arxiv.org/abs/2310.05914)
- Sebastian Raschka, [LoRA from scratch](https://magazine.sebastianraschka.com/p/lora-from-scratch) and the SFT chapters in *Build a Large Language Model (From Scratch)*
- [Unsloth](https://github.com/unslothai/unsloth), [Axolotl](https://github.com/axolotl-ai-cloud/axolotl)
- DeepSpeed, [ZeRO](https://www.deepspeed.ai/tutorials/zero/); PyTorch, [FSDP](https://pytorch.org/blog/introducing-pytorch-fully-sharded-data-parallel-api/)
- Stanford CS336, post-training / fine-tuning lectures
- Karpathy, Deep Dive (supervised instruction section)

## Knowledge check

1. When do you full-FT instead of LoRA?
2. What does `α / r` control, and why do two tools disagree?
3. Why mask loss on user tokens?
4. What does QLoRA quantize, and what stays 16-bit?
5. Name two reasons an SFT loss can look healthy while the model is
   useless at serve time.

<details>
<summary>Answers</summary>

1. When adapters plateau on a large domain shift, when you changed
   the tokenizer, or when you have the memory and enough data that
   full updates are worth the checkpoint size.
2. The scale of the LoRA update added to the frozen weight. Some
   trainers default `α = r`, others `α = 2r`. The multiplier is the
   actual hyperparameter.
3. So the gradient teaches the assistant completion, not the user's
   wording. Otherwise the model spends capacity modeling prompts.
4. The frozen base (commonly 4-bit NF4). LoRA weights and the
   backward of the adapter stay in 16-bit.
5. Train/serve template mismatch; eos never in targets; eval set
   leaked into train; you loaded the base without the adapter.

</details>
