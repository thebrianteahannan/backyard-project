#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a fence heat-reflection solutions PDF for a Tampa garden bed."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    ListFlowable, ListItem, KeepTogether, HRFlowable, PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

SUN = HexColor("#C45C26")
LEAF = HexColor("#2F6B3A")
DEEP = HexColor("#1A3D28")
SOIL = HexColor("#3A2A1A")
MUTED = HexColor("#5E6A5F")
LIGHT_ROW = HexColor("#F3F7F1")
BORDER = HexColor("#D0D9CB")
SKY = HexColor("#E8F0E4")
WARN = HexColor("#FFF4E5")


def make_styles():
    s = getSampleStyleSheet()
    specs = [
        ("CoverTitle", "Helvetica-Bold", 22, 28, DEEP, TA_CENTER, 8, 0),
        ("CoverSub", "Helvetica", 11, 15, MUTED, TA_CENTER, 5, 0),
        ("SectionHead", "Helvetica-Bold", 13, 17, DEEP, TA_LEFT, 6, 14),
        ("Body", "Helvetica", 10, 14, SOIL, TA_LEFT, 7, 0),
        ("CalloutText", "Helvetica", 9.5, 13, DEEP, TA_LEFT, 0, 0),
        ("TableCell", "Helvetica", 9, 12, SOIL, TA_LEFT, 0, 0),
        ("TableHeader", "Helvetica-Bold", 9, 12, white, TA_LEFT, 0, 0),
        ("BulletText", "Helvetica", 10, 13, SOIL, TA_LEFT, 0, 0),
        ("FooterNote", "Helvetica-Oblique", 8, 11, MUTED, TA_CENTER, 0, 0),
        ("CheckItem", "Helvetica", 10, 13, SOIL, TA_LEFT, 0, 0),
    ]
    for name, font, size, lead, color, align, after, before in specs:
        s.add(ParagraphStyle(
            name=name, fontName=font, fontSize=size, leading=lead,
            textColor=color, alignment=align, spaceAfter=after, spaceBefore=before,
        ))
    return s


def section_rule():
    return HRFlowable(width="100%", thickness=1, color=BORDER, spaceBefore=1, spaceAfter=7)


def bullets(items, styles):
    flow = [
        ListItem(Paragraph(i, styles["BulletText"]), leftIndent=12, bulletColor=LEAF, value="-")
        for i in items
    ]
    return ListFlowable(
        flow, bulletType="bullet", start="-", leftIndent=18, spaceBefore=1, spaceAfter=7
    )


def checklist(items, styles):
    rows = [
        [Paragraph("[ ]", styles["CheckItem"]), Paragraph(i, styles["CheckItem"])]
        for i in items
    ]
    t = Table(rows, colWidths=[0.4 * inch, 6.35 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def info_table(headers, data, styles, col_widths):
    header_row = [Paragraph(h, styles["TableHeader"]) for h in headers]
    body = [[Paragraph(c, styles["TableCell"]) for c in row] for row in data]
    table = Table([header_row] + body, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), DEEP),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(body) + 1):
        cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_ROW if i % 2 == 0 else white))
    table.setStyle(TableStyle(cmds))
    return table


def callout_box(title, text, styles, bg=SKY, border=LEAF):
    inner = Paragraph("<b>%s</b><br/>%s" % (title, text), styles["CalloutText"])
    t = Table([[inner]], colWidths=[6.75 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 1, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def heading(story, styles, text):
    story.append(Paragraph(text, styles["SectionHead"]))
    story.append(section_rule())


def build_pdf(path):
    styles = make_styles()
    doc = SimpleDocTemplate(
        path, pagesize=letter,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.65 * inch, bottomMargin=0.65 * inch,
        title="Fence Heat Solutions for Tampa Gardens",
        author="Backyard Garden Guide",
    )
    story = []

    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph("Fence Heat Solutions", styles["CoverTitle"]))
    story.append(Paragraph(
        "What to Do When a White Vinyl Fence Cooks Your Garden Bed", styles["CoverSub"]))
    story.append(Paragraph(
        "Tampa, Florida - Full-sun backyard - Reflective fence strip", styles["CoverSub"]))
    story.append(section_rule())

    heading(story, styles, "1. What is going on (and why you never noticed)")
    story.append(Paragraph(
        "Your plants already get direct sun most of the day. A bright white vinyl fence "
        "adds a second dose: sunlight hitting the panels bounces back onto leaves, fruit, "
        "mulch, and soil. That bounce raises the temperature in the narrow strip against "
        "the fence - often a few degrees hotter than the same bed a few feet out in the lawn.",
        styles["Body"]))
    story.append(Paragraph(
        "You usually notice it as wilted leaves at midday that perk up at dusk, pale "
        "bleached patches on tomatoes (sunscald), crispy leaf edges on ornamentals near the "
        "fence, or soil that dries faster along the back row than the front edge.",
        styles["Body"]))
    story.append(callout_box(
        "Simple picture",
        "Think of the fence as a mirror for heat and light. You are not imagining it - white "
        "surfaces reflect a lot of solar energy. Darker fences absorb more heat into the "
        "material itself; white flings more of it back into your plants.",
        styles, bg=WARN, border=SUN))

    heading(story, styles, "2. Quick fixes you can do this weekend")
    story.append(Paragraph(
        "Start here. These are cheap, reversible, and usually enough for a small Tampa bed "
        "like yours.", styles["Body"]))
    story.append(bullets([
        "<b>Thicken the mulch.</b> Keep 2-3 inches of wood mulch over bare soil so the "
        "reflected heat does not bake the root zone as fast. Pull mulch 1-2 inches off stems.",
        "<b>Water deeper, not more often.</b> Morning deep soaks (or drip under mulch) beat "
        "noon sprinkles. Fence-side soil often needs the consistent deep option first.",
        "<b>Leave a leaf canopy on tomatoes.</b> Do not strip the fence-facing side bare. "
        "Leaves shade fruit from bounce light and reduce sunscald.",
        "<b>Move sensitive plants forward.</b> Keep heat lovers (okra, sunflowers, peppers) "
        "nearest the fence; shift softer foliage farther from the panels or into pots.",
        "<b>Shade cloth over fruit crops only.</b> A 30% knit shade cloth on simple PVC/"
        "conduit hoops above tomatoes for July-August cuts glare without making a shade garden.",
        "<b>Add a living buffer.</b> Tall heat-tough plants along the fence (okra, sunflowers, "
        "lemongrass, corn in season) intercept bounce before it hits shorter crops.",
    ], styles))

    heading(story, styles, "3. DIY soft barriers between fence and plants")
    story.append(Paragraph(
        "If weekend tweaks are not enough, add a gentle buffer so light and heat do not hit "
        "plants head-on from behind.", styles["Body"]))
    story.append(info_table(
        ["Solution", "How it helps", "DIY notes"],
        [
            ["30% shade cloth hoop",
             "Cuts peak bounce + direct sun on fruit",
             "PVC hoops stuck in soil; clip cloth on July-Sept; remove for fall"],
            ["Fence-line trellis / lattice",
             "Breaks the flat reflective wall",
             "Stand lattice a few inches off vinyl; train beans, Malabar spinach, or cucumber"],
            ["Narrow green-wall planter",
             "Living screen absorbs bounce",
             "Tall pots of lemongrass, okra, or sweet potato vines along fence"],
            ["Bamboo / reed screening",
             "Diffuses reflected light",
             "Hang or freestanding panel; leave air gap so vinyl fence still vents"],
            ["Landscape fabric + mulch strip",
             "Cools soil at fence base",
             "Works with drip underneath; do not pile mulch against vinyl panels"],
        ],
        styles, [1.85 * inch, 2.15 * inch, 2.75 * inch],
    ))
    story.append(Spacer(1, 0.08 * inch))
    story.append(callout_box(
        "Vinyl fence tip",
        "Do not screw heavy frames into vinyl if HOA or warranty matters - use freestanding "
        "hoops, pots, or a separate trellis frame set a few inches away so airflow stays behind plants.",
        styles))

    heading(story, styles, "4. Plant placement map for a fence-line bed")
    story.append(Paragraph(
        "You do not have to fight the fence - use it. Put the toughest, tallest crops where "
        "bounce is strongest, and give picky plants a little distance.", styles["Body"]))
    story.append(info_table(
        ["Zone", "Where", "Best plants"],
        [
            ["Hot back row",
             "Within about 12-18 in. of fence",
             "Okra, sunflowers, southern peas, sweet potato, lemongrass, heat herbs "
             "(rosemary, Mexican tarragon)"],
            ["Middle row",
             "Center of bed / cages",
             "Cherry tomatoes, peppers, eggplant - keep leaf cover on fence side"],
            ["Cooler front edge",
             "Toward lawn / walkway",
             "Marigolds, basil, purslane, thyme; any plant that looked scorched near the panels"],
            ["Containers",
             "Just outside the mulch",
             "Good for moving heat-sensitive ornamentals off the bounce strip entirely"],
        ],
        styles, [1.35 * inch, 1.8 * inch, 3.6 * inch],
    ))

    story.append(PageBreak())

    heading(story, styles, "5. Bigger options if you want a lasting fix")
    story.append(Paragraph(
        "These cost more or take more planning, but they permanently soften fence-line heat.",
        styles["Body"]))
    story.append(bullets([
        "<b>Widen the bed away from the fence.</b> Even 6-12 inches toward the lawn lets you "
        "keep a buffer row of tough plants and more root space in cooler soil.",
        "<b>Pull planting out of the hottest inch.</b> Leave a mulched gap (no stems) right "
        "against the vinyl so roots are not in the absolute hottest strip.",
        "<b>Partial privacy screen in front of the fence.</b> Freestanding lattice with vines "
        "absorbs bounce; leave a few inches of space so vinyl does not stay soaked against wood.",
        "<b>Trees/shrubs elsewhere - not right on this bed.</b> Big shade trees can help the "
        "yard later in the day, but do not crowd this bed with roots. Your sun holds until "
        "about 5 p.m.; afternoon shade elsewhere is a long-term yard project, not a fence patch.",
        "<b>Fence color change is usually not worth it.</b> Painting vinyl is tricky and often "
        "against warranty. Soft barriers and plant placement beat a new fence color for a home garden.",
    ], styles))

    heading(story, styles, "6. Water + mulch playbook for the bounce strip")
    story.append(info_table(
        ["Symptom near fence", "Likely cause", "Try this"],
        [
            ["Midday wilt, fine by evening", "Heat stress / temporary water lag",
             "Keep drip schedule; do not panic-water at noon every day"],
            ["Wilt still there at dusk", "Roots truly dry",
             "Deep morning soak; check mulch thickness; feel soil 3 in. down"],
            ["Tomato white/bleached patches", "Sunscald from bounce + direct sun",
             "More leaf cover, 30% shade cloth, harvest earlier"],
            ["Leaf edges crisp / plants brown", "Scorch on soft foliage",
             "Move plant forward or to pot; swap for heat-tough filler"],
            ["Mulch bone-dry against fence", "Extra evaporation from bounce",
             "Remulch; drip under mulch along the back row"],
        ],
        styles, [2.0 * inch, 2.0 * inch, 2.75 * inch],
    ))

    heading(story, styles, "7. What NOT to do")
    story.append(bullets([
        "<b>Do not overwater every hour.</b> Soggy soil + Florida humidity brings root rot "
        "and leaf disease.",
        "<b>Do not wrap the fence in thick plastic.</b> It can trap heat, look bad, and hurt airflow.",
        "<b>Do not pile mulch against vinyl panels forever.</b> Keep a clean strip so moisture "
        "does not sit on the fence.",
        "<b>Do not strip tomatoes naked</b> to see fruit better - exposed fruit on the fence "
        "side burns first.",
        "<b>Do not plant cool-season greens against the fence in July.</b> The bounce strip is "
        "the worst seat in the house for lettuce and cilantro.",
    ], styles))

    heading(story, styles, "8. Weekend action checklist")
    story.append(checklist([
        "Walk the bed at noon and again at dusk - note which plants wilt and which rebound.",
        "Top up mulch to 2-3 inches, especially along the fence; leave stem collars clear.",
        "Route a soaker/drip line under mulch for the back row.",
        "Reposition any scorched ornamentals to the front edge or into larger pots.",
        "Keep okra / sunflowers as the fence buffer; keep tomato cages a little forward if crowded.",
        "Decide whether July-August needs a 30% shade-cloth hoop over tomatoes only.",
        "Optional: set a freestanding trellis or tall pots as a soft screen a few inches off the vinyl.",
        "After the next hot week, check fruit for sunscald and adjust leaf cover or cloth.",
    ], styles))

    heading(story, styles, "9. Quick reference card")
    story.append(info_table(
        ["Item", "Recommendation"],
        [
            ["Problem", "White vinyl fence reflecting extra light/heat into the bed"],
            ["Location", "Tampa full-sun bed that only eases up around 5 p.m."],
            ["Fastest wins", "Mulch + drip + leaf canopy + plant order (tough plants at fence)"],
            ["Best soft barrier", "30% shade cloth on hoops (summer) or living screen (okra/vines)"],
            ["Keep against fence", "Okra, sunflowers, sweet potato, lemongrass, hardy herbs"],
            ["Move away from fence", "Soft ornamentals and anything already crisping"],
            ["Skip as a first fix", "Painting the vinyl or replacing the fence"],
            ["Goal", "Same sunny bed, less double-sun stress on fruit and roots"],
        ],
        styles, [1.7 * inch, 5.05 * inch],
    ))

    story.append(Spacer(1, 0.18 * inch))
    story.append(section_rule())
    story.append(Paragraph(
        "Companion to the Tampa Full-Sun Garden Tips guide. Practical DIY ideas for a "
        "fence-line bed - not a fence construction manual. If an HOA or vinyl warranty applies, "
        "prefer freestanding screens and pots over attaching hardware to the panels.",
        styles["FooterNote"]))

    def add_page_bits(canvas, doc_):
        canvas.saveState()
        canvas.setFillColor(SUN)
        canvas.rect(0, letter[1] - 10, letter[0], 10, fill=1, stroke=0)
        canvas.setFillColor(DEEP)
        canvas.rect(0, letter[1] - 14, letter[0], 4, fill=1, stroke=0)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(0.7 * inch, 0.35 * inch, "Fence Heat Solutions - Tampa Garden")
        canvas.drawRightString(letter[0] - 0.7 * inch, 0.35 * inch, "Page %s" % doc_.page)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_bits, onLaterPages=add_page_bits)
    print("Wrote %s" % path)


if __name__ == "__main__":
    build_pdf("/workspace/Tampa_Fence_Heat_Solutions.pdf")
