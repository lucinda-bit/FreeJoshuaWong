"""Makes images/share-card.jpg: the picture shown when the site is shared on WhatsApp, X, LinkedIn etc.
Shows Joshua's photo and the number of days he has spent in prison as of the day the site is built.
Run automatically by build.py."""
import os, datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
START = datetime.datetime(2020, 11, 22, 16, 0, tzinfo=datetime.timezone.utc)  # in custody (23 Nov, Hong Kong time)
INK, LEMON, PAPER = (12, 12, 11), (255, 225, 53), (244, 242, 236)

def days_inside(now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc)
    return (now - START).days

def make():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), INK)
    photo = Image.open(os.path.join(ROOT, "images/joshua.jpg")).convert("RGB")
    pw = 500
    photo = ImageOps.fit(photo, (pw, H), centering=(0.6, 0.35))
    img.paste(photo, (W - pw, 0))
    d = ImageDraw.Draw(img)
    anton = lambda s: ImageFont.truetype(os.path.join(HERE, "Anton.ttf"), s)
    mont = lambda s: ImageFont.truetype(os.path.join(HERE, "Montserrat-Bold.ttf"), s)
    x = 64
    d.text((x, 54), "FREE", font=anton(64), fill=PAPER)
    fw = d.textlength("FREE ", font=anton(64))
    d.text((x + fw, 54), "JOSHUA WONG", font=anton(64), fill=LEMON)
    n = f"{days_inside():,}"
    big = anton(230)
    d.text((x - 6, 150), n, font=big, fill=LEMON)
    d.text((x, 448), "DAYS BEHIND BARS", font=mont(40), fill=PAPER)
    d.text((x, 502), "and ten more years to come", font=mont(26), fill=(190, 188, 182))
    d.rectangle([0, H - 14, W - pw, H], fill=LEMON)
    d.text((x, H - 68), "freejoshuawong.org", font=mont(22), fill=(190, 188, 182))
    out = os.path.join(ROOT, "images/share-card.jpg")
    img.save(out, quality=88)
    return out

if __name__ == "__main__":
    print(make(), days_inside())
