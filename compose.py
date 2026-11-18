#!/usr/bin/env python3
"""Compose the front-page image for 17 November 2026 news.

Draws a newspaper front page with PIL: every word is real, crisp text
rendered by PIL from system fonts. No AI-generated text anywhere.
Output: entry.png, 1024x1024, under 1 MiB.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (14, 42, 71)
RED = (176, 30, 36)
GOLD = (201, 162, 39)
GREY = (90, 90, 90)
LIGHT = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
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


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading):
    """Draw wrapped headline (bold serif), return y after last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((512, 14), "THE WORLD IN ONE PAGE", font=font(SANS_B, 20),
       fill=GOLD, anchor="ma")
d.text((512, 40), "TUESDAY 17 NOVEMBER 2026", font=font(SERIF_B, 52),
       fill=LIGHT, anchor="ma")
d.text((512, 96), "WORLD NEWS  •  ONE DAY  •  ONE IMAGE",
       font=font(SANS, 15), fill=(200, 210, 225), anchor="ma")
d.rectangle([0, 118, W, 122], fill=RED)

# ---------------------------------------------------------------- hero art: bridge over water, broken span
ax0, ay0, ax1, ay1 = 24, 130, 1000, 306
d.rectangle([ax0, ay0, ax1, ay1], fill=(207, 227, 242))
# skyline silhouettes
for bx, bw, bh in [(40, 60, 46), (120, 44, 66), (190, 70, 38),
                   (820, 52, 58), (900, 66, 40)]:
    d.rectangle([ax0 + bx, ay1 - 118 - bh, ax0 + bx + bw, ay1 - 118],
                fill=(120, 140, 160))
# water
d.rectangle([ax0, ay1 - 78, ax1, ay1], fill=(46, 111, 158))
for wx in range(ax0 + 10, ax1 - 10, 46):
    d.arc([wx, ay1 - 52, wx + 34, ay1 - 38], 0, 180, fill=(140, 190, 220), width=3)
    d.arc([wx + 14, ay1 - 26, wx + 48, ay1 - 12], 0, 180, fill=(140, 190, 220), width=3)
# bridge deck (left span intact, middle collapsed, right span intact)
deck_y = ay1 - 118
d.rectangle([ax0, deck_y, ax0 + 380, deck_y + 10], fill=(60, 60, 64))
d.rectangle([ax0 + 596, deck_y, ax1, deck_y + 10], fill=(60, 60, 64))
# fallen span, tilted into the water
d.polygon([(ax0 + 400, deck_y + 4), (ax0 + 560, deck_y + 4),
           (ax0 + 585, ay1 - 30), (ax0 + 425, ay1 - 30)], fill=(80, 80, 86))
# pylons and cables
for px in (ax0 + 150, ax0 + 800):
    d.rectangle([px, deck_y - 62, px + 12, deck_y], fill=(60, 60, 64))
    d.rectangle([px - 8, deck_y - 70, px + 20, deck_y - 62], fill=(60, 60, 64))
for cx in range(ax0 + 30, ax0 + 380, 34):
    d.line([(cx, deck_y), (ax0 + 156, deck_y - 62)], fill=(110, 110, 116), width=2)
for cx in range(ax0 + 620, ax1 - 10, 34):
    d.line([(cx, deck_y), (ax0 + 806, deck_y - 62)], fill=(110, 110, 116), width=2)
# explosion glow + smoke at the gap
d.ellipse([ax0 + 440, deck_y - 46, ax0 + 530, deck_y + 26], fill=(232, 120, 40))
d.ellipse([ax0 + 458, deck_y - 30, ax0 + 512, deck_y + 10], fill=(245, 190, 60))
for sx, sy, sr in [(470, deck_y - 34, 13), (505, deck_y - 44, 13),
                   (540, deck_y - 32, 12), (492, deck_y - 48, 9)]:
    d.ellipse([ax0 + sx - sr, sy - sr, ax0 + sx + sr, sy + sr], fill=(110, 110, 110))
d.rectangle([ax0, ay1, ax1, ay1 + 2], fill=INK)

# hero text
hy = 316
d.text((24, hy), "UKRAINE  •  CRIMEA  •  KYIV", font=font(SANS_B, 17), fill=RED)
hy = headline(d, 24, hy + 26, "BRIDGES UNDER FIRE", font(SERIF_B, 46), 952, 52)
hy = para(d, 24, hy + 6,
          "Ukraine struck the Kerch Bridge to Crimea again — the second hit in "
          "under 24 hours — and a section of the road bridge collapsed, halting "
          "traffic. Overnight, Russia hit Kyiv's North and South bridges over "
          "the Dnipro with ballistic missiles, disrupting heating, water and power.",
          font(SANS, 19), 952, 26)
d.line([24, 492, 1000, 492], fill=INK, width=2)

# ---------------------------------------------------------------- story panels
PANELS = [
    ("THE GULF", (150, 60, 40), "TANKERS ABLAZE OFF HORMUZ",
     "Mines struck tankers near the Strait of Hormuz and set them on fire. "
     "Iran's IRGC said it hit a US radar system in Bahrain; Bahrain said it "
     "intercepted Iranian drones. The USS Theodore Roosevelt arrived, a "
     "third US carrier group in the region."),
    ("DIPLOMACY", (20, 90, 130), "XI, TRUMP AND PUTIN TO MEET",
     "China confirmed the first-ever Xi–Trump–Putin trilateral summit, to be "
     "held on Thursday 19 November in Shenzhen, on the sidelines of the "
     "APEC leaders' meeting."),
    ("ASIA", (120, 60, 140), "QUAD LEADERS MEET IN MANILA",
     "Modi, Trump, Takaichi and Albanese met in Manila on the ASEAN summit "
     "sidelines. Delhi's air-pollution crisis worsened, and Cyclone Akvan "
     "bore down on Andhra Pradesh and Odisha, landfall due 20 November."),
    ("CYBER", (90, 40, 110), "178 TOP WEBSITES HACKED",
     "A cyberattack through the Optimizely platform planted malicious code "
     "on 178 major websites — including the BBC, CNN, Zoom and HSBC — aiming "
     "to steal crypto and card data."),
    ("WASHINGTON", (30, 70, 120), "PENTAGON FAILS 9TH AUDIT",
     "The Pentagon failed its financial audit for the ninth straight year: "
     "over $4.8 trillion in assets could not be verified. The US Commerce "
     "Department moved to close the loophole letting China rent US computing "
     "power for AI chips."),
    ("SPACE & SPORT", (160, 90, 20), "VULCAN FAILS; 40 SATELLITES LOST",
     "A ULA Vulcan rocket failed about 10 minutes after liftoff from Florida, "
     "losing all 40 Amazon Leo internet satellites. The ICC elected Jay Shah "
     "chairman for a second term, and the EU sanctioned 12 people and 101 "
     "entities over Russia."),
]

PX, PY, PW, PH, GX, GY = 24, 500, 312, 240, 20, 18
for i, (kicker, color, head, body) in enumerate(PANELS):
    col, row = i % 3, i // 3
    x = PX + col * (PW + GX)
    y = PY + row * (PH + GY)
    d.rectangle([x, y, x + PW, y + PH], fill=LIGHT, outline=(180, 175, 165), width=1)
    d.rectangle([x, y, x + PW, y + 30], fill=color)
    d.text((x + 10, y + 5), kicker, font=font(SANS_B, 16), fill=LIGHT)
    yy = headline(d, x + 12, y + 40, head, font(SERIF_B, 22), PW - 24, 26)
    para(d, x + 12, yy + 6, body, font(SANS, 14), PW - 24, 19)

# ---------------------------------------------------------------- footer
d.line([24, 1002, 1000, 1002], fill=INK, width=1)
d.text((512, 1008), "Every story above was reported on Tuesday 17 November 2026.",
       font=font(SANS, 13), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
