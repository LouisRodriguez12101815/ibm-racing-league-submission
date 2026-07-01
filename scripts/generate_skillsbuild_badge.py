#!/usr/bin/env python3
"""Generate a SkillsBuild verification card as PNG.

This is a self-contained evidence card judges can view directly. It contains
the IBM verification URL as both a QR code and clickable text, plus team +
course metadata. Not a copy of the IBM-hosted badge — this is a submission
reference card that points to the real certificate.

Output: assets/skillsbuild-badge.png (1600x2000)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2000
NAVY_DEEP = (6, 20, 56)
NAVY = (10, 32, 84)
NAVY_LIGHT = (26, 60, 130)
GOLD = (255, 205, 40)
WHITE = (255, 255, 255)
SOFT_WHITE = (235, 235, 245)
GREY = (170, 175, 190)
IBM_BLUE = (15, 98, 254)

CERT_URL = (
    "https://skills.yourlearning.ibm.com/certificate/share/"
    "34b188b7f0ewogICJvYmplY3RUeXBlIiA6ICJBQ1RJVklUWSIsCiAgImxlYXJuZXJDTlVN"
    "IiA6ICIzNTg1NTA5UkVHIiwKICAib2JqZWN0SWQiIDogIkFMTS1DT1VSU0VfNDA1ODkxNCIKfQ"
    "21b3a5fd18-10"
)

OUT_PATH = Path(__file__).resolve().parent.parent / "assets" / "skillsbuild-badge.png"
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


def draw_centered(img: Image.Image, text: str, y: int, font: ImageFont.FreeTypeFont, fill=WHITE):
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, font=font, fill=fill)


def make_qr(url: str, box_size: int = 12) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def main() -> int:
    img = Image.new("RGB", (W, H), NAVY_DEEP)
    draw = ImageDraw.Draw(img)

    # gradient
    for y in range(H):
        t = y / H
        r = int(NAVY_DEEP[0] + (NAVY[0] - NAVY_DEEP[0]) * t)
        g = int(NAVY_DEEP[1] + (NAVY[1] - NAVY_DEEP[1]) * t)
        b = int(NAVY_DEEP[2] + (NAVY[2] - NAVY_DEEP[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # borders
    draw.rectangle([(0, 0), (W, 24)], fill=GOLD)
    draw.rectangle([(0, H - 24), (W, H)], fill=GOLD)
    draw.rectangle([(0, 0), (18, H)], fill=GOLD)
    draw.rectangle([(W - 18, 0), (W, H)], fill=GOLD)

    # header
    tag_font = load_font(40, bold=True)
    draw_centered(img, "IBM SkillsBuild — Verified Completion", 80, tag_font, fill=SOFT_WHITE)

    # main title
    title_font = load_font(120, bold=True)
    draw_centered(img, "SkillsBuild", 180, title_font, fill=GOLD)
    draw_centered(img, "Badge Certificate", 320, title_font, fill=WHITE)

    # team
    sub_font = load_font(52, bold=False)
    label_font = load_font(38, bold=True)
    body_font = load_font(46, bold=False)

    draw_centered(img, "Team FINN-ISH LINE  ·  Miami Dade College  ·  AI Models", 490, sub_font, fill=SOFT_WHITE)

    # certificate detail box
    box_x0, box_y0, box_x1, box_y1 = 140, 620, W - 140, 900
    draw.rectangle([(box_x0, box_y0), (box_x1, box_y1)], fill=NAVY_LIGHT, outline=GOLD, width=4)
    draw.text((box_x0 + 40, box_y0 + 30), "LEARNER", font=label_font, fill=GOLD)
    draw.text((box_x0 + 340, box_y0 + 30), "Louis Rodriguez", font=body_font, fill=WHITE)
    draw.text((box_x0 + 40, box_y0 + 110), "COURSE ID", font=label_font, fill=GOLD)
    draw.text((box_x0 + 340, box_y0 + 110), "ALM-COURSE_4058914", font=body_font, fill=WHITE)
    draw.text((box_x0 + 40, box_y0 + 190), "CNUM", font=label_font, fill=GOLD)
    draw.text((box_x0 + 340, box_y0 + 190), "3585509REG", font=body_font, fill=WHITE)

    # QR code
    qr_img = make_qr(CERT_URL, box_size=10)
    qr_size = 520
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)
    qr_x = (W - qr_size) // 2
    qr_y = 970
    # white border around QR
    pad = 24
    draw.rectangle(
        [(qr_x - pad, qr_y - pad), (qr_x + qr_size + pad, qr_y + qr_size + pad)],
        fill=WHITE,
        outline=GOLD,
        width=4,
    )
    img.paste(qr_img, (qr_x, qr_y))

    # QR caption
    caption_font = load_font(38, bold=True)
    small_font = load_font(30, bold=False)
    draw_centered(img, "Scan to verify at IBM SkillsBuild", qr_y + qr_size + 60, caption_font, fill=SOFT_WHITE)

    # URL (broken into three lines to fit)
    url_font = load_font(24, bold=False)
    url_lines = [
        "skills.yourlearning.ibm.com/certificate/share/",
        "34b188b7f0ewogICJvYmplY3RUeXBlIiA6ICJBQ1RJVklUWSIsCiAg",
        "ImxlYXJuZXJDTlVNIiA6ICIzNTg1NTA5UkVHIiwKICAib2JqZWN0SWQi...",
    ]
    y_url = qr_y + qr_size + 130
    for line in url_lines:
        draw_centered(img, line, y_url, url_font, fill=GREY)
        y_url += 40

    # footer
    footer_font = load_font(30, bold=False)
    draw_centered(
        img,
        "IBM AI Racing League 2026  ·  Louis Rodriguez · Daniel Pino · Javier Perez-Hickman",
        H - 90,
        footer_font,
        fill=SOFT_WHITE,
    )

    img.save(OUT_PATH, "PNG", optimize=True)
    print(f"wrote {OUT_PATH}  ({OUT_PATH.stat().st_size / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
