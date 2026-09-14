# Tools

What each thing is **for**. Versions move. Read current docs.
This is not a sales page and not a ranking that survives a
quarter.

Hardware and SLO choice lives in [O1](../tracks/03-operator/01-serving-engines.md).
Trainers belong with S4. Evals belong with lab 12.

---

## Serving engines

**vLLM.** GPU inference server: continuous batching, paged KV,
prefix cache, tensor parallel, OpenAI-shaped HTTP. Default when
you have datacenter GPUs and concurrent chat or completion.
Docs: [docs.vllm.ai](https://docs.vllm.ai/). Paper: PagedAttention
in [PAPERS.md](PAPERS.md).

**SGLang.** Serving stack with a radix prefix cache and first-
class constrained decoding. Measure it when the workload is
multi-turn, JSON-heavy, or shares a fat preamble. Docs:
[docs.sglang.ai](https://docs.sglang.ai/).

**TGI (Text Generation Inference).** Hugging Face's production
generator: streaming, parallelism, Hub workflow. Compare on your
model and sequence mix, not on a screenshot. Docs:
[huggingface.co/docs/text-generation-inference](https://huggingface.co/docs/text-generation-inference).

**llama.cpp.** C/C++ runtime for GGUF, quantization-first, CPU,
Apple silicon, and CUDA. Honest path for laptops, edge, and
air-gapped boxes. `llama-server` speaks a usable chat API.
Repo: [github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp).

**Ollama.** Local developer daemon: pull a tag, run a model, hit
an API. Convenience over llama.cpp-class stacks. Fine for E1 and
demos. Usually the wrong process for a shared SLO. Site:
[ollama.com](https://ollama.com/).

**MLX / mlx-lm.** Apple unified-memory arrays plus a language-
model toolkit. Local Mac development and on-device experiments,
not a multi-tenant GPU fleet. [github.com/ml-explore/mlx](https://github.com/ml-explore/mlx),
[mlx-lm](https://github.com/ml-explore/mlx-lm).

---

## Train, adapt, merge

**Unsloth.** Faster LoRA/QLoRA training kernels and notebooks for
supported models. Use when you actually train; still freeze an
eval first. [unsloth.ai](https://unsloth.ai/).

**TRL (Transformer Reinforcement Learning).** Hugging Face library
for SFT, DPO, PPO-class, and related trainers on `transformers`.
The default open trainer API this course names. Docs:
[huggingface.co/docs/trl](https://huggingface.co/docs/trl).

**Axolotl.** YAML-driven fine-tune runner on top of HF stacks.
Useful when the team wants a config file rather than a custom
train script. [github.com/axolotl-ai-cloud/axolotl](https://github.com/axolotl-ai-cloud/axolotl).

**mergekit.** Merge model weights (and some adapter recipes)
without a story. Merging is S8. Measure after. Do not merge as a
substitute for an eval. [github.com/arcee-ai/mergekit](https://github.com/arcee-ai/mergekit).

---

## Evals and structured output

**Ragas.** Metrics aimed at RAG (faithfulness, relevancy, and
neighbors). A library, not a golden set.
[docs.ragas.io](https://docs.ragas.io/).

**DeepEval.** Unit-test style evals and scorers you can put next
to CI. Same warning: you still write the cases. Docs:
[deepeval.com](https://deepeval.com/).

**Outlines.** Constrained generation from Python types and
regex/JSON Schema. Pair with lab 11. Engines (SGLang, some vLLM
paths) have their own grammars; Outlines is the library-shaped
version. [github.com/dottxt-ai/outlines](https://github.com/dottxt-ai/outlines).

---

## Agents and contracts

**LangGraph.** State machines / graphs for model and tool nodes.
Use after you can write the loop in lab 10. It will not invent
your step cap or your allowlist.
[langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/).

**MCP (Model Context Protocol).** A protocol for exposing tools
and resources to clients (IDEs, chat apps, your agent). Spec and
SDKs: [modelcontextprotocol.io](https://modelcontextprotocol.io/).
Hugging Face MCP Course in [COURSES.md](COURSES.md). E9 is the
module.

---

## How to choose without a bake-off theater

1. Write hardware, QPS, prefix share, and features (O1).
2. Pick one engine family. Measure TTFT, tokens/s, memory, quality
   on **your** eval.
3. Pick one trainer if you fine-tune (TRL unless you have a reason).
4. Pick one eval library only after lab 12's harness exists.
5. Do not add LangGraph and MCP in the same week as the first
   loop.

If a tool requires a restricted, research-only, or non-commercial
weight as the demo default, skip the demo. S11 still applies.
