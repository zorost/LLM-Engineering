"""Shared Zorost diagram HTML wrapper. Tokens from diagram-design Zorost profile."""

FONTS = (
    "https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1"
    "&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap"
)

# Zorost house: PAPERG, INK, MUTE, LAVA, TEAL_D
PAPER = "#EEF1F4"
INK = "#11161D"
MUTED = "#5A6672"
SOFT = "#8A939C"
ACCENT = "#FF3621"
LINK = "#0A7F7A"
RULE = "rgba(17,22,29,0.12)"
DOT = "rgba(17,22,29,0.10)"


def page(title: str, eyebrow: str, h1: str, svg: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link href="{FONTS}" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --color-paper: {PAPER};
      --color-ink: {INK};
      --color-muted: {MUTED};
      --color-accent: {ACCENT};
      --font-sans: 'Geist', system-ui, sans-serif;
      --font-serif: 'Instrument Serif', serif;
      --font-mono: 'Geist Mono', ui-monospace, monospace;
    }}
    body {{
      font-family: var(--font-sans);
      background: var(--color-paper);
      color: var(--color-ink);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 3rem 2rem;
    }}
    .frame {{ max-width: 1200px; width: 100%; }}
    .eyebrow {{
      font-family: var(--font-mono);
      font-size: 0.66rem;
      font-weight: 500;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--color-muted);
      margin-bottom: 0.5rem;
    }}
    h1 {{
      font-family: var(--font-serif);
      font-size: clamp(1.5rem, 2.4vw + 0.75rem, 2rem);
      font-weight: 400;
      letter-spacing: -0.02em;
      line-height: 1.15;
      color: var(--color-ink);
      margin-bottom: 1.5rem;
    }}
    svg {{ width: 100%; min-width: 900px; display: block; }}
  </style>
</head>
<body>
  <div class="frame">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    {svg}
  </div>
</body>
</html>
"""


def defs(slug: str, title: str, desc: str) -> str:
    return f"""
      <title id="{slug}-title">{title}</title>
      <desc id="{slug}-desc">{desc}</desc>
      <defs>
        <pattern id="dots-{slug}" width="22" height="22" patternUnits="userSpaceOnUse">
          <circle cx="1" cy="1" r="0.9" fill="{DOT}"/>
        </pattern>
        <marker id="arrow-{slug}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="{MUTED}"/>
        </marker>
        <marker id="arrow-accent-{slug}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="{ACCENT}"/>
        </marker>
        <marker id="arrow-link-{slug}" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" fill="{LINK}"/>
        </marker>
      </defs>
      <rect width="100%" height="100%" fill="{PAPER}"/>
      <rect width="100%" height="100%" fill="url(#dots-{slug})" opacity="0.55"/>
"""
