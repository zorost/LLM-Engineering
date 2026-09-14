# Glossary

Every important term in LLM Engineering, in plain language. Search
this file when a module uses a word as if it were English. Each
entry is a definition, not a paper. Pointers at the end of an
entry show where the course goes deeper.

Do not read this cover to cover. Jump, read one paragraph, go back
to the module.

Part of **LLM Engineering** · Zorost Intelligence AI Lab · Training 02

---

## Tokens, text, and data

**Token.** An integer the model reads and writes. Not a word. English
often lands around three to four characters per token. Code and other
languages differ. *Lab 01; F5; tutorial tokenization.*

**Tokenizer.** The map between bytes and token ids, plus special
tokens. Serving and training must use the same one. *O1; S1.*

**BPE (byte-pair encoding).** A merge algorithm: start from bytes,
repeatedly merge the most frequent pair, stop at a vocabulary size.
The usual family for modern LLMs. *Lab 01.*

**Fertility.** Tokens per word (or per character). High fertility
makes a short sentence expensive and long. *F5; S11.*

**Chat template.** The string recipe that wraps roles (system, user,
assistant) and special stop tokens before encoding. Wrong template
looks like a worse model. *Lab 04; O1.*

**BOS / EOS / EOT.** Beginning-of-sequence, end-of-sequence, and
end-of-turn tokens. EOT is how a chat model learns to stop. *Lab 04.*

**Context window.** Maximum tokens of input plus output the engine
will accept for one generation. Product feature, memory cost, and
bill. *F5; E9; O3.*

**Contamination.** Eval items (or close paraphrases) present in
training or retrieval data, so the score is memorization. *S11; S6.*

**Train / validation / test split.** Holding out data by a unit
(document, user, time) so you measure generalization. If you tune
on test, it is not test. *F2.*

**Leakage.** Information from the future or from the test set
present in training or in features. Silent and fatal. *F2.*

**License (data or model).** The legal grant that says whether you
may serve, fine-tune, or sell. Cards that say research-only or
non-commercial are a procurement stop. *S11; L3.*

**Model card / dataset card.** The document that should name
intended use, data, evals, and license. Necessary, not sufficient,
as a system card. *S11; L3.*

---

## Architecture

**Embedding.** A vector for a token (or a chunk) used so similar
items are close in cosine. Input embeddings are a table in the
model; retrieval embeddings are often a separate model. *S1; E2.*

**Logits.** Raw scores over the vocabulary, before softmax. *F1;
lab 03.*

**Softmax.** Turn scores into a probability distribution. *F1.*

**Attention.** Weighting of other positions' values by a query-key
similarity. Decoder-only LLMs use causal (look-left) attention.
*Lab 02; S1.*

**Q, K, V.** Query, key, and value projections of the residual
stream. Scores are QKᵀ, then weighted V. *S1.*

**Causal language model / decoder-only.** Predict the next token
from previous tokens. GPT-style. The default in this course.

**Encoder-decoder.** Encode a source, decode a target (classic T5
and many translation models).

**Residual stream.** The backbone activations plus each block's
output. Why deep transformers train. *F3; S1.*

**RMSNorm / LayerNorm.** Normalize activations inside the block.
RMSNorm is common in recent Llama-family models. *S1.*

**RoPE (rotary position embedding).** Rotate Q and K by position
so attention depends on relative offset. *S1; paper RoFormer.*

**GQA (grouped-query attention).** Several query heads share a
key/value head. Shrinks KV cache. *S1; O1.*

**MQA (multi-query attention).** All query heads share one KV
head. Even smaller cache, sometimes a quality trade.

**MoE (mixture of experts).** Route each token to a few expert
MLPs instead of one dense MLP. Serving is a different job from
dense. *Lab 17; S1; O1.*

**SSM / hybrid.** State-space (or similar) layers mixed with
attention. The field is not decoder-only transformers forever.
*S1; S8.*

**KV cache.** Stored keys and values from previous tokens so
decode does not recompute the prompt. Grows with sequence, batch,
layers, KV heads, and dtype. *Lab 18; E6; O3.*

**Prefill.** Process the prompt, fill KV. Relatively compute-heavy.

**Decode.** Emit output tokens one (or a few) at a time. Often
memory-bound. *F5; O1.*

**FlashAttention.** IO-aware attention kernel that avoids
materializing the full score matrix in slow memory. *E6; paper.*

**Long context / YaRN / ALiBi / sliding window.** Methods to
extend or bound attention over long sequences. A 128k window is a
memory choice, not only a quality choice. *S1; E9; O3.*

**Tokenizer mismatch.** Using ids from tokenizer A in a model
trained on tokenizer B. Garbage in id space. *Tokenization
tutorial; O1.*

---

## Training and adaptation

**Pre-training.** Next-token prediction on a large unlabeled (or
weakly labeled) corpus. Cluster-scale. *S2.*

**SFT (supervised fine-tuning).** Continue next-token prediction
on instruction or conversation data. *S4; tutorial fine-tuning.*

**Teacher forcing.** During training, feed the true previous token,
not the model's last guess. *F3.*

**Cross-entropy / NLL.** Loss: how surprising the true next token
was. *F1.*

**Perplexity.** Exp of average NLL. A research metric. Weak as a
product gate.

**Gradient.** Vector of partial derivatives of the loss. Descent
steps opposite it. *F1.*

**AdamW.** Default optimizer in LLM work: Adam plus decoupled
weight decay. *F3; S2.*

**Mixed precision (fp16 / bf16).** Store and compute in 16-bit
formats to fit GPUs. bf16 is more numerically forgiving on
large runs. *F3; F5.*

**LoRA.** Freeze the base, learn low-rank adapters. Rank r and
alpha are the knobs. *Lab 05; S4.*

**QLoRA.** LoRA on a 4-bit quantized base so large adapters fit
on one GPU. *S4; S7.*

**Full fine-tune.** Update all (or most) weights. Memory-heavy.

**Instruction tuning.** SFT on instruction-response pairs. A
kind of SFT, not a separate physics.

**RLHF.** Reinforcement learning from human (or AI) preference,
classically PPO against a reward model, with a KL penalty to a
reference. *S5.*

**PPO.** Proximal policy optimization. The RL algorithm InstructGPT
popularized for LLMs. *S5; paper.*

**DPO.** Direct preference optimization: a closed-form loss on
preferred versus rejected pairs, no separate reward model.
*Lab 06; S5.*

**GRPO.** Group relative policy optimization, used in DeepSeekMath
and related reasoning recipes. RL without a separate value model
in the usual GRPO setup. *S5; S9.*

**KL divergence.** Distance between distributions. Appears as a
penalty to stay near a reference model, and in distillation. *F1;
S5.*

**Distillation.** Train a smaller student to match a teacher's
outputs or hidden states. *S10.*

**ChatGPT-style post-training.** Informal bundle: SFT plus
preference plus (sometimes) reasoning RL. Not one paper.

**Overfit.** Train metric improves, held-out metric does not, or
the model memorizes the suite. *F3.*

---

## Inference, decoding, serving

**Inference.** Using a trained model to produce outputs. Most of
engineering is here. *F3; Engineer and Operator tracks.*

**Temperature.** Divides logits before softmax. Low is sharp
(near greedy). High is flat. *Lab 03; F1.*

**Greedy decoding.** Always pick the highest-probability token.

**Top-k.** Sample from the k most likely tokens.

**Nucleus / top-p.** Sample from the smallest set whose
probability mass is at least p. *Lab 03; decoding tutorial.*

**Structured output / constrained decoding.** Mask illegal tokens
so outputs match JSON Schema or a grammar. *Lab 11; Outlines;
SGLang.*

**Speculative decoding.** A draft model proposes tokens; the main
model verifies. Speed technique. *Lab 16; S10.*

**MTP (multi-token prediction).** Train to predict more than one
future token; also used in some draft/verify stacks. *S10.*

**Continuous batching.** Let new requests join a running decode
batch as others finish. *O1.*

**PagedAttention.** Page the KV cache so memory is not one huge
contiguous reservation per request. vLLM's signature idea. *O1.*

**Prefix caching / radix cache.** Reuse KV for a shared prompt
prefix. Agents and fat system prompts care. *O1; E9; SGLang.*

**TTFT (time to first token).** Latency until the first emitted
token. User-felt. *O2.*

**TPOT / inter-token latency.** Time between output tokens after
TTFT.

**Throughput.** Tokens per second at a stated concurrency and
sequence length. Without those, a vanity number. *O3.*

**QPS.** Queries (requests) per second. Arrival rate. *O3.*

**Quantization.** Store weights (and maybe KV/activations) in
fewer bits with scales. GPTQ, AWQ, GGUF k-quants, bitsandbytes
NF4 are different methods. *Lab 07; S7.*

**GGUF.** File format used heavily by llama.cpp for quantized
weights. *O1; TOOLS.*

**vLLM / SGLang / TGI / llama.cpp / MLX.** Serving engines.
Choose by hardware and workload. *O1; TOOLS.md.*

**OpenAI-compatible API.** HTTP shapes like `/v1/chat/completions`
that many engines speak. Lab 15's point. *E1; O1.*

**Ollama.** Developer-friendly local daemon, typically wrapping
llama.cpp-class runtimes. Fine for E1. Rarely the production SLO
process. *O1; TOOLS.*

---

## Retrieval, agents, context

**RAG.** Retrieve documents, then generate an answer grounded in
them, with citations. *Labs 08 to 09; E3.*

**Chunking.** Splitting documents for the index. Size and overlap
are product choices. *E2.*

**Hybrid search.** Sparse lexical (BM25) plus dense vectors, then
usually a rerank. *Lab 09; E4.*

**Reranker.** A second model (often a cross-encoder) that scores
query-document pairs more carefully than cosine. *E4.*

**Faithfulness.** Whether the answer sticks to the retrieved
evidence. *E3; evals tutorial.*

**Hallucination.** Fluent output not supported by the allowed
evidence (or by the world). In RAG, often a retrieval miss.

**Context engineering.** What you put in the window, in what
order, with what cache. The window is the product. *E9.*

**Prefix / prompt cache.** Server-side reuse of the prompt's KV
or a vendor's cached input tokens. *E9; O3.*

**Agent.** A model in a loop that chooses tools until a stop or a
cap. *Lab 10; E5.*

**ReAct.** Thought, action, observation pattern. *Paper; lab 10.*

**Tool calling.** Structured actions (JSON) the application
executes. *E5; lab 11.*

**MCP (Model Context Protocol).** A standard way to expose tools
and resources to model clients. Not the loop itself. *E9.*

**A2A.** Agent-to-agent protocol proposals. Treat as contracts
between systems, still with caps and evals.

**LangGraph.** A library for stateful graphs of model and tool
nodes. Implementation of a loop. *TOOLS.md.*

**Memory (conversation).** Buffer, summary, or retrieve-from-notes.
Each can lie. *E11.*

---

## Evaluation and quality

**Eval.** A rerunnable measurement on a frozen set, with error
analysis. *Lab 12; S6; E10.*

**Golden set.** The frozen items you do not train on. Versioned.

**LLM-as-judge.** A model scores outputs. Needs calibration
against humans. *S6; O4.*

**Error bucket.** A named failure class (ungrounded, schema,
timeout, wrong tool). Fixes attach here. *Lab 12.*

**Release gate.** Numeric thresholds that block a ship. *E10; L4.*

**Ragas / DeepEval.** Libraries of metrics and harness helpers.
They do not replace your golden set. *TOOLS.md.*

---

## Reliability, cost, observability

**SLI.** A measurement (success ratio, p95 TTFT). *O2.*

**SLO.** The promise on that measurement over a window. *O2.*

**Error budget.** Residual failure you agreed to spend on change.
*O2.*

**Circuit breaker.** After repeated failures, stop calling a
dependency and serve a fallback. *O2.*

**Idempotency key.** A client-supplied id so retries do not start
a second generation or a second side effect. *O2.*

**Fallback ladder.** Ordered degraded modes, each eval'd. *O2; L4.*

**Token economics.** Input versus output prices, retries, idle
GPUs, tokenizer used for the bill. Cost per successful task. *O3.*

**Trace.** Per-request timeline with ids, model revision, token
counts, tool spans. *O4.*

**Redaction.** Removing secrets and personal data before logs
persist. Imperfect. Sometimes the right log is "payload omitted."
*O4.*

**PII.** Personal data in prompts and outputs. Retention and
access are design constraints. *O4; L3.*

---

## Security (defensive)

**Prompt injection.** Untrusted text in the window that tries to
override policy or tool use. Treat as a test case, not a trophy.
*E8; lab 14; security tutorial.*

**Data poisoning.** Hostile content in training data or in an
index. *E8; S3.*

**Jailbreak (as a test class).** Attempts to evade stated policy.
This course stores only the idea of testing policy hold, not
payload catalogs. *E8; L3.*

**Allowlist.** Tools, URLs, or actions explicitly permitted.
Privilege beats a sterner system prompt. *E5; E8.*

---

## Leadership and governance

**Buy / build / retrieve / fine-tune ladder.** Cheapest honest
move that hits the eval. *L1.*

**Seam.** A named crossing: untrusted text in, model decision,
tool write, human approval. Distilled's notation exists so you
cannot hide these in a box labeled "AI." *L1; BOOKS.md.*

**Eval owner.** The named human who freezes the set and runs the
gate. *L2.*

**Shaping the build.** Ng's skills-map term: deciding what to
make, what done means, and what to cut. Independent of this
course. *L2.*

**NIST AI RMF.** GOVERN, MAP, MEASURE, MANAGE. Voluntary US
framework, shared language. *L3.*

**EU AI Act.** EU risk-tiered regulation. Provider versus
deployer is a legal role. Counsel required. *L3.*

**System card.** Use, limits, evals, data map, kill switch. Not
only the model card. *L3.*

**Kill criteria.** Numeric stop rules written before a pilot.
*L4.*

**Configuration record.** Model revision, prompts, index
snapshot, tools, SLO, eval, rollback. How a demo becomes a
product. *L4; O4.*

**Andrew Ng AI Engineering Skills Map.** Public 2026 DeepLearning.AI
letter: applications, software fundamentals, coding agents,
shaping the build. Not a Zorost credential. *L2.*

---

## Hardware and scaling

**VRAM.** GPU memory. Weights + KV + activations + overhead. *F5;
lab 13.*

**FLOPs.** Arithmetic volume. Decode is often limited by memory
bandwidth instead. *F5.*

**Arithmetic intensity.** FLOPs per byte moved. *F5; CS336.*

**Scaling laws.** Loss versus compute, data, and parameters, in a
range, with caveats (Chinchilla and after). *Lab 19; F5.*

**Chinchilla.** A compute-optimal training result: smaller models
with more tokens can beat larger starved ones, with later caveats.
*F5.*

**Unified memory.** Apple silicon (and some others): CPU and GPU
share RAM. Changes the shopping list, not the math. *O1; MLX.*

---

## Interpretability and reasoning (short)

**SAE (sparse autoencoder).** A tool for decomposing activations
into features. Easy to overclaim. *S12.*

**Activation steering.** Adding a vector to activations to bias
behavior. Limited, not a moral system. *S12.*

**Reasoning model / test-time compute.** Spend more decode or
search at inference (longer chains, verifiers, tree search) on
purpose. *S9.*

**MCTS.** Monte Carlo tree search. Classical planning; some
LLM-at-test-time methods borrow the idea. *S9; PAPERS.md.*

**Process reward.** Scoring steps, not only final answers. *S5;
S9.*

---

If a term is missing, open an issue with the module path where you
met it.
