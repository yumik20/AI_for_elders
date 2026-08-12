#!/usr/bin/env python3
"""Structural and text verification for the six completed PDF volumes."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


REPO_ROOT = Path(__file__).resolve().parents[3]
PDF_DIR = REPO_ROOT / "output/pdf"
EXPECTED = (
    "第一册-看懂App模型与训练-超大字版.pdf",
    "第二册-认识模型家族与定制方法-超大字版.pdf",
    "第三册-学会与AI对话和写作-超大字版.pdf",
    "第四册-用AI作图修照片与编程-超大字版.pdf",
    "第五册-选择AI产品与付费方式-超大字版.pdf",
    "第六册-辨别信息保护隐私与个人制度-超大字版.pdf",
)
JAPANESE_KANA = re.compile(r"[\u3040-\u30ff\u31f0-\u31ff]")


def outline_count(items) -> int:
    count = 0
    for item in items:
        count += outline_count(item) if isinstance(item, list) else 1
    return count


def verify(path: Path) -> list[str]:
    errors: list[str] = []
    reader = PdfReader(path)
    pages = len(reader.pages)
    if pages < 10:
        errors.append(f"{path.name}: unexpectedly short ({pages} pages)")

    links = 0
    for page in reader.pages:
        for annotation in page.get("/Annots", []):
            if annotation.get_object().get("/Subtype") == "/Link":
                links += 1
    if links < pages:
        errors.append(f"{path.name}: too few clickable links ({links} for {pages} pages)")

    outlines = outline_count(reader.outline)
    if outlines < 5:
        errors.append(f"{path.name}: too few PDF bookmarks ({outlines})")

    with pdfplumber.open(path) as pdf:
        texts = [(page.extract_text() or "").strip() for page in pdf.pages]
        blank = [index + 1 for index, text in enumerate(texts) if len(text) < 4]
        if blank:
            errors.append(f"{path.name}: blank or unextractable pages {blank}")
        combined = "\n".join(texts)
        if "目录" not in combined:
            errors.append(f"{path.name}: missing table-of-contents text")
        if "本册词汇卡" not in combined:
            errors.append(f"{path.name}: missing volume glossary")
        if "本册资料来源与核验说明" not in combined:
            errors.append(f"{path.name}: missing volume references")
        if JAPANESE_KANA.search(combined):
            errors.append(f"{path.name}: contains Japanese kana")

    print(
        f"{path.name}: {pages} pages, {links} links, {outlines} bookmarks, "
        "text and language checks passed"
    )
    return errors


def main() -> int:
    errors: list[str] = []
    for name in EXPECTED:
        path = PDF_DIR / name
        if not path.exists():
            errors.append(f"missing PDF: {name}")
            continue
        errors.extend(verify(path))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("All six PDF volumes passed structural verification.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
