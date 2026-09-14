# Start here

You need a computer you can install software on, about six hours for the
first sitting, and the patience to run a notebook rather than only read it.
You do not need a GPU or a paid API key for the required path.

If you have never written Python, do [AI Engineering Lab](https://github.com/zorost/AI-Engineering-Lab)
weeks 1 to 4 first, then come back. That program is Training 01. This one is
Training 02, the specialist map of large language models.

## 1. Install

```bash
git clone https://github.com/zorost/LLM-Engineering.git
cd LLM-Engineering
python3 -m pip install -r requirements.txt
python3 scripts/check.py
```

`check.py` must print `ok` before you open a notebook. If it does not, paste
the traceback into an issue with your OS and `python3 --version`.

Use Python 3.11 or 3.12. 3.10 usually works. 3.9 is unsupported.

## 2. Choose a door, not a buffet

| You | First files | First lab |
|---|---|---|
| I cannot yet explain a derivative or a tensor | [Fundamentals](tracks/00-fundamentals/README.md) | `notebooks/00_environment_check.ipynb` then `01` and `02` |
| I want to train or adapt models | [Scientist](tracks/01-scientist/README.md) | `04_chat_templates.ipynb` |
| I want to ship a product on models | [Engineer](tracks/02-engineer/README.md) | `08_embeddings_rag.ipynb` |
| I run GPUs or a gateway for other teams | [Operator](tracks/03-operator/README.md) | `13_vram_and_cost.ipynb` |
| I decide budget, risk, or hiring | [Leader](tracks/04-leader/README.md) | no lab required; read L1 to L4, then the textbooks |

The [README decision table](README.md#pick-a-door) is the same advice in
shorter form. The tall posters in [`img/`](img/) are the map: one spine
per track, leaves for topics inside each hub. How to read them:
[docs/ROADMAPS.md](docs/ROADMAPS.md).

## 3. How a module works

Every module file has the same spine:

1. **Why it exists.** One claim.
2. **The idea.** Enough explanation that a second source is optional, not required.
3. **The gap.** What most roadmaps skip, and why that skip hurts.
4. **Practice.** The lab, if there is one.
5. **Watch and read.** YouTube, papers, docs. We point. We do not paste.
6. **Knowledge check.** Five questions. Answers at the bottom, inverted.

A module that you only highlight is unread. Run the lab or write the five
answers in a notebook of your own.

## 4. What to do when it breaks

1. Read the last line of the traceback.
2. Confirm `python3 scripts/check.py` still passes.
3. Search the [glossary](reference/GLOSSARY.md) for the term in the error.
4. Open a [lab-failure issue](.github/ISSUE_TEMPLATE/lab-failure.yml).

Do not paste API keys. The required labs do not need them. Optional API
exercises live in module "Going further" sections and are marked as such.

## 5. Compute honesty

| Work | Machine | Money |
|---|---|---|
| All 20 labs | Laptop CPU, 8 GB RAM is enough | $0 |
| Small LoRA on a 1B to 8B model | 16 GB unified or a 12 GB GPU | often $0 on Colab-class boxes |
| Serious SFT of 7B+ | 24 GB+ VRAM or a rented GPU | budget it; see [O3](tracks/03-operator/03-cost-and-capacity.md) |
| Pre-training | a cluster | not a weekend project |

If a blog post hides the hardware, ignore the result.

## 6. What this course will not do

- It will not give you a certificate.
- It will not rent you GPUs.
- It will not paste another author's notebooks.
- It will not teach exploit development. Security modules are defensive.
- It will not publish private Zorost client material.

## 7. After the first sitting

You should be able to say, out loud:

- what a token is
- why next-token prediction is the pre-training job
- why an eval that you cannot rerun is not an eval
- which door you are walking through next

Then open that track's README and take module 1.
