"""Count prose words in a .qmd, ignoring code, tables, YAML and headings.

    python misc/wordcount.py chapters/03-concepts/models.qmd

The number it reports is what the reader actually has to read. Code blocks and reference
tables are not prose and are not counted, so cutting a table will not move it.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from prosecheck import paragraphs, sentences  # noqa: E402


def words(path: Path) -> int:
    return sum(len(s.split()) for p in paragraphs(path.read_text()) for s in sentences(p))


def main(argv: list[str]) -> int:
    paths = []
    for a in argv or ["chapters"]:
        p = Path(a)
        paths.extend(sorted(q for q in p.rglob("*.qmd") if not q.name.startswith("_"))
                     if p.is_dir() else [p])
    total = 0
    for p in paths:
        n = words(p)
        total += n
        print(f"{n:6,}  {p}")
    if len(paths) > 1:
        print(f"{total:6,}  TOTAL")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
