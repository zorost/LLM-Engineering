# S1 · Architecture

## Why it exists

Every later module assumes you can trace one string from bytes to a
sampled token. If that path is a blur, LoRA ranks, KV caches, and MoE
routers are decorations on a box you cannot open.

## The idea

### Two families

The 2017 Transformer has an **encoder** and a **decoder**. The encoder
sees the whole source (bidirectional self-attention). The decoder
generates left to right and **cross-attends** into the encoder. T5,
BART, and classic machine translation still look like this. The encoder
is a good fit when the input is a complete document you will condition
on, and the output is a different sequence.

**Decoder-only** models dropped the encoder. Every token attends only
to the past (a causal mask). GPT, Llama, Gemma, Qwen, and almost every
chat checkpoint you will serve in 2026 are this family. Instruction
following did not change the wiring. It changed the data (S3) and the
loss mask (S4).

If a vendor says "encoder" in 2026, ask whether they mean a
bidirectional **embedding** model (retrieval) or an old seq2seq
generator. Those are different jobs.

### Tokenization

Text is not a tensor. A **tokenizer** maps bytes to integer ids from a
fixed vocabulary.

- **BPE** (byte-pair encoding) starts from characters or bytes and
  merges the most frequent adjacent pairs until the vocab budget is
  spent. GPT-2, tiktoken, and many English-centric recipes are BPE.
  Karpathy's [minbpe](https://github.com/karpathy/minbpe) and lab 01
  are the from-scratch version.
- **SentencePiece** trains on raw text without a language-specific
  pre-tokenizer. It can run BPE or Unigram. T5, ALBERT, and a large
  share of multilingual models use it. Whitespace becomes a normal
  character, which is why leading spaces are a real modeling event.
- **Unigram** (inside SentencePiece) starts with a large candidate
  vocab and **prunes** tokens that hurt a unigram language-model
  likelihood the least. Segmentation at encode time is a search, not a
  greedy merge. Fertility and rare-script behavior differ from BPE
  even at the same vocab size.

Fertility (tokens per word) is a product number. Code, CJK, and
agglutinative languages can be two to four times more expensive than
English on the same tokenizer. See F5 and S11.

Special tokens (`bos`, `eos`, `pad`, chat delimiters) are architecture.
A missing end token is an SFT bug, not a sampling bug. Lab 04 after
this module.

### Self-attention

For each position, the model builds **queries**, **keys**, and
**values** by linear maps of the residual stream. Scores are
`Q Kᵀ / √d`. Softmax turns scores into weights. The output is a
weighted sum of values.

One head is one subspace. **Multi-head attention (MHA)** runs `h`
heads in parallel and concatenates. The 2017 paper's bet was that
different heads specialize (syntax, copy, long-range). They often do.
They also waste KV memory, because every head stores its own keys and
values for every past token.

That memory is the **KV cache**. Decode is cheap on FLOPs and expensive
on the cache. Lab 18 is the arithmetic.

### MHA, GQA, MQA, MLA

Four ways to pay for that cache:

| Scheme | Keys and values | Typical use |
|---|---|---|
| **MHA** | one KV head per query head | textbooks, small models |
| **GQA** | query heads share groups of KV heads | Llama 2 70B, Llama 3, most 7B+ chat models |
| **MQA** | one KV head for all query heads | Falcon, PaLM-style decode, maximum cache save |
| **MLA** | KV compressed into a latent, then expanded | DeepSeek-V2/V3; long-context memory win |

**Grouped-query attention** is the 2024 default compromise: almost MHA
quality, closer to MQA memory. **Multi-query** is the extreme. **Multi-
head latent attention** (DeepSeek) stores a low-rank joint KV and
rebuilds heads on the fly. Read it as a cache codec, not as a new
kind of intelligence.

[transformer-explainer](https://github.com/zorost/transformer-explainer)
lets you switch these without a GPU. Brendan Bycroft's
[bbycroft.net/llm](https://bbycroft.net/llm) is the 3D walk through a
GPT-2-shaped stack.

### Positions: RoPE, ALiBi, YaRN

Attention is permutation-invariant without a position scheme.

- **RoPE** rotates each query and key in 2D planes by an angle that
  depends on position. The dot product then depends on **relative**
  offset. Llama, Qwen, Gemma, and most decoder-only models use some
  RoPE variant.
- **ALiBi** adds a linear penalty to attention scores as distance
  grows. No extra parameters. It extrapolates past the training
  length more gracefully than naive RoPE.
- **YaRN** (and related RoPE-scaling recipes) stretches the rotary
  wavelengths and adjusts attention temperature so a model trained at
  4k can be continued or inferred at 32k or 128k without inventing
  a new architecture. Long context is still a data and cache problem.
  The position scheme only stops the angles from wrapping into
  nonsense.

Sliding-window attention (Mistral-style) is a different knob: each
token sees a local window plus optional global sinks. Combine it with
GQA and the cache becomes a product choice, not a footnote.

### Residual stream and RMSNorm

A block is usually:

1. RMSNorm
2. Attention, add back to the stream
3. RMSNorm
4. MLP (SwiGLU in Llama-class models), add back

**Residual connections** are why depth trains. **RMSNorm** is LayerNorm
without mean subtraction: scale by root-mean-square, then a learned
gain. Cheaper, stable enough that Llama, Gemma, and Qwen standardized
on it. Pre-norm (norm before the sublayer) is the modern default.
Post-norm was the 2017 paper. If a run diverges at depth, check the
norm placement before you invent a new optimizer.

### Mixture of experts

The MLP is where most parameters live. A **MoE** layer replaces one MLP
with N experts and a **router** that picks k of them per token
(typically k=1 or 2). Sparse compute: Mixtral 8×7B has ~47B parameters
and roughly 13B active per token.

The router is a small linear map plus softmax or a sigmoid gate.
**Load imbalance** kills you: a few experts soak the batch, the rest
starve, and the all-to-all communication in expert parallel becomes a
tail latency problem. Training adds an auxiliary load-balancing loss
or uses loss-free balancing (DeepSeek-style). Serving MoE is an
operator problem (O1). Lab 17 is the router on tiny tensors.

Do not confuse MoE routing with mergekit. Merging stitches dense
weights offline. MoE is a runtime choice of which MLP runs.

### State-space models and hybrids

**SSMs** (Mamba and descendants) mix a sequence with a recurrent state
that updates in linear time, instead of quadratic attention. They scan.
They do not natively do the "this pronoun refers to that name 4k
tokens ago" lookup as cheaply as attention.

**Hybrids** interleave SSM blocks with attention blocks (Jamba, Samba,
Hymba, Griffin-class recipes). Attention keeps associative recall.
SSM keeps long-scan cost down. Decoder-only Transformers are still
the default you will fine-tune. Hybrids are a real serving option,
not a trivia category. If a card says "hybrid," ask which layers
are attention and what the cache looks like.

### Sampling

The model outputs logits. Everything after that is a policy.

- **Greedy**: argmax. Deterministic. Repeats and dullness on chat.
- **Beam search**: keep k partial strings, score the joint. Machine
  translation still uses it. Chat usually should not: beams collapse
  diversity and fight with temperature.
- **Temperature**: divide logits before softmax. T→0 approaches greedy.
  T>1 flattens. This is a distribution knob, not a "creativity" slider.
- **Top-k**: keep the k largest logits, renormalize.
- **Nucleus (top-p)**: smallest set whose cumulative probability
  exceeds p, then sample. The set size moves with the model's
  confidence.

Chat serving often combines temperature with top-p. Logit bias and
grammar sampling (JSON schema) are Engineer topics (E1). Lab 03 is
the four policies on a toy alphabet.

Train with teacher forcing (F3). Sample at inference. Those are
different loops. Speculative decoding (S10) is a faster way to
execute the same policy, not a fifth sampler.

## The gap most roadmaps leave

They draw one attention diagram from 2017 and stop. The missing
objects are the ones that decide VRAM, latency, and multilingual
cost in 2026:

| Object | Why it matters |
|---|---|
| Tokenizer fertility | bill, context fill, "the model is dumb on language X" |
| GQA / MLA | KV cache, not parameter count |
| RoPE vs YaRN | whether 128k is a flag or a trained fact |
| MoE routing | active params vs stored params |
| RMSNorm + residual | why the 32-layer stack trains at all |
| Nucleus vs beam | why your translation demo and your chatbot disagree |

If you can explain those six out loud, S2 is open.

## Practice

1. Lab `notebooks/01_tokenization_bpe.ipynb`. Encode the same sentence
   as English, as code, and as a second language. Count tokens.
2. Lab `notebooks/02_attention.ipynb`. One head, then two. Confirm
   `Q Kᵀ` shapes by hand.
3. Lab `notebooks/03_decoding_strategies.ipynb`. Greedy, temperature,
   top-k, nucleus on the same logits.
4. Lab `notebooks/17_moe_routing.ipynb`. Watch one expert soak the
   batch when the gate is untrained.
5. Lab `notebooks/18_kv_cache.ipynb`. Second token cheaper than the
   first.

Then open [transformer-explainer](https://github.com/zorost/transformer-explainer)
and [bbycroft.net/llm](https://bbycroft.net/llm). After that,
[nanoGPT](https://github.com/karpathy/nanoGPT) is a readable
decoder-only training loop, not a production engine.

## Watch and read

- 3Blue1Brown, [Attention in transformers](https://www.youtube.com/watch?v=wjZofJX0v4M) and [But what is a GPT?](https://www.youtube.com/watch?v=eMlx5fFNoYc)
- Andrej Karpathy, [Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY), [Let's build a tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE), [Deep Dive into LLMs](https://www.youtube.com/watch?v=7xTGNNLPyMI)
- Stanford [CS336](https://cs336.stanford.edu/), architecture and tokenization lectures ([2026 playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rMqXOcazWaTUHhq-yembLCV))
- Jay Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
- Lilian Weng, [Attention](https://lilianweng.github.io/posts/2018-06-24-attention/), [Transformer family](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/), [MoE](https://lilianweng.github.io/posts/2021-01-31-moe/)
- Hugging Face, [NLP course, Transformer chapter](https://huggingface.co/learn/nlp-course/chapter1/4)
- Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Su et al., [RoFormer / RoPE](https://arxiv.org/abs/2104.09864); Press et al., [ALiBi](https://arxiv.org/abs/2108.12409); Peng et al., [YaRN](https://arxiv.org/abs/2309.00071)
- Ainslie et al., [GQA](https://arxiv.org/abs/2305.13245); Shazeer, [MQA](https://arxiv.org/abs/1911.02150); DeepSeek-V2, [MLA](https://arxiv.org/abs/2405.04434)
- Mixtral, [MoE serving paper](https://arxiv.org/abs/2401.04088); Gu and Dao, [Mamba](https://arxiv.org/abs/2312.00752)
- Sebastian Raschka, [Build a Large Language Model (From Scratch)](https://github.com/rasbt/LLMs-from-scratch)

## Knowledge check

1. Why did most chat models drop the encoder?
2. What is the difference between BPE and Unigram tokenization?
3. Why does GQA exist if MHA already works?
4. Name one thing RoPE does that a learned absolute embedding does not.
5. When is beam search the wrong sampler?

<details>
<summary>Answers</summary>

1. Causal next-token training already consumes the context as a
   prefix. Cross-attention from a separate encoder is extra wiring
   unless the job is classic seq2seq. Chat, code, and agents are
   prefix jobs.
2. BPE greedily merges frequent pairs. Unigram starts large and prunes
   by likelihood; encoding is a segmentation search. Same vocab size
   does not mean the same splits.
3. KV cache grows with heads × sequence × batch. GQA shares KV across
   groups of query heads so decode fits in memory with a small quality
   cost.
4. Relative offset appears in the dot product through rotations, which
   is why length extrapolation recipes (YaRN and friends) can retune
   angles instead of retraining a table of absolute vectors.
5. Open-ended chat. Beams collapse diverse continuations and fight
   temperature. Use beams for translation or other tasks with a
   narrow set of good strings.

</details>
