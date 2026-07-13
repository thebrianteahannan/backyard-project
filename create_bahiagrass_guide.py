#!/usr/bin/env python3
"""Generate a Bahiagrass overseeding guide PDF for Tampa, Florida."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    ListFlowable,
    ListItem,
    KeepTogether,
    HRFlowable,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Colors — warm Florida lawn aesthetic (not purple/cream AI defaults)
FOREST = HexColor("#1B4D3E")
LEAF = HexColor("#2D6A4F")
SAND = HexColor("#F7F3EB")
SOIL = HexColor("#3D2914")
ACCENT = HexColor("#C4783A")
MUTED = HexColor("#5C6B63")
LIGHT_ROW = HexColor("#EEF5F0")
BORDER = HexColor("#C5D4CB")


def make_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=32,
            textColor=FOREST,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHead",
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=FOREST,
            spaceBefore=16,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=SOIL,
            spaceAfter=8,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Callout",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=FOREST,
            spaceAfter=8,
            leftIndent=8,
            rightIndent=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCell",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=SOIL,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHeader",
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=white,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletText",
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=SOIL,
        )
    )
    styles.add(
        ParagraphStyle(
            name="FooterNote",
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=11,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CheckItem",
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=SOIL,
        )
    )
    return styles


def section_rule():
    return HRFlowable(
        width="100%",
        thickness=1,
        color=BORDER,
        spaceBefore=2,
        spaceAfter=8,
    )


def bullets(items, styles):
    flow = []
    for item in items:
        flow.append(
            ListItem(
                Paragraph(item, styles["BulletText"]),
                leftIndent=12,
                bulletColor=LEAF,
                value="•",
            )
        )
    return ListFlowable(
        flow,
        bulletType="bullet",
        start="•",
        leftIndent=18,
        spaceBefore=2,
        spaceAfter=8,
    )


def checklist(items, styles):
    rows = []
    for item in items:
        rows.append(
            [
                Paragraph("☐", styles["CheckItem"]),
                Paragraph(item, styles["CheckItem"]),
            ]
        )
    t = Table(rows, colWidths=[0.35 * inch, 6.4 * inch])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def info_table(headers, data, styles, col_widths):
    header_row = [Paragraph(h, styles["TableHeader"]) for h in headers]
    body = []
    for row in data:
        body.append([Paragraph(cell, styles["TableCell"]) for cell in row])
    table = Table([header_row] + body, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), FOREST),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(body) + 1):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_ROW))
        else:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), white))
    table.setStyle(TableStyle(style_cmds))
    return table


def build_pdf(path):
    styles = make_styles()
    doc = SimpleDocTemplate(
        path,
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Tampa Bahiagrass Overseeding Guide",
        author="Backyard Lawn Guide",
    )

    story = []

    # Cover
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Tampa Backyard Lawn Guide", styles["CoverTitle"]))
    story.append(
        Paragraph(
            "Fill-in Seeding Plan for Bahiagrass (Paspalum notatum)",
            styles["CoverSub"],
        )
    )
    story.append(
        Paragraph("Tampa, Florida · Warm-season lawn · DIY overseed checklist", styles["CoverSub"])
    )
    story.append(section_rule())

    # Identification
    story.append(Paragraph("1. What grass is this?", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Based on your photo, this lawn is <b>Bahiagrass</b> "
            "(<i>Paspalum notatum</i>) — the most common utility lawn grass "
            "across Tampa and Central Florida.",
            styles["Body"],
        )
    )
    story.append(
        Paragraph("<b>Why it looks like Bahia:</b>", styles["Body"])
    )
    story.append(
        bullets(
            [
                "<b>Y-shaped (or V-shaped) seed heads</b> on taller stalks — "
                "the classic Bahia “wishbone” seed head.",
                "Wide, coarse, medium-green blades with a visible midrib.",
                "Patchy, open growth with brown thatch showing through — "
                "typical of Bahia as it thins in compacted or under-fertilized spots.",
                "Very common on Tampa residential lawns, especially sandy soils.",
            ],
            styles,
        )
    )
    story.append(
        Paragraph(
            "Your photo also shows some broadleaf weeds (likely clover and "
            "similar groundcovers) and thinner grassy patches. Filling bare "
            "spots with more Bahia seed — not a different grass type — is the "
            "right move so the lawn stays uniform.",
            styles["Body"],
        )
    )

    # Why Bahia
    story.append(Paragraph("2. Why stick with Bahiagrass in Tampa?", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        bullets(
            [
                "Thrives in Florida heat, humidity, and sandy soils.",
                "Deep roots — more drought-tolerant once established than St. Augustine.",
                "Cheapest warm-season grass to start from seed (St. Augustine is usually sod-only).",
                "Handles low-maintenance yards well; imperfect mowing still looks okay.",
            ],
            styles,
        )
    )
    story.append(
        Paragraph(
            "<b>Best window in Tampa:</b> March–June (primary) or "
            "late summer into early fall if you can keep seed watered. "
            "Avoid seeding when nighttime temps stay below about 65°F or "
            "during peak dry spells without irrigation.",
            styles["Body"],
        )
    )

    # Shopping list
    story.append(Paragraph("3. Shopping list — everything you need", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Use this as a checkout checklist. Quantities assume filling thin "
            "patches (overseeding), not starting a brand-new lawn from bare dirt. "
            "Scale up if you have large bare areas.",
            styles["Body"],
        )
    )

    story.append(Paragraph("<b>Seed & soil amendments</b>", styles["Body"]))
    story.append(
        checklist(
            [
                "<b>Bahiagrass seed</b> — look for Pensacola or Argentine (Argentine is denser/darker; Pensacola is the standard tough Florida type).",
                "<b>Seeding rate:</b> ~5–10 lb per 1,000 sq ft for overseeding thin areas; use the higher end for bare spots.",
                "<b>Starter fertilizer</b> — labeled for new grass / high phosphorus or “starter” (follow bag rates; Florida often has phosphorus limits — buy a Florida-friendly starter).",
                "<b>Soil test kit</b> (optional but recommended) — UF/IFAS Extension or a home kit; Bahia prefers soil pH around 5.5–6.5.",
                "<b>Lime or sulfur</b> — only if your soil test says you need it.",
                "<b>Compost or topsoil</b> — thin layer for bare patches to help seed contact moist soil.",
            ],
            styles,
        )
    )
    story.append(Spacer(1, 0.08 * inch))

    story.append(Paragraph("<b>Tools & application supplies</b>", styles["Body"]))
    story.append(
        checklist(
            [
                "<b>Lawn rake</b> (leaf or garden rake) — to thin thatch and scratch the soil surface.",
                "<b>Hand trowel or cultivator</b> — for scraping bare spots open.",
                "<b>Broadcast/hand seed spreader</b> — even seed distribution on larger areas.",
                "<b>Lawn roller</b> (optional) or walk-over-seed — to press seed into soil contact.",
                "<b>Hose + oscillating sprinkler or drip/soaker</b> — light, frequent watering is critical.",
                "<b>Straw mulch or seed-starting mulch</b> (optional) — light cover on bare spots to hold moisture; do not bury seed deep.",
                "<b>Mower</b> ready to cut at ~3–4 inches once grass is established.",
            ],
            styles,
        )
    )
    story.append(Spacer(1, 0.08 * inch))

    story.append(Paragraph("<b>Weed & pest items (use carefully)</b>", styles["Body"]))
    story.append(
        checklist(
            [
                "<b>Pre-emergent herbicide:</b> Do NOT apply before or right after seeding — it blocks seed from sprouting. Wait until new grass is established and mowed several times.",
                "<b>Post-emergent broadleaf weed killer</b> — wait until new seedlings are well established (usually several weeks); read the label for Bahia safety.",
                "<b>Mole cricket / grub monitoring</b> — common Tampa pests that thin lawns; treat only if you confirm activity (local garden center or Extension can help ID).",
            ],
            styles,
        )
    )

    # Step by step
    story.append(Paragraph("4. Step-by-step: put down more seed", styles["SectionHead"]))
    story.append(section_rule())

    steps = [
        (
            "Mow & clear",
            "Mow existing grass a little lower than usual (around 2–2.5 inches), bag clippings in thin areas, and rake out leaves, sticks, and thick thatch so seed can reach soil.",
        ),
        (
            "Scratch the soil",
            "In thin and bare spots, rake hard enough to loosen the top ¼ inch of soil. Seed must touch mineral soil — not sit on top of thatch.",
        ),
        (
            "Improve bare patches",
            "On bare dirt, scatter a thin dusting of compost or screened topsoil (⅛–¼ inch). Do not bury seed under a thick blanket of soil.",
        ),
        (
            "Spread Bahiagrass seed",
            "Broadcast seed evenly. Aim for about 5–10 lb per 1,000 sq ft over thin turf; heavier over completely bare soil. Mix seed in the spreader with a little sand or starter fertilizer if the bag is small and hard to distribute evenly.",
        ),
        (
            "Press seed in",
            "Rake lightly so seed settles into the scratched surface, then walk over the area or use a roller. Good seed-to-soil contact is the #1 success factor.",
        ),
        (
            "Optional light mulch",
            "On open bare spots only, add a very light straw veil so you can still see some soil/seed. Too much mulch smothers Bahia seed.",
        ),
        (
            "Water gently",
            "Water immediately after seeding. Keep the seedbed moist (not flooded) until seedlings are established — see watering schedule below.",
        ),
        (
            "Fertilize at the right time",
            "Apply a starter fertilizer at seeding or when seedlings emerge (follow the bag). After that, switch to a Bahia-friendly, slow-release nitrogen program.",
        ),
        (
            "First mows",
            "Wait until new grass is about 3–4 inches tall before the first cut. Never remove more than ⅓ of the blade. Then maintain Bahia at about 3–4 inches.",
        ),
    ]
    for i, (title, detail) in enumerate(steps, 1):
        story.append(
            KeepTogether(
                [
                    Paragraph(f"<b>Step {i}: {title}</b>", styles["Body"]),
                    Paragraph(detail, styles["Body"]),
                ]
            )
        )

    # Watering
    story.append(Paragraph("5. Watering schedule (Tampa heat)", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        info_table(
            ["Phase", "How often", "Goal"],
            [
                [
                    "Days 1–14 (germination)",
                    "Light water 2–3× per day",
                    "Keep top ½ inch moist. Do not wash seed away.",
                ],
                [
                    "Weeks 3–4",
                    "Once daily, deeper",
                    "Encourage roots to grow down.",
                ],
                [
                    "Weeks 5–6+",
                    "2–3× per week",
                    "About ½–¾ inch total water per session including rainfall.",
                ],
                [
                    "Established Bahia",
                    "As needed / rainfall",
                    "Deep, infrequent watering. Bahia is drought-tough once rooted.",
                ],
            ],
            styles,
            [1.85 * inch, 1.7 * inch, 3.2 * inch],
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "Bahiagrass usually germinates in about <b>14–28 days</b> in warm Tampa soil. "
            "Do not panic if it looks slow the first week — keep moisture consistent.",
            styles["Body"],
        )
    )

    # Fertility
    story.append(Paragraph("6. Feeding for a thicker, more fruitful lawn", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Bahiagrass is a lighter feeder than St. Augustine, but thin lawns still "
            "respond to a simple seasonal plan:",
            styles["Body"],
        )
    )
    story.append(
        info_table(
            ["When (Tampa)", "What", "Notes"],
            [
                [
                    "At seeding / emergence",
                    "Starter fertilizer",
                    "Helps root establishment. Follow bag rate.",
                ],
                [
                    "Late spring",
                    "Slow-release nitrogen",
                    "Example target: ~1 lb N per 1,000 sq ft per application.",
                ],
                [
                    "Summer (optional)",
                    "Light follow-up feeding",
                    "Do not over-fertilize — excess feeds weeds too.",
                ],
                [
                    "Early fall",
                    "Final light N if needed",
                    "Stop heavy feeding before cooler weather.",
                ],
            ],
            styles,
            [1.6 * inch, 1.7 * inch, 3.45 * inch],
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        Paragraph(
            "Iron supplements can green Bahia without a big flush of growth. "
            "Always follow Florida fertilizer ordinances (Tampa / Hillsborough often "
            "restrict nitrogen and phosphorus in summer rainy season — check current "
            "local rules before applying).",
            styles["Body"],
        )
    )

    # Troubleshooting
    story.append(Paragraph("7. Tips to make thin Bahia denser", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        bullets(
            [
                "<b>Match the grass you already have.</b> Mixing Bermuda or rye will make a blotchy lawn.",
                "<b>Sun exposure:</b> Bahia needs full to mostly-full sun. Dense shade patches will stay thin — plant groundcover or a shade grass strategy there instead.",
                "<b>Compacted soil:</b> If water puddles or the soil is hard, core-aerate before seeding next season.",
                "<b>Weeds:</b> Pull or spot-treat broadleafs after new grass is established so they do not steal space from seedlings.",
                "<b>Mow higher:</b> Keeping Bahia at 3–4 inches shades soil, slows weeds, and builds a fuller look.",
                "<b>Patience:</b> Over-seed thin areas for 1–2 seasons if needed. Bahia fills sideways slowly compared to Bermuda.",
            ],
            styles,
        )
    )

    # Quick reference
    story.append(Paragraph("8. Quick reference card", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        info_table(
            ["Item", "Recommendation"],
            [
                ["Grass type", "Bahiagrass (Pensacola or Argentine)"],
                ["Location", "Tampa, Florida (USDA Zone ~9b / 10a)"],
                ["Best seed timing", "March–June (warm soil, reliable germination)"],
                ["Overseed rate", "5–10 lb seed / 1,000 sq ft (higher for bare spots)"],
                ["Mowing height", "3–4 inches once established"],
                ["Water after seeding", "Keep surface moist until seedlings take hold"],
                ["Expect sprouts", "About 2–4 weeks in warm weather"],
                ["Avoid", "Pre-emergent herbicide before/right after seeding"],
            ],
            styles,
            [2.0 * inch, 4.75 * inch],
        )
    )

    story.append(Spacer(1, 0.25 * inch))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Local help: University of Florida IFAS Extension — Hillsborough County "
            "can help with soil tests and pest ID. This guide is for home DIY planning; "
            "always follow product labels and local fertilizer ordinances.",
            styles["FooterNote"],
        )
    )

    def add_page_bits(canvas, doc_):
        canvas.saveState()
        # Top accent bar
        canvas.setFillColor(FOREST)
        canvas.rect(0, letter[1] - 10, letter[0], 10, fill=1, stroke=0)
        # Bottom footer
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(
            0.7 * inch,
            0.35 * inch,
            "Tampa Bahiagrass Overseeding Guide",
        )
        canvas.drawRightString(
            letter[0] - 0.7 * inch,
            0.35 * inch,
            f"Page {doc_.page}",
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_bits, onLaterPages=add_page_bits)
    print(f"Wrote {path}")


if __name__ == "__main__":
    build_pdf("/workspace/Tampa_Bahiagrass_Overseeding_Guide.pdf")
