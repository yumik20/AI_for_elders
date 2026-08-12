#!/usr/bin/env python3
"""Build the current Chinese AI-literacy book draft as one offline HTML file."""

from __future__ import annotations

import html
import base64
import mimetypes
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "老年人AI读本-超大字版.html"

SOURCES = [
    ("全书规划", ROOT / "BOOK-OUTLINE.md", "planning"),
    ("序言", ROOT / "manuscript/00-preface.md", "manuscript"),
    ("第 1 章", ROOT / "manuscript/01-model-is-not-the-app.md", "manuscript"),
    ("第 2 章", ROOT / "manuscript/02-how-models-learn.md", "manuscript"),
    ("专题", ROOT / "manuscript/02a-ai-information-gap-scams.md", "manuscript"),
    ("第 3 章", ROOT / "manuscript/03-ai-model-family.md", "manuscript"),
    ("第 4 章", ROOT / "manuscript/04-rag-finetuning-tools-agents.md", "manuscript"),
    ("第 5 章", ROOT / "manuscript/05-why-models-differ.md", "manuscript"),
    ("第 6 章", ROOT / "manuscript/06-prompt-engineering.md", "manuscript"),
    ("第 7 章", ROOT / "manuscript/07-chat-and-language-learning.md", "manuscript"),
    ("第 8 章", ROOT / "manuscript/08-writing-with-ai.md", "manuscript"),
    ("第 9 章", ROOT / "manuscript/09-image-generation.md", "manuscript"),
    ("第 10 章", ROOT / "manuscript/10-photo-restoration.md", "manuscript"),
    ("第 11 章", ROOT / "manuscript/11-coding-with-ai.md", "manuscript"),
    ("第 12 章", ROOT / "manuscript/12-mainland-ai-map.md", "manuscript"),
    ("第 13 章", ROOT / "manuscript/13-model-version-updates.md", "manuscript"),
    ("第 14 章", ROOT / "manuscript/14-ai-cost-and-payment.md", "manuscript"),
    ("第 15 章", ROOT / "manuscript/15-why-ai-is-wrong.md", "manuscript"),
    ("第 16 章", ROOT / "manuscript/16-recommendation-echo.md", "manuscript"),
    ("第 17 章", ROOT / "manuscript/17-six-step-verification.md", "manuscript"),
    ("第 18 章", ROOT / "manuscript/18-high-stakes-ai.md", "manuscript"),
    ("第 19 章", ROOT / "manuscript/19-privacy-data-exit.md", "manuscript"),
    ("第 20 章", ROOT / "manuscript/20-personal-ai-workbench.md", "manuscript"),
    ("附录 A", ROOT / "manuscript/99-glossary.md", "glossary"),
    ("第一册资料来源", ROOT / "manuscript/references/01-sources.md", "reference"),
    ("第二册资料来源", ROOT / "manuscript/references/02-sources.md", "reference"),
    ("第三册资料来源", ROOT / "manuscript/references/03-sources.md", "reference"),
    ("第四册资料来源", ROOT / "manuscript/references/04-sources.md", "reference"),
    ("第五册资料来源", ROOT / "manuscript/references/05-sources.md", "reference"),
    ("第六册资料来源", ROOT / "manuscript/references/06-sources.md", "reference"),
    (
        "动态参考页",
        ROOT / "research/mainland-ai-product-landscape.md",
        "reference",
    ),
]


def inline(text: str) -> str:
    """Render the small inline-Markdown subset used by the manuscript."""
    placeholders: list[str] = []

    def hold(value: str) -> str:
        placeholders.append(value)
        return f"\x00{len(placeholders) - 1}\x00"

    def code_repl(match: re.Match[str]) -> str:
        return hold(f"<code>{html.escape(match.group(1))}</code>")

    def link_repl(match: re.Match[str]) -> str:
        label = html.escape(match.group(1))
        href = html.escape(match.group(2), quote=True)
        if href.startswith("#"):
            return hold(f'<a href="{href}">{label}</a>')
        return hold(f'<a href="{href}" target="_blank" rel="noopener noreferrer">{label}</a>')

    text = re.sub(r"`([^`]+)`", code_repl, text)
    text = re.sub(r"\[([^]]+)]\(([^)]+)\)", link_repl, text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = text.replace("  ", "<br>")

    for index, value in enumerate(placeholders):
        text = text.replace(f"\x00{index}\x00", value)
    return text


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def make_id(counter: int) -> str:
    return f"section-{counter}"


def heading_id_for(title: str, counter: int, canonical_chapters: bool = False) -> str:
    if canonical_chapters:
        chapter = re.match(r"第\s*(\d+)\s*章", title)
        if chapter:
            return f"chapter-{int(chapter.group(1))}"
        if title.startswith("序言"):
            return "preface"
        if title.startswith("专题"):
            return "topic-ai-information-gap"
    return make_id(counter)


def image_source(value: str, base_dir: Path) -> str:
    """Embed local assets so the preview remains one portable offline file."""
    if value.startswith(("http://", "https://", "data:")):
        return value
    path = (base_dir / value).resolve()
    if not path.is_file():
        return value
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def render_markdown(
    markdown: str, base_dir: Path, id_start: int = 0, canonical_chapters: bool = False
) -> tuple[str, list[dict], int]:
    lines = markdown.splitlines()
    output: list[str] = []
    toc: list[dict] = []
    heading_counter = id_start
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        image_match = re.fullmatch(r"!\[([^]]*)]\(([^)]+)\)", stripped)
        if image_match:
            alt = image_match.group(1).strip()
            source = image_source(image_match.group(2).strip(), base_dir)
            output.append(
                '<figure class="editorial-figure">'
                f'<img src="{html.escape(source, quote=True)}" alt="{html.escape(alt, quote=True)}" '
                'loading="eager" decoding="sync">'
                f"<figcaption>{inline(alt)}</figcaption></figure>"
            )
            index += 1
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            index += 1
            language_class = f" language-{html.escape(language)}" if language else ""
            output.append(
                f'<pre class="code-card"><code class="{language_class.strip()}">'
                f"{html.escape(chr(10).join(code_lines))}</code></pre>"
            )
            continue

        heading_match = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            heading_counter += 1
            heading_id = heading_id_for(title, heading_counter, canonical_chapters)
            output.append(
                f'<h{level} id="{heading_id}"><a class="heading-anchor" '
                f'href="#{heading_id}" aria-label="链接到本节">{inline(title)}</a></h{level}>'
            )
            if level <= 2:
                toc.append({"level": level, "title": re.sub(r"[*`]", "", title), "id": heading_id})
            index += 1
            continue

        if stripped in {"---", "***", "___"}:
            output.append('<hr class="section-break">')
            index += 1
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].strip())
                index += 1
            output.append(f'<blockquote>{"<br>".join(inline(item) for item in quote_lines)}</blockquote>')
            continue

        if (
            stripped.startswith("|")
            and index + 1 < len(lines)
            and is_table_separator(lines[index + 1])
        ):
            headers = [cell.strip() for cell in stripped.strip("|").split("|")]
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            table = ['<div class="table-scroll" role="region" tabindex="0"><table><thead><tr>']
            table.extend(f"<th>{inline(cell)}</th>" for cell in headers)
            table.append("</tr></thead><tbody>")
            for row in rows:
                table.append("<tr>")
                for cell_index in range(len(headers)):
                    cell = row[cell_index] if cell_index < len(row) else ""
                    table.append(f"<td>{inline(cell)}</td>")
                table.append("</tr>")
            table.append("</tbody></table></div>")
            output.append("".join(table))
            continue

        unordered = re.match(r"^-\s+(.+)$", stripped)
        if unordered:
            items: list[str] = []
            while index < len(lines):
                match = re.match(r"^-\s+(.+)$", lines[index].strip())
                if not match:
                    break
                items.append(match.group(1))
                index += 1
            output.append("<ul>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ul>")
            continue

        ordered = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if ordered:
            items = []
            while index < len(lines):
                match = re.match(r"^\d+[.)]\s+(.+)$", lines[index].strip())
                if not match:
                    break
                items.append(match.group(1))
                index += 1
            output.append("<ol>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ol>")
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index].strip()
            if not candidate:
                break
            if (
                candidate.startswith(("#", ">", "```", "|", "- "))
                or candidate in {"---", "***", "___"}
                or re.match(r"^\d+[.)]\s+", candidate)
            ):
                break
            paragraph_lines.append(candidate)
            index += 1
        paragraph_class = ""
        if paragraph_lines[0].startswith("**【这是一个比方】"):
            paragraph_class = ' class="term-callout analogy"'
        elif paragraph_lines[0].startswith("**【比方的边界】"):
            paragraph_class = ' class="term-callout boundary"'
        elif paragraph_lines[0].startswith("**【作为用户，这对您意味着什么】"):
            paragraph_class = ' class="term-callout user-meaning"'
        elif paragraph_lines[0].startswith(("**【回看前文】", "**【前册回顾】")):
            paragraph_class = ' class="term-callout cross-reference"'
        output.append(
            f'<p{paragraph_class}>{" ".join(inline(item) for item in paragraph_lines)}</p>'
        )

    return "\n".join(output), toc, heading_counter


def document() -> str:
    articles: list[str] = []
    navigation: list[dict] = []
    heading_counter = 0

    for label, source, kind in SOURCES:
        rendered, toc, heading_counter = render_markdown(
            source.read_text(encoding="utf-8"),
            source.parent,
            heading_counter,
            canonical_chapters=(kind == "manuscript"),
        )
        navigation.extend(toc)
        note = ""
        if kind == "planning":
            note = '<p class="document-note">本页是全书规划，不是已完成正文。</p>'
        elif kind == "reference":
            note = (
                '<p class="document-note warning">动态资料：版本、价格和登录方式会变化，'
                "使用前请查看核验日期和官方页面。</p>"
            )
        articles.append(
            f'<article class="book-section {kind}" data-label="{html.escape(label)}">'
            f"{note}{rendered}</article>"
        )

    nav_items = []
    for entry in navigation:
        class_name = "toc-chapter" if entry["level"] == 1 else "toc-section"
        nav_items.append(
            f'<a class="{class_name}" href="#{entry["id"]}">{html.escape(entry["title"])}</a>'
        )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="color-scheme" content="light dark">
  <meta name="description" content="《看懂 AI》成人手机大字版书稿预览">
  <title>看懂 AI｜手机大字版书稿预览</title>
  <style>
    :root {{
      color-scheme: light;
      --paper: #fbf7ef;
      --paper-raised: #fffdf8;
      --ink: #172522;
      --muted: #64706c;
      --line: #d9d1c2;
      --accent: #087f73;
      --accent-dark: #075e57;
      --accent-soft: #dcefeb;
      --gold: #bd7c23;
      --warning-bg: #fff0d4;
      --warning-ink: #70450c;
      --code-bg: #122623;
      --code-ink: #f1f7f5;
      --base-size: 40px;
      --measure: 780px;
      --shadow: 0 14px 45px rgba(45, 55, 50, .10);
    }}

    html[data-theme="dark"] {{
      color-scheme: dark;
      --paper: #101816;
      --paper-raised: #17211f;
      --ink: #edf4f1;
      --muted: #aab8b3;
      --line: #35443f;
      --accent: #62c8ba;
      --accent-dark: #83d7cb;
      --accent-soft: #203c37;
      --gold: #e5b465;
      --warning-bg: #46381f;
      --warning-ink: #ffdda2;
      --code-bg: #09100f;
      --code-ink: #e7f2ef;
      --shadow: 0 14px 45px rgba(0, 0, 0, .35);
    }}

    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; scroll-padding-top: 92px; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
      font-size: var(--base-size);
      line-height: 1.78;
      text-rendering: optimizeLegibility;
    }}
    a {{ color: var(--accent-dark); text-decoration-thickness: .08em; text-underline-offset: .16em; }}
    button {{ font: inherit; }}
    :focus-visible {{ outline: 3px solid var(--gold); outline-offset: 3px; }}

    .progress-track {{ position: fixed; inset: 0 0 auto; height: 5px; z-index: 100; background: transparent; }}
    .progress-bar {{ height: 100%; width: 0; background: linear-gradient(90deg, var(--gold), var(--accent)); }}

    .reader-bar {{
      position: sticky;
      top: 0;
      z-index: 90;
      min-height: 66px;
      padding: 9px max(14px, env(safe-area-inset-right)) 9px max(14px, env(safe-area-inset-left));
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      background: color-mix(in srgb, var(--paper-raised) 92%, transparent);
      border-bottom: 1px solid var(--line);
      backdrop-filter: blur(16px);
    }}
    .reader-title {{ font-size: 28px; font-weight: 750; letter-spacing: .03em; white-space: nowrap; }}
    .reader-controls {{ display: flex; align-items: center; gap: 7px; }}
    .reader-controls button {{
      width: 64px;
      height: 64px;
      padding: 0;
      display: inline-grid;
      place-items: center;
      border: 1px solid var(--line);
      border-radius: 50%;
      color: var(--ink);
      background: var(--paper-raised);
      cursor: pointer;
      font-size: 24px;
      font-weight: 760;
    }}
    .reader-controls button:first-child {{ width: auto; padding: 0 14px; border-radius: 24px; }}

    .cover {{
      min-height: calc(100vh - 66px);
      min-height: calc(100svh - 66px);
      padding: clamp(50px, 11vh, 120px) 24px 54px;
      display: grid;
      align-content: center;
      background:
        radial-gradient(circle at 85% 10%, color-mix(in srgb, var(--accent) 18%, transparent), transparent 32%),
        radial-gradient(circle at 10% 80%, color-mix(in srgb, var(--gold) 17%, transparent), transparent 34%),
        var(--paper);
      border-bottom: 1px solid var(--line);
    }}
    .cover-inner {{ width: min(100%, 860px); margin: 0 auto; }}
    .eyebrow {{ margin: 0 0 24px; color: var(--accent-dark); font-size: .86em; font-weight: 780; letter-spacing: .12em; }}
    .cover h1 {{ margin: 0; max-width: 8em; font-family: "Songti SC", "STSong", serif; font-size: clamp(80px, 22vw, 128px); line-height: 1.05; letter-spacing: -.04em; }}
    .cover-subtitle {{ max-width: 25em; margin: 30px 0 0; font-family: "Songti SC", "STSong", serif; font-size: clamp(50px, 12vw, 76px); line-height: 1.4; }}
    .cover-promise {{ max-width: 32em; margin: 28px 0 0; color: var(--muted); }}
    .status-row {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 32px; }}
    .status-pill {{ padding: 7px 13px; border: 1px solid var(--line); border-radius: 999px; background: var(--paper-raised); font-size: .78em; font-weight: 700; }}

    main {{ width: min(100%, var(--measure)); margin: 0 auto; padding: 46px 22px 120px; }}
    .book-section {{ margin: 0 0 110px; }}
    .book-section + .book-section {{ padding-top: 68px; border-top: 1px solid var(--line); }}
    .book-section.planning, .book-section.reference {{
      padding: 28px clamp(18px, 5vw, 42px) 46px;
      border: 1px solid var(--line);
      border-radius: 22px;
      background: var(--paper-raised);
      box-shadow: var(--shadow);
    }}
    .book-section.reference {{ margin-top: 90px; }}

    h1, h2, h3, h4 {{ color: var(--ink); line-height: 1.32; text-wrap: balance; }}
    h1 {{ margin: 0 0 1.2em; font-family: "Songti SC", "STSong", serif; font-size: clamp(80px, 18vw, 128px); letter-spacing: -.035em; }}
    h2 {{ margin: 2.8em 0 .75em; padding-top: .25em; font-size: clamp(56px, 12vw, 74px); letter-spacing: -.025em; }}
    h3 {{ margin: 2.1em 0 .65em; font-size: 1.26em; }}
    h4 {{ margin: 1.8em 0 .5em; font-size: 1.08em; }}
    .heading-anchor {{ color: inherit; text-decoration: none; }}
    p {{ margin: 0 0 1.18em; }}
    strong {{ color: color-mix(in srgb, var(--ink) 86%, var(--accent)); }}
    ul, ol {{ margin: .6em 0 1.4em; padding-left: 1.35em; }}
    li {{ margin: .42em 0; padding-left: .25em; }}
    li::marker {{ color: var(--accent); font-weight: 800; }}

    blockquote {{
      margin: 1.8em 0;
      padding: 1.1em 1.15em 1.1em 1.35em;
      border-left: 6px solid var(--accent);
      border-radius: 0 14px 14px 0;
      background: var(--accent-soft);
      font-family: "Songti SC", "STSong", serif;
      font-size: 1.13em;
      line-height: 1.72;
    }}
    .code-card {{
      margin: 1.6em 0;
      padding: 1.25em;
      overflow-x: auto;
      border-radius: 16px;
      background: var(--code-bg);
      color: var(--code-ink);
      font-size: .84em;
      line-height: 1.7;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      box-shadow: var(--shadow);
    }}
    :not(pre) > code {{ padding: .12em .38em; border-radius: 6px; background: var(--accent-soft); font-size: .88em; }}
    .table-scroll {{ margin: 1.5em 0 2em; overflow-x: auto; border: 1px solid var(--line); border-radius: 14px; background: var(--paper-raised); }}
    table {{ width: 100%; min-width: 620px; border-collapse: collapse; font-size: .82em; line-height: 1.55; }}
    th, td {{ padding: 14px 15px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ position: sticky; top: 0; background: var(--accent-soft); color: var(--ink); font-weight: 800; }}
    tr:last-child td {{ border-bottom: 0; }}
    .section-break {{ width: 80px; margin: 80px auto; border: 0; border-top: 3px solid var(--gold); }}
    .document-note {{ margin: 0 0 2em; padding: .8em 1em; border-radius: 12px; background: var(--accent-soft); font-size: .84em; font-weight: 700; }}
    .document-note.warning {{ background: var(--warning-bg); color: var(--warning-ink); }}
    .term-callout {{
      margin: 1em 0;
      padding: .9em 1em;
      border-radius: 12px;
      border-left: 6px solid var(--accent);
      background: var(--paper-raised);
    }}
    .term-callout.analogy {{ background: var(--accent-soft); }}
    .term-callout.boundary {{
      border-left-color: var(--gold);
      background: color-mix(in srgb, var(--warning-bg) 55%, var(--paper-raised));
    }}
    .term-callout.user-meaning {{
      border: 2px solid var(--accent);
      border-left-width: 7px;
      background: var(--paper-raised);
      box-shadow: 0 7px 22px rgba(45, 55, 50, .07);
    }}
    .term-callout.cross-reference {{
      border-left-color: var(--muted);
      background: color-mix(in srgb, var(--accent-soft) 48%, var(--paper-raised));
      color: var(--muted);
      font-size: .9em;
    }}
    .editorial-figure {{ margin: 1.4em 0 2.4em; }}
    .editorial-figure img {{
      display: block;
      width: 100%;
      height: auto;
      border-radius: 18px;
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
    }}
    .editorial-figure figcaption {{
      margin: .7em .4em 0;
      color: var(--muted);
      font-size: .75em;
      line-height: 1.55;
    }}

    .drawer-backdrop {{ position: fixed; inset: 0; z-index: 104; display: none; background: rgba(0,0,0,.38); }}
    .drawer {{
      position: fixed;
      inset: 0 auto 0 0;
      z-index: 105;
      width: min(88vw, 390px);
      padding: 22px 18px 80px;
      overflow-y: auto;
      transform: translateX(-105%);
      transition: transform .22s ease;
      background: var(--paper-raised);
      border-right: 1px solid var(--line);
      box-shadow: var(--shadow);
    }}
    body.drawer-open .drawer {{ transform: translateX(0); }}
    body.drawer-open .drawer-backdrop {{ display: block; }}
    .drawer-header {{ display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 22px; }}
    .drawer-header strong {{ font-size: 1.1em; }}
    .drawer-close {{ width: 46px; height: 46px; border: 1px solid var(--line); border-radius: 50%; background: var(--paper); color: var(--ink); cursor: pointer; }}
    .toc a {{ display: block; color: var(--ink); text-decoration: none; border-radius: 9px; }}
    .toc a:hover, .toc a.active {{ background: var(--accent-soft); color: var(--accent-dark); }}
    .toc-chapter {{ margin-top: 12px; padding: 11px 10px; font-weight: 800; }}
    .toc-section {{ padding: 7px 10px 7px 24px; color: var(--muted) !important; font-size: .82em; }}

    .footer {{ padding: 56px 22px 80px; border-top: 1px solid var(--line); color: var(--muted); text-align: center; font-size: 32px; }}
    .screen-reader-only {{ position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }}

    @media (max-width: 520px) {{
      .reader-title {{ display: none; }}
      .reader-controls {{ width: 100%; justify-content: space-between; }}
      main {{ padding-inline: 19px; }}
      .book-section.planning, .book-section.reference {{ margin-inline: -5px; padding-inline: 18px; }}
      table {{ min-width: 560px; }}
    }}

    @media print {{
      :root {{ --paper: #fff; --paper-raised: #fff; --ink: #000; --muted: #333; --line: #aaa; --base-size: 13pt; }}
      .reader-bar, .progress-track, .drawer, .drawer-backdrop {{ display: none !important; }}
      .cover {{ min-height: 90vh; page-break-after: always; background: #fff; }}
      main {{ width: 100%; max-width: none; padding: 0; }}
      .book-section {{ page-break-before: always; }}
      .book-section.planning, .book-section.reference {{ border: 0; box-shadow: none; padding: 0; }}
      h1, h2, h3 {{ break-after: avoid; }}
      p, li, blockquote, table {{ orphans: 3; widows: 3; }}
      a {{ color: #000; }}
    }}
  </style>
</head>
<body>
  <div class="progress-track" aria-hidden="true"><div class="progress-bar" id="progressBar"></div></div>
  <header class="reader-bar">
    <div class="reader-title">《看懂 AI》试读稿</div>
    <div class="reader-controls" aria-label="阅读设置">
      <button id="tocButton" type="button" aria-expanded="false" aria-controls="tocDrawer">目录</button>
      <button id="fontDown" type="button" aria-label="减小字号">A−</button>
      <button id="fontUp" type="button" aria-label="增大字号">A＋</button>
      <button id="themeButton" type="button" aria-label="切换明暗模式">◐</button>
    </div>
  </header>

  <aside class="drawer" id="tocDrawer" aria-label="本书目录">
    <div class="drawer-header"><strong>目录</strong><button class="drawer-close" id="drawerClose" type="button" aria-label="关闭目录">×</button></div>
    <nav class="toc">{"".join(nav_items)}</nav>
  </aside>
  <div class="drawer-backdrop" id="drawerBackdrop" aria-hidden="true"></div>

  <section class="cover" aria-labelledby="bookTitle">
    <div class="cover-inner">
      <p class="eyebrow">成人 AI 素养 · 手机大字版 · 试读稿 0.5</p>
      <h1 id="bookTitle">看懂<br>AI</h1>
      <p class="cover-subtitle">模型、应用、信息与选择</p>
      <p class="cover-promise">一本写给希望独立判断的成年人的手机读本。理解界面背后的系统，保留自己的选择权。</p>
      <div class="status-row" aria-label="书稿状态">
        <span class="status-pill">已完成序言</span>
        <span class="status-pill">已完成 11 / 20 章</span>
        <span class="status-pill">附 54 项工程词汇</span>
        <span class="status-pill">动态资料核验至 2026-08-12</span>
      </div>
    </div>
  </section>

  <main id="content">
    {"".join(articles)}
  </main>

  <footer class="footer">
    <p>《看懂 AI》书稿预览 · 生成于 {date.today().isoformat()}</p>
    <p>版本、价格和服务可用性会变化；重要决定请核对官方来源。</p>
  </footer>

  <script>
    (() => {{
      const root = document.documentElement;
      const body = document.body;
      const minSize = 18;
      const maxSize = 26;
      const savedSize = Number(localStorage.getItem('aiBookFontSize')) || 20;
      root.style.setProperty('--base-size', `${{Math.min(maxSize, Math.max(minSize, savedSize))}}px`);

      function setFont(delta) {{
        const current = parseInt(getComputedStyle(root).getPropertyValue('--base-size'), 10);
        const next = Math.min(maxSize, Math.max(minSize, current + delta));
        root.style.setProperty('--base-size', `${{next}}px`);
        localStorage.setItem('aiBookFontSize', String(next));
      }}

      document.getElementById('fontDown').addEventListener('click', () => setFont(-2));
      document.getElementById('fontUp').addEventListener('click', () => setFont(2));

      const preferredDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const savedTheme = localStorage.getItem('aiBookTheme');
      root.dataset.theme = savedTheme || (preferredDark ? 'dark' : 'light');
      document.getElementById('themeButton').addEventListener('click', () => {{
        root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('aiBookTheme', root.dataset.theme);
      }});

      const tocButton = document.getElementById('tocButton');
      const drawerClose = document.getElementById('drawerClose');
      const drawerBackdrop = document.getElementById('drawerBackdrop');
      function toggleDrawer(open) {{
        body.classList.toggle('drawer-open', open);
        tocButton.setAttribute('aria-expanded', String(open));
        if (open) drawerClose.focus();
      }}
      tocButton.addEventListener('click', () => toggleDrawer(true));
      drawerClose.addEventListener('click', () => toggleDrawer(false));
      drawerBackdrop.addEventListener('click', () => toggleDrawer(false));
      document.querySelectorAll('.toc a').forEach(link => link.addEventListener('click', () => toggleDrawer(false)));
      document.addEventListener('keydown', event => {{ if (event.key === 'Escape') toggleDrawer(false); }});

      function updateProgress() {{
        const scrollable = document.documentElement.scrollHeight - window.innerHeight;
        const percent = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
        document.getElementById('progressBar').style.width = `${{Math.min(100, percent)}}%`;
      }}
      updateProgress();
      window.addEventListener('scroll', updateProgress, {{ passive: true }});

      const navLinks = [...document.querySelectorAll('.toc a')];
      const sections = navLinks.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
      const observer = new IntersectionObserver(entries => {{
        const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
        if (!visible) return;
        navLinks.forEach(link => link.classList.toggle('active', link.getAttribute('href') === `#${{visible.target.id}}`));
      }}, {{ rootMargin: '-15% 0px -72% 0px' }});
      sections.forEach(section => observer.observe(section));
    }})();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    OUTPUT.write_text(document(), encoding="utf-8")
    print(OUTPUT)
