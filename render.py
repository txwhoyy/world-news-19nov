#!/usr/bin/env python3
"""Render 'The World Today' — a 1024x1024 newspaper front page summing up
Thursday 19 November 2026. Deterministic: fixed fonts, fixed layout, no
network, no randomness, no timestamps. Run: python3 render.py -> entry.png
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 234)
INK = (24, 24, 24)
RED = (163, 30, 34)
MUTED = (96, 90, 80)
RULE = (60, 56, 48)
BLUE = (38, 68, 110)
TEAL = (24, 110, 110)
GOLD = (176, 132, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, text, size=13):
    f = font(SANS_B, size)
    draw.text((x, y), text.upper(), font=f, fill=RED)
    return y + size + 8


def source_line(draw, x, y, text, size=11):
    f = font(SANS, size)
    draw.text((x, y), "Source: " + text, font=f, fill=MUTED)
    return y + size + 4


def hrule(draw, x0, x1, y, width=2, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- illustrations
def ill_skyline(d, x, y, w, h):
    """Shenzhen at dusk: sky gradient bands, tower silhouettes, three flags."""
    sky = [(52, 74, 110), (70, 96, 132), (96, 124, 148)]
    for i in range(h):
        t = i / max(h - 1, 1)
        c = sky[min(2, int(t * 3))]
        d.line([(x, y + i), (x + w, y + i)], fill=c)
    # sun
    d.ellipse([x + w - 92, y + 26, x + w - 44, y + 74], fill=(232, 190, 90))
    # towers
    import random as _r  # fixed seed -> deterministic
    rng = _r.Random(1911)
    bx = x + 8
    while bx < x + w - 30:
        tw = rng.randint(26, 52)
        th = rng.randint(int(h * 0.35), int(h * 0.78))
        d.rectangle([bx, y + h - th, bx + tw, y + h], fill=(28, 34, 48))
        for wy in range(y + h - th + 10, y + h - 8, 16):
            for wx in range(bx + 5, bx + tw - 4, 11):
                if rng.random() < 0.45:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(240, 200, 90))
        bx += tw + rng.randint(4, 14)
    # ground band
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(18, 22, 32))
    # three flags on poles in the foreground
    flags = [
        [(200, 40, 40), (255, 255, 255), (40, 60, 140)],  # USA-ish stripes
        [(222, 40, 40)],                                    # China red
        [(255, 255, 255), (40, 90, 180), (200, 40, 40)],  # Russia tricolour
    ]
    fx = x + 24
    for bands in flags:
        d.line([(fx, y + h - 96), (fx, y + h - 14)], fill=(230, 230, 220), width=3)
        fh = 44
        bh = fh // len(bands)
        for i, col in enumerate(bands):
            d.rectangle([fx, y + h - 96 - fh + i * bh, fx + 62, y + h - 96 - fh + (i + 1) * bh], fill=col)
        if len(bands) == 1:
            for sx, sy in [(fx + 10, y + h - 96 - fh + 8), (fx + 24, y + h - 96 - fh + 6),
                           (fx + 36, y + h - 96 - fh + 12), (fx + 16, y + h - 96 - fh + 20)]:
                d.ellipse([sx, sy, sx + 5, sy + 5], fill=(250, 220, 60))
        fx += 108


def ill_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 206, 188))
    d.rectangle([x, y, x + w, y + 26], fill=(176, 164, 140))
    d.polygon([(x + 12, y + 26), (x + w // 2, y + 2), (x + w - 12, y + 26)], fill=(96, 84, 66))
    d.ellipse([x + w // 2 - 9, y + 8, x + w // 2 + 9, y + 26], fill=(214, 206, 188))
    for i in range(5):
        cx = x + 22 + i * ((w - 44) // 4)
        d.rectangle([cx - 8, y + 30, cx + 8, y + h - 30], fill=(238, 232, 216))
        d.rectangle([cx - 12, y + 26, cx + 12, y + 32], fill=(238, 232, 216))
        d.rectangle([cx - 12, y + h - 36, cx + 12, y + h - 30], fill=(238, 232, 216))
    d.rectangle([x, y + h - 30, x + w, y + h - 22], fill=(96, 84, 66))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(140, 130, 110))
    # scales of justice, small, centred above the base
    cx, cy = x + w // 2, y + h - 96
    d.line([(cx, cy - 26), (cx, cy + 22)], fill=INK, width=3)
    d.line([(cx - 34, cy - 22), (cx + 34, cy - 22)], fill=INK, width=3)
    for sx in (cx - 34, cx + 34):
        d.line([(sx, cy - 22), (sx, cy + 2)], fill=INK, width=2)
        d.polygon([(sx - 14, cy + 2), (sx + 14, cy + 2), (sx, cy + 18)], fill=GOLD)
    d.ellipse([cx - 5, cy - 32, cx + 5, cy - 22], fill=GOLD)


def ill_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 26, 44))
    bars = [0.30, 0.42, 0.38, 0.55, 0.52, 0.72, 0.88]
    bw = w // len(bars)
    for i, v in enumerate(bars):
        bh = int((h - 46) * v)
        d.rectangle([x + i * bw + 7, y + h - 24 - bh, x + (i + 1) * bw - 7, y + h - 24],
                    fill=(70, 160, 110) if i < len(bars) - 1 else (240, 200, 90))
    pts = [(x + i * bw + bw // 2, y + h - 24 - int((h - 46) * v)) for i, v in enumerate(bars)]
    d.line(pts, fill=(240, 200, 90), width=4, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))
    d.polygon([(pts[-1][0] - 2, pts[-1][1] - 16), (pts[-1][0] + 16, pts[-1][1] - 2),
               (pts[-1][0] - 2, pts[-1][1] + 2)], fill=(240, 200, 90))
    d.text((x + 12, y + 8), "$81bn", font=font(SANS_B, 26), fill=(255, 255, 255))


def ill_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 226))
    cx, cy = x + w // 2, y + h // 2 - 2
    for r, col in [(46, (255, 255, 255)), (36, (240, 244, 248)), (26, (255, 255, 255))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=560, fill=col, width=9)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(120, 150, 170))
    # rain streaks
    for i in range(14):
        rx = x + 10 + i * 13
        d.line([(rx, y + h - 34), (rx - 6, y + h - 18)], fill=(90, 130, 160), width=2)
    # coastline band
    d.polygon([(x, y + h - 8), (x + w * 0.42, y + h - 30), (x + w * 0.62, y + h - 12),
               (x + w, y + h - 26), (x + w, y + h), (x, y + h)], fill=(120, 150, 110))


def ill_road(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 206, 178))
    # buildings
    for bx, bh, col in [(8, 46, (150, 120, 90)), (52, 70, (130, 105, 80)),
                        (104, 54, (160, 130, 96))]:
        d.rectangle([x + bx, y + h - 40 - bh, x + bx + 40, y + h - 40], fill=col)
    # road with dashed centre line
    d.rectangle([x, y + h - 40, x + w, y + h], fill=(70, 70, 70))
    for dx in range(6, w - 8, 22):
        d.rectangle([x + dx, y + h - 22, x + dx + 12, y + h - 18], fill=(240, 220, 80))
    # yellow line marker
    d.line([(x, y + h - 40), (x + w, y + h - 40)], fill=(240, 220, 80), width=3)


def ill_flame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 34, 40))
    # building silhouette
    d.rectangle([x + 18, y + h - 62, x + w - 18, y + h - 12], fill=(90, 78, 70))
    for wy in range(y + h - 54, y + h - 16, 14):
        for wx in range(x + 26, x + w - 26, 16):
            d.rectangle([wx, wy, wx + 7, wy + 8], fill=(240, 200, 90))
    # flame
    cx = x + w // 2
    d.polygon([(cx - 34, y + h - 58), (cx - 12, y + h - 108), (cx, y + h - 78),
               (cx + 12, y + h - 116), (cx + 34, y + h - 58)],
              fill=(230, 90, 30))
    d.polygon([(cx - 18, y + h - 58), (cx - 6, y + h - 88), (cx + 4, y + h - 70),
               (cx + 18, y + h - 58)], fill=(250, 200, 60))


def ill_boat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(158, 196, 222))
    d.ellipse([x + w - 46, y + 10, x + w - 14, y + 42], fill=(250, 230, 140))
    # hull + sail
    d.polygon([(x + w // 2 - 52, y + 58), (x + w // 2 + 52, y + 58),
               (x + w // 2 + 34, y + 82), (x + w // 2 - 34, y + 82)], fill=(120, 70, 40))
    d.polygon([(x + w // 2, y + 14), (x + w // 2, y + 56), (x + w // 2 + 34, y + 56)],
              fill=(240, 240, 230))
    d.line([(x + w // 2, y + 12), (x + w // 2, y + 58)], fill=(60, 50, 40), width=3)
    for i, wy in enumerate((y + 88, y + 102, y + 116)):
        for k in range(3):
            d.arc([x + 8 + k * 60, wy - 8, x + 58 + k * 60, wy + 8],
                  start=180, end=360, fill=(255, 255, 255), width=3)


def ill_atom(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 34, 52))
    cx, cy = x + w // 2, y + h // 2
    for ang in (0, 60, 120):
        bbox = [cx - 62, cy - 26, cx + 62, cy + 26]
        d.arc(bbox, start=0, end=360, fill=(120, 190, 220), width=3)
        # rotate by drawing a second ellipse via polygon approximation
    # draw three rotated ellipses properly
    for ang in (0, 60, 120):
        pts = []
        for t in range(0, 361, 6):
            a = math.radians(t)
            ex, ey = 62 * math.cos(a), 26 * math.sin(a)
            r = math.radians(ang)
            pts.append((cx + ex * math.cos(r) - ey * math.sin(r),
                        cy + ex * math.sin(r) + ey * math.cos(r)))
        d.line(pts, fill=(120, 190, 220), width=3)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(240, 200, 90))
    for ox, oy in [(-52, -14), (52, 14), (0, 26)]:
        d.ellipse([cx + ox - 5, cy + oy - 5, cx + ox + 5, cy + oy + 5], fill=(255, 255, 255))


# ---------------------------------------------------------------- page build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    X1 = W - M

    # ---- masthead ----
    d.rectangle([M, 26, X1, 28], fill=RULE)
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 74)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 34), title, font=tf, fill=INK)
    d.text((M, 118), "ONE DAY · ONE PAGE · THE WORLD",
           font=font(SANS, 13), fill=MUTED)
    d.text((X1 - d.textlength("No. 323 · PRICE: FREE", font=font(SANS, 13)), 118),
           "No. 323 · PRICE: FREE", font=font(SANS, 13), fill=MUTED)
    df = font(SERIF_B, 30)
    date = "THURSDAY 19 NOVEMBER 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 142), date, font=df, fill=RED)
    hrule(d, M, X1, 182, 4)
    hrule(d, M, X1, 188, 1)

    # ---- lead story ----
    ly = 204
    ill_w, ill_h = 392, 280
    ill_skyline(d, M, ly, ill_w, ill_h)
    lx = M + ill_w + 22
    lw = X1 - lx
    y = ly
    y = kicker(d, lx, y, "Diplomacy · Shenzhen", 14)
    y = para(d, lx, y, "Trump, Xi and Putin meet in Shenzhen in first three-way summit",
             font(SERIF_B, 31), lw, 38)
    y += 6
    y = para(d, lx, y,
             "The leaders of the United States, China and Russia held their first "
             "three-way talks on the sidelines of the APEC forum, discussing nuclear "
             "arms control, Ukraine and Iran — but announced no major agreement.",
             font(SANS, 15), lw, 22)
    y += 8
    source_line(d, lx, y, "Associated Press · Reuters", 12)

    # ---- middle row: two stories ----
    my = ly + ill_h + 18
    hrule(d, M, X1, my - 8, 1)
    mid_h = 180
    col_w = (X1 - M - 24) // 2
    mid = [
        ("International Justice · The Hague", ill_court,
         "World court rules Myanmar committed genocide against the Rohingya",
         "The court found by 9–6 that Myanmar's forces killed about 10,000 "
         "Rohingya in the 2017 crackdown.",
         "Associated Press"),
        ("Business · New York", ill_chart,
         "Anthropic's $81bn debut is the biggest IPO in history",
         "Shares in the AI firm behind Claude begin trading on Nasdaq as ANT "
         "after pricing at $83.",
         "Reuters"),
    ]
    mid_bottom = my
    for i, (kick, ill, head, body, src) in enumerate(mid):
        cx = M + i * (col_w + 24)
        ill(d, cx, my, 168, 150)
        tx = cx + 182
        twd = cx + col_w - tx
        yy = my
        yy = kicker(d, tx, yy, kick, 12)
        yy = para(d, tx, yy, head, font(SERIF_B, 19), twd, 23)
        yy += 3
        yy = para(d, tx, yy, body, font(SANS, 13), twd, 18, max_lines=3)
        mid_bottom = max(mid_bottom, source_line(d, tx, yy + 4, src, 11))
    if len(mid) == 2:
        d.line([(M + col_w + 12, my), (M + col_w + 12, mid_bottom - 6)],
               fill=(200, 192, 176), width=1)

    # ---- bottom row: five stories ----
    by = max(mid_bottom, my + 160) + 16
    hrule(d, M, X1, by - 8, 1)
    bot = [
        ("Weather · India", ill_cyclone,
         "Cyclone Akvan nears India's east coast",
         "Due to cross the Andhra Pradesh–Odisha coast by noon on Friday, "
         "winds gusting to 110 km/h.",
         "India Meteorological Dept."),
        ("Conflict · Gaza", ill_road,
         "Israel ends ground raid across Gaza ceasefire line",
         "Israeli forces completed their operation near Bureij and Nuseirat, "
         "the first raid beyond the truce's 'Yellow Line'.",
         "Agence France-Presse · Reuters"),
        ("Politics · Dhaka", ill_flame,
         "Four killed as unrest grips Bangladesh",
         "An opposition shutdown brought renewed violence; the ancestral home "
         "of interim leader Muhammad Yunus was set on fire.",
         "Reuters"),
        ("Migration · Dakar", ill_boat,
         "Dozens missing after migrant boat capsizes off Senegal",
         "A boat carrying about 50 people bound for Europe capsized off Yenne, "
         "south of Dakar; dozens are missing.",
         "Reuters"),
        ("Security · Vienna", ill_atom,
         "IAEA warns North Korea is expanding uranium enrichment",
         "The UN nuclear watchdog reported further expansion at North Korea's "
         "enrichment facilities.",
         "IAEA · Al Jazeera"),
    ]
    bw = (X1 - M - 4 * 14) // 5
    for i, (kick, ill, head, body, src) in enumerate(bot):
        cx = M + i * (bw + 14)
        ill(d, cx, by, bw, 96)
        yy = by + 106
        yy = kicker(d, cx, yy, kick, 11)
        yy = para(d, cx, yy, head, font(SERIF_B, 15), bw, 18)
        yy += 2
        yy = para(d, cx, yy, body, font(SANS, 11), bw, 14, max_lines=4)
        source_line(d, cx, yy + 3, src, 10)
        if i < 4:
            d.line([(cx + bw + 7, by), (cx + bw + 7, by + 208)],
                   fill=(200, 192, 176), width=1)

    # ---- footer ----
    fy = H - 34
    hrule(d, M, X1, fy - 10, 1)
    foot = "The World Today · Thursday 19 November 2026 · All eight stories verified against reporting published on the day."
    ff = font(SANS, 11)
    d.text(((W - d.textlength(foot, font=ff)) / 2, fy), foot, font=ff, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
