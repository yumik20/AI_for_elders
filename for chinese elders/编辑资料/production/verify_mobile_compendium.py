#!/usr/bin/env python3
"""Verify structure and extractable content in the mobile PDF compendium."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


REPO_ROOT = Path(__file__).resolve().parents[3]
PDF_PATH = REPO_ROOT / "output/pdf/看懂AI-六册合订手机版-标准字版.pdf"
JAPANESE_KANA = re.compile(r"[\u3040-\u30ff\u31f0-\u31ff]")


def outline_count(items) -> int:
    return sum(outline_count(item) if isinstance(item, list) else 1 for item in items)


def main() -> int:
    errors: list[str] = []
    if not PDF_PATH.exists():
        print(f"Missing PDF: {PDF_PATH}", file=sys.stderr)
        return 1

    reader = PdfReader(PDF_PATH)
    pages = len(reader.pages)
    if pages < 250:
        errors.append(f"unexpectedly short: {pages} pages")

    links = sum(
        1
        for page in reader.pages
        for annotation in page.get("/Annots", [])
        if annotation.get_object().get("/Subtype") == "/Link"
    )
    if links < pages:
        errors.append(f"too few clickable links: {links} for {pages} pages")

    outlines = outline_count(reader.outline)
    if outlines < 100:
        errors.append(f"too few PDF bookmarks: {outlines}")

    if reader.metadata.author != "爱吃的小柒":
        errors.append(f"unexpected PDF author: {reader.metadata.author!r}")

    with pdfplumber.open(PDF_PATH) as pdf:
        texts = [(page.extract_text() or "").strip() for page in pdf.pages]
    blank = [index + 1 for index, text in enumerate(texts) if len(text) < 4]
    if blank:
        errors.append(f"blank or unextractable pages: {blank}")

    combined = "\n".join(texts)
    required = (
        "六册合订手机版",
        "爱吃的小柒",
        "哥伦比亚大学 AI 研究及硅谷 AI 创业者",
        "总目录",
        "第 1 册",
        "第 6 册",
        "第 20 章",
        "本册词汇卡",
        "本册资料来源与核验说明",
    )
    for text in required:
        if text not in combined:
            errors.append(f"missing text: {text}")
    if JAPANESE_KANA.search(combined):
        errors.append("contains Japanese kana")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"{PDF_PATH.name}: {pages} pages, {links} links, {outlines} bookmarks; "
        "author, text, blank-page and language checks passed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
