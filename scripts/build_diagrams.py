#!/usr/bin/env python3
"""Write Zorost-skinned diagram HTML into assets/diagrams/."""

from pathlib import Path

from html_wrap import (
    ACCENT,
    INK,
    LINK,
    MUTED,
    PAPER,
    RULE,
    SOFT,
    defs,
    page,
)

OUT = Path(__file__).resolve().parents[1] / "assets" / "diagrams"


def box(x, y, w, h, name, sub="", tag="", focal=False, store=False):
    fill = "rgba(255,54,33,0.08)" if focal else ("rgba(17,22,29,0.05)" if store else "#FFFFFF")
    stroke = ACCENT if focal else (MUTED if store else INK)
    tag_w = 36 if len(tag) <= 4 else 48
    cx = x + w / 2
    name_y = y + (28 if tag else 22)
    sub_y = name_y + 16
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>',
    ]
    if tag:
        parts.append(
            f'<rect x="{x + 8}" y="{y + 6}" width="{tag_w}" height="12" rx="2" fill="transparent" stroke="{stroke}" stroke-opacity="0.4" stroke-width="0.8"/>'
        )
        parts.append(
            f'<text x="{x + 8 + tag_w / 2}" y="{y + 15}" fill="{stroke}" fill-opacity="0.8" font-size="7" font-family="\'Geist Mono\', monospace" text-anchor="middle" letter-spacing="0.08em">{tag}</text>'
        )
    parts.append(
        f'<text x="{cx}" y="{name_y + (4 if tag else 8)}" fill="{INK}" font-size="12" font-weight="600" font-family="\'Geist\', sans-serif" text-anchor="middle">{name}</text>'
    )
    if sub:
        parts.append(
            f'<text x="{cx}" y="{sub_y + (4 if tag else 8)}" fill="{MUTED}" font-size="9" font-family="\'Geist Mono\', monospace" text-anchor="middle">{sub}</text>'
        )
    return "\n".join(parts)


def legend(y, items, width=1000):
    bits = [
        f'<line x1="32" y1="{y}" x2="{width - 32}" y2="{y}" stroke="rgba(17,22,29,0.10)" stroke-width="0.8"/>',
        f'<text x="32" y="{y + 20}" fill="{MUTED}" font-size="8" font-family="\'Geist Mono\', monospace" letter-spacing="0.14em">LEGEND</text>',
    ]
    x = 120
    for label, kind in items:
        if kind == "focal":
            bits.append(f'<rect x="{x}" y="{y + 10}" width="12" height="12" rx="2" fill="rgba(255,54,33,0.08)" stroke="{ACCENT}"/>')
        elif kind == "store":
            bits.append(f'<rect x="{x}" y="{y + 10}" width="12" height="12" rx="2" fill="rgba(17,22,29,0.05)" stroke="{MUTED}"/>')
        else:
            bits.append(f'<rect x="{x}" y="{y + 10}" width="12" height="12" rx="2" fill="#FFFFFF" stroke="{INK}"/>')
        bits.append(
            f'<text x="{x + 20}" y="{y + 20}" fill="{MUTED}" font-size="8" font-family="\'Geist Mono\', monospace">{label}</text>'
        )
        x += 160
    return "\n".join(bits)


def course_map():
    slug = "course-map"
    svg = f'''<svg viewBox="0 0 1000 480" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
      {defs(slug, "Five tracks of LLM engineering", "Tree from LLM Engineering to Fundamentals, Scientist, Engineer, Operator, and Leader, with Engineer as the default working path.")}
      <line x1="500" y1="96" x2="500" y2="160" stroke="{MUTED}" stroke-width="1.2"/>
      <line x1="88" y1="160" x2="912" y2="160" stroke="{MUTED}" stroke-width="1.2"/>
      <line x1="120" y1="160" x2="120" y2="196" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <line x1="312" y1="160" x2="312" y2="196" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <line x1="500" y1="160" x2="500" y2="196" stroke="{ACCENT}" stroke-width="1.2" marker-end="url(#arrow-accent-{slug})"/>
      <line x1="688" y1="160" x2="688" y2="196" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <line x1="880" y1="160" x2="880" y2="196" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      {box(420, 48, 160, 48, "LLM Engineering", "Training 02", "ROOT")}
      {box(40, 200, 160, 56, "Fundamentals", "math to hardware", "F0")}
      {box(232, 200, 160, 56, "Scientist", "make the weights", "S")}
      {box(420, 200, 160, 56, "Engineer", "default working path", "E", focal=True)}
      {box(608, 200, 160, 56, "Operator", "serve and observe", "O")}
      {box(800, 200, 160, 56, "Leader", "buy, staff, kill", "L")}
      {box(232, 300, 160, 48, "Labs 00 to 19", "CPU, no API key", "LAB", store=True)}
      <line x1="500" y1="256" x2="500" y2="280" stroke="{MUTED}" stroke-width="1"/>
      <line x1="312" y1="280" x2="688" y2="280" stroke="{MUTED}" stroke-width="1"/>
      <line x1="312" y1="280" x2="312" y2="296" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      {legend(400, [("Default path", "focal"), ("Track", "node"), ("Labs", "store")])}
    </svg>'''
    # patch title in defs duplicate - the wrap already has title in svg child 1
    return page("Five tracks · LLM Engineering", "Tree · Zorost Intelligence", "Five tracks. Engineer is the default working path.", svg)


def llm_layers():
    slug = "llm-layers"
    rows = [
        (80, False, "L5", "Leadership and product", "kill criteria, staff, risk"),
        (144, False, "L4", "Applications and agents", "tools, MCP, eval gates"),
        (208, True, "L3", "Context and retrieval", "the window is the product"),
        (272, False, "L2", "Post-training", "SFT, preference, reasoning"),
        (336, False, "L1", "Pre-training weights", "data, parallel, loss"),
        (400, False, "L0", "Silicon and serving", "VRAM, engines, tokens"),
    ]
    layers = []
    for y, focal, idx, name, sub in rows:
        fill = "rgba(255,54,33,0.08)" if focal else "#FFFFFF"
        stroke = f'stroke="{ACCENT}" stroke-width="1"' if focal else ""
        color = ACCENT if focal else MUTED
        layers.append(f'<rect x="120" y="{y}" width="840" height="64" fill="{fill}" {stroke}/>')
        if not focal:
            layers.append(f'<line x1="120" y1="{y + 64}" x2="960" y2="{y + 64}" stroke="{RULE}" stroke-width="1"/>')
        layers.append(
            f'<text x="140" y="{y + 36}" fill="{color}" font-size="8" font-family="\'Geist Mono\', monospace" letter-spacing="0.14em">{idx}</text>'
        )
        layers.append(
            f'<text x="260" y="{y + 38}" fill="{INK}" font-size="16" font-weight="600" font-family="\'Geist\', sans-serif">{name}</text>'
        )
        layers.append(
            f'<text x="940" y="{y + 38}" fill="{color}" font-size="10" font-family="\'Geist Mono\', monospace" text-anchor="end" letter-spacing="0.04em">{sub}</text>'
        )
    svg = f'''<svg viewBox="0 0 1000 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
      {defs(slug, "LLM work from silicon to the boardroom", "Layer stack from serving silicon up through weights, post-training, context, applications, and leadership, with context and retrieval as the focal layer.")}
      <text x="48" y="64" fill="{MUTED}" font-size="8" font-family="\'Geist Mono\', monospace" letter-spacing="0.18em">BOARD</text>
      <line x1="80" y1="80" x2="80" y2="464" stroke="rgba(17,22,29,0.30)" stroke-width="1"/>
      <polygon points="76,80 84,80 80,72" fill="{MUTED}"/>
      <text x="40" y="488" fill="{MUTED}" font-size="8" font-family="\'Geist Mono\', monospace" letter-spacing="0.18em">SILICON</text>
      {''.join(layers)}
      {legend(500, [("Focal layer", "focal"), ("Other layers", "node")])}
    </svg>'''
    return page("LLM layers · LLM Engineering", "Layer stack · Zorost Intelligence", "LLM work, from silicon to the boardroom", svg)


def scientist_pipeline():
    slug = "scientist-pipeline"
    steps = [
        (40, "Data", "curate, dedup", "S2"),
        (196, "Pre-train", "next token", "S2"),
        (352, "SFT", "instructions", "S4"),
        (508, "Align", "DPO / GRPO", "S5", True),
        (664, "Eval", "harness", "S6"),
        (820, "Compress", "quant, distill", "S7"),
    ]
    nodes = []
    arrows = []
    for i, item in enumerate(steps):
        x, name, sub, tag = item[0], item[1], item[2], item[3]
        focal = len(item) > 4
        nodes.append(box(x, 160, 140, 64, name, sub, tag, focal=focal))
        if i:
            x1 = steps[i - 1][0] + 140
            x2 = x
            arrows.append(
                f'<line x1="{x1}" y1="192" x2="{x2}" y2="192" stroke="{ACCENT if focal else MUTED}" stroke-width="1.2" marker-end="url(#arrow-{"accent-" if focal else ""}{slug})"/>'
            )
    svg = f'''<svg viewBox="0 0 1000 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
      {defs(slug, "Scientist pipeline", "Left to right pipeline: data, pre-train, supervised fine-tuning, preference alignment, evaluation, then compression.")}
      {''.join(arrows)}
      {''.join(nodes)}
      {legend(280, [("Alignment stage", "focal"), ("Other stages", "node")])}
    </svg>'''
    return page("Scientist pipeline · LLM Engineering", "Process · Zorost Intelligence", "How weights are made, left to right", svg)


def engineer_stack():
    slug = "engineer-stack"
    svg = f'''<svg viewBox="0 0 1000 520" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
      {defs(slug, "Engineer application stack", "User request through an application into retrieval and tools, then a model, with traces and evals on the side.")}
      <rect x="40" y="48" width="200" height="280" rx="8" fill="rgba(17,22,29,0.02)" stroke="rgba(17,22,29,0.10)" stroke-width="0.8"/>
      <rect x="88" y="52" width="104" height="12" rx="2" fill="{PAPER}"/>
      <text x="140" y="61" fill="rgba(17,22,29,0.40)" font-size="7" font-family="\'Geist Mono\', monospace" text-anchor="middle" letter-spacing="0.14em">CLIENT</text>
      <rect x="280" y="48" width="440" height="280" rx="8" fill="rgba(17,22,29,0.02)" stroke="rgba(17,22,29,0.10)" stroke-width="0.8"/>
      <rect x="456" y="52" width="88" height="12" rx="2" fill="{PAPER}"/>
      <text x="500" y="61" fill="rgba(17,22,29,0.40)" font-size="7" font-family="\'Geist Mono\', monospace" text-anchor="middle" letter-spacing="0.14em">APPLICATION</text>
      <rect x="760" y="48" width="200" height="280" rx="8" fill="rgba(17,22,29,0.02)" stroke="rgba(17,22,29,0.10)" stroke-width="0.8"/>
      <rect x="820" y="52" width="80" height="12" rx="2" fill="{PAPER}"/>
      <text x="860" y="61" fill="rgba(17,22,29,0.40)" font-size="7" font-family="\'Geist Mono\', monospace" text-anchor="middle" letter-spacing="0.14em">CONTROL</text>
      <line x1="180" y1="160" x2="300" y2="160" stroke="{LINK}" stroke-width="1.2" marker-end="url(#arrow-link-{slug})"/>
      <rect x="214" y="140" width="52" height="12" rx="2" fill="{PAPER}"/>
      <text x="240" y="150" fill="{LINK}" font-size="8" font-family="\'Geist Mono\', monospace" text-anchor="middle" letter-spacing="0.06em">PROMPT</text>
      <line x1="500" y1="176" x2="500" y2="204" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <line x1="580" y1="240" x2="780" y2="240" stroke="{LINK}" stroke-width="1.2" marker-end="url(#arrow-link-{slug})"/>
      <rect x="652" y="220" width="56" height="12" rx="2" fill="{PAPER}"/>
      <text x="680" y="230" fill="{LINK}" font-size="8" font-family="\'Geist Mono\', monospace" text-anchor="middle" letter-spacing="0.06em">TRACE</text>
      <line x1="500" y1="276" x2="500" y2="360" stroke="{ACCENT}" stroke-width="1.2" marker-end="url(#arrow-accent-{slug})"/>
      <rect x="508" y="308" width="40" height="12" rx="2" fill="{PAPER}"/>
      <text x="528" y="318" fill="{ACCENT}" font-size="8" font-family="\'Geist Mono\', monospace" text-anchor="middle" letter-spacing="0.06em">CALL</text>
      {box(60, 128, 160, 64, "User", "task, constraint", "IN")}
      {box(320, 112, 160, 64, "App + policy", "prompt, schema", "APP")}
      {box(520, 112, 160, 64, "RAG and tools", "retrieve, MCP", "CTX")}
      {box(420, 212, 160, 64, "Agent loop", "optional", "LOOP", store=True)}
      {box(780, 112, 160, 64, "Evals", "gate the release", "QA")}
      {box(780, 208, 160, 64, "Traces", "cost, privacy", "OPS")}
      {box(420, 364, 160, 64, "Model runtime", "API or local", "LLM", focal=True)}
      {legend(456, [("Runtime", "focal"), ("Control plane", "node"), ("Optional loop", "store")])}
    </svg>'''
    return page("Engineer stack · LLM Engineering", "Architecture · Zorost Intelligence", "A request, grounded, gated, and observed", svg)


def choose_path():
    slug = "choose-path"
    # flowchart, 4px grid
    svg = f'''<svg viewBox="0 0 1000 640" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
      {defs(slug, "Choose RAG, fine-tune, or agents", "Flowchart: start from a measurable task, prefer retrieval, fine-tune only for behavior in weights, add agents only for multi-step tools.")}
      <line x1="500" y1="68" x2="500" y2="96" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <line x1="500" y1="176" x2="500" y2="204" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <line x1="500" y1="204" x2="500" y2="204"/>
      <path d="M 500,256 L 720,256 Q 728,256 728,264 L 728,300" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <path d="M 500,256 L 280,256 Q 272,256 272,264 L 272,300" fill="none" stroke="{ACCENT}" stroke-width="1.2" marker-end="url(#arrow-accent-{slug})"/>
      <rect x="508" y="240" width="28" height="12" rx="2" fill="{PAPER}"/>
      <text x="522" y="250" fill="{SOFT}" font-size="8" font-family="\'Geist Mono\', monospace" text-anchor="middle">NO</text>
      <rect x="360" y="240" width="36" height="12" rx="2" fill="{PAPER}"/>
      <text x="378" y="250" fill="{ACCENT}" font-size="8" font-family="\'Geist Mono\', monospace" text-anchor="middle">YES</text>
      <line x1="272" y1="364" x2="272" y2="400" stroke="{ACCENT}" stroke-width="1.2" marker-end="url(#arrow-accent-{slug})"/>
      <line x1="728" y1="364" x2="728" y2="400" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <path d="M 728,464 L 728,500 Q 728,508 720,508 L 500,508 Q 492,508 492,516 L 492,536" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <path d="M 272,464 L 272,500 Q 272,508 280,508 L 492,508" fill="none" stroke="{MUTED}" stroke-width="1.2"/>
      <rect x="160" y="24" width="680" height="44" rx="20" fill="#FFFFFF" stroke="{INK}"/>
      <text x="500" y="52" fill="{INK}" font-size="12" font-weight="600" font-family="\'Geist\', sans-serif" text-anchor="middle">Start with a task you can score</text>
      {box(380, 100, 240, 76, "Is the knowledge already", "in a corpus you can index?", "Q1")}
      {box(160, 304, 224, 60, "RAG plus tools", "Engineer E2 to E4", "RAG", focal=True)}
      {box(616, 304, 224, 60, "Fine-tune the behavior", "Scientist S4 to S5", "SFT")}
      {box(380, 400, 240, 64, "Need multi-step tools", "or a long-running loop?", "Q2")}
      {box(380, 540, 240, 56, "Add an agent later", "never as step one", "END")}
      {legend(612, [("Prefer this first", "focal"), ("Later move", "node")], 1000)}
    </svg>'''
    return page("Choose a path · LLM Engineering", "Flowchart · Zorost Intelligence", "Retrieval first. Fine-tune for behavior. Agents last.", svg)


def eval_pyramid():
    slug = "eval-pyramid"
    # 5 trapezoids, apex focal
    # canvas 1000x520, center 500, heights 56
    polys = []
    labels = [
        (80, 200, 800, "Production outcomes", "incidents, cost, win rate", True),
        (140, 256, 680, "Human / arena", "sampled, expensive", False),
        (200, 312, 560, "Judge models", "biased, useful", False),
        (260, 368, 440, "Golden sets", "frozen, rerunnable", False),
        (320, 424, 320, "Unit checks", "schema, citations, regex", False),
    ]
    # Actually pyramid point UP so production at apex is smallest. Reverse widths.
    layers = [
        (320, 80, 360, "Production outcomes", "the only score that pays", True),
        (260, 148, 480, "Human review", "sampled, expensive", False),
        (200, 216, 600, "Judge models", "biased, still useful", False),
        (140, 284, 720, "Golden sets", "frozen, rerunnable", False),
        (80, 352, 840, "Unit checks", "schema, citations, regex", False),
    ]
    body = []
    for x, y, w, name, sub, focal in layers:
        fill = "rgba(255,54,33,0.08)" if focal else "#FFFFFF"
        stroke = ACCENT if focal else "rgba(17,22,29,0.20)"
        # trapezoid: top width slightly smaller
        inset = 24
        pts = f"{x + inset},{y} {x + w - inset},{y} {x + w},{y + 56} {x},{y + 56}"
        body.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
        cx = x + w / 2
        body.append(
            f'<text x="{cx}" y="{y + 28}" fill="{INK}" font-size="12" font-weight="600" font-family="\'Geist\', sans-serif" text-anchor="middle">{name}</text>'
        )
        body.append(
            f'<text x="{cx}" y="{y + 44}" fill="{MUTED}" font-size="9" font-family="\'Geist Mono\', monospace" text-anchor="middle">{sub}</text>'
        )
    svg = f'''<svg viewBox="0 0 1000 500" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
      {defs(slug, "Evaluation pyramid", "Pyramid from unit checks at the base up to production outcomes at the apex, which is the focal layer.")}
      <text x="40" y="72" fill="{MUTED}" font-size="8" font-family="\'Geist Mono\', monospace" letter-spacing="0.18em">RARER</text>
      {''.join(body)}
      {legend(432, [("What pays", "focal"), ("Supporting evals", "node")])}
    </svg>'''
    return page("Evaluation pyramid · LLM Engineering", "Pyramid · Zorost Intelligence", "Unit checks at the base. Outcomes at the apex.", svg)


def companion_shelf():
    slug = "companion-shelf"
    svg = f'''<svg viewBox="0 0 1000 480" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
      {defs(slug, "Zorost companion shelf", "LLM Engineering as the focal training next to AI Engineering Lab, textbooks, Transformer Explainer, and Fieldwork.")}
      {box(380, 40, 240, 56, "Zorost Intelligence AI Lab", "zorost.com/ai-lab", "LAB")}
      <line x1="500" y1="96" x2="500" y2="132" stroke="{MUTED}" stroke-width="1.2"/>
      <line x1="120" y1="132" x2="880" y2="132" stroke="{MUTED}" stroke-width="1.2"/>
      <line x1="160" y1="132" x2="160" y2="164" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <line x1="380" y1="132" x2="380" y2="164" stroke="{ACCENT}" stroke-width="1.2" marker-end="url(#arrow-accent-{slug})"/>
      <line x1="620" y1="132" x2="620" y2="164" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      <line x1="840" y1="132" x2="840" y2="164" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      {box(40, 168, 240, 72, "AI Engineering Lab", "Training 01 · 24 weeks", "T01")}
      {box(260, 168, 240, 72, "LLM Engineering", "Training 02 · this repo", "T02", focal=True)}
      {box(500, 168, 240, 72, "Textbooks", "Leadership · Distilled", "BOOK")}
      {box(720, 168, 240, 72, "Instruments", "Explainer · Fieldwork", "TOOL")}
      {box(260, 292, 240, 64, "20 CPU labs", "ideas, not Colab gists", "LAB", store=True)}
      <line x1="380" y1="240" x2="380" y2="288" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow-{slug})"/>
      {legend(392, [("This course", "focal"), ("Sibling program", "node"), ("Labs", "store")])}
    </svg>'''
    return page("Companion shelf · LLM Engineering", "Tree · Zorost Intelligence", "Where this course sits on the public shelf", svg)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "course-map.html": course_map(),
        "llm-layers.html": llm_layers(),
        "scientist-pipeline.html": scientist_pipeline(),
        "engineer-stack.html": engineer_stack(),
        "choose-path.html": choose_path(),
        "eval-pyramid.html": eval_pyramid(),
        "companion-shelf.html": companion_shelf(),
    }
    for name, html in files.items():
        path = OUT / name
        path.write_text(html, encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
