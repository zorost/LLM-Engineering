# Labs

Twenty CPU-first notebooks. None of them require a paid API key.
They exist so you can break the idea, not so you can screenshot a
rented GPU.

Install from the repo root (`python3 -m pip install -r requirements.txt`),
then `python3 scripts/check.py` must print `ok` before you open a
notebook. How to run: [START-HERE.md](../START-HERE.md).

Tutorial notes for the lab *types*: [tutorials/README.md](../tutorials/README.md).

| Lab | File | Purpose |
|---|---|---|
| 00 | `00_environment_check.ipynb` | Confirm install, versions, and the check script before any other lab. |
| 01 | `01_tokenization_bpe.ipynb` | Train a tiny BPE merge table so tokens are not magic. |
| 02 | `02_attention.ipynb` | One-head attention on small tensors you can print. |
| 03 | `03_decoding_strategies.ipynb` | Greedy, temperature, top-k, and nucleus on explicit logits. |
| 04 | `04_chat_templates.ipynb` | Show why a missing end-of-turn token wrecks SFT. |
| 05 | `05_lora_shapes.ipynb` | LoRA rank, alpha, and parameter count without a 7B download. |
| 06 | `06_dpo_loss.ipynb` | Direct preference optimization on toy chosen/rejected pairs. |
| 07 | `07_quantization.ipynb` | Absmax and zero-point quantization, with reconstruction error. |
| 08 | `08_embeddings_rag.ipynb` | Chunk, embed, retrieve, and cite on a corpus you can read. |
| 09 | `09_hybrid_retrieval.ipynb` | Sparse plus dense, then a rerank step. |
| 10 | `10_react_agent.ipynb` | Thought, action, observation, without a framework. |
| 11 | `11_structured_output.ipynb` | JSON Schema as a contract the sampler must obey. |
| 12 | `12_eval_harness.ipynb` | A suite, a release gate, and error buckets. |
| 13 | `13_vram_and_cost.ipynb` | Weight memory, KV cache, and token economics on paper-true numbers. |
| 14 | `14_prompt_injection_defense.ipynb` | Hostile fixtures as eval tests, not as an exploit cookbook. |
| 15 | `15_openai_compatible_client.ipynb` | One client request shape against many backends. |
| 16 | `16_speculative_decoding.ipynb` | Draft and verify on a toy alphabet. |
| 17 | `17_moe_routing.ipynb` | Experts, gates, and load balance as tensors. |
| 18 | `18_kv_cache.ipynb` | Why the second token is cheaper than the first. |
| 19 | `19_scaling_laws.ipynb` | A toy loss-versus-compute curve, with honest limits. |

Open one:

```bash
python3 -m jupyter notebook notebooks/00_environment_check.ipynb
```

Notebook files may land in a later commit than this index. If a
path 404s, you still have the purpose line, the matching track
module, and the tutorial. Do not replace a missing lab with a
random Colab from the internet; wait for the in-tree file or
open an issue.

Going further (GPU or paid APIs) is always labeled optional in
the module. It is never required to finish the knowledge check.
