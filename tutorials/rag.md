# Tutorial · RAG

## Why it exists

Retrieval-augmented generation is the default grounded system in
this course (L1). Labs 08 and 09 exist so you can see a citation
fail for a reason you can name: chunking, embedding, metric, or
ranker, not "the LLM hallucinated" as a personality flaw.

## The idea

RAG is four systems glued together:

1. **Ingest.** Load documents, preserve source ids, split into
   **chunks** with overlap you can justify. Chunking is a product
   decision: too small loses meaning, too large wastes the window
   and dilutes the embedding.
2. **Index.** Embed chunks (dense), and usually also index
   **sparse** terms (BM25 or similar). Store metadata: title, url,
   date, access control.
3. **Retrieve.** Embed the query, take top-k, optionally **hybrid**
   with sparse, optionally **rerank** with a cross-encoder. This
   is lab 08 then 09.
4. **Generate.** Pack the window with the ranked chunks, instruct
   the model to answer **only** from them, and ask for **citations**
   that map to chunk ids. Then **measure** faithfulness (did the
   answer stick to the chunks?) and answer relevance.

The embedding model is a second model with its own tokenizer and
license. Do not mix embedding spaces. Re-embed when you change the
model. Cosine similarity on normalized vectors is the usual dense
metric. It is a ranking heuristic, not a proof of truth.

**Hallucination** in RAG is often a retrieval miss, a chunk that
almost matches, or a prompt that allows the model to fill gaps
from pretraining. Fix retrieval and the prompt before you fine-tune.

Advanced moves (E4): query rewrite, HyDE, parent-document retrieval,
graph edges, text-to-SQL for tables. Each one is a new failure
mode. Do not add them until lab 08's error buckets are boring.

## The gap most tutorials leave

They print a LangChain diagram and never score **faithfulness**.
They chunk at 512 because a blog did. They evaluate on questions
that appear verbatim in the chunks (the exam was in the textbook).

## How the labs should feel

**Lab 08.** A tiny corpus you can read in full. You will watch a
wrong chunk win because the embedding liked a shared rare word.
You will force a citation. You should feel that RAG is information
retrieval plus a generator, not magic.

**Lab 09.** Sparse plus dense, then a rerank step. You should see a
query where BM25 wins and a query where dense wins. If both labs
always "just work," sabotage the corpus (swap a label, split a
table badly) and try again.

## Practice

1. `08_embeddings_rag.ipynb` then `09_hybrid_retrieval.ipynb`.
2. Write five questions: two easy (answer in one chunk), two hard
   (need two chunks), one impossible (not in the corpus). The
   impossible one must produce a refusal or "not in sources," not
   a fluent guess.
3. Optional: run a faithfulness metric from Ragas or a simple
   checklist you wrote. DeepEval is another harness
   ([TOOLS.md](../reference/TOOLS.md)). The metric is a tool. The
   golden questions are the product.

## Watch and read

- Lewis et al., RAG, 2020, [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)
- E3 and E4 in this course
- Hugging Face and DeepLearning.AI RAG courses as pointers
  ([COURSES.md](../reference/COURSES.md))
- Chip Huyen, *AI Engineering*, RAG chapters

## Knowledge check

1. What does a citation that cannot be mapped to a chunk id tell
   you?
2. Why hybrid search?
3. Why is a question copied from a chunk a weak eval item?
4. What should the model do when retrieval returns nothing useful?
5. When does L1 say to stop at RAG and not fine-tune?

<details>
<summary>Answers</summary>

1. The generator invented a source, or your prompt did not bind
   citations to ids. Either way the grounding contract failed.
2. Sparse lexical match catches identifiers and rare terms.
   Dense catch paraphrases. They fail on different queries.
3. It tests extractive copy, not retrieval under paraphrase, and
   it inflates scores. Include paraphrases and impossible
   questions.
4. Refuse or say the corpus does not contain it. Not "a helpful
   guess."
5. When the failure was missing or stale facts you own, and the
   eval is hit once retrieval and citations work. Fine-tune if
   the remaining gap is form or dialect, not facts.

</details>
