# L4 · Portfolio and product

## Why it exists

A lab that cannot kill a demo will drown a company in assistants.
Portfolio management is the skill of funding a few systems that have
users, evals, and owners, and of withdrawing oxygen from the rest.
This is the last leader module because L1 to L3 are the criteria you
kill with.

## The idea

### A demo is not a product

A product has a user, a job, a metric, a cost line (O3), an owner
(L2), a risk file (L3), and a way to stop it. A demo has a
screenshot and a champion. Champions are not evidence.

Write **kill criteria before the pilot**, while everyone is still
honest. Examples that have teeth:

- Eval below threshold X on a frozen golden set after N weeks, with
  a named sample size
- Cost per successful task above Y at the volume the business case
  assumed
- p95 latency above the SLO the UI requires
- No eval owner, or the owner left and was not replaced
- License, residency, or high-risk classification that the pilot
  pretended not to see
- A human process that already meets the same bar at lower risk

If the criterion is "stakeholders still excited," you do not have a
criterion.

Pilots expire. A date in the calendar, not "when we know more." At
expiry, **promote, pause, or kill**. Pause is allowed once. Pause
twice is a kill you are too polite to perform.

### Portfolio shape

Most organizations need a **small number of production systems**
(often retrieval-grounded, tightly tooled) and a **deliberate
sandbox** for exploration. The sandbox uses dummy data or licensed
public data, a cheap model, and no path to customer PII. Mixing
sandbox and production keys is how you get an incident.

Platform versus product: a shared gateway, eval service, and index
can be a platform if two or more products need them (Track 3). A
platform with one consumer is a product with extra meetings. Do not
fund a "center of excellence" as a substitute for an eval owner on
each system.

### Evidence versus theater

Theater looks like:

- A leaderboard score with no task match and no contamination check
- A chatbot for a job that is a form
- "Agent" in the name, a single LLM call in the trace
- A calibrated-sounding accuracy from an uncalibrated judge (O4)
- A roadmap of models instead of a roadmap of user jobs

Evidence looks like Distilled's **Evidence view**: what was measured,
on what distribution, with what provenance. Trust-family patterns in
that book (approval gates, fallback ladders, calibrated judges,
provenance seals, configuration records) are the productization
checklist. *The AI Leadership Textbook* puts the same objects in an
executive sequence: value, operating model, risk, and stop rules.
Read the Distilled Trust family, then write which patterns your
pilot actually implements. If the answer is none, it is still a
demo.

### Promote with configuration, not with hope

Promotion to production is a **configuration record**: model
revision, prompt and template hashes, index snapshot, tool
allowlist, SLO, eval report, rollback. O1 to O4 are the machinery.
L4 is the decision that the machinery is allowed to face users.
Canary, then enlarge. Keep the previous configuration bootable.

When you kill, kill the **access paths** (keys, routes, indexes),
not only the slide. Orphaned agents with live tools are still
products, just unowned ones.

### What to fund instead of another assistant

Work that compounds:

- Golden sets and error buckets (lab 12)
- Document pipelines you would need anyway (Training 01's lakehouse
  path, DocPrep-class tools on the public shelf)
- Operator excellence on one gateway rather than five snowflake
  stacks
- Training for the L2 skills you actually lack

Work that does not compound: a new wrapper around the same model
for each vice president.

## The gap most roadmaps leave

They end at "deploy." They never teach a stop rule. They never say
that a portfolio of twelve chatbots is a management failure.

## Practice

1. List every LLM demo in your org that a user could still open.
   Mark product / pilot / zombie. Put a date on each pilot.
2. Write kill criteria for the most beloved pilot, before the next
   steering meeting. Use numbers from O3 and S6.
3. For one system you would promote, write the configuration record
   (a page). If you own Distilled, use Configuration and Evidence
   views. If you do not, buy it and redo the page.
4. Leadership Textbook: portfolio and product chapters. Then decide
   one thing to kill this quarter. If you cannot name one, your
   filter is too kind.

## Watch and read

- Hashemipour, *AI Engineering Distilled*: Evidence and
  Configuration views; Trust-family patterns
  ([Amazon](https://www.amazon.com/dp/B0HHZM4QQS))
- Hashemipour, *The AI Leadership Textbook*
  ([Amazon](https://www.amazon.com/dp/B0HHTJHK5R))
- Chip Huyen, *AI Engineering*, on iteration and feedback (independent)
- This course: O2 fallbacks, O3 cost, E10 evals, L1 ladder

## Knowledge check

1. When should kill criteria be written?
2. Why is "pause" twice a smell?
3. What is the difference between a platform and a single-consumer
   gateway?
4. Name two Trust-family ideas (from Distilled) that turn a demo
   into something you can defend.
5. Why must a kill include keys and routes, not only a slide?

<details>
<summary>Answers</summary>

1. Before the pilot, while incentives still allow honesty. After
   launch, every number has a constituency.
2. The second pause is a refusal to apply the criteria. Convert it
   to a kill or a promotion with a new, explicit eval.
3. A platform has multiple products sharing SLOs, evals, and
   operations. One consumer means you built a product and called it
   a platform.
4. Any two of: approval gate, fallback ladder, calibrated judge,
   provenance seal, configuration record. They bind action, failure,
   measurement, sources, and versions.
5. Because live credentials and DNS still serve users. An unowned
   live path is an unowned product.

</details>
