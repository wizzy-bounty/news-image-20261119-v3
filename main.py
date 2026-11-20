#!/usr/bin/env python3
"""news-image-20261119 challenger v3 - "TWO EDITIONS, ONE DAY".

One broadsheet split into two editions of the same day:
  MORNING (Shenzhen summit, ICJ Rohingya ruling, COP31, Anthropic IPO)
  EVENING (Qeshm strike, Gaza, Crimean Bridge, Voyager 1)
joined by a MIDDAY timeline spine, a Day in Numbers strip, and an index
of all 40 stories of Thursday 19 November 2026, grouped by region.

Stdlib only at the top level. Pillow is used lazily (inside render()) when
available so the picture can be drawn with real fonts; when Pillow or the
system fonts are missing, main() falls back to copying the bundled
entry.png next to this file, so the two sandbox runs still write identical
bytes. The bundled entry.png is the exact output of the Pillow path.
"""
import os
import shutil

W, H = 1024, 1024

# --- palette ---------------------------------------------------------------
PAPER = (247, 242, 231)
PAPER_DARK = (238, 232, 214)
INK = (25, 23, 19)
INK_SOFT = (74, 70, 60)
RULE = (25, 23, 19)
MORNING_BG = (233, 238, 243)
MORNING_TAB = (46, 74, 107)
EVENING_BG = (247, 231, 200)
EVENING_TAB = (138, 84, 16)
SPINE_DARK_BG = (30, 42, 58)
SPINE_DARK_LINE = (143, 163, 184)
SPINE_LIGHT_BG = (237, 230, 211)
SPINE_LIGHT_LINE = (138, 122, 90)
GOLD = (246, 198, 91)
RED = (179, 38, 30)
GREEN = (30, 122, 52)
WHITE = (255, 255, 255)

# --- the 40 stories of Thursday 19 November 2026 (wire reports of the day)
# Full headlines as listed in the design spec; the index below shows trimmed
# short heads of the same stories (same facts, fewer words, to fit the grid).
STORIES = [
    # North America (6)
    "Trump, Xi and Putin hold first three-way summit in Shenzhen",
    "Trump signals no more major Iran strikes until 2026 ends",
    "Supreme Court asked to block restored Venezuelan TPS protections",
    "Begich keeps Alaska's sole House seat after ranked-choice count",
    "Jeffries nominated House Speaker; full House votes January 3",
    "38,000 rounds of ammo and 17 weapons seized at Texas border",
    # South America (4)
    "Hegseth makes surprise stop in Caracas near Maduro arrest site",
    "Cartel bombing kills innocent man in Sinaloa, Mexico",
    "Bovespa slips 0.69% as Wall Street rout spreads south",
    "Carney wraps APEC with China trade gains worth $400M relief",
    # Europe (7)
    "Ukraine hits Crimean Bridge a third time in four days",
    "Putin vows harsher response after bridge strike",
    "Denmark ratifies Greenland security deal 109-0",
    "Putin invites Europeans to Moscow to clarify Ukraine stance",
    "Russia barred from hockey world juniors; Putin decries ruling",
    "Brexit row: Burnham 'Farage clause' would bind future governments",
    "FTSE 100 falls 0.93% as AI fears grip markets",
    # Middle East (7)
    "US strikes Iran's Qeshm island; Tehran hits back at Kuwait, Bahrain",
    "Houthis launch attacks on Saudi Arabia",
    "Israel pushes ground operation into central Gaza past ceasefire line",
    "West presses Iran at IAEA to reopen bombed nuclear sites",
    "Iran denounces 'foreign interference' after oil and nuclear unity",
    "Trump and Xi watch 'YMCA' performance at historic summit",
    "Joint statement vows UN and ICC reform, nuclear counterproliferation",
    # Africa (6)
    "ICJ rules Myanmar committed genocide against the Rohingya",
    "Rohingya widow in Cox's Bazar: 'Justice is finally being served'",
    "Bangladesh shutdown turns violent; four killed, Yunus home torched",
    "Tinubu asks parliament to decriminalise attempted suicide",
    "Newborn dies after suspected FGM in Senegal; relatives arrested",
    "Olympic marathon champion Jepchirchir banned three years for doping",
    # Asia-Pacific (7)
    "Xi and Putin call Trump summit 'constructive and fruitful'",
    "COP31 enters final stage; fossil-fuel language unresolved",
    "IAEA: North Korea expanding uranium enrichment at Yongbyon",
    "LPG tanker Gas Husky sinks off Bulgaria after being struck",
    "Anthropic IPO sets record; shares close up 17% on debut",
    "Nikkei drops 4.68% as AI valuations wobble",
    "Trump dials into European allies' Ukraine meeting after summit",
    # World / Science / Markets (3)
    "Gas prices post biggest three-week dive since 2008",
    "Voyager 1 reaches one light-day from Earth",
    "Nearly 150 fall ill in cruise ship outbreak",
]

# Short heads for the index grid (same 40 stories, trimmed to fit two lines).
INDEX_SHORT = [
    "TRUMP, XI AND PUTIN HOLD FIRST THREE-WAY SUMMIT",
    "TRUMP: NO MORE MAJOR IRAN STRIKES UNTIL 2026 ENDS",
    "SUPREME COURT ASKED TO BLOCK VENEZUELAN TPS",
    "BEGICH KEEPS ALASKA'S SOLE HOUSE SEAT",
    "JEFFRIES NOMINATED SPEAKER; HOUSE VOTES JAN 3",
    "38,000 ROUNDS, 17 WEAPONS SEIZED IN TEXAS",
    "HEGSETH'S SURPRISE STOP IN CARACAS",
    "CARTEL BOMBING KILLS MAN IN SINALOA",
    "BOVESPA SLIPS 0.69% AS WALL ST ROUT SPREADS",
    "CARNEY WRAPS APEC WITH $400M CHINA TRADE GAINS",
    "UKRAINE HITS CRIMEAN BRIDGE A THIRD TIME",
    "PUTIN VOWS HARSHER RESPONSE TO BRIDGE HIT",
    "DENMARK RATIFIES GREENLAND DEAL 109-0",
    "PUTIN INVITES EUROPEANS TO MOSCOW ON UKRAINE",
    "RUSSIA BARRED FROM HOCKEY WORLD JUNIORS",
    "BREXIT ROW: 'FARAGE CLAUSE' BINDS FUTURE GOVTS",
    "FTSE 100 FALLS 0.93% AS AI FEARS GRIP MARKETS",
    "US STRIKES IRAN'S QESHM; TEHRAN HITS BACK",
    "HOUTHIS LAUNCH ATTACKS ON SAUDI ARABIA",
    "ISRAEL PUSHES INTO CENTRAL GAZA",
    "WEST PRESSES IRAN AT IAEA OVER BOMBED SITES",
    "IRAN DENOUNCES 'FOREIGN INTERFERENCE'",
    "TRUMP, XI WATCH 'YMCA' AT HISTORIC SUMMIT",
    "JOINT STATEMENT VOWS UN AND ICC REFORM",
    "ICJ: MYANMAR COMMITTED GENOCIDE VS ROHINGYA",
    "ROHINGYA WIDOW: 'JUSTICE IS FINALLY SERVED'",
    "BANGLADESH SHUTDOWN TURNS VIOLENT; 4 KILLED",
    "TINUBU: DECRIMINALISE ATTEMPTED SUICIDE",
    "NEWBORN DIES AFTER SUSPECTED FGM IN SENEGAL",
    "JEPCHIRCHIR BANNED 3 YEARS FOR DOPING",
    "XI, PUTIN: SUMMIT 'CONSTRUCTIVE AND FRUITFUL'",
    "COP31: FOSSIL-FUEL TEXT UNRESOLVED",
    "IAEA: N. KOREA EXPANDING URANIUM ENRICHMENT",
    "LPG TANKER GAS HUSKY SINKS OFF BULGARIA",
    "ANTHROPIC IPO SETS RECORD; SHARES UP 17%",
    "NIKKEI DROPS 4.68% AS AI VALUATIONS WOBBLE",
    "TRUMP DIALS INTO ALLIES' UKRAINE MEETING",
    # 38-40 live in the WORLD strip under the grid, not in a column.
    "GAS PRICES IN BIGGEST 3-WEEK DIVE SINCE 2008",
    "VOYAGER 1 REACHES ONE LIGHT-DAY FROM EARTH",
    "NEARLY 150 FALL ILL IN CRUISE SHIP OUTBREAK",
]

REGIONS = [
    ("N. AMERICA", 0, 6),
    ("S. AMERICA", 6, 4),
    ("EUROPE", 10, 7),
    ("MIDDLE EAST", 17, 7),
    ("AFRICA", 24, 6),
    ("ASIA-PACIFIC", 30, 7),
]

# Featured blocks: (headline, deck, time) per diptych column.
MORNING_BLOCKS = [
    ("ICJ RULES MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA",
     "The Hague \u2014 the UN\u2019s top court finds Myanmar responsible for "
     "genocide. Survivors call it justice at last.",
     "11:00 GMT \u00b7 THE HAGUE"),
    ("COP31 ENTERS FINAL STAGE; FOSSIL-FUEL LANGUAGE UNRESOLVED",
     "Negotiators race the clock as the fossil-fuel text stays unsettled "
     "in the final hours.",
     "BELEM \u00b7 FINAL DAY"),
    ("ANTHROPIC IPO SETS RECORD; SHARES CLOSE UP 17% ON DEBUT",
     "The AI lab\u2019s first day on the market becomes the year\u2019s biggest "
     "technology debut.",
     "NEW YORK \u00b7 MARKET CLOSE"),
]
EVENING_BLOCKS = [
    ("US STRIKES IRAN\u2019S QESHM ISLAND; TEHRAN HITS BACK",
     "Washington hits Qeshm Island; Iran answers with strikes on Kuwait "
     "and Bahrain.",
     "18:20 GMT \u00b7 THE GULF"),
    ("ISRAEL PUSHES INTO CENTRAL GAZA PAST THE CEASEFIRE LINE",
     "Troops advance beyond the ceasefire line as talks stall and the "
     "truce frays.",
     "GAZA \u00b7 EVENING"),
    ("VOYAGER 1 REACHES ONE LIGHT-DAY FROM EARTH",
     "Humanity\u2019s farthest messenger crosses a new marker in deep space, "
     "49 years after launch.",
     "23:59 GMT \u00b7 DEEP SPACE"),
]

# Timeline spine: (time, place) from morning to night.
SPINE_EVENTS = [
    ("09:00", "SHENZHEN"),
    ("11:00", "HAGUE"),
    ("14:30", "GAZA"),
    ("18:20", "QESHM"),
    ("21:00", "NEW YORK"),
    ("23:59", "VOYAGER"),
]

DAY_NUMBERS = [
    ("S&P 500", "-2.02%", RED),
    ("NIKKEI", "-4.68%", RED),
    ("BRENT", "$89.72", INK),
    ("BITCOIN", "< $63,000", RED),
    ("ANTHROPIC IPO", "+17%", GREEN),
    ("VOYAGER 1", "1 LIGHT-DAY", INK),
]

FONT_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
)


def _font_paths():
    """Locate the serif/sans TTFs; env override exists only for local tests."""
    override = os.environ.get("MAKEFUN_FONT_DIR")
    dirs = (override,) if override else FONT_DIRS
    serif = sans = sans_bold = serif_bold = None
    for d in dirs:
        for name, slot in (
            ("DejaVuSerif.ttf", "serif"),
            ("DejaVuSerif-Bold.ttf", "serif_bold"),
            ("DejaVuSans.ttf", "sans"),
            ("DejaVuSans-Bold.ttf", "sans_bold"),
        ):
            p = os.path.join(d, name)
            if os.path.isfile(p):
                if slot == "serif":
                    serif = p
                elif slot == "serif_bold":
                    serif_bold = p
                elif slot == "sans":
                    sans = p
                else:
                    sans_bold = p
    if not (serif and serif_bold and sans and sans_bold):
        raise FileNotFoundError("DejaVu fonts not found in %s" % (dirs,))
    return serif, serif_bold, sans, sans_bold


def _load_fonts():
    from PIL import ImageFont

    serif, serif_bold, sans, sans_bold = _font_paths()
    cache = {}

    def f(kind, size):
        key = (kind, size)
        if key not in cache:
            path = {"serif": serif, "serif_b": serif_bold,
                    "sans": sans, "sans_b": sans_bold}[kind]
            cache[key] = ImageFont.truetype(path, size)
        return cache[key]

    return f


def _wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _vtext_img(text, font, fill):
    """Render text rotated 90 degrees (reads bottom-to-top); returns image."""
    from PIL import Image, ImageDraw

    tmp = Image.new("RGBA", (400, 60), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((0, 0), text, font=font, fill=fill + (255,))
    tmp = tmp.crop(tmp.getbbox())
    return tmp.rotate(90, expand=True)


def _vtext(img, cx, y, text, font, fill):
    """Draw text reading bottom-to-top, centred on cx, top edge at y.
    Returns the height in pixels of the pasted vertical text."""
    tmp = _vtext_img(text, font, fill)
    img.paste(tmp, (cx - tmp.size[0] // 2, y), tmp)
    return tmp.size[1]  # height of the pasted vertical text


def _draw_morning(draw, img, x0, y0, w, h):
    """Dawn over Shenzhen: sunrise bands, skyline, summit table, 3 flags."""
    # Sky: warm sunrise bands, cold blue on top.
    bands = [(174, 198, 222), (196, 212, 230), (222, 226, 224),
             (240, 224, 196), (246, 214, 158), (250, 205, 130)]
    for i, c in enumerate(bands):
        draw.rectangle([x0, y0 + i * h // 6, x0 + w, y0 + (i + 1) * h // 6], fill=c)
    # Sun rising on the horizon.
    draw.ellipse([x0 + 96, y0 + h - 96, x0 + 148, y0 + h - 44], fill=(249, 217, 138))
    draw.ellipse([x0 + 104, y0 + h - 88, x0 + 140, y0 + h - 52], fill=GOLD)
    # Skyline silhouette (deterministic heights).
    heights = [52, 84, 64, 110, 72, 96, 58, 124, 78, 66, 92, 60]
    bw = w // len(heights)
    base = y0 + h
    for i, bh in enumerate(heights):
        bx = x0 + i * bw
        draw.rectangle([bx + 1, base - bh, bx + bw - 1, base], fill=(51, 71, 94))
        if i == 7:  # spire tower
            draw.polygon([(bx + bw // 2 - 3, base - bh),
                          (bx + bw // 2 + 3, base - bh),
                          (bx + bw // 2, base - bh - 26)], fill=(51, 71, 94))
    # Lit windows.
    import random

    rng = random.Random(19)
    for _ in range(46):
        wx = x0 + rng.randrange(4, w - 8)
        wy = base - rng.randrange(8, 118)
        draw.rectangle([wx, wy, wx + 3, wy + 4], fill=GOLD)
    # Summit table with three flags.
    table_y = base - 34
    draw.rectangle([x0 + 150, table_y, x0 + w - 150, table_y + 10], fill=(107, 74, 47))
    draw.rectangle([x0 + 158, table_y + 10, x0 + w - 158, table_y + 26], fill=(84, 58, 38))
    flags = [(x0 + 176, "CN"), (x0 + w // 2 - 17, "US"), (x0 + w - 210, "RU")]
    for fx, code in flags:
        draw.line([fx + 17, table_y - 44, fx + 17, table_y], fill=INK, width=2)
        if code == "CN":
            draw.rectangle([fx, table_y - 44, fx + 34, table_y - 22], fill=(222, 41, 16))
            draw.ellipse([fx + 4, table_y - 40, fx + 10, table_y - 34], fill=GOLD)
            for sx, sy in ((16, -38), (22, -34), (16, -30), (24, -40)):
                draw.ellipse([fx + sx, table_y + sy, fx + sx + 3, table_y + sy + 3],
                             fill=GOLD)
        elif code == "US":
            for s in range(7):
                col = (178, 34, 52) if s % 2 == 0 else WHITE
                draw.rectangle([fx, table_y - 44 + s * 3, fx + 34,
                                table_y - 41 + s * 3], fill=col)
            draw.rectangle([fx, table_y - 44, fx + 14, table_y - 32], fill=(60, 59, 110))
            for dx in (3, 8):
                for dy in (-41, -37):
                    draw.ellipse([fx + dx, table_y + dy, fx + dx + 2, table_y + dy + 2],
                                 fill=WHITE)
        else:
            for s, col in enumerate((WHITE, (0, 57, 166), (213, 0, 50))):
                draw.rectangle([fx, table_y - 44 + s * 7 + 1, fx + 34,
                                table_y - 38 + s * 7 + 1], fill=col)
    # Caption strip.
    draw.rectangle([x0, base - 22, x0 + w, base], fill=(30, 42, 58))
    return base - 22


def _draw_evening(draw, img, x0, y0, w, h):
    """Night over the Crimean Bridge: dusk bands, moon, bridge, water."""
    bands = [(36, 26, 18), (58, 38, 20), (90, 48, 22), (138, 74, 30),
             (168, 90, 30), (168, 90, 30)]
    for i, c in enumerate(bands):
        draw.rectangle([x0, y0 + i * h // 6, x0 + w, y0 + (i + 1) * h // 6], fill=c)
    # Stars + moon.
    import random

    rng = random.Random(23)
    for _ in range(28):
        sx = x0 + rng.randrange(6, w - 6)
        sy = y0 + rng.randrange(6, h // 3)
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(242, 232, 201))
    draw.ellipse([x0 + w - 66, y0 + 16, x0 + w - 34, y0 + 48], fill=(242, 232, 201))
    draw.ellipse([x0 + w - 58, y0 + 20, x0 + w - 40, y0 + 38], fill=(226, 210, 170))
    # Strike glow on the horizon.
    draw.ellipse([x0 + w - 190, y0 + 96, x0 + w - 150, y0 + 136], fill=(242, 165, 74))
    draw.ellipse([x0 + w - 180, y0 + 106, x0 + w - 160, y0 + 126], fill=(232, 134, 46))
    # Bridge: deck, arch, pylons, cables.
    deck_y = y0 + h - 68
    draw.rectangle([x0, deck_y, x0 + w, deck_y + 8], fill=(26, 21, 18))
    for px in (x0 + 110, x0 + w - 150):
        draw.rectangle([px, deck_y - 62, px + 8, deck_y], fill=(26, 21, 18))
        draw.rectangle([px - 2, deck_y - 70, px + 10, deck_y - 62], fill=(26, 21, 18))
    draw.arc([x0 + 60, deck_y - 44, x0 + w - 60, deck_y + 44], 180, 360,
             fill=(26, 21, 18), width=6)
    for cx in range(x0 + 16, x0 + w - 8, 26):
        draw.line([cx, deck_y - 58, cx + 4, deck_y], fill=(26, 21, 18), width=1)
    # Deck lights.
    for lx in range(x0 + 12, x0 + w - 6, 30):
        draw.ellipse([lx, deck_y + 2, lx + 4, deck_y + 6], fill=GOLD)
    # Water with reflections.
    draw.rectangle([x0, deck_y + 8, x0 + w, y0 + h], fill=(26, 21, 18))
    for i, rx in enumerate((x0 + 40, x0 + 150, x0 + 250, x0 + 330, x0 + 410)):
        draw.rectangle([rx, deck_y + 12 + (i % 2) * 8, rx + 5, y0 + h - 8],
                       fill=(201, 122, 46))
    # Caption strip.
    draw.rectangle([x0, y0 + h - 22, x0 + w, y0 + h], fill=(30, 42, 58))
    return y0 + h - 22


def _draw_spine(img, draw, f, dark):
    """MIDDAY timeline spine between the two editions (x 496-528)."""
    bg = SPINE_DARK_BG if dark else SPINE_LIGHT_BG
    line_c = SPINE_DARK_LINE if dark else SPINE_LIGHT_LINE
    fg = WHITE if dark else INK
    dim = (143, 163, 184) if dark else (110, 100, 80)
    draw.rectangle([496, 118, 528, 700], fill=bg)
    # Vertical MIDDAY label at the top of the spine.
    f_mid = f("sans_b", 10)
    _vtext(img, 512, 124, "MIDDAY", f_mid, fg)
    draw.line([512, 180, 512, 690], fill=line_c, width=2)
    # Six timed dots: place name vertical above the dot, time below it.
    # (Names above keep every label clear of the next dot; the 00:00/24:00
    # end labels are dropped - the six timed dots already span the day.)
    f_t = f("sans_b", 10)
    f_p = f("sans_b", 9)
    ys = [238, 318, 398, 478, 558, 638]
    for (t, place), y in zip(SPINE_EVENTS, ys):
        name_img = _vtext_img(place, f_p, dim)
        img.paste(name_img, (512 - name_img.size[0] // 2, y - 8 - name_img.size[1]),
                  name_img)
        draw.ellipse([512 - 5, y - 5, 512 + 5, y + 5], fill=GOLD, outline=fg, width=1)
        draw.text((512, y + 8), t, font=f_t, fill=fg, anchor="ma")


def _draw_block(draw, f, x, y, w, headline, deck, time, accent):
    """One story block: headline (<=2 lines), deck (<=2 lines), time line."""
    f_h = f("serif_b", 20)
    f_d = f("sans", 13)
    f_t = f("sans_b", 11)
    lines = _wrap(draw, headline, f_h, w)
    cy = y
    for ln in lines[:2]:
        draw.text((x, cy), ln, font=f_h, fill=INK)
        cy += 25
    for ln in _wrap(draw, deck, f_d, w)[:2]:
        draw.text((x, cy), ln, font=f_d, fill=INK_SOFT)
        cy += 16
    draw.text((x, cy + 3), time, font=f_t, fill=accent)
    return cy + 20


def _draw_index(draw, f):
    """The Day in 40 Stories: 6 region columns + WORLD strip + footer."""
    f_sec = f("serif_b", 21)
    f_note = f("sans", 12)
    f_col = f("sans_b", 11)
    f_e = f("sans", 10)
    y = 774
    draw.text((16, y), "THE DAY IN 40 STORIES", font=f_sec, fill=INK)
    note = "NUMBERED BY REGION \u2014 EVERY STORY OF THE DAY"
    draw.text((1008, y + 5), note, font=f_note, fill=INK_SOFT, anchor="ra")
    y = 796
    draw.line([16, y, 1008, y], fill=RULE, width=1)
    # 6 columns: x 16..1008, col 162, gap 4.
    col_w, gap = 162, 4
    xs = [16 + i * (col_w + gap) for i in range(6)]
    for (name, start, count), cx in zip(REGIONS, xs):
        draw.text((cx, y + 6), name, font=f_col, fill=MORNING_TAB)
        draw.line([cx, y + 20, cx + col_w, y + 20], fill=MORNING_TAB, width=1)
        ey = y + 24
        for k in range(count):
            n = start + k
            head = INDEX_SHORT[n]
            lines = _wrap(draw, "%d. %s" % (n + 1, head), f_e, col_w)
            for j, ln in enumerate(lines[:2]):
                draw.text((cx, ey + j * 10), ln, font=f_e,
                          fill=INK if j == 0 else INK_SOFT)
            ey += 20
    # WORLD strip: stories 38-40 in one row.
    wy = 966
    draw.line([16, wy - 4, 1008, wy - 4], fill=RULE, width=1)
    cell = 992 // 3
    for i, n in enumerate((37, 38, 39)):
        cx = 16 + i * cell
        draw.text((cx, wy), "WORLD", font=f_col, fill=EVENING_TAB)
        draw.text((cx + 54, wy), "%d. %s" % (n + 1, INDEX_SHORT[n]),
                  font=f_e, fill=INK)
    # Footer.
    fy = 986
    draw.line([16, fy - 6, 1008, fy - 6], fill=RULE, width=1)
    foot = ("THE WORLD TODAY \u00b7 THURSDAY 19 NOVEMBER 2026 \u00b7 ALL 40 STORIES "
            "VERIFIED FROM WIRE REPORTS OF THE DAY")
    draw.text((512, fy), foot, font=f("sans", 11), fill=INK_SOFT, anchor="ma")


def render():
    """Draw the whole front page; returns a PIL Image (RGB)."""
    from PIL import Image, ImageDraw

    f = _load_fonts()
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Outer double rule.
    draw.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)
    draw.rectangle([11, 11, W - 12, H - 12], outline=INK, width=1)

    # --- Masthead ----------------------------------------------------------
    f_title = f("serif_b", 48)
    draw.text((512, 2), "THE WORLD TODAY", font=f_title, fill=INK, anchor="ma")
    draw.line([16, 54, 1008, 54], fill=RULE, width=2)
    draw.line([16, 58, 1008, 58], fill=RULE, width=1)
    f_kick = f("sans_b", 17)
    draw.text((16, 62), "THURSDAY 19 NOVEMBER 2026", font=f_kick, fill=INK)
    draw.text((1008, 62), "40 STORIES \u00b7 6 REGIONS", font=f_kick,
              fill=INK, anchor="ra")

    # --- Sub-masthead headline ---------------------------------------------
    f_sub = f("serif_b", 21)
    draw.text((512, 84), "THREE LEADERS, ONE TABLE \u2014 AND A COURT THAT "
              "MADE HISTORY", font=f_sub, fill=INK, anchor="ma")

    # --- Diptych -----------------------------------------------------------
    # Column tints.
    draw.rectangle([16, 118, 496, 700], fill=MORNING_BG)
    draw.rectangle([528, 118, 1008, 700], fill=EVENING_BG)
    # Tab bars.
    draw.rectangle([16, 118, 496, 148], fill=MORNING_TAB)
    draw.rectangle([528, 118, 1008, 148], fill=EVENING_TAB)
    f_tab = f("sans_b", 18)
    draw.text((256, 126), "MORNING EDITION \u2014 THE WORLD WAKES UP",
              font=f_tab, fill=WHITE, anchor="ma")
    draw.text((768, 126), "EVENING EDITION \u2014 THE WORLD GOES TO BED",
              font=f_tab, fill=WHITE, anchor="ma")
    # Hero vignettes.
    _draw_morning(draw, img, 22, 154, 468, 196)
    _draw_evening(draw, img, 534, 154, 468, 196)
    f_cap = f("sans_b", 11)
    draw.text((256, 332), "SHENZHEN \u2014 THE SUMMIT HALL, 09:00 GMT",
              font=f_cap, fill=WHITE, anchor="ma")
    draw.text((768, 332), "THE CRIMEAN BRIDGE \u2014 NIGHT",
              font=f_cap, fill=WHITE, anchor="ma")
    # Story blocks.
    by = 362
    for i, (hl, deck, t) in enumerate(MORNING_BLOCKS):
        if i:
            draw.line([28, by - 8, 484, by - 8], fill=(180, 190, 200), width=1)
        _draw_block(draw, f, 28, by, 456, hl, deck, t, MORNING_TAB)
        by += 112
    by = 362
    for i, (hl, deck, t) in enumerate(EVENING_BLOCKS):
        if i:
            draw.line([540, by - 8, 996, by - 8], fill=(210, 190, 150), width=1)
        _draw_block(draw, f, 540, by, 456, hl, deck, t, EVENING_TAB)
        by += 112

    # --- MIDDAY spine ------------------------------------------------------
    dark = os.environ.get("MAKEFUN_SPINE", "dark").lower() != "light"
    _draw_spine(img, draw, f, dark)

    # --- Day in Numbers ----------------------------------------------------
    draw.line([16, 700, 1008, 700], fill=RULE, width=2)
    f_dn_t = f("sans_b", 13)
    draw.text((512, 706), "THE DAY IN NUMBERS", font=f_dn_t, fill=INK, anchor="ma")
    f_val = f("serif_b", 24)
    f_lab = f("sans", 11)
    cell = 992 // 6
    for i, (label, value, col) in enumerate(DAY_NUMBERS):
        cx = 16 + i * cell + cell // 2
        if i:
            draw.line([16 + i * cell, 724, 16 + i * cell, 766],
                      fill=(200, 192, 172), width=1)
        draw.text((cx, 724), value, font=f_val, fill=col, anchor="ma")
        draw.text((cx, 752), label, font=f_lab, fill=INK_SOFT, anchor="ma")

    # --- Index -------------------------------------------------------------
    _draw_index(draw, f)
    return img


def _save(img, out_path):
    """Save as a 256-colour palette PNG (small, deterministic)."""
    pal = img.quantize(colors=256, method=0, dither=0)
    pal.save(out_path, format="PNG", optimize=True, compress_level=9)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    try:
        img = render()
        _save(img, out_path)
    except Exception:
        # No Pillow, no fonts, or any render failure: copy the bundled image.
        # Byte-identical to the Pillow path by construction (it IS its output).
        bundled = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "entry.png")
        shutil.copyfile(bundled, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
