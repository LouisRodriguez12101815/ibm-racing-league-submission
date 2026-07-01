#!/usr/bin/env python3
"""Generate the FINN-ISH LINE F1 livery reference sheet.

Outputs assets/mdc_racing_livery.jpg (same filename kept for URL stability with
the pre-uploaded S3 object). The livery is a print-ready reference sheet:
- Big team name and university identifier
- Stylized F1 car side profile in the team colors (navy + gold + white)
- Color palette swatches with hex codes
- IBM AI Racing League badge and design metadata

Usage:
    python scripts/generate_livery.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 1600
NAVY_DEEP = (6, 20, 56)
NAVY = (10, 32, 84)
NAVY_LIGHT = (26, 60, 130)
GOLD = (255, 205, 40)
GOLD_DEEP = (200, 155, 20)
WHITE = (255, 255, 255)
SOFT_WHITE = (235, 235, 245)
GREY = (170, 175, 190)
CHARCOAL = (20, 22, 30)

OUT_PATH = Path(__file__).resolve().parent.parent / "assets" / "mdc_racing_livery.jpg"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates_bold = [
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
    ]
    candidates_regular = [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in (candidates_bold if bold else candidates_regular):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def make_base() -> Image.Image:
    """Navy gradient background with gold accent bars."""
    img = Image.new("RGB", (W, H), NAVY_DEEP)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(NAVY_DEEP[0] + (NAVY[0] - NAVY_DEEP[0]) * t)
        g = int(NAVY_DEEP[1] + (NAVY[1] - NAVY_DEEP[1]) * t)
        b = int(NAVY_DEEP[2] + (NAVY[2] - NAVY_DEEP[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    # thick gold bars
    draw.rectangle([(0, 0), (W, 20)], fill=GOLD)
    draw.rectangle([(0, H - 20), (W, H)], fill=GOLD)
    # side gold accents
    draw.rectangle([(0, 0), (14, H)], fill=GOLD)
    draw.rectangle([(W - 14, 0), (W, H)], fill=GOLD)
    return img


def draw_centered(img: Image.Image, text: str, y: int, font: ImageFont.FreeTypeFont, fill=WHITE):
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, font=font, fill=fill)


def draw_left(img: Image.Image, text: str, x: int, y: int, font: ImageFont.FreeTypeFont, fill=WHITE):
    ImageDraw.Draw(img).text((x, y), text, font=font, fill=fill)


def draw_car(img: Image.Image, cx: int, cy: int, scale: float = 1.0) -> None:
    """Draw a stylized F1 side-profile at (cx, cy) center.

    Composed of primitives: floor, sidepod, cockpit + halo, nose, front and
    rear wings, plus two wheels. Livery colors: NAVY body, GOLD accent stripe,
    WHITE text zones. Purely decorative — not a technical drawing.
    """
    draw = ImageDraw.Draw(img)
    s = scale

    def sx(v: float) -> int:
        return int(cx + v * s)

    def sy(v: float) -> int:
        return int(cy + v * s)

    # rear wing (endplate + main plane)
    draw.polygon(
        [
            (sx(-780), sy(-90)),
            (sx(-620), sy(-90)),
            (sx(-620), sy(-160)),
            (sx(-720), sy(-160)),
            (sx(-720), sy(-30)),
            (sx(-780), sy(-30)),
        ],
        fill=NAVY_LIGHT,
        outline=GOLD,
        width=3,
    )
    # rear wing top plane accent
    draw.rectangle([(sx(-770), sy(-150)), (sx(-630), sy(-135))], fill=GOLD)

    # main body: floor + sidepod hump
    body_pts = [
        (sx(-620), sy(20)),          # rear-bottom
        (sx(-620), sy(-40)),         # rear-top
        (sx(-350), sy(-140)),        # sidepod top rear
        (sx(-50), sy(-160)),         # sidepod top peak
        (sx(150), sy(-135)),         # nose base top
        (sx(600), sy(-40)),          # nose tip top
        (sx(720), sy(-15)),          # nose tip
        (sx(600), sy(30)),           # nose bottom
        (sx(-620), sy(30)),          # floor rear
    ]
    draw.polygon(body_pts, fill=NAVY, outline=GOLD, width=4)

    # gold accent stripe along the sidepod
    draw.polygon(
        [
            (sx(-340), sy(-95)),
            (sx(-40), sy(-115)),
            (sx(200), sy(-90)),
            (sx(200), sy(-60)),
            (sx(-40), sy(-85)),
            (sx(-340), sy(-65)),
        ],
        fill=GOLD,
    )

    # cockpit halo
    draw.arc(
        [(sx(-260), sy(-260)), (sx(-40), sy(-140))],
        start=200,
        end=340,
        fill=CHARCOAL,
        width=int(14 * s),
    )
    # cockpit opening / driver headrest
    draw.rectangle([(sx(-260), sy(-170)), (sx(-40), sy(-140))], fill=CHARCOAL)

    # airbox behind cockpit
    draw.polygon(
        [
            (sx(-380), sy(-150)),
            (sx(-260), sy(-220)),
            (sx(-260), sy(-140)),
            (sx(-380), sy(-140)),
        ],
        fill=NAVY_LIGHT,
        outline=GOLD,
        width=2,
    )

    # front wing (endplate + planes)
    draw.polygon(
        [
            (sx(600), sy(30)),
            (sx(760), sy(30)),
            (sx(820), sy(60)),
            (sx(560), sy(60)),
        ],
        fill=NAVY_LIGHT,
        outline=GOLD,
        width=3,
    )
    draw.rectangle([(sx(560), sy(48)), (sx(820), sy(58))], fill=GOLD)

    # wheels (rear + front)
    for wheel_x in (sx(-520), sx(430)):
        # tire
        draw.ellipse(
            [(wheel_x - int(130 * s), sy(-40)), (wheel_x + int(130 * s), sy(220))],
            fill=CHARCOAL,
            outline=GOLD,
            width=4,
        )
        # rim
        draw.ellipse(
            [(wheel_x - int(70 * s), sy(30)), (wheel_x + int(70 * s), sy(170))],
            fill=NAVY_LIGHT,
            outline=GOLD,
            width=3,
        )
        # center cap
        draw.ellipse(
            [(wheel_x - int(20 * s), sy(80)), (wheel_x + int(20 * s), sy(120))],
            fill=GOLD,
        )

    # team name on the sidepod
    sidepod_font = load_font(int(58 * s), bold=True)
    tag_font = load_font(int(28 * s), bold=True)
    draw.text((sx(-320), sy(-58)), "FINN-ISH LINE", font=sidepod_font, fill=WHITE)
    draw.text((sx(-320), sy(0)), "MIAMI DADE COLLEGE", font=tag_font, fill=SOFT_WHITE)

    # #01 on the nose
    number_font = load_font(int(100 * s), bold=True)
    draw.text((sx(350), sy(-105)), "01", font=number_font, fill=GOLD)


def swatch(img: Image.Image, x: int, y: int, w: int, h: int, color, label: str, hex_code: str) -> None:
    draw = ImageDraw.Draw(img)
    draw.rectangle([(x, y), (x + w, y + h)], fill=color, outline=GOLD, width=3)
    label_font = load_font(28, bold=True)
    hex_font = load_font(26, bold=False)
    draw.text((x, y + h + 12), label, font=label_font, fill=WHITE)
    draw.text((x, y + h + 50), hex_code, font=hex_font, fill=GREY)


def main() -> int:
    img = make_base()

    # header
    tag_font = load_font(34, bold=True)
    draw_left(img, "FINN-ISH LINE  ·  IBM AI RACING LEAGUE 2026", 60, 46, tag_font, fill=SOFT_WHITE)
    draw_left(img, "F1 LIVERY REFERENCE  ·  DESIGN #01", W - 720, 46, tag_font, fill=SOFT_WHITE)

    # main title
    title_font = load_font(180, bold=True)
    sub_font = load_font(58, bold=False)
    draw_centered(img, "FINN-ISH LINE", 140, title_font, fill=GOLD)
    draw_centered(img, "Miami Dade College  ·  AI Models  ·  IBM F1", 340, sub_font, fill=SOFT_WHITE)

    # car
    draw_car(img, cx=W // 2, cy=780, scale=1.05)

    # palette swatches
    palette_y = 1120
    swatch_w = 240
    swatch_h = 140
    gap = 60
    total_w = 4 * swatch_w + 3 * gap
    start_x = (W - total_w) // 2
    swatch(img, start_x + 0 * (swatch_w + gap), palette_y, swatch_w, swatch_h, NAVY, "DEEP NAVY", "#0A2054")
    swatch(img, start_x + 1 * (swatch_w + gap), palette_y, swatch_w, swatch_h, NAVY_LIGHT, "RACE BLUE", "#1A3C82")
    swatch(img, start_x + 2 * (swatch_w + gap), palette_y, swatch_w, swatch_h, GOLD, "TROPHY GOLD", "#FFCD28")
    swatch(img, start_x + 3 * (swatch_w + gap), palette_y, swatch_w, swatch_h, WHITE, "SHARK WHITE", "#FFFFFF")

    # footer
    footer_font = load_font(32, bold=False)
    draw_centered(
        img,
        "Louis Rodriguez  ·  Daniel Pino  ·  Javier Perez-Hickman  ·  2026-07-01",
        1470,
        footer_font,
        fill=SOFT_WHITE,
    )

    img = img.convert("RGB")
    img.save(OUT_PATH, "JPEG", quality=92, optimize=True)
    print(f"wrote {OUT_PATH}  ({OUT_PATH.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
