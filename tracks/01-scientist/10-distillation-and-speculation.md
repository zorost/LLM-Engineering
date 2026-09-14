# S10 · Distillation and speculative decoding

## Why it exists

A 70B reasoner that you cannot serve is a paper. Distillation copies
behavior into a smaller policy. Speculative decoding copies **work**
onto a cheap drafter so the big model verifies several tokens at
once. Both are systems for **cost**, not new intelligence.

## The idea

### Distillation

Classic **knowledge distillation** (Hinton et al.): a student
matches a teacher's distribution (soft logits), not only hard
labels. In LLMs the common forms are:

- **On-policy / trace distillation**: the teacher generates
  completions (or hidden traces, S9). You SFT the student on those
  strings. DeepSeek-R1 distilled into Qwen/Llama-sized students
  this way. Easy. The student copies style and some skill. It does
  not automatically copy the teacher's full distribution.
- **Logit / KL distillation**: student minimizes KL to teacher
  token distributions on a prefix corpus. Closer to classic KD.
  Needs teacher forward passes, not only text. Heavier.
- **On-policy KD**: student samples, teacher scores those prefixes,
  so the student is not only imitating a frozen teacher corpus.

SFT on teacher text is the default you can actually run. Treat it
as S4 with a synthetic corpus whose license you must read (S11).
Teacher outputs are often **not** free to use for competing models.
The card and the terms win.

Distillation is also how MoE giants become dense servers, and how
a reasoning RL run becomes a 7B that still thinks. Eval the
student as a **new model** (S6). Do not inherit the teacher's
leaderboard screenshot.

### Speculative decoding

Autoregressive decode is memory-bound (F5): one token, a full
weight read. **Speculative decoding** (Leviathan et al.,
[2211.17192](https://arxiv.org/abs/2211.17192); Chen et al.,
DeepMind speculative sampling) uses a cheap **draft** to propose
k tokens. The **target** model then scores those k prefixes **in
parallel** (one forward with a k-token query, still using the
cache). A rejection sampler accepts a prefix that the target
would have sampled, and resamples at the first mismatch.

If the draft is good, you accept several tokens per expensive
forward. If the draft is bad, you fall back to roughly the
baseline cost plus overhead. The **output distribution matches the
target** when the algorithm is implemented correctly. That is the
point. You are not approximating the big model with the small one.
You are using the small one as a proposal.

Lab 16 is draft-and-verify on a toy alphabet. The acceptance rate
is the product metric. Domain shift (code vs chat) kills it.

### Draft models

A draft can be:

- A **smaller sibling** (1B draft for 70B target) trained on the
  same tokenizer. Simplest. Quality gap vs speed is the trade.
- A **pruned or distilled** copy of the target.
- **Heads on the target itself** that predict extra tokens
  (Medusa-style). No second model to host, extra training.

Tokenizer mismatch is fatal. Architecture mismatch is painful.
Keep drafts in the same family.

Batch size matters. Speculation shines at **small batch** (chat,
low QPS) where decode is memory-bound. At huge batches the GPU
is already compute-busy and the extra draft work can lose.
Measure on your QPS, not on a blog's batch-1 graph.

### EAGLE

**EAGLE** ([arxiv:2401.15077](https://arxiv.org/abs/2401.15077))
drafts at the **feature** level: a lightweight module predicts
the next hidden state (second-to-top layer), then the target's
lm_head turns that into tokens. Later EAGLE-2/3 improve the tree
of draft tokens and training. Serving stacks (vLLM, TensorRT-LLM)
ship EAGLE paths because you avoid a fully separate 1B model,
with a training job for the draft head.

Read EAGLE as "speculative decoding whose draft is a trained
feature predictor," not as a different sampler. You still verify
with the target. You still track acceptance length.

### Multi-token prediction (MTP), as a public concept

Ordinary LMs predict **one** next token. **Multi-token prediction**
trains extra heads (or a joint loss) to predict tokens t+1, t+2,
… given the same backbone state. Gloeckle et al.
([arxiv:2404.19737](https://arxiv.org/abs/2404.19737)) showed
this can improve sample efficiency and give you a natural
**draft** for speculative decoding. DeepSeek-V3's public tech
report uses MTP as an **auxiliary training** objective: extra
heads trained with the main model, then reused to propose tokens
at decode time.

MTP is therefore two things, and you should keep them straight:

1. A **training** loss that asks the network to look further.
2. A **draft mechanism** at inference, in the same family as
   Medusa/EAGLE, often with higher acceptance because the heads
   were co-trained.

This course treats MTP as that public literature. It does not
document private serving recipes or restricted speculators.

### Putting them together

Distill when the **student** must be the policy you serve (edge,
price, a reasoning 7B). Speculate when the **target** must stay
the policy and you need it faster at decode. You can distill a
drafter for a frozen target. You can MTP-train a model so it
brings its own drafter. Quantization (S7) stacks with both.
Engineer-side inference (E6) is where vLLM flags live. This
module is why those flags exist.

## The gap most roadmaps leave

Quantization is the only "make it fast" chapter. Missing:

- Distillation as SFT on teacher traces vs true KD.
- Speculative decoding as **lossless** (distribution-matching)
  acceleration with an acceptance rate.
- EAGLE and MTP as public draft designs, not vendor magic.
- Batch size as the condition where speculation dies.

## Practice

Lab `notebooks/16_speculative_decoding.ipynb`. Change draft
quality and k. Plot accepted tokens per verify. Then write three
sentences: when you would distill a 7B, when you would attach a
1B draft to a 70B, when you would train MTP heads instead.

Going further: read a vLLM speculative-decoding doc and name the
draft it expects. Do not implement a custom kernel here.

## Watch and read

- Hinton et al., [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531)
- Leviathan et al., [Fast Inference via Speculative Decoding](https://arxiv.org/abs/2211.17192)
- Li et al., [EAGLE](https://arxiv.org/abs/2401.15077)
- Gloeckle et al., [Multi-token prediction](https://arxiv.org/abs/2404.19737); DeepSeek-V3 technical report (MTP section)
- Hugging Face / vLLM speculative decoding docs; [LLM course](https://huggingface.co/learn/llm-course)
- Stanford CS336, inference lectures
- Karpathy, Deep Dive (sampling / inference)
- Lab 16 in this repo is the hands-on version

## Knowledge check

1. Why is SFT on teacher traces not the same as KL distillation?
2. What does speculative decoding guarantee when the rejection
   sampler is correct?
3. Why does a tokenizer mismatch kill a draft model?
4. What does EAGLE predict that a 1B sibling draft does not?
5. Name the two roles of MTP in public papers.

<details>
<summary>Answers</summary>

1. Trace SFT matches strings (hard labels). KL distillation
   matches the teacher's full next-token distributions on
   prefixes. The second needs teacher logits.
2. The accepted tokens are distributed as if you had sampled
   the target alone. Speed changes. The policy should not.
3. Draft token ids are not the target's ids. Verification is
   then comparing different languages.
4. Next hidden features (and then tokens via the target head),
   rather than running a separate small LM from scratch.
5. An auxiliary training loss that predicts several future
   tokens, and a built-in draft for speculative decode.

</details>
