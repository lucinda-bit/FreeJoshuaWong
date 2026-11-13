"""Branded cover images for video/podcast cards that have no picture of their own (images/covers/*.jpg).
We make our own covers rather than copying broadcasters' thumbnails."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INK, LEMON, PAPER = (12, 12, 11), (255, 225, 53), (244, 242, 236)

def f(name, size):
    return ImageFont.truetype(os.path.join(HERE, name), size)

def wrap(d, text, font, width):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            out.append(cur); cur = w
    out.append(cur)
    return out

def cover(key, kind, outlet, title, style="lemon", photo="images/joshua.jpg"):
    W, H = 1280, 720
    if style == "photo":
        src = Image.open(os.path.join(ROOT, photo)).convert("L")
        if "film-poster" in photo:  # leave out the burnt-in subtitle at the bottom of the frame
            src = src.crop((0, 0, src.width, int(src.height * 0.74)))
        img = ImageOps.fit(src, (W, H), centering=(0.4, 0.3)).convert("RGB")
        img = ImageEnhance.Brightness(img).enhance(0.38)
        fg, accent = PAPER, LEMON
    else:
        bg = LEMON if style == "lemon" else INK
        img = Image.new("RGB", (W, H), bg)
        ph = ImageOps.fit(Image.open(os.path.join(ROOT, photo)).convert("L"), (440, H), centering=(0.6, 0.35)).convert("RGB")
        img.paste(ph, (W - 440, 0))
        fg = INK if style == "lemon" else PAPER
        accent = INK if style == "lemon" else LEMON
    d = ImageDraw.Draw(img)
    x, box = 70, (W - 140) if style == "photo" else (W - 440 - 110)
    # kind label in a pill
    lab = kind.upper()
    lf = f("Montserrat-Bold.ttf", 26)
    lw = d.textlength(lab, font=lf)
    pill_bg = INK if style == "lemon" else LEMON
    pill_fg = LEMON if style == "lemon" else INK
    d.rounded_rectangle([x, 70, x + lw + 44, 70 + 50], radius=25, fill=pill_bg)
    d.text((x + 22, 80), lab, font=lf, fill=pill_fg)
    d.text((x, 150), outlet, font=f("Montserrat-Bold.ttf", 34), fill=fg)
    for size in range(104, 40, -4):
        tf = f("Anton.ttf", size)
        lines = wrap(d, title.upper(), tf, box)
        if len(lines) * size * 1.02 <= 380:
            break
    y = 215 + (380 - len(lines) * int(size * 1.02)) // 2
    for ln in lines:
        d.text((x, y), ln, font=tf, fill=accent if style != "lemon" else INK)
        y += int(size * 1.02)
    d.text((x, H - 70), "#FreeJoshuaWong", font=f("Montserrat-Bold.ttf", 24), fill=fg)
    os.makedirs(os.path.join(ROOT, "images/covers"), exist_ok=True)
    out = os.path.join(ROOT, "images/covers", key + ".jpg")
    img.save(out, quality=84)
    return "images/covers/" + key + ".jpg"

COVERS = [
    ("guardian-podcast", "Podcast", "The Guardian · Today in Focus", "Nathan Law on his friend Joshua Wong", "lemon"),
    ("byline-podcast", "Podcast", "Byline Times Podcast", "China vs Joshua Wong", "ink"),
    ("byline-tv", "Video", "Byline Times TV", "Andrew Duncan on Joshua’s story", "photo", "images/film-poster.jpg"),
    ("sky-nathan", "Interview", "Sky News · The World with Yalda Hakim", "Nathan Law: “losing ground globally”", "ink"),
    ("c4-plea", "News report", "Channel 4 News", "Joshua pleads guilty", "photo", "images/film-poster.jpg"),
    ("pelosi-floor", "Video", "US House of Representatives", "Pelosi calls for Joshua’s freedom", "lemon"),
]

def make_all():
    return {c[0]: cover(*c) for c in COVERS}

if __name__ == "__main__":
    print(make_all())
