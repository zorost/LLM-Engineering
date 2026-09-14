# E7 · Deployment

## Why it exists

A notebook is not a product. Deployment is how a caller
reaches a model under a URL, a quota, a cost line, and a
rollback. This module is the ladder: local process, demo
UI, dedicated server, edge. Cloud platforms as *products*
are E12. Serving-engine operations are O1. Here you choose
a rung without cargo-culting a cluster.

## The idea

### Local servers

The OpenAI-compatible loopback is the unit of local deploy:

- llama.cpp server, Ollama, LM Studio, vLLM in OpenAI mode,
  TGI, SGLang. Lab 15 is the client. Point it at
  `localhost`.
- Bind to loopback until you intend a network. Auth is not
  optional the moment the port is reachable.
- One process, one model, one GPU (or unified memory) is a
  valid production for a team tool. It is not a valid
  production for a public SLA.

### Demo UIs

**Gradio** and **Streamlit** wrap a Python function in a
form. [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)
hosts them. Good for eval review, internal demos, and
teaching. Bad as the only auth story for customer data.

A Space is a deployment. Read the hardware, the sleep
policy, and whether secrets belong there (they often do
not). CPU Spaces are enough for this course's labs.

### Dedicated inference servers

These are the engines that implement E6 in production
form:

| Engine | Docs | Role |
|---|---|---|
| vLLM | [docs.vllm.ai](https://docs.vllm.ai/) | Paged attention, continuous batching, OpenAI API |
| TGI | [huggingface.co/docs/text-generation-inference](https://huggingface.co/docs/text-generation-inference) | Hugging Face's server; DLCs on several clouds |
| SGLang | [docs.sglang.ai](https://docs.sglang.ai/) | Fast serving, structured generation, radix prefix cache |

SkyPilot ([docs.skypilot.co](https://docs.skypilot.co/)) is
not an engine. It is how you *launch* jobs and services
across clouds and GPU types without rewriting the YAML
every quarter. Use it when the team already knows the
engine and is tired of each provider's submit UI.

Pick on: model support (GQA, MoE, draft models), structured
output, metrics, LoRA adapters, and whether your weights'
license allows serving. Do not pick on a single tokens/s
tweet.

### Edge

[MLC LLM](https://llm.mlc.ai/) compiles models for client
devices (WebGPU, iOS, Android, metal). On-device is a
privacy and latency play. It is also a model-size play:
you ship a quantized small model, not a 70B. Quality eval
on-device is still required. Update channels for weights
are a product.

### Managed endpoints, as pointers

You will see Amazon SageMaker, Azure model catalogs, Vertex
endpoints, Databricks Model Serving. The pattern is: a
container, an instance type, an autoscaling metric, a
gateway in front. **Philipp Schmid's SageMaker + Hugging
Face posts are pointers, not assigned reading to copy.**
Start at:

- [Hugging Face LLM DLC on SageMaker](https://www.philschmid.de/sagemaker-huggingface-llm)
- [Multi-replica LLM on SageMaker](https://www.philschmid.de/sagemaker-multi-replica)
- AWS, [HF LLM inference containers announcement](https://aws.amazon.com/blogs/machine-learning/announcing-the-launch-of-new-hugging-face-llm-inference-containers-on-amazon-sagemaker/)

Read for the *shape* (image URI, env vars, instance class).
Copy-paste from 2023 instance types into a 2026 account
will fail. Confirm live AWS and Hugging Face docs. E12 is
Foundry, Vertex, Bedrock, Databricks as platforms.

### Cost line

A deploy without a unit cost is a demo. Tokens in, tokens
out, GPU-hours, and idle time. Lab 13 is the arithmetic.
Batch when you can. Cache prefixes (E6, E9). Do not leave
a 70B warm for a team of three.

## The gap most roadmaps leave

They "deploy to Spaces" or "deploy to SageMaker" as a
trophy. The missing checklist:

- Health: liveness versus "the model is still loading."
- Authn/z on the HTTP surface.
- A rollback: previous image or previous adapter.
- An eval gate (E10) before the DNS cut.
- Logs that do not store secrets or raw PII (E8, O4).

If those five are absent, you shipped a port.

## Practice

Lab `15_openai_compatible_client.ipynb`. Then:

1. Write a 15-line FastAPI or stdlib HTTP wrapper around a
   mock `chat` function (no GPU). Return usage tokens.
2. Put Gradio or Streamlit on the same function locally.
   Do not deploy customer data to a public Space.

Going further: run Ollama or llama.cpp server and hit it
with the lab 15 client. Optional: skim one Philipp Schmid
SageMaker post and list what you would still have to
verify in today's console (instance family, image tag,
quota).

Hands-on Foundry / Vertex / Bedrock / Databricks serving
is Training 01 weeks 18 to 24, not this file.

## Watch and read

- Gradio, [docs](https://www.gradio.app/docs)
- Streamlit, [docs](https://docs.streamlit.io/)
- Hugging Face Spaces, [docs](https://huggingface.co/docs/hub/spaces)
- vLLM, [docs](https://docs.vllm.ai/)
- TGI, [docs](https://huggingface.co/docs/text-generation-inference)
- SGLang, [docs](https://docs.sglang.ai/)
- SkyPilot, [docs](https://docs.skypilot.co/)
- MLC LLM, [llm.mlc.ai](https://llm.mlc.ai/)
- Philipp Schmid, SageMaker LLM posts above (pointers)
- Hugging Face, [inference overview](https://huggingface.co/docs/transformers/main/en/pipeline_tutorial)

## Knowledge check

1. What does an OpenAI-compatible server buy you at deploy
   time?
2. When is a Hugging Face Space the wrong front door?
3. How is SkyPilot different from vLLM?
4. What is the honest cost line for a dedicated GPU
   endpoint that is idle 20 hours a day?
5. Name four checks that belong in a deploy, not in a
   notebook README.

<details>
<summary>Answers</summary>

1. The same client (lab 15), eval harness, and gateway can
   target local, TGI, vLLM, or a cloud shim without a
   rewrite.
2. When you owe auth, VPC, data residency, or an SLA.
   Spaces are demos and some internal tools.
3. vLLM *serves* tokens. SkyPilot *places* the job or
   service on machines across clouds.
4. You pay for those 20 hours of GPU anyway unless you
   scale to zero (and accept cold start). Token price
   during the 4 busy hours is not the bill.
5. Health, auth, rollback, eval gate, privacy-safe logs
   (any four of those; all five if you are shipping).

</details>
