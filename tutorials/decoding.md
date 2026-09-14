# Tutorial · Decoding

## Why it exists

Training produces a distribution over the next token. Decoding is
how you **draw** from it. Labs 03 and 16 are the difference between
"the model said" and "we sampled." Operators who skip this module
debug temperature in production as if it were a myth.

## The idea

The model emits **logits**. Softmax (with **temperature** T) turns
them into a probability distribution. T < 1 sharpens. T > 1
flattens. T → 0 approaches **argmax / greedy**.

**Greedy** is deterministic given the logits: always pick the max.
Useful for evals you want to rerun, and for many structured tasks.
It can loop.

**Top-k:** keep the k highest logits, renormalize, sample.
**Nucleus / top-p:** keep the smallest set whose mass ≥ p, then
sample. Combined top-k and top-p is common in serving stacks.

**Stop sequences** and **max_tokens** are part of decoding, not
etiquette. They are how O3 caps the bill and how chat templates
end a turn (lab 04).

**Speculative decoding** (lab 16, S10): a cheap **draft** model
proposes several tokens. The main model **verifies** them in one
prefill-like pass. Accepted tokens are free; a mismatch rolls
back. This is a speed method. It should not change the
distribution if implemented correctly. If quality moves, your
verify step is wrong.

Constrained decoding (Outlines, engine grammars, SGLang) zeroes
or masks illegal tokens so JSON and regex stay valid. It is the
right default for lab 11-style contracts. It will hide errors if
you constrain before you have an eval: the string parses and the
content is still wrong.

## The gap most tutorials leave

They set `temperature=0.7` because a screenshot did. They never
plot the same prompt at T=0 and T=1. They treat speculative
decoding as a different model rather than a sampler acceleration.

## How the labs should feel

**Lab 03.** Tiny logits. You compute greedy, then sample with T,
top-k, and nucleus by hand. You should see mass concentrate as T
drops. If you only call `model.generate`, you missed it.

**Lab 16.** A toy alphabet, a draft, a verifier. You should count
accepts and rejects. The lesson is the accept rule, not a
production speedup number.

## Practice

1. `03_decoding_strategies.ipynb` then `16_speculative_decoding.ipynb`.
2. For a product: write default T, top-p, max_tokens, and stop
   strings. Write which evals run greedy.
3. Optional: enable an engine grammar for JSON on a local server
   (O1) and show that invalid JSON rate drops on lab 11's task.

## Watch and read

- F1 softmax section; S1 sampling; E6 inference
- Holtzman et al., The Curious Case of Neural Text Degeneration
  (nucleus sampling), 2019, [arXiv:1904.09751](https://arxiv.org/abs/1904.09751)
- Leviathan et al., Fast Inference from Transformers via
  Speculative Decoding, 2022,
  [arXiv:2211.17192](https://arxiv.org/abs/2211.17192)
- 3Blue1Brown, attention / transformer videos for the logits
  pipeline

## Knowledge check

1. What does temperature divide?
2. Why run some evals greedy?
3. What does top-p keep?
4. When speculative decoding is correct, what should happen to
   quality?
5. Why can a JSON grammar still ship a wrong answer?

<details>
<summary>Answers</summary>

1. The logits (before softmax). Lower T sharpens the distribution.
2. To remove sampler noise so a regression is a model or prompt
   change, not a lucky draw.
3. The smallest prefix of sorted tokens whose cumulative
   probability is at least p, then it renormalizes and samples.
4. It should match the main model's distribution, within
   implementation noise. Speed changes. Quality should not.
5. Because the grammar enforces shape, not truth. Content evals
   still apply.

</details>
