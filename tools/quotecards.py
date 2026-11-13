"""One shareable picture per quote on the Voices page (images/quotes/<slug>.jpg).
When someone shares a quote's own link, this picture is what appears in WhatsApp, X, LinkedIn etc."""
import os, re, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INK, LEMON, PAPER, GREY = (12, 12, 11), (255, 225, 53), (244, 242, 236), (190, 188, 182)
WHERE_LABEL = {"parliament": "Parliament", "government": "Government", "rights": "Human rights", "social": "On social media"}

def slug(v):
    if v.get("id"):
        return v["id"]
    return re.sub(r"[^a-z0-9]+", "-", (v["who"] + "-" + v["date"]).lower()).strip("-")

def load_voices():
    js = "global.window={};require(%s);process.stdout.write(JSON.stringify(window.VOICES))" % json.dumps(os.path.join(ROOT, "assets/voices.js"))
    return json.loads(subprocess.check_output(["node", "-e", js]))

def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, name), size)

def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines

def card(v, out):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), INK)
    pw = 330
    photo = ImageOps.fit(Image.open(os.path.join(ROOT, "images/joshua.jpg")).convert("RGB"), (pw, H), centering=(0.62, 0.4))
    img.paste(photo, (W - pw, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 14, H], fill=LEMON)
    x, box_w = 70, W - pw - 70 - 50
    d.text((x, 44), "FREE", font=font("Anton.ttf", 34), fill=PAPER)
    d.text((x + d.textlength("FREE ", font=font("Anton.ttf", 34)), 44), "JOSHUA WONG", font=font("Anton.ttf", 34), fill=LEMON)
    q = "“" + v["quote"] + "”"
    short = len(v["quote"]) < 40
    top, bottom = 118, 470
    for size in range(110 if short else 64, 22, -2):
        f = font("Anton.ttf", size) if short else font("Newsreader.ttf", size)
        text = q.upper() if short else q
        lines = wrap(d, text, f, box_w)
        lh = int(size * (1.0 if short else 1.22))
        if len(lines) * lh <= bottom - top:
            break
    y = top + ((bottom - top) - len(lines) * lh) // 2
    for ln in lines:
        d.text((x, y), ln, font=f, fill=LEMON if short else (255, 255, 255))
        y += lh
    d.text((x, 498), v["who"].upper(), font=font("Anton.ttf", 34), fill=LEMON if not short else PAPER)
    role = v["role"] + (" · " + v["where"] if v.get("where") else "")
    rs = 21
    while d.textlength(role, font=font("Montserrat-SemiBold.ttf", rs)) > box_w and rs > 14:
        rs -= 1
    d.text((x, 546), role, font=font("Montserrat-SemiBold.ttf", rs), fill=GREY)
    d.text((x, 582), "freejoshuawong.org  #FreeJoshuaWong", font=font("Montserrat-Bold.ttf", 19), fill=GREY)
    img.save(out, quality=86)

def make_all():
    os.makedirs(os.path.join(ROOT, "images/quotes"), exist_ok=True)
    vs = load_voices()
    for v in vs:
        v["slug"] = slug(v)
        card(v, os.path.join(ROOT, "images/quotes", v["slug"] + ".jpg"))
    return vs

if __name__ == "__main__":
    for v in make_all():
        print(v["slug"])
