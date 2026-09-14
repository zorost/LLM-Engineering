# E1 · Running models

## Why it exists

Every later module assumes you can send text to a model and get text
back under a contract. Hosted APIs, a local runtime, and a JSON schema
are three surfaces of that one job. If you cannot do all three, RAG
and agents are theater.

## The idea

### One client, many backends

A chat request is a list of messages with roles (`system`, `user`,
`assistant`, later `tool`), a model id, and sampling knobs. The
useful knobs in production are few:

- **Temperature** and **top-p** (nucleus). Lab 03 is the picture.
  Classification and extraction want greedy or near-greedy.
  Open-ended drafting can tolerate more entropy. Do not tune both
  at once unless you are measuring.
- **Max tokens** is a cost and latency cap, not a quality lever.
- **Stop sequences** and **chat templates** decide whether the
  model keeps talking. Lab 04 exists because a missing end-of-turn
  token wrecks both SFT and local chat.

The HTTP shape that won is the OpenAI-compatible chat completions
(and, on some hosts, the Responses) API. Lab 15 is the point: one
Python client, many backends. You will use that fact in E7 and E12.

### Hosted APIs

You will meet these names. Learn the *contract*, not the brand
slide.

| Provider | What you are buying | Docs |
|---|---|---|
| OpenAI | Chat, embeddings, structured outputs, tools | [platform.openai.com/docs](https://platform.openai.com/docs) |
| Anthropic | Messages API, tool use, prompt caching, long context | [docs.anthropic.com](https://docs.anthropic.com/) |
| Google | Gemini API / Vertex; multimodal is a first-class input | [ai.google.dev](https://ai.google.dev/gemini-api/docs) |
| OpenRouter | One key, many upstream models, OpenAI-shaped | [openrouter.ai/docs](https://openrouter.ai/docs) |
| Hugging Face | Hub weights, Inference Providers, Spaces | [huggingface.co/docs](https://huggingface.co/docs) |
| Together | Hosted open models, OpenAI-compatible | [docs.together.ai](https://docs.together.ai/) |

Pick a provider with an eval, a license, a data-retention policy,
and a price per million tokens, not with a tweet. OpenRouter is a
router. It does not repeal the upstream license or the retention
clause. Hugging Face is a hub and an inference option; a model
card is mandatory reading before you serve (S11).

Optional API work is marked below. Required labs in this repository
use no paid key.

### Local runtimes

Local is for privacy, cost at high volume, and debugging the
template. It is not automatically cheaper at low volume.

- **LM Studio.** Desktop app, local OpenAI-compatible server,
  GGUF-centric. Good first local server.
- **Ollama.** CLI plus a local server. `ollama pull` then chat.
  Convenient. You still own the template and the license.
- **llama.cpp.** The engine under a lot of GGUF serving. Metal on
  Apple silicon, CUDA and others elsewhere. Closest to the metal
  if you need flags.

Read the model card. Prefer Apache-2.0, MIT, BSD, or a published
community license you can actually ship. Do not treat a
research-only or non-commercial weight as a house default. This
course will not name restricted speculators as the path.

VRAM and KV math live in F5, lab 13, and E6. A 7B in fp16 is
roughly 14 GB of weights before cache. Quantized GGUF is how a
laptop participates.

### Prompt patterns

The catalog is stable. The mistake is treating the catalog as the
product. [promptingguide.ai](https://www.promptingguide.ai/) is the
public map. Use it. Then measure.

- **Zero-shot.** Task, constraints, output shape. The baseline.
  Beat it before you add examples.
- **Few-shot.** One to a few input-output pairs that show a
  convention (label set, JSON keys, tone). Extra shots cost
  context on every call and invite copying the example *values*.
- **Chain-of-thought.** Ask for intermediate steps on tasks that
  actually have steps (math, multi-hop, policy trees). Hidden
  reasoning in some hosted models is a product feature, not a
  prompt you paste. You still need an eval on the *answer*.
- **ReAct.** Thought, action, observation, in a loop, with tools.
  That loop is E5. Learn the names here so lab 10 is not a
  surprise. Do not import a framework to print those three words.

Prompting is the interface. **Context engineering** (E9) is the
budget: what else is in the window, in what order, at what cache
key. A beautiful instruction in a stuffed window still loses.

Treat the system prompt as policy, not as a lock. Untrusted text
(retrieved docs, tickets, web pages) is data. It goes in a
delimited user or tool field. Enforcement lives in code. See E8.

### Structured output

Free text is for humans. Programs need a type.

Three layers, in the order you should reach for them:

1. **Ask for JSON** and parse. Cheap. It will fail on a bad day.
   Retry with the error. Not a contract.
2. **JSON Schema as a contract.** OpenAI structured outputs,
   Gemini response schemas, and several local servers will
   constrain or validate against a schema. Lab 11 is the CPU
   version of that idea: the schema is the API.
3. **Constrained decoding.** The sampler is only allowed tokens
   that continue a valid string under a grammar. [Outlines](https://github.com/dottxt-ai/outlines)
   (and its docs at [dottxt-ai.github.io/outlines](https://dottxt-ai.github.io/outlines/))
   and [XGrammar](https://github.com/mlc-ai/xgrammar)
   ([xgrammar.mlc.ai/docs](https://xgrammar.mlc.ai/docs/)) are the
   libraries. vLLM, SGLang, TGI, and MLC wire this in so JSON
   is not a regex after the fact.

A schema that the model can satisfy is a product decision. A
schema the task cannot fill is a hallucination machine with extra
braces. Put required fields only where the eval can check them.

Tool calling is structured output with side effects. The model
emits a name and arguments. Your code runs the function. The
observation comes back as a tool message. Contracts for those
tools are E9. The loop is E5.

## The gap most roadmaps leave

They list APIs, then jump to LangChain. The missing objects are:

| Object | Why it bites |
|---|---|
| Chat template | Local model ignores your "system" string and concatenates |
| Schema vs prose | The demo parses; production gets a trailing fence |
| Router vs provider | OpenRouter uptime is not OpenAI's DPA |
| License on the card | You cannot ship a non-commercial GGUF in a product |
| Sampling as a product choice | Temperature 0.8 on extraction is noise, not style |

If you can explain those five, you can call a model on purpose.

## Practice

Required, no API key:

1. Lab `03_decoding_strategies.ipynb`. Greedy, temperature, top-k,
   nucleus. Write one sentence on when you would freeze temperature
   at 0.
2. Lab `04_chat_templates.ipynb`. Break a template on purpose.
   Notice the extra tokens.
3. Lab `11_structured_output.ipynb`. JSON schema as a contract.
4. Lab `15_openai_compatible_client.ipynb`. One client, a fake
   backend, then (optional) a local server if you have one.

Going further, optional, your key, never committed:

- Send the same prompt suite through OpenAI, Anthropic, a Gemini
  call, and OpenRouter. Record cost, latency, and schema-validity.
- Serve a small openly licensed GGUF in LM Studio or Ollama and
  point lab 15 at `http://localhost`.

Do not download a weight whose card says research-only or
non-commercial and then call it production.

## Watch and read

- [promptingguide.ai](https://www.promptingguide.ai/) (zero-shot,
  few-shot, CoT, ReAct; use as a catalog, then measure)
- OpenAI, [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- Anthropic, [Messages](https://docs.anthropic.com/en/api/messages)
  and [prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- Google, [Gemini API docs](https://ai.google.dev/gemini-api/docs)
- [OpenRouter docs](https://openrouter.ai/docs)
- [Together docs](https://docs.together.ai/)
- Hugging Face, [Inference Providers](https://huggingface.co/docs/inference-providers)
- [Ollama](https://ollama.com/), [LM Studio](https://lmstudio.ai/),
  [llama.cpp](https://github.com/ggml-org/llama.cpp)
- Outlines, [docs](https://dottxt-ai.github.io/outlines/) ·
  XGrammar, [docs](https://xgrammar.mlc.ai/docs/)
- Hugging Face, [LLM Course](https://huggingface.co/learn/llm-course)
  (independent; we do not copy it)

## Knowledge check

1. Why is an OpenAI-compatible local server a bigger deal than a
   vendor-specific SDK?
2. When is few-shot the wrong next step after zero-shot fails?
3. What does constrained decoding guarantee that "please return
   JSON" does not?
4. Why is a chat template a production bug, not a cosmetic one?
5. What four documents do you read before you call a new hosted
   model from a product?

<details>
<summary>Answers</summary>

1. Application code, eval harnesses, and gateways can swap
   backends without a rewrite. Lab 15 is that client. Vendor SDKs
   remain useful for features the common shape does not cover.
2. When the failure is missing evidence, a bad schema, or a
   window packed with noise. More examples will not fetch the
   document. See E3 and E9.
3. Every sampled token stays inside the grammar, so the string is
   structurally valid (JSON, regex, a custom CFG). It does not
   make the *values* true.
4. Special tokens mark roles and turns. A missing or doubled end
   token trains and serves the wrong conversation. Local models
   are unforgiving. Lab 04.
5. Model card (license, intended use), data-retention and training
   policy, pricing, and your eval suite on *your* task. A blog
   benchmark is not the fourth.

</details>
