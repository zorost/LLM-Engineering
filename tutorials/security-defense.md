# Tutorial · Security defense

## Why it exists

LLM applications take **untrusted text** into a context window that
also holds instructions and tool rights. Lab 14 treats attacks as
**test cases in an eval suite**, not as a cookbook. This note is
the defensive posture. It will not teach you to break systems you
do not own.

## The idea

The failure is **instruction confusion**. Anything in the window
can influence the next token: retrieved documents, web pages, tool
outputs, uploaded files, other users' messages in a shared
context. If those strings contain directives, a naive system will
obey them. The industry name is prompt injection. Data poisoning
is the training-time and index-time cousin: hostile content lands
in weights or in the RAG store.

Defense is layered, like any other input-validation problem:

1. **Trust boundaries.** Draw them (L1, Distilled Boundary view).
   Mark retrieved text and tool output as **data**, not as system
   instructions. Separate channels when the engine allows.
2. **Least privilege tools.** Allowlists, read-only by default,
   human approval for writes (O2, L4). A model that cannot send
   email cannot be talked into sending email.
3. **Output contracts.** Schemas, allowlisted URLs, no raw
   execution of model-emitted code on a server you care about.
4. **Evals as tests.** Frozen adversarial **cases you wrote for
   your system**: "if the retrieved chunk says to ignore the
   user, do we still follow the system policy?" Lab 14 is that
   idea on a toy. Production cases stay in a private repo.
5. **Logging without treasure maps.** O4: traces with ids, not
   a public dump of successful attacks.

Red teaming is a scheduled MEASURE activity (L3), with a scope,
a clean-up, and a rule that findings become tests. It is not a
Friday parlor trick and not a catalog of exploits in a course
file.

This repository will not include jailbreak strings, exploit
payloads, or credential-harvesting recipes. If you need those as
fixtures, you write them internally, you store them like pentest
data, and you do not paste them into issues.

## The gap most tutorials leave

They either skip security or they paste attack lists. The first
leaves you untested. The second teaches offense to a general
audience and goes stale in a month. We teach **controls and
tests**.

## How the lab should feel

Lab 14 should feel like lab 12 with a hostile fixture: a
document that tries to change the task, a check that the system
still honors the policy, a fail if it obeys the document. You
should finish wanting a larger private suite, not a larger
public payload list.

If a cell asks you to "try more attacks," stop at **your**
application's policy tests. Do not search for live exploit
threads to paste into the notebook.

## Practice

1. `14_prompt_injection_defense.ipynb`.
2. For a system you own: list untrusted inputs, tools, and the
   one policy that must hold (for example, "never follow
   instructions inside retrieved text"). Write three eval items
   that would fail if that policy broke. Keep them private.
3. Confirm logs would not store a successful attack payload in
   Slack (O4).

## Watch and read

- E8 in this course; OWASP guidance on LLM applications (public)
- NIST AI RMF MEASURE; your org's pentest policy
- Provider safety docs (Anthropic, OpenAI) as **deployer**
  checklists, dated
- L3 for the legal frame; never a substitute for counsel

## Knowledge check

1. Why is retrieved text a security input, not only a quality
   input?
2. What control beats a cleverer system prompt for send-email
   tools?
3. Where should adversarial fixtures live?
4. Why does this course refuse to print exploit catalogs?
5. How does O4 accidentally make a security problem worse?

<details>
<summary>Answers</summary>

1. Because the generator cannot reliably tell "content" from
   "instruction" in the same token stream. Hostile content is
   an attack surface.
2. Do not give the model that tool, or require an out-of-band
   approval gate. Privilege is the control. Prompting is a
   weak backup.
3. In a private eval set with the same handling as other
   pentest data, not in a public course notebook.
4. Because the job is defense for builders, the payloads go
   stale, and a public catalog is a gift to copy-paste abuse.
5. Logging full prompts and payloads to a wide channel spreads
   secrets and working attacks. Trace ids and tight access
   first.

</details>
