# S9 · Reasoning and test-time compute

## Why it exists

2024 chat SFT taught models to **sound** helpful. 2025 made a second
axis obvious: spend more **decode-time compute** (longer traces,
search, verifiers) on problems that have a checkable answer. If you
treat "reasoning models" as a new architecture, you will buy the
wrong GPU and skip the reward.

## The idea

### Two public recipes

**o1-style** (OpenAI's public description): train a model to produce
a long hidden chain of thought, use **reinforcement learning** so
that chains which reach correct answers are reinforced, and at
inference **sample more thinking** when the user wants a harder
problem. The product knob is test-time compute. The weights still
look like a decoder-only Transformer (S1).

**DeepSeek-R1-style** ([paper](https://arxiv.org/abs/2501.12948)):
publish the recipe. Start from a base (or a lightly mid-trained)
model, run **large-scale RL** with **verifiable rewards** (math,
code, format), often **GRPO** (S5), sometimes after a cold-start
SFT on traces. **R1-Zero** is the "RL on the base, almost no SFT"
ablation. Distill the resulting traces into smaller models (S10).
The open lesson is not a secret architecture. It is **RL plus
verifiers plus long rollouts**, then distillation.

Both families still next-token-predict. They differ in data,
reward, and how much they roll out before they emit the user-facing
answer.

### Outcome rewards vs process rewards

An **outcome reward** scores the final answer: match the number,
tests pass, format valid. Cheap. Credit assignment is brutal: a
200-step trace gets one bit. GRPO with group baselines is the
standard way to live with that (S5).

A **process reward** scores **steps**. A **PRM** (process reward
model) is trained on annotated or automatically labeled steps
("this line is still correct"). OpenAI's
[Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) is
the canonical paper: process supervision can beat outcome
supervision per bit of label, on math.

PRMs are expensive to label and they can be gamed (a fluent wrong
step). Outcome RL with enough samples is often the thing that
actually shipped in 2025 open recipes. PRMs still matter for
**search**: they score partial trees.

### Search: MCTS and friends

If you can score a partial or complete solution, you can **search**:

- Sample n independent traces (best-of-n). This **is** test-time
  compute. Diminishing returns, easy to implement.
- Beam or tree over steps, with a PRM or a verifier at nodes.
- **MCTS** (Monte Carlo Tree Search): expand promising steps,
  roll out, back up values. AlphaGo-shaped. Costly. Shows up in
  papers more than in cheap serving paths.

Search does not replace RL. RL changes the policy so that a short
search finds better traces. Search on a weak policy burns tokens
for style.

### Test-time compute scaling

[Snell et al.](https://arxiv.org/abs/2408.03314) and the o1 release
notes the same curve: for some tasks, extra **inference** FLOPs
(longer chains, more samples, more search) buy more accuracy than
the same FLOPs spent on a larger pretrained model. That statement
has a domain: contest math, code, puzzles with verifiers. It is
weaker on "write a polite email."

Practical knobs:

| Knob | What you spend |
|---|---|
| Max think / max tokens | latency and money, always |
| Temperature on the trace | diversity of attempts |
| n samples + verifier | n times the decode, then pick |
| PRM-guided beam / MCTS | memory, implementation, a PRM |
| User-facing short answer | hide the trace or show a summary |

The KV cache of a 32k-token thought is an operator bill (O3, lab
18). GQA/MLA (S1) and spec decoding (S10) are how you survive it.

Do not confuse **chain-of-thought prompting** (E1) with a reasoning
model. Prompting a 7B chat model to "think step by step" is a
decode policy. An R1-class model was **optimized** so that those
tokens are worth generating. You still eval both with task
checkers (S6: LiveCodeBench, contest sets, your own tests), not
with MMLU alone.

### What to train, in order

1. Decontaminated SFT on **traces that reach correct answers**
   (optional cold start).
2. RL with a **function reward** (GRPO) on a curriculum the
   verifier can grade.
3. Mix chat / refusal data if you still need an assistant (S5).
4. Distill to the size you can serve (S10).
5. At serve time, expose a think budget the product can afford.

If you cannot write the verifier, you do not have this loop. You
have chat DPO with longer outputs, which is a different (worse)
plan for math.

## The gap most roadmaps leave

They add "o1" to the trends slide next to LLaVA. Missing:

- Architecture unchanged; **reward and rollout** changed.
- Outcome vs process rewards as a labeling budget.
- Test-time compute as a **scaling law you choose**, with a bill.
- GRPO as the open trainer (S5), distillation as the deploy
  step (S10).

## Practice

No required lab in this track (lab 16 is speculation, S10). On
paper:

1. Pick a task you can grade with code (a tiny GSM-like set, unit
   tests). Write an outcome reward in one paragraph.
2. Estimate tokens if you sample n=8 traces at 2k tokens vs n=1
   at 256. Use lab 13's cost sketch.
3. Decide whether a PRM is worth labeling, or whether best-of-n
   plus GRPO later is the honest next step.

Do not scrape hidden chain-of-thought from a hosted API if the
terms forbid it. Train on public traces (R1 distill data, your
own verifier loop) or do not train.

## Watch and read

- OpenAI, [Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/) (o1 system card / blog)
- DeepSeek, [R1](https://arxiv.org/abs/2501.12948); [DeepSeekMath / GRPO](https://arxiv.org/abs/2402.03300)
- Lightman et al., [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050)
- Snell et al., [Scaling LLM test-time compute](https://arxiv.org/abs/2408.03314)
- Stanford CS336, post-training / reasoning lectures when present in the current playlist
- Hugging Face, GRPO / R1 reproduction notes in [TRL](https://huggingface.co/docs/trl) and the [LLM course](https://huggingface.co/learn/llm-course)
- Lilian Weng, [RLHF](https://lilianweng.github.io/posts/2023-01-27-rlhf/) as the precursor
- Karpathy, Deep Dive (reasoning / thinking sections if you are on the 2025 video)

## Knowledge check

1. What stayed the same between a 2024 chat model and an o1-style
   model at the architecture level?
2. Outcome reward vs process reward: who assigns credit?
3. Why did open recipes lean on GRPO for reasoning RL?
4. When does extra test-time compute beat training a larger model?
5. Why is "just prompt it to think" not the same as R1-style
   training?

<details>
<summary>Answers</summary>

1. Decoder-only Transformer, next-token loss, KV cache. The
   change is data, RL, and how long they decode.
2. Outcome: one score at the end. Process: scores on steps (a
   PRM or a step checker), so a wrong line can be blamed.
3. Verifiable group scores replace a learned critic; sampling a
   group matches "try several solutions"; memory is lower than
   PPO with a value model.
4. On checkable hard tasks, in a window where more samples or
   longer traces still raise accuracy. Not on generic chitchat,
   and not once the verifier is saturated.
5. Prompting does not change weights. R1-style RL changes the
   policy so long traces are an optimized skill, then you still
   spend test-time compute on purpose.

</details>
