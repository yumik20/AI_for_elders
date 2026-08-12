#!/usr/bin/env python3
"""Create one page-thumbnail contact sheet for each rendered PDF volume."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[3]
RENDER_ROOT = REPO_ROOT / "tmp/pdfs"


def page_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    return int(match.group(1)) if match else 0


def build_sheet(directory: Path) -> Path:
    pages = sorted(directory.glob("page-*.png"), key=page_number)
    if not pages:
        raise FileNotFoundError(f"No rendered pages in {directory}")
    columns = 8
    thumb_width = 115
    label_height = 20
    gap = 10
    with Image.open(pages[0]) as sample:
        ratio = sample.height / sample.width
    thumb_height = round(thumb_width * ratio)
    rows = (len(pages) + columns - 1) // columns
    width = gap + columns * (thumb_width + gap)
    height = gap + rows * (thumb_height + label_height + gap)
    sheet = Image.new("RGB", (width, height), "#ddd8cf")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, page in enumerate(pages):
        row, column = divmod(index, columns)
        x = gap + column * (thumb_width + gap)
        y = gap + row * (thumb_height + label_height + gap)
        with Image.open(page) as image:
            image = image.convert("RGB")
            image.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            sheet.paste(image, (x, y))
        label = f"p{page_number(page):03d}"
        draw.text((x, y + thumb_height + 4), label, fill="#172522", font=font)
    output = directory / "contact-sheet.jpg"
    sheet.save(output, quality=90)
    return output


def main() -> None:
    for directory in sorted(RENDER_ROOT.glob("vol*")):
        print(build_sheet(directory))


if __name__ == "__main__":
    main()

