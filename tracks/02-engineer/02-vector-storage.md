# E2 · Vector storage

## Why it exists

Retrieval starts before the generator. If the right passage is not
in the index, or is split in the wrong place, or is compared with
the wrong metric, no prompt will find it. This module is ingest,
chunk, embed, store, and a first retrieve. Generation is E3.

## The idea

### The objects

A **document** is a source (PDF, HTML, ticket, markdown, row). A
**chunk** is the unit you embed and retrieve. An **embedding** is
a dense vector for that chunk. An **index** stores vectors plus
the raw text and metadata (source id, page, ACL, timestamp). A
**query vector** is the same embedding model run on the question
(or on a rewrite of it). **k-NN** (or ANN) returns the nearest
chunks under a similarity.

Cosine similarity is a normalized dot product. Inner product and
L2 show up too. The metric must match how the embedding was
trained. Mixing them is a silent bug.

### Loaders and splitters

Loaders turn files into text. They are plumbing. PDF extraction,
HTML stripping, and table handling decide the ceiling of the
whole pipeline. Garbage in is not a retrieval research problem.

Splitters cut text into chunks:

- **Fixed size** with overlap. Predictable. Cuts mid-sentence
  unless you also split on punctuation.
- **Recursive character.** Try paragraph, then sentence, then
  character, so you keep structure when you can. The default
  that most libraries ship, for a reason.
- **Header-aware / Markdown.** Split on `#` headings so a
  section stays a section. The right default for docs, ADRs,
  and policy manuals.
- **Semantic splitters** (embed, cut where similarity drops).
  Sometimes better, always slower to build, harder to debug.
  Measure against recursive on *your* corpus before you keep
  them.

Chunk size is a product knob. Too large: the answer sentence is
diluted. Too small: the chunk has no meaning. Overlap is how you
survive a sentence that straddled a boundary. Start around 256
to 512 tokens with a small overlap, then move only when recall
or faithfulness (E3) tells you to.

Metadata is not optional. Source URI, title, section, as-of
date, and permission tags travel with the chunk. Citations and
ACL filters are metadata problems.

### Embeddings

A **bi-encoder** embeds query and document separately. Retrieval
is a nearest-neighbor lookup. That is how you search millions of
chunks. A **cross-encoder** reads query and document together
and scores the pair. Too slow for the first pass. Use it to
**rerank** a shortlist (E4).

[sentence-transformers](https://www.sbert.net/) is the Python
library you will actually import. The Hub is full of embedding
checkpoints. Read the card: language, context length, license,
whether it was trained for retrieval or for clustering.

**MTEB** ([huggingface.co/spaces/mteb/leaderboard](https://huggingface.co/spaces/mteb/leaderboard),
docs at [embeddings-benchmark.github.io/mteb](https://embeddings-benchmark.github.io/mteb/))
is the public retrieval and embedding leaderboard. It is a
starting shortlist, not your eval. Domain shift is the rule, not
the exception. Embed a held-out slice of *your* corpus and rank
with labeled queries before you freeze a model.

English-only embeddings punish other languages and code. Matryoshka
and other shorten-the-vector tricks trade a little quality for
RAM. Dimension is a bill.

Do not embed PII you are not allowed to store. The vector is a
lossy copy of the text, not an anonymizer.

### Stores

The store is an index plus metadata filters plus a backup story.

| Store | Shape | When it is the right size |
|---|---|---|
| [Chroma](https://docs.trychroma.com/) | Local / small server, simple API | Prototypes, labs, single-box apps |
| [FAISS](https://github.com/facebookresearch/faiss) | Library, not a database | You own the process; research and custom indexes |
| [Pinecone](https://docs.pinecone.io/) | Managed cloud | You want an SLA and do not want to run ANN |
| [Milvus](https://milvus.io/docs) | Open, scalable | You need scale and you will operate it (or use Zilliz) |

pgvector, Weaviate, Qdrant, OpenSearch, and Databricks Vector
Search appear in real shops. The idea does not change: ANN index,
filters, payload. Pick on operations (backup, VPC, IAM, cost at
your QPS), not on a blog benchmark of 10k toy vectors.

ANN (HNSW, IVF, DiskANN) is approximate. You trade recall for
latency. Record recall@k on a labeled set when you change
`efSearch` or `nprobe`. Exact search is a debugging mode.

Hybrid retrieval (BM25 plus dense) is E4. You still need a
keyword index next to this one. Classical NLP did not retire.

## The gap most roadmaps leave

They say "use Chroma" and skip **the index as data**:

- Re-embedding after a model change is a migration, with two
  indexes and a cutover, not a flag.
- Deletes and updates. Stale chunks answer with last quarter's
  policy. Tombstones and as-of dates are product features.
- ACL at retrieve time. Filtering after generation is too late.
- The embedding model and the chunker are coupled. Changing one
  without re-measuring recall is how RAG "regresses" overnight.

Lab 08 is small enough that FAISS-in-process is enough. Pretend
it is production anyway: store source ids.

## Practice

Lab `08_embeddings_rag.ipynb`: chunk, embed, retrieve, cite.
Before you touch the generator:

1. Build three chunkings (small, medium, header-aware) of the
   same tiny corpus.
2. Label ten questions with the chunk id that *should* return.
3. Report recall@5 for each chunking.

That table is the module. The chatbot demo is optional.

Going further: embed the same corpus with two
sentence-transformers models from MTEB's retrieval slice and
compare the table. Keep licenses clean.

## Watch and read

- sentence-transformers, [sbert.net](https://www.sbert.net/)
- MTEB, [leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
  and [docs](https://embeddings-benchmark.github.io/mteb/)
- Chroma, [docs](https://docs.trychroma.com/)
- Pinecone, [docs](https://docs.pinecone.io/)
- Milvus, [docs](https://milvus.io/docs)
- FAISS, [wiki](https://github.com/facebookresearch/faiss/wiki)
- Hugging Face, [Getting Started With Embeddings](https://huggingface.co/blog/getting-started-with-embeddings)
- Pinecone learning, [chunking strategies](https://www.pinecone.io/learn/chunking-strategies/)
  (vendor text; read as a catalog of splits, not as doctrine)

## Knowledge check

1. Why is cosine the default metric for many embedding models?
2. What does a recursive splitter try to preserve that a naive
   character slice does not?
3. Why is MTEB not a purchase order?
4. When is FAISS the wrong product?
5. What must travel with every stored vector besides the floats?

<details>
<summary>Answers</summary>

1. Those models were trained so that related texts have high
   directional similarity. Cosine (normalized dot product)
   matches that geometry. Confirm on the card; some models want
   inner product on already-normalized vectors.
2. Larger semantic units (paragraphs, then sentences) until the
   size budget forces a cut.
3. It ranks models on public tasks. Your corpus, languages, and
   query style can reorder the list. Run a labeled slice.
4. When you need a database: replication, metadata query, IAM,
   backups, multi-tenant filters. FAISS is an ANN library in
   your process.
5. The chunk text (or a pointer to it), a stable source id, and
   the metadata you will filter and cite on (time, ACL, section).

</details>
