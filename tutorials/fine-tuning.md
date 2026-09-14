# Tutorial · Fine-tuning

## Why it exists

Fine-tuning is the most over-requested move in L1. This note is how
labs 04 and 05 should leave you: respectful of chat templates, able
to count LoRA parameters, and unwilling to start an SFT run without
a frozen eval.

## The idea

**Supervised fine-tuning (SFT)** continues next-token prediction on
**instruction-response** pairs (and often on full conversations).
The model is not "taught facts" in the school sense. It is shifted
toward a format, a tone, a tool schema, or a local dialect. Facts
that change still belong in retrieval (E3) unless you are willing
to retrain when they change.

Two objects decide whether SFT works:

1. **The chat template.** If training strings omit the end-of-turn
   token that serving will emit, the model never learns to stop.
   Lab 04 exists because this bug eats weeks. Train and serve with
   the **same** template file.
2. **The data.** Duplicates, leaked eval items, and "assistant"
   text that is actually the user: S3. A hundred clean examples of
   the target format beat ten thousand scraped chats.

**LoRA** freezes the base weights and learns low-rank adapters on
chosen matrices (often attention projections). Rank `r` and scaling
`alpha` set capacity. Lab 05 is shapes and parameter counts, not a
full trainer. **QLoRA** stores the base in 4-bit and computes in a
higher precision, so a 7B adapter run fits on a single consumer GPU.
Full fine-tuning updates all weights and needs a memory story from
F5.

Preference methods (DPO, PPO, GRPO) come **after** a competent SFT,
usually. Lab 06 is the DPO loss on toy pairs. Do not start there.

Unsloth, TRL, and Axolotl are trainers and accelerators
([TOOLS.md](../reference/TOOLS.md)). This tutorial does not pick a
winner. It picks the invariants: template, data, eval, rank, and
whether you needed this rung at all (L1).

## The gap most tutorials leave

Colab "fine-tune Llama in 15 minutes" hides the template, hides the
eval, and fine-tunes on a dataset that contains the benchmark. You
will get a screenshot and a contaminated score.

## How the labs should feel

**Lab 04.** You construct a conversation with and without the end
token. Loss looks fine both ways. Generation does not. That
discomfort is the lesson.

**Lab 05.** You compute how many parameters a LoRA of rank `r` adds
on a linear layer of size `d × d`. You change `r` and watch the
count move. You should be able to say why `r=8` on attention is a
different budget from `r=64` on every linear.

Neither lab trains a 7B. CPU-first means the **idea** runs. A later
optional GPU run is going further, not the exam.

## Practice

1. `04_chat_templates.ipynb` then `05_lora_shapes.ipynb`.
2. Read one public SFT dataset card. Write: license, likely
   contamination risk, and whether the template is specified.
3. Only if you have a GPU and a license: run a **tiny** LoRA (for
   example 0.5B to 1B class) with TRL or Unsloth on a dataset you
   actually read, and evaluate on a held-out set you froze first.
   If you cannot freeze an eval, do not train.

## Watch and read

- Hugging Face TRL SFT docs; Unsloth docs for the accelerator path
- LoRA paper, Hu et al., 2021, [arXiv:2106.09685](https://arxiv.org/abs/2106.09685)
- QLoRA, Dettmers et al., 2023, [arXiv:2305.14314](https://arxiv.org/abs/2305.14314)
- Hamel Husain, Mastering LLMs (fine-tuning weeks)
- Raschka, *Build a Large Language Model (From Scratch)*,
  instruction-finetuning chapters
- S4 in this course

## Knowledge check

1. What failure does a missing end-of-turn token cause at
   generation time?
2. When is LoRA the wrong tool because RAG is the right one?
3. What does rank `r` buy you, and what does it cost?
4. Why freeze the eval set before the first SFT epoch?
5. Why does this course run LoRA **shapes** on CPU instead of a
   7B Colab?

<details>
<summary>Answers</summary>

1. The model does not learn to emit the stop token in that
   template, so it rambles, wraps, or continues into a fake user
   turn.
2. When the missing skill is current or private facts. Weights
   will be stale the day after training.
3. Capacity to fit the adaptation. Cost: more trained parameters,
   more adapter memory at train and (if not merged) at serve, and
   a higher chance of overfitting a small set.
4. Because you will otherwise tune on it and report a score you
   cannot rerun honestly.
5. Because the idea (template, rank, parameter count) does not
   require 7B, and Colab links rot. Optional GPU is going further.

</details>
