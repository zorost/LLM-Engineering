# E12 · Platforms

## Why it exists

Many teams will never run vLLM themselves. They will call
Azure, Google, AWS, or Databricks, plus an OpenAI-shaped
gateway in front of whatever is actually serving. This
module is **curriculum-level**: what each platform is for,
what to compare, and where the hands-on lives. The
notebooks are Training 01 weeks 18 to 24 in
[AI Engineering Lab](https://github.com/zorost/AI-Engineering-Lab).
Do not duplicate them here. Do not treat a 2024 screenshot
as today's menu. Names churn. Verify live docs.

Lakehouse literacy that Databricks assumes is
[30 days of Databricks](https://github.com/zorost/30-days-of-Databricks).

## The idea

### How to read a platform

Every major cloud now sells: a model catalog, a chat/embed
API, a retrieval product, an agent runtime, an eval/trace
product, a gateway (quotas, keys, safety), and IAM. The
engineering questions are stable:

- Identity: API keys versus workload identity.
- Data path: does customer text leave the region? Is it
  used to train?
- Grounding: their RAG (AI Search, Knowledge Bases, Vertex
  AI Search, Vector Search) versus yours (E2 to E4).
- Agents: their SDK versus the loop you wrote in lab 10.
- Evals: can you import *your* golden set (E10)?
- Cost: units, reserved throughput, idle endpoints (E7).
- Exit: OpenAI-compatible surface, or lock-in at the tool
  layer?

Lab `15_openai_compatible_client.ipynb` is the exit drill.
If the platform speaks that dialect, your harness moves.

### Azure AI Foundry

Microsoft's hub-and-project surface for generative apps:
model catalog (including Azure OpenAI), serverless
endpoints, Foundry Agent Service / Agent Framework,
evaluation and tracing, Content Safety, AI Gateway
patterns via Azure API Management. Governance and Entra ID
are the reason enterprises pick it, not a unique model.

Hands-on: Training 01 **week 18**. Platform notes:
`reference/platforms/ai-foundry/` in that repo. Live docs:
[learn.microsoft.com/en-us/azure/ai-foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/).
The portal has been renamed more than once. Click through.

### Google Vertex AI and Gemini

Two doors: **Google AI Studio** (fast keys, Gemini) and
**Vertex AI** (IAM, VPC, Model Garden, Agent Engine, ADK,
eval, batch). Multimodal is a default, not an add-on.
BigQuery as the place traces and structured extracts land
is a real pattern.

Hands-on: Training 01 **week 19**. Notes:
`reference/platforms/google-vertex/`. Docs:
[cloud.google.com/vertex-ai/docs](https://cloud.google.com/vertex-ai/docs)
and [ai.google.dev](https://ai.google.dev/). ADK:
[google.github.io/adk-docs](https://google.github.io/adk-docs/).

### AWS Bedrock and SageMaker AI

**Bedrock:** Converse API (one shape across Claude, Nova,
Llama, Mistral, and others on the catalog), Knowledge
Bases for RAG, Agents, Guardrails, prompt management,
AgentCore. IAM is the control plane.

**SageMaker AI:** training, JumpStart, endpoints, the
older "I have a container" path. Philipp Schmid's Hugging
Face DLC posts (E7) are historical pointers to that path.
Bedrock is where many new LLM apps start; SageMaker
remains when you own the image.

Hands-on: Training 01 **week 20**. Notes:
`reference/platforms/aws-bedrock/`. Docs:
[docs.aws.amazon.com/bedrock](https://docs.aws.amazon.com/bedrock/).

### Databricks: Mosaic, Genie, Vector Search

Databricks is not "another LLM API." It is the lakehouse
plus Mosaic-style GenAI: Unity Catalog as the permission
boundary, Model Serving and Unity AI Gateway, **Vector
Search** on table-backed indexes, **AI functions** in SQL
(`ai_query` and friends), **Genie** (text-to-SQL over
governed tables, with verified answers), Agent Bricks /
agent eval, MLflow. Weeks 21 to 24 of Training 01 are the
zero-to-capstone: UC and Delta, pipelines, then ML/GenAI,
then DABs, governance, FinOps.

This course will not paste those notebooks. E4's
text-to-SQL discussion is the conceptual prep for Genie.
E2's ACL-at-retrieve is the conceptual prep for Vector
Search under Unity Catalog. If you have not seen a
medallion table, do 30 days of Databricks or Training 01
weeks 21 to 22 before you argue about Genie.

Docs starting points:
[docs.databricks.com/aws/en/generative-ai](https://docs.databricks.com/aws/en/generative-ai/)
(cloud path in the URL may vary). Verify in your workspace
cloud.

### OpenAI-compatible gateways

A gateway speaks chat completions (and often embeddings)
to callers and routes to OpenAI, Azure, Bedrock, vLLM,
Ollama, or a house router. **OpenRouter** (E1) is a hosted
example. **LiteLLM**, **TGI**, **vLLM**, and many internal
proxies are the self-hosted pattern. Command-center-style
house routers belong in Operator (O1, O3) when you run
them.

Rules for a gateway:

- One client in application code (lab 15).
- Per-route auth, quota, and audit.
- Do not strip licenses: routing to a non-commercial
  weight does not make it commercial.
- Evals run against the *route name*, not only the vendor
  id, because aliases move.

E7 is deploying an engine. This section is putting a
stable URL in front of several engines.

### How to choose

| Constraint | Lean toward |
|---|---|
| Entra, Purview, existing Azure estate | Foundry |
| Multimodal documents, BigQuery, ADK | Vertex / Gemini |
| IAM-first AWS estate, Converse, Guardrails | Bedrock |
| Truth in Delta tables, SQL analysts, UC | Databricks |
| Multi-provider, your VPC, one SDK | OpenAI-compatible gateway + engines |

Re-run the comparison when a product name changes. The
table is a bias, not a contract. Cost and residency beat
brand.

## The gap most roadmaps leave

They either ignore clouds or they paste one vendor's
workshop. Missing: **the same agent, three clouds, one
eval suite**, which is exactly Training 01 weeks 18 to 20,
then the lakehouse as a fourth runtime (weeks 21 to 24).
This repository teaches the portable ideas (E1 to E11)
and sends you there for clicks.

## Practice

Required here:

1. Lab 15 against at least a mock and, if you have one, a
   local OpenAI-compatible server.
2. Write a one-page comparison for *your* employer
   constraint (identity, region, warehouse) with a
   tentative pick. No notebooks to fork.

Hands-on platforms: clone
[AI-Engineering-Lab](https://github.com/zorost/AI-Engineering-Lab)
and run the week that matches the pick (18 Foundry, 19
Vertex, 20 Bedrock, 21 to 24 Databricks). Use their
tracker. Do not copy those notebooks into this repo.

Optional literacy:
[30-days-of-Databricks](https://github.com/zorost/30-days-of-Databricks).

## Watch and read

- Azure AI Foundry, [docs](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- Vertex AI, [docs](https://cloud.google.com/vertex-ai/docs)
- Gemini API, [ai.google.dev](https://ai.google.dev/)
- Amazon Bedrock, [docs](https://docs.aws.amazon.com/bedrock/)
- Databricks Generative AI, [docs](https://docs.databricks.com/aws/en/generative-ai/)
- OpenRouter, [docs](https://openrouter.ai/docs)
- LiteLLM, [docs](https://docs.litellm.ai/)
- Training 01, [curriculum README](https://github.com/zorost/AI-Engineering-Lab/blob/main/curriculum/README.md)
  weeks 18 to 24
- [The AI Leadership Textbook](https://www.amazon.com/dp/B0HHTJHK5R)
  (platforms and governance as leadership context)
- [AI Engineering Distilled](https://www.amazon.com/dp/B0HHZM4QQS)
  (seam notation when you specify a platform-shaped system)

## Knowledge check

1. What portable interface should an application prefer
   when talking to a platform?
2. Why is Databricks Vector Search not "just another
   Chroma"?
3. What is Genie, at curriculum level?
4. Why do weeks 18 to 20 of Training 01 exist as a set?
5. What does a gateway owe you besides a URL?

<details>
<summary>Answers</summary>

1. An OpenAI-compatible (or equally stable) chat/embed
   client, with platform-specific SDKs only for features
   the common shape lacks. Lab 15.
2. The index lives next to Unity Catalog tables, lineage,
   and existing IAM. It is a lakehouse retrieval product,
   not a sidecar toy DB. Operations and permissions differ.
3. A governed text-to-SQL / analyst agent over warehouse
   tables, with verified answers, not a generic chatbot.
4. So the same support-style agent is deployed three ways
   (Foundry, Vertex, Bedrock) and compared on governance
   and cost, instead of collecting three unrelated demos.
5. Auth, quota, audit, a stable route name, and honesty
   about which license and retention apply upstream.

</details>
