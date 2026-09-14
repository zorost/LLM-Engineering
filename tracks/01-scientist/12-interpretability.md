# S12 · Interpretability

## Why it exists

Weights are not an explanation. Interpretability is the set of
tools that turn activations into **partial**, testable claims:
this direction tracks that concept; this layer has already
decided the next token; this vector steers a behavior. The
failure mode is a demo that looks like mind-reading and does
not survive a second prompt.

## The idea

### The residual stream is the object

Everything you probe is a vector sitting in the residual stream
(S1), or a linear map of it (logits, SAE latents). Causal
claims need an **intervention**: add, ablate, or replace that
vector and show the output changed in the predicted way.
Visualizing an attention map is not an intervention.

### Logit lens

The **logit lens** (nostalgebraist) applies the final unembedding
to intermediate residual states and reads a distribution over
tokens "as if" that layer were the last. Early layers look like
noise. Later layers often already prefer the answer.

It is a **diagnostic**, not a decoder the model uses. The real
network still has later MLP and attention updates. Use it to
ask "when did the model commit?" on a known prompt. Do not use
it to claim a layer "thinks the answer is Paris."

Tuned lenses (learned maps per layer) reduce the smash of
applying the wrong unembed. Same idea, extra fitting, extra
overfit risk.

### Sparse autoencoders (SAEs)

Activations are **superposed**: many features share dimensions
(dictionary learning / superposition story from the
Anthropic transformer-circuits work). A **sparse autoencoder**
learns an overcomplete dictionary so that a hidden state is a
sparse combination of latents that are easier to name.

[Towards Monosemanticity](https://transformer-circuits.pub/2023/monosemantic-features/index.html)
is the readable starting paper. **SAELens** and Gemma Scope-class
releases are the public artifacts. You will spend more time
**validating** a latent (does it fire on the concept, does
steering it move the concept) than training one.

Limits that belong on every SAE slide:

- A named latent is a correlation until you intervene.
- Dictionaries miss features, split features, and invent
  reconstruction-only features.
- A 16k latent on one layer of one 7B is not a map of cognition.

### Activation steering

If a direction **d** in residual space corresponds to a behavior
(truthfulness, a language, a style), then at generate time you
can add `α d` to the stream (**activation addition**, steering
vectors, representation engineering).

How you get **d**: difference of means between contrastive
prompts ("I am in France" vs "I am in Japan"), or an SAE latent,
or a linear probe. How you prove it: sweep `α`, show the
behavior moves, show a control behavior does not, show it
still works on held-out prompts.

Steering is a **runtime control**, not a substitute for SFT.
It is brittle across models and templates. It is also one of
the few interp tools a product can actually call.

### Abliteration, as an application with risks

Community write-ups under the name **abliteration** locate a
**refusal direction** (activations on harmful vs benign prompts)
and subtract or project it out so the model stops refusing.

This course treats that literature as **interpretability**:
refusal is a readable direction in some chat models; intervening
on it changes behavior. That is a scientific fact with a safety
and license shadow.

What this module will not do:

- It will not give a procedure whose goal is to strip safety
  training, produce an "uncensored" checkpoint, or bypass a
  provider's acceptable use policy.
- It will not treat "abliterated weights" as a recommended
  artifact to ship.

If you study refusal directions, keep the work in a controlled
setting, measure **both** over-refusal and under-refusal, and
read the model license (S11). Removing a refusal vector is easy
to overclaim (the model still has other circuits) and easy to
abuse. Capability research that needs to understand refusals
can use steering **on a narrow eval** and then put the vector
down. Product work that needs fewer false refusals belongs in
**data and policy** (S3, S5, L3), not in a one-shot projection
sold as alignment reversal.

Jailbreaks and exploit catalogs are out of scope for the whole
course. Security as defense is Engineer E8.

### What a claim is allowed to sound like

Allowed: "Adding this SAE latent at layer 18 increases the rate
of French completions on this 200-prompt set from 4% to 61%,
and a random direction of the same norm does not."

Not allowed: "We found the French neuron, so we understand the
model."

Interp is a measurement discipline. It borrows eval habits from
S6: controls, held-out prompts, effect sizes, failure buckets.

## The gap most roadmaps leave

A single abliteration notebook, framed as a party trick. Missing:

- Logit lens as a timing diagnostic.
- SAEs as dictionary learning with reconstruction error.
- Steering as an intervention with a coefficient and a control.
- Refusal-direction work named as **risky interp**, not as a
  how-to for uncensoring.
- The split from S8, so this is not "new trends."

## Practice

No required lab. On paper, for a 2B to 8B instruct model you are
allowed to run:

1. Write a logit-lens experiment: one factual prompt, which
   layers you would plot, what would falsify "the model decided
   at layer L."
2. Write a steering experiment: contrastive pair, where you add
   the vector, what you will count, what the control direction
   is.
3. Write one paragraph on why subtracting a refusal direction
   is a poor substitute for changing SFT data, including a
   license and safety sentence.

Do not publish weights whose only selling point is disabled
refusals. If you need a milder assistant, collect better
preference data (S5) and eval over-refusal properly (S6).

## Watch and read

- nostalgebraist, [Interpreting GPT: the logit lens](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens)
- Anthropic, [Towards Monosemanticity](https://transformer-circuits.pub/2023/monosemantic-features/index.html), later SAE papers on [transformer-circuits.pub](https://transformer-circuits.pub/)
- [SAELens](https://github.com/decoderesearch/SAELens)
- Turner et al., activation addition / steering literature; Zou et al., representation engineering
- Stanford CS336, interpretability lectures when present
- Lilian Weng, [Transformer family](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/) (mechanistic notes)
- Hugging Face, interpretability blog posts and Gemma Scope cards
- [docs/ASSESSMENT.md](../../docs/ASSESSMENT.md) on why abliteration is not the whole topic

## Knowledge check

1. Why is an attention map not enough for a causal claim?
2. What does the logit lens apply to intermediate states?
3. What problem are SAEs trying to reduce in raw activations?
4. How do you show a steering vector is not a placebo?
5. Why does this course refuse a how-to whose goal is stripping
   safety refusals?

<details>
<summary>Answers</summary>

1. Correlation without an intervention. You must change the
   activation and show the output moves as predicted.
2. The final unembedding (or a tuned stand-in), producing a
   token distribution as a diagnostic of that layer's state.
3. Superposition: many features packed into fewer dimensions.
   SAEs learn a sparse overcomplete dictionary that is easier
   to name and to intervene on, with reconstruction error.
4. Held-out prompts, a coefficient sweep, and a control
   direction of the same norm that should not move the metric.
5. That procedure is a safety and license event, easy to abuse,
   and a poor product substitute for data and policy. Refusal
   directions can be studied as interp with controls; they are
   not a recommended shipping trick.

</details>
