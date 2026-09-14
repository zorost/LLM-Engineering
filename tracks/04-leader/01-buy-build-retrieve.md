# L1 · Buy, build, retrieve, or fine-tune

## Why it exists

Most LLM programs fail at the choice of move, not at the choice of
model. They fine-tune when a prompt would do, retrieve nothing when
the facts change daily, or build a platform because a slide said
"own the stack." This module is the decision in one page, then the
book-length version.

## The idea

Write an **eval** before you write a purchase order. The eval names
the task, the user, the stakes, the metric, and the failure the user
will not forgive. Until that exists, every architecture is theater.
S6 and E10 are the engineering form. Here you only need to insist
that it exists and that it is rerunnable.

Then pick the **cheapest move that hits that eval**. The usual ladder,
cheapest first, is:

1. **Prompt a hosted model.** Change instructions, tools off, single
   call. Buy API time. Good when the knowledge is in the model or the
   user supplies the text, and the format is easy.
2. **Constrain the output.** JSON schema, regex, enumerations (E1,
   lab 11). Good when the model can think but the downstream system
   cannot parse prose.
3. **Retrieve, then generate (RAG).** Your corpus, citations, freshness
   (E3, E4). Good when answers must be grounded in documents you own
   and those documents change faster than weights.
4. **Tools and workflows.** Search, SQL, tickets, calculators, MCP
   (E5, E9). Good when the job is an action or a lookup the model
   should not memorize.
5. **Fine-tune or adapter.** SFT, then preference methods if you must
   (S4, S5). Good when the *form* or *local dialect* is stable, data
   exists, and a smaller model plus adapter beats a larger prompted
   model on the eval **and** on cost (O3).
6. **Train or heavily adapt a base model.** Rare. A research or data
   advantage, a license wall, or a regulated air gap. Read S2 before
   you fund it.

"Buy versus build" is orthogonal to that ladder. You can buy the
model and build the retrieval. You can build nothing but a prompt in
a vendor studio. You can self-host (O1) because of data residency,
unit economics at volume, or a license, not because ownership is a
personality trait.

A compact rule:

- **Facts that move** → retrieve (or tools), do not bake into weights.
- **Behavior and format that do not move** → prompt first, fine-tune
  if the eval and the cost model agree.
- **Actions** → tools with contracts, not a bigger context window.
- **Privacy / residency / license** → may force self-host or a
  specific vendor, even if the API is cheaper this quarter.

Draw the **seams** before you fund the stack: where untrusted text
enters, where a model decides, where a tool writes, where a person
must approve. *AI Engineering Distilled* exists so that drawing is a
notation (Boundary and Context views), not a box labeled "AI." *The
AI Leadership Textbook* exists so the same choice can be explained
to a board: silicon, vendors, risk, and money in one field guide.
Read both. This module will not replace them.

### What "buy" actually buys

A hosted API buys uptime, a model revision train, and a legal paper
trail you still have to read. It does not buy an eval, a retrieval
index, or a product manager. A self-hosted engine buys control of
weights and logs, and it buys O1 to O4 as a permanent job. A
marketplace fine-tune buys someone else's data habits. Read the model
card and the dataset card (S11) as if they were contracts. They are.

### What "build" actually builds

Application code, eval harnesses, indexes, gateways, and runbooks.
Weights are the expensive special case. Most organizations should
build the **system** and rent the **model** until the numbers in O3
flip. Distilled's Configuration view is the reminder that the system
is the prompts, indexes, and flags, not only the network weights.

## The gap most roadmaps leave

They jump to LoRA because LoRA is a notebook. They never force the
ladder. They treat "build our own model" as prestige. They also skip
the seam drawing, so security and tool rights appear after the demo
is already in customers' hands.

## Practice

No lab. Do this in a document your budget committee could read:

1. Name one real task. Write the eval in six lines: user, input,
   output, metric, sample size, unforgivable failure.
2. Walk the ladder. For each rung, write "hits eval?" and "cost
   driver." Stop at the first honest yes.
3. Draw one Boundary view: untrusted inputs, model call, tools,
   human gate. If you do not have Distilled yet, a labeled diagram
   is enough. Then buy the book and redraw it in Seam.
4. Open the Amazon look-inside for *The AI Leadership Textbook*
   ([Kindle](https://www.amazon.com/dp/B0HHTJHK5R)) and read the
   chapters that cover make-versus-buy and platform choice. Come
   back and tighten your memo.

## Watch and read

- Hashemipour, *The AI Leadership Textbook* (2026). Silicon to
  boardroom. Full citation in [BOOKS.md](../../reference/BOOKS.md).
- Hashemipour, *AI Engineering Distilled* (2026). Seam notation,
  Boundary and Context views.
- Chip Huyen, *AI Engineering*, on the application development
  process and RAG versus fine-tune (independent; O'Reilly).
- Andrew Ng, [The AI Engineering Skills Map](https://www.deeplearning.ai/the-batch/the-ai-engineering-skills-map)
  (independent; DeepLearning.AI, 2026).
- This course: E3, S4, O3.

## Knowledge check

1. Why does the eval belong before the architecture?
2. When is RAG the wrong next step after a prompt fails?
3. When is fine-tuning a cost strategy rather than a ritual?
4. Name a reason to self-host that is not "we like owning GPUs."
5. What is a seam, in one sentence a director can repeat?

<details>
<summary>Answers</summary>

1. Without a rerunnable eval, you cannot tell whether a prompt, RAG,
   or adapter actually won. You will fund the most exciting diagram.
2. When the failure is format, policy, or style on text the user
   already provided, or when the job is an action. Retrieval fixes
   missing or stale facts you own.
3. When a smaller adapted model meets the eval at lower serving
   cost than prompting a larger one, and you have data and a
   harness. Not when you lack documents and hope weights will
   memorize the intranet.
4. Data residency, a license that forbids the API, unit economics
   at sustained volume, or an air-gapped network.
5. A named place where untrusted text, a model decision, a tool
   write, or a human approval crosses a boundary you can control.

</details>
