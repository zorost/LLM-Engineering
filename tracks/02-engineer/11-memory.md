# E11 · Memory and conversation

## Why it exists

Chat products pretend the model "remembers." It does not.
You feed it tokens from a store you designed. Buffer,
summary, and RAG-over-history are three stores with three
ways to **lie**. If you cannot name the lie, you will
debug personality instead of data.

## The idea

### There is no durable memory in the weights of a call

Each request sees only what you pack (E9). Vendor "memory"
features are extra retrieval or extra prefixes they store
for you. Your application still needs a policy: what is
stored, for how long, for whom, under which ACL, with
which eval.

### Buffer memory

Keep the last *n* turns (or last *k* tokens) verbatim.

**What it is good for.** Short tasks, pronouns, the file
the user just pasted.

**How it lies.** It drops the commitment from turn 2 when
*n* is small. It repeats a corrected error if the wrong
turn is still inside *n*. It spends the window on greetings.
It can re-inject a prompt-injection from an old tool
observation if you never sanitized history (E8).

**Control.** Token budget, strip tool dumps, never store
secrets, per-tenant isolation.

### Summary memory

A running synopsis: "User is a shipper on lane X, prefers
email." Updated every few turns by the model (or a smaller
model).

**What it is good for.** Long sessions where the buffer
cannot hold the plot.

**How it lies.** Summaries invent preferences, drop
negations ("do *not* use carrier Y" becomes "uses Y"),
and freeze stale facts. They are generations. They need
the same faithfulness mindset as RAG answers (E3). A
summary without a link to source turn ids cannot be
audited.

**Control.** Regenerate from a buffer of ids, not from the
previous summary only (avoid telephone). Put high-stakes
facts (account id, legal basis) in a structured profile,
not in prose memory. Eval: after a session, can a judge
(or you) find a fabricated preference?

### RAG memory

Embed past turns, tickets, or notes. Retrieve the relevant
ones. This is E2/E3 on a conversation corpus.

**What it is good for.** "What did we decide last quarter?"
when that decision is a document. Cross-session recall
with ACL.

**How it lies.** Wrong neighbor: it retrieves a *different*
customer's thread if tenant filters fail. Right neighbor,
wrong time: an outdated policy chunk. Summarized memories
in the index compound summary lies with retrieval misses.
Hybrid search still applies (E4) for names and ticket ids.

**Control.** Tenant key on every vector, as-of timestamps,
citation back to the turn or ticket, the same recall@k
table you built in E2.

### Profiles and working memory

A **structured profile** (JSON you validate) is not a
chat summary. Preferences the user confirmed belong there.
**Working memory** inside an agent loop (the scratchpad)
is the ReAct thought stream. It should be ephemeral unless
you deliberately persist it. Persisting thoughts can leak
chain-of-thought and private tool data.

### What to store

Ask, for each field: is it required for the next task,
allowed by policy, and testable? Default to not storing.
Retention and deletion are product features. Memory is
personal data even when it is "just chat."

Agents (E5) plus memory is how systems get confidently
wrong across days. E10 gates should include a "memory
lie" slice: inject a negation, confirm the next session
still honors it.

## The gap most roadmaps leave

They show `ConversationBufferMemory` in a framework and
move on. The gap is **epistemology**:

| Store | Typical lie |
|---|---|
| Buffer | Amnesia past *n*; repetition of errors |
| Summary | Fabricated or inverted facts |
| RAG memory | Wrong person, wrong time |
| Vendor memory | Unclear retention; hard to eval |

Framework memory classes are buffers and summarizers with
brand names. Draw the store. Then import.

## Practice

Lab `08_embeddings_rag.ipynb` as a memory index: treat
five synthetic "past turns" as documents. Ask a follow-up
that requires turn 2. Report whether retrieve + generate
honored a negation you planted in turn 2.

On paper: for a support bot, assign each of (account id,
last intent, user tone, legal disclaimer) to buffer,
summary, profile, or RAG. One sentence on how that slot
fails.

No extra notebook is required. If you skip the planted
negation, you have not tested memory.

## Watch and read

- LangChain, [memory concepts](https://python.langchain.com/docs/concepts/memory/)
  (catalog of types; orchestrator)
- LlamaIndex, [chat memory](https://docs.llamaindex.ai/)
- MCP resources as a memory backend:
  [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- E3 faithfulness: summaries are generations
- Anthropic, [contextual retrieval](https://www.anthropic.com/news/contextual-retrieval)
  (related: packing evidence, not a memory silver bullet)
- Training 01 week 14 memory notes in
  [AI Engineering Lab](https://github.com/zorost/AI-Engineering-Lab)
  if you want the longer agent treatment

## Knowledge check

1. Why is "the model remembered" a misstatement?
2. How does a summary invert a negation?
3. What ACL mistake is unique to RAG memory versus a
   single-tenant buffer?
4. Where should an account id live instead of in a prose
   synopsis?
5. What eval catches a memory lie that a single-turn
   golden set will miss?

<details>
<summary>Answers</summary>

1. The weights are not updated by the chat. You (or a
   vendor store) supplied tokens from a buffer, summary,
   or index.
2. The summarizer drops "not" or compresses "never use X"
   into "discussed X." The next turn treats X as allowed.
3. Vectors from another tenant (or another ticket) can
   enter the window if filters are missing. A local buffer
   in one session does not search other people by default.
4. A structured, validated profile (or the source system of
   record), cited, not a sentence in a rolling summary.
5. A two-session (or compacted-history) test: plant a fact
   or a negation, run the memory path, score whether it
   survives. Single-turn evals never exercise the store.

</details>
