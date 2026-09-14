# F2 · Python and data

## Why it exists

The labs are Python. The failure mode is not syntax. It is silent data
leakage, a shuffled split that is not a split, and a notebook that only
runs on the author's laptop.

## The idea

### Language

You need enough Python to read the labs: types, functions, classes,
exceptions, list and dict comprehensions, `pathlib`, virtual
environments. You do not need to be a software architect yet. You do
need to stop running `pip install` into the system interpreter.

[Real Python](https://realpython.com/) and the
[freeCodeCamp Python](https://www.youtube.com/watch?v=rfscVS0vtbw)
video are enough for syntax.

### The data science layer

- **NumPy** is the tensor before you meet PyTorch. Slices, broadcasting,
  `einsum` later.
- **Pandas** is tables. LLM work still has tables: eval spreadsheets,
  trace dumps, cost logs.
- **Matplotlib** is "show me the loss." If you cannot plot it, you do
  not understand it.

Jake VanderPlas, [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/),
is the free book.

### PyTorch

PyTorch is the tensor library the labs and most open training stacks use.
You need `Tensor` shapes, `requires_grad`, a tiny `nn.Module`, a
`DataLoader`, and the habit of printing `x.shape` before you debug a
loss. You do not need to memorize every op. Device placement (`cpu` vs
`cuda` vs `mps`) is F5. Autograd is F3.

The [official 60-minute blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
is enough to start. Patrick Loeber's playlist is the spoken version.

### Hugging Face

`transformers`, `datasets`, and `tokenizers` are how you load a public
checkpoint without writing a file format parser. A model id on the Hub
is not a license to ship it. Read the card (S11). A `pipeline()` is a
demo. A `AutoTokenizer` plus an explicit `chat_template` is engineering
(E1, lab 04).

Do not start this course by fine-tuning with a one-click Trainer script.
Load a tokenizer, encode ten strings, and print the special tokens first.

### The split is the product

Before any model:

1. Define the unit (row, document, user, conversation). Leakage hides
   in the unit you forgot.
2. Split train / validation / test by that unit. Time-based if the world
   moves.
3. Freeze the test set. If you tune on it, it is not a test set.
4. Write a data dictionary: column, type, allowed missingness, source.

Classical ML libraries (scikit-learn) still matter. Logistic regression
on bag-of-words is the control model you should beat before you celebrate
an LLM.

## The gap most roadmaps leave

They mention pandas and skip **what an LLM dataset actually looks like**:

- JSONL of conversations, not a CSV of iris flowers
- a `messages` array with roles `system`, `user`, `assistant`
- a chat template that is *not* the JSON you stored
- duplicates, near-duplicates, and eval items hiding in train

Read [S3](../01-scientist/03-post-training-data.md) after this. Do not
collect a dataset until you can say how you will split it.

## Practice

Lab `notebooks/00_environment_check.ipynb`. Then, without a model,
download any small public JSONL (or write twenty fake support tickets)
and produce train/val/test counts with no shared ticket ids.

## Watch and read

- freeCodeCamp, Learn Python, and Machine Learning for Everybody
- Real Python
- Python Data Science Handbook
- Udacity, Intro to Machine Learning (PCA and the old-but-clear
  supervised loop)

## Knowledge check

1. Why is a random row split wrong for support-ticket classification?
2. What is the difference between a stored conversation and a chat
   template?
3. Name two leakage paths in RAG evaluation.
4. When is logistic regression the right first model?
5. What does `scripts/check.py` prove?

<details>
<summary>Answers</summary>

1. Multiple rows may be the same customer or the same incident. Split by
   ticket or customer, not by row.
2. Storage is a structure you own (ShareGPT, OpenAI messages, a table).
   The template is the tokenizer's string, with special tokens, that the
   model was trained to see.
3. The answer string sitting in the retrieved chunk; the test question
   sitting in the indexed corpus.
4. When the baseline is tabular or linear in bag-of-words and you need a
   number before you spend GPU.
5. That this repository's labs import and that the tiny self-checks
   still pass on your machine.

</details>
