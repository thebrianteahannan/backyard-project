#!/usr/bin/env python3
"""Generate a full-sun vegetable & flower garden tips PDF for Tampa, Florida."""

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


def make_styles():
    s = getSampleStyleSheet()
    specs = [
        ("CoverTitle", "Helvetica-Bold", 24, 30, DEEP, TA_CENTER, 8, 0, 0),
        ("CoverSub", "Helvetica", 11, 15, MUTED, TA_CENTER, 5, 0, 0),
        ("SectionHead", "Helvetica-Bold", 13, 17, DEEP, TA_LEFT, 6, 14, 0),
        ("Body", "Helvetica", 10, 14, SOIL, TA_LEFT, 7, 0, 0),
        ("CalloutText", "Helvetica", 9.5, 13, DEEP, TA_LEFT, 0, 0, 0),
        ("TableCell", "Helvetica", 9, 12, SOIL, TA_LEFT, 0, 0, 0),
        ("TableHeader", "Helvetica-Bold", 9, 12, white, TA_LEFT, 0, 0, 0),
        ("BulletText", "Helvetica", 10, 13, SOIL, TA_LEFT, 0, 0, 0),
        ("FooterNote", "Helvetica-Oblique", 8, 11, MUTED, TA_CENTER, 0, 0, 0),
        ("CheckItem", "Helvetica", 10, 13, SOIL, TA_LEFT, 0, 0, 0),
    ]
    for name, font, size, lead, color, align, after, before, indent in specs:
        s.add(ParagraphStyle(
            name=name, fontName=font, fontSize=size, leading=lead,
            textColor=color, alignment=align, spaceAfter=after,
            spaceBefore=before, leftIndent=indent,
        ))
    return s


def section_rule():
    return HRFlowable(width="100%", thickness=1, color=BORDER, spaceBefore=1, spaceAfter=7)


def bullets(items, styles):
    flow = [
        ListItem(Paragraph(i, styles["BulletText"]), leftIndent=12, bulletColor=LEAF, value="•")
        for i in items
    ]
    return ListFlowable(flow, bulletType="bullet", start="•", leftIndent=18, spaceBefore=1, spaceAfter=7)


def checklist(items, styles):
    rows = [[Paragraph("☐", styles["CheckItem"]), Paragraph(i, styles["CheckItem"])] for i in items]
    t = Table(rows, colWidths=[0.35 * inch, 6.4 * inch])
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


def callout_box(title, text, styles):
    inner = Paragraph(f"<b>{title}</b><br/>{text}", styles["CalloutText"])
    t = Table([[inner]], colWidths=[6.75 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SKY),
        ("BOX", (0, 0), (-1, -1), 1, LEAF),
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
        title="Tampa Full-Sun Garden Tips & Tricks",
        author="Backyard Garden Guide",
    )
    story = []

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Tampa Full-Sun Garden Guide", styles["CoverTitle"]))
    story.append(Paragraph("Tips & Tricks for a Hot, Bright Backyard Bed", styles["CoverSub"]))
    story.append(Paragraph(
        "Tampa, Florida · USDA Zone 9b/10a · All-day sun until ~5 p.m.", styles["CoverSub"]))
    story.append(section_rule())

    heading(story, styles, "1. What you already have going")
    story.append(Paragraph(
        "Your curved mulch bed against the white vinyl fence is a classic Tampa side-yard setup: "
        "long day-length sun, reflected heat, and sandy Florida soil. From your photos, the bed is "
        "already doing real work — and a few upgrades will make it more productive and less stressful "
        "in peak summer.", styles["Body"]))
    story.append(bullets([
        "<b>Sunflowers</b> — strong in full Florida sun; great for pollinators and cut flowers.",
        "<b>Cherry / salad tomatoes in cages</b> — fruiting already; cages handle wind and sprawl.",
        "<b>Marigolds under tomatoes</b> — smart companions for pests and bare-mulch cover.",
        "<b>Okra (likely) on the sunny end</b> — one of the best heat crops for Tampa summers.",
        "<b>Dark wood mulch + curved edging</b> — moisture retention and a clean bed line.",
        "<b>White fence behind the bed</b> — beautiful, but it <b>bounces extra heat and light</b> onto plants.",
    ], styles))
    story.append(callout_box(
        "Sun schedule note",
        "This spot stays sunny almost all day and only eases up around 5 p.m. Treat it as true full sun "
        "(8–10+ hours). Choose heat-loving plants, water deeply, and protect fruit from scald — do not try "
        "cool-season crops here in midsummer.", styles))

    heading(story, styles, "2. Beat the heat (and the white fence bounce)")
    story.append(Paragraph(
        "Tampa summers routinely push mid-90s with high humidity. A white vinyl fence acts like a "
        "reflector: plants in that strip often cook harder than the same varieties in open lawn.",
        styles["Body"]))
    story.append(bullets([
        "<b>Water early.</b> Aim for dawn (or before 9 a.m.) so leaves dry and roots drink before peak heat.",
        "<b>Mulch thicker.</b> Keep 2–3 inches of wood mulch, pulled back 1–2 inches from stems.",
        "<b>Shade cloth for fruit crops (optional).</b> 30% knit shade cloth on a PVC hoop over tomatoes "
        "in July–August cuts scald without stealing too much light.",
        "<b>Keep foliage between fruit and the fence.</b> Do not strip lower leaves too hard on the fence side.",
        "<b>Afternoon check.</b> Wilt that rebounds by evening is heat stress; wilt at dusk means water deeply next morning.",
        "<b>Feel the soil:</b> moist a few inches down is good; a dry/crusty top inch with limp plants means roots are baking.",
    ], styles))

    heading(story, styles, "3. Watering schedule for full-sun Tampa beds")
    story.append(info_table(
        ["Plant stage / weather", "How much", "How often"],
        [
            ["New transplants (first 10–14 days)", "Keep root zone evenly moist", "Daily light soak; then taper"],
            ["Established veggies in summer", "~1–1.5 inches total water / week", "2–3 deep waterings (not daily sprinkle)"],
            ["Fruiting tomatoes / peppers", "Deep soak to 6–8 inches", "Consistent schedule — swings cause blossom end rot & splitting"],
            ["Sunflowers & okra", "Deep weekly soak once established", "More during multi-day dry spells"],
            ["Afternoon thunderstorm weeks", "Skip or reduce irrigation", "Feel the soil 3 inches down before watering"],
        ],
        styles, [2.3 * inch, 2.2 * inch, 2.25 * inch],
    ))
    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph(
        "<b>Pro tip:</b> A soaker hose or drip line under the mulch fits this narrow bed. You water roots, "
        "leave leaves dry (fewer fungal issues in Florida humidity), and waste less water on the front grass strip.",
        styles["Body"]))

    heading(story, styles, "4. Soil upgrades that actually matter here")
    story.append(Paragraph(
        "Tampa yards are usually sandy and hungry. Dark mulch helps, but plants still need richer planting pockets.",
        styles["Body"]))
    story.append(bullets([
        "<b>Enrich each planting hole:</b> mix native sand with compost / vegetable garden mix (~50/50 for tomatoes and okra).",
        "<b>Top-dress midseason:</b> ½–1 inch finished compost around plants (keep off stems), then remulch.",
        "<b>Soil test yearly:</b> UF/IFAS Hillsborough kits are cheap; Florida often restricts phosphorus.",
        "<b>pH target:</b> most veggies prefer ~6.0–6.8. Compost helps sandy/acid soil more than quick chemical fixes.",
        "<b>Do not over-till every year.</b> Top-dress so structure and microbes build under the mulch.",
    ], styles))

    heading(story, styles, "5. Plant-by-plant tips for your bed")
    plant_tips = [
        ("Tomatoes (caged)",
         "Keep cages snug and stake them if wind hits that fence corridor. Water at soil level on a consistent "
         "schedule. Harvest cherries as they blush to reduce bird damage. Midsummer blossom drop is normal in "
         "Tampa heat. Leave enough leaf canopy to shade fruit from fence glare. Remove yellow/spotted lower "
         "leaves and bag them — do not compost diseased leaves."),
        ("Marigolds",
         "Already well placed under tomatoes. Deadhead spent blooms. Tuck more along the sunny front edge to "
         "shade bare mulch and discourage some nematodes/pests over time."),
        ("Sunflowers",
         "Water deeply at the base — tall stalks tip if only the top inch is moist. Leave a few seed heads for "
         "birds, or cut for bouquets as petals fully open. Stake early if stems lean toward the fence. Avoid "
         "heavy nitrogen — you get giant leaves and weak necks."),
        ("Okra",
         "Harvest pods at 3–4 inches (every 1–2 days in Florida heat) or they get woody fast. Side-dress lightly "
         "with nitrogen when plants are knee-high if growth stalls. Wear long sleeves when picking — many varieties itch."),
        ("Color foliage / ornamentals",
         "Deep red leafy accents are fine if they are heat types (some coleus scorches by a reflective fence). "
         "If a plant fades, move it to a container or swap for purslane, portulaca, Joseph’s coat, or ornamental sweet potato."),
        ("Nursery pots on the left",
         "Containers dry out faster than in-ground plants. Check daily in July–August. Plant into the bed when "
         "milder, or up-pot so roots do not cook against black plastic."),
    ]
    for title, detail in plant_tips:
        story.append(KeepTogether([
            Paragraph(f"<b>{title}</b>", styles["Body"]),
            Paragraph(detail, styles["Body"]),
        ]))

    story.append(PageBreak())

    heading(story, styles, "6. Best next plants for this exact spot")
    story.append(Paragraph(
        "Lean into crops that laugh at Florida summer sun. Save lettuce, spinach, and peas for fall "
        "(starting around October in Tampa).", styles["Body"]))
    story.append(info_table(
        ["Great for your bed now / summer", "Why it fits", "Skip here in midsummer"],
        [
            ["Okra, southern peas, sweet potatoes", "Built for heat & sand", "Lettuce, cilantro, spinach"],
            ["Peppers, eggplant, cherry tomatoes (heat-set)", "Fruiting veggies that tolerate 90°F+", "Large slicing tomatoes (often stall)"],
            ["Basil, lemongrass, rosemary, Mexican tarragon", "Herbs that handle sun", "Parsley / soft cool herbs"],
            ["Zinnias, sunflowers, cosmos, marigolds, purslane", "Color without constant pampering", "Impatiens / shade annuals"],
            ["Malabar / New Zealand spinach", "Heat “greens” substitutes", "English peas / broccoli (wait for fall)"],
        ],
        styles, [2.45 * inch, 2.0 * inch, 2.3 * inch],
    ))

    heading(story, styles, "7. Layout upgrades for this curved bed")
    story.append(bullets([
        "<b>Tallest at the fence:</b> sunflowers and okra so they do not shade tomatoes as much.",
        "<b>Medium height in the middle:</b> tomatoes, peppers, eggplant in cages.",
        "<b>Low front edge:</b> marigolds, basil, purslane, thyme — living mulch that looks intentional.",
        "<b>Leave 18–24 inches between tomato cages</b> for airflow; humidity + crowding = leaf spot.",
        "<b>Widen the bed 6–12 inches</b> toward the lawn if you want more capacity.",
        "<b>Mow/weed the grass apron</b> in front — tall weeds steal water and make the bed look unfinished.",
        "<b>Upgrade thin plastic edging</b> over time to thicker composite or metal if it buckles.",
    ], styles))

    heading(story, styles, "8. Tampa pests & disease quick hits")
    story.append(info_table(
        ["Issue", "What you will see", "What to do"],
        [
            ["Tomato leaf spot / blight", "Yellowing lower leaves, dark spots",
             "Remove leaves, water soil only, improve spacing, mulch to stop splash"],
            ["Hornworms", "Missing leaves, green caterpillars",
             "Hand-pick mornings; leave wasps’ white cocoons on worms if present"],
            ["Whiteflies / aphids", "Sticky leaves, tiny insects undersides",
             "Spray undersides with water; insecticidal soap if needed"],
            ["Fruit scald", "Pale/bleached patches on tomatoes",
             "More leaf cover, light shade cloth, harvest earlier"],
            ["Blossom end rot", "Dark leathery bottom on fruit",
             "Even watering + calcium; do not overdo high-N fertilizer"],
            ["Snails/slugs after storms", "Ragged holes, slime trails",
             "Hand-pick evenings; iron phosphate bait if pressure is high"],
        ],
        styles, [1.6 * inch, 2.15 * inch, 3.0 * inch],
    ))

    heading(story, styles, "9. Weekly Tampa garden checklist")
    story.append(checklist([
        "Check soil moisture 3 inches down before watering; soak deeply if dry.",
        "Harvest okra / cherry tomatoes frequently — little and often beats weekend overgrowth.",
        "Deadhead marigolds and cut spent sunflower blooms you do not want for seed.",
        "Scan tomato leaf undersides for pests; remove diseased lower foliage.",
        "Tuck drip/soaker under mulch; remulch thin spots so bare soil is not exposed.",
        "Pull weeds along the bed edge and mow the front lawn strip.",
        "Check potted plants daily during heat waves.",
        "After big storms: reset cages, clear mud splash, and check for snapped stems.",
    ], styles))

    heading(story, styles, "10. Simple Tampa seasonal rhythm")
    story.append(info_table(
        ["Season", "Focus in this bed"],
        [
            ["Now through summer",
             "Heat crops (okra, peppers, eggplant, cherry tomatoes, sweet potato, basil, zinnias). Deep water, mulch, harvest hard."],
            ["Late summer",
             "Keep plants alive through rainy humidity. Prune for air. Start planning fall transplants."],
            ["Fall (Oct–Nov)",
             "Prime season: tomatoes again, beans, cucumbers, herbs, flowers, and leafy crops that fail in July."],
            ["Winter",
             "Cool crops thrive — brassicas, lettuce, peas, carrots. Protect only on rare frost nights."],
            ["Spring",
             "Replant warm-season crops as nights stay above ~60°F. Refresh compost and mulch."],
        ],
        styles, [1.55 * inch, 5.2 * inch],
    ))

    heading(story, styles, "11. Quick reference card")
    story.append(info_table(
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
        styles, [1.7 * inch, 5.05 * inch],
    ))

    story.append(Spacer(1, 0.2 * inch))
    story.append(section_rule())
    story.append(Paragraph(
        "Tailored to a sunny Tampa fence-line bed with tomatoes, sunflowers, marigolds, and heat-loving "
        "crops. Follow product labels and local fertilizer ordinances. For soil tests and pest ID, contact "
        "UF/IFAS Extension — Hillsborough County.", styles["FooterNote"]))

    def add_page_bits(canvas, doc_):
        canvas.saveState()
        canvas.setFillColor(SUN)
        canvas.rect(0, letter[1] - 10, letter[0], 10, fill=1, stroke=0)
        canvas.setFillColor(DEEP)
        canvas.rect(0, letter[1] - 14, letter[0], 4, fill=1, stroke=0)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(0.7 * inch, 0.35 * inch, "Tampa Full-Sun Garden Tips & Tricks")
        canvas.drawRightString(letter[0] - 0.7 * inch, 0.35 * inch, f"Page {doc_.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_bits, onLaterPages=add_page_bits)
    print(f"Wrote {path}")


if __name__ == "__main__":
    build_pdf("/workspace/Tampa_Full_Sun_Garden_Tips.pdf")
