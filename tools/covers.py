"""Branded cover images for video/podcast cards that have no picture of their own (images/covers/*.jpg).
Each cover has its own look so the wall doesn't repeat. We make our own rather than copying broadcasters' thumbnails."""
import os, random, math
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INK, LEMON, PAPER, GREY = (12, 12, 11), (255, 225, 53), (244, 242, 236), (60, 60, 56)
W, H = 1280, 720

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

def fit_lines(d, text, box_w, box_h, start=150, lh=1.0, font="Anton.ttf"):
    for size in range(start, 30, -4):
        ft = f(font, size)
        lines = wrap(d, text, ft, box_w)
        if len(lines) * size * lh <= box_h:
            break
    return ft, lines, int(size * lh)

def pill(d, x, y, text, bg, fg):
    ft = f("Montserrat-Bold.ttf", 24)
    w = d.textlength(text, font=ft)
    d.rounded_rectangle([x, y, x + w + 40, y + 46], radius=23, fill=bg)
    d.text((x + 20, y + 9), text, font=ft, fill=fg)

def save(img, key):
    os.makedirs(os.path.join(ROOT, "images/covers"), exist_ok=True)
    img.save(os.path.join(ROOT, "images/covers", key + ".jpg"), quality=86)
    return "images/covers/" + key + ".jpg"

def waveform(key):  # Guardian podcast: lemon, audio waveform
    img = Image.new("RGB", (W, H), LEMON); d = ImageDraw.Draw(img)
    pill(d, 70, 64, "PODCAST", INK, LEMON)
    d.text((70, 128), "The Guardian · Today in Focus", font=f("Montserrat-Bold.ttf", 30), fill=INK)
    rnd = random.Random(7); cx = 70
    while cx < W - 70:
        h = int(30 + 150 * abs(math.sin(cx / 37.0)) * (0.5 + rnd.random() * 0.6))
        d.rounded_rectangle([cx, 300 - h // 2, cx + 9, 300 + h // 2], radius=4, fill=INK)
        cx += 17
    ft, lines, lh = fit_lines(d, "NATHAN LAW ON HIS FRIEND JOSHUA", W - 140, 230, 120)
    y = H - 60 - len(lines) * lh
    for ln in lines:
        d.text((70, y), ln, font=ft, fill=INK); y += lh
    return save(img, key)

def versus(key):  # Byline podcast: black, giant outline VS
    img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
    d.text((W - 600, -60), "VS", font=f("Anton.ttf", 640), fill=INK, stroke_width=5, stroke_fill=LEMON)
    pill(d, 70, 64, "PODCAST", LEMON, INK)
    d.text((70, 128), "Byline Times Podcast", font=f("Montserrat-Bold.ttf", 30), fill=PAPER)
    d.text((70, 290), "CHINA", font=f("Anton.ttf", 150), fill=PAPER)
    d.text((70, 445), "VS JOSHUA", font=f("Anton.ttf", 150), fill=LEMON)
    d.text((70, H - 58), "Andrew Duncan with Adrian Goldberg", font=f("Montserrat-SemiBold.ttf", 24), fill=(170, 168, 160))
    return save(img, key)

def duotone(key):  # Byline TV: film still in lemon/black duotone
    src = Image.open(os.path.join(ROOT, "images/film-poster.jpg")).convert("L")
    src = src.crop((0, 0, src.width, int(src.height * 0.74)))
    g = ImageOps.autocontrast(ImageOps.fit(src, (W, H), centering=(0.35, 0.3)))
    img = ImageOps.colorize(g, black=INK, white=LEMON)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H - 190, W, H], fill=INK)
    pill(d, 70, 64, "VIDEO", INK, LEMON)
    d.text((70, H - 172), "BYLINE TIMES TV", font=f("Montserrat-Bold.ttf", 26), fill=LEMON)
    d.text((70, H - 132), "ANDREW DUNCAN ON JOSHUA’S STORY", font=f("Anton.ttf", 78), fill=PAPER)
    return save(img, key)

def rings(key):  # Sky: black, concentric rings, quote
    img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
    cx, cy = W - 230, H // 2
    for r in range(40, 900, 46):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(52, 52, 47), width=3)
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=LEMON)
    pill(d, 70, 64, "INTERVIEW", LEMON, INK)
    d.text((70, 128), "Sky News · The World with Yalda Hakim", font=f("Montserrat-Bold.ttf", 30), fill=PAPER)
    d.text((64, 190), "“", font=f("Anton.ttf", 180), fill=LEMON)
    d.text((70, 330), "LOSING GROUND", font=f("Anton.ttf", 120), fill=PAPER)
    d.text((70, 455), "GLOBALLY”", font=f("Anton.ttf", 120), fill=PAPER)
    d.text((70, H - 62), "Nathan Law, the day Joshua was sentenced", font=f("Montserrat-SemiBold.ttf", 26), fill=(170, 168, 160))
    return save(img, key)

def datestamp(key):  # Channel 4: split with big date
    img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
    d.polygon([(0, 0), (560, 0), (440, H), (0, H)], fill=LEMON)
    d.text((70, 100), "2", font=f("Anton.ttf", 340), fill=INK)
    d.text((70, 480), "SEP 2026", font=f("Anton.ttf", 96), fill=INK)
    pill(d, 560, 64, "NEWS REPORT", LEMON, INK)
    d.text((560, 128), "Channel 4 News", font=f("Montserrat-Bold.ttf", 30), fill=PAPER)
    ft, lines, lh = fit_lines(d, "JOSHUA PLEADS GUILTY", W - 560 - 60, 330, 130)
    y = 220
    for ln in lines:
        d.text((560, y), ln, font=ft, fill=PAPER); y += lh
    d.text((560, H - 62), "With analysis on China and the UK", font=f("Montserrat-SemiBold.ttf", 24), fill=(170, 168, 160))
    return save(img, key)

def stripes(key):  # Pelosi: paper with stripes, quote
    img = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(img)
    for i in range(7):
        d.rectangle([W - 330, i * 104, W, i * 104 + 52], fill=INK)
    pill(d, 70, 64, "VIDEO", INK, LEMON)
    d.text((70, 128), "US House of Representatives", font=f("Montserrat-Bold.ttf", 30), fill=INK)
    ft, lines, lh = fit_lines(d, "“WE MUST NOT LET THIS BE IGNORED.”", W - 330 - 140, 360, 120)
    y = 200 + (360 - len(lines) * lh) // 2
    for ln in lines:
        d.text((70, y), ln, font=ft, fill=INK); y += lh
    d.rectangle([70, H - 84, 150, H - 76], fill=LEMON)
    d.text((70, H - 62), "Nancy Pelosi on the House floor", font=f("Montserrat-SemiBold.ttf", 26), fill=GREY)
    return save(img, key)

COVERS = {"guardian-podcast": waveform, "byline-podcast": versus, "byline-tv": duotone,
          "sky-nathan": rings, "c4-plea": datestamp, "pelosi-floor": stripes}

def make_all():
    return {k: fn(k) for k, fn in COVERS.items()}

if __name__ == "__main__":
    print(make_all())
