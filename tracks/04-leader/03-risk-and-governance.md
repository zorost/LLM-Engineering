# L3 · Risk and governance

## Why it exists

LLM systems fail as products and as legal objects. A leader who can
fund a RAG demo but cannot map it onto a risk framework will fund
it into a headline. This module is the minimum mapping: what the
system does, who is harmed if it is wrong, which public regime
applies, and what evidence you keep.

## The idea

### Start with use, not with model names

Governance attaches to a **system in a context**: user, decision,
domain, data classes, autonomy (suggest versus act), and human
oversight. A 7B model that can send email is a different object from
a 70B model that drafts a paragraph a lawyer rewrites. Distilled's
Boundary view is the picture. A model card is not a substitute for
that picture.

Write, for each system:

- Intended use and explicitly out-of-scope uses
- Data in: personal, secret, licensed, public
- Data out: stored, logged, trained on, sent to a vendor
- Who may be harmed, and how you would know
- What a human must approve (L1 seams)
- How you turn it off

If you cannot turn it off, you do not control it.

### NIST AI Risk Management Framework

The [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
is voluntary in the United States and widely used as a shared
language. Four functions:

- **GOVERN.** Policies, roles, accountability, culture. Your L2 eval
  owner and a named executive live here.
- **MAP.** Context, capabilities, dependencies, impacts. Your system
  card and Boundary view live here.
- **MEASURE.** Evals, metrics, incident tests, including the
  defensive security tests in E8 and lab 14. O4's traces feed
  MEASURE without dumping raw prompts to a shared channel.
- **MANAGE.** Once you know the risks, treat, transfer, or accept
  them, and monitor residual risk. Fallbacks (O2) and kill switches
  (L4) live here.

Playbooks in *The AI Leadership Textbook* translate this for
executives. Do not replace NIST's text with a vendor's colored wheel.
Read the original functions, then write two sentences per function
for your system.

Related NIST profiles (generative AI profile, and later updates)
exist. Check nist.gov for the current PDF. This course will not
mirror them paragraph for paragraph.

### EU AI Act, at the level a leader must not fake

The EU AI Act is a risk-tiered regulation for placing AI systems on
the EU market and for their use. You need counsel. You also need
enough literacy to know when to call counsel:

- **Prohibited** practices are listed in the Act. Do not try to
  "prompt around" them.
- **High-risk** systems (listed domains and use cases: some
  employment, credit, education, biometric, critical infrastructure,
  and others as amended) carry data, documentation, logging, human
  oversight, and conformity duties.
- **GPAI / general-purpose** model duties attach to providers of
  foundation models, with extra duties at systemic scale. If you
  only *use* an API, you are often a **deployer**, which is a
  different role with different duties. If you fine-tune and
  rebrand, get advice: you may have moved along that chain.
- Transparency duties for certain chatbots and synthetic content
  (people must know they are talking to a machine, with the details
  the Act and implementing acts specify).

Official text: EUR-Lex. Summaries on a startup blog are not the Act.
Deadlines and extra-territorial effects are easy to get wrong. This
module's job is to make you dangerous enough to ask precise
questions, not to certify you.

Other regimes will apply at the same time: sector rules (health,
aviation, finance), privacy law (GDPR and equivalents), copyright
and training-data disputes, export controls, and contractual limits
in the model license (S11). Licensed "research only" or
non-commercial weights are a procurement fail if you put them in a
product. This course will not name restricted internal stacks; the
public rule is: **read the card, read the license, do not ship a
weight you cannot defend.**

### Evidence you should be able to produce

- System card: use, limits, eval summary, known failure modes
- Data map: sources, licenses, retention, subprocessors
- Eval reports with dates, versions, and contamination notes (S6,
  S11)
- Incident log and a red-team **test list** (E8), not a catalog of
  exploits
- Human oversight record where the Act or your policy requires it
- A model and tokenizer version pin (O4)

*AI Engineering Distilled* calls some of this the Evidence view and
the Trust-family patterns (approval, provenance, calibrated judges).
Use the book when you specify. Use NIST when you audit. Use counsel
when you ship into a named regime.

## The gap most roadmaps leave

They add a "responsible AI" slide with three adjectives. They never
make the student map GOVERN / MAP / MEASURE / MANAGE onto a real
system. They confuse deployer with provider. They skip licenses.

## Practice

1. Download NIST AI RMF 1.0. For one system, write eight sentences:
   two per function.
2. Classify that system, with a lawyer if it might be high-risk, as
   a toy, a limited-risk chatbot, or something that needs a file.
   If you sell in the EU, write provider versus deployer and why.
3. Read three model cards, including the license section. Reject one
   you would not ship and write the sentence you would put in a
   procurement note.
4. Leadership Textbook: governance and risk chapters. Distilled:
   Evidence view. Lab 14: defensive tests as tests, not as a cookbook.

## Watch and read

- [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
- EU AI Act, official text via [EUR-Lex](https://eur-lex.europa.eu/)
- Hashemipour, *The AI Leadership Textbook*; *AI Engineering
  Distilled* ([BOOKS.md](../../reference/BOOKS.md))
- S11 licenses and contamination; E8 security; O4 observability
- Provider cards from the model you actually use (OpenAI, Anthropic,
  Google, Meta, Mistral, and so on): usage policies and training
  opt-out as of the day you read them

## Knowledge check

1. Why is a model card insufficient as a system card?
2. Name the four NIST AI RMF functions and one artifact you would
   file under MEASURE.
3. What is the difference between a GPAI **provider** and a
   **deployer** of a chat feature, at the level this module uses?
4. Why do non-commercial or research-only weights belong in a
   procurement review?
5. What belongs in a security eval that does not belong in a public
   course repository?

<details>
<summary>Answers</summary>

1. The card describes a model. Governance attaches to use, data,
   autonomy, logging, and oversight of the whole system.
2. GOVERN, MAP, MEASURE, MANAGE. MEASURE: a dated eval report, a
   drift dashboard, or a defensive test suite result.
3. The provider places the general-purpose model on the market. The
   deployer uses a system in a professional context. Fine-tuning and
   rebranding can move you; that move is a legal question.
4. Because putting them in a paid product can breach the license,
   regardless of quality. That is a shipping defect.
5. Your own test cases, logs, and controls. Not exploit code, not a
   jailbreak catalog, not copied attack strings offered as
   instruction.

</details>
