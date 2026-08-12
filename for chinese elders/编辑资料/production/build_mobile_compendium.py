#!/usr/bin/env python3
"""Build all six volumes as one linked, standard-size mobile PDF."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    PageBreak,
    PageBreakIfNotEmpty,
    PageTemplate,
    Paragraph,
    Spacer,
)
from reportlab.platypus.tableofcontents import TableOfContents

import build_pdf_series as series


BOOK_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "output/pdf"
OUTPUT_PATH = OUTPUT_DIR / "看懂AI-六册合订手机版-标准字版.pdf"
AUTHOR_NAME = "爱吃的小柒"
AUTHOR_DESCRIPTION = "哥伦比亚大学 AI 研究及硅谷 AI 创业者"

# 14.2 pt * 1.1 = 15.62 pt, approximately 20.8 CSS px.  On the
# 430-point mobile page this gives about 20-26 Chinese characters per line.
FONT_SCALE = 1.1


class CompendiumDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str):
        super().__init__(
            filename,
            pagesize=series.PAGE_SIZE,
            leftMargin=series.LEFT,
            rightMargin=series.RIGHT,
            topMargin=series.TOP,
            bottomMargin=series.BOTTOM,
            title="《看懂 AI》六册合订手机版",
            author=AUTHOR_NAME,
            subject="面向年长读者的生成式 AI 中文读本，手机版标准字号合订本",
        )
        self.toc_key = "combined-toc"
        self.heading_counter = 0
        self.current_volume: series.Volume | None = None
        frame = Frame(
            series.LEFT,
            series.BOTTOM,
            series.CONTENT_WIDTH,
            series.PAGE_HEIGHT - series.TOP - series.BOTTOM,
            id="main",
        )
        self.addPageTemplates(PageTemplate(id="book", frames=[frame], onPage=self.draw_page))

    @property
    def volume(self) -> series.Volume:
        # series.heading_flowable uses doc.volume for unique bookmark names.
        return self.current_volume or series.VOLUMES[0]

    def beforeDocument(self) -> None:
        self.current_volume = None
        self.heading_counter = 0

    def draw_page(self, canvas, doc) -> None:
        canvas.saveState()
        canvas.setFillColor(series.WARM)
        canvas.rect(0, 0, series.PAGE_WIDTH, series.PAGE_HEIGHT, stroke=0, fill=1)
        if doc.page > 1:
            canvas.setStrokeColor(series.LINE)
            canvas.line(
                series.LEFT,
                series.PAGE_HEIGHT - 29,
                series.PAGE_WIDTH - series.RIGHT,
                series.PAGE_HEIGHT - 29,
            )
            footer_size = 8.5 * FONT_SCALE
            canvas.setFont("HeitiLight", footer_size)
            canvas.setFillColor(series.MUTED)
            canvas.drawString(series.LEFT, series.PAGE_HEIGHT - 21, "《看懂 AI》六册合订本")
            canvas.drawCentredString(series.PAGE_WIDTH / 2, 22, str(doc.page))
            label = "返回总目录"
            width = series.pdfmetrics.stringWidth(label, "HeitiLight", footer_size)
            x = series.PAGE_WIDTH - series.RIGHT - width
            canvas.setFillColor(series.ACCENT_DARK)
            canvas.drawString(x, 22, label)
            canvas.linkRect(
                "",
                self.toc_key,
                Rect=(x - 3, 17, series.PAGE_WIDTH - series.RIGHT + 3, 34),
                relative=0,
                thickness=0,
            )
        canvas.restoreState()

    def afterFlowable(self, flowable) -> None:
        if not isinstance(flowable, Paragraph):
            return
        key = getattr(flowable, "_bookmarkName", None)
        if not key:
            return

        if flowable.style.name == "VolumeTitle":
            level = 0
        elif flowable.style.name == "ChapterTitle":
            level = 1
        elif flowable.style.name == "SectionHeading":
            level = 2
        else:
            return

        text = flowable.getPlainText()
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level=level, closed=(level != 0))

        # The printed contents includes volumes and chapters.  Section-level
        # destinations remain available in the PDF reader's bookmark sidebar.
        if level <= 1:
            toc_text = "专题 看穿 AI 信息差销售" if text.startswith("专题") else text
            self.notify("TOCEntry", (level, toc_text, self.page, key))


def add_volume_title_style() -> None:
    series.STYLES["VolumeTitle"] = ParagraphStyle(
        "VolumeTitle",
        fontName="HeitiMedium",
        fontSize=30 * FONT_SCALE,
        leading=39 * FONT_SCALE,
        textColor=series.INK,
        spaceAfter=16,
        wordWrap="CJK",
    )


def master_cover() -> list[Flowable]:
    cover_image = Image(str(BOOK_ROOT / "assets/illustrations/learning-five-ai-tools-web.jpg"))
    cover_image._restrictSize(series.CONTENT_WIDTH, 150)
    return [
        Spacer(1, 28),
        Paragraph("《看懂 AI》老年人 AI 读本", series.STYLES["CoverSeries"]),
        Paragraph("六册合订手机版", series.STYLES["CoverTitle"]),
        Paragraph(
            "看懂模型与产品，学会对话、写作、作图、修照片和编程；辨别信息，保护钱财与隐私。",
            series.STYLES["CoverSubtitle"],
        ),
        Spacer(1, 8),
        cover_image,
        Spacer(1, 14),
        Paragraph(f"作者：{AUTHOR_NAME}", series.STYLES["CoverAuthor"]),
        Paragraph(AUTHOR_DESCRIPTION, series.STYLES["CoverAuthorDescription"]),
        Spacer(1, 8),
        Paragraph("手机竖屏 · 标准字号 · 2026-08-13", series.STYLES["CoverSeries"]),
        PageBreak(),
    ]


def volume_cover(volume: series.Volume) -> list[Flowable]:
    title = Paragraph(f"第 {volume.number} 册｜{volume.title}", series.STYLES["VolumeTitle"])
    title._bookmarkName = f"volume-{volume.number}"
    image = Image(str(BOOK_ROOT / volume.cover_image))
    image._restrictSize(series.CONTENT_WIDTH, 125)
    return [
        Spacer(1, 42),
        Paragraph(f"全六册 · 第 {volume.number} 册", series.STYLES["CoverSeries"]),
        title,
        Paragraph(volume.subtitle, series.STYLES["CoverSubtitle"]),
        image,
        Spacer(1, 14),
        Paragraph(volume.description, series.STYLES["CoverDescription"]),
        PageBreak(),
    ]


def build() -> Path:
    series.FONT_SCALE = FONT_SCALE
    series.register_fonts()
    series.STYLES = series.make_styles()
    add_volume_title_style()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    glossary = series.glossary_map()
    doc = CompendiumDocTemplate(str(OUTPUT_PATH))
    story: list[Flowable] = master_cover()

    story.extend(
        [
            series.BookmarkFlowable(doc.toc_key),
            Paragraph("总目录", series.STYLES["TocTitle"]),
        ]
    )
    toc = TableOfContents()
    toc.levelStyles = [series.STYLES["Toc0"], series.STYLES["Toc1"]]
    toc.dotsMinLevel = 0
    story.append(toc)

    for volume in series.VOLUMES:
        doc.current_volume = volume
        story.append(PageBreakIfNotEmpty())
        story.extend(volume_cover(volume))

        story.append(Paragraph("本册学习目标", series.STYLES["Subheading"]))
        story.append(Paragraph(volume.description, series.STYLES["Body"]))
        story.append(
            Paragraph(
                "阅读技术词时，请依次看准确解释、明确标注的生活比方、比方边界，以及“作为用户，这对您意味着什么”。英文只用于帮助识别产品页面中的常见写法，旁边保留中文名称或说明。",
                series.STYLES["UserMeaning"],
            )
        )
        story.append(PageBreak())

        for source_index, relative in enumerate(volume.sources):
            if source_index:
                story.append(PageBreak())
            source = BOOK_ROOT / relative
            story.extend(
                series.render_markdown(source.read_text(encoding="utf-8"), source.parent, doc)
            )

        story.append(PageBreak())
        story.append(series.heading_flowable("本册词汇卡", 1, doc))
        story.append(
            Paragraph(
                "这些词只选取本册实际使用的概念。每个词先给准确解释，再给明确标注的生活比方和比方边界。",
                series.STYLES["Body"],
            )
        )
        for term in volume.glossary:
            if term not in glossary:
                raise KeyError(f"Glossary term not found: {term}")
            story.extend(series.render_markdown(glossary[term], BOOK_ROOT / "manuscript", doc))

        references = BOOK_ROOT / "manuscript/references" / f"{volume.number:02d}-sources.md"
        if not references.exists():
            raise FileNotFoundError(f"Missing volume references: {references}")
        story.append(PageBreak())
        story.extend(
            series.render_markdown(
                references.read_text(encoding="utf-8"), references.parent, doc
            )
        )

    doc.multiBuild(story)
    return OUTPUT_PATH


if __name__ == "__main__":
    print(build())
