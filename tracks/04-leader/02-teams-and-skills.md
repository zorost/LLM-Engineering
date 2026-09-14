# L2 · Teams and skills

## Why it exists

Leaders staff LLM work as if they were cloning a 2018 research lab, or
as if one "prompt engineer" were a department. Both mistakes are
expensive. This module is who you actually need, mapped to a public
skills model we did not write.

## The idea

### Ng's map, used independently

In August 2026, Andrew Ng and DeepLearning.AI published **The AI
Engineering Skills Map** in The Batch (issue 366), based on job
postings and interviews they describe in that letter. The four
top-level skills they name are:

1. **Building and deploying AI applications**
2. **Software engineering fundamentals**
3. **Using coding agents**
4. **Shaping the build**

Follow-up letters unpack the first skill into sub-skills such as
LLM foundations, grounding with data, agentic systems,
evaluation-driven development, operating in production, and machine
learning foundations. Read the [primary letter](https://www.deeplearning.ai/the-batch/the-ai-engineering-skills-map)
and [issue 366](https://www.deeplearning.ai/the-batch/issue-366).
Read Ng's later parts on [andrewng.org/writing](https://www.andrewng.org/writing)
as they appear.

**We are not affiliated with Ng or DeepLearning.AI.** We use the map
because it matches what hiring actually asks for in 2026, and because
it names **shaping the build** and **evals** instead of treating
"knows PyTorch" as the job. Where this course disagrees, it says so.
Where we staff a Zorost Lab team, we still hire for these four, then
add domain and governance depth the map does not try to exhaust.

How the map sits on this repository:

| Ng skill | Where it lives here |
|---|---|
| Building and deploying applications | Engineer track, L1 ladder |
| Software engineering fundamentals | F2, E7, O2, AI Engineering Lab weeks 1 to 4 |
| Using coding agents | Practice, not a personality hire; see below |
| Shaping the build | This module, L4, Distilled's concept phase |

Underlying the map, Ng writes, is continuous learning. That is a
hiring filter: people who cannot update after a model revision will
freeze your stack to a blog post from last winter.

### Do not clone a research lab

Pre-training a frontier model is a different industry. A product org
needs, in roughly this order:

- **Someone who owns the eval.** Named human. Not "the team." This is
  the scarce role. Without it, every demo ships.
- **Application engineers** who can ship retrieval, tools, and a UI,
  and who can read a trace (Engineer + Operator literacy).
- **A platform / operator slice** once more than one team shares a
  model: engines, quotas, keys, SLOs (Track 3). This can be a
  fraction of a person until the second product lands.
- **A scientist / adapter specialist** when you actually fine-tune on
  a schedule, not when you might. LoRA is not a full-time job until
  the data flywheel exists (S3, S4).
- **Product and domain.** Shaping the build is mostly this. Ng's
  fourth skill is not a rebrand of "project manager." It is deciding
  what the system may do, what "done" means, and what to cut.
- **Risk / legal / security** as a partner, not a gate at the end
  (L3, E8).

A "prompt engineer" as a standalone career ladder is a 2023 artifact.
Prompting is a skill on the application engineer. Coding agents are a
skill on every engineer. If nobody on the team can **shape** (scope,
eval, cut), agents will generate a larger mess faster.

### Using coding agents without lying to yourself

Ng's third skill is real: steering agents for code and for operations
is now part of the job. It does not replace software fundamentals.
The failure mode he names, vibe coding without those fundamentals, is
the failure mode we see in reviews: no tests, no eval, no ownership
of the diff. House rule for this course: agents may draft, humans
merge, evals decide. Training 01 (AI Engineering Lab) spends weeks on
harnesses for that reason.

Staff for people who can **specify, review, and measure**, not for
people who can only paste from a chat.

### Team size honesty

- One engineer plus a domain expert: prompt, RAG, eval on a laptop.
  This is a valid product.
- Four to eight: add platform, eval ownership, security review.
- Dozens: you are building a platform. Read O1 to O4 and the
  Leadership Textbook on operating models before you hire the
  twentieth "AI person" who all write agents.

Contractors can burst a prototype. They cannot own your eval golden
set unless you treat that set as a deliverable you keep.

## The gap most roadmaps leave

They list papers, not roles. They never say who is fired if the eval
is fake. They staff GPUs before they staff evaluation. They ignore
Ng's map or they treat it as a certificate to buy.

## Practice

1. Read Ng's skills map letter. Write four sentences: how your
   current team covers each skill, or that it does not.
2. Name the eval owner for one live or proposed system. If the name
   is "everyone," pick one person this week.
3. Sketch a six-month hiring plan with **no** research-scientist
   line unless you have a data flywheel and a reason L1 reached
   fine-tune or train.
4. In *The AI Leadership Textbook*, read the chapters on talent and
   operating model. In Distilled, read how shaping the build shows
   up in the concept phase (needs, requirements, V&V plan).

## Watch and read

- Ng, [The AI Engineering Skills Map](https://www.deeplearning.ai/the-batch/the-ai-engineering-skills-map)
  (independent)
- Hashemipour, *The AI Leadership Textbook* and *AI Engineering
  Distilled* ([BOOKS.md](../../reference/BOOKS.md))
- AI Engineering Lab, weeks on harnesses and agents, if you need
  engineers who have already practiced the loop
  ([COMPANION-PROGRAMS.md](../../reference/COMPANION-PROGRAMS.md))
- Chip Huyen, *AI Engineering*, on the application development
  workflow (independent)

## Knowledge check

1. Why is "eval owner" a role rather than a ceremony?
2. Which Ng skill is most often missing on a team that only hires
   model specialists?
3. When do you hire a full-time fine-tuning specialist?
4. What goes wrong if coding agents are treated as a substitute for
   software engineering fundamentals?
5. Why does this course insist the Ng map is independent?

<details>
<summary>Answers</summary>

1. Someone has to freeze the golden set, run the gate, and refuse a
   release. Shared ownership means the gate does not run.
2. Shaping the build (and often software fundamentals / production
   operation). Model specialists optimize weights. Products die from
   scope and missing evals.
3. When adapters are on a schedule, data is produced continuously,
   and L1 has already shown that prompting and RAG are not enough.
   Not at the kickoff slide.
4. Generated code without tests, evals, or reviewers. Throughput of
   defects rises. Ng's letter flags this as vibe coding rather than
   engineering.
5. Because it is not a Zorost product and we are not a reseller of
   DeepLearning.AI. We point at a public source. We do not wrap it
   as our credential.

</details>
