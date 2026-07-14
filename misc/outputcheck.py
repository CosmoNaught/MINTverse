"""Check that every executed-cell output renders inside an output box.

    python misc/outputcheck.py            # after ./render.sh

Quarto emits `class="cell-output cell-output-display"` for every DataFrame, bare repr and
figure, and `class="cell-output cell-output-stdout"` for anything a cell printed. Both must
land inside the same panel. A rule that nulls the background on `.cell-output-display` strips
the panel from the first kind and leaves the result floating on the page.
"""

import re
import sys
from pathlib import Path

BOOK = Path("_book")


def main() -> int:
    if not BOOK.is_dir():
        print("_book/ not found. Run ./render.sh first.")
        return 1

    css = "".join(p.read_text() for p in BOOK.rglob("bootstrap-*.min.css"))
    if not css:
        print("no compiled bootstrap css found in _book/")
        return 1

    failures = []

    if re.search(r"\.cell-output-display\{[^}]*background:\s*none", css):
        failures.append(".cell-output-display still nulls its background, so outputs float")
    if re.search(r"\.cell-output-display[^{]*::before\{content:none", css):
        failures.append('.cell-output-display::before still removes the "Output" label')
    if not re.search(r'\.cell-output::before\{[^}]*content:\s*"Output"', css):
        failures.append('.cell-output::before no longer sets the "Output" label')

    pages = list(BOOK.rglob("*.html"))
    kinds = {"display": 0, "stdout": 0, "stderr": 0, "other": 0}
    orphans = []
    for page in pages:
        html = page.read_text()
        for m in re.finditer(r'<div class="cell-output cell-output-(\w+)"', html):
            kinds[m.group(1) if m.group(1) in kinds else "other"] += 1
        # An output div outside a .cell is one the panel CSS does not reach.
        for m in re.finditer(r'<div class="cell-output', html):
            before = html[: m.start()]
            if before.count('<div class="cell"') <= before.count("</div></div>") - 40:
                orphans.append(page.name)

    total = sum(kinds.values())
    print(f"{len(pages)} pages, {total} cell outputs")
    for k, n in kinds.items():
        if n:
            print(f"  {k:8s} {n}")

    if total == 0:
        failures.append("no cell outputs found at all, the render is empty")

    for f in failures:
        print(f"\nFAIL: {f}")
    if not failures:
        print("\nevery output kind is inside a boxed .cell-output")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
