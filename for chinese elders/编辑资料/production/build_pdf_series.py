#!/usr/bin/env python3
"""Build the completed AI-literacy manuscript as six linked mobile PDFs."""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.graphics.shapes import String as DrawingString
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents
from svglib.svglib import svg2rlg


BOOK_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "output/pdf"
FONT_SCALE = 2.0

PAGE_SIZE = (430, 760)
PAGE_WIDTH, PAGE_HEIGHT = PAGE_SIZE
LEFT = 38
RIGHT = 38
TOP = 52
BOTTOM = 48
CONTENT_WIDTH = PAGE_WIDTH - LEFT - RIGHT

INK = colors.HexColor("#172522")
MUTED = colors.HexColor("#5f706b")
ACCENT = colors.HexColor("#087f73")
ACCENT_DARK = colors.HexColor("#075e57")
ACCENT_SOFT = colors.HexColor("#dcefeb")
GOLD = colors.HexColor("#bd7c23")
WARM = colors.HexColor("#fbf7ef")
WHITE = colors.HexColor("#fffdf8")
WARNING = colors.HexColor("#fff0d4")
LINE = colors.HexColor("#d9d1c2")
CODE_BG = colors.HexColor("#16302c")
REFERENCE_BG = colors.HexColor("#eef3f1")


@dataclass(frozen=True)
class Volume:
    number: int
    title: str
    short_title: str
    subtitle: str
    description: str
    sources: tuple[str, ...]
    glossary: tuple[str, ...]
    cover_image: str
    filename: str


VOLUMES = (
    Volume(
        1,
        "看懂 App、模型与训练",
        "第一册｜App、模型与训练",
        "先看见手机界面背后的系统",
        "区分 App、模型、API、账号与会员；看懂终端、本地与云端入口、数据污染，以及多个“专家按钮”、信息差收费和虚假微调怎样形成。",
        (
            "manuscript/00-preface.md",
            "manuscript/01-model-is-not-the-app.md",
            "manuscript/02-how-models-learn.md",
            "manuscript/02a-ai-information-gap-scams.md",
        ),
        (
            "人工智能（Artificial Intelligence, AI）",
            "算法（algorithm）",
            "模型（model）",
            "机器学习（machine learning）",
            "生成式人工智能（generative AI）",
            "训练（training）",
            "推理或运行（inference）",
            "参数（parameter）",
            "数据集（dataset）",
            "数据污染（data contamination / data pollution）",
            "数据投毒（data poisoning）",
            "模型坍塌（model collapse）",
            "Token（文字片段）",
            "幻觉（hallucination）",
            "应用程序（application, App）",
            "用户界面（User Interface, UI）",
            "图形用户界面（Graphical User Interface, GUI）",
            "终端（terminal）与命令行界面（Command-Line Interface, CLI）",
            "应用程序接口（Application Programming Interface, API）",
            "服务器（server）",
            "模型路由（model routing）",
            "提示词（prompt）",
            "系统提示词（system prompt）",
            "检索增强生成（Retrieval-Augmented Generation, RAG）",
            "微调（fine-tuning）",
        ),
        "assets/illustrations/learning-five-ai-tools-web.jpg",
        "第一册-看懂App模型与训练-超大字版.pdf",
    ),
    Volume(
        2,
        "认识模型家族与定制方法",
        "第二册｜模型家族与定制",
        "从 LLM、SLM 到 RAG、微调与智能体",
        "理解不同模型和产品外层能力的分工；知道为什么没有永远的总冠军，并能为自己的真实任务设计比较测试。",
        (
            "manuscript/03-ai-model-family.md",
            "manuscript/04-rag-finetuning-tools-agents.md",
            "manuscript/05-why-models-differ.md",
        ),
        (
            "大型语言模型（Large Language Model, LLM）",
            "小型语言模型（Small Language Model, SLM）",
            "上下文（context）",
            "上下文窗口（context window）",
            "知识截止时间（knowledge cutoff）",
            "多模态模型（multimodal model）",
            "光学字符识别（Optical Character Recognition, OCR）",
            "语音识别（speech recognition）",
            "语音合成（Text-to-Speech, TTS）",
            "嵌入（embedding）与嵌入模型（embedding model）",
            "知识库（knowledge base）",
            "检索增强生成（Retrieval-Augmented Generation, RAG）",
            "微调（fine-tuning）",
            "记忆（memory）",
            "工具调用（tool use / function calling）",
            "智能体（agent）",
            "基准测试（benchmark）",
            "延迟（latency）",
            "速率限制（rate limit）与使用额度（quota）",
            "模型版本（model version）",
            "开放权重（open weights）与闭源服务（proprietary service）",
        ),
        "assets/illustrations/ai-model-family-workshop-web.jpg",
        "第二册-认识模型家族与定制方法-超大字版.pdf",
    ),
    Volume(
        3,
        "学会与 AI 对话和写作",
        "第三册｜提示词、对话与写作",
        "把自己的目标说清楚，也保留自己的声音",
        "用任务、背景、材料、输出和限制组成清楚提示词；建立语言练习伙伴，并让 AI 分阶段协助写作而不替代作者。",
        (
            "manuscript/06-prompt-engineering.md",
            "manuscript/07-chat-and-language-learning.md",
            "manuscript/08-writing-with-ai.md",
        ),
        (
            "提示词（prompt）",
            "系统提示词（system prompt）",
            "提示词工程（prompt engineering）",
            "上下文（context）",
            "上下文窗口（context window）",
            "幻觉（hallucination）",
            "记忆（memory）",
            "语音识别（speech recognition）",
            "语音合成（Text-to-Speech, TTS）",
            "事实、推断与意见（fact, inference, opinion）",
        ),
        "assets/illustrations/prompt-engineering-clear-brief-web.jpg",
        "第三册-学会与AI对话和写作-超大字版.pdf",
    ),
    Volume(
        4,
        "用 AI 作图、修照片与编程",
        "第四册｜作图、修照片与编程",
        "从创意生成到安全验收",
        "学会描述画面和局部修改；区分历史修复与模型想象；在明确文件、权限和测试标准的情况下让 AI 协助制作小工具。",
        (
            "manuscript/09-image-generation.md",
            "manuscript/10-photo-restoration.md",
            "manuscript/11-coding-with-ai.md",
        ),
        (
            "多模态模型（multimodal model）",
            "光学字符识别（Optical Character Recognition, OCR）",
            "图片生成（image generation）",
            "局部重绘（inpainting）",
            "放大与增强（upscaling / enhancement）",
            "程序代码（code）",
            "依赖（dependency）",
            "运行环境（runtime environment）",
            "错误信息（error message）",
            "测试（test）",
            "API 密钥（API key）",
            "云端（cloud）与本地运行（on-device / local）",
            "个人信息（personal information）",
            "敏感个人信息（sensitive personal information）",
        ),
        "assets/illustrations/learning-five-ai-tools-web.jpg",
        "第四册-用AI作图修照片与编程-超大字版.pdf",
    ),
    Volume(
        5,
        "选择 AI 产品与付费方式",
        "第五册｜产品、版本与付费",
        "从官方入口到真实成本",
        "在中国大陆找到官方产品；区分 App、模型、版本和 API；看懂免费层、会员、Token 价格与第三方服务的真实附加价值。",
        (
            "manuscript/12-mainland-ai-map.md",
            "manuscript/13-model-version-updates.md",
            "manuscript/14-ai-cost-and-payment.md",
        ),
        (
            "应用程序（application, App）",
            "应用程序接口（Application Programming Interface, API）",
            "Token（文字片段）",
            "模型路由（model routing）",
            "模型版本（model version）",
            "固定快照（snapshot）与移动别名（alias）",
            "订阅（subscription）与自动续费（automatic renewal）",
            "速率限制（rate limit）与使用额度（quota）",
            "开放权重（open weights）与闭源服务（proprietary service）",
        ),
        "assets/illustrations/learning-five-ai-tools-web.jpg",
        "第五册-选择AI产品与付费方式-超大字版.pdf",
    ),
    Volume(
        6,
        "辨别信息与保护隐私",
        "第六册｜信息、隐私与个人制度",
        "建立个人 AI 制度，保留证据、账号、资料与停止权",
        "理解 AI 错误和推荐回路；使用六步核验法处理高风险信息；控制输入资料、共享账号和订阅，并建立自己的 AI 工作台。",
        (
            "manuscript/15-why-ai-is-wrong.md",
            "manuscript/16-recommendation-echo.md",
            "manuscript/17-six-step-verification.md",
            "manuscript/18-high-stakes-ai.md",
            "manuscript/19-privacy-data-exit.md",
            "manuscript/20-personal-ai-workbench.md",
        ),
        (
            "数据污染（data contamination / data pollution）",
            "幻觉（hallucination）",
            "个性化推荐（personalized recommendation）",
            "回声室（echo chamber）",
            "来源追溯（source tracing）",
            "横向阅读（lateral reading）",
            "事实、推断与意见（fact, inference, opinion）",
            "个人信息（personal information）",
            "敏感个人信息（sensitive personal information）",
            "数据最小化（data minimization）",
            "多因素认证（Multi-Factor Authentication, MFA）",
            "个人 AI 工作台（personal AI workbench）",
        ),
        "assets/illustrations/ai-model-family-workshop-web.jpg",
        "第六册-辨别信息保护隐私与个人制度-超大字版.pdf",
    ),
)


def register_fonts() -> None:
    pdfmetrics.registerFont(
        TTFont("HeitiLight", "/System/Library/Fonts/STHeiti Light.ttc", subfontIndex=0)
    )
    pdfmetrics.registerFont(
        TTFont("HeitiMedium", "/System/Library/Fonts/STHeiti Medium.ttc", subfontIndex=0)
    )
    pdfmetrics.registerFontFamily(
        "HeitiLight",
        normal="HeitiLight",
        bold="HeitiMedium",
        italic="HeitiLight",
        boldItalic="HeitiMedium",
    )


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    size = lambda value: value * FONT_SCALE
    return {
        "Body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="HeitiLight",
            fontSize=size(14.2),
            leading=size(23.5),
            textColor=INK,
            spaceAfter=11,
            wordWrap="CJK",
            allowWidows=0,
            allowOrphans=0,
        ),
        "ChapterTitle": ParagraphStyle(
            "ChapterTitle",
            fontName="HeitiMedium",
            fontSize=size(25),
            leading=size(33),
            textColor=INK,
            spaceBefore=8,
            spaceAfter=22,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "SectionHeading": ParagraphStyle(
            "SectionHeading",
            fontName="HeitiMedium",
            fontSize=size(19),
            leading=size(27),
            textColor=INK,
            spaceBefore=23,
            spaceAfter=11,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "Subheading": ParagraphStyle(
            "Subheading",
            fontName="HeitiMedium",
            fontSize=size(16),
            leading=size(23),
            textColor=ACCENT_DARK,
            spaceBefore=17,
            spaceAfter=8,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "MinorHeading": ParagraphStyle(
            "MinorHeading",
            fontName="HeitiMedium",
            fontSize=size(14.5),
            leading=size(21),
            textColor=ACCENT_DARK,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True,
            wordWrap="CJK",
        ),
        "Quote": ParagraphStyle(
            "Quote",
            fontName="HeitiLight",
            fontSize=size(14),
            leading=size(23),
            leftIndent=16,
            rightIndent=8,
            borderWidth=0,
            borderColor=ACCENT,
            borderPadding=10,
            backColor=ACCENT_SOFT,
            textColor=INK,
            spaceBefore=7,
            spaceAfter=13,
            wordWrap="CJK",
        ),
        "Analogy": ParagraphStyle(
            "Analogy",
            fontName="HeitiLight",
            fontSize=size(13.5),
            leading=size(22),
            leftIndent=10,
            rightIndent=6,
            borderWidth=1.5,
            borderColor=ACCENT,
            borderPadding=9,
            backColor=ACCENT_SOFT,
            textColor=INK,
            spaceBefore=5,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "Boundary": ParagraphStyle(
            "Boundary",
            fontName="HeitiLight",
            fontSize=size(13.2),
            leading=size(21),
            leftIndent=10,
            rightIndent=6,
            borderWidth=1.2,
            borderColor=GOLD,
            borderPadding=9,
            backColor=WARNING,
            textColor=INK,
            spaceBefore=2,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "UserMeaning": ParagraphStyle(
            "UserMeaning",
            fontName="HeitiLight",
            fontSize=size(13.5),
            leading=size(22),
            leftIndent=10,
            rightIndent=6,
            borderWidth=1.8,
            borderColor=ACCENT_DARK,
            borderPadding=9,
            backColor=WHITE,
            textColor=INK,
            spaceBefore=2,
            spaceAfter=11,
            wordWrap="CJK",
        ),
        "CrossReference": ParagraphStyle(
            "CrossReference",
            fontName="HeitiLight",
            fontSize=size(12.8),
            leading=size(20.5),
            leftIndent=9,
            rightIndent=6,
            borderWidth=1,
            borderColor=LINE,
            borderPadding=9,
            backColor=REFERENCE_BG,
            textColor=MUTED,
            spaceBefore=4,
            spaceAfter=15,
            wordWrap="CJK",
        ),
        "Code": ParagraphStyle(
            "Code",
            fontName="HeitiLight",
            fontSize=size(10.4),
            leading=size(16),
            leftIndent=8,
            rightIndent=8,
            borderPadding=10,
            backColor=CODE_BG,
            textColor=colors.white,
            spaceBefore=7,
            spaceAfter=13,
            wordWrap="CJK",
            allowWidows=0,
            allowOrphans=0,
        ),
        "Caption": ParagraphStyle(
            "Caption",
            fontName="HeitiLight",
            fontSize=size(10.5),
            leading=size(16),
            textColor=MUTED,
            spaceBefore=5,
            spaceAfter=15,
            wordWrap="CJK",
        ),
        "CoverSeries": ParagraphStyle(
            "CoverSeries",
            fontName="HeitiMedium",
            fontSize=size(11),
            leading=size(16),
            textColor=ACCENT_DARK,
            spaceAfter=14,
        ),
        "CoverTitle": ParagraphStyle(
            "CoverTitle",
            fontName="HeitiMedium",
            fontSize=size(32),
            leading=size(42),
            textColor=INK,
            spaceAfter=15,
            wordWrap="CJK",
        ),
        "CoverSubtitle": ParagraphStyle(
            "CoverSubtitle",
            fontName="HeitiLight",
            fontSize=size(17),
            leading=size(26),
            textColor=INK,
            spaceAfter=16,
            wordWrap="CJK",
        ),
        "CoverDescription": ParagraphStyle(
            "CoverDescription",
            fontName="HeitiLight",
            fontSize=size(12.5),
            leading=size(20),
            textColor=MUTED,
            wordWrap="CJK",
        ),
        "TocTitle": ParagraphStyle(
            "TocTitle",
            fontName="HeitiMedium",
            fontSize=size(28),
            leading=size(36),
            textColor=INK,
            spaceAfter=18,
        ),
        "Toc0": ParagraphStyle(
            "Toc0",
            fontName="HeitiMedium",
            fontSize=size(13.5),
            leading=size(21),
            leftIndent=0,
            rightIndent=42,
            firstLineIndent=0,
            textColor=INK,
            spaceBefore=6,
        ),
        "Toc1": ParagraphStyle(
            "Toc1",
            fontName="HeitiLight",
            fontSize=size(11.5),
            leading=size(18),
            leftIndent=14,
            rightIndent=42,
            firstLineIndent=0,
            textColor=MUTED,
            spaceBefore=2,
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader",
            fontName="HeitiMedium",
            fontSize=size(10.5),
            leading=size(15),
            textColor=INK,
            wordWrap="CJK",
        ),
        "TableBody": ParagraphStyle(
            "TableBody",
            fontName="HeitiLight",
            fontSize=size(10.5),
            leading=size(15.5),
            textColor=INK,
            wordWrap="CJK",
        ),
        "CardLabel": ParagraphStyle(
            "CardLabel",
            fontName="HeitiMedium",
            fontSize=size(10.3),
            leading=size(15),
            textColor=ACCENT_DARK,
            wordWrap="CJK",
        ),
    }


STYLES: dict[str, ParagraphStyle]


class BookmarkFlowable(Flowable):
    def __init__(self, key: str):
        super().__init__()
        self.key = key
        self.width = 0
        self.height = 0

    def draw(self) -> None:
        self.canv.bookmarkPage(self.key)


class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, volume: Volume):
        super().__init__(
            filename,
            pagesize=PAGE_SIZE,
            leftMargin=LEFT,
            rightMargin=RIGHT,
            topMargin=TOP,
            bottomMargin=BOTTOM,
            title=f"《看懂 AI》第{volume.number}册：{volume.title}",
            author="《看懂 AI》书稿项目",
            subject=volume.subtitle,
        )
        self.volume = volume
        self.toc_key = f"volume-{volume.number}-toc"
        self.heading_counter = 0
        frame = Frame(LEFT, BOTTOM, CONTENT_WIDTH, PAGE_HEIGHT - TOP - BOTTOM, id="main")
        self.addPageTemplates(PageTemplate(id="book", frames=[frame], onPage=self.draw_page))

    def draw_page(self, canvas, doc) -> None:
        canvas.saveState()
        canvas.setFillColor(WARM)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
        if doc.page > 1:
            canvas.setStrokeColor(LINE)
            canvas.line(LEFT, PAGE_HEIGHT - 29, PAGE_WIDTH - RIGHT, PAGE_HEIGHT - 29)
            footer_size = 8.5 * FONT_SCALE
            canvas.setFont("HeitiLight", footer_size)
            canvas.setFillColor(MUTED)
            canvas.drawString(LEFT, PAGE_HEIGHT - 21, self.volume.short_title)
            canvas.drawCentredString(PAGE_WIDTH / 2, 22, str(doc.page))
            label = "返回目录"
            width = pdfmetrics.stringWidth(label, "HeitiLight", footer_size)
            x = PAGE_WIDTH - RIGHT - width
            canvas.setFillColor(ACCENT_DARK)
            canvas.drawString(x, 22, label)
            canvas.linkRect(
                "",
                self.toc_key,
                Rect=(x - 3, 17, PAGE_WIDTH - RIGHT + 3, 34),
                relative=0,
                thickness=0,
            )
        canvas.restoreState()

    def afterFlowable(self, flowable) -> None:
        if not isinstance(flowable, Paragraph):
            return
        if flowable.style.name not in {"ChapterTitle", "SectionHeading"}:
            return
        level = 0 if flowable.style.name == "ChapterTitle" else 1
        text = flowable.getPlainText()
        key = getattr(flowable, "_bookmarkName", None)
        if not key:
            return
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level=level, closed=(level == 1))
        # Keep the printed, clickable contents deliberately short on a phone:
        # only chapters appear there.  Section-level destinations remain
        # available in the PDF reader's bookmark/outline sidebar.
        if level == 0:
            toc_text = "专题 看穿 AI 信息差销售" if text.startswith("专题") else text
            self.notify("TOCEntry", (level, toc_text, self.page, key))


def inline_markup(text: str) -> str:
    placeholders: list[str] = []

    def hold(value: str) -> str:
        placeholders.append(value)
        return f"\x00{len(placeholders) - 1}\x00"

    def link_repl(match: re.Match[str]) -> str:
        label = html.escape(match.group(1))
        href = html.escape(match.group(2), quote=True)
        return hold(f'<link href="{href}" color="#075e57"><u>{label}</u></link>')

    def code_repl(match: re.Match[str]) -> str:
        return hold(f'<font name="HeitiMedium" color="#075e57">{html.escape(match.group(1))}</font>')

    text = re.sub(r"`([^`]+)`", code_repl, text)
    text = re.sub(r"\[([^]]+)]\(([^)]+)\)", link_repl, text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = text.replace("  ", "<br/>")
    for index, value in enumerate(placeholders):
        text = text.replace(f"\x00{index}\x00", value)
    return text


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def heading_flowable(text: str, level: int, doc: BookDocTemplate) -> Paragraph:
    style = {1: STYLES["ChapterTitle"], 2: STYLES["SectionHeading"], 3: STYLES["Subheading"], 4: STYLES["MinorHeading"]}[level]
    para = Paragraph(inline_markup(text), style)
    if level <= 2:
        doc.heading_counter += 1
        chapter = re.match(r"第\s*(\d+)\s*章", text)
        if level == 1 and chapter:
            para._bookmarkName = f"chapter-{int(chapter.group(1))}"
        elif level == 1 and text.startswith("序言"):
            para._bookmarkName = "preface"
        elif level == 1 and text.startswith("专题"):
            para._bookmarkName = "topic-ai-information-gap"
        elif level == 1 and text == "本册词汇卡":
            para._bookmarkName = f"volume-{doc.volume.number}-glossary"
        else:
            para._bookmarkName = f"volume-{doc.volume.number}-heading-{doc.heading_counter}"
    return para


def image_flowable(path: Path, alt: str) -> list[Flowable]:
    if path.suffix.lower() == ".svg":
        drawing = svg2rlg(str(path))
        if drawing is None:
            return [Paragraph(f"[示意图无法载入：{inline_markup(alt)}]", STYLES["Caption"])]

        # svglib preserves the SVG strings but substitutes unavailable Chinese
        # fonts with Helvetica.  Helvetica has no CJK glyphs, so replace every
        # drawing label with the same embedded fonts used by the book body.
        stack = [drawing]
        while stack:
            node = stack.pop()
            if isinstance(node, DrawingString):
                source_font = str(getattr(node, "fontName", ""))
                node.fontName = "HeitiMedium" if ("700" in source_font or "Bold" in source_font) else "HeitiLight"
            stack.extend(getattr(node, "contents", None) or [])

        scale = min(CONTENT_WIDTH / drawing.width, 420 / drawing.height)
        drawing.scale(scale, scale)
        drawing.width *= scale
        drawing.height *= scale
        media: Flowable = drawing
    else:
        media = Image(str(path))
        media._restrictSize(CONTENT_WIDTH, 250)
    return [Spacer(1, 6), media, Paragraph(inline_markup(alt), STYLES["Caption"])]


def table_flowables(headers: list[str], rows: list[list[str]]) -> list[Flowable]:
    if FONT_SCALE >= 2:
        cards: list[Flowable] = [Spacer(1, 6)]
        for row in rows:
            padded = row + [""] * (len(headers) - len(row))
            for label, value in zip(headers, padded):
                cards.append(
                    Paragraph(
                        f'<font color="#075e57"><b>{inline_markup(label)}：</b></font>'
                        f'{inline_markup(value)}',
                        STYLES["Quote"],
                    )
                )
            cards.append(Spacer(1, 9))
        return cards

    if len(headers) <= 3:
        data = [[Paragraph(inline_markup(cell), STYLES["TableHeader"]) for cell in headers]]
        for row in rows:
            padded = row + [""] * (len(headers) - len(row))
            data.append([Paragraph(inline_markup(cell), STYLES["TableBody"]) for cell in padded[: len(headers)]])
        col_widths = [CONTENT_WIDTH / len(headers)] * len(headers)
        table = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), ACCENT_SOFT),
                    ("GRID", (0, 0), (-1, -1), 0.6, LINE),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return [Spacer(1, 6), table, Spacer(1, 12)]

    cards: list[Flowable] = [Spacer(1, 5)]
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        content = []
        for label, value in zip(headers, padded):
            content.append(
                Paragraph(
                    f'<font color="#075e57"><b>{inline_markup(label)}：</b></font>{inline_markup(value)}',
                    STYLES["TableBody"],
                )
            )
        card = Table([[content]], colWidths=[CONTENT_WIDTH - 12])
        card.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                    ("BOX", (0, 0), (-1, -1), 0.8, LINE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 9),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        cards.extend([card, Spacer(1, 7)])
    return cards


def render_markdown(text: str, base_dir: Path, doc: BookDocTemplate) -> list[Flowable]:
    lines = text.splitlines()
    output: list[Flowable] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue

        image_match = re.fullmatch(r"!\[([^]]*)]\(([^)]+)\)", stripped)
        if image_match:
            output.extend(image_flowable((base_dir / image_match.group(2)).resolve(), image_match.group(1)))
            index += 1
            continue

        if stripped.startswith("```"):
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            index += 1
            code_text = "\n".join(code_lines)
            if re.search(r"[\u3400-\u9fff]", code_text):
                code_rows = [
                    [Paragraph(html.escape(item) if item else "&#160;", STYLES["Code"])]
                    for item in code_lines
                ]
                code_panel = Table(code_rows, colWidths=[CONTENT_WIDTH], hAlign="LEFT", splitByRow=1)
                code_style = [
                    ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, 0), 9),
                    ("BOTTOMPADDING", (0, -1), (-1, -1), 9),
                ]
                code_panel.setStyle(TableStyle(code_style))
            else:
                code = Preformatted(code_text, STYLES["Code"], maxLineLength=22)
                code_panel = Table([[code]], colWidths=[CONTENT_WIDTH], hAlign="LEFT")
                code_panel.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                            ("LEFTPADDING", (0, 0), (-1, -1), 10),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                            ("TOPPADDING", (0, 0), (-1, -1), 9),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                        ]
                    )
                )
            output.extend([Spacer(1, 7), code_panel, Spacer(1, 13)])
            continue

        heading_match = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            output.append(heading_flowable(heading_match.group(2), level, doc))
            index += 1
            continue

        if stripped in {"---", "***", "___"}:
            output.append(HRFlowable(width="24%", thickness=1.5, color=GOLD, spaceBefore=14, spaceAfter=18))
            index += 1
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].strip())
                index += 1
            output.append(Paragraph("<br/>".join(inline_markup(x) for x in quote_lines), STYLES["Quote"]))
            continue

        if stripped.startswith("|") and index + 1 < len(lines) and is_table_separator(lines[index + 1]):
            headers = [cell.strip() for cell in stripped.strip("|").split("|")]
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append([cell.strip() for cell in lines[index].strip().strip("|").split("|")])
                index += 1
            output.extend(table_flowables(headers, rows))
            continue

        if re.match(r"^-\s+", stripped):
            items: list[ListItem] = []
            while index < len(lines):
                match = re.match(r"^-\s+(.+)$", lines[index].strip())
                if not match:
                    break
                items.append(ListItem(Paragraph(inline_markup(match.group(1)), STYLES["Body"]), leftIndent=14))
                index += 1
            output.append(ListFlowable(items, bulletType="bullet", leftIndent=18, bulletColor=ACCENT, spaceAfter=8))
            continue

        if re.match(r"^\d+[.)]\s+", stripped):
            items = []
            while index < len(lines):
                match = re.match(r"^\d+[.)]\s+(.+)$", lines[index].strip())
                if not match:
                    break
                items.append(ListItem(Paragraph(inline_markup(match.group(1)), STYLES["Body"]), leftIndent=16))
                index += 1
            output.append(ListFlowable(items, bulletType="1", leftIndent=21, bulletColor=ACCENT, spaceAfter=8))
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index].strip()
            if not candidate:
                break
            if (
                candidate.startswith(("#", ">", "```", "|", "- ", "!["))
                or candidate in {"---", "***", "___"}
                or re.match(r"^\d+[.)]\s+", candidate)
            ):
                break
            paragraph_lines.append(candidate)
            index += 1
        raw = " ".join(paragraph_lines)
        if raw.startswith("**【这是一个比方】"):
            style = STYLES["Analogy"]
        elif raw.startswith("**【比方的边界】"):
            style = STYLES["Boundary"]
        elif raw.startswith("**【作为用户，这对您意味着什么】"):
            style = STYLES["UserMeaning"]
        elif raw.startswith(("**【回看前文】", "**【前册回顾】")):
            style = STYLES["CrossReference"]
        else:
            style = STYLES["Body"]
        paragraph = Paragraph(inline_markup(raw), style)
        if style.name in {"Analogy", "Boundary", "UserMeaning", "CrossReference"}:
            output.append(KeepTogether([paragraph]))
        else:
            output.append(paragraph)
    return output


def glossary_map() -> dict[str, str]:
    text = (BOOK_ROOT / "manuscript/99-glossary.md").read_text(encoding="utf-8")
    entries: dict[str, str] = {}
    pattern = re.compile(r"^### (.+?)\n(.*?)(?=^### |^## |\Z)", re.MULTILINE | re.DOTALL)
    for match in pattern.finditer(text):
        entries[match.group(1).strip()] = f"### {match.group(1).strip()}\n\n{match.group(2).strip()}\n"
    return entries


def cover_story(volume: Volume) -> list[Flowable]:
    image = Image(str(BOOK_ROOT / volume.cover_image))
    image._restrictSize(CONTENT_WIDTH, 105)
    return [
        Spacer(1, 18),
        Paragraph(f"《看懂 AI》手机超大字版 · 第 {volume.number} 册 / 全六册", STYLES["CoverSeries"]),
        Paragraph(volume.title, STYLES["CoverTitle"]),
        Paragraph(volume.subtitle, STYLES["CoverSubtitle"]),
        image,
        Spacer(1, 10),
        Paragraph("超大字版 · 2026-08-12", STYLES["CoverSeries"]),
        PageBreak(),
    ]


def build_volume(volume: Volume, glossary: dict[str, str]) -> Path:
    output = OUTPUT_DIR / volume.filename
    doc = BookDocTemplate(str(output), volume)
    story: list[Flowable] = cover_story(volume)

    story.extend(
        [
            BookmarkFlowable(doc.toc_key),
            Paragraph("目录", STYLES["TocTitle"]),
        ]
    )
    toc = TableOfContents()
    toc.levelStyles = [STYLES["Toc0"], STYLES["Toc1"]]
    toc.dotsMinLevel = 0
    story.extend([toc, PageBreak()])

    story.append(Paragraph("本册学习目标", STYLES["SectionHeading"]))
    story.append(Paragraph(volume.description, STYLES["Body"]))
    story.append(
        Paragraph(
            "阅读技术词时，请依次看准确解释、明确标注的生活比方、比方边界，以及“作为用户，这对您意味着什么”。英文只用于帮助识别产品页面中的常见写法，旁边保留中文名称或说明。",
            STYLES["UserMeaning"],
        )
    )
    story.append(PageBreak())

    for source_index, relative in enumerate(volume.sources):
        if source_index:
            story.append(PageBreak())
        source = BOOK_ROOT / relative
        story.extend(render_markdown(source.read_text(encoding="utf-8"), source.parent, doc))

    story.append(PageBreak())
    story.append(heading_flowable("本册词汇卡", 1, doc))
    story.append(
        Paragraph(
            "这些词只选取本册实际使用的概念。每个词先给准确解释，再给明确标注的生活比方和比方边界。",
            STYLES["Body"],
        )
    )
    for term in volume.glossary:
        if term not in glossary:
            raise KeyError(f"Glossary term not found: {term}")
        story.extend(render_markdown(glossary[term], BOOK_ROOT / "manuscript", doc))

    references = BOOK_ROOT / "manuscript/references" / f"{volume.number:02d}-sources.md"
    if not references.exists():
        raise FileNotFoundError(f"Missing volume references: {references}")
    story.append(PageBreak())
    story.extend(render_markdown(references.read_text(encoding="utf-8"), references.parent, doc))

    doc.multiBuild(story)
    return output


def main() -> None:
    global STYLES
    register_fonts()
    STYLES = make_styles()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    glossary = glossary_map()
    requested = {int(value) for value in sys.argv[1:]} if len(sys.argv) > 1 else set()
    unknown = requested - {volume.number for volume in VOLUMES}
    if unknown:
        raise ValueError(f"Unknown volume numbers: {sorted(unknown)}")
    for volume in VOLUMES:
        if requested and volume.number not in requested:
            continue
        path = build_volume(volume, glossary)
        print(path)


if __name__ == "__main__":
    main()
