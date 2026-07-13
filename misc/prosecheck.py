"""Check the docs against the malariasimulation house style.

    python misc/prosecheck.py                       # the whole site
    python misc/prosecheck.py chapters/03-concepts  # one chapter
    python misc/prosecheck.py --rhythm              # rhythm metrics only, no gate

Two kinds of check. Violations are hard failures and exit non-zero: em-dashes, semicolons and
colons in prose, rhetorical questions, headings that tease, and the vocabulary that marks text
as machine-written. Rhythm is advisory and reports how far the prose sits from the
malariasimulation vignettes, which are the model for the voice.
"""

import re
import statistics as st
import sys
from pathlib import Path

# Measured from the malariasimulation vignettes (Model, Bednets, Treatment, Vaccines, SetSpecies).
BASELINE = {
    "mean_sentence_words": 16.0,
    "stdev": 10.3,
    "pct_short_sentences": 28.9,
    "pct_paras_opening_short": 29.2,
}
TOLERANCE = {
    "mean_sentence_words": 1.5,
    "stdev": 1.0,       # one-sided, only "too uniform" fails
    "pct_short_sentences": 2.0,
    "pct_paras_opening_short": 2.0,
}

SELF_REFERENCE = re.compile(
    r"\b(this site|on this site|this page|on this page|this chapter|this section|"
    r"these docs|the docs|this book|this guide|this document)\b",
    re.I,
)

# Excess vocabulary from Kobak et al., "Delving into LLM-assisted writing in biomedical
# publications through excess vocabulary" (Science Advances, 2025; arXiv:2406.07016), and
# Liang et al. (ICML 2024; arXiv:2403.07183). Plus the marketing register and the American
# spellings, neither of which belong in these docs.
AI_WORDS = [
    "delve", "delving", "underscore", "underscores", "underscoring", "showcase", "showcases",
    "showcasing", "intricate", "intricacies", "meticulous", "meticulously", "commendable",
    "pivotal", "realm", "realms", "tapestry", "testament", "nuanced", "nuances", "boasts",
    "leverage", "leverages", "leveraging", "seamless", "seamlessly", "crucial", "crucially",
    "comprehensive", "landscape", "multifaceted", "groundbreaking", "transformative",
    "paramount", "unwavering", "compelling", "unlock", "unlocks", "unlocking", "streamline",
    "streamlines", "streamlining", "myriad", "plethora", "holistic", "paradigm", "synergy",
    "facilitate", "facilitates", "interplay", "elevate", "elevates", "harness", "harnesses",
    "harnessing", "unveil", "unveils", "unveiling", "illuminate", "illuminates", "foster",
    "fosters", "fostering", "moreover", "furthermore", "additionally", "ultimately",
    "importantly", "notably", "utilise", "utilises", "utilised", "utilize", "utilizes",
    "cutting-edge", "state-of-the-art", "game-changer", "effortless", "revolutionise",
    "revolutionize", "empower", "empowers", "embark", "vibrant", "invaluable", "impactful",
    # American spellings. The house style is British.
    "analyze", "analyzed", "behavior", "color", "colors", "modeled", "modeling",
    "parameterize", "parameterized", "summarize", "summarized", "visualize", "visualized",
]
AI_WORD_RE = re.compile(r"\b(" + "|".join(sorted(AI_WORDS, key=len, reverse=True)) + r")\b", re.I)

AI_PHRASES = [
    "it is worth noting", "it's worth noting", "it is important to note", "in conclusion",
    "in summary", "to sum up", "shed light on", "plays a pivotal role", "paves the way",
    "at its core", "in essence", "deep dive", "dive into", "at the forefront",
    "when it comes to", "not just a", "more than just", "the ever-evolving",
    "navigate the complexities", "that settles it",
]
AI_PHRASE_RE = re.compile("|".join(re.escape(p) for p in AI_PHRASES), re.I)

# "Sentences that go nowhere" as headings: a heading that gestures at a point instead of
# naming its subject. Also anything long enough to be a sentence rather than a label.
TEASER_HEADING_RE = re.compile(
    r"\b(and why|and what|and how|rather than|the reason|is decided|what it means|"
    r"why it|not just|against the|the meaning of)\b",
    re.I,
)

# Numeric ranges (0–1, 0.7–0.95) are the only place an en-dash is allowed.
EN_DASH_IN_PROSE = re.compile(r"(?<!\d)–|–(?!\d)")
# A colon after a word, closing bracket, backtick or quote, followed by more prose on the
# same line. A colon at end of line is a lead-in to a code block or list and is fine.
PROSE_COLON = re.compile(r"[A-Za-z0-9\)\`\"']:\s+\S")


def strip_front_matter(text: str) -> str:
    """Drop the leading YAML block. Without this, `title: "..."` counts as a paragraph."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :]
    return text


def prose_lines(text: str) -> list[tuple[int, str]]:
    """Prose lines with their 1-based line numbers. Skips code, tables, headings, YAML."""
    out, in_code = [], False
    offset = len(text) - len(strip_front_matter(text))
    lineno = text[:offset].count("\n")
    for line in strip_front_matter(text).split("\n"):
        lineno += 1
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        s = line.strip()
        if not s or s.startswith(("|", "#", ":::", "---", "#|", "$$")):
            continue
        out.append((lineno, s))
    return out


def paragraphs(text: str) -> list[str]:
    """Prose paragraphs. List items are excluded, they are not prose."""
    kept, in_code = [], False
    for line in strip_front_matter(text).split("\n"):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            kept.append("")
            continue
        s = line.strip()
        if in_code or not s or s.startswith(("|", "#", "-", "*", ":::", "---", ">", "#|")):
            kept.append("")
            continue
        kept.append(s)
    blocks = [b.strip() for b in "\n".join(kept).split("\n\n") if b.strip()]
    return [" ".join(b.split("\n")) for b in blocks]


def sentences(para: str) -> list[str]:
    para = re.sub(r"`[^`]*`", "X", para)
    para = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", para)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", para) if s.strip()]


def violations(path: Path) -> list[tuple[int, str, str]]:
    """Hard failures. Every one of these must be zero."""
    text = path.read_text()
    hits = []

    # Em-dashes anywhere outside code, including in the link glosses that list items carry.
    in_code = False
    for lineno, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.strip().startswith("#|"):
            continue
        if "—" in line:
            hits.append((lineno, "em-dash", line.strip()))

    for lineno, line in prose_lines(text):
        # A line that is only a link gloss is checked for dashes above, not for prose rules.
        stripped = re.sub(r"`[^`]*`", "X", line)
        if ";" in stripped:
            hits.append((lineno, "semicolon", line))
        if PROSE_COLON.search(stripped):
            hits.append((lineno, "prose colon", line))
        if EN_DASH_IN_PROSE.search(stripped):
            hits.append((lineno, "en-dash", line))
        if stripped.rstrip().endswith("?"):
            hits.append((lineno, "rhetorical question", line))
        for m in AI_WORD_RE.finditer(stripped):
            hits.append((lineno, f"ai-word: {m.group(0).lower()}", line))
        for m in AI_PHRASE_RE.finditer(stripped):
            hits.append((lineno, f"ai-phrase: {m.group(0).lower()}", line))

    # Headings must name their subject, not gesture at it.
    for lineno, line in enumerate(strip_front_matter(text).split("\n"), 1):
        m = re.match(r"^(#{2,3})\s+(.*)", line)
        if not m:
            continue
        title = m.group(2).strip()
        if TEASER_HEADING_RE.search(title):
            hits.append((lineno, "teaser heading", title))
        words = [w for w in re.sub(r"[`*]", "", title).split() if w]
        if len(words) > 7:
            hits.append((lineno, f"heading of {len(words)} words", title))
    return hits


def rhythm(paths: list[Path]) -> tuple[dict, list, list]:
    paras, offenders, self_refs = [], [], []
    for p in paths:
        text = strip_front_matter(p.read_text())
        for m in SELF_REFERENCE.finditer(text):
            self_refs.append((p, m.group(0)))
        for para in paragraphs(p.read_text()):
            paras.append(para)
            ss = sentences(para)
            if ss and len(ss[0].split()) <= 9 and len(ss) > 1:
                offenders.append((p, ss[0]))

    lengths = [len(s.split()) for para in paras for s in sentences(para)]
    if not lengths:
        return {}, [], []
    got = {
        "mean_sentence_words": st.mean(lengths),
        "stdev": st.pstdev(lengths),
        "pct_short_sentences": 100 * sum(1 for w in lengths if w <= 9) / len(lengths),
        "pct_paras_opening_short": 100 * len(offenders) / len(paras),
    }
    return got, offenders, self_refs


def main(argv: list[str]) -> int:
    rhythm_only = "--rhythm" in argv
    args = [a for a in argv if not a.startswith("--")]

    paths = []
    for a in args or ["chapters", "index.qmd"]:
        p = Path(a)
        paths.extend(sorted(p.rglob("*.qmd")) if p.is_dir() else [p])

    failed = 0
    if not rhythm_only:
        for p in paths:
            for lineno, kind, line in violations(p):
                failed += 1
                print(f"{p}:{lineno}: {kind}")
                print(f"    {line[:110]}")
        print(f"\n{failed} violation(s)\n" if failed else "\nno violations\n")

    got, offenders, self_refs = rhythm(paths)
    if not got:
        print("no prose found")
        return failed

    n_paras = sum(len(paragraphs(p.read_text())) for p in paths)
    print(f"{n_paras} paragraphs, rhythm against the malariasimulation baseline\n")
    print(f"{'metric':32s} {'yours':>8s} {'target':>8s}")
    soft = 0
    for k, target in BASELINE.items():
        d = got[k] - target
        flag = ""
        if k == "stdev":
            # Only uniformity is a fault. Prose more varied than the baseline is fine.
            if d < -TOLERANCE[k]:
                flag, soft = "  <-- too uniform", soft + 1
        elif k == "pct_paras_opening_short":
            # Only an excess is a fault. A paragraph that opens on a short sentence and then
            # explains it is the teaser pattern these docs exist to avoid, so sitting below
            # the malariasimulation baseline is the intended direction.
            if d > TOLERANCE[k]:
                flag, soft = "  <-- TOO HIGH", soft + 1
        elif abs(d) > TOLERANCE[k]:
            flag = "  <-- TOO HIGH" if d > 0 else "  <-- TOO LOW"
            soft += 1
        print(f"{k:32s} {got[k]:8.1f} {target:8.1f}{flag}")

    if self_refs:
        print(f"\nself-reference (cut these): {len(self_refs)}")
        for p, s in self_refs[:10]:
            print(f"  {p}: {s}")

    if offenders:
        print(f"\nparagraphs opening on a short sentence: {len(offenders)}")
        for p, s in offenders[:20]:
            print(f"  {p}: {s}")

    if soft:
        print(f"\n{soft} rhythm metric(s) outside tolerance")
    return failed


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1:]) else 0)
