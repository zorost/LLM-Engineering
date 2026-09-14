# S5 · Preference alignment

## Why it exists

SFT teaches "what an answer looks like." Preference training teaches
**which** answer to prefer when several look like answers. Chat
models that refuse too much, ramble, or fail a rubric usually need
this stage, or better data, not a larger LoRA rank.

## The idea

### The stack, in order

1. Start from an SFT model that already speaks your template.
2. Collect **preferences**: for a prompt, a winner and a loser, or a
   scalar score, or a group of samples with rewards.
3. Update the policy so winners become more likely, with a tether to
   the SFT model so it does not collapse into reward hacking.

Offline methods (DPO and cousins) train on a frozen pair dataset.
Online methods (PPO, GRPO) sample from the current policy, score,
update. Online is more expensive and more powerful when the reward
is **verifiable** (unit tests, math, a compiler).

### Rejection sampling, again

Same idea as S3, now as an alignment step: sample n from the SFT
model, score, keep the best as new SFT data (**RAFT**-style) or as
preferred pairs. Do this before you stand up a reward model. It is
often enough for style and for easy code.

### Reward models and PPO

Classic RLHF (InstructGPT):

1. Humans rank completions.
2. A **reward model** (RM) learns to predict those ranks (pairwise
   Bradley-Terry is the usual loss).
3. **PPO** treats the SFT model as a policy. It samples, the RM
   scores, a **value model** estimates advantages, PPO clips the
   update. A **KL penalty** toward a frozen **reference** (usually
   SFT) stops the policy from drifting into gibberish that fools
   the RM.

Four networks in the naive picture: policy, reference, RM, value.
VRAM and engineering cost are why the field spent 2023 to 2025
trying to delete pieces.

**RLAIF** replaces the human ranker with a judge model (and a
constitution, in the Anthropic lineage). Cheaper, biased by the
judge. Treat the judge as a noisy annotator. Calibrate it on a
human slice.

### DPO and the offline family

**DPO** (Direct Preference Optimization) skips the RM and the RL
loop. Given a pair (winner, loser), it raises the log-odds of the
winner vs the loser relative to the reference model. The closed form
is a classification loss on those implicit rewards. Lab 06 is that
loss on toy pairs.

DPO needs **contrastive pairs**, not only gold answers. Pairs that
are too close teach nothing. Pairs that are too far teach "be
different," not "be better." The reference model should be the SFT
checkpoint you actually serve from, not a random base.

Cousins, in one line each:

| Method | What it changes |
|---|---|
| **DPO** | Pairwise logistic on implicit rewards vs a reference |
| **IPO** | Squared loss toward a target gap; less collapse when pairs are easy |
| **KTO** | Does not need pairs. Uses binary desirable / undesirable flags (Kahneman-Tversky-inspired) |
| **ORPO** | Odds-ratio term **on top of SFT**. No separate reference model. One stage |

IPO (Azar et al.) is the "DPO overfits easy pairs" fix. KTO is the
"we only have thumbs up/down" fix. ORPO is the "I do not want two
stages" fix, with a smaller literature and a different failure
surface. None of them is "RL." They are preference losses.

### GRPO and reasoning

**GRPO** (Group Relative Policy Optimization, DeepSeekMath, then
DeepSeek-R1) deletes the value model. For each prompt, sample a
**group** of completions, score each (usually a **verifiable**
reward: correct answer, tests passed, format), and set advantages
relative to the **group mean**. Policy gradient with that baseline.
KL to reference still exists.

This is why 2025 reasoning recipes talk GRPO more than PPO: no
critic, group sampling matches "try n solutions," and math/code
rewards are cheap to compute. Chat style with a fuzzy RM is still
often DPO or PPO.

**Reasoning vs chat is a data-and-reward choice, not a new
architecture.** Chat DPO on "which reply is nicer" will not create
chain-of-thought that survives a contest. GRPO on a verifier, with
long rollouts, can. The reverse is also true: a math RL model can
become a worse general assistant if you never mix chat data. S9
picks up process rewards, MCTS, and test-time compute. This module
is the trainer.

### Frameworks

- **TRL**: `DPOTrainer`, `ORPOTrainer`, `KTOTrainer`, `PPOTrainer`,
  `GRPOTrainer`. Right starting point. Online GRPO wants a fast
  sampler (vLLM) beside the trainer.
- **[verl](https://github.com/verl-project/verl)** (ByteDance Seed,
  HybridFlow): Ray, splits actor / rollout / reference, Megatron
  for huge MoE. The library people reach for when GRPO must scale.
- **[OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)**: Ray + vLLM,
  PPO/GRPO/REINFORCE++ family, production-shaped.

Read one TRL trainer through before you clone verl. The algorithm
is small. The distributed sampler is the product.

Reward hacking is the constant: the RM loves a phrase, the policy
repeats it. Length bias, emoji, fake citations. Watch **win rate
on a frozen human or held-out judge set**, not only the training
reward. Clip KL. Keep a slice of SFT mixed in if chat quality
falls off a cliff.

## The gap most roadmaps leave

They list RLHF, then paste a DPO notebook, then stop. The missing
split:

| Job | Method that usually fits |
|---|---|
| Style, tone, "this reply not that" | DPO / IPO / KTO / ORPO |
| Verifiable math, code, format | GRPO (or PPO) with a function reward |
| You have only thumbs | KTO, or build pairs first |
| You cannot host four models | DPO or ORPO, not PPO |
| You need DeepSeek-R1-like reasoning | SFT on traces, then GRPO; see S9 |

Also missing: the reference model is a first-class artifact. Change
SFT and you must redo preference training or accept drift.

## Practice

Lab `notebooks/06_dpo_loss.ipynb`. Change the beta (KL-ish scale)
and a pair that is too easy. Watch the loss look perfect while the
policy would collapse.

On paper, pick one product behavior (shorter answers, stricter
JSON, better GSM-style math). Write whether you need pairs, a
verifier, or an RM, and which trainer that implies. Do not start
from "we should do PPO" because a blog did.

## Watch and read

- Hugging Face, [TRL](https://huggingface.co/docs/trl), [LLM course, alignment](https://huggingface.co/learn/llm-course)
- Lilian Weng, [RLHF](https://lilianweng.github.io/posts/2023-01-27-rlhf/)
- Ouyang et al., [InstructGPT](https://arxiv.org/abs/2203.02155); Bai et al., [Constitutional AI](https://arxiv.org/abs/2212.08073); [RLAIF](https://arxiv.org/abs/2309.00267)
- Rafailov et al., [DPO](https://arxiv.org/abs/2305.18290); Azar et al., [IPO](https://arxiv.org/abs/2310.12036); Ethayarajh et al., [KTO](https://arxiv.org/abs/2402.01306); Hong et al., [ORPO](https://arxiv.org/abs/2403.07691)
- Shao et al., [DeepSeekMath / GRPO](https://arxiv.org/abs/2402.03300); [DeepSeek-R1](https://arxiv.org/abs/2501.12948)
- [verl](https://github.com/verl-project/verl), [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)
- Stanford CS336, alignment lectures
- Sebastian Raschka, preference-tuning notes on his magazine and GitHub

## Knowledge check

1. What does DPO use instead of a reward model?
2. When is GRPO a better default than PPO?
3. What problem is IPO aimed at relative to DPO?
4. Why keep a KL tether (or a reference) at all?
5. Why does chat-preference DPO fail as a plan for contest math?

<details>
<summary>Answers</summary>

1. An implicit reward from the policy's log-probabilities relative
   to a frozen reference, trained on winner/loser pairs.
2. When you can score a group of samples with a cheap verifier and
   you want to drop the value network. Math, code, format.
3. Overfitting very easy pairs; IPO's squared objective targets a
   gap instead of driving the logistic to extremes.
4. Without it the policy chases the reward or the pair loss into
   repetitive, high-reward nonsense. The reference is the SFT
   dialect you still need.
5. The preference data and reward are about style, not about a
   checkable solution. You need verifiable rewards and long
   rollouts (GRPO, S9), or at least traces in SFT.

</details>
