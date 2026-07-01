#!/usr/bin/env python3
"""Generate MDC Racing team-video PNG visuals.

Produces ten 1920x1080 PNG title cards under docs/video-visuals/ with a
consistent brand style (deep royal blue background, gold accents, white text)
matching the MDC Racing livery.

Usage:
    python scripts/generate_video_visuals.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
NAVY = (10, 32, 84)
NAVY_DEEP = (6, 20, 56)
GOLD = (255, 205, 40)
WHITE = (255, 255, 255)
SOFT_WHITE = (230, 230, 240)
GREY = (170, 175, 190)

OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "video-visuals"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load a font, preferring bold when requested. Falls back to default."""
    candidates_bold = [
        r"C:\Windows\Fonts\segoeuib.ttf",
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
    ]
    candidates_regular = [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
    ]
    for path in (candidates_bold if bold else candidates_regular):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def make_base() -> Image.Image:
    """1920x1080 canvas with vertical navy gradient + gold accent bar."""
    img = Image.new("RGB", (W, H), NAVY_DEEP)
    draw = ImageDraw.Draw(img)
    # vertical gradient
    for y in range(H):
        t = y / H
        r = int(NAVY_DEEP[0] + (NAVY[0] - NAVY_DEEP[0]) * t)
        g = int(NAVY_DEEP[1] + (NAVY[1] - NAVY_DEEP[1]) * t)
        b = int(NAVY_DEEP[2] + (NAVY[2] - NAVY_DEEP[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    # gold accent bar top and bottom
    draw.rectangle([(0, 0), (W, 12)], fill=GOLD)
    draw.rectangle([(0, H - 12), (W, H)], fill=GOLD)
    # tag in corner
    tag = load_font(28, bold=True)
    draw.text((40, 26), "MDC RACING · IBM AI RACING LEAGUE 2026", font=tag, fill=SOFT_WHITE)
    return img


def draw_centered(img: Image.Image, text: str, y: int, font: ImageFont.FreeTypeFont, fill=WHITE):
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, font=font, fill=fill)


def draw_left(img: Image.Image, text: str, x: int, y: int, font: ImageFont.FreeTypeFont, fill=WHITE):
    ImageDraw.Draw(img).text((x, y), text, font=font, fill=fill)


def save(img: Image.Image, name: str) -> None:
    path = OUT_DIR / name
    img.save(path, "PNG", optimize=True)
    print(f"  wrote {path}")


# ------------------------------------------------------------------ Slide 01
def slide_01_title() -> None:
    img = make_base()
    title_font = load_font(140, bold=True)
    sub_font = load_font(56, bold=False)
    small_font = load_font(40, bold=False)
    draw_centered(img, "MDC RACING", 340, title_font, fill=GOLD)
    draw_centered(img, "Miami Dade College · AI Models", 520, sub_font)
    draw_centered(img, "IBM AI Racing League 2026", 610, sub_font, fill=SOFT_WHITE)
    draw_centered(img, "Corkscrew · IBM F1 · Standing Start", 730, small_font, fill=GREY)
    save(img, "01-title.png")


# ------------------------------------------------------------------ Slide 02
def slide_02_team() -> None:
    img = make_base()
    heading = load_font(96, bold=True)
    body = load_font(64, bold=False)
    role = load_font(38, bold=False)
    draw_centered(img, "The Team", 200, heading, fill=GOLD)
    y = 400
    for name in ("Louis Rodriguez", "Daniel Pino", "Javier Perez-Hickman"):
        draw_centered(img, name, y, body)
        y += 100
    draw_centered(img, "Miami Dade College · AI Models", 820, role, fill=GREY)
    save(img, "02-team.png")


# ------------------------------------------------------------------ Slide 03
def slide_03_what_we_built() -> None:
    img = make_base()
    heading = load_font(96, bold=True)
    body = load_font(50, bold=False)
    code = load_font(38, bold=True)
    draw_centered(img, "What We Built", 180, heading, fill=GOLD)
    draw_centered(img, "A rule-based autonomous driver for TORCS", 360, body)
    draw_centered(img, "connected over the SCR scr_server UDP protocol.", 430, body)
    draw_left(img, "src/driver_baseline.py", 260, 620, code, fill=WHITE)
    draw_left(img, "telemetry/segments_baseline_current.yaml", 260, 700, code, fill=WHITE)
    draw_centered(img, "Every decision traceable to a physics-grounded parameter.", 860, body, fill=SOFT_WHITE)
    save(img, "03-what-we-built.png")


# ------------------------------------------------------------------ Slide 04
def slide_04_lap_time() -> None:
    img = make_base()
    heading = load_font(96, bold=True)
    time_font = load_font(360, bold=True)
    body = load_font(52, bold=False)
    small = load_font(38, bold=False)
    draw_centered(img, "Submission Lap", 140, heading, fill=GOLD)
    draw_centered(img, "02:23.96", 300, time_font)
    draw_centered(img, "CLEAN · 0 damage · standing start · Corkscrew", 720, body, fill=SOFT_WHITE)
    draw_centered(img, "From 3:32.99 (Run 001) → 2:23.96 (submission) · −69 seconds", 830, small, fill=GREY)
    save(img, "04-lap-time.png")


# ------------------------------------------------------------------ Slide 05
def slide_05_strategy() -> None:
    img = make_base()
    heading = load_font(96, bold=True)
    body = load_font(46, bold=False)
    num = load_font(64, bold=True)
    draw_centered(img, "How We Got Faster", 160, heading, fill=GOLD)
    items = [
        ("1", "Structured telemetry archive per run"),
        ("2", "Per-segment target speed + racing-line tuning"),
        ("3", "Physics-based lookahead brake controller"),
    ]
    y = 380
    for n, text in items:
        draw_left(img, n, 260, y, num, fill=GOLD)
        draw_left(img, text, 380, y + 10, body)
        y += 130
    save(img, "05-strategy.png")


# ------------------------------------------------------------------ Slide 06
def slide_06_granite() -> None:
    img = make_base()
    heading = load_font(96, bold=True)
    body = load_font(46, bold=False)
    small = load_font(36, bold=False)
    draw_centered(img, "IBM Granite", 140, heading, fill=GOLD)
    draw_centered(img, "Our offline strategy analyst", 260, body)
    draw_centered(img, "Local via Ollama · Continue extension in VS Code", 340, small, fill=SOFT_WHITE)
    y = 500
    for text in (
        "· Per-segment telemetry review",
        "· Config generation (wider exit-line YAML)",
        "· Plateau-breaking hypothesis ranking",
    ):
        draw_left(img, text, 340, y, body)
        y += 90
    draw_centered(img, "Dense telemetry in · Structured strategy out", 900, small, fill=GREY)
    save(img, "06-granite.png")


# ------------------------------------------------------------------ Slide 07
def slide_07_skillsbuild() -> None:
    img = make_base()
    heading = load_font(96, bold=True)
    body = load_font(46, bold=False)
    small = load_font(36, bold=False)
    draw_centered(img, "IBM SkillsBuild", 140, heading, fill=GOLD)
    draw_centered(img, "Shared vocabulary for AI system tradeoffs", 260, body)
    draw_centered(img, "Every MDC Racing team member completed coursework", 340, small, fill=SOFT_WHITE)
    y = 500
    for text in (
        "· Sample efficiency vs generalization",
        "· Deterministic control vs learned control",
        "· Small local models for offline analysis",
    ):
        draw_left(img, text, 320, y, body)
        y += 90
    draw_centered(img, "Framed our choice: rule-based first, RL later.", 900, small, fill=GREY)
    save(img, "07-skillsbuild.png")


# ------------------------------------------------------------------ Slide 08
def slide_08_repo() -> None:
    img = make_base()
    heading = load_font(90, bold=True)
    body = load_font(44, bold=False)
    url = load_font(48, bold=True)
    draw_centered(img, "Our Work Is Public", 200, heading, fill=GOLD)
    draw_centered(img, "GitHub · MDC Racing submission repo", 380, body, fill=SOFT_WHITE)
    draw_centered(img, "github.com/LouisRodriguez12101815/", 560, url)
    draw_centered(img, "ibm-racing-league-submission", 640, url)
    draw_centered(img, "Reproducible: clone, install TORCS, run one script.", 840, body, fill=GREY)
    save(img, "08-repo.png")


# ------------------------------------------------------------------ Slide 09
def slide_09_blog() -> None:
    img = make_base()
    heading = load_font(90, bold=True)
    body = load_font(42, bold=False)
    url = load_font(40, bold=True)
    draw_centered(img, "Full Write-Up on Medium", 200, heading, fill=GOLD)
    draw_centered(img, "\"IBM Bob's Reward Shaper: Keep Us Moving\"", 380, body, fill=SOFT_WHITE)
    draw_centered(img, "medium.com/@louis.rodriguez006/", 560, url)
    draw_centered(img, "ibm-bobs-reward-shaper-keep-us-moving", 640, url)
    draw_centered(img, "Architecture · Granite workflow · Lessons learned", 840, body, fill=GREY)
    save(img, "09-blog.png")


# ------------------------------------------------------------------ Slide 10
def slide_10_close() -> None:
    img = make_base()
    heading = load_font(160, bold=True)
    body = load_font(56, bold=False)
    small = load_font(40, bold=False)
    draw_centered(img, "See You on the", 340, heading, fill=WHITE)
    draw_centered(img, "Leaderboard.", 500, heading, fill=GOLD)
    draw_centered(img, "MDC Racing · Miami Dade College", 780, body)
    draw_centered(img, "Louis Rodriguez · Daniel Pino · Javier Perez-Hickman", 880, small, fill=SOFT_WHITE)
    save(img, "10-close.png")


def main() -> int:
    print(f"Generating visuals in: {OUT_DIR}")
    slide_01_title()
    slide_02_team()
    slide_03_what_we_built()
    slide_04_lap_time()
    slide_05_strategy()
    slide_06_granite()
    slide_07_skillsbuild()
    slide_08_repo()
    slide_09_blog()
    slide_10_close()
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
