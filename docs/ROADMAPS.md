# Roadmap posters

The five tall images in [`img/`](../img/) are the public face of this LLM
course. They are original Zorost artwork. They follow the information shape
that made public LLM roadmaps readable: a numbered spine of hubs, with leaf
topics fanned to the opposite side.

They are not a copy of anyone else's pixels, palette, icons, or labels.

## What you are looking at

| File | Hubs | Job |
|---|---|---|
| `img/roadmap_fundamentals.png` | 5 | Vocabulary: math through hardware |
| `img/roadmap_scientist.png` | 9 | How weights are made |
| `img/roadmap_engineer.png` | 9 | How products use those weights |
| `img/roadmap_operator.png` | 4 | How a runtime stays up |
| `img/roadmap_leader.png` | 4 | How money and risk get allocated |
| `img/banner.png` | n/a | README header |
| `img/social.png` | n/a | Link-preview card |

A **hub** is a module family (S1 Architecture, E3 RAG). A **leaf** is a
topic inside that hub, not a sixth track. The lava hub is the sitting people
skip or start too late: hardware in Fundamentals, evaluation in Scientist,
RAG in Engineer, cost in Operator, buy-vs-build in Leader.

## Why nine scientist hubs instead of eight

Public scientist posters usually stop at eight stages and dump merging,
multimodality, reasoning, distillation, interpretability, and licenses into
one "new trends" column. That column is how those topics stay unread.

This course splits them:

- Hubs 01 to 07 match the working pipeline (architecture through quantization).
- Hub 08 is merge and multimodal, with interpretability as a leaf that points
  at S12.
- Hub 09 is reasoning, distillation, licenses, and model cards (S9, S10, S11).

The engineer poster does the same for the production surface: context and
MCP, production evals, memory, and platforms are hub 09, not a caption.

## How they were drawn

- Orthogonal spine. Horizontal connectors. No diagonal fans.
- PAPERG `#EEF1F4`, INK `#11161D`, MUTE `#5A6672`, LAVA `#FF3621`.
- Instrument Serif titles, Geist labels, Geist Mono chips.
- HTML source in `assets/diagrams/roadmap-*.html`.
- Rebuild: `python3 scripts/build_roadmaps.py && python3 scripts/export_diagrams.py`

Do not paste a third-party roadmap into this folder. If a leaf is wrong,
edit `scripts/build_roadmaps.py` and export again.
