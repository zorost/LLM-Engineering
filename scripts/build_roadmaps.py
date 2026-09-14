#!/usr/bin/env python3
"""Zorost hub-and-leaf LLM roadmaps for GitHub README posters.

Orthogonal spine, numbered hubs, leaf topics. Same information shape as
public LLM-course roadmaps; original layout, copy, and Zorost skin.
HTML lives in assets/diagrams/. PNG copies land in img/ after export.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from html_wrap import write_poster_html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "diagrams"

W = 960
M = 40
HUB_W, HUB_H = 280, 64
LEAF_W, LEAF_H = 232, 40
LEAF_GAP = 12
STAGE_GAP = 48
SPINE = 480
LEFT_HUB = 40
RIGHT_HUB = 640
LEFT_LEAF = 40
RIGHT_LEAF = 688
HEADER = 128
INK = "#11161D"
MUTE = "#5A6672"
RULE = "#D5DBE1"
PAPER = "#EEF1F4"
WHITE = "#FFFFFF"
LAVA = "#FF3621"
TEAL = "#0A7F7A"
CHIP = "#F4F6F8"


def g(n: int) -> int:
    return 4 * round(n / 4)


def rrect(x, y, w, h, fill, stroke, sw=1, rx=8):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


FAM = {
    "Geist": "'Geist', system-ui, sans-serif",
    "Geist Mono": "'Geist Mono', ui-monospace, monospace",
    "Instrument Serif": "'Instrument Serif', Georgia, serif",
}


def txt(x, y, s, *, size=12, fill=INK, family="Geist", w=500, anchor="start"):
    face = FAM.get(family, FAM["Geist"])
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-family="{face}" '
        f'font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'
    )


def hline(x1, x2, y, color, sw=1.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
        f'stroke="{color}" stroke-width="{sw}"{d}/>'
    )


def vline(x, y1, y2, color, sw=1.5):
    return (
        f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{sw}"/>'
    )


def stage_h(n_leaves: int) -> int:
    return g(max(HUB_H, n_leaves * LEAF_H + max(0, n_leaves - 1) * LEAF_GAP))


def poster(title: str, desc: str, stages: list, focal: int, extra: str) -> str:
    ys = []
    y = HEADER
    for i, st in enumerate(stages):
        h = stage_h(len(st["leaves"]))
        ys.append((y, h))
        y = g(y + h + STAGE_GAP)
    legend_y = y
    H = g(legend_y + 72)
    slug = "".join(ch if ch.isalnum() else "-" for ch in title.lower()).strip("-")
    parts = [
        f'<title id="{slug}-title">{title}</title>',
        f'<desc id="{slug}-desc">{desc}</desc>',
        f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
        txt(M, 36, "ZOROST INTELLIGENCE  ·  LLM ENGINEERING  ·  TRAINING 02", size=8, fill=MUTE, family="Geist Mono", w=500),
        txt(M, 72, title, size=28, fill=INK, family="Instrument Serif", w=400),
        txt(M, 100, desc, size=12, fill=MUTE, w=400),
        txt(W - M, 36, "zorost.com/ai-lab", size=8, fill=MUTE, family="Geist Mono", w=500, anchor="end"),
    ]
    hub_cys = []
    for i, st in enumerate(stages):
        y0, h = ys[i]
        left = i % 2 == 0
        hx = LEFT_HUB if left else RIGHT_HUB
        lx = RIGHT_LEAF if left else LEFT_LEAF
        hy = g(y0 + (h - HUB_H) / 2)
        hcy = g(hy + HUB_H / 2)
        hub_cys.append(hcy)
        accent = i == focal
        fill = WHITE
        stroke = LAVA if accent else RULE
        sw = 2 if accent else 1
        parts.append(rrect(hx, hy, HUB_W, HUB_H, fill, stroke, sw, 8))
        chip_fill = LAVA if accent else CHIP
        chip_fg = WHITE if accent else INK
        parts.append(rrect(hx + 12, hy + 20, 28, 24, chip_fill, chip_fill, 0, 4))
        parts.append(txt(hx + 26, hy + 38, f"{i + 1:02d}", size=12, fill=chip_fg, family="Geist Mono", w=500, anchor="middle"))
        parts.append(txt(hx + 52, hy + 40, st["title"], size=16, fill=INK, family="Geist", w=500))
        inner_hub = hx + HUB_W if left else hx
        parts.append(hline(inner_hub, SPINE, hcy, LAVA if accent else INK, 1.5))
        for j, leaf in enumerate(st["leaves"]):
            ly = g(y0 + j * (LEAF_H + LEAF_GAP))
            lcy = g(ly + LEAF_H / 2)
            parts.append(rrect(lx, ly, LEAF_W, LEAF_H, WHITE, RULE, 1, 8))
            parts.append(txt(lx + 16, ly + 26, leaf, size=12, fill=INK, w=400))
            inner_leaf = lx if left else lx + LEAF_W
            parts.append(hline(inner_leaf, SPINE, lcy, MUTE, 1, "4 4"))
    parts.append(vline(SPINE, hub_cys[0], hub_cys[-1], INK, 2))
    parts.append(rrect(M, legend_y, 12, 12, LAVA, LAVA, 0, 2))
    parts.append(txt(M + 20, legend_y + 11, "Accent hub is the sitting most people skip or start too late.", size=12, fill=MUTE, w=400))
    parts.append(txt(M, legend_y + 36, extra, size=12, fill=MUTE, w=400))
    svg = "\n".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" aria-labelledby="{slug}-title {slug}-desc">{svg}</svg>'
    )


ROADMAPS = {
    "roadmap-fundamentals": {
        "h1": "LLM fundamentals roadmap",
        "p": "Five hubs. Math through scaling. The last hub is the hardware sitting public LLM courses usually omit.",
        "title": "LLM fundamentals",
        "desc": "Build the vocabulary before you train, retrieve, or serve. Hub 05 is the hardware sitting.",
        "focal": 4,
        "extra": "Leaves are topics inside the hub, not extra courses. Finish knowledge checks before Track 1.",
        "stages": [
            {"title": "Mathematics", "leaves": ["Linear algebra", "Calculus", "Probability", "Statistics", "Information theory"]},
            {"title": "Python for ML", "leaves": ["Python", "NumPy and pandas", "PyTorch", "Hugging Face", "Honest splits"]},
            {"title": "Neural networks", "leaves": ["Layers and loss", "Training loop", "Overfitting", "Regularization", "Residuals"]},
            {"title": "NLP to LLMs", "leaves": ["Tokenization", "Embeddings", "Attention", "Transformer stack", "LLM families"]},
            {"title": "Scaling and hardware", "leaves": ["Scaling laws", "GPU vs CPU", "KV cache RAM", "MoE routing", "Token cost"]},
        ],
    },
    "roadmap-scientist": {
        "h1": "LLM scientist roadmap",
        "p": "Nine hubs from architecture through licenses. Hubs 08 and 09 are the expansion past a single new-trends column.",
        "title": "The LLM scientist",
        "desc": "How capable models are made. Nine hubs. Reasoning, distillation, and licenses are first-class, not a footnote.",
        "focal": 5,
        "extra": "Accent is evaluation. If you cannot measure the model, you cannot claim the fine-tune worked.",
        "stages": [
            {"title": "LLM architecture", "leaves": ["Tokenization", "Attention", "MLP / FFN", "Positional encodings", "KV cache and GQA"]},
            {"title": "Pre-training", "leaves": ["Pre-training data", "Parallelism", "Scaling laws", "Compute budget", "Checkpoints", "Mid-training"]},
            {"title": "Post-training data", "leaves": ["Chat templates", "Instruction sets", "Synthetic data", "Preference pairs", "Quality filters", "Contamination"]},
            {"title": "Fine-tuning (SFT)", "leaves": ["Full vs LoRA", "Packing", "Chat SFT", "Adapters", "Unsloth / TRL", "Merge adapters"]},
            {"title": "Alignment", "leaves": ["Reward models", "DPO / ORPO", "PPO", "GRPO", "RLAIF", "Over-refusal"]},
            {"title": "Evaluation", "leaves": ["Harnesses", "Task evals", "Leaderboards", "Arena scores", "Contamination", "Human review"]},
            {"title": "Quantization", "leaves": ["GGUF / llama.cpp", "AWQ", "GPTQ", "bitsandbytes", "Calibration", "Quality drop"]},
            {"title": "Merge · multimodal", "leaves": ["Weight merging", "MoE merge", "Vision-language", "Audio / video", "Interpretability"]},
            {"title": "Reasoning and licenses", "leaves": ["Chain of thought", "Test-time compute", "Distillation", "Speculative decode", "Licenses", "Model cards"]},
        ],
    },
    "roadmap-engineer": {
        "h1": "LLM engineer roadmap",
        "p": "Nine hubs from running a model to the production surface. Hub 09 is context, evals, memory, and platforms.",
        "title": "The LLM engineer",
        "desc": "How applications use models. Retrieval before agents. Security and evals before the demo.",
        "focal": 2,
        "extra": "Accent is RAG. Fine-tune for behavior you cannot retrieve. Agents last.",
        "stages": [
            {"title": "Running LLMs", "leaves": ["Hosted APIs", "llama.cpp", "vLLM / SGLang", "Ollama", "Chat templates", "Local vs hosted"]},
            {"title": "Vector storage", "leaves": ["Embeddings", "ANN indexes", "Chunking", "Metadata filters", "Hybrid search"]},
            {"title": "Retrieval (RAG)", "leaves": ["Index", "Retrieve", "Augment", "Generate", "Citations", "When not to RAG"]},
            {"title": "Advanced RAG", "leaves": ["Query rewrite", "Rerankers", "Graph RAG", "Agentic RAG", "RAG evals"]},
            {"title": "Agents", "leaves": ["ReAct loop", "Tools", "Planner", "Multi-agent", "Memory", "Guards"]},
            {"title": "Inference optimization", "leaves": ["Batching", "KV cache", "Speculative", "Quantized serve", "Prefix cache"]},
            {"title": "Deployment", "leaves": ["OpenAI-compatible", "Containers", "Autoscaling", "Gateways", "SLOs"]},
            {"title": "Security", "leaves": ["Prompt injection", "Data leaks", "Supply chain", "Red team", "Defense in depth"]},
            {"title": "Production surface", "leaves": ["Context and MCP", "Production evals", "Conversation memory", "Cloud platforms"]},
        ],
    },
    "roadmap-operator": {
        "h1": "LLM operator roadmap",
        "p": "Four hubs public LLM scientist/engineer posters skip: engines, reliability, cost, traces.",
        "title": "The LLM operator",
        "desc": "Keep a model answering under a latency budget, on a GPU bill finance can defend.",
        "focal": 2,
        "extra": "Accent is cost. Tokens, KV RAM, and batch size are the same conversation.",
        "stages": [
            {"title": "Serving engines", "leaves": ["vLLM", "SGLang", "llama.cpp", "TensorRT-LLM", "OpenAI-compatible"]},
            {"title": "Reliability", "leaves": ["Timeouts", "Fallbacks", "Canary", "Load shed", "Retries"]},
            {"title": "Cost and capacity", "leaves": ["Token economics", "KV RAM", "Batch size", "Scaling laws", "Headroom"]},
            {"title": "Observability", "leaves": ["Traces", "Token logs", "Online evals", "Incidents", "SLOs"]},
        ],
    },
    "roadmap-leader": {
        "h1": "LLM leader roadmap",
        "p": "Four hubs for people who allocate money and risk. Read with the two Zorost textbooks.",
        "title": "The LLM leader",
        "desc": "Allocate money, risk, and attention. You do not need to train a model to kill a bad demo.",
        "focal": 0,
        "extra": "Accent is the first decision: buy, build, retrieve, or fine-tune. Most portfolios skip it.",
        "stages": [
            {"title": "Buy, build, retrieve", "leaves": ["Hosted API", "Fine-tune", "RAG first", "Build weights", "Kill criteria"]},
            {"title": "Teams and skills", "leaves": ["Skills map", "Hiring", "Review cadence", "Scientist vs engineer", "On-call"]},
            {"title": "Risk and governance", "leaves": ["NIST AI RMF", "EU AI Act", "Licenses", "Audit trail", "Data rights"]},
            {"title": "Portfolio", "leaves": ["Evidence", "Trust patterns", "Budget", "Vendor lock", "Ship / kill"]},
        ],
    },
}


def banner_svg() -> str:
    W, H = 1280, 320
    parts = [
        f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
        f'<rect x="0" y="0" width="8" height="{H}" fill="{LAVA}"/>',
        txt(48, 88, "ZOROST INTELLIGENCE  ·  AI LAB  ·  TRAINING 02", size=12, fill=MUTE, family="Geist Mono", w=500),
        txt(48, 148, "LLM Engineering", size=40, fill=INK, family="Instrument Serif", w=400),
        txt(48, 188, "A free, original course and roadmap for LLM fundamentals, the LLM scientist,", size=16, fill=MUTE, w=400),
        txt(48, 216, "the LLM engineer, plus operator and leader tracks public hubs omit.", size=16, fill=MUTE, w=400),
        rrect(48, 248, 8, 8, LAVA, LAVA, 0, 2),
        txt(64, 257, "RAG  ·  fine-tuning  ·  agents  ·  quantization  ·  evals  ·  serving", size=12, fill=INK, w=500),
        txt(1232, 257, "zorost.com/ai-lab", size=12, fill=MUTE, family="Geist Mono", w=500, anchor="end"),
    ]
    svg = "\n".join(parts)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">{svg}</svg>'


def social_svg() -> str:
    W, H = 1280, 640
    parts = [
        f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
        f'<rect x="0" y="0" width="12" height="{H}" fill="{LAVA}"/>',
        txt(64, 160, "FREE LLM COURSE  ·  OPEN ROADMAP", size=16, fill=MUTE, family="Geist Mono", w=500),
        txt(64, 248, "LLM Engineering", size=40, fill=INK, family="Instrument Serif", w=400),
        txt(64, 304, "Fundamentals, scientist, engineer, operator, leader.", size=20, fill=INK, w=400),
        txt(64, 348, "Fine-tuning, RAG, agents, quantization, evaluation, serving.", size=20, fill=MUTE, w=400),
        txt(64, 520, "Zorost Intelligence AI Lab", size=16, fill=INK, w=500),
        txt(64, 552, "github.com/zorost/LLM-Engineering", size=16, fill=MUTE, family="Geist Mono", w=400),
        txt(1216, 552, "MIT", size=16, fill=MUTE, family="Geist Mono", w=500, anchor="end"),
    ]
    svg = "\n".join(parts)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">{svg}</svg>'


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_poster_html(OUT / "banner.html", "LLM Engineering", banner_svg())
    write_poster_html(OUT / "social.html", "LLM Engineering course", social_svg())
    for key, spec in ROADMAPS.items():
        svg = poster(spec["title"], spec["desc"], spec["stages"], spec["focal"], spec["extra"])
        write_poster_html(OUT / f"{key}.html", spec["h1"], svg)
    print("wrote", len(ROADMAPS) + 2, "html files")


if __name__ == "__main__":
    main()
