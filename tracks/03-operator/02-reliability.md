# O2 · Reliability

## Why it exists

A demo that works once is not a service. Users experience timeouts,
partial streams, duplicate tool calls, and silent fallbacks to a worse
model. Reliability is the set of boring contracts that keep those
events rare, bounded, and recoverable.

## The idea

### SLIs, SLOs, and error budgets

An **SLI** is a measurement: request success ratio, time to first token
(TTFT), time per output token, end-to-end latency at p50 and p95,
tokens actually produced versus requested. An **SLO** is the promise:
for example, 99% of interactive chat requests complete within 8 seconds
at p95, with TTFT under 1.2 seconds, over a 30-day window. The **error
budget** is the leftover failure you agreed to spend on deploys,
experiments, and bad days. When the budget is gone, you freeze features
and repair.

Do not SLO "the model is smart." SLO the machine-measurable envelope
around the model. Quality gates belong in evals (S6, E10, O4), not in
the load balancer.

### Timeouts are a ladder, not a number

A single 60-second timeout hides three different failures:

- **Connect / TLS:** the engine is down or DNS is wrong.
- **TTFT:** prefill is overloaded, the queue is long, or the prompt is
  huge.
- **Total / idle between tokens:** decode stalled, a tool hung, or the
  client stopped reading a stream.

Set them separately. Streamed responses need an idle-between-chunks
timeout so a stuck generator cannot hold a worker forever. The client's
timeout must be **longer** than the gateway's, which must be longer
than the engine's, or you retry a request that is still running.

### Retries

Retry only what is **safe to repeat**. A completion that already
streamed tokens to the user is not safe. A tool that charged a card is
not safe unless the tool is idempotent. Prefer:

- Retry connect failures and HTTP 429 / 503 with **exponential backoff
  and jitter**.
- Honor `Retry-After` when the engine sends it.
- Cap attempts. Three is a lot. Infinite retries are a self-DDoS.
- Put a **idempotency key** on the request if your gateway might
  replay. The engine should treat the same key as the same in-flight
  or finished job, not as a second generate.

Do not retry 400s from a bad schema. Fix the client.

### Fallback and degradation

A fallback is an explicit, tested path, not an accident:

1. Same model, other replica.
2. Smaller or quantized twin with a known quality drop.
3. Retrieval-only or template answer when generation is down.
4. Fail closed: a structured error the UI can show.

Write the quality drop in the runbook. "Fall back to the 8B" is a
product decision. Measure it in the eval suite so you know what users
get. Circuit breakers stop you from stampeding a sick engine: after N
failures in a window, open the circuit, serve the fallback, and probe
half-open on a timer.

### Concurrency, queues, and load shedding

GPUs have a concurrency sweet spot. Past that, TTFT explodes because
prefill and KV fight for memory. Put a **queue with a max depth** in
front of the engine. When the queue is full, reject fast (429 or 503)
instead of accepting work you will time out. Load shedding is kinder
than a timeout graveyard.

Health checks: **liveness** means the process is not dead.
**Readiness** means it can take a new request (weights loaded, enough
KV headroom). Orchestrators that use liveness for both will kill a
model that is only busy.

### Idempotency and exactly-once theater

Generation is not exactly-once. Streams disconnect. Users retry. Tool
calls have side effects. Design for **at-least-once** with:

- Idempotency keys on side-effecting tools.
- Dedup of identical user submits in a short window.
- A request id that follows logs, traces, and billing.

If a client replays a chat turn, the safe server behavior is to return
the stored completion or to refuse, not to sample a new one and bill
twice.

### Releases

Treat a model, a tokenizer, a chat template, and an engine flag set as
one **release**. Canary a percentage of traffic. Keep the previous
release bootable. Shadow traffic (copy requests to the candidate, do
not show the output) is how you learn latency before you learn
regret. Never ship a new template and a new quantization in the same
hour if you can avoid it.

## The gap most roadmaps leave

They teach "call the API with backoff" and skip the part where **the
retry is the outage**. They skip readiness versus liveness. They skip
the fact that a streamed chat completion is not an HTTP POST you can
blindly repeat. They never mention that a fallback model needs an eval
score, not a hope.

## Practice

No dedicated reliability notebook. Do this on paper, then against lab
15's client if you have a local server:

1. Draw the timeout ladder: client, gateway, engine, tool.
2. Write which status codes you retry, and which you do not.
3. Write a four-rung fallback ladder for a chat product, including
   what the user sees on the last rung.
4. Name one tool in your system that is unsafe to retry, and how you
   would make it idempotent.

If you operate a real engine, break it on purpose in a staging
environment: kill a replica, fill the queue, and confirm clients get
429s instead of 60-second hangs.

## Watch and read

- Google SRE book, chapters on SLOs and eliminating toil (public
  HTML): [sre.google/books](https://sre.google/books/)
- Engine metrics docs for vLLM and SGLang (queue depth, KV usage,
  prefix hit rate)
- Chip Huyen, *AI Engineering*, chapters on the inference and
  feedback loop (see [BOOKS.md](../../reference/BOOKS.md))
- E10 production evals: a reliable server serving the wrong model is
  still a failure

## Knowledge check

1. What is an error budget for, if the SLO is already 99%?
2. Why must the client timeout be longer than the gateway timeout?
3. When is retrying a chat completion the wrong move?
4. What is the difference between liveness and readiness for a model
   server?
5. Why does a fallback model need a place in the eval suite?

<details>
<summary>Answers</summary>

1. It is the planned remainder you can spend on change (deploys,
   experiments, incidents). When it is exhausted, you stop spending
   and stabilize.
2. Otherwise the client gives up and retries while the gateway is
   still generating, which doubles load and can duplicate side
   effects.
3. When tokens already streamed, when a non-idempotent tool already
   ran, or when the error is a 4xx from a bad request. Replay needs a
   stored result or an idempotency key.
4. Liveness: the process should be restarted if it is wedged.
   Readiness: the process should receive traffic only when weights
   are loaded and it has capacity. A busy healthy replica is alive
   and not ready.
5. Because fallback is a product you will actually serve. If you do
   not measure its quality and latency, you will discover the drop in
   production.

</details>
