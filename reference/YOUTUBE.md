# YouTube and lecture video

A curated map of lectures this course actually sends people to.
Dated when it matters. Not a dump of every thumbnail. Watch in the
order the matching module says. We point. We do not paste transcripts.

Refresh this file when Stanford CS336 posts a new year (see
[ROADMAP.md](../ROADMAP.md)).

---

## Start here (the five)

Watch these before you wander.

1. **3Blue1Brown, neural networks, then the Transformer.** Geometry
   first. [But what is a neural network?](https://www.youtube.com/watch?v=aircAruvnKk)
   then [But what is a GPT? Visual intro to Transformers](https://www.youtube.com/watch?v=wjZofJX0v4M)
   and [Attention in transformers, visually explained](https://www.youtube.com/watch?v=eMlx5fFNoYc).
   Why: F1 and F3 become pictures instead of slogans.
2. **Andrej Karpathy, Deep Dive, then Zero to Hero builds.**
   [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)
   (2025, long, the field in one sitting), then
   [Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) and
   [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE).
   Why: the Deep Dive is the map; the builds are the hands. Playlist:
   [Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ).
3. **Stanford CS336, Language Modeling from Scratch.** The university
   course this repository is willing to lose to.
   Site: [cs336.stanford.edu](https://cs336.stanford.edu/).
   [2025 playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rOY23Y0BoGoBGgQ1zmU_MT_),
   [2026 playlist](https://www.youtube.com/playlist?list=PLoROMvodv4rMqXOcazWaTUHhq-yembLCV).
   Why: tokenization, resource accounting, kernels, scaling, and
   training as they are taught to people who will actually run jobs.
4. **Hugging Face courses (video where they provide it, else the
   written course).** NLP, then LLM, then Agents, then MCP. Links in
   [COURSES.md](COURSES.md). Why: tokenizers, `transformers`, and
   agent/MCP practice without a university calendar.
5. **fast.ai Practical Deep Learning for Coders.**
   [course.fast.ai](https://course.fast.ai/). Why: code-first
   intuition if F3 still feels like notation.

---

## Karpathy (Zero to Hero and after)

| Piece | Why it is here |
|---|---|
| [Zero to Hero playlist](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ) | Micrograd through GPT. The scientific literacy this course assumes in Scientist. |
| [Let's build GPT](https://www.youtube.com/watch?v=kCc8FmEb1nY) | A decoder you can type. Pair with lab 02. |
| [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) | Pair with lab 01 and the tokenization tutorial. |
| [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) | Pretraining, post-training, tokens, and product behavior in one long lecture. |
| [Let's reproduce GPT-2](https://www.youtube.com/watch?v=l8pRSuU81PU) | Training loop seriousness. Optional after S2. |

Karpathy's other one-off talks are optional. These five are not.

---

## 3Blue1Brown

| Piece | Why it is here |
|---|---|
| [Essence of linear algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) | Dot products and bases before anyone says "embedding." F1. |
| Neural network series (from [aircAruvnKk](https://www.youtube.com/watch?v=aircAruvnKk)) | Gradient descent as a picture. F3. |
| Transformer and attention videos above | S1 without a wall of notation. |

---

## Stanford lecture courses

**CS336 (required pointer for Scientist and Operator).** Playlists
above. Prefer 2026 if you are starting now; keep 2025 for lectures
the new year has not replaced. Course site first when the playlist
lags the syllabus.

**CS224N, Natural Language Processing with Deep Learning.**
Course: [web.stanford.edu/class/cs224n](https://web.stanford.edu/class/cs224n/).
Lecture video is posted per year on the Stanford YouTube channel
and on the course page. Why: the classical NLP-to-transformers
arc (F4, S1) taught as a full class, including attention before
it was a product. Use the latest year that has complete recordings.

**CS25, Transformers United.**
Course: [web.stanford.edu/class/cs25](https://web.stanford.edu/class/cs25/).
Example playlist (V5):
[PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM](https://www.youtube.com/playlist?list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM).
V6 recordings are linked from the course page as they land. Why:
guest lectures on serving, scaling, and current architectures that
a single textbook will not refresh yearly. The serving talks belong
with O1.

---

## GPU Mode

Channel: [youtube.com/@GPUMODE](https://www.youtube.com/@GPUMODE).
Notes and material: [github.com/gpu-mode](https://github.com/gpu-mode).
Why: kernels, profiling, and the gap between a PyTorch line and
what the GPU did. Watch after F5, before you argue about vLLM
flags. Operator track, not week one.

---

## Umar Jamil (transformers from scratch)

Channel: [youtube.com/@umarjamilai](https://www.youtube.com/@umarjamilai).
The LLaMA-from-scratch and attention/RoPE walkthroughs are the
usual pair. Why: a second implementation pass after Karpathy, with
shapes written on screen. Use when S1 still feels like a paper.

---

## Hugging Face (video companions)

The canonical material is written: see [COURSES.md](COURSES.md).
Hugging Face's YouTube channel posts course walkthroughs, paper
discussions, and event talks. Use them when you want a human
voice on `transformers`, tokenizers, or TRL, not as a substitute
for the course units. Why: the library this Scientist track
assumes.

---

## fast.ai

[course.fast.ai](https://course.fast.ai/) and the fast.ai YouTube
channel. Why: Practical Deep Learning, then part 2 if you will
train. F2/F3 door for people who bounce off theorem-first math.

---

## StatQuest

Channel: [youtube.com/@statquest](https://www.youtube.com/@statquest).
Statistics fundamentals playlist, plus softmax, cross-entropy, and
neural net pieces. Why: F1 probability in spoken English. Josh
Starmer is the backup when 3Blue1Brown is too geometric.

---

## Yannic Kilcher

Channel: [youtube.com/@YannicKilcher](https://www.youtube.com/@YannicKilcher).
Paper walkthroughs (Attention is All You Need, RAG, LoRA, DPO, and
whatever just dropped). Why: a first pass on a PDF before you
read it. Not a substitute for the paper. Skip hype thumbnails;
use the long reviews that open the PDF.

---

## Hamel Husain / Mastering LLMs

Mastering LLMs (Parlance Labs / Maven) is the paid cohort. Public
talks and clips from Hamel on evals, fine-tuning, and traces show
up on YouTube and in conference recordings. Why: the eval attitude
in E10 and the evals tutorial (error analysis first, harness
second). We do not copy the course. We send you to Hamel's public
writing and to talks you can actually play. Start from
[hamel.dev](https://hamel.dev/) and the [Maven listing](https://maven.com/parlance-labs/fine-tuning)
for the current offering.

---

## Anthropic and OpenAI (public talks)

Public only. Product keynotes rot. Prefer technical talks and
named lectures with a date.

**Anthropic.** Constitutional AI and interpretability talks,
research seminar recordings, and conference appearances by the
research org. The written [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
note is not video; still required for E5. Why: agents as workflows
plus evals, and a public safety research voice. Channel and event
pages change; search the talk title plus "Anthropic."

**OpenAI.** DevDay technical sessions, system-card livestreams
when they exist, and older research talks (GPT-era) on the
[OpenAI YouTube channel](https://www.youtube.com/@OpenAI). Why:
API product reality and (older) research context for GPT-2/3
papers. Treat marketing sessions as optional. Karpathy's builds
above are the better "OpenAI-era teaching" path for this course.

If a talk is behind a login or is not public, it does not belong
on this list.

---

## How to use this list with the tracks

| Track | Video diet |
|---|---|
| Fundamentals | 3Blue1Brown, StatQuest, fast.ai, Karpathy tokenizer |
| Scientist | CS336, Zero to Hero, Umar Jamil, Yannic on the week's paper |
| Engineer | HF courses, Anthropic agents note + talks, Hamel evals |
| Operator | CS336 resource lectures, GPU Mode, CS25 serving |
| Leader | Skip video unless you need Ng's Batch letter (text) and a CS336 lecture 1 for vocabulary |

Conference keynotes (NeurIPS, ICML) are optional calories. The
table above is the meal.
