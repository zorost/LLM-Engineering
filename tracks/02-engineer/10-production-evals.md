# E10 · Evals in production

## Why it exists

A demo that "seemed fine" is not a release. Production
evals are **gates**: a suite with a threshold, run on
every change, with traces you can debug. Scientist
evaluation (S6) is whether a *model* is capable.
This module is whether *your application* is allowed to
ship today. Lab 12 is the harness.

## The idea

### Offline versus online

**Offline.** A frozen golden set (and challenge sets) you
run in CI or before a deploy. Labels, rubrics, automated
metrics, LLM-as-judge with a calibration slice. You can
replay. This is the gate.

**Online.** Live traffic: sampled traces, user feedback,
task success (did the refund actually post), latency,
cost, judge-on-sample. You cannot freeze the world. You
use this to *find* new failures and to promote examples
into the offline set.

If you only have online thumbs, you will ship a regression
that users have not yet clicked. If you only have offline,
you will miss drift. Both, with a promotion path.

### Traces

A trace is the ordered record of a request: messages,
retrieved ids, tool calls, tokens, timings, model ids,
prompt version. Spans are the steps. Langfuse, LangSmith,
OpenTelemetry-based stacks, Foundry tracing, Vertex eval
traces: pick one, require it in staging.

Without traces, an eval score is a rumor. With traces you
can bucket errors. Redact (E8). Retention is a policy.

### Error buckets

Do not file "the bot was wrong." File a type:

- Retrieval miss / wrong neighbor
- Faithfulness (said what the chunk did not)
- Schema invalid / tool parse
- Policy (should have refused)
- Latency / timeout
- Cost outlier
- Judge disagreement with a human spot-check

Fix the bucket with the most mass × severity, not the
funniest screenshot. Training 01 week 11 is this habit at
program length. Lab 12 is the CPU-sized version.

### Gates

A gate is: **metric, threshold, slice, owner, what happens
on fail.** Example: faithfulness ≥ 0.X on the policy slice,
schema-validity 100% on extraction, injection tests from
lab 14 green. Fail blocks merge or blocks the deploy (E7).

Slices matter. A mean that hides the "refunds" intent is
how incidents happen. Track the slice that makes money or
makes regulators unhappy.

LLM-as-judge: version the judge model and the rubric.
Measure agreement with humans on a panel. A judge you
never calibrate is another untested model.

### Goodhart

When a measure becomes a target, it stops being a measure
(Goodhart's law; Strathern's formulation is the one people
mean). If you optimize only the judge score, the system
learns the judge. If you optimize only latency, it
abstains. If you add a metric to the gate, watch for
collapse on the ones you did not include.

Defenses: a small human panel that is not in the loss, a
held-out slice the team does not tune on, periodic
rotation of challenge items, and the rule that a metric
without an error-bucket review is not a gate.

Scientist leaderboards (S6) have the same disease.
Production has more ways to cheat because you own the
pipeline.

### What to version

Prompt, tool schema, retriever, embedding model, chunker,
model id, judge, golden set. A regression you cannot
attribute is an unversioned stack. Lab 12's "suite, gate,
error bucket" is the minimum object.

## The gap most roadmaps leave

They stop at "use RAGAS" or "use an eval Colab." Missing:

- Offline gate in CI.
- Online sample with promotion to golden.
- Buckets, not a single score.
- Goodhart as a design threat.
- Traces as the debugger.

Hamel Husain's eval writing and Chip Huyen's *AI
Engineering* eval chapters are the independent depth.
This file is the contract for the engineer track.

## Practice

Lab `12_eval_harness.ipynb`. Required.

1. Define three metrics and a fail threshold.
2. Bucket five synthetic failures by type.
3. Write the one-sentence gate: what blocks a release.

Then attach the lab 14 fixture class as a fourth metric
("unsafe handling = fail"). Security is a gate, not a
later audit.

Going further: Langfuse (or equivalent) on lab 10. Sample
ten traces. Promote one failure into the golden set.

## Watch and read

- This course, [S6 Evaluation](../01-scientist/06-evaluation.md)
  (model evals; do not conflate)
- RAGAS, [docs](https://docs.ragas.io/)
- DeepEval, [docs](https://docs.confident-ai.com/)
- Langfuse, [docs](https://langfuse.com/docs)
- OpenAI, [evals](https://github.com/openai/evals)
- Anthropic, [Claude eval documentation](https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool)
  and [research](https://www.anthropic.com/research)
- Hamel Husain, [Your AI product needs evals](https://hamel.dev/blog/posts/evals/)
- Eugene Yan, [eval essays](https://eugeneyan.com/writing/)
- Goodhart / Strathern: treat as a design rule, not a
  citation hunt

## Knowledge check

1. What is a release gate, in one sentence?
2. Why do traces belong next to scores?
3. Give an example of Goodhart in an LLM product.
4. What is the promotion path between online and offline?
5. Why is a single "accuracy" number a bad gate for RAG?

<details>
<summary>Answers</summary>

1. An automated suite with a threshold that must pass
   before merge or before production traffic moves.
2. Scores tell you it failed. Traces show which span
   (retrieve, tool, generate) failed so you can bucket
   and fix.
3. Optimizing an LLM judge until answers flatter the
   rubric but users still fail the real task; or cutting
   tokens until the bot always says "I don't know."
4. Sample live failures (and rare successes), label them,
   add them to the frozen set, rerun the gate so the
   incident cannot silently return.
5. It mixes retrieval misses with generator invention.
   You will "fix the model" when you needed the index
   (E3).

</details>
