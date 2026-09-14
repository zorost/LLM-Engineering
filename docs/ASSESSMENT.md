# Assessment of the public LLM-course landscape

This note is the design record for **LLM Engineering** (Zorost Intelligence
AI Lab, Training 02). It is not a review of a person. It is a map of a
genre, and a list of holes we refused to ship.

## The genre

By 2024 a public "LLM course" had a stable shape:

1. Optional fundamentals (math, Python, networks, classical NLP).
2. A scientist track (architecture, pre-training, data, SFT, alignment,
   evals, quantization, plus a bucket of "new trends").
3. An engineer track (APIs, RAG, agents, inference tricks, deploy, security).
4. A README used as the entire product, with Colab notebooks as the labs.

The most-used example of that shape is Maxime Labonne's
[llm-course](https://github.com/mlabonne/llm-course): three roadmaps, a
notebook table, and dense reference lists. It did the field a service by
making the *skeleton* obvious. It is also, by design, a hub rather than a
textbook. Topics are named in a paragraph. The explanations live in other
people's blogs, papers, and Colabs.

We read that hub, and the courses around it, in full. We did not fork it.
We did not copy its prose, images, or notebooks. We kept the skeleton
because the skeleton is the field, then we wrote the missing pages.

## What that skeleton gets right

- **The three-way split is real.** Fundamentals, model science, and
  application engineering are different jobs. Mixing them in one week
  produces tourists.
- **Pointers beat fake completeness.** A paragraph plus a 3Blue1Brown link
  is more honest than a page of paraphrased Wikipedia.
- **Labs that run in a browser lowered the door.** QLoRA-in-Colab taught more
  people LoRA than any paper did.
- **Security as a first-class engineer topic** is the correct instinct.
  Most bootcamps still skip it.

## What it leaves out (and why that matters)

These are the holes we filled. Each one has a module or a lab in this repo.

| Gap | Why it hurts | Where we put it |
|---|---|---|
| Tokenizer design, fertility, multilingual failure | People debug "the model is dumb" when the tokenizer split the word | S1, lab 01 |
| Long context: RoPE, ALiBi, YaRN, sliding window | Context windows became a product feature without a mental model | S1, E9 |
| Mixture of experts as architecture, not only franken-merges | Serving MoE is a different job from merging LoRAs | S1, lab 17, O1 |
| State-space and hybrid models | The field is not decoder-only Transformers forever | S1, S8 |
| Reasoning models, process rewards, GRPO as a default | 2025 made "chat SFT" the wrong last step for many tasks | S5, S9 |
| Distillation, MTP, speculative decoding as a system | Speed is not only quantization | S10, E6, lab 16 |
| Dataset licenses, model licenses, contamination | Shipping a contaminated eval or a non-commercial weight is a legal event | S11 |
| Interpretability beyond a single abliteration notebook | Steering and SAEs are easy to overclaim | S12 |
| Context engineering and prefix cache | The window is the product | E9 |
| MCP, A2A, structured tools as contracts | Agents without contracts become prompt soup | E5, E9 |
| Production evals, traces, release gates | "We tried it and it seemed fine" is not engineering | E10, lab 12 |
| Memory as a lying component | Chat history is not knowledge | E11 |
| Cloud and Databricks as first-class serving | Many teams will never run vLLM themselves | E12 |
| Operator track: engines, SLOs, FinOps, observability | The scientist-engineer split hides the person on call | Track 3 |
| Leader track: buy vs build, staff, risk, kill criteria | Most failures are decision failures | Track 4 |
| Hardware and scaling laws before the GPU is rented | People buy the wrong box | F5, lab 13, 19 |
| Knowledge checks in the same file as the idea | A hub you cannot fail is a bookmark list | every module |
| CPU-first labs that teach the *idea* | Colab GPU labs expire; tensor labs do not | `notebooks/` |

Other honest limits of the hub genre, which we tried not to repeat:

- **Colab links rot.** A course whose labs are other people's gists will
  404. Ours live in-tree.
- **The "new trends" bucket becomes a junk drawer.** Merging, multimodality,
  interpretability, and test-time compute are four topics, not one.
- **Frameworks are treated as the idea.** LangChain is a library. RAG is
  the idea. We teach the idea first.
- **No leadership surface.** A CTO cannot use a QLoRA Colab as a staff
  plan. Track 4 exists so they are not sent to a vendor slide instead.

## What we deliberately did not copy

- Roadmap artwork, README wording, and notebook tables from any third party.
- Vendor collabs that exist to sell a cloud.
- Internal Zorost serving recipes, private models, or client data.
- Exploit code. Security is written as tests and controls.

## Independent courses we send people to

We would rather you watch a great lecture than read our paraphrase of it.
The short list:

- Stanford CS336 (2025 and 2026), [cs336.stanford.edu](https://cs336.stanford.edu/)
- Andrej Karpathy, Zero to Hero and the 2025 Deep Dive
- Hugging Face NLP, LLM, Agents, and MCP courses
- fast.ai
- Hamel Husain, Mastering LLMs
- Chip Huyen, *AI Engineering*
- Sebastian Raschka, *Build a Large Language Model (From Scratch)*
- Our own [AI Engineering Lab](https://github.com/zorost/AI-Engineering-Lab)
  when the reader needs a 24-week build cadence rather than a field map

Full pointers: [reference/YOUTUBE.md](../reference/YOUTUBE.md),
[reference/COURSES.md](../reference/COURSES.md).

## How this course should be judged

A year from now, this repository is working if:

1. A motivated engineer can pick a door and not get lost.
2. Every named concept in the 2024 public skeleton still has a module, and
   the 2025 to 2026 additions are not stuffed into "new trends."
3. The labs still run on CPU without a key.
4. A leader can read Track 4 and make a cheaper decision.
5. Nothing in git history or file copy attributes the work to an agent.

If you find a missing concept that a working LLM engineer needs, open an
issue with the module path where it should live.
