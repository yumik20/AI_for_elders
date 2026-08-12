#!/usr/bin/env python3
"""Check terminology and language invariants for the AI-literacy manuscript."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_FILES = [
    ROOT / "BOOK-OUTLINE.md",
    *sorted((ROOT / "manuscript").glob("**/*.md")),
]


def check_no_japanese() -> list[str]:
    errors: list[str] = []
    pattern = re.compile(r"[\u3040-\u30ff\u31f0-\u31ff]")
    for path in TEXT_FILES:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if pattern.search(line):
                errors.append(f"{path.relative_to(ROOT)}:{number}: contains Japanese kana")
    return errors


def check_glossary() -> list[str]:
    errors: list[str] = []
    path = ROOT / "manuscript/99-glossary.md"
    text = path.read_text(encoding="utf-8")
    entries = re.split(r"(?=^### )", text, flags=re.MULTILINE)[1:]
    for entry in entries:
        heading = entry.splitlines()[0].removeprefix("### ")
        for required in ("**准确解释：**", "**【这是一个比方】**", "**【比方的边界】**"):
            if required not in entry:
                errors.append(f"glossary entry '{heading}' is missing {required}")
    if "## 工程概念对用户的直接意义索引" not in text:
        errors.append("glossary is missing the user-significance index")
    return errors


def main() -> int:
    errors = check_no_japanese() + check_glossary()
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Manuscript checks passed: {len(TEXT_FILES)} files; no Japanese kana; glossary structure complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
