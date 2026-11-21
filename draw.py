#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: a professional newspaper front page
summing up the world news of Friday 20 November 2026.

Renders entry.png (1024x1024) next to this script. Local authoring tool
only (uses Pillow); the submitted program is main.py, which copies the
finished PNG into the grader's output directory.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (24, 24, 28)
MUTED = (92, 90, 86)
RED = (178, 24, 32)
NAVY = (23, 48, 84)
GOLD = (184, 134, 42)
RULE = (58, 56, 52)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, s, f, x, y, max_w, fill, leading):
    for line in wrap(draw, s, f, max_w):
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, color=RULE, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")
M = 44  # page margin
RIGHT = W - M

# ---------------------------------------------------------------- masthead
y = 26
hrule(d, M, RIGHT, y, width=3)
y += 10
f_date = font(SANS_B, 19)
d.text((M, y), "FRIDAY, 20 NOVEMBER 2026", font=f_date, fill=INK)
r = "WORLD EDITION"
d.text((RIGHT - text_w(d, r, f_date), y), r, font=f_date, fill=INK)
y += 30
mast = "THE WORLD TODAY"
msize = 92
while text_w(d, mast, font(SERIF_B, msize)) > RIGHT - M - 8:
    msize -= 2
f_mast = font(SERIF_B, msize)
d.text(((W - text_w(d, mast, f_mast)) / 2, y), mast, font=f_mast, fill=INK)
y += 94
# date badge centred under the masthead
badge = "20 NOV 2026"
f_badge = font(SANS_B, 20)
bw = text_w(d, badge, f_badge) + 28
bx = (W - bw) / 2
d.rounded_rectangle([bx, y, bx + bw, y + 34], radius=6, fill=RED)
d.text((bx + 14, y + 5), badge, font=f_badge, fill=(255, 255, 255))
hrule(d, M, bx - 14, y + 17, width=2)
hrule(d, bx + bw + 14, RIGHT, y + 17, width=2)
y += 46
hrule(d, M, RIGHT, y, width=4)
hrule(d, M, RIGHT, y + 7, width=1)

# ---------------------------------------------------------------- lead head
ly = y + 20
f_kick = font(SANS_B, 18)
d.text((M, ly), "EUROPE  •  WAR IN UKRAINE", font=f_kick, fill=RED)
ly += 28
f_lead = font(SERIF_B, 42)
ly = draw_wrapped(d, "RUSSIA RAINS MISSILES AND DRONES ON KYIV IN MASS BARRAGE",
                  f_lead, M, ly, RIGHT - M, INK, 47)

# ---------------------------------------------------------------- lead art
# Night skyline panel: Kyiv under missile and drone attack.
ART_Y = ly + 8
ART_H = 168
ART_X1 = 640  # art panel spans M..ART_X1, text column to its right
sky_top, sky_bot = (16, 22, 48), (86, 52, 66)
for i in range(ART_H):
    t = i / ART_H
    c = tuple(int(sky_top[k] + (sky_bot[k] - sky_top[k]) * t) for k in range(3))
    d.line([(M, ART_Y + i), (ART_X1, ART_Y + i)], fill=c)

# stars
import random

rng = random.Random(20261120)
for _ in range(70):
    sx, sy = rng.uniform(M + 6, ART_X1 - 6), rng.uniform(ART_Y + 6, ART_Y + 120)
    d.ellipse([sx, sy, sx + 2, sy + 2], fill=(230, 230, 240))

# missile trails arcing down
for (x0, x1, peak) in [(120, 300, 60), (300, 430, 40), (480, 560, 80), (210, 250, 100)]:
    pts = []
    for t in range(0, 41):
        tt = t / 40
        px = x0 + (x1 - x0) * tt
        py = ART_Y + 18 + (ART_H - 90) * tt * tt + peak * math.sin(tt * math.pi) * 0.15
        pts.append((px, py))
    d.line(pts, fill=(255, 170, 80), width=3)
    d.line(pts[::3], fill=(255, 230, 180), width=1)
    ex, ey = pts[-1]
    for rr, col in [(26, (255, 120, 40, 90)), (16, (255, 170, 60, 140)), (8, (255, 220, 140, 220))]:
        d.ellipse([ex - rr, ey - rr, ex + rr, ey + rr], fill=col)

# skyline silhouettes + a bridge
base = ART_Y + ART_H
buildings = [(M, 90), (96, 140), (150, 80), (205, 165), (268, 105), (322, 150),
             (382, 88), (432, 128), (488, 96), (540, 142), (596, 84)]
for bx0, bh in buildings:
    d.rectangle([bx0, base - bh, bx0 + 52, base], fill=(10, 12, 24))
    for wy in range(base - bh + 10, base - 14, 16):
        for wx in range(bx0 + 8, bx0 + 46, 13):
            if rng.random() < 0.42:
                d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 205, 110))
# bridge deck across the lower third
d.rectangle([M, base - 44, ART_X1, base - 38], fill=(8, 10, 20))
for px in range(M + 20, ART_X1, 46):
    d.line([(px, base - 44), (px, base - 4)], fill=(8, 10, 20), width=4)
# river glow
d.rectangle([M, base - 6, ART_X1, base], fill=(38, 52, 92))
d.rectangle([M, ART_Y, ART_X1, base], outline=RULE, width=2)
f_cap = font(SANS, 15)
cap = "Kyiv under fire: missiles and drones rain on the capital overnight."
d.text((M + 2, base + 7), cap, font=f_cap, fill=MUTED)

# ---------------------------------------------------------------- lead text
TX = ART_X1 + 26
TW = RIGHT - TX
ty = ART_Y - 2
f_stand = font(SERIF, 17.5)
ty = draw_wrapped(d, "Strikes hit three Kyiv bridges and the capital's power and water "
                     "networks. Missiles and a drone crossed into Poland — NATO condemns "
                     "the 'provocative' attack.",
                  f_stand, TX, ty, TW, (40, 40, 44), 22)
ty += 10
# fact chips
f_chip = font(SANS_B, 16)
chips = ["9 KILLED", "3 BRIDGES HIT", "POLAND AIRSPACE BREACHED"]
cy = ty
for ch in chips:
    cw = text_w(d, ch, f_chip) + 20
    d.rounded_rectangle([TX, cy, TX + cw, cy + 30], radius=5, outline=RED, width=2)
    d.text((TX + 10, cy + 5), ch, font=f_chip, fill=RED)
    cy += 37

GRID_Y = max(base + 38, cy + 16)
hrule(d, M, RIGHT, GRID_Y - 14, width=2)

# ---------------------------------------------------------------- grid icons
def icon_chart(x, y, s):
    d.line([(x, y + s), (x + s * 0.35, y + s * 0.55), (x + s * 0.6, y + s * 0.72),
            (x + s, y + s * 0.15)], fill=RED, width=5)
    d.polygon([(x + s, y + s * 0.15), (x + s - 16, y + s * 0.12), (x + s - 4, y + s * 0.3)], fill=RED)


def icon_globe(x, y, s):
    d.ellipse([x, y, x + s, y + s], outline=NAVY, width=4)
    d.line([(x, y + s / 2), (x + s, y + s / 2)], fill=NAVY, width=3)
    d.arc([x + s * 0.22, y, x + s * 0.78, y + s], 90, 270, fill=NAVY, width=3)
    d.arc([x + s * 0.22, y, x + s * 0.78, y + s], 270, 90, fill=NAVY, width=3)


def icon_thermo(x, y, s):
    d.rounded_rectangle([x + s * 0.4, y, x + s * 0.6, y + s * 0.72], radius=8, outline=(196, 90, 20), width=4)
    d.ellipse([x + s * 0.28, y + s * 0.6, x + s * 0.72, y + s], outline=(196, 90, 20), width=4)
    d.rectangle([x + s * 0.46, y + s * 0.3, x + s * 0.54, y + s * 0.78], fill=(196, 90, 20))
    d.ellipse([x + s * 0.4, y + s * 0.68, x + s * 0.6, y + s * 0.88], fill=(196, 90, 20))


def icon_shield(x, y, s):
    d.polygon([(x + s / 2, y), (x + s, y + s * 0.18), (x + s, y + s * 0.55),
               (x + s / 2, y + s), (x, y + s * 0.55), (x, y + s * 0.18)],
              outline=(30, 110, 60), width=4)
    d.line([(x + s * 0.3, y + s * 0.5), (x + s * 0.46, y + s * 0.66), (x + s * 0.72, y + s * 0.34)],
           fill=(30, 110, 60), width=5)


def icon_quake(x, y, s):
    pts = [(x, y + s * 0.5), (x + s * 0.22, y + s * 0.5), (x + s * 0.34, y + s * 0.18),
           (x + s * 0.48, y + s * 0.82), (x + s * 0.6, y + s * 0.36), (x + s * 0.7, y + s * 0.5),
           (x + s, y + s * 0.5)]
    d.line(pts, fill=(120, 72, 20), width=5)


STORIES = [
    ("DIPLOMACY", NAVY, icon_globe,
     "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
     "Joint peace declaration; Berlin rejects any 'new Yalta' for Europe."),
    ("MARKETS", RED, icon_chart,
     "AI SELL-OFF WIPES 3.7% OFF THE S&P 500",
     "Global stocks slide as AI bubble fears spread; Asia falls further."),
    ("CLIMATE", (196, 90, 20), icon_thermo,
     "COP31 TALKS OVERRUN IN ANTALYA",
     "Summit misses Friday deadline; draft drops fossil-fuel language, no deal."),
    ("AMERICAS", (30, 110, 60), icon_shield,
     "MEXICO CAPTURES FBI MOST-WANTED CARTEL BOSS",
     "'El Chapo Isidro' seized in Sinaloa; violence follows the arrest."),
    ("DISASTER", (120, 72, 20), icon_quake,
     "6.8 QUAKE SHAKES PERU, CONGRESS EVACUATED",
     "Strong tremor in central Peru sends lawmakers into the streets."),
]

f_head = font(SERIF_B, 21.5)
f_body = font(SANS, 15.5)
COL_W = (RIGHT - M - 2 * 24) / 3
ROW_H = 160
positions = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)]
for (kick, col, icon, head, body), (cx, cyi) in zip(STORIES, positions):
    x = M + cx * (COL_W + 24)
    yy = GRID_Y + cyi * ROW_H
    if cx:
        d.line([(x - 12, yy + 4), (x - 12, yy + ROW_H - 18)], fill=(200, 196, 188), width=1)
    icon(x, yy + 2, 30)
    d.text((x + 40, yy + 6), kick, font=font(SANS_B, 17), fill=col)
    hy = draw_wrapped(d, head, f_head, x, yy + 42, COL_W, INK, 26)
    draw_wrapped(d, body, f_body, x, hy + 4, COL_W, (52, 52, 56), 19)

# last grid cell: "at a glance" numbers box
x = M + 2 * (COL_W + 24)
yy = GRID_Y + ROW_H
d.line([(x - 12, yy + 4), (x - 12, yy + ROW_H - 18)], fill=(200, 196, 188), width=1)
d.text((x, yy + 6), "THE DAY IN NUMBERS", font=font(SANS_B, 17), fill=GOLD)
f_num = font(SERIF_B, 26)
f_numl = font(SANS, 14.5)
nums = [("148", "drones launched at Ukraine"),
        ("-3.7%", "S&P 500 in the AI sell-off"),
        ("62-33", "US Senate passes energy bill")]
ny = yy + 40
for n, lab in nums:
    d.text((x, ny), n, font=f_num, fill=INK)
    draw_wrapped(d, lab, f_numl, x + 96, ny + 5, COL_W - 96, (52, 52, 56), 17)
    ny += 40

# ---------------------------------------------------------------- in brief
BRIEF_Y = GRID_Y + 2 * ROW_H + 2
d.rectangle([M, BRIEF_Y, RIGHT, BRIEF_Y + 62], fill=NAVY)
d.text((M + 14, BRIEF_Y + 8), "IN BRIEF", font=font(SANS_B, 16), fill=(255, 210, 90))
f_brief = font(SANS, 15.5)
brief = ("UK–EU leaders seal new ties at Brussels summit  •  ICJ: Myanmar responsible for "
         "Rohingya genocide  •  Israeli strike kills 3 in Gaza aid vehicle  •  Haiti police "
         "say 34 suspected gang members killed")
draw_wrapped(d, brief, f_brief, M + 14, BRIEF_Y + 27, RIGHT - M - 28, (240, 242, 248), 18)

# ---------------------------------------------------------------- footer
FY = BRIEF_Y + 72
hrule(d, M, RIGHT, FY, width=2)
f_foot = font(SANS, 14)
foot = "THE WORLD TODAY  •  Friday 20 November 2026  •  The day's world news on one page"
d.text(((W - text_w(d, foot, f_foot)) / 2, FY + 8), foot, font=f_foot, fill=MUTED)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
