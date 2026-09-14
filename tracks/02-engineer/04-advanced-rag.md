# E4 · Advanced RAG

## Why it exists

Naive dense top-k is the control experiment, not the product.
Real corpora mix SKUs and prose, tables and graphs, questions
that are really SQL. This module is the next layer: query
construction, hybrid search, fusion, rerank, late interaction,
graphs as a *concept*, and DSPy when the pipeline itself needs
an optimizer. Lab 09 is the required hands. Cloud-scale graphs
and text-to-SQL platforms wait for E12.

## The idea

### Query construction

Not every question wants a vector.

- **Rewrite and decompose.** Multi-hop questions become a
  sequence of lookups (the cheap cousin of CoRAG).
- **Text-to-SQL.** The answer lives in a warehouse. The model
  writes SQL (or a query builder calls an API). The control
  is a schema dump, a read-only role, a limit clause, and an
  eval on *query plus result*, not on fluency. Never let the
  model issue unconstrained DDL.
- **Text-to-Cypher** (or another graph query language). Same
  shape: schema, read-only, eval on the query. Use when the
  question is a relation ("which carriers serve both ports")
  rather than a paragraph.

Tools (E5) are how these constructors get called. The
constructor is still a typed function with a contract (E9).

### Hybrid search and fusion

Sparse (BM25) catches exact tokens. Dense catches paraphrase.
**Hybrid** runs both, then merges.

**Reciprocal rank fusion (RRF)** is the usual merge: a chunk
that ranked well in *either* list rises. You do not have to
calibrate two score scales. Tune k and the RRF constant on
labeled queries.

**RAG-fusion** generates several rewritten queries, retrieves
for each, then fuses (often RRF). It is multi-query plus
hybrid thinking. Cost scales with the number of rewrites.

Lab `09_hybrid_retrieval.ipynb` is sparse plus dense, then a
rerank. That is the whole argument in tensors.

### Rerank

Bi-encoders are fast and coarse. A **cross-encoder** reranker
scores (query, chunk) jointly on the top 20 to 50. Latency is
acceptable on a shortlist. After hybrid, this is the usual
next precision move.

Dedicated rerank APIs exist. A small cross-encoder you host
is enough to learn the shape. Do not rerank 10,000 chunks.

### Late interaction (ColBERT)

[ColBERT](https://github.com/stanford-futuredata/ColBERT)
(Khattab and Zaharia) keeps a vector **per token** and
computes similarity as a late interaction (MaxSim) between
query tokens and document tokens. You get more of the
cross-encoder's precision without scoring every pair from
scratch at query time, at the cost of a larger index than a
single vector per chunk.

RAGatouille and similar wrappers exist so you do not have to
start from the paper's training code. Conceptual takeaway:
one vector per chunk is a bottleneck. Late interaction is the
principled middle. Use it when hybrid plus rerank still
misses, and you can pay storage.

### GraphRAG, conceptually

A knowledge graph stores entities and relations. Retrieval
can walk the graph (neighbors of "Lane LHR-JFK") instead of,
or before, dense search. Microsoft's
[GraphRAG](https://microsoft.github.io/graphrag/) popularized
a pattern: LLM-extract a graph from a corpus, community
summaries, then answer with both local neighbors and global
summaries.

The idea you need: **when the question is structural**,
vectors of prose are the wrong index. When the question is
"summarize the themes," community summaries can beat chunk
lottery. Graphs are not a default. Extraction is expensive
and stale unless you operate it. Training 01 week 7 is a
lab-sized graph. This module stops at the decision.

### DSPy

[DSPy](https://dspy.ai/) treats the RAG (or agent) pipeline as
a program: signatures, modules, and an optimizer that tunes
prompts or weights against a metric. You stop hand-editing a
string when the metric moves. That is the point. It is not a
retriever. It is how you search the space of prompts and
few-shots with the same seriousness as hyperparameters.

Use it after you have a metric (E3, E10) and a pipeline you
could explain without DSPy. Otherwise you are optimizing fog.

## The gap most roadmaps leave

They dump twenty paper names. Production teams need a
**ladder**:

1. Hybrid + RRF.
2. Rerank the shortlist.
3. Query rewrite or fusion if recall is the miss.
4. SQL/Cypher when the source of truth is structured.
5. Late interaction or a graph when the ladder below has
   numbers that say so.

Skipping to GraphRAG because a vendor keynote did is how
budgets disappear. Lab 09 is step 1 and 2. Stay there until
the table is boring.

## Practice

Lab `09_hybrid_retrieval.ipynb`.

1. Record recall@10 for dense-only, sparse-only, hybrid.
2. Add a rerank on the hybrid shortlist. Record precision@5.
3. Write three error ids: a BM25-only win, a dense-only win,
   a still-miss. That is the design review.

Going further: sketch, do not implement, a text-to-SQL tool
for a two-table schema. List the guards (read-only, limit,
allow-list of tables). Optional DSPy tutorial on
[dspy.ai](https://dspy.ai/) once lab 12 exists in your
muscle memory.

## Watch and read

- ColBERT, [github.com/stanford-futuredata/ColBERT](https://github.com/stanford-futuredata/ColBERT)
  and the SIGIR 2020 paper
- RAG-fusion write-ups via LangChain's query-transform docs:
  [python.langchain.com](https://python.langchain.com/docs/how_to/MultiQueryRetriever/)
- Reciprocal rank fusion: Cormack et al., SIGIR 2009
- GraphRAG, [microsoft.github.io/graphrag](https://microsoft.github.io/graphrag/)
- DSPy, [dspy.ai](https://dspy.ai/)
- LlamaIndex, [query engines / routers](https://docs.llamaindex.ai/)
  (orchestrator, after the idea)
- Training 01, week 7 RAG and graph notebooks in
  [AI Engineering Lab](https://github.com/zorost/AI-Engineering-Lab)
  if you want a second corpus. Do not copy them here.

## Knowledge check

1. Why does RRF beat naive score addition for hybrid search?
2. What does a cross-encoder see that a bi-encoder does not?
3. When is text-to-SQL the retrieval system?
4. What storage cost does ColBERT accept, and why?
5. What must you already have before DSPy is worth importing?

<details>
<summary>Answers</summary>

1. BM25 and cosine are on different scales. Rank positions
   are comparable. RRF merges ranks.
2. The pair (query, document) in one forward pass, so
   interactions between terms are scored together. The
   bi-encoder never sees them in the same encoder call.
3. When the answer is a row aggregate or a join, not a
   paragraph. The "retriever" is the warehouse; the model
   constructs a query under guards.
4. Token-level vectors per document, so the index is much
   larger than one vector per chunk. You pay RAM/disk for
   finer matching.
5. A pipeline with named stages and a metric you trust. DSPy
   optimizes that. It will not invent the metric.

</details>
