#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a cucumber growing tips & tricks PDF guide."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    ListFlowable, ListItem, HRFlowable, PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

LEAF = HexColor("#2F6B3A")
DEEP = HexColor("#1A3D28")
CUKE = HexColor("#5A9A3C")
SOIL = HexColor("#3A2A1A")
MUTED = HexColor("#5E6A5F")
LIGHT_ROW = HexColor("#F3F7F1")
BORDER = HexColor("#D0D9CB")
SKY = HexColor("#E8F0E4")
SUN = HexColor("#C45C26")


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
        ListItem(Paragraph(i, styles["BulletText"]), leftIndent=12, bulletColor=CUKE, value="•")
        for i in items
    ]
    return ListFlowable(flow, bulletType="bullet", start="•", leftIndent=18, spaceBefore=1, spaceAfter=7)


def checklist(items, styles):
    rows = [[Paragraph("?", styles["CheckItem"]), Paragraph(i, styles["CheckItem"])] for i in items]
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
        title="Cucumber Growing Tips & Tricks",
        author="Backyard Garden Guide",
    )
    story = []

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Growing Cucumbers", styles["CoverTitle"]))
    story.append(Paragraph(
        "Tips &amp; Tricks: Vine Habits, Vertical vs. Ground, and What They Need",
        styles["CoverSub"]))
    story.append(Paragraph(
        "A practical backyard guide for healthy vines and crisp harvests", styles["CoverSub"]))
    story.append(section_rule())

    heading(story, styles, "1. Quick answers")
    story.append(Paragraph(
        "Start here if you only have a minute — then dig into the sections below.",
        styles["Body"]))
    story.append(info_table(
        ["Question", "Short answer"],
        [
            ["Is a cucumber a vine?",
             "Yes. Almost all garden cucumbers are climbing/rambling vines with tendrils."],
            ["Vertical or horizontal?",
             "Both work. Vertical (trellis) saves space, improves air flow, and keeps fruit cleaner. Horizontal (on the ground) is fine if you have room and use mulch."],
            ["On the ground or off?",
             "Roots stay in soil either way. Fruit is happier off the ground (trellis or a bed of mulch/straw) to reduce rot and pests."],
            ["What does it need?",
             "Warmth, full sun, steady water, rich well-drained soil, and pollination (or a parthenocarpic variety)."],
        ],
        styles, [2.0 * inch, 4.75 * inch],
    ))
    story.append(Spacer(1, 0.08 * inch))
    story.append(callout_box(
        "Bottom line",
        "Treat cucumbers as warm-season vines. Give them a trellis if you can — they climb gladly — "
        "and keep soil evenly moist once fruit sets. Most problems come from cold starts, irregular "
        "watering, or wet leaves sitting overnight.",
        styles))

    heading(story, styles, "2. Yes — cucumbers are vines")
    story.append(Paragraph(
        "Garden cucumbers (<i>Cucumis sativus</i>) are annual vines in the squash family. They send out "
        "long stems with curling tendrils that grab fences, netting, string, or neighboring plants. "
        "Bush or “patio” types exist, but even those still sprawl a bit — they are compact vines, not "
        "true upright shrubs.",
        styles["Body"]))
    story.append(bullets([
        "<b>Vining / slicing types</b> — long runners (often 6–10+ ft). Best on a trellis.",
        "<b>Pickling types</b> — often vigorous vines; same training rules as slicers.",
        "<b>Bush / container types</b> — shorter internodes; still appreciate a small cage or stake.",
        "<b>Tendrils</b> — the plant’s “hands.” Guide them onto supports early so stems don’t flop.",
    ], styles))

    heading(story, styles, "3. Vertical vs. horizontal growing")
    story.append(Paragraph(
        "You can let vines crawl on mulched ground or train them up. For most small yards, "
        "<b>vertical wins</b> — especially in humid climates where leaf diseases move fast.",
        styles["Body"]))
    story.append(info_table(
        ["Method", "Pros", "Cons / tips"],
        [
            ["Vertical (trellis, A-frame, cattle panel, netting)",
             "Saves space; cleaner fruit; better airflow; easier picking; less slug/rot contact",
             "Needs sturdy support (vines + fruit get heavy). Soft-tie stems every 12–18 in."],
            ["Horizontal (ground sprawl)",
             "No build; good for large beds; fruit can hide in shade of leaves",
             "Needs 4–6+ ft of room per plant. Mulch under fruit. Scout for soft spots and bugs."],
            ["Hybrid: sprawl + straw mulch pads",
             "Simple middle path if you lack a trellis",
             "Still watch for mildew and yellowing lower leaves; don’t walk on vines."],
        ],
        styles, [2.25 * inch, 2.25 * inch, 2.25 * inch],
    ))
    story.append(Spacer(1, 0.08 * inch))
    story.append(callout_box(
        "Support tip",
        "Cucumbers climb with tendrils but stems can slip. Weave young vines through netting or "
        "loosely figure-eight them with soft cloth ties. Avoid thin wire that cuts into stems as they thicken.",
        styles))

    heading(story, styles, "4. On the ground or off the ground?")
    story.append(Paragraph(
        "Roots always grow in soil (or a container mix). The decision is where the <b>stems and fruit</b> live.",
        styles["Body"]))
    story.append(bullets([
        "<b>Best fruit quality:</b> hang cucumbers vertically so they hang free — straighter shapes, less yellow belly, less soil splash.",
        "<b>If sprawling:</b> lay a bed of clean straw, leaves, or landscape fabric under vines so fruit is not sitting on bare dirt.",
        "<b>Raised beds &amp; containers:</b> still “in soil,” just warmer and better drained — excellent for cucumbers in clay yards.",
        "<b>Hanging baskets:</b> only for compact bush varieties with frequent watering — fruit dries out fast in wind.",
    ], styles))
    story.append(Paragraph(
        "Off-the-ground fruit ? hydroponics. You are simply keeping cucumbers away from mud, slugs, "
        "and fungal splash — one of the highest-payoff tricks in cucumber growing.",
        styles["Body"]))

    heading(story, styles, "5. What a cucumber plant needs")
    story.append(info_table(
        ["Need", "Target", "Notes"],
        [
            ["Sun", "6–8+ hours full sun", "Morning sun + afternoon shade can help in extreme heat."],
            ["Warmth", "Soil ~70°F+; air warm nights", "Cold soil = stunted vines and bitter fruit. Don’t rush spring."],
            ["Soil", "Rich, loose, well-drained; pH ~6.0–7.0", "Work in compost. Avoid soggy clay pockets."],
            ["Water", "~1–1.5 in/week; even moisture", "Inconsistent water ? bitter cukes and misshapen fruit."],
            ["Food", "Moderate nitrogen; steady later nutrients", "Too much early N = big leaves, few flowers."],
            ["Space / support", "12–24 in apart on trellis; more if sprawling", "Crowding traps humidity and disease."],
            ["Pollination", "Bees (or hand-pollinate)", "Or choose parthenocarpic / greenhouse types that set without bees."],
        ],
        styles, [1.35 * inch, 2.15 * inch, 3.25 * inch],
    ))

    story.append(PageBreak())

    heading(story, styles, "6. Planting &amp; early care")
    story.append(bullets([
        "<b>Timing:</b> plant after frost risk and when nights stay reliably warm. In Tampa Bay, that often means spring plantings after cool snaps fade, and a second shot in early fall before nights chill.",
        "<b>Sow vs. transplant:</b> cucumbers dislike root disturbance. Direct-sow ½–1 in deep, or start in biodegradable pots and plant the whole pot.",
        "<b>Hill or row:</b> traditional “hills” of 2–3 seeds thinned to the strongest plant still work; on a trellis, plant in a straight row along the base.",
        "<b>Mulch early:</b> once soil is warm, mulch to lock moisture and block weeds — don’t mulch over ice-cold soil in early spring.",
        "<b>Protect seedlings:</b> cutworms, snails, and birds love tender starts. Use collars or light covers at night if needed.",
    ], styles))

    heading(story, styles, "7. Watering, feeding &amp; training tricks")
    story.append(bullets([
        "<b>Water at the base</b> in the morning. Wet leaves overnight invite powdery mildew and downy mildew.",
        "<b>Deep, less often</b> beats daily sips once roots are established — keep the top couple inches from crusting bone-dry.",
        "<b>Side-dress</b> with compost or a balanced organic fertilizer when vines run and again when first fruit sets.",
        "<b>Train weekly:</b> tuck new growth onto the trellis before it flops sideways into the lawn.",
        "<b>Prune lightly:</b> you can remove a few oldest yellow leaves near the base for airflow. Don’t strip the plant bare.",
        "<b>Male vs. female flowers:</b> early male flowers are normal. Females have a tiny cucumber behind the bloom. Patience — then bees do the rest.",
    ], styles))
    story.append(callout_box(
        "Bitter cucumber fix",
        "Bitterness is often stress: irregular water, extreme heat, or genetics. Pick often, water "
        "evenly, choose “burpless” or milder varieties, and harvest before fruits get oversized and seedy.",
        styles))

    heading(story, styles, "8. Common problems &amp; quick fixes")
    story.append(info_table(
        ["Problem", "Likely cause", "What to do"],
        [
            ["Powdery mildew (white dust on leaves)",
             "Humidity + poor air + evening wet leaves",
             "Grow vertical; morning water; thin leaves; use resistant varieties"],
            ["Yellow leaves / sudden wilt",
             "Bacterial wilt (cucumber beetles) or root stress",
             "Control beetles early; remove collapsed vines; don’t compost them"],
            ["Flowers but no fruit",
             "No pollinators, heat stress, or only male blooms yet",
             "Hand-pollinate with a soft brush; plant bee flowers; wait for females"],
            ["Misshapen / hooked fruit",
             "Incomplete pollination or water stress",
             "Improve bee visits; keep moisture even"],
            ["Fruit soft / yellow belly on ground",
             "Sitting on wet soil; overripe",
             "Trellis or mulch; harvest when skin is firm and green"],
            ["Cucumber beetles chewing leaves",
             "Common early-season pest",
             "Row cover until flowers; hand-pick; yellow sticky traps nearby"],
        ],
        styles, [2.1 * inch, 2.15 * inch, 2.5 * inch],
    ))

    heading(story, styles, "9. Harvest tips")
    story.append(bullets([
        "<b>Pick young and often.</b> Leaving giant cukes on the vine signals the plant to stop making new ones.",
        "<b>Use snips or a knife</b> — twisting can yank vines off the trellis.",
        "<b>Slicers:</b> usually best at 6–8 in (check the seed packet). Skin should be firm, not dull and soft.",
        "<b>Picklers:</b> harvest smaller, at the size your recipe wants.",
        "<b>Morning harvest</b> often tastes crispest; refrigerate soon after picking.",
    ], styles))

    heading(story, styles, "10. Tampa / hot-humid climate notes")
    story.append(Paragraph(
        "In Florida’s humid heat, disease pressure is the real boss — not cold. Vertical growing, "
        "morning watering, and choosing resistant varieties matter more here than in dry climates.",
        styles["Body"]))
    story.append(bullets([
        "<b>Prefer trellis culture</b> to dry leaves faster after afternoon storms.",
        "<b>Watch extreme midsummer:</b> fruit set can pause when nights and days stay brutally hot — fall plantings often perform beautifully.",
        "<b>Downy mildew</b> is a regional threat on cucurbits; look for yellow angular leaf spots and act early (remove bad leaves; avoid crowding).",
        "<b>Afternoon shade cloth (30%)</b> during heat waves can reduce wilting without killing productivity.",
        "<b>Sandy soil:</b> add compost so water and nutrients don’t drain straight through.",
    ], styles))

    heading(story, styles, "11. Quick-start checklist")
    story.append(checklist([
        "Wait for warm soil and frost-free nights before planting.",
        "Choose a sunny spot with compost-rich, well-drained soil (or a raised bed/large pot).",
        "Decide: trellis (recommended) or mulched ground sprawl.",
        "Install a sturdy support before vines take off.",
        "Sow or transplant with gentle root handling; water in well.",
        "Mulch once soil is warm; water at the base in the morning.",
        "Train tendrils onto the support weekly; soft-tie as needed.",
        "Watch for beetles and mildew; harvest often while fruit is crisp.",
        "Side-dress at vine-run and first fruit set.",
        "Save a note of which variety performed best for next season.",
    ], styles))

    heading(story, styles, "12. Quick reference card")
    story.append(info_table(
        ["Item", "Recommendation"],
        [
            ["Plant type", "Warm-season annual vine with tendrils"],
            ["Best training", "Vertical trellis for most backyards"],
            ["Fruit position", "Off the ground (hanging or on thick mulch)"],
            ["Sun / water", "Full sun; even moisture at the root zone"],
            ["Soil", "Rich, drained, compost-amended; raised bed OK"],
            ["Spacing", "Closer on a trellis; generous room if sprawling"],
            ["Pollination", "Bees or hand-pollinate; or parthenocarpic seed"],
            ["Biggest tip", "Pick often + water evenly + keep leaves dry at night"],
        ],
        styles, [1.7 * inch, 5.05 * inch],
    ))

    story.append(Spacer(1, 0.2 * inch))
    story.append(section_rule())
    story.append(Paragraph(
        "Home-garden guidance based on common horticultural practice. Variety choices, local pests, "
        "and microclimate can change results — always check your seed packet and local extension advice "
        "for Tampa Bay planting windows and disease alerts.",
        styles["FooterNote"]))

    def add_page_bits(canvas, doc_):
        canvas.saveState()
        canvas.setFillColor(CUKE)
        canvas.rect(0, letter[1] - 10, letter[0], 10, fill=1, stroke=0)
        canvas.setFillColor(DEEP)
        canvas.rect(0, letter[1] - 14, letter[0], 4, fill=1, stroke=0)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(0.7 * inch, 0.35 * inch, "Growing Cucumbers — Tips & Tricks")
        canvas.drawRightString(letter[0] - 0.7 * inch, 0.35 * inch, f"Page {doc_.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_bits, onLaterPages=add_page_bits)
    print(f"Wrote {path}")


if __name__ == "__main__":
    build_pdf("/workspace/Cucumber_Growing_Guide.pdf")
