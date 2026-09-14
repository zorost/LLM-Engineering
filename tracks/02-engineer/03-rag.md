# E3 · Retrieval-augmented generation

## Why it exists

A foundation model does not know your policy manual, your tickets,
or this morning's table. RAG fetches passages from a corpus you
control and asks the model to answer *from those passages*, with
citations. Freshness is a re-index. Permissions are a filter.
Hallucinated procedure is the failure mode this exists to catch.

## The idea

### The pipeline is the idea

```
ingest → chunk → embed → index → retrieve → (rerank) → generate + cite
```

E2 is the left half. This module is retrieve, generate, and
*measure the two stages apart*. LangChain and LlamaIndex can
wire the arrows. They are orchestrators. They are not RAG. If
you cannot draw the pipeline on a whiteboard without a class
name from either library, you are not ready to import them.

A generator that never saw the right chunk cannot be faithful.
A retriever that always returns the right chunk still needs a
model that will not ignore it. Those are two evals.

### Retrievers

**Dense.** Embed the query, k-NN in the vector index (E2).

**Sparse.** BM25 / keyword. Precision on rare tokens, SKUs,
error codes, names. Hybrid with fusion is E4; know that dense
alone misses them.

**Query rewriting.** The user said "that fee." The retriever
needs "customs exam fee on inbound ocean FCL." A small model
call expands pronouns and domain terms. Cheap when recall@k is
the bottleneck.

**Multi-query.** Several paraphrases, retrieve for each, union
or fuse. More recall, more latency, more duplicates.

**HyDE.** Hypothetical Document Embeddings (Gao et al.,
[arXiv:2212.10496](https://arxiv.org/abs/2212.10496)). The
model writes a short *imagined* answer. You embed that, not the
question. The hypothetical sits closer to a real passage than a
terse query does. It also invents facts; the dense bottleneck
is supposed to wash the fiction. Use when questions and
documents live in different registers. Measure the extra call.

**CoRAG.** Chain-of-Retrieval Augmented Generation
([arXiv:2501.14342](https://arxiv.org/abs/2501.14342)). One
retrieval is not enough for multi-hop questions. The system
issues a sequence of queries, each conditioned on what it
already saw, then answers. That is test-time compute spent on
search. It is not a default for "what is the refund window."

Rerankers, RAG-fusion, ColBERT, and graphs are E4. MCP appears
when the retriever is a *tool* an agent can call rather than a
fixed first stage: the same index, a schema for `search(query,
k, filters)`, hosted as a server. E5 and E9. Mention it here so
you do not rebuild RAG inside every agent framework.

### Grounding and citations

The generation prompt has a job:

1. Answer only from the supplied chunks.
2. Cite chunk ids (or URLs) on claims.
3. Say you do not know when the chunks do not contain the
   answer.

That is an instruction, not a guarantee. Models will still
blend parametric memory with the context. Faithfulness evals
exist because of that. Never concatenate retrieved text into
the system prompt as if it were policy. Retrieved text is
untrusted data. Delimit it. See E8.

Permissions: filter the index *before* the model sees chunks.
A prompt that says "do not reveal other tenants' docs" is not
an ACL.

### Measuring RAG

You need labels. A golden set is: question, acceptable answer
(or rubric), and the chunk ids that *should* have been
retrieved. Without the third, you cannot tell retrieval from
generation.

**Retrieval metrics**

- Recall@k: did a gold chunk appear in the top k?
- Precision@k: of the k, how many were useful?
- MRR / nDCG if order matters before rerank.

**Generation metrics, grounded**

- **Faithfulness:** claims in the answer are supported by the
  retrieved context. The model may be fluent and still invent.
- **Answer relevancy:** the answer addresses the question.
- **Context precision / context recall:** did we retrieve
  signal, and enough of it?

[RAGAS](https://docs.ragas.io/) and [DeepEval](https://docs.confident-ai.com/)
implement these (often with an LLM-as-judge plus embeddings).
Judges need a rubric and a spot-check against humans. A
faithfulness number you cannot replay from traces is a vibe.
Lab 12 is the harness shape; use it on RAG, not only on
prompts.

Error buckets that actually get fixed: miss (gold chunk absent),
wrong chunk (index noise), uncited claim, refusal when the
chunk was there, citation to a chunk that does not support the
sentence. E10 is how those buckets become a release gate.

## The gap most roadmaps leave

They demo a chatbot on a PDF and call it RAG. They skip:

- Retrieval eval without the generator.
- "I don't know" as a first-class label.
- ACL and tenancy on the index.
- Orchestrator lock-in: the pipeline is five functions. A
  library that hides them becomes the system.

Frameworks are allowed after you can replace them. Then they
save time on loaders, retries, and tracing.

## Practice

Lab `08_embeddings_rag.ipynb` again, this time for generation:

1. Keep the recall@5 table from E2.
2. Generate answers with a "cite or abstain" instruction.
   A tiny local model or a mocked generator is enough to
   practice the *protocol*.
3. Hand-score five answers: faithful, relevant, cited.

Optional: run the same five through a RAGAS or DeepEval
faithfulness check once you have an API key, and compare to
your hand labels. Disagreement is the lesson.

## Watch and read

- Lewis et al., RAG, [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- HyDE, [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
- CoRAG, [arXiv:2501.14342](https://arxiv.org/abs/2501.14342)
- RAGAS, [docs](https://docs.ragas.io/)
- DeepEval, [docs](https://docs.confident-ai.com/)
- LangChain, [docs](https://python.langchain.com/) (orchestrator)
- LlamaIndex, [docs](https://docs.llamaindex.ai/) (orchestrator)
- MCP, [modelcontextprotocol.io](https://modelcontextprotocol.io/)
  (retriever as a tool)
- Chip Huyen, *AI Engineering*, retrieval chapters (book)

## Knowledge check

1. Why measure retrieval and generation on separate scores?
2. What problem is HyDE trying to fix, and what new cost does
   it add?
3. Why is "answer from the context" not a security control?
4. Name three RAGAS/DeepEval-style quantities and what a drop
   in each would make you inspect first.
5. Where does MCP belong in a RAG system?

<details>
<summary>Answers</summary>

1. A wrong answer can be a miss in the index or a fluent
   ignore of a good chunk. One number hides which team should
   act.
2. Query and document live in different language; a
   hypothetical answer is closer to passage style. Cost: an
   extra generation, latency, and invented details that can
   drag retrieval toward the wrong neighborhood.
3. The model can be talked out of it, and retrieved text can
   contain instructions. ACLs, output filters, and treating
   context as data are controls. The sentence is a hope.
4. Faithfulness → generator or mixed memory; context recall →
   chunking, embedding, k; context precision → noise in the
   top k, need a reranker (E4).
5. Expose `search` (and maybe `fetch_by_id`) as a typed tool
   a host can call. The index stays one service. Agents (E5)
   do not each embed the corpus.

</details>
