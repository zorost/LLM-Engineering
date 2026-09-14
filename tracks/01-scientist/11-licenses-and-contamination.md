# S11 · Licenses and contamination

## Why it exists

A checkpoint is a legal object. A dataset is a legal object. An
eval score is a scientific object only if the test did not leak
into train. Shipping without reading the card is how teams donate
their product to a license they cannot meet, or to a leaderboard
they did not earn.

This module is literacy for engineers, not legal advice. Counsel
signs the contract. You still open the LICENSE file.

## The idea

### Weights: four families you will actually meet

**Apache 2.0** (and MIT): permissive OSI licenses. Commercial use,
modification, distribution, a patent grant in Apache's case.
Keep notices. State modifications if Apache asks you to. Many
Qwen2.5/Qwen3 sizes, OLMo, Mistral's Apache checkpoints, and
other open weights use this. There is no monthly-active-user
gate in the license text.

**Llama Community License** (Meta, 3.x and 4.x variants): a
custom **source-available** license, not OSI open source.
Commercial use is granted for most organizations, with extra
terms that Apache does not have:

- A **700 million monthly active users** threshold, measured on
  the release date of that Llama version (affiliates included).
  Above it, you request a separate license Meta may refuse.
- An **Acceptable Use Policy** that flows down.
- Naming and "Built with Llama" duties for derivative **models**.
- Version-specific extras (Llama 4 has had geographic limits
  reported in the community license). Read **that** version.

If you are not a hyperscaler, the MAU clause is usually idle.
The AUP and naming duties are not.

**Gemma**: Google has shipped under **Gemma Terms of Use** plus a
**Prohibited Use Policy** (Gemma 1 to 3), which permit many
commercial uses but are not Apache. Later Gemma checkpoints have
appeared under Apache 2.0. The family name is not the license.
Open the card on the repo you downloaded.

**Qwen**: mixed. A large share of current dense sizes are Apache
2.0. Earlier flagship sizes used Alibaba's **Tongyi Qianwen**
license (commercial use with its own conditions, historically a
lower MAU threshold than Llama). Again: the file on **that**
revision, not a tweet about "Qwen is open."

Other custom licenses exist (OpenRAIL, research-only, "contact us
for commercial"). This course does not treat research-only or
non-commercial weights as a default you should ship. Restricted
house checkpoints have no place in a public training path.

### Data: copyright is not solved by "it was on the web"

Common Crawl is a crawl, not a grant. FineWeb's **ODC-By** covers
Hugging Face's **compilation**. Underlying pages still have
authors. Courts and regulators are in motion. Your practical bar:

- Prefer datasets with a **datasheet** (Dolma, FineWeb, OLMo) so
  you can say what you used.
- Do not dump customer tickets, email, or licensed books into
  SFT because the trainer accepted JSONL (S3).
- Synthetic data inherits the **teacher's terms**. If a hosted
  API forbids using outputs to train competing models, a trace
  dump is not a loophole.
- ShareGPT-style scrapes are a license mine. Many forks never
  had rights to redistribute.

Merges (S8) and LoRAs (S4) produce **derivatives**. The strictest
parent license is the one you assume until counsel says otherwise.

### Decontamination

Covered as method in S3 and as eval threat in S6. Here it is a
**release duty**:

1. List the evals you will quote.
2. Run MinHash / exact match and a semantic near-dup (semhash or
   embeddings) of train vs those evals.
3. Write the hit rate on the card. Zero hits is a claim. Show
   the threshold.
4. Keep a private or dated eval that never entered any mix.

Contamination is also a **tokenizer** event: the same MMLU item
with different whitespace still counts. Canonicalize before you
hash.

### Model cards and dataset cards

A card that is doing its job states:

| Field | Why |
|---|---|
| License, and a link to the full text | procurement |
| Base model (if a LoRA/merge) | derivative chain |
| Training data summary | copyright, contamination, PII |
| Eval protocol (template, harness, seed) | S6 |
| Intended use and out-of-scope | AUP, product |
| Quantized variants and calibration | S7 |

Hugging Face model cards and dataset cards are the usual place.
If a repo has a beautiful README and `license: other` with no
text, you do not have a ship decision. You have a poster.

Read three cards before you finish this module: one Apache dense
instruct, one Llama instruct, one Gemma or Qwen. Compare license
lines and eval sections. Note what is missing.

## The gap most roadmaps leave

They celebrate "open weights" as one bucket. Missing:

- Apache vs community vs terms-of-use, with MAU and AUP as
  real clauses.
- Dataset copyright vs compilation license.
- Decontamination as a shipping artifact, not a blog virtue.
- Model cards as the interface to legal and to S6.

## Practice

No notebook. Three model cards, written notes:

1. License family, commercial conditions you can name without
   guessing, derivative duties.
2. Whether training data is named enough to audit contamination.
3. Whether reported scores include a harness pin (S6).

If a card cannot survive those three, do not put it in a product
path. Optional: run a toy MinHash of a 100-row SFT file against
a 20-row fake eval.

## Watch and read

- Apache License 2.0 text; Meta Llama license on the specific model repo; [Gemma terms](https://ai.google.dev/gemma/terms) when that is the card; Qwen `LICENSE` on the checkpoint
- Hugging Face, [model card guide](https://huggingface.co/docs/hub/model-cards), [dataset cards](https://huggingface.co/docs/hub/datasets-cards)
- FineWeb / Dolma / OLMo datasheets (S2)
- Stanford CS336, data governance remarks in the data lectures
- [docs/ASSESSMENT.md](../../docs/ASSESSMENT.md) on why this course added S11

## Knowledge check

1. Why is "Llama is open source" the wrong sentence?
2. What does Apache 2.0 give a product team that a community
   license often does not?
3. Why can FineWeb's ODC-By still leave you with copyright work?
4. What two decontamination methods belong on a release card?
5. Name four fields a model card must have before you serve the
   weights.

<details>
<summary>Answers</summary>

1. Llama uses a custom community license with AUP, naming, and
   a MAU threshold. That is not OSI open source (Apache or MIT).
2. A standard, royalty-free grant without a use-policy annex or
   a scale trigger in the license text, plus Apache's patent
   language. Still keep notices.
3. ODC-By licenses the dataset compilation. Pages inside the
   crawl remain other people's works. You still need a data
   policy, not only a Hugging Face badge.
4. Exact/MinHash near-dup against named evals, and a semantic
   near-dup for paraphrases, with thresholds.
5. License text, base/derivative chain, data summary, eval
   protocol. Intended use and quantization notes if you ship
   those artifacts.

</details>
