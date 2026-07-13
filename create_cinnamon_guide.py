#!/usr/bin/env python3
"""Generate a cinnamon-for-gardening benefits PDF guide."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    ListFlowable, ListItem, KeepTogether, HRFlowable, PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

CINNAMON = HexColor("#9C4A1A")
BARK = HexColor("#5C2E14")
LEAF = HexColor("#2F6B3A")
DEEP = HexColor("#1F3D2A")
SOIL = HexColor("#3A2A1A")
MUTED = HexColor("#6B5E52")
LIGHT_ROW = HexColor("#F7F1EA")
BORDER = HexColor("#D9CBB8")
WARM = HexColor("#F4E8D8")
SPICE = HexColor("#C45C26")


def make_styles():
    s = getSampleStyleSheet()
    specs = [
        ("CoverTitle", "Helvetica-Bold", 24, 30, BARK, TA_CENTER, 8, 0, 0),
        ("CoverSub", "Helvetica", 11, 15, MUTED, TA_CENTER, 5, 0, 0),
        ("SectionHead", "Helvetica-Bold", 13, 17, DEEP, TA_LEFT, 6, 14, 0),
        ("Body", "Helvetica", 10, 14, SOIL, TA_LEFT, 7, 0, 0),
        ("CalloutText", "Helvetica", 9.5, 13, BARK, TA_LEFT, 0, 0, 0),
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
        ListItem(Paragraph(i, styles["BulletText"]), leftIndent=12, bulletColor=CINNAMON, value="•")
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
        ("BACKGROUND", (0, 0), (-1, 0), BARK),
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
        ("BACKGROUND", (0, 0), (-1, -1), WARM),
        ("BOX", (0, 0), (-1, -1), 1, CINNAMON),
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
        title="Cinnamon for Gardening: Benefits & How-To Guide",
        author="Backyard Garden Guide",
    )
    story = []

    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Cinnamon for Gardening", styles["CoverTitle"]))
    story.append(Paragraph("Benefits, Uses & How-To for Healthier Seedlings", styles["CoverSub"]))
    story.append(Paragraph(
        "Kitchen-spice methods for baby plants, cuttings, pests & soil fungi", styles["CoverSub"]))
    story.append(section_rule())

    heading(story, styles, "1. Why gardeners reach for cinnamon")
    story.append(Paragraph(
        "Ground cinnamon is more than a baking spice. The bark of "
        "<i>Cinnamomum</i> trees contains compounds (especially cinnamaldehyde) that many home "
        "gardeners use as a gentle, low-cost helper around seedlings and cuttings. It will not "
        "replace good soil, light, and watering — but used right, it can tip the odds toward "
        "stronger baby plants like basil.",
        styles["Body"]))
    story.append(bullets([
        "<b>Antifungal boost</b> — helps discourage soft molds that flatten young seedlings.",
        "<b>Cutting nurse</b> — dust on stem ends as a simple stand-in for rooting powder.",
        "<b>Pest nudge</b> — ants and some soil insects dislike crossing a cinnamon barrier.",
        "<b>Wound dust</b> — can dry and protect small pruning or transplant cuts.",
        "<b>Cheap & kitchen-ready</b> — no special product required beyond plain ground cinnamon.",
    ], styles))
    story.append(callout_box(
        "Baby basil tip",
        "Basil seedlings are famous for damping-off: stems blacken at the soil line and flop overnight. "
        "A light cinnamon dust on the potting mix surface (plus airflow and careful watering) is the "
        "classic buddy-approved trick many herb growers swear by.", styles))

    heading(story, styles, "2. Fight damping-off on seedlings")
    story.append(Paragraph(
        "Damping-off is a soil-borne fungal/oomycete problem (often <i>Pythium</i>, <i>Rhizoctonia</i>, "
        "or <i>Fusarium</i>). It thrives in cool, wet, poorly ventilated seed trays. Cinnamon’s "
        "natural antifungal properties make it a popular first-aid dust for soft seedlings.",
        styles["Body"]))
    story.append(bullets([
        "<b>When to use:</b> right after sowing, at first sprout, or at the first hint of fuzzy mold.",
        "<b>How:</b> sift a thin, even dust of ground cinnamon over the soil surface — not a thick crust.",
        "<b>Pair it with basics:</b> sterile seed-starting mix, clean trays, morning water, and a fan on low.",
        "<b>Reapply lightly</b> after heavy watering if the surface looks bare again.",
        "<b>Don’t bury seeds in cinnamon</b> — a surface dust is enough; a packed layer can slow germination.",
    ], styles))
    story.append(info_table(
        ["Symptom", "Likely cause", "Cinnamon + fix"],
        [
            ["Seedlings tip over at soil line", "Damping-off fungi",
             "Dust cinnamon; water less; add airflow"],
            ["White fuzzy mold on mix", "Surface fungus / soggy media",
             "Thin cinnamon dust; scrape mold; dry top layer"],
            ["Seeds rot before sprouting", "Overwater + cool temps",
             "Fresh mix; warmer spot; light dust after sowing"],
            ["Stems look mushy / translucent", "Advanced damping-off",
             "Remove sick plants; dust survivors; start over if needed"],
        ],
        styles, [2.1 * inch, 2.0 * inch, 2.65 * inch],
    ))

    heading(story, styles, "3. Use cinnamon as a cutting helper")
    story.append(Paragraph(
        "Commercial rooting hormones use synthetic auxins. Cinnamon is not a true hormone, but many "
        "propagators dust cuttings with it to keep stem ends cleaner while roots form — especially "
        "useful for soft herbs (basil, mint, coleus) and houseplant stems.",
        styles["Body"]))
    story.append(bullets([
        "<b>Take a clean cutting</b> with a sharp knife or snips (diagonal cut below a node).",
        "<b>Dip the cut end in water</b>, then into ground cinnamon so a light coat sticks.",
        "<b>Plant in moist (not soggy) mix</b> or place in water for easy-rooting herbs.",
        "<b>Keep humid & bright</b> (indirect light) until roots show — usually 1–3 weeks for basil.",
        "<b>Watch for rot:</b> if the stem turns brown/mushy, recut and try again with less moisture.",
    ], styles))
    story.append(callout_box(
        "Honest expectations",
        "Cinnamon is a gardener’s helper, not a miracle fertilizer. It does not feed plants N-P-K. "
        "Think of it as preventative fungal/pest hygiene that supports plants that already have "
        "decent light, drainage, and moisture.", styles))

    heading(story, styles, "4. Deter ants, gnats & curious pests")
    story.append(Paragraph(
        "Cinnamon’s strong scent and chemical bite annoy several pests. Results vary, and heavy "
        "infestations still need sanitation and traps — but cinnamon is a useful barrier tool.",
        styles["Body"]))
    story.append(info_table(
        ["Pest / issue", "How cinnamon helps", "How to apply"],
        [
            ["Ant trails into pots or beds", "Breaks scent trails; ants avoid dust",
             "Line a cinnamon trail where ants walk; refresh after rain"],
            ["Fungus gnats in seed trays", "Dries surface; less inviting top layer",
             "Dust soil surface; let top ½ inch dry between waterings"],
            ["Squirrels / cats digging", "Strong smell can discourage digging",
             "Light sprinkle on disturbed soil (reapply often)"],
            ["Aphids / soft insects", "Mild deterrent only — not a knockdown spray",
             "Use with soap spray or rinse; don’t rely on cinnamon alone"],
        ],
        styles, [2.0 * inch, 2.35 * inch, 2.4 * inch],
    ))

    story.append(PageBreak())

    heading(story, styles, "5. Protect plant wounds & transplants")
    story.append(Paragraph(
        "After pruning a soft stem, snapping a seedling, or scraping a root during transplant, a "
        "pinch of cinnamon can help dry the wound surface and discourage opportunistic mold while "
        "the plant seals itself.",
        styles["Body"]))
    story.append(bullets([
        "<b>Pruning:</b> dust freshly cut soft stems (herbs, annuals) — woody tree cuts need proper pruning sealant practice, not kitchen spice layers.",
        "<b>Transplants:</b> dust any torn root or stem nick before settling into new soil.",
        "<b>Broken seedling:</b> if the stem is still mostly intact, dust the scrape and stake gently.",
        "<b>Keep it light:</b> a pinch, not a paste — thick cloves of cinnamon can stay wet and cause its own problems.",
    ], styles))

    heading(story, styles, "6. Cinnamon tea spray (optional)")
    story.append(Paragraph(
        "Some gardeners brew a mild cinnamon “tea” to mist soil surfaces or rinse cutting ends. "
        "This is milder than dry powder and can reach into nooks of a seed tray.",
        styles["Body"]))
    story.append(info_table(
        ["Step", "What to do"],
        [
            ["1. Steep", "Stir 1–2 tsp ground cinnamon into 2 cups hot (not boiling) water."],
            ["2. Rest", "Steep 20–30 minutes, then cool fully to room temperature."],
            ["3. Strain", "Filter through a coffee filter or fine cloth so mist tips don’t clog."],
            ["4. Use", "Mist soil surface or rinse cutting tools/ends. Do not soak foliage in hot weather."],
            ["5. Shelf life", "Make fresh; refrigerate leftovers up to ~2–3 days and discard if cloudy/sour."],
        ],
        styles, [1.2 * inch, 5.55 * inch],
    ))
    story.append(Spacer(1, 0.08 * inch))
    story.append(Paragraph(
        "<b>Caution:</b> Always spot-test on one plant. Essential oils from cinnamon can burn soft "
        "leaves if too strong — stick to grocery ground cinnamon steeped in water, not concentrated oils.",
        styles["Body"]))

    heading(story, styles, "7. Which cinnamon to buy")
    story.append(info_table(
        ["Type", "Notes for gardening"],
        [
            ["Grocery ground cinnamon (Cassia)",
             "Cheapest & widely available. Perfect for dusting trays and cuttings."],
            ["Ceylon cinnamon (“true” cinnamon)",
             "Milder aroma; also fine for gardening, usually priced higher — no need to spend more."],
            ["Cinnamon sticks",
             "Grind for use, or simmer sticks for tea. Sticks alone don’t dust seed trays well."],
            ["Cinnamon essential oil",
             "Too concentrated for most DIY garden use — easy to burn plants. Skip unless diluted by an expert recipe."],
            ["Cinnamon sugar / baking blends",
             "Skip. Sugar feeds microbes and can make fungal problems worse."],
        ],
        styles, [2.35 * inch, 4.4 * inch],
    ))

    heading(story, styles, "8. Baby basil playbook")
    story.append(Paragraph(
        "Basil loves warmth and hates wet feet. Combine cinnamon with these seedling habits for "
        "better survival rates:",
        styles["Body"]))
    story.append(bullets([
        "<b>Warmth:</b> aim for ~70–80°F soil for germination; cold + wet = damping-off city.",
        "<b>Sow shallow:</b> cover seeds lightly; press mix gently, then dust a whisper of cinnamon.",
        "<b>Water from below</b> when possible so the surface stays drier; empty saucers after 20 minutes.",
        "<b>Thin early:</b> crowded basil stays humid — space or pot up once true leaves appear.",
        "<b>Airflow:</b> a small fan on low for a few hours a day toughens stems and dries the surface.",
        "<b>Light:</b> strong light after sprouting (south window or grow light 2–3 inches above tops).",
        "<b>Cinnamon touch-up:</b> re-dust if you see white mold or if the surface cake washes away.",
    ], styles))
    story.append(callout_box(
        "Humidity warning (Florida & similar climates)",
        "In humid regions, seedling fungi move fast. Cinnamon helps, but airflow + sterile mix + "
        "morning watering matter more. Never leave trays sealed under plastic after seedlings emerge.",
        styles))

    heading(story, styles, "9. What cinnamon does NOT do")
    story.append(bullets([
        "It is <b>not fertilizer</b> — plants still need compost, potting mix nutrients, or dilute feed.",
        "It will <b>not cure</b> advanced root rot or total damping-off once stems have collapsed.",
        "It is <b>not a full insecticide</b> for heavy spider mite, thrips, or caterpillar outbreaks.",
        "A thick coating can <b>crust the soil</b> and reduce water/air exchange — keep applications light.",
        "Indoor pets: keep cinnamon away from curious noses; concentrate powders can irritate airways.",
    ], styles))

    heading(story, styles, "10. Quick-start checklist")
    story.append(checklist([
        "Buy plain ground cinnamon (no sugar) and a small shaker or spice jar with holes.",
        "Start seeds in sterile seed mix; clean trays before filling.",
        "After sowing or at sprout, dust a thin cinnamon layer on the soil surface.",
        "Water carefully — damp, never swampy; prefer bottom watering for trays.",
        "Add gentle airflow once seedlings appear.",
        "For cuttings: wet stem end → dip in cinnamon → plant in moist mix.",
        "Use cinnamon lines to disrupt ant trails into seedling areas.",
        "Spot-check daily for mold, collapsed stems, or fungus gnats — act early.",
        "Reapply light dust after hard watering if the surface looks bare.",
        "Graduate survivors to stronger light and pot up before roots circle the cell.",
    ], styles))

    heading(story, styles, "11. Quick reference card")
    story.append(info_table(
        ["Item", "Recommendation"],
        [
            ["Best use", "Prevent damping-off on seedlings (basil, peppers, tomatoes, flowers)"],
            ["Secondary uses", "Cutting dust, ant barrier, light fungus-gnat surface control"],
            ["Form", "Plain ground grocery cinnamon"],
            ["Amount", "Thin dust — visible but not caked"],
            ["Frequency", "At sow/sprout; again if mold returns or rain washes it off"],
            ["Pair with", "Sterile mix, warmth, airflow, careful watering"],
            ["Avoid", "Cinnamon sugar, essential oil dumps, thick pastes"],
            ["Mindset", "Supportive hygiene — not a substitute for good culture"],
        ],
        styles, [1.7 * inch, 5.05 * inch],
    ))

    story.append(Spacer(1, 0.2 * inch))
    story.append(section_rule())
    story.append(Paragraph(
        "Home-garden methods based on common horticultural practice. Cinnamon can help discourage "
        "fungi and pests but is not a registered pesticide product — follow local guidance for serious "
        "outbreaks. Keep kitchen spices labeled separately from true garden chemicals.",
        styles["FooterNote"]))

    def add_page_bits(canvas, doc_):
        canvas.saveState()
        canvas.setFillColor(SPICE)
        canvas.rect(0, letter[1] - 10, letter[0], 10, fill=1, stroke=0)
        canvas.setFillColor(BARK)
        canvas.rect(0, letter[1] - 14, letter[0], 4, fill=1, stroke=0)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(0.7 * inch, 0.35 * inch, "Cinnamon for Gardening — Benefits & How-To")
        canvas.drawRightString(letter[0] - 0.7 * inch, 0.35 * inch, f"Page {doc_.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_page_bits, onLaterPages=add_page_bits)
    print(f"Wrote {path}")


if __name__ == "__main__":
    build_pdf("/workspace/Cinnamon_Gardening_Guide.pdf")
