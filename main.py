"""Front page for Tuesday 17 November 2026.

Draws a newspaper front page (1024x1024 PNG) summing up the day's world
news: a masthead, a red date band, six story panels in three rows, and a
ticker strip. Everything is drawn procedurally with PIL; no network, no
randomness, so two runs write byte-identical output.

Stories (all reported on 17 November 2026):
  1. Kerch Bridge span falls after a Ukrainian strike.
  2. Iranian drones target a US radar base in Bahrain; all intercepted.
  3. China confirms a Xi-Putin-Trump meeting at APEC in Shenzhen.
  4. Five EU states plan a Rwanda return hub for migrants.
  5. The US tightens its AI chip export ban on China.
  6. Japan scrambles jets after Russian aircraft enter its airspace.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 229)
INK = (24, 24, 24)
NAVY = (20, 38, 77)
RED = (163, 18, 30)
GOLD = (198, 158, 62)
WHITE = (255, 255, 255)
SKY = (207, 227, 238)
WATER = (43, 108, 176)
STEEL = (58, 58, 58)
DUSK = (44, 62, 87)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu face; fall back to PIL's built-in font."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, text, fnt):
    """Pixel width of a string in a font."""
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centred(draw, cx, y, text, fnt, fill):
    """Draw text centred on x=cx at height y."""
    w = text_w(draw, text, fnt)
    draw.text((cx - w // 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def left(draw, x, y, text, fnt, fill):
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + fnt.size


def panel(draw, x0, y0, x1, y1):
    """A white story panel with a thin rule border."""
    draw.rectangle([x0, y0, x1, y1], fill=WHITE, outline=(120, 110, 95), width=2)


def headline(draw, x, y, w, text, fnt, fill=INK, max_lines=2):
    """Wrapped headline; returns the y just below it."""
    lines = wrap(draw, text, fnt, w)[:max_lines]
    for line in lines:
        y = left(draw, x, y, line, fnt, fill)
    return y


def subline(draw, x, y, w, text, fnt, fill=(70, 70, 70), max_lines=2):
    lines = wrap(draw, text, fnt, w)[:max_lines]
    for line in lines:
        y = left(draw, x, y, line, fnt, fill)
    return y


# ---------------------------------------------------------------------------
# Illustrations: each draws one story scene inside a box (x0, y0, x1, y1).
# ---------------------------------------------------------------------------

def draw_bridge(draw, x0, y0, x1, y1):
    """Kerch Bridge: a deck with its middle span dropped into the strait."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # sun and clouds
    draw.ellipse([x1 - 90, y0 + 14, x1 - 38, y0 + 66], fill=(250, 214, 120))
    for cx in (x0 + 60, x0 + 190):
        draw.ellipse([cx, y0 + 30, cx + 90, y0 + 58], fill=WHITE)
    # water
    wy = y1 - 64
    draw.rectangle([x0, wy, x1, y1], fill=WATER)
    for wx in range(x0 + 8, x1 - 20, 44):
        draw.arc([wx, wy + 12, wx + 36, wy + 40], 180, 360, fill=WHITE, width=3)
    # bridge deck: left segment and right segment, a gap in the middle
    deck_y = y0 + 118
    mid = (x0 + x1) // 2
    draw.rectangle([x0, deck_y, mid - 52, deck_y + 14], fill=STEEL)
    draw.rectangle([mid + 66, deck_y, x1, deck_y + 14], fill=STEEL)
    # road dashes on the two deck pieces
    for dx in range(x0 + 12, mid - 60, 30):
        draw.rectangle([dx, deck_y + 5, dx + 16, deck_y + 9], fill=(240, 200, 60))
    for dx in range(mid + 76, x1 - 16, 30):
        draw.rectangle([dx, deck_y + 5, dx + 16, deck_y + 9], fill=(240, 200, 60))
    # standing arch on the left piece
    draw.arc([x0 + 40, deck_y - 62, x0 + 200, deck_y + 30], 180, 360, fill=STEEL, width=6)
    # fallen span: a deck plank sliding into the gap, half under water
    draw.polygon(
        [(mid - 56, deck_y + 4), (mid - 30, deck_y + 4),
         (mid + 6, wy + 30), (mid - 20, wy + 30)],
        fill=(96, 96, 96),
    )
    # yellow dashes along the fallen plank, so it reads as road deck
    for t in (0.25, 0.5, 0.75):
        px = int((mid - 43) + t * 36)
        py = int((deck_y + 4) + t * 26)
        draw.ellipse([px - 4, py - 3, px + 4, py + 3], fill=(240, 200, 60))
    # broken arch stub still attached to the left deck
    draw.arc([mid - 70, deck_y - 40, mid + 10, deck_y + 30], 250, 340, fill=(96, 96, 96), width=6)
    # blast starburst at the gap
    bx, by = mid + 8, deck_y - 6
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 10, 26
        a = math.radians(ang)
        x_a, y_a = bx + r1 * math.cos(a), by + r1 * math.sin(a)
        x_b, y_b = bx + r2 * math.cos(a), by + r2 * math.sin(a)
        draw.line([x_a, y_a, x_b, y_b], fill=(255, 170, 30), width=5)
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 200, 60))


def draw_drone_base(draw, x0, y0, x1, y1):
    """Bahrain: a radar dish, an incoming drone, and an interception burst."""
    draw.rectangle([x0, y0, x1, y1], fill=DUSK)
    # stars
    for sx, sy in [(30, 18), (120, 34), (210, 14), (300, 40), (380, 20), (450, 30)]:
        draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 4, y0 + sy + 4], fill=WHITE)
    # ground
    gy = y1 - 26
    draw.rectangle([x0, gy, x1, y1], fill=(30, 40, 30))
    # radar dish on a mast, left side: a bright white bowl on a thick mast
    mx = x0 + 86
    draw.rectangle([mx - 5, gy - 66, mx + 5, gy], fill=(200, 200, 200))
    draw.pieslice([mx - 58, gy - 128, mx + 58, gy - 48], 0, 180, fill=WHITE)
    draw.ellipse([mx - 6, gy - 96, mx + 6, gy - 84], fill=(255, 200, 60))
    draw.line([mx, gy - 90, mx, gy - 66], fill=(200, 200, 200), width=3)
    # drone: body, arms, rotors, upper right
    dx, dy = x1 - 150, y0 + 42
    draw.ellipse([dx - 26, dy - 10, dx + 26, dy + 10], fill=(30, 30, 30))
    draw.line([dx - 40, dy - 16, dx + 40, dy - 16], fill=(30, 30, 30), width=4)
    draw.line([dx - 40, dy + 14, dx + 40, dy + 14], fill=(30, 30, 30), width=4)
    for rx in (dx - 44, dx + 44):
        draw.ellipse([rx - 16, dy - 26, rx + 16, dy - 6], outline=(200, 200, 200), width=3)
        draw.ellipse([rx - 16, dy + 4, rx + 16, dy + 24], outline=(200, 200, 200), width=3)
    # interception burst between dish and drone
    bx, by = (x0 + x1) // 2, y0 + 58
    for dx2, dy2 in [(-18, 0), (18, 0), (0, -18), (0, 18), (-13, -13), (13, -13), (-13, 13), (13, 13)]:
        draw.line([bx, by, bx + dx2 * 2, by + dy2 * 2], fill=(255, 200, 60), width=4)
    draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=(255, 220, 90))


def draw_flags(draw, x0, y0, x1, y1):
    """Three leaders: the flags of China, Russia and the United States."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 236, 228))
    fw = (x1 - x0 - 80) // 3
    fh = 84
    top = y0 + 18
    # China: red field, one big yellow star and four small ones
    cx = x0 + 26
    draw.rectangle([cx, top, cx + fw, top + fh], fill=(222, 41, 16))
    draw.ellipse([cx + 12, top + 12, cx + 34, top + 34], fill=(255, 222, 0))
    for sx, sy in [(cx + 44, top + 10), (cx + 52, top + 24), (cx + 48, top + 40), (cx + 36, top + 48)]:
        draw.ellipse([sx, sy, sx + 8, sy + 8], fill=(255, 222, 0))
    # Russia: white, blue, red horizontal bands
    rx = cx + fw + 14
    draw.rectangle([rx, top, rx + fw, top + fh // 3], fill=WHITE)
    draw.rectangle([rx, top + fh // 3, rx + fw, top + 2 * fh // 3], fill=(0, 57, 166))
    draw.rectangle([rx, top + 2 * fh // 3, rx + fw, top + fh], fill=(213, 0, 50))
    draw.rectangle([rx, top, rx + fw, top + fh], outline=(120, 120, 120), width=1)
    # United States: stripes and a blue canton with dots
    ux = rx + fw + 14
    for i in range(7):
        col = (179, 25, 66) if i % 2 == 0 else WHITE
        draw.rectangle([ux, top + i * fh // 7, ux + fw, top + (i + 1) * fh // 7], fill=col)
    draw.rectangle([ux, top, ux + fw * 2 // 5, top + 4 * fh // 7], fill=(10, 49, 97))
    for gx in range(3):
        for gy in range(2):
            draw.ellipse(
                [ux + 8 + gx * 16, top + 8 + gy * 16, ux + 14 + gx * 16, top + 14 + gy * 16],
                fill=WHITE,
            )
    draw.rectangle([ux, top, ux + fw, top + fh], outline=(120, 120, 120), width=1)


def draw_eu_rwanda(draw, x0, y0, x1, y1):
    """EU return hub: the EU stars, an arrow, and a green Rwanda marker."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 236, 228))
    # EU flag: blue field, ring of yellow stars
    ex, ey, ew, eh = x0 + 18, y0 + 16, 96, 64
    draw.rectangle([ex, ey, ex + ew, ey + eh], fill=(0, 51, 153))
    import math
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = ex + ew // 2 + int(26 * math.cos(a)) - 3
        sy = ey + eh // 2 + int(20 * math.sin(a)) - 3
        draw.ellipse([sx, sy, sx + 6, sy + 6], fill=(255, 204, 0))
    # arrow to the right
    ay = ey + eh // 2
    draw.line([ex + ew + 8, ay, x1 - 96, ay], fill=INK, width=5)
    draw.polygon(
        [(x1 - 96, ay - 10), (x1 - 96, ay + 10), (x1 - 78, ay)],
        fill=INK,
    )
    # green landmass with a pin, labelled RWANDA
    lx = x1 - 74
    draw.polygon(
        [(lx, y0 + 22), (lx + 56, y0 + 14), (lx + 62, y0 + 58),
         (lx + 34, y0 + 84), (lx + 6, y0 + 60)],
        fill=(34, 139, 34),
    )
    draw.ellipse([lx + 22, y0 + 26, lx + 40, y0 + 44], fill=(200, 30, 30))
    draw.polygon([(lx + 31, y0 + 44), (lx + 26, y0 + 58), (lx + 36, y0 + 58)], fill=(200, 30, 30))
    centred(draw, (x0 + x1) // 2, y1 - 26, "RWANDA", SANS_BOLD(18), INK)


def draw_chip(draw, x0, y0, x1, y1):
    """AI chip ban: a chip under a red prohibition sign."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 236, 228))
    cx, cy = (x0 + x1) // 2, y0 + 52
    # pins
    for px in range(cx - 36, cx + 40, 16):
        draw.line([px, cy - 52, px, cy - 38], fill=(180, 140, 40), width=4)
        draw.line([px, cy + 38, px, cy + 52], fill=(180, 140, 40), width=4)
    for py in range(cy - 36, cy + 40, 16):
        draw.line([cx - 52, py, cx - 38, py], fill=(180, 140, 40), width=4)
        draw.line([cx + 38, py, cx + 52, py], fill=(180, 140, 40), width=4)
    # chip body
    draw.rectangle([cx - 38, cy - 38, cx + 38, cy + 38], fill=(30, 34, 44))
    draw.rectangle([cx - 38, cy - 38, cx + 38, cy + 38], outline=(120, 120, 120), width=2)
    centred(draw, cx, cy - 13, "AI", SANS_BOLD(26), WHITE)
    # red prohibition ring and slash
    draw.ellipse([cx - 58, cy - 58, cx + 58, cy + 58], outline=(200, 20, 30), width=8)
    draw.line([cx - 42, cy + 42, cx + 42, cy - 42], fill=(200, 20, 30), width=8)


def draw_jets(draw, x0, y0, x1, y1):
    """Japan scrambles jets: a red sun and a fighter climbing past it."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # rising sun
    sx, sy = x0 + 52, y0 + 44
    draw.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=(188, 0, 45))
    # clouds
    for cx in (x0 + 150, x0 + 240):
        draw.ellipse([cx, y1 - 34, cx + 70, y1 - 12], fill=WHITE)
    # fighter jet: fuselage, swept wings, tail, nose
    jx, jy = x0 + 150, y0 + 62
    draw.polygon(
        [(jx, jy - 6), (jx + 118, jy + 2), (jx, jy + 10)],
        fill=(52, 58, 64),
    )
    draw.polygon(
        [(jx + 46, jy - 4), (jx + 78, jy - 30), (jx + 96, jy - 28), (jx + 70, jy - 2)],
        fill=(52, 58, 64),
    )
    draw.polygon(
        [(jx + 46, jy + 8), (jx + 74, jy + 30), (jx + 92, jy + 28), (jx + 68, jy + 8)],
        fill=(52, 58, 64),
    )
    draw.polygon(
        [(jx + 8, jy - 4), (jx + 26, jy - 22), (jx + 34, jy - 20), (jx + 22, jy - 2)],
        fill=(52, 58, 64),
    )
    # contrail
    draw.line([jx - 6, jy + 2, x0 + 30, jy + 22], fill=WHITE, width=4)
    # small second jet, higher and smaller
    kx, ky = x0 + 210, y0 + 16
    draw.polygon([(kx, ky - 3), (kx + 52, ky + 1), (kx, ky + 5)], fill=(90, 96, 102))


# ---------------------------------------------------------------------------
# Page assembly
# ---------------------------------------------------------------------------

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 80], fill=NAVY)
    centred(d, W // 2, 12, "THE WORLD TODAY", SERIF_BOLD(52), WHITE)
    d.rectangle([0, 80, W, 84], fill=GOLD)

    # Date band
    d.rectangle([0, 84, W, 128], fill=RED)
    centred(d, W // 2, 94, "TUESDAY, 17 NOVEMBER 2026", SANS_BOLD(30), WHITE)

    # ---- Top story: Kerch Bridge (full width) ----
    panel(d, 20, 140, 1004, 396)
    draw_bridge(d, 36, 152, 436, 384)
    tx = 460
    y = 168
    y = headline(d, tx, y, 520, "KERCH BRIDGE SPAN FALLS", SANS_BOLD(36))
    y += 6
    y = subline(d, tx, y, 520, "Ukraine strike drops the 227m road arch into the strait; road and rail halted.", SANS(21))
    y += 10
    y = subline(d, tx, y, 520, "Second strike in two days on the Crimea link.", SANS(21))

    # ---- Middle row: two panels ----
    # Iran / Bahrain
    panel(d, 20, 408, 500, 648)
    draw_drone_base(d, 32, 420, 488, 540)
    y = 552
    y = headline(d, 36, y, 448, "IRAN DRONES TARGET BAHRAIN BASE", SANS_BOLD(24))
    y += 4
    y = subline(d, 36, y, 448, "US radar attacked; Bahrain intercepts all drones, no damage.", SANS(17))
    # Trilateral
    panel(d, 524, 408, 1004, 648)
    draw_flags(d, 536, 420, 992, 540)
    y = 552
    y = headline(d, 540, y, 448, "CHINA CONFIRMS XI\u2013PUTIN\u2013TRUMP TALKS", SANS_BOLD(24))
    y += 4
    y = subline(d, 540, y, 448, "Three leaders to meet Thursday at APEC in Shenzhen.", SANS(17))

    # ---- Bottom row: three panels ----
    # EU Rwanda
    panel(d, 20, 660, 336, 936)
    draw_eu_rwanda(d, 32, 672, 324, 800)
    y = 812
    y = headline(d, 32, y, 292, "FIVE EU STATES PLAN RWANDA MIGRANT HUB", SANS_BOLD(20))
    y += 4
    y = subline(d, 32, y, 292, "Rejected asylum seekers to a return hub; transfers from 2027.", SANS(15))
    # Chip ban
    panel(d, 352, 660, 668, 936)
    draw_chip(d, 364, 672, 656, 800)
    y = 812
    y = headline(d, 364, y, 292, "US TIGHTENS AI CHIP BAN ON CHINA", SANS_BOLD(20))
    y += 4
    y = subline(d, 364, y, 292, "Export loophole closed; Nvidia in focus ahead of earnings.", SANS(15))
    # Japan jets
    panel(d, 684, 660, 1004, 936)
    draw_jets(d, 696, 672, 992, 800)
    y = 812
    y = headline(d, 696, y, 292, "JAPAN SCRAMBLES FIGHTER JETS", SANS_BOLD(20))
    y += 4
    y = subline(d, 696, y, 292, "Two Russian jets enter airspace; Tokyo protests.", SANS(15))

    # ---- Ticker strip ----
    d.rectangle([0, 948, W, H], fill=NAVY)
    centred(d, W // 2, 960, "ALSO: US loses measles-free status after nearly 30 years  \u2022  Trump meets Quad leaders in Manila", SANS(19), (255, 220, 130))
    centred(d, W // 2, 988, "COP31 climate talks enter decisive stage in Antalya", SANS(19), (255, 220, 130))

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
