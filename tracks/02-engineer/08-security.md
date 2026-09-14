# E8 · Security

## Why it exists

LLM applications fail in ways that look like conversation.
Prompt injection, data leaks, and poisoned corpora are
vulnerability *classes*. This module is tests, controls,
and process. It is not a catalog of attacks. Lab 14 treats
hostile strings as **test cases**. You will not find recipes
for bypassing safety here, and you should not add them.

## The idea

### Classes, not exploits

**Prompt injection.** Untrusted text (retrieved docs, email,
web, tool output) contains instructions that compete with
your policy. Direct (the user) and indirect (a document the
system fetched) are the same class: the model cannot tell
data from commands by itself. Control: delimit untrusted
content, never merge it into the system prompt, least
privilege on tools, output allow-lists, human approval on
side effects. The system prompt is policy, not a lock.

**Leaking.** System prompts, tool schemas, other users'
retrieval hits, secrets in traces, PII in logs. Control:
secret scanning, redaction, no secrets in prompts, tenant
filters at retrieve time (E2), retention limits, trace
stores that are access-controlled (Langfuse below).

**Jailbreak, as a class.** Attempts to make the *application*
violate its intended policy (disallowed content, disallowed
tools, policy evasion). Your job is to define the policy,
test that the *product* holds it, and keep vendor filters
on where they apply. This course does not teach phrasing
that evades filters. Red teams use private playbooks under
an authorization. Public curriculum uses fixtures and
scanners.

**Data poisoning and backdoors.** Training or fine-tune
data, or the RAG corpus, is modified so the model or the
retriever behaves badly on a trigger (or generally).
Control: provenance, signed sources, review of ingested
data, canary evals, integrity checks on indexes, restricted
who-can-write-the-corpus. Retrieval poisoning is an index
integrity problem as much as an ML problem.

**Supply chain.** Models, adapters, MCP servers, and
prompts you did not write. Pin versions, read licenses
(S11), verify checksums where you can, run evals after
every bump.

**Unbounded consumption.** Recursive tool loops, huge
contexts, unbounded max-token settings. Caps from E5 and
E6 are security controls.

### OWASP

The living list is the
[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications)
and the GenAI project page
[genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/).
Numbers and names move between 2025 and 2026 releases. Map
your system onto the **current** list: injection, supply
chain, data and model poisoning, sensitive disclosure,
improper output handling, excessive agency, system prompt
leakage, embedding/vector weaknesses, misinformation,
unbounded consumption. Use the PDF as a checklist for
*controls and tests*, not as a how-to.

### Red team as a process

Microsoft,
[Planning red teaming for LLMs](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/red-teaming):
assemble a diverse group, cover benign and adversarial
*goals*, test model and application, iterate with and
without mitigations, record inputs/outputs/ids, report
top issues, and **do not treat red teaming as a substitute
for measurement**. Start with authorized, scoped testing
of *your* product. Systematic evals (E10) follow.

Microsoft AI Red Team hub:
[learn.microsoft.com/en-us/security/ai-red-team](https://learn.microsoft.com/en-us/security/ai-red-team/).
PyRIT is their open automation for *authorized* probing.
Use it inside a program with a written scope, never against
systems you do not own.

### Scanners and traces

**garak** ([github.com/NVIDIA/garak](https://github.com/NVIDIA/garak),
[garak.ai](https://garak.ai/)) is an LLM vulnerability
scanner. You point it at an endpoint you are allowed to
test. It reports probe results. Treat findings as tickets:
severity, repro id, control, retest. Do not paste probe
payloads into public issues.

**Langfuse** ([langfuse.com/docs](https://langfuse.com/docs))
is traces, scores, and prompt versions. Security use:
inspect who sent what, whether a tool fired, whether PII
landed in a span. Configure redaction. Traces without
access control are a leak.

Lab 14 is the in-repo discipline: fixtures of hostile
*classes*, expected refusals or safe handling, no cookbook.

### Controls that belong in code

- Tool allow-lists and argument schemas (E1, E5, E9).
- Retrieve-time ACL (E2).
- Output encoding if you render model text as HTML.
- Rate limits and cost caps (E7, O3).
- Content filters from the cloud (E12) as a layer, not the
  only layer.
- Human in the loop for irreversible actions.

Leader track L3 is NIST AI RMF and the EU AI Act as
governance. This file is the engineer checklist.

## The gap most roadmaps leave

They either skip security or they publish attack strings.
Both fail. The missing move is **security as eval**:

- A fixture set of injection and leak *attempts* with
  expected safe behavior.
- A scanner (garak) in CI against a staging endpoint.
- Traces (Langfuse or equivalent) with redaction.
- A written red-team cadence (Microsoft's planning guide).

If it is not a test, it will regress.

## Practice

Lab `14_prompt_injection_defense.ipynb`. Run it. Add one
new *test* that describes a class (for example: "instruction
in a retrieved chunk must not fire a tool") and asserts the
safe outcome. Do not add a novel bypass write-up.

Going further: read the current OWASP LLM Top 10 HTML.
Tick which items your toy RAG from lab 08 even has a
control for. Optional: Langfuse local or cloud on lab 10
traces, with PII filters on.

Do not run scanners against third-party products without
permission.

## Watch and read

- OWASP, [LLM Top 10 project](https://owasp.org/www-project-top-10-for-large-language-model-applications)
- OWASP GenAI, [llm-top-10](https://genai.owasp.org/llm-top-10/)
- Microsoft, [Planning red teaming for LLMs](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/red-teaming)
- Microsoft, [AI Red Team](https://learn.microsoft.com/en-us/security/ai-red-team/)
- garak, [github.com/NVIDIA/garak](https://github.com/NVIDIA/garak)
- Langfuse, [docs](https://langfuse.com/docs)
- NVIDIA, [Trustworthy AI / NeMo Guardrails docs](https://docs.nvidia.com/nemo/guardrails/)
  (controls; optional)
- This repository, [.github/SECURITY.md](../../.github/SECURITY.md)

## Knowledge check

1. Why is the system prompt not a security boundary?
2. What is the difference between a leak of the system
   prompt and a leak of another tenant's chunks?
3. What does a data-poisoning control look like on a RAG
   index?
4. What is garak for, and what is it not for?
5. What does Microsoft's red-teaming guide insist you do
   besides adversarial sessions?

<details>
<summary>Answers</summary>

1. The model attends to all tokens. Untrusted text in the
   window can override or argue with policy. Enforcement
   is in tools, filters, and application code.
2. Prompt leak is a confidentiality failure of *your*
   instructions. Cross-tenant chunk leak is a data-isolation
   failure and often a legal incident. Both are disclosure;
   the fix (redaction vs ACL at retrieve) differs.
3. Provenance on ingest, who can write, integrity/canary
   queries, and an eval that the answers did not shift on
   a frozen golden set after a corpus update.
4. For: authorized scanning of an endpoint for known
   failure classes. Not for: attacking systems out of
   scope, and not a replacement for product-specific tests.
5. Record findings, iterate with mitigations on and off,
   and run systematic measurement. Red team identifies;
   evals quantify.

</details>
