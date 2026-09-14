# Tutorial · Evals

## Why it exists

An eval is a **rerunnable measurement on a frozen set**, plus an
error analysis. A leaderboard screenshot is not an eval. Lab 12 is
the habit. This note is how to keep the habit when someone asks
for "a quick accuracy."

## The idea

Four pieces:

1. **Task definition.** Input, allowed tools, output schema, who
   the user is. If this is fuzzy, the metric will be theater (L4).
2. **A frozen set.** Items the team does not train or prompt-tune
   on. Versioned. Contamination checked (S11). Include easy, hard,
   and **should-refuse** cases.
3. **A scorer.** Exact match, rubric, citation check, human label,
   or an LLM judge. Judges need **calibration** against humans on
   a subsample. An uncalibrated judge is another model you have
   not evaluated.
4. **A gate.** A number and a slice (overall, plus buckets) that
   must hold before release. When it fails, you read the **error
   buckets**, you do not average harder.

Production adds traces and sampled online scoring (E10, O4). Offline
golden sets still win arguments. Online sampling catches drift.

Ragas and DeepEval are libraries that implement some metrics
([TOOLS.md](../reference/TOOLS.md)). They do not invent your golden
set. Hamel Husain's public eval teaching is the attitude: error
analysis first, automation second.

Do not use MMLU as a product eval unless your product is taking
MMLU. Public academic suites are for scientists (S6) and for
contamination caution, not for a freight chatbot's go-live.

A judge that is also the model under test will flatter itself.
If you must judge automatically, use a **different** model, a
rubric with yes/no checks before a 1 to 5 score, and a human
spot-check of disagreements. Record the judge name and prompt
hash in the eval report. Changing the judge is a new eval, not
a continuation of the old number.

Pass/fail on **slices** (language, tenant, document type, tool
path) or you will ship a system that works on the average and
fails on the customer who pays. O3's cost per successful task
belongs on the same report as quality: a cheaper model that
fails the gate is not a saving.

## The gap most tutorials leave

They report a single accuracy. They hide the prompt in a gist. They
let the judge score the same items the team just eyeballed. They
never add items that must fail.

## How the lab should feel

Lab 12 should feel like a small CI job: a suite, a threshold, a
table of misses grouped by reason. You should be slightly
embarrassed by how small the set is, then keep it frozen anyway.
A set of thirty well-chosen items beats a thousand you will not
read.

## Practice

1. `12_eval_harness.ipynb`.
2. Add one bucket: schema-invalid, ungrounded, timeout, wrong
   tool, refuse-correctly. Label the lab's misses.
3. Write a gate in one line: "Ship if faithfulness ≥ X on N=…
   and schema-valid ≥ Y, else block." Put it in the README of an
   imaginary product.

## Watch and read

- S6 and E10 in this course
- Hamel Husain, eval talks and Mastering LLMs
- Ragas and DeepEval docs
- Anthropic and OpenAI public eval / safety eval writeups (dated)

## Knowledge check

1. What makes a set "frozen"?
2. Why bucket errors instead of only reporting a mean?
3. When is an LLM judge acceptable in the gate?
4. Why include items the system should refuse?
5. How does O4's sampling differ from lab 12?

<details>
<summary>Answers</summary>

1. You do not train, retrieve-tune, or prompt-tune on it, and you
   version it so yesterday's number can be rerun on today's code.
2. Means hide a new failure mode that a bucket would show. Fixes
   attach to buckets.
3. After you measure agreement with humans on a subsample, and
   never as the only score on a high-stakes release.
4. Otherwise you only measure helpfulness and you will ship a
   system that answers when it should stop.
5. Lab 12 is offline, full golden set, blocking. O4 sampling is
   online, partial, for drift. You need both.

</details>
