# S8 · Merging and multimodal

## Why it exists

Public roadmaps used to dump merging, images, interpretability, and
test-time compute into one "new trends" slide. Those are four jobs.
This module is **weight merging** and **vision-language adapters**.
Reasoning and test-time compute are [S9](09-reasoning-and-test-time.md).
Distillation and draft models are [S10](10-distillation-and-speculation.md).
Interpretability is [S12](12-interpretability.md). Hybrids and MoE
already live in [S1](01-architecture.md).

## The idea

### Merging is arithmetic on checkpoints

If two models share an architecture and a tokenizer, their weights
are vectors in the same space. **Merging** interpolates those
vectors so one file behaves a bit like both parents: a code LoRA
plus a chat SFT, two DPO runs, a base plus an instruct.

This is **not** MoE (no router at runtime). It is **not**
distillation (no teacher logits). It is cheap. It also fails
silently when tokenizers drift or when you merge an instruct head
onto a base that never saw the template.

**[mergekit](https://github.com/arcee-ai/mergekit)** is the tool
that made this a YAML job. Read the YAML. The method name is the
idea.

### SLERP, TIES, DARE

- **SLERP** (spherical linear interpolation): walk the great circle
  between two weight tensors instead of a naive average. Two-parent
  merges. Better than lerp when the tensors are not colinear. Does
  not magically merge five specialists.
- **TIES** ([paper](https://arxiv.org/abs/2306.01708)): trim small
  changes, elect a **sign** per parameter so models do not cancel,
  then merge. Built for several task vectors (finetune minus base).
- **DARE** ([paper](https://arxiv.org/abs/2311.03099)): randomly
  **drop** a large fraction of fine-tune deltas and **rescale** the
  rest. The claim is that task vectors are redundant; sparsifying
  them reduces interference before you add them back to the base.

People stack DARE then TIES then a SLERP, because mergekit lets
them. That stack is an experiment, not a theory. Always eval (S6)
against each parent and against the product suite. A merge that
wins a vibe check and loses IFEval is a worse model.

Linear **model soups** (average of several finetunes) still work
when the runs are siblings. TIES/DARE are for **different tasks**
on the same base.

Licenses compose (S11). Merging Llama with Gemma is an architecture
error and a legal headache. Merging two Apache checkpoints is still
a card you must write.

### Multimodal: CLIP, then a projector, then LLaVA

A decoder-only LLM does not take pixels. The open recipe that
stuck:

1. **CLIP** ([paper](https://arxiv.org/abs/2103.00020)) trains an
   image encoder and a text encoder so paired captions match in
   embedding space. The image encoder is the frozen (or later
   unfrozen) **vision backbone**.
2. A thin **projector** (MLP) maps vision tokens into the LLM's
   embedding width.
3. **LLaVA** ([paper](https://arxiv.org/abs/2304.08485)) connects
   those tokens as a prefix (or interleaved tokens) and SFT on
   image-instruction data: "describe," "reason about the chart,"
   "OCR this."

Training usually stages: freeze the LLM and CLIP, train the
projector; then LoRA the LLM; optionally unfreeze more of the
vision tower. Native multimodal models (Gemma, Qwen-VL, Llama
vision variants) hide this as one card. The wiring is still
"vision tokens enter the residual stream."

What breaks:

- Resolution and tiling. A 224 CLIP was not built for a 4k UI
  screenshot. Later LLaVA-style recipes tile or use dynamic
  resolution. If your product is documents, ask what the encoder
  actually sees.
- Token budget. A picture can cost hundreds of tokens. Context
  math from F5 still applies.
- Hallucinated objects. Eval with grounded tasks (OCR exact match,
  chart number check), not with "the caption sounded nice."
- Audio and video are the same pattern with a different encoder.
  Do not invent a new religion per modality.

You do not need to train CLIP from scratch. You do need to know
whether the projector was trained on **your** image domain.

### What is left, and what is not this file

Still in the junk drawer until they earn a module (see
[ROADMAP.md](../../ROADMAP.md)):

- **Continued pre-training / mid-training** on domain text before
  SFT. Same loop as S2, smaller. Often a better first move than
  a merge.
- **Discrete diffusion** language models, if you serve them. Not
  a 2026 default job.
- **Tool-special tokens** and fill-in-the-middle. Data and template
  work (S3, E9), not a merge.

Explicitly elsewhere: SSM hybrids (S1), GRPO and test-time (S9),
EAGLE and MTP (S10), SAEs and steering (S12). If a slide says
"trends 2025" and lists all of those, it is the document this
course refused to ship.

## The gap most roadmaps leave

One bucket. One Colab for "franken-merge." One demo of LLaVA.
Missing:

- Merging as **task-vector arithmetic** with an eval duty.
- Tokenizer and license as merge preconditions.
- Multimodal as CLIP + projector + SFT, with token cost.
- A clean split so interpretability and o1-style compute do not
  hide here.

## Practice

No required lab. Do this on paper:

1. Two public Apache (or otherwise shippable) siblings on the same
   base: write a mergekit-style plan (SLERP vs TIES vs DARE) and
   the suite that would kill the merge.
2. For a screenshot-heavy product, estimate vision tokens per
   page at the encoder's resolution and whether they fit your
   context (lab 13).

Optional: run mergekit on two tiny same-arch checkpoints you own
and compare five prompts plus a tiny IFEval-style constraint. Skip
any weight whose card you cannot license (S11).

## Watch and read

- [mergekit](https://github.com/arcee-ai/mergekit)
- Yadav et al., [TIES-Merging](https://arxiv.org/abs/2306.01708); Yu et al., [DARE](https://arxiv.org/abs/2311.03099)
- Radford et al., [CLIP](https://arxiv.org/abs/2103.00020); Liu et al., [LLaVA](https://arxiv.org/abs/2304.08485)
- Hugging Face, vision-language and merge docs; [LLM course](https://huggingface.co/learn/llm-course)
- Stanford CS336, remaining lectures on multimodality if posted in the current year
- Lilian Weng, contrastive / CLIP notes in the transformer-family posts

## Knowledge check

1. How does a merge differ from a MoE?
2. What does TIES do that a uniform average does not?
3. Why is DARE a sparsify-and-rescale of **deltas**, not of the
   full weights?
4. What three pieces does a LLaVA-style model add on top of a
   text LLM?
5. Why are interpretability and test-time compute not in this
   module?

<details>
<summary>Answers</summary>

1. A merge is a static combination of weights. MoE routes among
   experts at runtime and pays communication for that choice.
2. It trims small task-vector entries and resolves sign conflicts
   so models trained on different tasks cancel less.
3. The interesting signal is finetune minus base. Dropping and
   rescaling that delta reduces interference; sparsifying the
   whole checkpoint would destroy the pretrained features.
4. A vision encoder (often CLIP-class), a projector into the LLM
   width, and instruction data that includes images.
5. They are full topics with their own trainers, evals, and
   failure modes: S9 and S12. Leaving them here recreates the
   junk-drawer roadmap.

</details>
