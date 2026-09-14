# O4 · Observability

## Why it exists

You cannot repair what you cannot see, and you cannot keep a regulator
if you logged every prompt in plaintext. Observability for LLMs is
traces, metrics, and sampled evals, with **privacy as a design
constraint**, not a later filter.

## The idea

### Three signals

**Metrics** answer "is the service sick?": QPS, queue depth, KV cache
utilization, prefix-cache hit rate, GPU memory, TTFT, inter-token
time, error rate by code, tokens in/out, estimated dollar. These are
cheap and high-volume. Put them on a dashboard with the SLO lines from
O2.

**Traces** answer "what happened to request X?": a request id, model
id, engine version, template hash, token counts, cache hit, tool names
and durations, fallback taken, finish reason (`stop`, `length`,
`content_filter`). One trace per user-visible turn. Spans for
retrieval, rerank, generate, tools. OpenTelemetry is the usual
carrier. If you cannot join a user complaint to a trace id, you do
not have production.

**Eval samples** answer "did quality move?": a scheduled slice of
production-like inputs run through the release gate (lab 12, E10).
Online, you may score a **sample**, never 100% of traffic with an
expensive judge, unless the product is tiny. Offline golden sets catch
regressions. Online sampling catches drift. Neither replaces the
other.

Logs are the text attached to traces. They are not a strategy by
themselves.

### What to record besides the string

Always:

- Request id, session id, tenant id
- Model name, revision, quantization, engine, template id
- Token counts (prompt, completion, cached)
- Timings (queue, prefill, decode, tools)
- Retrieval ids (document and chunk ids, not necessarily the text)
- Tool names, latency, and structured error codes
- Sampler settings (temperature, top-p, seed if any)

Prefer **pointers** over payloads: chunk ids in the index, object ids
in object storage, with a retention policy. Rehydration is a privilege,
not the default log line.

Tokenizer ids, when you can store them safely, debug Unicode and
template bugs that strings hide. CS25 serving talks beg for this for
a reason.

### Privacy and retention

Prompts are often **personal data**, secrets, or regulated text.
Default rules for this course:

- Do not log API keys, cookies, auth headers, or known secret
  patterns. Redact before persist.
- Treat user content as sensitive. Sample, encrypt at rest, access
  control, and a short default retention (days, not years) unless a
  legal hold says otherwise.
- Separate **operational traces** (ids, timings, hashes) from **content
  archives** (full prompts). Most on-call should not need the archive.
- Do not train, fine-tune, or vendor-log customer content unless the
  contract and the UI say so. "The provider's default is opt-in for
  training" is a vendor setting you verify, not a rumor.
- LLM-as-judge on production text is another processor. It needs the
  same legal story as the main model.

Redaction is imperfect. Do not invent a sense of safety from regexes
for credit cards if your corpus is clinical notes. Sometimes the
correct log is "payload omitted."

Prompt injection and exfiltration are Engineer E8. The operator's job
is to make sure **tool outputs and retrieved documents are marked as
untrusted data in traces**, so an incident review can see that the
model was reading a poisoned chunk. That is evidence. It is not an
exploit tutorial.

### Quality without voyeurism

You still need to read failures. Build an **error-bucket review** on a
sample: empty retrieval, timeout, schema fail, refusal, user thumbs
down. Reviewers see the minimum text required, in a locked tool, with
audit of who opened it. Thumbs-down is a biased sample. Use it to
start analysis, not as a KPI to game.

Drift: embedding index staleness, template drift, model revision
swap, tokenizer upgrade. Alert on **distribution shifts** you can
measure (token length, retrieval score, refusal rate, schema-fail
rate) before you alert on vibes.

### What not to do

- Debug by tailing production prompts in a shared Slack channel.
- Store traces forever "because storage is cheap."
- Put the full RAG corpus into every span event.
- Measure "accuracy" online with an uncalibrated judge and ship the
  number to the board (see L4).

## The gap most roadmaps leave

They add LangSmith or an equivalent in a screenshot and call it
observability. They never mention **retention**, **who can replay a
prompt**, or **join keys to billing**. They log everything for a week
during a hackathon and forget to turn it off.

## Practice

1. Lab `12_eval_harness.ipynb`: a suite, a gate, an error bucket.
   That is the quality half.
2. On paper, design a trace schema for one RAG turn with no raw
   chunk text in the default span, only chunk ids.
3. Write a one-page data policy: what is stored, for how long, who
   can rehydrate, and whether any vendor may train on it.
4. If you run a local engine, enable its metrics endpoint and name
   five gauges you would page on.

Going further: read OpenTelemetry's GenAI semantic conventions when
you instrument a real app. Match names so you are not the only person
who understands your dashboard.

## Watch and read

- OpenTelemetry, GenAI / LLM semantic conventions (current docs)
- NIST AI RMF, MEASURE function (pointer in L3)
- E8 security and E10 production evals in the Engineer track
- Anthropic and OpenAI public docs on logging, retention, and
  training opt-out (they change; read the date)
- Hamel Husain's public writing on evals and traces (see
  [YOUTUBE.md](../../reference/YOUTUBE.md) and
  [COURSES.md](../../reference/COURSES.md))

## Knowledge check

1. Why are metrics insufficient by themselves after a "the model is
   being weird" ticket?
2. What should a default RAG span store instead of chunk text?
3. Why is logging 100% of prompts a governance incident waiting to
   happen?
4. Name two distribution metrics that can move before a leaderboard
   score does.
5. Who should be able to rehydrate a full prompt from a trace id?

<details>
<summary>Answers</summary>

1. Metrics tell you latency and error rate. They do not tell you
   which template, revision, retrieval set, or tool path that ticket
   hit. You need a trace id and, if policy allows, a sampled payload.
2. Chunk and document ids, rank, and scores. Text lives in the index
   under access control, rehydrated on purpose.
3. Prompts contain secrets and personal data. Broad logs expand
   breach scope, complicate retention law, and tempt people to paste
   them into chat. Sample and protect, or omit.
4. Any two of: schema-fail rate, refusal rate, retrieval score
   distribution, output length, TTFT, thumbs-down rate, cache hit
   rate.
5. A small, audited role (trust and safety, on-call lead, or legal
   hold), not every engineer with cluster access.

</details>
