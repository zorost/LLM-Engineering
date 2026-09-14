# Papers

Title, year, why it matters for this course, arXiv (or the
canonical PDF when there is no arXiv). Read the PDF when the
module names it. Do not cite a thread.

arXiv links use `https://arxiv.org/abs/<id>`.

---

## Architecture and bases

**Attention Is All You Need.** Vaswani, Shazeer, Parmar, Uszkoreit,
Jones, Gomez, Kaiser, Polosukhin. 2017.
[arXiv:1706.03762](https://arxiv.org/abs/1706.03762).
Why: the Transformer. Everything in S1 is a footnote to this
wiring. Read it once after lab 02.

**Language Models are Unsupervised Multitask Learners** (GPT-2).
Radford, Wu, Child, Luan, Amodei, Sutskever. 2019. OpenAI report
(not an arXiv preprint):
[PDF](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf).
Why: GPT-2 showed that a decoder trained on web text does many
NLP tasks without a new head. The product path from "language
model" to "general model" starts here.

**Language Models are Few-Shot Learners** (GPT-3). Brown et al.
2020. [arXiv:2005.14165](https://arxiv.org/abs/2005.14165).
Why: in-context learning at scale, and the size jump that made
prompting a job. S2 and E1.

**Llama 2: Open Foundation and Fine-Tuned Chat Models.** Touvron
et al. 2023. [arXiv:2307.09288](https://arxiv.org/abs/2307.09288).
Why: the open-weights recipe a generation of engineers actually
served: pretrain, SFT, preference, GQA, a usable card. S2, S4,
S11, O1.

**The Llama 3 Herd of Models.** Grattafiori (Dubey) et al. 2024.
[arXiv:2407.21783](https://arxiv.org/abs/2407.21783).
Why: the 2024 open-weights default: data mix, post-training,
multilingual, MoE in the larger herd. Read the card next to the
paper. S1, S2, S11.

**RoFormer: Enhanced Transformer with Rotary Position Embedding.**
Su, Lu, Pan, Wen, Liu. 2021 (RoPE).
[arXiv:2104.09864](https://arxiv.org/abs/2104.09864).
Why: relative position by rotating Q and K. Default in Llama-
family models. S1.

**GQA: Training Generalized Multi-Query Transformer Models from
Multi-Head Checkpoints.** Ainslie, Lee-Thorp, de Jong, Zemlyanskiy,
Lebrón, Sanghai. 2023. [arXiv:2305.13245](https://arxiv.org/abs/2305.13245).
Why: grouped-query attention, the KV-cache shrink operators live
on. S1, O1, lab 18.

**FlashAttention: Fast and Memory-Efficient Exact Attention with
IO-Awareness.** Dao, Fu, Ermon, Rudra, Ré. 2022.
[arXiv:2205.14135](https://arxiv.org/abs/2205.14135).
Why: attention as an IO problem. E6. FlashAttention-2 is
[arXiv:2307.08691](https://arxiv.org/abs/2307.08691) if you
implement kernels.

---

## Post-training and preference

**Training language models to follow instructions with human
feedback** (InstructGPT). Ouyang et al. 2022.
[arXiv:2203.02155](https://arxiv.org/abs/2203.02155).
Why: SFT plus PPO-style RLHF as a public recipe. Chat models as
a product. S3, S5.

**LoRA: Low-Rank Adaptation of Large Language Models.** Hu et al.
2021. [arXiv:2106.09685](https://arxiv.org/abs/2106.09685).
Why: adapters you can actually train. Lab 05, S4.

**QLoRA: Efficient Finetuning of Quantized LLMs.** Dettmers,
Pagnoni, Holtzman, Zettlemoyer. 2023.
[arXiv:2305.14314](https://arxiv.org/abs/2305.14314).
Why: 4-bit base plus LoRA on a single GPU. S4, S7.

**Direct Preference Optimization: Your Language Model is Secretly
a Reward Model.** Rafailov et al. 2023.
[arXiv:2305.18290](https://arxiv.org/abs/2305.18290).
Why: preference without a separate RL loop. Lab 06, S5.

**Proximal Policy Optimization Algorithms.** Schulman, Wolski,
Dhariwal, Radford, Klimov. 2017.
[arXiv:1707.06347](https://arxiv.org/abs/1707.06347).
Why: the RL algorithm InstructGPT stood on. Read this after
InstructGPT, not before you understand SFT.

**DeepSeekMath: Pushing the Limits of Mathematical Reasoning in
Open Language Models.** Shao et al. 2024. (GRPO)
[arXiv:2402.03300](https://arxiv.org/abs/2402.03300).
Why: group relative policy optimization as a practical RL recipe
for reasoning. S5, S9.

**DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via
Reinforcement Learning.** DeepSeek-AI. 2025.
[arXiv:2501.12948](https://arxiv.org/abs/2501.12948).
Why: reasoning models as a 2025 default, not a demo. S9. Read
next to DeepSeekMath, not instead of it.

---

## Quantization

**GPTQ: Accurate Post-Training Quantization for Generative
Pre-trained Transformers.** Frantar, Ashkboos, Hoefler, Alistarh.
2022. [arXiv:2210.17323](https://arxiv.org/abs/2210.17323).
Why: 4-bit GPU serving with calibration. S7, O1.

**AWQ: Activation-aware Weight Quantization for LLM Compression
and Acceleration.** Lin et al. 2023.
[arXiv:2306.00978](https://arxiv.org/abs/2306.00978).
Why: protect salient weights. The other 4-bit citizen next to
GPTQ. S7.

---

## Retrieval, agents, test-time

**Retrieval-Augmented Generation for Knowledge-Intensive NLP
Tasks.** Lewis et al. 2020.
[arXiv:2005.11401](https://arxiv.org/abs/2005.11401).
Why: generate from retrieved documents. E3, lab 08. The 2020
paper is the name. Your production RAG is hybrid search plus
evals.

**ReAct: Synergizing Reasoning and Acting in Language Models.**
Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao. 2022.
[arXiv:2210.03629](https://arxiv.org/abs/2210.03629).
Why: thought-action-observation. Lab 10, E5. The loop is the
idea. The framework is later.

**Scaling LLM Test-Time Compute Optimally can be More Effective
than Scaling Model Parameters.** Snell, Lee, Xu, Kumar. 2024.
[arXiv:2408.03314](https://arxiv.org/abs/2408.03314).
Why: spend compute at decode on purpose. S9, O3 (because that
spend is a bill).

**Tree of Thoughts: Deliberate Problem Solving with Large
Language Models.** Yao et al. 2023.
[arXiv:2305.10601](https://arxiv.org/abs/2305.10601).
Why: search over intermediate thoughts. A readable test-time
search paper before you reach MCTS variants.

**Language Agent Tree Search Unifies Reasoning, Acting, and
Planning in Language Models** (LATS). Zhou et al. 2023.
[arXiv:2310.04406](https://arxiv.org/abs/2310.04406).
Why: MCTS-style search wrapped around an LLM agent. S9. Classic
MCTS itself is not an LLM paper; start from AlphaGo (Silver et
al., Nature 2016) only if you need the planning backbone.

---

## Also cited in modules (short)

| Paper | Year | arXiv | Module |
|---|---|---|---|
| Efficient Memory Management… PagedAttention (vLLM) | 2023 | [2309.06135](https://arxiv.org/abs/2309.06135) | O1 |
| Fast Inference via Speculative Decoding | 2022 | [2211.17192](https://arxiv.org/abs/2211.17192) | S10, lab 16 |
| The Curious Case of Neural Text Degeneration (nucleus) | 2019 | [1904.09751](https://arxiv.org/abs/1904.09751) | lab 03 |
| Neural Machine Translation of Rare Words with Subword Units (BPE) | 2016 | [1508.07909](https://arxiv.org/abs/1508.07909) | lab 01 |
| Scaling Laws for Neural Language Models (Kaplan et al.) | 2020 | [2001.08361](https://arxiv.org/abs/2001.08361) | F5, lab 19 |
| Training Compute-Optimal LLMs (Chinchilla / Hoffmann et al.) | 2022 | [2203.15556](https://arxiv.org/abs/2203.15556) | F5 |

Add a paper with an issue if a working engineer needs it and it
is not a tweet.
