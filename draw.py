#!/usr/bin/env python3
"""Render the one-page broadsheet for news-image-20261124 (Sparta r2).

Run: python3 draw.py  -> writes entry.png next to this file.
All drawing lives here; main.py only copies the pre-rendered PNG.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (250, 247, 238)
INK = (18, 18, 18)
RULE = (120, 115, 100)
ACCENT = (150, 30, 25)
BLUE = (25, 60, 110)
GREEN = (30, 95, 55)
MUTED = (90, 86, 76)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK, justify=False):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading):
    return para(draw, x, y, text, fnt, max_w, leading)


def rule(draw, x, y, w, width=2, color=RULE):
    draw.line([(x, y), (x + w, y)], fill=color, width=width)


def kicker(draw, x, y, text, color=ACCENT):
    draw.text((x, y), text, font=font(SANS_B, 15), fill=color)
    return y + 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer border
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    d.rectangle([14, 14, W - 15, H - 15], outline=RULE, width=1)

    # ---- masthead ----
    d.text((512, 34), "THE DAILY GLOBE", font=font(SERIF_B, 64),
           fill=INK, anchor="ma")
    d.text((512, 108), "WORLD NEWS  •  MARKETS  •  SPORT  •  CLIMATE",
           font=font(SANS_B, 15), fill=MUTED, anchor="ma")
    rule(d, 34, 138, 956, 3, INK)
    d.text((34, 148), "TUESDAY, NOVEMBER 24, 2026",
           font=font(SANS_B, 20), fill=ACCENT)
    d.text((990, 148), "No. 328  •  PRICE $2.50", font=font(SANS_B, 16),
           fill=MUTED, anchor="ra")
    rule(d, 34, 180, 956, 1)

    # ---- LEAD: markets / tech ----
    y = 196
    y = kicker(d, 34, y, "MARKETS  •  TECHNOLOGY")
    y = headline(d, 34, y, "Tech rally lifts Nasdaq 1.4% as chip stocks",
                 font(SERIF_B, 40), 640, 46)
    y = headline(d, 34, y, "surge on AI spending plans",
                 font(SERIF_B, 40), 640, 46)
    y = para(d, 34, y + 6,
             "The S&P 500 closed at a record high as investors bought "
             "chipmakers and cloud stocks after big technology firms "
             "reaffirmed plans to keep raising AI infrastructure spending "
             "into 2027. Nvidia rose 3.2% and AMD gained 2.6%.",
             font(SERIF, 18), 640, 25)

    # mini bar chart: index moves
    cx, cy = 716, 210
    d.rectangle([cx - 6, cy - 6, 990, 452], outline=RULE, width=1)
    d.text((cx + 12, cy + 8), "TUESDAY'S MARKETS", font=font(SANS_B, 15),
           fill=INK)
    bars = [("Nasdaq", 1.4, BLUE), ("S&P 500", 0.9, BLUE),
            ("Dow", 0.6, BLUE), ("Nvidia", 3.2, ACCENT),
            ("AMD", 2.6, ACCENT)]
    bx = cx + 14
    for name, val, col in bars:
        bw = int(val * 38)
        d.text((bx, cy + 44), name, font=font(SANS, 14), fill=INK)
        d.rectangle([bx + 78, cy + 42, bx + 78 + bw, cy + 60], fill=col)
        d.text((bx + 84 + bw, cy + 44), "+%.1f%%" % val,
               font=font(SANS_B, 14), fill=INK)
        cy += 36
    d.text((cx + 12, 424), "S&P 500 at a record close.",
           font=font(SANS, 14), fill=MUTED)

    rule(d, 34, 470, 956, 2, INK)

    # ---- second row: politics (left) + climate (right) ----
    y = 488
    y = kicker(d, 34, y, "POLITICS")
    y = headline(d, 34, y, "UN council presses for Gaza aid surge as",
                 font(SERIF_B, 27), 460, 32)
    y = headline(d, 34, y, "ceasefire holds into second month",
                 font(SERIF_B, 27), 460, 32)
    y = para(d, 34, y + 6,
             "The UN Security Council met in New York on Tuesday to press "
             "for more food, fuel and medical aid into Gaza, where a "
             "ceasefire first agreed in October is holding into its second "
             "month. Aid agencies said convoys are moving but still fall "
             "short of daily needs.",
             font(SERIF, 17), 460, 24)

    y2 = 488
    y2 = kicker(d, 528, y2, "CLIMATE  •  ENERGY", color=GREEN)
    y2 = headline(d, 528, y2, "COP31 draft calls for tripling renewables",
                  font(SERIF_B, 27), 462, 32)
    y2 = headline(d, 528, y2, "by 2035 as talks enter final week",
                  font(SERIF_B, 27), 462, 32)
    y2 = para(d, 528, y2 + 6,
              "Negotiators at the COP31 climate talks in Antalya released "
              "a draft text on Tuesday urging countries to triple renewable "
              "energy capacity by 2035 and to set out new finance for "
              "adaptation. Ministers arrive this week for the final days "
              "of bargaining over who pays.",
              font(SERIF, 17), 462, 24)

    rule(d, 34, 780, 956, 2, INK)

    # ---- briefs ----
    y = 798
    d.text((34, y), "IN BRIEF", font=font(SANS_B, 15), fill=ACCENT)
    y = para(d, 34, y + 24,
             "Oil steadied near $63 a barrel as OPEC+ held output steady.  "
             "Gold held above $4,000 an ounce.  The Federal Reserve signalled "
             "a December rate cut is still on the table, while the European "
             "Central Bank held its key rate at 2.0%.",
             font(SERIF, 17), 956, 24)

    rule(d, 34, 872, 956, 2, INK)

    # ---- sports strip ----
    y = 890
    d.rectangle([34, 890, 990, 968], fill=BLUE)
    d.text((52, 902), "SPORT", font=font(SANS_B, 20), fill=(255, 255, 255))
    d.text((140, 904),
           "Arsenal stay top of the Premier League; Liverpool held 1-1",
           font=font(SERIF_B, 19), fill=(255, 255, 255))
    d.text((52, 934),
           "Champions League returns tonight: PSG visit Madrid; "
           "Bayern host Chelsea.",
           font=font(SANS, 15), fill=(225, 232, 245))

    d.text((512, 984), "The Daily Globe  •  Tuesday, November 24, 2026  •  "
           "All times local", font=font(SANS, 13), fill=MUTED, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
