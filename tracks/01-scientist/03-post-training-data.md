# S3 · Post-training data

## Why it exists

Pre-training teaches next tokens on a crawl. Post-training teaches a
**conversation contract**: who speaks, when the model should stop, and
what a good answer looks like. Most failed fine-tunes are failed
datasets with a fashionable trainer wrapped around them.

## The idea

### Two JSON dialects

You will meet two on-disk formats. They are not chat templates.

**ShareGPT** (Vicuna-era, still everywhere) is a conversation as a
list of turns with `from` / `value` (or `human` / `gpt`). Tools glued
to that schema. It is a community convention, not a standard.

**OpenAI messages** is a list of objects with `role` and `content`.
Roles are `system`, `user`, `assistant`, and later `tool` /
`function`. Hugging Face datasets, TRL, and almost every 2025 API
client speak this dialect. If you can, store this.

Convert once, at ingest. Do not train from a mix of dialects and hope
the template layer guesses.

### Chat templates are the real string

The model never saw your JSON. It saw a **rendered string** with
special tokens. That render is the **chat template** (Jinja in
Hugging Face `tokenizer.chat_template`).

**ChatML** is the lineage many templates still rhyme with:

```
<|im_start|>system
You are a concise assistant.<|im_end|>
<|im_start|>user
How do I reset the token?<|im_end|>
<|im_start|>assistant
```

Llama, Gemma, Qwen, and Mistral each have their own delimiters. Mix
them and you have taught the model a language it will not see at
serve time. A missing `<|im_end|>` (or the model's `eos`) is why SFT
runs "never stop." Lab 04 exists for that bug.

Rules that save weeks:

1. Train with the **same** `apply_chat_template` you will use in
   vLLM or llama.cpp.
2. Mask loss on tokens the user already typed (S4). The template
   decides where those tokens are.
3. Put the system prompt in the data if the product will send one.
   A model that never saw `system` will ignore it in production.

Hugging Face documents this under
[chat templating](https://huggingface.co/docs/transformers/chat_templating).
Read that page before you collect another 10k rows.

### Where the rows come from

Human labels (ShareGPT dumps, contractor writes, customer tickets
with consent) are expensive and leaky. The 2024 to 2026 default is a
**synthetic pipeline** with a human or model-in-the-loop filter.

[Distilabel](https://github.com/argilla-io/distilabel) is the public
pipeline library: generate, evolve, judge, filter, export. [Argilla](https://github.com/argilla-io/argilla)
is the review UI that sits on top so a person can reject garbage
without writing a new trainer. Together they are a factory, not a
dataset.

**Evol-Instruct** (WizardLM) rewrites a seed instruction to be harder:
add constraints, ask for reasoning, increase depth, then generate a
new target. **Auto-Evol** (and Distilabel's evol pipelines) search
over those rewrite strategies instead of a single handwritten
template. The failure mode is instruction inflation: every prompt
becomes a six-part exam, and the product no longer looks like your
users.

**Rejection sampling** here means: sample n completions from a teacher,
score them (unit tests, a judge model, a rubric), keep the best, drop
the rest. It is a data filter, not yet RL (S5). On math and code it
is the cheapest quality lever you have. On open chat it is as good
as the judge.

### Decontamination

Your SFT set will contain eval items unless you look. Copy-paste from
blogs pulls MMLU stems. Synthetic teachers regurgitate GSM8K. Two
layers:

- **MinHash / LSH** (same family as S2): near-duplicate strings
  against the eval corpus. Fast, catches clones and light edits.
- **Semantic hash** ([semhash](https://github.com/MinishLab/semhash)
  and embedding near-dup): paraphrases that MinHash misses.

Run the filter **against the evals you will quote**, not against a
vague "we deduped." S6 and S11 return to this. A 2-point MMLU bump
that vanishes on a fresh set is contamination, not alignment.

### Curators at scale

When the set is larger than a laptop,
[NeMo Curator](https://github.com/NVIDIA-NeMo/Curator) is the
GPU-accelerated pipeline for load, language ID, quality filter,
exact and fuzzy dedup, PII, and downstream export. Same job as
datatrove, aimed at NVIDIA shops and Ray clusters. Use it for
**volume**. Use Distilabel for **instruction evolution**. Use Argilla
for **human no**.

Also document:

- License of every seed (S11). ShareGPT forks are often not yours
  to ship.
- PII. Tickets and emails do not become instruction data because
  the trainer accepts JSONL.
- A frozen **held-out** conversation set that never enters SFT or
  preference training. That is your real eval, not the leaderboard.

## The gap most roadmaps leave

They paste "use Alpaca" and a Colab. Alpaca is a 2023 synthetic
snapshot with known contamination and a template that is not your
production tokenizer. The missing work is the **contract**:

| Piece | Failure if skipped |
|---|---|
| Messages vs ShareGPT | silent role swaps |
| Chat template = serve template | endless generation, ignored system |
| Evol without a product rubric | verbose exams nobody asked |
| MinHash + semantic decontam | fake leaderboard gains |
| Human review sample | confident garbage at 5% |

## Practice

Lab `notebooks/04_chat_templates.ipynb`. Break it on purpose: drop
the end token, swap Llama delimiters onto a ChatML tokenizer, mask
the wrong span. Then write twenty messages in OpenAI format for a
domain you know, render them with `apply_chat_template`, and read
the raw string. If you would not want that string in the loss, fix
the data, not the rank.

Optional: Distilabel's evol-instruct example on ten seeds. Keep one
row that got worse after evolution so you remember the failure.

## Watch and read

- Hugging Face, [chat templating](https://huggingface.co/docs/transformers/chat_templating), [LLM course, post-training data](https://huggingface.co/learn/llm-course)
- Karpathy, Deep Dive (the post-training / assistant sections)
- Stanford CS336, data and alignment-data lectures
- [Distilabel](https://github.com/argilla-io/distilabel), [Argilla](https://github.com/argilla-io/argilla)
- Xu et al., [WizardLM / Evol-Instruct](https://arxiv.org/abs/2304.12244)
- [semhash](https://github.com/MinishLab/semhash), [NeMo Curator](https://github.com/NVIDIA-NeMo/Curator)
- Lilian Weng, [RLHF](https://lilianweng.github.io/posts/2023-01-27-rlhf/) (the data half, before PPO)

## Knowledge check

1. What is the difference between a messages JSONL and a chat template?
2. Why does a missing end-of-turn token wreck SFT?
3. What does Evol-Instruct change, and what does it tend to overproduce?
4. Why run both MinHash and a semantic near-dup against evals?
5. When is rejection sampling a dataset method rather than RL?

<details>
<summary>Answers</summary>

1. JSONL is storage you own. The template is the tokenizer's rendered
   string with special tokens, which is what the model is trained to
   see and later complete.
2. The model never observes a stop. At inference it keeps going until
   a length cap. Loss on "continue forever" is a data bug.
3. It rewrites instructions to be harder and regenerates answers. It
   overproduces long, exam-like prompts that no longer match users.
4. MinHash catches copies and light edits. Semantic near-dup catches
   paraphrases. Evals leak in both forms.
5. When you sample offline, score, and keep winners as SFT or
   preference pairs. Online RL (S5) updates the policy from rewards
   during training.

</details>
