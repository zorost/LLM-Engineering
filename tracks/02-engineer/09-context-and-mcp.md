# E9 · Context, tools, and MCP

## Why it exists

The context window is a budget. Everything you add (system
policy, tools, retrieved chunks, history, memory) spends
it. Prompt caching makes a *stable prefix* cheap and a
jittery prefix expensive. MCP makes tools a protocol
instead of a pile of Python callables. This is the module
the 2024 roadmaps under-named. Ng's later skills maps put
**context engineering** where "prompt engineering" used to
be the whole job. Phrasing still matters (E1). Packing,
caching, and contracts are the scarce skill.

## The idea

### Context engineering

A request is an ordered packing problem:

1. **Policy** (system): stable, short, cacheable.
2. **Tool contracts:** names, JSON schemas, short
   descriptions. These are prefix if they do not change
   per user.
3. **Task:** the user turn.
4. **Evidence:** retrieved chunks, files, images, tables.
5. **History / memory:** E11. Compact or retrieve; do not
   paste a year of chat.

Every token you add competes with evidence. A 40k-token
system prompt that restates the company wiki is a RAG miss
with extra latency. Measure: tokens in, cache hit rate,
latency, and task eval. Not vibes.

**Compaction.** When history exceeds a budget, summarize
or drop the middle with a rule you can test. Summaries
lie (E11). Keep hashes or ids of source turns if you must
rehydrate.

**Position.** Models still overweight the start and the
end of a long window. Put the instruction that must bind
in a stable prefix. Put the evidence next to the question,
delimited. Do not bury the question under ten tool dumps.

Long-context architecture (RoPE scale, sliding windows)
is S1. Here you assume a finite window and spend it.

### Prompt caching and prefix cache

Hosted: Anthropic prompt caching, OpenAI prompt caching,
Gemini implicit/explicit caches. Local engines: radix /
prefix cache (SGLang), vLLM prefix caching.

The rule is physical: **the cached span must be
byte-identical** from the start of the prompt. A per-request
UUID, timestamp, or shuffled tool list in the prefix
destroys the hit. Design:

- Static prefix: policy + tool schemas.
- Dynamic suffix: user, retrieved chunks, the latest
  observation.

Billing often distinguishes write, hit, and uncached
tokens. Log those. E6 is the serving view of the same
idea.

Lab 04 (templates) and lab 11 (schemas) are the packing
primitives. A broken template wastes prefix on tokens the
model was not trained to see.

### Tool contracts

A tool is an API:

- **Name** stable across versions.
- **JSON Schema** for arguments (E1 structured output).
- **Description** that tells the model *when* to call, not
  a novel.
- **Side-effect class:** read-only vs irreversible.
- **Timeout, idempotency key, error shape.**
- **Auth:** the tool runs as the user, not as a god role.

The model emits a call. Your runtime validates the schema
*before* execution. Invalid calls are observations, not
crashes. Excessive agency (OWASP) is a contract failure:
the tool should not exist, or should require approval.

MCP is how those contracts travel between processes.

### MCP servers and clients

[Model Context Protocol](https://modelcontextprotocol.io/)
defines:

- **Host.** The app (IDE, agent runtime) the user is in.
- **Client.** The host's MCP client session.
- **Server.** A process that exposes **tools**,
  **resources** (data), and **prompts** (templates).

Transport is stdio or HTTP with the negotiated protocol
version. Discovery means the host can list tools without
importing your Python. That is the operational win: one
retriever server (E3), one warehouse SQL server (E4), many
hosts (Cursor, Claude, a custom agent).

Write a server when a capability should be reused and
audited. Write a client when you are the host. Test with
the MCP inspector. Version the schemas. Do not put secrets
in resource URIs that will be logged.

A2A (E5) is peer agents. MCP is tools and context into an
agent. You can use both. You can use neither if you own
the whole process. Teams start to need MCP when the tool
owners are not the agent owners.

Hugging Face, [MCP Course](https://huggingface.co/learn/mcp-course),
is an independent companion.

## The gap most roadmaps leave

They teach "write a better prompt" and skip **the cache
key** and **the tool schema as an API**. Symptoms:

- Spend on input tokens that were identical to yesterday.
- Agent calls `delete_all` because the description was
  cute and the schema had no confirmation flag.
- Every host reimplements the same SQL tool.

Context engineering is budget plus contracts. Prompt
poetry is a subset.

## Practice

1. Lab `04_chat_templates.ipynb` with an eye on prefix
   tokens.
2. Lab `11_structured_output.ipynb` as a tool argument
   schema.
3. Lab `15_openai_compatible_client.ipynb`: send a long
   static prefix plus a short question twice. If you have
   a provider with caching, compare usage fields.

On paper: pack a 8k window for a RAG+tools app. Assign
token budgets to policy, tools, evidence, history. What
gets cut first when a user pastes a 6k log?

Going further: official MCP quickstart, one server that
wraps lab 08 search as `search_corpus`. Hugging Face MCP
Course after that.

## Watch and read

- MCP, [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- Hugging Face, [MCP Course](https://huggingface.co/learn/mcp-course)
- Anthropic, [prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- OpenAI, [prompt caching](https://platform.openai.com/docs/guides/prompt-caching)
- Google, [Gemini context caching](https://ai.google.dev/gemini-api/docs/caching)
- vLLM, [prefix caching](https://docs.vllm.ai/)
- SGLang, [radix cache](https://docs.sglang.ai/)
- Anthropic, [writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
  (engineering notes; independent)

## Knowledge check

1. What should sit in the cacheable prefix, and what must
   not?
2. Why can a timestamp in the system prompt double your
   input bill?
3. What does schema validation do that a tool description
   cannot?
4. Name the three MCP surface types a server can expose.
5. When is MCP unnecessary?

<details>
<summary>Answers</summary>

1. Policy and tool schemas (stable bytes). Not: per-user
   PII, retrieved chunks, the live question, unique ids.
2. Caches key on an exact prefix. A changing clock makes
   every request a miss, so you pay full prefill (and
   miss-rate prices) on the large static part too.
3. It rejects illegal arguments before side effects. Prose
   cannot enforce types, enums, or required fields.
4. Tools, resources, prompts.
5. When one process owns the agent and the tools, and no
   other host will call them. A function plus a schema is
   enough. Add MCP when reuse or isolation appears.

</details>
