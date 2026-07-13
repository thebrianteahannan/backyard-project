#!/usr/bin/env python3
"""Generate a full-sun vegetable & flower garden tips PDF for Tampa, Florida."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
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
    PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Colors — sunny Tampa garden aesthetic (avoid purple/cream AI defaults)
SUN = HexColor("#C45C26")
LEAF = HexColor("#2F6B3A")
DEEP = HexColor("#1A3D28")
SOIL = HexColor("#3A2A1A")
SAND = HexColor("#FBF6EE")
MUTED = HexColor("#5E6A5F")
LIGHT_ROW = HexColor("#F3F7F1")
BORDER = HexColor("#D0D9CB")
SKY = HexColor("#E8F0E4")


def make_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            textColor=DEEP,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHead",
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=DEEP,
            spaceBefore=14,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=SOIL,
            spaceAfter=7,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CalloutText",
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=DEEP,
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
        spaceBefore=1,
        spaceAfter=7,
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
        spaceBefore=1,
        spaceAfter=7,
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
        ("BACKGROUND", (0, 0), (-1, 0), DEEP),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(body) + 1):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_ROW))
        else:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), white))
    table.setStyle(TableStyle(style_cmds))
    return table


def callout_box(title, text, styles):
    inner = Paragraph(f"<b>{title}</b><br/>{text}", styles["CalloutText"])
    t = Table([[inner]], colWidths=[6.75 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SKY),
                ("BOX", (0, 0), (-1, -1), 1, LEAF),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def build_pdf(path):
    styles = make_styles()
    doc = SimpleDocTemplate(
        path,
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Tampa Full-Sun Garden Tips & Tricks",
        author="Backyard Garden Guide",
    )

    story = []

    # Cover
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Tampa Full-Sun Garden Guide", styles["CoverTitle"]))
    story.append(
        Paragraph(
            "Tips & Tricks for a Hot, Bright Backyard Bed",
            styles["CoverSub"],
        )
    )
    story.append(
        Paragraph(
            "Tampa, Florida · USDA Zone 9b/10a · All-day sun until ~5 p.m.",
            styles["CoverSub"],
        )
    )
    story.append(section_rule())

    # Snapshot from photos
    story.append(Paragraph("1. What you already have going", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Your curved mulch bed against the white vinyl fence is a classic Tampa "
            "side-yard setup: long day-length sun, reflected heat, and sandy Florida soil. "
            "From your photos, the bed is already doing real work — and a few upgrades "
            "will make it more productive and less stressful in peak summer.",
            styles["Body"],
        )
    )
    story.append(
        bullets(
            [
                "<b>Sunflowers</b> — strong performer in full Florida sun; great for pollinators and cut flowers.",
                "<b>Cherry / salad tomatoes in cages</b> — fruiting already; cages are the right call for wind and sprawl.",
                "<b>Marigolds under tomatoes</b> — smart companion planting; they help with pest deterrence and fill bare mulch.",
                "<b>Okra (likely) on the sunny end</b> — one of the best heat crops for Tampa summers.",
                "<b>Dark wood mulch + curved edging</b> — moisture retention and a clean bed line.",
                "<b>White fence behind the bed</b> — beautiful, but it <b>bounces extra heat and light</b> onto leaves and fruit.",
            ],
            styles,
        )
    )
    story.append(
        callout_box(
            "Sun schedule note",
            "You said this spot stays sunny almost all day and only eases up around 5 p.m. "
            "Treat this bed as true full sun (8–10+ hours). Choose heat-loving plants, water "
            "deeply, and protect fruit from scald — do not try cool-season crops here in midsummer.",
            styles,
        )
    )

    # Heat & fence
    story.append(Paragraph("2. Beat the heat (and the white fence bounce)", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Tampa summers routinely push mid-90s with high humidity. A white vinyl fence "
            "acts like a reflector: plants in that strip often cook a bit harder than the "
            "same varieties planted out in open lawn. Use these tactics:",
            styles["Body"],
        )
    )
    story.append(
        bullets(
            [
                "<b>Water early.</b> Aim for dawn (or before 9 a.m.) so leaves dry and roots drink before peak heat.",
                "<b>Mulch thicker.</b> Keep 2–3 inches of wood mulch, pulled back 1–2 inches from stems so crowns do not rot.",
                "<b>Shade cloth for fruit crops (optional).</b> A 30% knit shade cloth on a simple PVC hoop over tomatoes during July–August cuts scald without stealing too much light.",
                "<b>Keep foliage between fruit and the fence.</b> Do not strip lower leaves too aggressively on the fence side — they buffer reflected heat.",
                "<b>Afternoon check.</b> If leaves look wilted at noon but rebound by evening, that is heat stress — not always a call for more water. If they stay wilted at dusk, water deeply the next morning.",
                "<b>Soil thermometer habit:</b> Warm, moist soil is good; dry/crusty top inch with wilted plants means roots are baking.",
            ],
            styles,
        )
    )

    # Watering
    story.append(Paragraph("3. Watering schedule for full-sun Tampa beds", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        info_table(
            ["Plant stage / weather", "How much", "How often"],
            [
                [
                    "New transplants (first 10–14 days)",
                    "Keep root zone evenly moist",
                    "Daily light soak; then taper",
                ],
                [
                    "Established veggies in summer",
                    "~1–1.5 inches total water / week",
                    "2–3 deep waterings (not daily sprinkle)",
                ],
                [
                    "Fruiting tomatoes / peppers",
                    "Deep soak to 6–8 inches",
                    "Consistent schedule — swings cause blossom end rot & splitting",
                ],
                [
                    "Sunflowers & okra",
                    "Deep weekly soak once established",
                    "More during multi-day dry spells",
                ],
                [
                    "Afternoon thunderstorm weeks",
                    "Skip or reduce irrigation",
                    "Feel the soil 3 inches down before watering",
                ],
            ],
            styles,
            [2.3 * inch, 2.2 * inch, 2.25 * inch],
        )
    )
    story.append(Spacer(1, 0.08 * inch))
    story.append(
        Paragraph(
            "<b>Pro tip:</b> A cheap soaker hose or drip line under the mulch is ideal for this "
            "narrow bed. You water roots, leave leaves dry (fewer fungal issues in Florida humidity), "
            "and waste less water on the grass strip out front.",
            styles["Body"],
        )
    )

    # Soil
    story.append(Paragraph("4. Soil upgrades that actually matter here", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Tampa yards are usually sandy and hungry. Dark mulch helps, but the plants still "
            "need richer planting pockets than native fill.",
            styles["Body"],
        )
    )
    story.append(
        bullets(
            [
                "<b>Enrich each planting hole:</b> mix native sand with compost and a Florida-friendly vegetable garden mix (about 50/50 in the hole for tomatoes/okra).",
                "<b>Top-dress midseason:</b> ½–1 inch of finished compost around plants (keep off stems), then remulch.",
                "<b>Soil test once a year:</b> UF/IFAS Hillsborough Extension kits are inexpensive; Florida often restricts phosphorus — do not blindly add “bloom booster.”",
                "<b>pH target:</b> most veggies prefer ~6.0–6.8. If soil is very sandy/acidic, compost helps more than quick chemical fixes.",
                "<b>Do not over-till every year.</b> Top-dress and plant into improved zones so structure and microbes build under the mulch.",
            ],
            styles,
        )
    )

    # Plant-by-plant
    story.append(Paragraph("5. Plant-by-plant tips for your bed", styles["SectionHead"]))
    story.append(section_rule())

    plant_tips = [
        (
            "Tomatoes (caged)",
            "Keep cages snug and stake the cage if wind hits that fence corridor. Water at soil level "
            "on a consistent schedule. Harvest cherry tomatoes as they blush to reduce bird/pecking damage. "
            "In peak Tampa heat, blossoms can drop — that is normal; plants usually rebound when nights ease. "
            "Strip only crowded inner suckers; leave enough leaf canopy to shade fruit from fence glare. "
            "Watch for leaf spot: remove yellow/spotted lower leaves and bag them — do not compost diseased leaves.",
        ),
        (
            "Marigolds",
            "You are already using them well under tomatoes. Deadhead spent blooms so they keep flowering. "
            "They are excellent border fillers; tuck more along the sunny front edge to shade bare mulch and "
            "discourage some nematodes/pests over time.",
        ),
        (
            "Sunflowers",
            "Water deeply at the base; tall stalks in sandy soil tip if the top inch is the only moist layer. "
            "Leave a few seed heads for birds, or cut for bouquets as petals just fully open. If a stalk "
            "leans toward the fence from glare, stake early. Avoid over-fertilizing nitrogen — you get "
            "giant leaves and weak necks.",
        ),
        (
            "Okra",
            "Harvest pods when 3–4 inches long (every 1–2 days in Florida heat) or they get woody fast. "
            "Okra loves this site. Side-dress lightly with nitrogen when plants are knee-high if growth stalls. "
            "Wear long sleeves when picking — many varieties are itchy.",
        ),
        (
            "Color foliage / ornamentals",
            "Deep red leafy accents are fine in sun if they are heat types (some coleus varieties struggle "
            "in roasting afternoon light). If a plant scorches or fades next to the fence, move it to a "
            "container on the lawn edge or swap for purslane, portulaca, Joseph’s coat, or ornamental sweet potato.",
        ),
        (
            "Nursery pots on the left",
            "Those containers dry out faster than in-ground plants. Check daily in July–August. "
            "Either plant them into the bed once weather is milder, or up-pot into larger containers "
            "with a saucer so roots do not cook against black plastic.",
        ),
    ]
    for title, detail in plant_tips:
        story.append(
            KeepTogether(
                [
                    Paragraph(f"<b>{title}</b>", styles["Body"]),
                    Paragraph(detail, styles["Body"]),
                ]
            )
        )

    story.append(PageBreak())

    # What to grow next
    story.append(Paragraph("6. Best next plants for this exact spot", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        Paragraph(
            "Lean into crops that laugh at Florida summer sun. Save lettuce, spinach, and peas "
            "for fall/winter planting (starting around October in Tampa).",
            styles["Body"],
        )
    )
    story.append(
        info_table(
            ["Great for your bed now / summer", "Why it fits", "Skip here in midsummer"],
            [
                [
                    "Okra, southern peas (crowder/black-eye), sweet potatoes",
                    "Built for heat & sand",
                    "Lettuce, cilantro, spinach",
                ],
                [
                    "Peppers, eggplant, cherry tomatoes (heat-set types)",
                    "Fruiting vegetables that tolerate 90°F+",
                    "Large slicing tomatoes (often stall)",
                ],
                [
                    "Basil, lemongrass, rosemary, Mexican tarragon",
                    "Herbs that handle sun",
                    "Parsley / soft cool herbs",
                ],
                [
                    "Zinnias, sunflowers, cosmos, marigolds, purslane",
                    "Color without constant pampering",
                    "Impatiens / shade annuals",
                ],
                [
                    "Malabar spinach, New Zealand spinach",
                    "Heat “greens” substitutes",
                    "English peas / broccoli (wait for fall)",
                ],
            ],
            styles,
            [2.45 * inch, 2.0 * inch, 2.3 * inch],
        )
    )

    # Layout & bed upgrades
    story.append(Paragraph("7. Layout upgrades for this curved bed", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        bullets(
            [
                "<b>Tallest plants at the fence:</b> sunflowers and okra already belong on the back/northish edge so they do not shade tomatoes as much.",
                "<b>Medium height in the middle:</b> tomatoes, peppers, eggplant in cages.",
                "<b>Low front edge:</b> marigolds, basil, purslane, thyme — living mulch that looks intentional from the patio.",
                "<b>Leave 18–24 inches between tomato cages</b> for airflow; Florida humidity + crowded foliage = fungal leaf spot.",
                "<b>Widen the bed by 6–12 inches</b> toward the lawn if you want more capacity — your river-stone/hardscape edge already frames a nice viewing strip.",
                "<b>Mow/weed the grass apron</b> in front of the edging. Tall weeds steal water and look unfinished next to a mulched bed.",
                "<b>Replace thin plastic edging over time</b> with thicker composite or metal edging if it buckles — keeps mulch from migrating into the lawn.",
            ],
            styles,
        )
    )

    # Pests & disease
    story.append(Paragraph("8. Tampa pests & disease quick hits", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        info_table(
            ["Issue", "What you will see", "What to do"],
            [
                [
                    "Tomato leaf spot / blight",
                    "Yellowing lower leaves, dark spots",
                    "Remove leaves, water soil only, improve spacing, mulch to stop soil splash",
                ],
                [
                    "Hornworms",
                    "Missing leaves, green caterpillars",
                    "Hand-pick mornings; leave wasps’ white cocoons on worms if present",
                ],
                [
                    "Whiteflies / aphids",
                    "Sticky leaves, tiny insects undersides",
                    "Spray undersides with water; insecticidal soap if needed",
                ],
                [
                    "Fruit scald",
                    "Pale/bleached patches on tomatoes",
                    "More leaf cover, light shade cloth, harvest earlier",
                ],
                [
                    "Blossom end rot",
                    "Dark leathery bottom on fruit",
                    "Even watering + calcium availability; do not overdo high-N fertilizer",
                ],
                [
                    "Snail/slug damage after storms",
                    "Ragged holes, slime trails",
                    "Hand-pick evenings; iron phosphate bait if pressure is high",
                ],
            ],
            styles,
            [1.6 * inch, 2.15 * inch, 3.0 * inch],
        )
    )

    # Weekly checklist
    story.append(Paragraph("9. Weekly Tampa garden checklist", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        checklist(
            [
                "Check soil moisture 3 inches down before watering; soak deeply if dry.",
                "Harvest okra / cherry tomatoes frequently — little and often beats weekend overgrowth.",
                "Deadhead marigolds and cut spent sunflower blooms you do not want for seed.",
                "Scan underside of tomato leaves for pests; remove diseased lower foliage.",
                "Tuck drip/soaker under mulch; remulch thin spots so black soil is not exposed.",
                "Pull weeds along the bed edge and mow the front lawn strip.",
                "Empty saucers / check potted plants daily during heat waves.",
                "After big storms: reset cages, clear mud splash, and check for snapped stems.",
            ],
            styles,
        )
    )

    # Seasonal calendar
    story.append(Paragraph("10. Simple Tampa seasonal rhythm", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        info_table(
            ["Season", "Focus in this bed"],
            [
                [
                    "Now through summer",
                    "Heat crops (okra, peppers, eggplant, cherry tomatoes, sweet potato, basil, zinnias). Deep water, mulch, harvest hard.",
                ],
                [
                    "Late summer",
                    "Keep plants alive through rainy humidity. Prune for air. Start planning fall transplants.",
                ],
                [
                    "Fall (Oct–Nov)",
                    "Prime season: tomatoes again, beans, cucumbers, herbs, flowers, and many leafy crops that fail in July.",
                ],
                [
                    "Winter",
                    "Cool crops thrive outdoors — brassicas, lettuce, peas, carrots. Protect only on rare frost nights.",
                ],
                [
                    "Spring",
                    "Replant warm-season crops as nights stay above ~60°F. Refresh compost and mulch.",
                ],
            ],
            styles,
            [1.55 * inch, 5.2 * inch],
        )
    )

    # Quick reference
    story.append(Paragraph("11. Quick reference card", styles["SectionHead"]))
    story.append(section_rule())
    story.append(
        info_table(
            ["Item", "Recommendation"],
            [
                ["Location", "Tampa backyard bed — full sun until ~5 p.m."],
                ["Hardiness", "USDA Zone 9b / 10a"],
                ["Biggest challenge", "Heat + white-fence reflected light + sandy soil"],
                ["Mulch depth", "2–3 inches wood mulch, clear of stems"],
                ["Watering", "Deep & consistent; morning preferred; drip ideal"],
                ["Hero crops", "Okra, cherry tomatoes, peppers, sunflowers, sweet potato, basil"],
                ["Companions", "Keep marigolds; add basil along the front edge"],
                ["Avoid midsummer", "Lettuce, spinach, cilantro, large beefsteak tomatoes"],
                ["Local help", "UF/IFAS Extension — Hillsborough County"],
            ],
            styles,
            [1.7 * inch, 5.05 * inch],
        )
    )

    story.append(Spacer(1, 0.2 * inch))
    story.append(section_rule())
    story.append(
        Paragraph(
            "This guide is tailored to a sunny Tampa fence-line bed with tomatoes, "
            "sunflowers, marigolds, and heat-loving crops. Always follow product labels "
            "and local fertilizer ordinances. For soil tests and pest ID, contact "
            "UF/IFAS Extension — Hillsborough County.",
            styles["FooterNote"],
        )
    )

    def add_page_bits(canvas, doc_):
        canvas.saveState()
        canvas.setFillColor(SUN)
        canvas.rect(0, letter[1] - 10, letter[0], 10, fill=1, stroke=0)
        canvas.setFillColor(DEEP)
        canvas.rect(0, letter[1] - 14, letter[0], 4, fill=1, stroke=0)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(
            0.7 * inch,
            0.35 * inch,
            "Tampa Full-Sun Garden Tips & Tricks",
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
    build_pdf("/workspace/Tampa_Full_Sun_Garden_Tips.pdf")
