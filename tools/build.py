#!/usr/bin/env python3
"""Builds the Free Joshua Wong site pages from shared header/footer.
Run from the repo root:  python3 tools/build.py
Edit page content in this file, then re-run. Output: *.html in the repo root and letters/."""
import os

# The site's full address. Until freejoshuawong.org points straight at the site (DNS, not GoDaddy forwarding),
# links and share previews must use the GitHub address. When the domain is connected properly, set this back to
# "https://freejoshuawong.org" and change SITE_URL at the top of assets/site.js to match.
SITE = "https://freejoshuawong.org"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import re as _re
PRESS_COUNT = len(_re.findall(r'^\s*\{date:', open(os.path.join(ROOT, "assets/press.js")).read(), _re.M))

NAV = [("case.html", "The case"), ("film.html", "Watch"), ("newsroom.html", "Newsroom"), ("parliament.html", "Parliament"), ("voices.html", "Voices"), ("socials.html", "Socials"), ("write.html", "Write to Joshua")]

# Visitor counting (GoatCounter: no cookies, nothing that identifies visitors).
# Put the site code from goatcounter.com here, e.g. "freejoshuawong". Leave empty to switch counting off.
GOATCOUNTER = "freejoshuawong"

def analytics():
    if not GOATCOUNTER:
        return ""
    return f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n'

import re
# Party labels for sitting parliamentarians (checked against members.parliament.uk). Key = text that appears in the name.
PARTY = {
    "Alton": "CB", "Bennett of Manor Castle": "Green", "Bob Blackman": "Con", "Alistair Carmichael": "LD",
    "Graeme Downie": "Lab", "Iain Duncan Smith": "Con", "Foster of Aghadrumsee": "NA", "Jeremy Hunt": "Con",
    "Alicia Kearns": "Con", "Kennedy of The Shaws": "Lab", "Andrew Mitchell": "Con", "James Naish": "Lab",
    "Patten of Barnes": "Con", "Tom Tugendhat": "Con", "Bobby Dean": "LD", "Lord Garnier": "Con",
    "Alex Barros-Curtis": "Lab", "Emily Darlington": "Lab", "Lord Shinkwin": "Con", "Richard Holden": "Con",
    "Marie Rimmer": "Lab", "Catherine West": "Lab", "Gregory Stafford": "Con", "Luke Akehurst": "Lab", "Alyn Smith": "SNP",
}
PARTY_NAME = {"Con": "Conservative", "Lab": "Labour", "LD": "Liberal Democrat", "Green": "Green Party", "SNP": "SNP", "CB": "Crossbench", "NA": "Non-affiliated"}
def party_tag(name):
    for k, p in PARTY.items():
        if k in name:
            return f'<span class="pty pty-{p.lower()}" title="{PARTY_NAME[p]}">{p}</span>'
    return ""
def tag_names(text):
    """Add a party label after each parliamentarian named in a short line of text (first mention each)."""
    for k, p in PARTY.items():
        m = re.search(re.escape(k) + r"[^,·<]*?(?: MP)?(?=$|[,·<]| \()", text)
        if m and 'class="pty' not in text[m.end():m.end()+30]:
            text = text[:m.end()] + " " + party_tag(k) + text[m.end():]
    return text.replace("</span>, ", "</span>&emsp;")

# One date per count, so every "days" number on the site agrees.
JAILED_DATE = "2020-11-23"   # in custody continuously since
PROMISE_DATE = "2026-09-01"  # the Foreign Secretary said he would take up the case

def head(title, desc, path, depth=0):
    up = "../" * depth
    full = "Free Joshua Wong" if title == "Free Joshua Wong" else f"{title} — Free Joshua Wong"
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0C0C0B">
<meta name="apple-mobile-web-app-title" content="Free Joshua">
<link rel="apple-touch-icon" href="{up}images/apple-touch-icon.png">
<link rel="icon" type="image/png" href="{up}images/favicon.png">
<title>{full}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/images/share-card.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:image" content="{SITE}/images/share-card.jpg">
<meta property="og:url" content="{SITE}/{path}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Montserrat:wght@500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/site.css">
{analytics()}</head>
<body>
"""

def nav(current, depth=0):
    up = "../" * depth
    links = "".join(
        f'<a href="{up}{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV)
    return f"""<nav class="top" aria-label="Main">
  <div class="wrap">
    <a class="brand" href="{up}index.html">Free <span>Joshua Wong</span></a>
    <div class="links">{links}<a href="{up}zh.html" lang="zh-Hant-HK" class="lang"{" aria-current=\"page\"" if current == "zh.html" else ""}>中文</a><a href="{up}act.html" class="mob-only"{" aria-current=\"page\"" if current == "act.html" else ""}>Take action</a></div>
    <a class="btn" href="{up}act.html">Take action</a>
    <button class="menu-btn" type="button" aria-expanded="false">Menu</button>
  </div>
</nav>
"""

COLLEAGUES = [
    ("Hong Kong Watch", "https://www.hongkongwatch.org"),
    ("Committee for Freedom in Hong Kong Foundation", "https://thecfhk.org"),
    ("Index on Censorship", "https://www.indexoncensorship.org"),
    ("Fortify Rights", "https://www.fortifyrights.org"),
    ("Inter-Parliamentary Alliance on China", "https://www.ipac.global"),
]

import datetime as _dt
try:
    from zoneinfo import ZoneInfo as _Z
    _now = _dt.datetime.now(_Z("Europe/London"))
except Exception:
    _now = _dt.datetime.now()
UPDATED = f"{_now.day} {_now:%B %Y}"

def footer(depth=0, scripts=""):
    up = "../" * depth
    col = "".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in COLLEAGUES)
    return f"""<section class="colleagues" aria-label="Further reading">
  <div class="wrap">
    <div class="label dim">More on Hong Kong’s political prisoners</div>
    <div class="row">{col}</div>
  </div>
</section>
<footer>
  <div class="wrap">
    <div>
      <div class="brand">Free <span>Joshua Wong</span></div>
      <p>A campaign for the release of Joshua Wong, the Hong Kong democracy campaigner in prison since November 2020.</p>
      <p class="updated" style="font-size:12px;opacity:.6">Last updated {UPDATED}</p>
    </div>
    <div class="cols">
      <nav aria-label="Footer">
        <a href="{up}case.html">The case</a><a href="{up}film.html">Watch</a><a href="{up}newsroom.html">Newsroom</a><a href="{up}parliament.html">Parliament</a><a href="{up}voices.html">Voices</a><a href="{up}socials.html">Socials</a>
        <a href="{up}newsroom.html#presskit">Press kit</a><a href="{up}act.html">Take action</a>
      </nav>
      <div>
        <p style="font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:11px;color:var(--accent);margin:0">Press enquiries</p>
        <p style="margin-top:10px"><a class="btn small-btn" href="{up}contact.html">Contact us</a></p>
      </div>
    </div>
  </div>
</footer>
{scripts}<script src="{up}assets/site.js"></script>
</body>
</html>
"""

LETTER = """Dear [MP name],

I am writing as your constituent about Joshua Wong, the Hong Kong democracy campaigner who on 5 November was sentenced to a further ten years in prison under the National Security Law.

Britain guaranteed Hong Kong’s freedoms in the Joint Declaration. Joshua only ever asked that this promise be kept.

On 1 September the Foreign Secretary told the House of Commons he would take up Joshua’s case. There has been no public update since.

Please urge the Foreign Secretary to summon the Chinese Ambassador over Joshua’s case, as the Foreign Office did for Jimmy Lai, and tell me what it is doing to secure his release.

Yours sincerely,
[Name, address]"""

def page_head(label, title_html, lede, crumbs=None):
    c = f'<div class="crumbs">{crumbs}</div>' if crumbs else f'<div class="label">{label}</div>'
    return f"""<header class="phead">
  <div class="wrap">
    {c}
    <h1>{title_html}</h1>
    <p class="lede">{lede}</p>
  </div>
</header>
"""

ASKS = """<div class="asks">
      <div class="ask ask-lead"><h3>Summon China’s Ambassador</h3><p>The Foreign Secretary should summon the Chinese Ambassador and raise Joshua and the others imprisoned for standing up for democracy, by name, as the Foreign Office did for Jimmy Lai.</p></div>
      <div class="ask"><h3>Review the Hong Kong Economic and Trade Office’s privileges</h3><p>The Hong Kong Economic and Trade Office in London keeps diplomatic-style privileges, even after a senior manager there was convicted of spying on Hong Kongers in Britain.</p></div>
      <div class="ask"><h3>Sanction those responsible</h3><p>Hold to account the officials behind National Security Law prosecutions, working with Britain’s allies.</p></div>
    </div>"""

FACTS = """<section class="facts" aria-label="Key facts">
  <div class="wrap">
    <div class="fact"><div class="n">Nov&nbsp;2020</div><div class="t">In prison continuously since</div></div>
    <div class="fact"><div class="n">Jan&nbsp;2027</div><div class="t">When he was due to walk free</div></div>
    <div class="fact"><div class="n">10&nbsp;years</div><div class="t">New sentence, handed down on 5 November 2026</div></div>
    <div class="fact"><div class="n">2036</div><div class="t">Around when he may be released, aged 40</div></div>
  </div>
</section>
"""

CTA = """<section class="cta-band">
  <div class="wrap">
    <div>
      <h2>Two minutes.<br>Two things you can do.</h2>
      <p>Ask your MP to raise Joshua’s case with the Foreign Secretary, and share his story so he isn’t forgotten.</p>
    </div>
    <div class="btns">
      <a class="btn dark" href="{up}act.html#mp">Write to your MP</a>
      <a class="btn line-dark" href="{up}act.html#share">Share his story</a>
    </div>
  </div>
</section>
"""

# ---------------- HOME ----------------
PLAYER = '''<div class="screen vid"><video controls preload="none" playsinline poster="images/film-poster.jpg?v=2"><source src="media/joshua-prisoner-vs-superpower.mp4" type="video/mp4">Your browser can’t play this video.</video></div>'''

FLAGS = ["UK","US","Australia","Canada","France","Germany","Italy","Japan","Netherlands","New Zealand"]

# Years with shorter spells in prison before 2020: Aug-Oct 2017 (unlawful assembly, sentence later quashed);
# Jan 2018 and May-Jun 2019 (contempt of court, Mong Kok clearance).
BRIEF_YEARS = {2017, 2018, 2019}

def life_bar():
    cells, labels = [], []
    marks = {1996:"Born", 2012:"Age 15", 2020:"Age 24, jailed", 2027:"Was due out", 2036:"Age 40, possible release"}
    for i, y in enumerate(range(1996, 2037)):
        state = "s-brief" if y in BRIEF_YEARS else ("s-free" if y < 2020 else ("s-in" if y <= 2026 else "s-ahead"))
        cells.append(f'<span class="c {state}" title="{y}"></span>')
    for y, t in marks.items():
        col = y - 1996 + 1
        cls = " last" if y == 2036 else (" end" if y >= 2027 else "")
        labels.append(f'<span class="m{cls}" style="grid-column:{col} / span 1"><b>{y}</b>{t}</span>')
    return "".join(cells), "".join(labels)

def home():
    cells, labels = life_bar()
    latest = "".join(
        f'<li><a href="{u}" target="_blank" rel="noopener"><span class="o">{o}</span><span class="h">{h}</span><span class="d">{d}</span></a></li>'
        for o, h, d, u in LATEST)
    return head("Free Joshua Wong", "Joshua Wong spoke up for Hong Kong. He has been in prison since November 2020, and on 5 November 2026 was given ten more years.", "") + nav("index.html") + """
<main class="home4">
<script>if(!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))document.documentElement.classList.add('intro');</script>
<header class="h4-hero" id="top">
  <div class="h4-text">
    <h1 class="fit"><span>Free Joshua Wong</span></h1>
    <div class="h4-titles" aria-label="The film: in 2017, Teenager vs. Superpower; in 2026, Prisoner vs. Superpower">
      <div class="r then"><span class="y">2017</span><s>Teenager vs. Superpower</s></div>
      <div class="r now"><span class="y">2026</span><b>Prisoner vs. Superpower</b></div>
      <div class="r cell-row"><span class="y">Now</span>
        <div class="cell" role="timer" aria-label="Days Joshua Wong has spent in prison">
          <div class="cell-in"><span class="n" id="days" """ + 'data-jailed="' + JAILED_DATE + '"' + """>2,181</span><span class="u">days<br>behind bars</span></div>
        </div>
      </div>
    </div>
    <p class="h4-lead">He was due out in January 2027. Instead, he has been given ten more years.</p>
    <div class="h4-cta">
      <a class="btn" href="#write">Email your MP</a>
      <a class="btn ghost" href="#film">Watch the film</a>
    </div>
  </div>
  <figure class="h4-pic">
    <img src="images/joshua.jpg?v=2" alt="Joshua Wong raising a two-fingered salute beneath an umbrella during the 2014 Umbrella Movement">
    <figcaption>Hong Kong, 2014</figcaption>
  </figure>
</header>

<section class="h4-life" aria-labelledby="life-h">
  <div class="wrap">
    <h2 id="life-h">His life, year by year</h2>
    <p class="h4-sub">If the sentence stands, Joshua will spend the years from 24 to 40 in prison: his late twenties and almost all of his thirties.</p>
    <div class="lifebar" role="img" aria-label="A bar of 41 years from 1996 to 2036. 1996 to 2016 free; 2017 to 2019 free apart from shorter spells in prison; 2020 to 2026 in prison; 2027 to 2036 still to serve.">""" + cells + """</div>
    <div class="lifemarks" aria-hidden="true">""" + labels + """</div>
    <ul class="key"><li><i class="s-free"></i>Free</li><li><i class="s-brief"></i>Shorter spells in prison</li><li><i class="s-in"></i>In prison</li><li><i class="s-ahead"></i>Still to serve</li></ul>
  </div>
</section>

<section class="h4-msgs" id="h4-msgs" hidden aria-label="Messages for Joshua">
  <div class="wrap">
    <div class="h4-msgs-head"><h2>Messages for Joshua</h2><a class="btn" href="write.html">Write yours</a></div>
    <div class="h4-msgs-row" id="h4-msgs-row"></div>
  </div>
</section>

<section class="h4-words">
  <div class="wrap">
    <blockquote>“The only thing I worry about is that people will forget Hong Kong.”</blockquote>
    <p class="by">Joshua Wong, in a letter to a friend from prison, published by <a href="https://www.theguardian.com/world/2026/nov/05/joshua-wong-hong-kong-prison-letters-sentenced-10-years" target="_blank" rel="noopener"><em>The Guardian</em></a>, 5 November 2026</p>
  </div>
</section>

<section class="h4-film" id="film">
  <div class="wrap">
    <div class="h4-film-head">
      <h2>Joshua: Prisoner vs. Superpower</h2>
      <p>In 2017, <em>Teenager vs. Superpower</em> followed a schoolboy who took on Beijing. This short film tells what happened next.</p>
    </div>
    <div class="film-wide">
      """ + PLAYER + """
    </div>
  </div>
</section>

<section class="h4-pressure" aria-label="The pressure so far">
  <div class="wrap">
    <h2>The pressure is building</h2>
    <div class="pstats">
      <a href="voices.html#governments"><b>11</b><span>governments, plus the EU, condemned his sentence</span></a>
      <a href="letters/open-letter-prime-minister-sept-2026.html"><b>""" + str(len(SIGNATORIES)) + """</b><span>MPs, peers and rights leaders signed the open letter to the Prime Minister</span></a>
      <a href="parliament.html"><b>""" + str(sum(1 for r in RECORD if r[1] not in ("event", "letter") and r[0] >= "2025-06-06")) + """</b><span>times raised in Parliament since the new charge in June 2025</span></a>
      <a href="newsroom.html"><b>""" + str(PRESS_COUNT) + """</b><span>reports, podcasts and editorials since June 2025</span></a>
    </div>
  </div>
</section>

<section class="h4-asks">
  <div class="wrap">
    <h2>What Britain should do</h2>
    <p class="h4-sub">Britain guaranteed Hong Kong’s freedoms in 1984. Ten governments, including our own, signed a joint statement condemning Joshua’s sentence. Now words need to become action.</p>
    <div class="asklist">
      <div class="ask-lead"><span class="ask-tag">Our first ask</span><h3>Summon China’s Ambassador</h3><p>The Foreign Secretary should summon the Chinese Ambassador and name Joshua and the others jailed for standing up for democracy, as the Foreign Office did for Jimmy Lai.</p><a class="btn" href="letters/open-letter-prime-minister-sept-2026.html">Read the open letter</a></div>
      <div><h3>Review the Hong Kong Economic and Trade Office’s privileges</h3><p>Its London office keeps diplomatic-style privileges, even after a senior manager there was convicted of spying on Hong Kongers in Britain.</p></div>
      <div><h3>Sanction those responsible</h3><p>Hold the officials behind National Security Law prosecutions to account, together with Britain’s allies.</p></div>
    </div>
    <p class="h4-who"><span><b>MP, peer or journalist?</b> See the <a href="parliament.html">record in Parliament</a> or get our <a href="newsroom.html#presskit">press kit</a>.</span></p>
    """ + tracker() + """
    <p class="h4-more"><a href="case.html">Read the full case</a></p>
  </div>
</section>

<section class="h4-act" id="write">
  <div class="wrap">
    <h2>Tell your MP: summon China’s Ambassador</h2>
    <p>Two minutes. We’ve written the letter, asking your MP to urge the Foreign Secretary to summon the Chinese Ambassador. Put in your postcode and we’ll find your MP and open an email to them with the letter filled in. <a href="act.html#mp">Read the letter first</a></p>
    """ + mp_box() + """
    <div class="tpl" id="tpl" hidden>""" + LETTER + """</div>
  </div>
</section>

<section class="h4-news">
  <div class="wrap">
    <div class="h4-news-head"><h2>Latest coverage</h2><a class="h4-link" href="newsroom.html">All coverage and statements</a></div>
    <ul class="newslist">""" + latest + """</ul>
  </div>
</section>
</main>
<script>
(function(){ // fit the title to the width of its column
  function fit(){document.querySelectorAll('h1.fit span').forEach(function(s){
    var box=s.parentElement.clientWidth; s.style.fontSize='100px';
    var w=s.getBoundingClientRect().width; if(w>0) s.style.fontSize=Math.min(170,100*box/w)+'px';});}
  fit(); if(document.fonts&&document.fonts.ready) document.fonts.ready.then(fit);
  window.addEventListener('resize',fit);
})();
window.addEventListener('DOMContentLoaded',function(){
  var el=document.getElementById('days');
  if(!el || !window.daysSince) return;
  var fmt=function(n){return n.toLocaleString('en-GB');}, pl=function(n,w){return n+' '+w+(n===1?'':'s');};
  var total=window.daysSince(el.getAttribute('data-jailed'));
  var intro=document.documentElement.classList.contains('intro');
  if(!intro){el.textContent=fmt(total);}
  else{el.textContent='0';setTimeout(function(){var t0=null;requestAnimationFrame(function step(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/1700);k=1-Math.pow(1-k,3);el.textContent=fmt(Math.round(total*k));if(k<1)requestAnimationFrame(step);});},2000);}
  setInterval(function(){el.textContent=fmt(window.daysSince(el.getAttribute('data-jailed')));},60000);
});
(function(){ // scroll moments: the life bar fills year by year; the pressure numbers count up
  if(!document.documentElement.classList.contains('intro')||!('IntersectionObserver' in window)) return;
  var bar=document.querySelector('.lifebar');
  if(bar){bar.classList.add('wait');new IntersectionObserver(function(es,o){es.forEach(function(e){if(!e.isIntersecting)return;o.disconnect();
    bar.querySelectorAll('.c').forEach(function(c,i){c.style.transitionDelay=(i*45)+'ms';});bar.classList.remove('wait');});},{threshold:.5}).observe(bar);}
  var nums=document.querySelectorAll('.pstats b');
  if(nums.length){var box=nums[0].closest('.pstats');nums.forEach(function(b){b.dataset.to=b.textContent;b.textContent='0';});
    new IntersectionObserver(function(es,o){es.forEach(function(e){if(!e.isIntersecting)return;o.disconnect();
      nums.forEach(function(b){var to=+b.dataset.to,t0=null;requestAnimationFrame(function st(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/1200);k=1-Math.pow(1-k,3);b.textContent=Math.round(to*k);if(k<1)requestAnimationFrame(st);});});});},{threshold:.4}).observe(box);}
})();
</script>
""" + footer(0, '<script src="assets/messages.js"></script>\n')

LATEST = [
    ("US Senate", "Senator Josh Hawley urges the Secretary of State to press for Joshua’s release", "20 Nov 2026", "https://www.hawley.senate.gov/hawley-urges-state-department-to-advocate-for-release-of-hong-kong-rights-champion-joshua-wong/"),
    ("Parliament · Written answers", "Asked whether the Ambassador was summoned, the minister doesn’t say", "18–19 Nov 2026", "parliament.html"),
    ("Human Rights Research Center", "Hong Kong pro-democracy activist Joshua Wong sentenced to ten years", "18 Nov 2026", "https://www.humanrightsresearch.org/post/hong-kong-pro-democracy-activist-joshua-wong-sentenced-to-ten-years"),
    ("Global Voices", "‘Who will respond?’ Joshua fears being forgotten amid his 10-year sentence", "18 Nov 2026", "https://globalvoices.org/2026/11/18/who-will-respond-jailed-hong-kong-pro-democracy-activist-joshua-wong-fears-being-forgotten-amid-10-year-sentence/"),
    ("The Washington Post · Opinion", "Joshua Wong and the APEC summit: calling Hong Kong’s bluff", "17 Nov 2026", "https://www.washingtonpost.com/opinions/2026/11/17/joshua-wong-apec-call-hong-kong-bluff/"),
]

# ---------------- THE CASE ----------------
TIMELINE = [
    ("Born", "Oct 1996", "", "Born in Hong Kong", "Joshua Wong Chi-fung grows up in a city promised a high degree of autonomy until 2047."),
    ("15", "Sep 2012", "", "Defeats “national education”", "With Scholarism, the student group he co-founded the year before, he leads the protests that force the Hong Kong government to shelve a compulsory “national education” curriculum."),
    ("17", "Sep 2014", "", "The Umbrella Movement", "His arrest at Civic Square helps spark 79 days of street occupation demanding genuine universal suffrage. <em>Time</em> puts him on its cover."),
    ("19", "Apr 2016", "", "Co-founds Demosistō", "With Nathan Law and other Umbrella Movement leaders, he launches Demosistō, a new political party campaigning for democracy in Hong Kong."),
    ("19", "Sep 2016", "", "Gets his friend Nathan Law elected", "Too young to stand himself, Joshua campaigns for Demosistō’s chairman, Nathan Law, who wins a seat on Hong Kong Island and becomes the youngest lawmaker in Hong Kong’s history, at 23. Nathan is disqualified the following year."),
    ("19", "Oct 2016", "", "Detained at Bangkok airport", "Held and deported by Thai authorities on his way to speak at a university, an early sign of how far Beijing’s pressure would reach."),
    ("20", "Jan 2017", "", "The film", "<em>Joshua: Teenager vs. Superpower</em> premieres at Sundance and wins the World Cinema Documentary Audience Award."),
    ("20", "Aug 2017", "", "First prison sentence: unlawful assembly", "Jailed for six months for unlawful assembly over the 2014 Civic Square protest. Released on bail after about two months, in October 2017; Hong Kong’s top court quashes the sentence in February 2018."),
    ("21–22", "2018–19", "", "Second prison term: contempt of court", "Jailed for contempt of court over the 2014 clearance of the Mong Kok protest site. He serves the sentence in separate periods, the last in May–June 2019."),
    ("22", "Sep 2019", "", "Testifies to the US Congress", "Gives evidence to the Congressional-Executive Commission on China on human rights in Hong Kong. Years later, prosecutors cite his lobbying in Washington against him."),
    ("23", "Jun 2020", "", "The National Security Law", "Beijing imposes the National Security Law on Hong Kong. His party, Demosistō, disbands the same day."),
    ("24", "Nov 2020", "", "Jailed over protests, and never released", "Held in custody from 23 November after pleading guilty, he is sentenced in December to 13½ months for unauthorised assembly over a 2019 protest outside police headquarters. More protest sentences follow in 2021, including for joining a Tiananmen vigil. He has not been free since."),
    ("24", "Jan 2021", "", "Subversion case: arrested as one of the Hong Kong 47", "Arrested in prison under the National Security Law for taking part in an unofficial pro-democracy primary election, and charged with subversion in February."),
    ("28", "Nov 2024", "", "Subversion case: 4 years 8 months", "Sentenced in the largest national security trial in Hong Kong’s history. His release date is set for early 2027."),
    ("28", "Jun 2025", "", "Collusion case: charged again in prison", "Charged with conspiracy to collude with foreign forces, carrying a maximum of life imprisonment. The evidence is his own advocacy and public statements."),
    ("29", "Sep 2026", "", "Raised in Parliament, then a guilty plea", "On 1 September Sir Iain Duncan Smith <a href=\"parliament.html#exchange\">raises his case in the Commons</a> and the Foreign Secretary says he will take it up. The next day Joshua pleads guilty in the collusion case. On 13 September, 31 MPs, peers and rights leaders sign <a href=\"letters/open-letter-prime-minister-sept-2026.html\">an open letter to the Prime Minister</a>."),
    ("30", "13 Oct 2026", "", "Turns thirty in prison", "Parliamentarians mark his birthday with a screening of <a href=\"film.html\">the new film</a> in the Houses of Parliament."),
    ("30", "5 Nov 2026", "", "Collusion case: ten more years", "A Hong Kong court sentences him to ten years for conspiracy to collude with foreign forces. Ten governments, including the UK, condemn it in <a href=\"https://www.gov.uk/government/news/statement-on-the-sentencing-of-joshua-wong\" target=\"_blank\" rel=\"noopener\">a joint statement</a>. <a href=\"https://focustaiwan.tw/politics/202611050018\" target=\"_blank\" rel=\"noopener\">Taiwan</a> and <a href=\"https://www.eeas.europa.eu/eeas/hong-kong-statement-spokesperson-sentencing-joshua-wong_en\" target=\"_blank\" rel=\"noopener\">the EU</a> condemn it too."),
    ("30", "10 Nov 2026", "", "Raised again in the Commons", "Five days after the sentence, Emily Darlington MP <a href=\"parliament.html#exchange-nov\">asks the Government</a> to summon the Chinese Ambassador and call for Joshua’s release. The next day she and seven other MPs and peers set out the same demands in <a href=\"letters/times-letter-nov-2026.html\">a letter to <em>The Times</em></a>."),
    ("40", "c. 2036", "future", "Release, if nothing changes", "Unless governments act, Joshua may not walk free until he is around 40, having spent most of his adult life in prison."),
]

def case():
    items = "".join(
        f'<div class="titem{" future" if fut else ""}"><div class="d">{d}<span class="age">{age if age=="Born" else "Age " + age}</span></div><div><h3>{h}</h3><p>{p}</p></div></div>'
        for age, d, fut, h, p in TIMELINE)
    return head("The case", "Who Joshua Wong is, what he is charged with, and why Britain has a responsibility to act.", "case.html") + nav("case.html") + page_head(
        "The case", "He kept his&nbsp;word.<br><em>Will&nbsp;we?</em>",
        "Joshua Wong has spent his adult life asking Beijing to keep the promises it made to Hong Kong. He is now serving ten more years for it.") + """
""" + FACTS + """
<section>
  <div class="wrap">
    <div class="two">
      <div>
        <h3>Who he is</h3>
        <p>Joshua Wong has campaigned for democracy in Hong Kong since he was a schoolboy. At fifteen he stopped a Beijing-backed “national education” curriculum; at seventeen he was the face of the Umbrella Movement, on the cover of TIME as <a href="https://time.com/3482556/hong-kong-protest-teenagers/" target="_blank" rel="noopener">“The Face of Protest”</a>; at twenty he was the subject of an award-winning Netflix documentary. At thirty, he is in a maximum-security prison.</p>
      </div>
      <div>
        <h3>What his latest sentence is for</h3>
        <p>“Conspiracy to collude with foreign forces” under the National Security Law, a law imposed by Beijing in 2020.</p>
        <ul>
          <li><strong>The evidence is his own words:</strong> his meetings with foreign politicians, social media posts, op-eds and interviews.</li>
          <li><strong>Much of it predates the law:</strong> prosecutors relied on his lobbying from before the law existed, and on later posts and interviews to argue it carried on.</li>
          <li><strong>He was already in prison:</strong> he was charged from his cell, while still serving another sentence.</li>
          <li><strong>The result:</strong> ten more years, handed down on 5 November 2026.</li>
        </ul>
      </div>
    </div>
    <div class="cases">
      <h3>His cases at a glance</h3>
      <table>
        <thead><tr><th>Sentenced</th><th>Charge</th><th>What it was for</th><th>Sentence</th></tr></thead>
        <tbody>
          <tr><td>2017</td><td>Unlawful assembly</td><td>The 2014 Civic Square protest that helped spark the Umbrella Movement</td><td>6 months; released on bail after about two months, and the sentence was quashed by Hong Kong’s top court in 2018</td></tr>
          <tr><td>2018</td><td>Contempt of court</td><td>The 2014 clearance of the Mong Kok protest site</td><td>Served in separate periods, the last in May–June 2019</td></tr>
          <tr><td>2020–21</td><td>Unauthorised assembly</td><td>Protests in 2019 and 2020, including a Tiananmen vigil</td><td>Several sentences, the longest 13½ months. He has been in prison since November 2020</td></tr>
          <tr><td>2024</td><td>Subversion (Hong Kong 47)</td><td>Taking part in an unofficial pro-democracy primary election in 2020</td><td>4 years 8 months, due to end in early 2027</td></tr>
          <tr class="now"><td>2026</td><td>Collusion with foreign forces</td><td>His advocacy abroad: meetings with foreign politicians, posts and interviews</td><td>10 years</td></tr>
        </tbody>
      </table>
    </div>
    <p class="pull">He is serving a sentence for believing us.</p>
    <div class="why">
      <div><div class="k">1984</div><h4>Britain gave its word</h4><p>The UK signed the Joint Declaration and guaranteed Hong Kong’s freedoms for fifty years. The Government has itself declared China in breach of it.</p></div>
      <div><div class="k">1996</div><h4>Britain was responsible for him the day he was born. It still is.</h4><p>Joshua was born under British rule, shortly before the handover. His generation was promised fifty years of freedom. Britain must keep its promise.</p></div>
      <div><div class="k">2026</div><h4>It has reached our streets</h4><p>Two men were convicted at the Old Bailey this year of spying on Hong Kong dissidents in Britain, and jailed. Hong Kongers settled here have bounties on their heads.</p></div>
    </div>
  </div>
</section>

<section id="timeline">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="label">His life so far</div><h2 class="sec">From 15 <em>to 40</em></h2></div>
      <a class="btn ghost" href="newsroom.html#presskit">Download the fact sheet</a>
    </div>
    <p class="tl-note">Joshua was born on 13 October 1996, so each age shown is his age at the time.</p>
    <div class="timeline life">""" + items + """</div>
  </div>
</section>
""" + CTA.format(up="") + footer()

# ---------------- FILM ----------------
def film():
    return head("Watch", "Joshua: Prisoner vs. Superpower, plus interviews, Commons clips and podcasts about Joshua Wong.", "film.html") + nav("film.html") + page_head(
        "The film", "Prisoner vs.<br><em>Superpower</em>",
        "The award-winning 2017 documentary followed a schoolboy who took on a superpower. This is what happened next.") + """
<section class="film" style="border-top:0">
  <div class="wrap">
    <div class="film-card">
      <!-- FILM: self-hosted in media/ -->
      <div class="screen vid"><video controls preload="none" playsinline poster="images/film-poster.jpg?v=2"><source src="media/joshua-prisoner-vs-superpower.mp4" type="video/mp4">Your browser can’t play this video.</video></div>
      <div class="film-copy">
        <div class="label dim">Producer Andrew Duncan</div>
        <h3>Joshua: <span>Prisoner</span> vs. Superpower</h3>
        <p>A new short film from the team behind <em>Joshua: Teenager vs. Superpower</em>. Archive, new interviews, and the six years since the cameras stopped.</p>
        <p>First shown to parliamentarians in Committee Room 15, Houses of Parliament, on 13 October 2026, Joshua’s 30th birthday.</p>
        <div data-share data-url="https://freejoshuawong.org/film.html" data-text="Joshua: Prisoner vs. Superpower — the second chapter"></div>
      </div>
    </div>

    <div class="film-note">
      <div class="big">#1</div>
      <p>In September 2026, Hong Kong’s Security Bureau said <a href="https://www.dimsumdaily.hk/security-bureau-reviewing-netflix-film-on-joshua-wong/" target="_blank" rel="noopener">“follow-up steps were under way”</a> over <a href="https://www.netflix.com/watch/80169348" target="_blank" rel="noopener">the original documentary</a>, which is still on Netflix in the city. Hong Kongers responded by sending it to <a href="https://www.theepochtimes.com/china/documentary-on-joshua-wong-surges-to-no-1-on-netflix-hong-kong-after-criticism-6093687" target="_blank" rel="noopener">number one on Netflix</a> there.</p>
    </div>

    <section class="parl-feature kb-feature" id="badenoch">
      <div class="label" style="margin-bottom:22px">Also on the record</div>
      <div class="px">
        <div class="px-vid">
          <div class="screen vid"><video controls preload="none" playsinline poster="images/badenoch-2026-11-03-poster.jpg"><source src="media/badenoch-2026-11-03.mp4" type="video/mp4">Your browser can’t play this video.</video></div>
          <p class="px-cap">Conservative Party rally, HMS Wellington, London, 3 November 2026.</p>
        </div>
        <div class="px-side">
          <div class="px-when">3 November 2026 · Conservative rally, London</div>
          <div class="px-sp">
            <div class="px-name">Kemi Badenoch MP</div>
            <div class="px-role">Conservative, North West Essex · Leader of the Opposition</div>
            <p>Two days before Joshua was sentenced, the Conservative leader was asked about China. She said Britain should not do business as usual while Beijing holds dissidents and British citizens in its prisons: “I would be going and getting those people released.”</p>
          </div>
          <p class="px-link"><a href="https://thenightly.com.au/politics/uk-oppposition-leader-kemi-badenoch-demands-prisoner-release-before-xi-talks-rejects-chogm-reparations-c-23113763" target="_blank" rel="noopener">Read the report</a></p>
          <div data-share data-url="https://freejoshuawong.org/film.html#badenoch" data-text="Kemi Badenoch on China’s political prisoners: “I would be going and getting those people released.”"></div>
        </div>
      </div>
    </section>

    <div class="watch-wall" id="watch">
      <div class="sec-head"><div><div class="label">Watch and listen</div><h2 class="sec">Interviews, clips and <em>podcasts</em></h2></div></div>
      <div class="vwall">""" + video_cards(skip_film=True) + """</div>
    </div>


    <div class="res-grid">
      <div class="res"><div class="label">The original</div><h3>Teenager vs. Superpower</h3><p>The 2017 documentary, winner of the Sundance World Cinema Documentary Audience Award. <a href="https://www.netflix.com/watch/80169348" target="_blank" rel="noopener">Watch it on Netflix</a>.</p></div>
      <div class="res"><div class="label">For social</div><h3>Trailer clip</h3><p>A short clip for sharing on X, Instagram and WhatsApp.</p><span class="soon">Coming soon</span></div>
      <div class="res"><div class="label">Screenings</div><h3>Host a screening</h3><p>Parliamentarians, universities and community groups can request a screening with a short panel.</p><p><a class="btn small-btn" href="contact.html?topic=screening">Request a screening</a></p></div>
    </div>
  </div>
</section>
""" + footer()

# ---------------- NEWSROOM ----------------
STATEMENTS = """<div class="timeline">
      <div class="titem"><div class="d">10 Nov 2026</div><div>
          <div class="who">UK Government · Minister of State for Security, in the Commons</div>
          <div class="flags"><span>UK</span></div>
          <h3>“The Government share the concerns about Mr Wong”</h3>
          <p>Replying to Emily Darlington MP at an urgent question, Security Minister Dan Jarvis said the Government share the concerns about Joshua and Jimmy Lai, pointing to recent Foreign Office statements on both cases.</p>
          <a class="src" href="https://hansard.parliament.uk/Commons/2026-11-10/debates/E43553F9-3D50-41D2-844C-D23E5DCFBF96/ChinaBreachOfUKParliamentariansData" target="_blank" rel="noopener">Hansard</a></div></div>
      <div class="titem"><div class="d">6 Nov 2026</div><div>
          <div class="who">Joint statement · 10 foreign ministries</div>
          <div class="flags"><span>UK</span><span>US</span><span>Australia</span><span>Canada</span><span>France</span><span>Germany</span><span>Italy</span><span>Japan</span><span>Netherlands</span><span>New Zealand</span></div>
          <h3>Ten governments, including the UK, condemn the sentence</h3>
          <p>The day after sentencing, the foreign ministries said the case shows how the National Security Law is used to target people for political expression. They called for an end to unjust NSL prosecutions and for the rights promised under the 1984 Sino-British Joint Declaration to be honoured.</p>
          <a class="src" href="https://www.gov.uk/government/news/statement-on-the-sentencing-of-joshua-wong" target="_blank" rel="noopener">Read the statement</a></div></div>
      <div class="titem"><div class="d">6 Nov 2026</div><div>
          <div class="who">US Secretary of State</div>
          <div class="flags"><span>US</span></div>
          <h3>“We call for his immediate release”</h3>
          <p>Marco Rubio said the US strongly condemns the decision to sentence Joshua again for exercising his freedom of speech, and called for his immediate release and that of all unjustly detained persons.</p>
          <a class="src" href="https://x.com/SecRubio/status/2118728915464176060" target="_blank" rel="noopener">See the post</a></div></div>
      <div class="titem"><div class="d">5 Nov 2026</div><div>
          <div class="who">European Union · EEAS spokesperson</div>
          <div class="flags"><span>EU</span></div>
          <h3>The EU “deplores” a politically motivated sentence</h3>
          <p>The European Union said it deplores the politically motivated sentencing of Joshua to an exceptionally long prison term under the National Security Law.</p>
          <a class="src" href="https://www.eeas.europa.eu/eeas/hong-kong-statement-spokesperson-sentencing-joshua-wong_en" target="_blank" rel="noopener">Read the statement</a></div></div>
      <div class="titem"><div class="d">5 Nov 2026</div><div>
          <div class="who">US Consulate General, Hong Kong</div>
          <div class="flags"><span>US</span></div>
          <h3>“Unjustly imprisoned”</h3>
          <p>The US Consulate said Joshua has been unjustly imprisoned since late 2020, and that Beijing will go to extraordinary lengths to silence those who advocate for fundamental freedoms.</p>
          <a class="src" href="https://www.wamc.org/2026-11-05/hong-kong-activist-joshua-wong-is-sentenced-to-10-more-years-in-prison" target="_blank" rel="noopener">AP report</a></div></div>
      <div class="titem"><div class="d">5 Nov 2026</div><div>
          <div class="who">Presidential Office, Taiwan</div>
          <div class="flags"><span>Taiwan</span></div>
          <h3>Taiwan condemns the sentence</h3>
          <p>Taiwan’s Presidential Office condemned the 10-year sentence and urged Beijing and Hong Kong to release detained pro-democracy figures.</p>
          <a class="src" href="https://focustaiwan.tw/politics/202611050018" target="_blank" rel="noopener">Focus Taiwan</a></div></div>
      <div class="titem"><div class="d">22 Oct 2026</div><div>
          <div class="who">UK Government · Six-monthly Report on Hong Kong</div>
          <div class="flags"><span>UK</span></div>
          <h3>Named in the Government’s report to Parliament</h3>
          <p>The report for January to June 2026 cites developments in Joshua’s case as reinforcing concerns about the increasingly broad application of national security legislation.</p>
          <a class="src" href="https://www.gov.uk/government/publications/six-monthly-report-on-hong-kong-january-to-june-2026/six-monthly-report-on-hong-kong-1-january-to-30-june-2026" target="_blank" rel="noopener">GOV.UK</a></div></div>
      <div class="titem"><div class="d">1 Sep 2026</div><div>
          <div class="who">UK Government · Foreign Secretary, in the Commons</div>
          <div class="flags"><span>UK</span></div>
          <h3>The Foreign Secretary says he will take up the case</h3>
          <p>Asked by Sir Iain Duncan Smith at Foreign Office Questions, Ed Miliband said he would take up Joshua’s case. There has been no public update since.</p>
          <a class="src" href="parliament.html#exchange">Watch the exchange</a></div></div>
      <div class="titem"><div class="d">23 Oct 2025</div><div>
          <div class="who">UK Government · Six-monthly Report on Hong Kong</div>
          <div class="flags"><span>UK</span></div>
          <h3>His re-arrest on the record</h3>
          <p>The report for January to June 2025 records Joshua’s re-arrest on 6 June on suspicion of collusion with foreign forces.</p>
          <a class="src" href="https://www.gov.uk/government/publications/six-monthly-report-on-hong-kong-january-to-june-2025/six-monthly-report-on-hong-kong-1-january-to-30-june-2025" target="_blank" rel="noopener">GOV.UK</a></div></div>
      <div class="titem"><div class="d">3 Jul 2025</div><div>
          <div class="who">UK Government · Foreign Office written answer</div>
          <div class="flags"><span>UK</span></div>
          <h3>The UK is “deeply concerned”</h3>
          <p>Answering a written question from Alicia Kearns MP, the Foreign Office said it was deeply concerned by the news of further charges against Joshua.</p>
          <a class="src" href="https://questions-statements.parliament.uk/written-questions/detail/2025-06-26/63014" target="_blank" rel="noopener">Parliamentary answer</a></div></div>
      <div class="titem"><div class="d">2 Dec 2020</div><div>
          <div class="who">UK Government · Foreign Secretary</div>
          <div class="flags"><span>UK</span></div>
          <h3>“Bring an end to their campaign to stifle opposition”</h3>
          <p>As Joshua, Agnes Chow and Ivan Lam began their prison sentences, Foreign Secretary Dominic Raab urged the Hong Kong and Beijing authorities to bring an end to their campaign to stifle opposition.</p>
          <a class="src" href="https://www.aljazeera.com/news/2020/12/2/joshua-wong-jailed-for-xx-years-over-2019-illegal-assembly" target="_blank" rel="noopener">Al Jazeera</a></div></div>
      <div class="titem" style="padding-bottom:0"><div class="d">24 Sep 2020</div><div>
          <div class="who">UK Government · Foreign Secretary</div>
          <div class="flags"><span>UK</span></div>
          <h3>“Deeply concerned about the arrest of Joshua Wong”</h3>
          <p>Dominic Raab said the arrest was another example of the Hong Kong authorities targeting activists, and that Chinese and Hong Kong authorities must respect the rights and freedoms protected in the Joint Declaration.</p>
          <a class="src" href="socials.html#raab-2020">See the post</a></div></div>
    </div>"""

def newsroom():
    return head("Newsroom", "Press coverage, press releases, government statements, letters and the press kit on Joshua Wong’s case.", "newsroom.html") + nav("newsroom.html") + page_head(
        "Newsroom", "The world is <em>watching</em>",
        "Coverage of Joshua’s case, the campaign’s press releases, what governments have said on the record, letters, and the press kit.") + """
<section style="border-top:0;padding-top:20px">
  <div class="wrap">
    <div class="tabs" role="tablist">
      <a href="#coverage" role="tab">Coverage</a>
      <a href="#releases" role="tab">Press releases</a>
      <a href="#letters" role="tab">Letters</a>
      <a href="#presskit" role="tab">Press kit</a>
    </div>

    <div class="panel" id="panel-coverage">
      <p class="cov-intro">Joshua has been in the headlines since he co-founded Scholarism at 14 and led the fight against Beijing’s “national education” plans. This wall follows the current case, from the new charge in June 2025 to today.</p>
      <div class="cov-stats" id="cov-stats"></div>
      <div class="ticker" aria-hidden="true"><div class="ticker-track" id="ticker"></div></div>
      <div class="moments" id="moments" role="group" aria-label="Filter by moment"></div>
      <div class="cov-bar">
        <div class="filters" role="group" aria-label="Filter by type">
          <button class="chip" data-t="all" aria-pressed="true">Everything</button>
          <button class="chip" data-t="news" aria-pressed="false">News</button>
          <button class="chip" data-t="opinion" aria-pressed="false">Opinion</button>
          <button class="chip" data-t="rights" aria-pressed="false">Rights groups</button>
        </div>
        <label class="cov-search"><span>Search</span><input type="search" id="cov-q" placeholder="Outlet or headline, e.g. Guardian"></label>
        <p class="cov-note">Headlines link to the original. Some outlets may ask you to subscribe.</p>
      </div>
      <div id="cov-feature"></div>
      <div id="cov-list" class="cov-list"></div>
    </div>

    <div class="panel" id="panel-releases" hidden>
      <p class="lede" style="margin-bottom:34px">Statements and press releases from the Free Joshua Wong campaign.</p>
      """ + releases_html() + """
    </div>

    <div class="panel" id="panel-presskit" hidden>
      <p class="lede" style="margin-bottom:34px">For journalists and MPs’ offices: the key facts, images and interviews.</p>
""" + PRESSKIT + """
    </div>

    <div class="panel" id="panel-letters" hidden>
      <p class="lede" style="margin-bottom:34px">Letters from parliamentarians and supporters, to the Prime Minister and to the press.</p>
      <div class="rel">
        <div class="d">11 Nov 2026</div>
        <div>
          <div class="type">Letter to the editor · The Times</div>
          <h3><a href="letters/times-letter-nov-2026.html">Unjust prosecution</a></h3>
          <p>Eight MPs and peers, including Emily Darlington MP, Lord Alton and Lord Patten, answer The Times’s leader: “condemnation is a statement, not a policy.” They ask the Government to summon the Chinese ambassador, sanction those responsible and tell Parliament what further consequences will follow. <a href="https://www.thetimes.com/comment/letters-to-editor/article/times-letters-civil-service-needs-urgent-reform-wq3bcj955" target="_blank" rel="noopener">In The Times</a></p>
        </div>
        <span class="pill pub">Published</span>
      </div>
      <div class="rel">
        <div class="d">13 Sep 2026</div>
        <div>
          <div class="type">Open letter · to the Prime Minister</div>
          <h3><a href="letters/open-letter-prime-minister-sept-2026.html">Britain should stand for something</a></h3>
          <p>31 MPs and peers from across the parties, former Foreign Secretaries and human rights leaders and organisations ask the Prime Minister to call in the Chinese Ambassador and raise Joshua’s case. Published by <a href="https://www.hongkongwatch.org/all-posts/2026/9/14/cross-party-coalition-of-parliamentarians-and-human-rights-leaders-calls-on-prime-minister-to-act-on-hong-kong" target="_blank" rel="noopener">Hong Kong Watch</a>.</p>
        </div>
        <span class="pill"><i></i>Awaiting reply</span>
      </div>
    </div>
  </div>
</section>
""" + footer(0, '<script src="assets/press.js"></script>\n')

# ---------------- LETTER PAGE ----------------
SIGNATORIES = [  # as in the final letter (Lucy, 17 Nov 2026)
    ("Lord Alton of Liverpool", ""), ("Alex Barros-Curtis MP", ""), ("Baroness Bennett of Manor Castle", ""),
    ("Bob Blackman CBE MP", ""), ("Sir Bill Browder KCMG", ""), ("The Rt Hon Alistair Carmichael MP", ""),
    ("Mark Clifford", "President, The Committee for Freedom in Hong Kong Foundation"), ("Bobby Dean MP", ""),
    ("Graeme Downie MP", ""), ("Andrew Duncan", "Co-Founder, RT Weatherman Foundation"),
    ("The Rt Hon Sir Iain Duncan Smith MP", ""), ("Fortify Rights", ""),
    ("The Rt Hon the Baroness Foster of Aghadrumsee DBE", ""), ("The Rt Hon The Lord Garnier KC", ""),
    ("The Rt Hon Sir Jeremy Hunt MP", "Former Foreign Secretary"), ("Jamie Fly", "CEO, Freedom House"), ("Hong Kong Watch", ""),
    ("Alicia Kearns MP", "Shadow Minister for Foreign Affairs and Chair of the APPG on Arbitrary Detention and Hostage Affairs"),
    ("Baroness Kennedy of The Shaws KC", "Director of the International Bar Association’s Human Rights Institute"),
    ("Tim Loughton", "Former Member of Parliament and current Chair of the Conservative Party Human Rights Commission"),
    ("The Rt Hon Sir Andrew Mitchell KCMG MP", ""), ("Meaghan Mobbs", "President, RT Weatherman Foundation"),
    ("Sir Geoffrey Nice KC", "Chair of the Uyghur Tribunal and China Tribunal"), ("James Naish MP", ""),
    ("The Rt Hon the Lord Patten of Barnes KG CH", ""), ("The Rt Hon Sir Malcolm Rifkind KCMG KC", ""),
    ("Benedict Rogers", "Co-founder and Chair of Hong Kong Watch and Senior Director of Fortify Rights"),
    ("Jemimah Steinfeld", "Chief Executive, Index on Censorship"),
    ("The Rt Hon Tom Tugendhat MBE VR MP", "Shadow Foreign Secretary"),
    ("Sara Wilbourne", "Acting Deputy Executive Director, ARTICLE 19"), ("Bess Weatherman", "Co-Founder, RT Weatherman Foundation"),
]

def letter_pm():
    sig = "".join(f"<li>{n} {party_tag(n)}{f'<small>{r}</small>' if r else ''}</li>" for n, r in SIGNATORIES)
    return head("Open letter to the Prime Minister", "Parliamentarians and human rights organisations ask the Prime Minister to raise Joshua Wong’s case with the Chinese Ambassador.", "letters/open-letter-prime-minister-sept-2026.html", 1) + nav("newsroom.html", 1) + page_head(
        "", "Britain should <em>stand for something</em>",
        "An open letter to the Prime Minister, Andy Burnham, sent on 13 September 2026.",
        crumbs='<a href="../newsroom.html#letters">Newsroom</a> &nbsp;/&nbsp; Letters') + """
<section class="letters letter-page" style="border-top:0">
  <div class="wrap">
    <div class="letter">
      <article class="paper">
        <div class="meta"><span class="status" style="margin:0"><i></i> Awaiting a reply from Downing Street</span></div>
        <div class="head">Open letter to the Prime Minister · 13 September 2026</div>
        <p style="margin-top:22px">Dear Prime Minister,</p>
        <p>This week, you said ‘it is more important than ever that Britain stands for something.’ The Foreign Secretary went further: that governments ‘have to make our own decisions about legality, values’ and act on them.</p>
        <p>We agree. We are asking you to apply that principle to Hong Kong and the Joint Declaration, and hold China to account for its abusive use of the National Security Law, criminalising peaceful democratic activity.</p>
        <p>Joshua Wong has been a pro-democracy advocate since he was a child. At 15 he founded a movement to resist Beijing’s education law and went on to become the face of the Umbrella Movement. His work always sought to hold Beijing to the 1997 agreement, ‘One Country, Two Systems’, agreed between the UK and China. But in 2020 he was arrested and detained. Now, like British Citizen Jimmy Lai, he faces the prospect of life in prison.</p>
        <p>This is not a distant problem. Two men were convicted at the Old Bailey this year for spying on Hong Kong dissidents in Britain, reportedly also monitoring British parliamentarians. Police are investigating footage appearing to show Chinese embassy security in London brandishing banned electroshock weapons at peaceful protesters. Hong Kongers settled in the UK have bounties on their heads. China’s National Security Law is felt on the streets of Britain.</p>
        <p>The UK has a moral and diplomatic responsibility, arising from the 1997 handover and the Joint Declaration, to speak out for those who stood up for the treaty it guaranteed. The UK Government has already found China in breach of the treaty. In December, the last Foreign Secretary told the Commons plainly: “China breached the Joint Declaration by imposing its National Security Law on the city.”</p>
        <p>It is time that you called the Chinese Ambassador to raise Joshua’s case and that of the others imprisoned for standing up for democracy.</p>
        <p><strong>Britain signed the Joint Declaration and guaranteed Hong Kong’s freedoms for fifty years. Joshua Wong only ever asked his government to keep its word. We are asking ours to keep it too.</strong></p>
        <p class="sign">Written before Joshua was sentenced on 5 November 2026.</p>
        <p class="no-print" style="font-family:var(--label);font-size:14px">After the sentence, eight MPs and peers followed up with <a href="times-letter-nov-2026.html">a letter to <em>The Times</em></a> (11 November 2026).</p>
        <p class="no-print" style="font-family:var(--label);font-size:14px">Published by <a href="https://www.hongkongwatch.org/all-posts/2026/9/14/cross-party-coalition-of-parliamentarians-and-human-rights-leaders-calls-on-prime-minister-to-act-on-hong-kong" target="_blank" rel="noopener">Hong Kong Watch</a> · <a href="open-letter-prime-minister-sept-2026.pdf" download>Download the letter (PDF)</a></p>
        <div class="no-print" style="margin-top:26px" data-share data-url="https://freejoshuawong.org/letters/open-letter-prime-minister-sept-2026.html" data-text="Open letter to the Prime Minister on Joshua Wong"></div>
      </article>
      <aside class="signs">
        <h4>Signatories</h4>
        <ul>""" + sig + """</ul>
      </aside>
    </div>
  </div>
</section>
""" + footer(1)

# ---------------- RESOURCES ----------------
def resources():
    # Resources now lives in the Newsroom (Press kit tab). This page sends old links there.
    return """<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><title>Press kit — Free Joshua Wong</title>
<meta http-equiv="refresh" content="0; url=newsroom.html#presskit"><link rel="canonical" href="https://freejoshuawong.org/newsroom.html#presskit"></head>
<body><p>The press kit has moved to the <a href="newsroom.html#presskit">Newsroom</a>.</p></body></html>
"""


PRESSKIT = """    <div class="facts-sheet">
      <h2 id="factsheet">Joshua Wong: fact sheet</h2>
      <div class="sub">Updated 22 November 2026</div>
      <dl>
        <dt>Who</dt><dd>Joshua Wong Chi-fung, born 13 October 1996, Hong Kong. Democracy campaigner since age 14; leader of the 2012 campaign against a Beijing-backed “national education” curriculum and a face of the 2014 Umbrella Movement.</dd>
        <dt>In prison since</dt><dd>November 2020, continuously.</dd>
        <dt>Earlier prison terms</dt><dd>2017, for unlawful assembly over the 2014 Civic Square protest (released on bail after about two months; the sentence was later overturned), and 2018–19, for contempt of court over the clearance of the Mong Kok protest site (served in separate periods, the last in May–June 2019).</dd>
        <dt>Latest sentence</dt><dd>Ten years, handed down 5 November 2026, for “conspiracy to collude with foreign forces” under the National Security Law.</dd>
        <dt>Previous release date</dt><dd>January 2027, at the end of his 4 year 8 month sentence in the Hong Kong 47 case.</dd>
        <dt>Possible release</dt><dd>Around 2036, when he will be about 40.</dd>
        <dt>The evidence</dt><dd>His own advocacy: meetings with foreign politicians, social media posts, op-eds and interviews, much of it from before the law existed.</dd>
        <dt>International response</dt><dd>Joint statement of 6 November 2026 by Australia, Canada, France, Germany, Italy, Japan, the Netherlands, New Zealand, the UK and the US condemning the sentence. Taiwan and the EU issued their own statements.</dd>
        <dt>Why the UK</dt><dd>The UK signed the 1984 Joint Declaration guaranteeing Hong Kong’s freedoms for fifty years, and has declared China in breach of it.</dd>
        <dt>UK Government</dt><dd>Says it remains “deeply concerned” by his continued imprisonment (written answer, 17 November 2026). Asked in writing whether the Chinese Ambassador has been summoned, the minister did not say (18 November 2026).</dd>
        <dt>The asks</dt><dd>The Foreign Secretary to summon the Chinese Ambassador and raise Joshua’s case; review the privileges of the Hong Kong Economic and Trade Office in London; sanction officials responsible for NSL prosecutions, with allies.</dd>
        <dt>Press contact</dt><dd>freejoshuawong.org/contact.html</dd>
      </dl>
      <p class="no-print" style="margin:26px 0 0;font-family:var(--label);font-size:13px;color:rgba(12,12,11,.65)">To save as a PDF, use your browser’s Print option and choose “Save as PDF”.</p>
    </div>

    <div class="res-grid">
      <div class="res" id="video"><div class="label">Campaign video</div><h3>What has the Prime Minister done for Joshua?</h3><p>Watch and download the video, with captions, and the share image.</p><p><a href="video.html">Go to the video page</a></p></div>
      <div class="res" id="press-kit"><div class="label">Press kit</div><h3>Photos &amp; stills</h3><p>Approved images of Joshua and stills from <em>Prisoner vs. Superpower</em>, cleared for editorial use.</p><p><a class="btn small-btn" href="contact.html?topic=press">Request images</a></p></div>
      <div class="res" id="briefs"><div class="label">Policy briefs</div><h3>Transnational repression</h3><p>How Beijing’s National Security Law reaches Hong Kongers in Britain, and what the UK can do about it.</p><span class="soon">Coming soon</span></div>
      <div class="res"><div class="label">Interviews</div><h3>Speak to us</h3><p>Interviews with the film’s producer and campaign spokespeople can be arranged.</p><p><a class="btn small-btn" href="contact.html?topic=interview">Request an interview</a></p></div>
    </div>
"""

# Campaign press releases, newest first: (date, title, summary, url or "")
RELEASES = [
    ("4 Nov 2026", "Ahead of Joshua Wong’s sentencing, cross-party MPs urge Government to summon Chinese Ambassador",
     "Issued the evening before sentencing, with comment from Andrew Duncan, Nathan Law, Sir Iain Duncan Smith MP and James Naish MP. <a href=\"press/2026-11-04-joshua-wong-sentencing-press-release.pdf\" download>Download the release (PDF)</a>",
     "press/2026-11-04-joshua-wong-sentencing-press-release.pdf"),
]

def releases_html():
    if not RELEASES:
        return """<div class="empty-rel"><h3>Press releases will appear here</h3><p>The campaign’s statements and releases will be published on this page, newest first. For comment or interviews, <a href="contact.html?topic=press">contact us</a>.</p></div>"""
    out = ""
    for d, t, summ, u in RELEASES:
        out += f"""<div class="rel"><div class="d">{d}</div><div><div class="type">Press release</div><h3>{'<a href="'+u+'">'+t+'</a>' if u else t}</h3><p>{summ}</p></div></div>"""
    return out

# ---------------- TAKE ACTION ----------------
def mp_box(dark=False):
    return f"""<form class="pcbox{' on-dark' if dark else ''}" data-mp novalidate>
      <label for="pc-{'h' if dark else 'a'}">Your postcode</label>
      <div class="pc-row"><input id="pc-{'h' if dark else 'a'}" name="pc" autocomplete="postal-code" placeholder="e.g. SW1A 1AA" required>
      <button type="submit" class="btn{' dark' if not dark else ''}">Find my MP and write</button></div>
      <p class="pc-err" hidden></p>
      <div class="pc-ok" hidden>
        <p class="pc-mp"></p>
        <p class="pc-links"><a class="btn pc-mail" href="#">Open the email</a> <span class="pc-or">or open in <a class="pc-alt pc-gmail" href="#" target="_blank" rel="noopener">Gmail</a> · <a class="pc-alt pc-outlook" href="#" target="_blank" rel="noopener">Outlook</a></span></p>
        <p class="pc-pasted" hidden>We’ve also copied the letter. If your email opens empty, paste it in.</p>
        <p class="pc-tip">The letter is filled in for you. Add your name and full address at the bottom (MPs only reply to their own constituents), then send. If no email opens, <button type="button" class="pc-copy">copy the letter</button> and send it to <b class="pc-addr"></b>.</p>
      </div>
      <p class="pc-note">Your postcode is used only to look up your MP on UK Parliament’s website. We don’t see or store it, or anything you send.</p>
    </form>"""

def act():
    return head("Take action", "Write to your MP about Joshua Wong and share his story.", "act.html") + nav("act.html") + page_head(
        "Take action", "Don’t let him <em>be forgotten</em>",
        "“The only thing I worry about is that people will forget Hong Kong.” Joshua, in a letter to a friend from prison, published by <a href=\"https://www.theguardian.com/world/2026/nov/05/joshua-wong-hong-kong-prison-letters-sentenced-10-years\" target=\"_blank\" rel=\"noopener\"><em>The Guardian</em></a>, 5 November 2026.") + """
<section style="border-top:0;padding-top:30px" id="mp">
  <div class="wrap">
    <div class="mp" style="margin-top:0">
      <div>
        <div class="label" style="color:#6f6a2a">In the UK</div>
        <h3>Tell your MP: summon China’s Ambassador</h3>
        <p>Two minutes. We’ve written the letter, asking your MP to urge the Foreign Secretary to summon the Chinese Ambassador. Put in your postcode and we’ll find your MP and open an email to them with the letter already filled in.</p>
        """ + mp_box() + """
      </div>
      <div>
        <div class="tpl" id="tpl">""" + LETTER + """</div>
        <button class="copy" type="button" data-target="tpl">Copy letter</button>
      </div>
    </div>
  </div>
</section>

<section id="share">
  <div class="wrap">
    <div class="share" style="margin-top:0">
      <div>
        <div class="label">Share</div>
        <h3>Post it.<br><span>Tag your MP.</span></h3>
        <p class="lede" style="font-size:18px">Copy a line, add your MP’s handle, and use #FreeJoshuaWong and #JoshuaWong.</p>
        <div data-share data-url="https://freejoshuawong.org" data-text="Joshua Wong spoke up for Hong Kong. Now he faces ten more years."></div>
      </div>
      <div>
        <div class="post"><p>Joshua Wong was two months from freedom. Hong Kong has given him ten more years for speaking up to foreign parliaments. <b>#FreeJoshuaWong #JoshuaWong</b></p><button class="copy" type="button">Copy</button></div>
        <div class="post"><p>Britain guaranteed Hong Kong’s freedoms for fifty years. Joshua Wong only asked us to keep our word. <b>#FreeJoshuaWong #JoshuaWong</b></p><button class="copy" type="button">Copy</button></div>
        <div class="post"><p>He has been in prison since he was 24. He may not walk free until he is 40. <b>#FreeJoshuaWong #JoshuaWong</b></p><button class="copy" type="button">Copy</button></div>
      </div>
    </div>

    <div class="voices" style="margin-top:70px">
      <div class="voice"><q>The harsh sentence on baseless charges against Joshua Wong is cruel and unjust.</q><div class="by"><a href="https://www.hrw.org/news/2026/11/05/hong-kong-joshua-wong-gets-nearly-10-more-years-in-prison" target="_blank" rel="noopener">Elaine Pearson</a><small>Asia Director, Human Rights Watch</small></div></div>
      <div class="voice"><q>Joshua Wong’s bravery in speaking truth to power should be commended.</q><div class="by"><a href="https://www.amnestyusa.org/press-releases/hong-kong-cruel-joshua-wong-sentence-a-grim-reminder-of-authorities-disdain-for-human-rights/" target="_blank" rel="noopener">Sarah Brooks</a><small>Amnesty International</small></div></div>
      <div class="voice"><q>Joshua Wong deserves to be honoured and applauded, not jailed.</q><div class="by"><a href="https://www.spectator.com.au/?p=10947071" target="_blank" rel="noopener">Benedict Rogers</a><small>Hong Kong Watch, in The Spectator</small></div></div>
    </div>
    <div class="hashtag">#FreeJoshuaWong<small>and #JoshuaWong</small></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head">
      <div><div class="label">What Britain should do</div><h2 class="sec">Three <em>asks</em></h2></div>
    </div>
    """ + ASKS + """
  </div>
</section>
""" + footer()

# ---------------- PARLIAMENT ----------------
# kind: commons | lords | written | report | event
RECORD = [
    ("2026-11-19", "written", "Sanctions on the officials responsible?", "Written question · Richard Holden MP",
     "Richard Holden MP asked whether the Foreign Secretary will assess the merits of targeted sanctions on the Chinese and Hong Kong officials responsible for jailing Joshua and other activists. Answering on 19 November, Minister Chris Elmore pointed to the joint statement issued with international partners after the sentence and said it “would not be appropriate for me to speculate on future measures”.",
     "https://questions-statements.parliament.uk/written-questions/detail/2026-11-11/42157", "Parliamentary answer", ""),
    ("2026-11-18", "written", "Seven questions, one cross-reference", "Written answers · Chris Elmore MP, Foreign Office minister",
     "On 18 November the minister answered the seven questions tabled on 10 November by Richard Holden MP, Alex Barros-Curtis MP and Marie Rimmer MP, including whether the Foreign Secretary has summoned the Chinese Ambassador, what steps he is taking to secure Joshua’s release, and whether sanctions will be considered. Each answer simply referred to his answer to Alex Barros-Curtis on 17 November. None said whether the Ambassador has been summoned.",
     "https://questions-statements.parliament.uk/written-questions/detail/2026-11-10/41576", "The answer on the Ambassador", ""),
    ("2026-11-17", "written", "“Deeply concerned”", "Written question · Alex Barros-Curtis MP",
     "Alex Barros-Curtis MP asked what discussions the Foreign Secretary has had with international partners on Joshua’s case. Minister Chris Elmore said the Government remains “deeply concerned by Joshua Wong's continued imprisonment” and pointed to the joint statement issued with international partners after the sentence.",
     "https://questions-statements.parliament.uk/written-questions/detail/2026-11-04/41010", "Parliamentary answer", ""),
    ("2026-11-11", "letter", "“A treaty broken without cost invites the next breach”", "Letter to The Times · Eight MPs and peers",
     "The day after the urgent question, Emily Darlington MP, Lord Alton, Lord Patten and five other MPs and peers wrote to The Times asking the Government to summon the Chinese Ambassador, sanction those responsible and tell Parliament what further consequences will follow.",
     "letters/times-letter-nov-2026.html", "Read the letter", ""),
    ("2026-11-10", "commons", "“Not, sadly, like the islanders Joshua Wong and Jimmy Lai”", "Commonwealth Heads of Government Meeting statement · House of Commons",
     "The same day, responding to the Government’s statement on the Commonwealth summit, Shadow Foreign Secretary Tom Tugendhat contrasted the dignity owed to Caribbean islanders with the treatment of Joshua and Jimmy Lai in Hong Kong.",
     "#exchange-tugendhat", "Watch the clip", ""),
    ("2026-11-10", "commons", "“Calling for Joshua Wong’s release”", "Urgent question on China · House of Commons",
     "At an urgent question secured by Sir Iain Duncan Smith on China obtaining MPs’ phone and financial records, Emily Darlington MP asked the Government to summon the Chinese Ambassador and call for Joshua’s release, as it did for Jimmy Lai. Security Minister Dan Jarvis replied that the Government share the concerns about Joshua and Jimmy Lai. For the Opposition, Alicia Kearns MP said both remain imprisoned for speaking out for democracy. <a href=\"https://hansard.parliament.uk/Commons/2026-11-10/debates/E43553F9-3D50-41D2-844C-D23E5DCFBF96/ChinaBreachOfUKParliamentariansData\" target=\"_blank\" rel=\"noopener\">Read it in Hansard</a>",
     "#exchange-nov", "Watch the clip", ""),
    ("2026-11-10", "written", "Seven written questions in one day", "Written questions · Richard Holden MP, Alex Barros-Curtis MP, Marie Rimmer MP",
     "After the sentence, three MPs tabled seven questions to the Foreign Secretary, including whether he has summoned the Chinese Ambassador, what diplomatic steps he is taking to secure Joshua’s release, and whether the Government will consider sanctions on the officials responsible. They were answered on 18 November (see above).",
     "https://commonsbusiness.parliament.uk/Document/108853/Html?subType=Standard", "Questions tabled", ""),
    ("2026-11-09", "written", "Named in a Lords answer on a ministerial visit", "Written question · Lord Alton (HL4687)",
     "Lord Alton asked what the minister raised during her visit to Hong Kong on 29 October. Answering, Baroness Winterton said she raised concerns including Jimmy Lai’s continued detention, and pointed to the six-monthly report, which highlights Joshua’s case.",
     "https://questions-statements.parliament.uk/written-questions/detail/2026-10-29/HL4687", "Parliamentary answer", ""),
    ("2026-11-03", "written", "What has the Foreign Secretary said to his Chinese counterpart?", "Written question · Catherine West MP",
     "Catherine West MP asked what recent discussions the Foreign Secretary has had with his Chinese counterpart on Joshua. Minister Chris Elmore simply referred her to his earlier answer to James Naish MP.",
     "https://questions-statements.parliament.uk/written-questions/detail/2026-10-27/38519", "Parliamentary answer", ""),
    ("2026-11-03", "written", "The Chinese Embassy and Joshua’s treatment", "Written question · Alex Barros-Curtis MP",
     "Alex Barros-Curtis MP asked whether Joshua’s treatment would be taken into account in any further approvals for the proposed Chinese Embassy at Royal Mint Court. Minister Chris Elmore replied that the planning decision was taken independently and that the Government does not comment on ongoing legal proceedings.",
     "https://questions-statements.parliament.uk/written-questions/detail/2026-10-22/37356", "Parliamentary answer", ""),
    ("2026-10-28", "written", "How often has Joshua’s case been raised?", "Written questions · James Naish MP",
     "James Naish MP asked what steps the Foreign Office has taken to raise Joshua’s case with Chinese counterparts since 1 September, on how many occasions and at what level, and whether the next six-monthly report would set out the Government’s assessment of his case. Answering on 28 October, Minister Chris Elmore said the further charges reinforce concerns about national security legislation and that the UK continues to call for the law’s repeal. He did not say how often the case had been raised, or at what level.",
     "https://questions-statements.parliament.uk/written-questions/detail/2026-10-20/36419", "Parliamentary answer", ""),
    ("2026-10-22", "report", "Six-monthly Report on Hong Kong", "Foreign Secretary · Report to Parliament",
     "The Government’s report for January to June 2026 cites developments in Joshua’s case as reinforcing concerns about the broad use of national security legislation.",
     "https://www.gov.uk/government/publications/six-monthly-report-on-hong-kong-january-to-june-2026/six-monthly-report-on-hong-kong-1-january-to-30-june-2026", "GOV.UK", ""),
    ("2026-10-13", "event", "The film is shown in Parliament", "Committee Room 15 · Houses of Parliament",
     "<em>Joshua: Prisoner vs. Superpower</em> was first shown to parliamentarians on Joshua’s 30th birthday.",
     "film.html", "Watch the film", ""),
    ("2026-09-13", "letter", "Open letter to the Prime Minister", "Open letter · 31 MPs, peers and rights leaders",
     "MPs and peers from across the parties, former Foreign Secretaries and human rights leaders asked the Prime Minister to call in the Chinese Ambassador and raise Joshua’s case. No reply has been made public.",
     "letters/open-letter-prime-minister-sept-2026.html", "Read the letter", ""),
    ("2026-09-08", "written", "Six questions, one answer", "Written questions · Gregory Stafford MP",
     "Gregory Stafford MP asked six questions on Joshua’s case, including what representations the UK has made to the Hong Kong authorities and its assessment of the rule of law in his case. Minister Chris Elmore gave a single answer: the Government continues to monitor the case, reports on it in the six-monthly reports, and repeats its call for the National Security Law to be repealed.",
     "https://qna.files.parliament.uk/qnadailyreports/Written-Questions-Answers-Statements-Daily-Report-Commons-2026-09-08.pdf", "Daily Report, p.478", ""),
    ("2026-09-01", "commons", "“Enough is enough”", "Foreign Office Questions · House of Commons",
     "Sir Iain Duncan Smith urged the Government to raise Joshua’s case with Beijing. Foreign Secretary Ed Miliband said he would take it up. No update has been made public since.",
     "#exchange", "Watch the exchange", PROMISE_DATE),
    ("2025-12-17", "lords", "Named in the Lords after Jimmy Lai’s conviction", "Jimmy Lai Conviction · House of Lords",
     "Lord Alton asked what the Government is doing to raise the cases of pro-democracy prisoners “such as Joshua Wong and Andy Li”.",
     "https://hansard.parliament.uk/Lords/2025-12-17/debates/6CF28FA8-3A92-4C34-808D-A4BDD6322D85/JimmyLaiConviction", "Read the debate", ""),
    ("2025-10-28", "commons", "Hong Kong human rights violations", "Foreign Office Questions · Luke Akehurst MP",
     "At questions led by Alison Bennett MP, Luke Akehurst MP raised Joshua’s rearrest and the new charges against him, and asked whether the National Security Law is being used to erode rights.",
     "https://hansard.parliament.uk/Commons/2025-10-28/debates/FCFA35AB-A007-4F6D-BF8A-3D80321D4046/HongKongHumanRightsViolations", "Hansard", ""),
    ("2025-10-23", "report", "His re-arrest on the record", "Foreign Secretary · Report to Parliament",
     "The six-monthly report for January to June 2025 records Joshua’s re-arrest on 6 June on suspicion of collusion with foreign forces.",
     "https://www.gov.uk/government/publications/six-monthly-report-on-hong-kong-january-to-june-2025/six-monthly-report-on-hong-kong-1-january-to-30-june-2025", "GOV.UK", ""),
    ("2025-07-03", "written", "The UK is “deeply concerned”", "Written question · Alicia Kearns MP",
     "Answering Alicia Kearns MP, the Foreign Office said it was deeply concerned by the further charges against Joshua.",
     "https://questions-statements.parliament.uk/written-questions/detail/2025-06-26/63014", "Parliamentary answer", ""),
    ("2024-12-19", "lords", "China: human rights and security", "Debate · House of Lords · Lord Alton",
     "Opening a Lords debate on China, Lord Alton urged the Government to condemn the jailing of the Hong Kong pro-democracy leaders, including Joshua and Benny Tai.",
     "https://hansard.parliament.uk/Lords/2024-12-19/debates/EC75B825-49A1-4C49-888E-BC9DD4576DB1/ChinaHumanRightsAndSecurity", "Read the debate", ""),
    ("2024-11-28", "written", "Raised during a ministerial visit?", "Written question · Lord Alton (HL2535)",
     "Lord Alton asked whether the minister raised political prisoners, including Joshua, Gwyneth Ho, Jimmy Lai and Owen Chow, during her visit to Hong Kong. Answered by Baroness Chapman.",
     "https://questions-statements.parliament.uk/written-questions/detail/2024-11-14/HL2535", "Parliamentary answer", ""),
    ("2020-12-07", "commons", "Urgent question on Joshua’s sentencing", "Urgent question · Alyn Smith MP",
     "The Commons held an urgent question on the sentencing of Joshua, Agnes Chow and Ivan Lam for their part in the 2019 protests.",
     "https://hansard.parliament.uk/Commons/2020-12-07/debates/B5D3C0DB-2F7C-48F4-91B0-0BD2E87227CE/HongKongSentencingOfPro-DemocracyActivists", "Hansard", ""),
]
KINDS = [("commons", "Commons"), ("lords", "Lords"), ("written", "Written questions"), ("letter", "Letters"), ("report", "Government reports"), ("event", "In Parliament")]
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# ===== Asked and answered: the accountability tracker (home page and Newsroom) =====
# (date asked, status, what was asked, who/when detail, link, link text). Newest first. Status: "none" | "dodged" | "noupdate" | "weak" | "due".
TRACKER = [
    ("2026-11-11", "weak", "Will the UK consider sanctions on those responsible?",
     "Written question from Richard Holden MP. Answering on 19 November, the minister said it “would not be appropriate for me to speculate on future measures”.",
     "https://questions-statements.parliament.uk/written-questions/detail/2026-11-11/42157", "The answer"),
    ("2026-11-10", "dodged", "Has the Foreign Secretary summoned the Chinese Ambassador over Joshua?",
     "Written question from Alex Barros-Curtis MP, one of seven tabled after the sentence. Answered on 18 November with a reference to another answer, which does not say whether the Ambassador has been summoned.",
     "https://questions-statements.parliament.uk/written-questions/detail/2026-11-10/41576", "The answer"),
    ("2026-11-10", "weak", "Summon the Ambassador and call for Joshua’s release, as the Government did for Jimmy Lai",
     "Emily Darlington MP in the Commons. The Security Minister said the Government “share the concerns” but made no commitment.",
     "parliament.html#exchange-nov", "Watch the exchange"),
    ("2026-11-03", "weak", "Will Joshua’s treatment count in decisions on China’s new embassy?",
     "Written question from Alex Barros-Curtis MP. The Government said it does not comment on ongoing legal proceedings.",
     "https://questions-statements.parliament.uk/written-questions/detail/2026-10-22/37356", "The answer"),
    ("2026-09-13", "none", "Summon China’s Ambassador to raise Joshua’s case",
     "<a href=\"letters/open-letter-prime-minister-sept-2026.html\">The open letter to the Prime Minister</a>, Andy Burnham, signed by 31 MPs, peers and rights leaders. No reply.",
     "letters/open-letter-prime-minister-sept-2026.html", "Read the letter"),
    ("2026-09-08", "weak", "What has the UK said to Hong Kong about Joshua’s case?",
     "Six written questions from Gregory Stafford MP. One answer for all six: the Government “continues to monitor” the case.",
     "https://qna.files.parliament.uk/qnadailyreports/Written-Questions-Answers-Statements-Daily-Report-Commons-2026-09-08.pdf", "Read the answer (p.478)"),
    (PROMISE_DATE, "noupdate", "Take Joshua’s case up with China",
     "Sir Iain Duncan Smith in the Commons. The Foreign Secretary, Ed Miliband, said he would. No update has been made public.",
     "parliament.html#exchange", "Watch the exchange"),
]
STATUS = {"none": "No reply", "dodged": "Not answered", "noupdate": "No update", "weak": "No action", "due": "Awaiting answer"}

def tracker(h="Asked and answered"):
    rows = ""
    for d, st, ask, detail, url, link in TRACKER:
        y, m, dd = d.split("-")
        when = f"{int(dd)} {MONTHS[int(m)-1]}"
        ext = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        rows += f"""
      <div class="wait-row">
        <div class="wait-n"><span data-since="{d}">0</span><small>days since {when}</small></div>
        <div><em class="tk-st st-{st}">{STATUS[st]}</em><h4>{ask}</h4><p>{detail} <a href="{url}"{ext}>{link}</a></p></div>
      </div>"""
    return f"""<div class="waiting h4-wait tracker" id="asked">
      <h3>{h}</h3>
      <p class="tk-lede">What ministers have been asked about Joshua since September, and what they have said.</p>{rows}
      <p class="tk-foot">For comparison: when Jimmy Lai was convicted on 15 December 2025, the Foreign Office <a href="https://www.gov.uk/government/news/statement-fcdo-summons-chinese-ambassador-15-december-2025" target="_blank" rel="noopener">summoned the Chinese Ambassador the same day</a>. Joshua was sentenced <b data-since="2026-11-05">0</b> days ago. There has been no public word of the Ambassador being summoned over his case.</p>
    </div>"""

VIDEOS = [
    ("film.html", "Film", "Joshua: Prisoner vs. Superpower", "The new short film, first shown in Parliament on 13 October 2026.", "images/film-poster.jpg?v=2", False),
    ("#exchange-nov", "House of Commons · 10 Nov 2026", "Emily Darlington MP", "Asks the Government to call for Joshua’s release, five days after his sentence.", "images/commons-2026-11-10-poster.jpg", False),
    ("#exchange-kearns", "House of Commons · 10 Nov 2026", "Alicia Kearns MP", "For the Opposition: Joshua and Jimmy Lai remain imprisoned for speaking out for democracy.", "images/commons-2026-11-10-kearns-poster.jpg", False),
    ("https://podcasts.apple.com/gb/podcast/today-in-focus/id1440133626?i=1000801652639", "The Guardian · Today in Focus · 13 Nov 2026", "Teen prodigy, Netflix star, prisoner", "Podcast: Nathan Law and journalist Danny Vincent on Joshua’s story and his new sentence.", "images/covers/guardian-podcast.jpg", True),
    ("https://www.youtube.com/live/iw5a5aQKgNM?t=2400", "Sky News · 5 Nov 2026", "Nathan Law on Sky News", "On the day of the sentence, Nathan tells Yalda Hakim that democracy and human rights are “losing ground globally”.", "images/stills/sky-nathan.jpg", True),
    ("film.html#badenoch", "Conservative rally · 3 Nov 2026", "Kemi Badenoch on China’s political prisoners", "Two days before the sentence, the Conservative leader says she would be “going and getting those people released”.", "images/stills/badenoch-rally.jpg", False),
    ("https://www.youtube.com/watch?v=gwQ1bK0KSJE", "Byline Times TV · 26 Oct 2026", "China versus Joshua Wong", "Video: filmmaker Andrew Duncan tells Joshua’s story to Adrian Goldberg.", "images/stills/byline-andrew.jpg", True),
    ("#exchange-tugendhat", "House of Commons · 10 Nov 2026", "Tom Tugendhat MP", "The Shadow Foreign Secretary names Joshua in the Commonwealth summit statement.", "images/commons-2026-11-10-tugendhat-poster.jpg", False),
    ("#exchange", "House of Commons · 1 Sep 2026", "Duncan Smith and the Foreign Secretary", "The exchange at Foreign Office Questions, the day before Joshua’s plea.", "images/commons-poster.jpg", False),
    ("https://www.channel4.com/news/hong-kong-pro-democracy-activist-joshua-wong-pleads-guilty-to-colluding-with-foreign-entities", "Channel 4 News · 2 Sep 2026", "Joshua pleads guilty", "Channel 4 News reports on the plea, with analysis on China and the UK.", "images/stills/c4-plea.jpg", True),
    ("https://pelosi.house.gov/news/press-releases/pelosi-calls-joshua-wongs-freedom-house-floor-we-want-be-sure-they-know-we", "US House of Representatives · 2 Sep 2026", "Pelosi on the House floor", "Speaker Emerita Nancy Pelosi calls for Joshua’s freedom.", "images/stills/pelosi-floor.jpg", True),
]

def video_cards(skip_film=False):
    cards = ""
    for url, kicker, title, blurb, img, ext in VIDEOS:
        if skip_film and url == "film.html":
            continue
        if url.startswith("#"):
            url = "parliament.html" + url
        tgt = ' target="_blank" rel="noopener"' if ext else ""
        art = f'<img src="{img}" alt="" loading="lazy">' if img else f'<span class="vc-mark">{kicker.split(" · ")[0]}</span>'
        cards += f"""<a class="vcard{" has-cover" if "images/covers" in img else ""}" href="{url}"{tgt}>
        <div class="vc-img">{art}<span class="vc-play"></span>{'<span class="vc-ext">Opens on '+ ('YouTube' if 'youtube' in url else 'Apple Podcasts' if 'podcasts.apple' in url else 'Facebook' if 'facebook.com' in url else 'X' if 'x.com/' in url else 'the Guardian' if 'theguardian.com' in url else 'their site') +'</span>' if ext else ''}</div>
        <div class="vc-k">{kicker}</div><h3>{title}</h3><p>{blurb}</p></a>"""
    return cards

def parliament():
    def dfmt(d):
        y, m, dd = d.split("-"); return f"{int(dd)} {MONTHS[int(m)-1]} {y}"
    counts = {k: sum(1 for r in RECORD if r[1] == k) for k, _ in KINDS}
    label = dict(KINDS)
    chips = '<button class="chip" data-k="all" aria-pressed="true">Everything <i>' + str(len(RECORD)) + '</i></button>' + "".join(
        f'<button class="chip" data-k="{k}" aria-pressed="false">{t} <i>{counts[k]}</i></button>' for k, t in KINDS if counts[k])
    rows = ""
    for d, k, title, who, body, url, link, since in RECORD:
        ext = url.startswith("http")
        tgt = ' target="_blank" rel="noopener"' if ext else ""
        wait = f'<div class="rec-wait"><b data-since="{since}">—</b> days, no update</div>' if since else ""
        rows += f"""<article class="rec" data-k="{k}"{' id="rec-'+d+'"' if since else ''}>
        <div class="rec-d"><span>{dfmt(d)}</span><em class="k-{k}">{label[k]}</em></div>
        <div><div class="rec-who">{tag_names(who)}</div><h3>{title}</h3><p>{body}</p>{wait}<a class="src" href="{url}"{tgt}>{link}</a></div>
      </article>"""
    return head("Parliament", "Every time Joshua Wong’s case has been raised at Westminster, with the clips.", "parliament.html") + nav("parliament.html") + page_head(
        "Parliament", "On the <em>record</em>",
        "Every time Joshua’s case has been raised at Westminster, with the clips to watch.") + """
<section class="parl-feature" id="exchange-nov" style="border-top:0;padding-top:10px">
  <div class="wrap">
    <div class="px">
      <div class="px-vid">
        <div class="screen vid"><video controls preload="none" playsinline poster="images/commons-2026-11-10-poster.jpg"><source src="media/commons-2026-11-10.mp4" type="video/mp4">Your browser can’t play this video.</video></div>
        <p class="px-cap">BBC Parliament, House of Commons, urgent question on China, 10 November 2026.</p>
      </div>
      <div class="px-side">
        <div class="px-when">10 November 2026 · House of Commons · Latest</div>
        <div class="px-sp">
          <div class="px-name">Emily Darlington MP</div>
          <div class="px-role">Labour, Milton Keynes Central</div>
          <p>At an urgent question secured by Sir Iain Duncan Smith on China obtaining MPs’ data, five days after Joshua was sentenced, she asked the Government to summon the Chinese Ambassador and call for his release, as it did for Jimmy Lai. The next day she and seven other MPs and peers made the same case in <a href="letters/times-letter-nov-2026.html">a letter to <em>The Times</em></a>.</p>
        </div>
        <div class="px-sp">
          <div class="px-name">Dan Jarvis MP</div>
          <div class="px-role">Minister of State for Security</div>
          <p>Replying to her: “The Government share the concerns about Mr Wong and Jimmy Lai.”</p>
        </div>

        <p class="px-link"><a href="https://hansard.parliament.uk/Commons/2026-11-10/debates/E43553F9-3D50-41D2-844C-D23E5DCFBF96/ChinaBreachOfUKParliamentariansData" target="_blank" rel="noopener">Read the exchange in Hansard</a></p>
        <div data-share data-url="https://freejoshuawong.org/parliament.html#exchange-nov" data-text="In the Commons, Emily Darlington MP asked the Government to call for Joshua Wong’s release. #FreeJoshuaWong #JoshuaWong"></div>
      </div>
    </div>
  </div>
</section>

<section class="parl-feature" id="exchange-kearns">
  <div class="wrap">
    <div class="px">
      <div class="px-vid">
        <div class="screen vid"><video controls preload="none" playsinline poster="images/commons-2026-11-10-kearns-poster.jpg"><source src="media/commons-2026-11-10-kearns.mp4" type="video/mp4">Your browser can’t play this video.</video></div>
        <p class="px-cap">BBC Parliament, House of Commons, urgent question on China, 10 November 2026.</p>
      </div>
      <div class="px-side">
        <div class="px-when">10 November 2026 · House of Commons · For the Opposition</div>
        <div class="px-sp">
          <div class="px-name">Alicia Kearns MP</div>
          <div class="px-role">Conservative, Rutland and Stamford · Shadow Minister</div>
          <p>Responding for the Opposition in the same urgent question, she reminded the House that Jimmy Lai and Joshua Wong remain imprisoned in Hong Kong for speaking out for democracy.</p>
        </div>
        <p class="px-link"><a href="https://hansard.parliament.uk/Commons/2026-11-10/debates/E43553F9-3D50-41D2-844C-D23E5DCFBF96/ChinaBreachOfUKParliamentariansData" target="_blank" rel="noopener">Read it in Hansard</a></p>
        <div data-share data-url="https://freejoshuawong.org/parliament.html#exchange-kearns" data-text="Alicia Kearns MP in the Commons: Jimmy Lai and Joshua Wong remain imprisoned for speaking out for democracy. #FreeJoshuaWong #JoshuaWong"></div>
      </div>
    </div>
  </div>
</section>

<section class="parl-feature" id="exchange-tugendhat">
  <div class="wrap">
    <div class="px">
      <div class="px-vid">
        <div class="screen vid"><video controls preload="none" playsinline poster="images/commons-2026-11-10-tugendhat-poster.jpg"><source src="media/commons-2026-11-10-tugendhat.mp4" type="video/mp4">Your browser can’t play this video.</video></div>
        <p class="px-cap">BBC Parliament, House of Commons, statement on the Commonwealth Heads of Government Meeting, 10 November 2026.</p>
      </div>
      <div class="px-side">
        <div class="px-when">10 November 2026 · House of Commons · Shadow Foreign Secretary</div>
        <div class="px-sp">
          <div class="px-name">Tom Tugendhat MP</div>
          <div class="px-role">Conservative, Tonbridge · Shadow Foreign Secretary</div>
          <p>Responding to the Government’s statement on the Commonwealth summit, he asked about Chinese influence in the Caribbean, so that islanders there are treated with dignity, “not, sadly, like the islanders Joshua Wong and Jimmy Lai in Hong Kong”.</p>
        </div>
        <p class="px-link"><a href="https://hansard.parliament.uk/Commons/2026-11-10/debates/98BED7DA-2BAA-487C-9BE5-EB7CD6C6657C/CommonwealthHeadsOfGovernmentMeeting" target="_blank" rel="noopener">Read it in Hansard</a></p>
        <div data-share data-url="https://freejoshuawong.org/parliament.html#exchange-tugendhat" data-text="Tom Tugendhat MP raises Joshua Wong in the Commons. #FreeJoshuaWong #JoshuaWong"></div>
      </div>
    </div>
  </div>
</section>

<section class="parl-feature" id="exchange">
  <div class="wrap">
    <div class="px">
      <div class="px-vid">
        <div class="screen vid"><video controls preload="none" playsinline poster="images/commons-poster.jpg"><source src="media/commons-2026-09-01.mp4" type="video/mp4">Your browser can’t play this video.</video></div>
        <p class="px-cap">BBC Parliament, House of Commons, Foreign Office Questions, 1 September 2026.</p>
      </div>
      <div class="px-side">
        <div class="px-when">1 September 2026 · House of Commons</div>
        <div class="px-sp">
          <div class="px-name">Sir Iain Duncan Smith</div>
          <div class="px-role">Conservative, Chingford and Woodford Green</div>
          <p>Asked the Government to raise Joshua’s case with Beijing. Twelve days later he was among 31 MPs, peers and rights leaders who signed <a href="letters/open-letter-prime-minister-sept-2026.html">an open letter to the Prime Minister</a>.</p>
        </div>
        <div class="px-sp">
          <div class="px-name">Ed Miliband</div>
          <div class="px-role">Foreign Secretary</div>
          <p>Said he would take up Joshua’s case.</p>
        </div>
        <div class="px-count"><b """ + 'data-since="' + PROMISE_DATE + '"' + """>—</b><span>days since that promise.<br>No update has been made public.</span></div>
        <div data-share data-url="https://freejoshuawong.org/parliament.html" data-text="The Foreign Secretary promised to take up Joshua Wong’s case. No update since. #FreeJoshuaWong #JoshuaWong"></div>
      </div>
    </div>
  </div>
</section>

<section class="parl-more">
  <div class="wrap">
    <a class="to-socials" href="film.html#watch"><b>Watch and listen</b><span>The film, interviews and podcasts about Joshua are on the Watch page</span></a>
  </div>
</section>

<section class="parl-record">
  <div class="wrap">
    <div class="sec-head"><div><div class="label">The record</div><h2 class="sec">Raised at <em>Westminster</em></h2></div></div>
    <div class="filters rec-bar" role="group" aria-label="Filter the record">""" + chips + """</div>
    <div class="recs">""" + rows + """</div>
    <p class="rec-note">Know of a mention we’ve missed? <a href="contact.html?topic=parliament">Tell us</a>.</p>
  </div>
</section>
""" + CTA.replace("{up}", "") + footer()

# ---------------- VOICES ----------------
def gov_section():
    import html as _h, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import quotecards
    V = [v for v in quotecards.load_voices() if v["kind"] == "government" or v.get("gov")]
    V.sort(key=lambda v: (v.get("country") != "UK", "" if False else v["date"]), reverse=False)
    uk = sorted([v for v in V if v.get("country") == "UK"], key=lambda v: v["date"], reverse=True)
    rest = sorted([v for v in V if v.get("country") != "UK"], key=lambda v: v["date"], reverse=True)
    def dfmt(d):
        y, m, dd = d.split("-"); return f"{int(dd)} {MONTHS[int(m)-1]} {y}"
    def row(v):
        ext = ' target="_blank" rel="noopener"' if v["url"].startswith("http") else ""
        src = "As reported by " + v["via"] if v.get("via") else ("Hansard" if "hansard" in v["url"] else "Read the report" if "six-monthly-report" in v["url"] else "See the post" if "On X" in v.get("where", "") else "Read the statement")
        return f"""<div class="gov-row"><div class="gov-d">{dfmt(v["date"])}<span>{_h.escape(v.get("country",""))}</span></div><div><blockquote>“{_h.escape(v["quote"])}”</blockquote><div class="gov-by"><b>{_h.escape(v["who"])}</b> · {_h.escape(v["role"])}</div><a class="src" href="{_h.escape(v["url"])}"{ext}>{src}</a></div></div>"""
    return f"""<section class="gov-sec" id="governments">
  <div class="wrap">
    <div class="v-sec"><h2 class="sec">What governments <em>have said</em></h2><p>Official statements on Joshua’s case, starting with the UK Government. For every question put to UK ministers and their answers, see <a href="parliament.html">Parliament</a>.</p></div>
    <h3 class="gov-h">UK Government</h3>
    <div class="gov-list">{"".join(row(v) for v in uk)}</div>
    <h3 class="gov-h">Other governments and the EU</h3>
    <div class="gov-list">{"".join(row(v) for v in rest)}</div>
  </div>
</section>
"""

def voices():
    return head("Voices", "What parliamentarians, governments and human rights leaders are saying about Joshua Wong.", "voices.html") + nav("voices.html") + page_head(
        "Voices", "They are <em>speaking up</em>",
        "Parliamentarians, governments and human rights leaders, in their own words. Every quote links to where it was said.") + """
<section class="voices-page v-intro" style="border-top:0;padding-top:0">
  <div class="wrap">
    <div class="v-stats" id="v-stats"></div>
    <a class="to-socials" href="socials.html"><b>On social media</b><span>See what MPs, ministers, governments and campaigners are posting about Joshua</span></a>
  </div>
</section>
""" + gov_section() + """
<section class="voices-page v-rest" style="border-top:0">
  <div class="wrap">
    <div class="v-sec"><h2 class="sec">Parliamentarians and <em>rights groups</em></h2><p>In Parliament, in Congress, and from human rights organisations.</p></div>
    <div class="filters v-bar" role="group" aria-label="Filter voices">
      <button class="chip" data-k="all" aria-pressed="true">Everyone</button>
      <button class="chip" data-k="parliament" aria-pressed="false">Parliamentarians</button>
      <button class="chip" data-k="rights" aria-pressed="false">Rights groups</button>
    </div>
    <div class="vwall2" id="vwall"></div>
  </div>
</section>

<section class="add-voice">
  <div class="wrap">
    <div class="av">
      <div>
        <div class="label">Add your voice</div>
        <h2 class="sec">Post it. <em>Tag your MP.</em></h2>
        <p class="lede">Copy a line, add your MP’s handle, and post it with #FreeJoshuaWong and #JoshuaWong. If you are a parliamentarian or public figure and have spoken about Joshua, <a href="contact.html">tell us</a> and we’ll add you here.</p>
      </div>
      <div class="av-posts">
        <div class="post"><p>Joshua Wong was two months from freedom. Hong Kong has given him ten more years for speaking up to foreign parliaments. <b>#FreeJoshuaWong #JoshuaWong</b></p><button class="copy" type="button">Copy</button><a class="sh-x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=Joshua%20Wong%20was%20two%20months%20from%20freedom.%20Hong%20Kong%20has%20given%20him%20ten%20more%20years%20for%20speaking%20up%20to%20foreign%20parliaments.%20%23FreeJoshuaWong%20%23JoshuaWong&url=https%3A%2F%2Ffreejoshuawong.org">Post on X</a></div>
        <div class="post"><p>The Foreign Secretary promised to take up Joshua Wong’s case on 1 September. We’re still waiting. <b>#FreeJoshuaWong #JoshuaWong</b></p><button class="copy" type="button">Copy</button><a class="sh-x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=The%20Foreign%20Secretary%20promised%20to%20take%20up%20Joshua%20Wong%E2%80%99s%20case%20on%201%20September.%20We%E2%80%99re%20still%20waiting.%20%23FreeJoshuaWong%20%23JoshuaWong&url=https%3A%2F%2Ffreejoshuawong.org%2Fparliament.html">Post on X</a></div>
        <div class="post"><p>He has been in prison since he was 24. He may not walk free until he is 40. <b>#FreeJoshuaWong #JoshuaWong</b></p><button class="copy" type="button">Copy</button><a class="sh-x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=He%20has%20been%20in%20prison%20since%20he%20was%2024.%20He%20may%20not%20walk%20free%20until%20he%20is%2040.%20%23FreeJoshuaWong%20%23JoshuaWong&url=https%3A%2F%2Ffreejoshuawong.org">Post on X</a></div>
      </div>
    </div>
  </div>
</section>
""" + footer(0, '<script src="assets/voices.js"></script>\n')

# ---------------- ONE PAGE PER QUOTE (for sharing) ----------------
def quote_page(v):
    import html as _h
    e = _h.escape
    url = f"{SITE}/voices/{v['slug']}.html"
    title = f"“{v['quote']}” — {v['who']}"
    ext = v["url"].startswith("http")
    orig = v["url"] if ext else "../" + v["url"]
    watch = f'<a class="btn ghost" href="../{e(v["watch"])}">Watch the clip</a>' if v.get("watch") else ""
    page = head(title, f"{v['who']} on Joshua Wong. #FreeJoshuaWong #JoshuaWong", f"voices/{v['slug']}.html", 1)
    page = page.replace(f"{SITE}/images/share-card.jpg", f"{SITE}/images/quotes/{v['slug']}.jpg")
    return page + nav("voices.html", 1) + f"""
<section class="qpage" style="border-top:0">
  <div class="wrap">
    <div class="crumbs"><a href="../voices.html">Voices</a> &nbsp;/&nbsp; {e(v['who'])}</div>
    <figure class="vq qbig k-{e(v['kind'])}{' big' if len(v['quote']) < 40 else ' mid'}">
      <div class="vq-top"><span class="vq-where">{e(v['where'])}</span><span class="vq-date">{int(v['date'][8:])} {MONTHS[int(v['date'][5:7])-1]} {v['date'][:4]}</span></div>
      <blockquote>{e(v['quote'])}</blockquote>
      <figcaption><b>{e(v['who'])}</b><span>{e(v['role'])}{' · ' + e(v['country']) if v.get('country') and v['country'] != 'Global' else ''}</span></figcaption>
    </figure>
    <div data-share data-url="{url}" data-text="“{e(v['quote'])}” — {e(v['who'])}"></div>
    <p class="q-actions"><a class="btn" href="{e(orig)}"{' target="_blank" rel="noopener"' if ext else ''}>{'As reported by ' + e(v['via']) if v.get('via') else 'See where it was said'}</a>{watch}<a class="btn ghost" href="../voices.html">All voices</a></p>
    <p class="q-img"><a href="../images/quotes/{v['slug']}.jpg" download>Download this quote as an image</a> for Instagram or WhatsApp.</p>
  </div>
</section>
""" + footer(1)

# ---------------- SOCIALS ----------------
def socials():
    return head("Socials", "What MPs, ministers, governments and campaigners are posting about Joshua Wong.", "socials.html") + nav("socials.html") + page_head(
        "Socials", "#Free<wbr><em>JoshuaWong</em>",
        "What MPs, ministers, governments and campaigners are posting about Joshua. Every post links back to the original.") + """
<section class="socials-page" style="border-top:0;padding-top:0">
  <div class="wrap">
    <div id="s-lead"></div>
    <div class="s-head">
      <div class="v-stats" id="s-stats"></div>
      <div class="filters s-bar" role="group" aria-label="Filter posts" id="s-bar"></div>
    </div>
    <div class="s-wall" id="s-wall"></div>
    <p class="rec-note">Seen a post we’ve missed? <a href="contact.html">Send us the link</a>. We link to posts rather than embedding them, so your visit here isn’t tracked by social media companies.</p>
  </div>
</section>

<section class="add-voice">
  <div class="wrap">
    <div class="av">
      <div>
        <div class="label">Add your voice</div>
        <h2 class="sec">Post it. <em>Tag your MP.</em></h2>
        <p class="lede">Copy a line, add your MP’s handle, and post it with #FreeJoshuaWong and #JoshuaWong.</p>
      </div>
      <div class="av-posts">
        <div class="post"><p>Joshua Wong was two months from freedom. Hong Kong has given him ten more years for speaking up to foreign parliaments. <b>#FreeJoshuaWong #JoshuaWong</b></p><button class="copy" type="button">Copy</button><a class="sh-x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=Joshua%20Wong%20was%20two%20months%20from%20freedom.%20Hong%20Kong%20has%20given%20him%20ten%20more%20years%20for%20speaking%20up%20to%20foreign%20parliaments.%20%23FreeJoshuaWong%20%23JoshuaWong&url=https%3A%2F%2Ffreejoshuawong.org">Post on X</a></div>
        <div class="post"><p>The Foreign Secretary promised to take up Joshua Wong’s case on 1 September. We’re still waiting. <b>#FreeJoshuaWong #JoshuaWong</b></p><button class="copy" type="button">Copy</button><a class="sh-x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=The%20Foreign%20Secretary%20promised%20to%20take%20up%20Joshua%20Wong%E2%80%99s%20case%20on%201%20September.%20We%E2%80%99re%20still%20waiting.%20%23FreeJoshuaWong%20%23JoshuaWong&url=https%3A%2F%2Ffreejoshuawong.org%2Fparliament.html">Post on X</a></div>
      </div>
    </div>
  </div>
</section>
""" + footer(0, '<script src="assets/socials.js"></script>\n')

# ---------------- LETTER TO THE TIMES ----------------
TIMES_SIGNATORIES = ["Emily Darlington MP", "Bobby Dean MP", "Lord David Alton of Liverpool", "Lord Patten of Barnes",
    "Sir Geoffrey Nice KC", "Sir Malcolm Rifkind", "Lord Shinkwin", "Baroness Bennett of Manor Castle"]

def letter_times():
    sig = "".join(f"<li>{n} {party_tag(n)}</li>" for n in TIMES_SIGNATORIES)
    return head("Unjust prosecution: letter to The Times", "MPs and peers write to The Times: Britain should summon the Chinese ambassador, sanction those responsible and say what further consequences will follow.", "letters/times-letter-nov-2026.html", 1) + nav("newsroom.html", 1) + page_head(
        "", "Unjust <em>prosecution</em>",
        "A letter to the editor of The Times from MPs and peers across the parties, published on 11 November 2026.",
        crumbs='<a href="../newsroom.html#letters">Newsroom</a> &nbsp;/&nbsp; Letters') + """
<section class="letters letter-page" style="border-top:0">
  <div class="wrap">
    <div class="letter">
      <article class="paper">
        <div class="head">Letter to the editor · The Times · 11 November 2026</div>
        <p style="margin-top:22px">Sir,</p>
        <p>Your leading article is right to ask what Britain will do for Joshua Wong (“Supine Silence”, Nov 6). The government has joined nine allies in calling for an end to “unjust prosecutions” under Hong Kong’s national security law, but condemnation is a statement, not a policy. Joshua Wong, who has been sentenced to ten years’ imprisonment, stood up for the Sino-British joint declaration, a treaty Britain signed and registered at the United Nations, which our own government says China has breached. <strong>A treaty broken without cost invites the next breach.</strong></p>
        <p>The government should summon the Chinese ambassador, as it did for Jimmy Lai; sanction those responsible for national security law prosecutions, as the US has; and tell parliament what further consequences will follow if Jimmy Lai, Joshua Wong and Benny Tai are not freed.</p>
        <p class="no-print" style="font-family:var(--label);font-size:14px">Published in The Times: <a href="https://www.thetimes.com/comment/letters-to-editor/article/times-letters-civil-service-needs-urgent-reform-wq3bcj955" target="_blank" rel="noopener">read it on thetimes.com</a> (subscription may be needed). The letter responds to The Times’s leading article, <a href="https://www.thetimes.com/comment/the-times-view/article/joshua-wong-jailed-hong-kong-uk-china-nn9c6vpzc" target="_blank" rel="noopener">“Supine Silence”</a>.</p>
        <p class="no-print" style="font-family:var(--label);font-size:14px">It follows <a href="open-letter-prime-minister-sept-2026.html">the open letter to the Prime Minister</a> signed by 31 MPs, peers and rights leaders in September 2026.</p>
        <div class="no-print" style="margin-top:26px" data-share data-url="https://freejoshuawong.org/letters/times-letter-nov-2026.html" data-text="“A treaty broken without cost invites the next breach.” MPs and peers write to The Times on Joshua Wong"></div>
      </article>
      <aside class="signs">
        <h4>Signed by</h4>
        <ul>""" + sig + """</ul>
      </aside>
    </div>
  </div>
</section>
""" + footer(1)

def zh():
    h = head("釋放黃之鋒", "黃之鋒自2020年11月起身陷囹圄，2026年11月再被加判十年。了解他的案件，以及身在英國的你可以怎樣幫忙。", "zh.html")
    h = h.replace('<html lang="en-GB">', '<html lang="zh-Hant-HK">')
    return h + nav("zh.html") + page_head("中文",
        "釋放<em>黃之鋒</em>",
        "他原定於2027年1月出獄。如今，他被加判十年。") + """
<div class="wrap"><p class="zh-demand">召見中國大使，釋放黃之鋒。</p></div>
<section class="zh" style="border-top:0;padding-top:20px">
  <div class="wrap zh-body">
    <div class="zh-count"><b """ + 'data-since="' + JAILED_DATE + '"' + """>—</b><span>日<br>身陷囹圄</span></div>

    <h2 class="zh-h">他是誰</h2>
    <p>黃之鋒十四歲時與同學創立學民思潮，2012年帶領反對國民教育科的運動。2014年雨傘運動期間，他是學生領袖之一。2016年，他與羅冠聰等人創立香港眾志。</p>
    <p>他此前曾兩度入獄：2017年因2014年重奪公民廣場一事被判非法集結罪成，入獄約兩個月後獲准保釋，刑罰其後被終審法院撤銷；2018至2019年因2014年旺角清場藐視法庭，分段服刑，最後一段為2019年5月至6月。</p>
    <p>他自2020年11月起一直被羈押。</p>

    <h2 class="zh-h">發生了甚麼事</h2>
    <ul class="zh-list">
      <li><b>2021年2月</b>　作為「香港47人」案被告之一，被控串謀顛覆國家政權罪。</li>
      <li><b>2024年11月</b>　被判囚四年八個月，原定於2027年1月出獄。</li>
      <li><b>2025年6月6日</b>　在獄中再被控串謀勾結外國或者境外勢力危害國家安全罪。</li>
      <li><b>2026年9月2日</b>　承認控罪。</li>
      <li><b>2026年11月5日</b>　被判囚十年。</li>
    </ul>
    <p>控方引用他在《國安法》實施前會見外國政界人士的游說活動，以及其後的社交媒體帖文、評論文章和訪問，指有關活動一直持續。</p>

    <h2 class="zh-h">為甚麼英國有責任</h2>
    <p>黃之鋒於1996年10月在香港出生，距離回歸只有八個月，當時香港仍由英國管治。他出生那天，英國對他負有責任；今天依然如此。</p>
    <p>英國在1984年簽署《中英聯合聲明》，承諾香港的權利和自由五十年不變。黃之鋒所爭取的，正是這個承諾得到兌現。</p>
    <p>判刑後，11個國家及地區政府，連同歐盟，就判決發表聲明，表達譴責或關注，當中包括英國。</p>

    <h2 class="zh-h">我們要求英國政府</h2>
    <div class="zh-asks">
      <div class="ask-lead"><h3>召見中國駐英大使</h3><p>外相應召見中國大使，點名提出黃之鋒及其他因爭取民主而入獄的人士的個案，正如英國外交部曾為黎智英所做的一樣。</p></div>
      <div><h3>檢討香港駐倫敦經濟貿易辦事處</h3><p>該辦事處仍享有類似外交機構的特權，即使其一名高級經理已被裁定在英國監視港人罪成。</p></div>
      <div><h3>制裁相關官員</h3><p>聯同英國的盟友，追究負責《國安法》檢控的官員。</p></div>
    </div>

    <h2 class="zh-h">仍在等待回應</h2>
    <p>2026年9月1日，外相文禮彬（Ed Miliband）在下議院表示會跟進黃之鋒的個案，至今沒有公開的進展。9月13日，31名國會議員、上議院議員及人權界人士聯署<a href="letters/open-letter-prime-minister-sept-2026.html">公開信致首相</a>，至今未獲回覆。</p>

    <h2 class="zh-h">身在英國的你可以怎樣幫忙</h2>
    <div class="zh-act">
      <div>
        <h3>寫信給你的國會議員</h3>
        <p>請你選區的國會議員向外相提出黃之鋒的個案。我們已準備好英文信件範本：輸入郵遞區號，網站會找出你的議員，並在電郵中填好信件，你只需加上姓名和地址再寄出。</p>
        <p><a class="btn" href="act.html#mp">寫信給你的議員</a></p>
        <p class="zh-small">郵遞區號只用於在英國國會網站查找你的議員。本網站不會看到或儲存你的郵遞區號或寄出的內容。</p>
      </div>
      <div>
        <h3>分享他的故事</h3>
        <p>使用標籤 #FreeJoshuaWong 及 #JoshuaWong，並標註你的國會議員。</p>
        <p class="zh-small">如你在香港有家人，或擔心自身安全，可以只轉發本網站或其他公開內容，無須公開表態。請先照顧好自己。</p>
      </div>
      <div>
        <h3>觀看新短片</h3>
        <p>《Joshua: Prisoner vs. Superpower》（英語）講述2017年紀錄片之後，黃之鋒的遭遇。</p>
        <p><a class="btn ghost" href="film.html">觀看短片</a></p>
      </div>
    </div>
    <p class="zh-small" style="margin-top:40px"><a href="index.html">English</a></p>
  </div>
</section>
""" + footer(0)

# ===== Messages for Joshua: a virtual wall of hope (unlisted until hosting is on Netlify) =====
# The form posts to Netlify Forms (works once the site is hosted on Netlify). Nothing is shown on the wall
# until it is approved and copied into assets/messages.js.
def write():
    h = head("Messages for Joshua", "Write Joshua Wong a message of hope.", "write.html")
    return h + nav("write.html") + """
<header class="mw-hero">
  <div class="wrap mw-hero-in">
    <div>
      <div class="label">Messages for Joshua</div>
      <h1>Send Joshua <em>a little hope</em></h1>
      <p>His greatest fear is that the world will forget Hong Kong. A few kind words from you can show him it hasn’t.</p>
      <a class="btn" href="#write-box">Write your message</a>
    </div>
    <figure class="mw-photo"><img src="images/joshua.jpg?v=2" alt="Joshua Wong raising a V sign beneath an umbrella, Hong Kong, 2014"></figure>
  </div>
</header>

<section class="mw-steps" aria-label="How it works">
  <div class="wrap">
    <ol>
      <li><b>Write</b><span>A few lines about you, your life, or what gives you hope.</span></li>
      <li><b>We read every one</b><span>So the wall stays a kind place.</span></li>
      <li><b>It goes on the wall</b><span>For everyone to see, and shared with people close to Joshua to pass on when they can.</span></li>
    </ol>
  </div>
</section>

<section class="mw" id="write-box">
  <div class="wrap">
    <div class="mw-grid">
      <form class="mw-form" name="joshua-messages" method="POST" action="write.html?sent=1#sent" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="joshua-messages">
        <p hidden><label>Leave this empty <input name="bot-field"></label></p>
        <div class="mw-paper">
          <div class="mw-dear">Dear Joshua,</div>
          <label for="mw-msg" class="sr">Your message to Joshua</label>
          <textarea id="mw-msg" name="message" rows="8" maxlength="600" required placeholder="Write from the heart…"></textarea>
          <div class="mw-count"><span id="mw-left">600</span> characters left</div>
          <div class="mw-row">
            <div><label for="mw-name">From</label><input id="mw-name" name="first-name" maxlength="40" required placeholder="Your first name"></div>
            <div><label for="mw-town">In</label><input id="mw-town" name="place" maxlength="60" required placeholder="Town or country"></div>
          </div>
        </div>
        <div class="mw-starts" aria-label="Need a start?"><span>Need a start?</span>
          <button type="button" data-start="What gives me hope is ">What gives me hope…</button>
          <button type="button" data-start="Where I live, ">Where I live…</button>
          <button type="button" data-start="A book I think you would love is ">A book for you…</button>
          <button type="button" data-start="When I heard your story, ">When I heard your story…</button>
        </div>
        <label class="mw-check"><input type="checkbox" name="show-on-wall" value="yes" checked> You can show my message, first name and town on this page</label>
        <button class="btn" type="submit">Send my message</button>
        <p class="mw-note">We never ask for your email or surname. Please keep it personal: the prison reads his post, and politics may stop it reaching him.</p>
        <p class="mw-sent" id="sent" hidden>Thank you. Your message is on its way, and will appear on the wall once it has been read.</p>
      </form>
      <div class="mw-wall-wrap">
        <h2>From around the world</h2>
        <div class="mw-wall" id="mw-wall"></div>
      </div>
    </div>
  </div>
</section>
""" + footer(0, '<script src="assets/messages.js"></script>\n')

def messages_print():
    h = head("Messages for Joshua: print", "Approved messages for Joshua, ready to print.", "messages-print.html")
    h = h.replace("<title>", '<meta name="robots" content="noindex">\n<title>', 1)
    return h + """<main class="mp-print">
  <div class="mp-tools"><label>Month <select id="mp-month"></select></label><button class="btn" type="button" onclick="window.print()">Print</button></div>
  <h1>Messages for Joshua</h1>
  <p class="mp-sub" id="mp-sub"></p>
  <p class="mp-open">Dear Joshua, these are some of the messages people around the world have written to you. Hong Kong has not been forgotten, and neither have you.</p>
  <div id="mp-list"></div>
</main>
<script src="assets/messages.js"></script>
<script>
(function(){
  var M=window.MESSAGES||[], months=['January','February','March','April','May','June','July','August','September','October','November','December'];
  var keys=[]; M.forEach(function(m){var k=(m.date||'').slice(0,7); if(k&&keys.indexOf(k)<0) keys.push(k);}); keys.sort().reverse();
  var sel=document.getElementById('mp-month'); sel.innerHTML='<option value="">All</option>'+keys.map(function(k){var p=k.split('-');return '<option value="'+k+'">'+months[+p[1]-1]+' '+p[0]+'</option>';}).join('');
  var q=new URLSearchParams(location.search).get('month'); if(q) sel.value=q;
  var esc=function(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});};
  function render(){var k=sel.value, L=M.filter(function(m){return !k||(m.date||'').slice(0,7)===k;});
    document.getElementById('mp-sub').textContent=(k?months[+k.split('-')[1]-1]+' '+k.split('-')[0]:'All messages')+' \u00b7 '+L.length+' messages';
    document.getElementById('mp-list').innerHTML=L.length?L.map(function(m){return '<div class="mp-m"><p>'+esc(m.text).replace(/\\n/g,'<br>')+'</p><span>'+esc(m.name)+', '+esc(m.place)+'</span></div>';}).join(''):'<p>No approved messages yet.</p>';}
  sel.onchange=render; render();
})();
</script>
</body></html>"""

# ---------------- CAMPAIGN VIDEO (launch: Monday 23 Nov 2026, six years in prison) ----------------
# Put the files here, then rebuild. Leave REEL_CAPTIONED empty if there is only one version.
REEL = "media/what-has-the-pm-done.mp4?v=7"   # main video (portrait 1080x1920, captions burned in), hosted on the site
REEL_DOWNLOAD = REEL
REEL_POSTER = "images/what-has-the-pm-done-poster.jpg?v=3"
REEL_CAPTIONED = ""  # add a link here if there is a separate captioned version  # captioned version for posting directly
REEL_IMAGE = "images/what-has-the-pm-done-share.jpg"         # share image (also used as the poster)
REEL_URL = "https://freejoshuawong.org/video.html"
REEL_UNLISTED = False  # True hides the page from search engines (noindex)
REEL_POSTS = [
    "When Jimmy Lai was convicted, the UK summoned the Chinese Ambassador the same day. Joshua Wong was sentenced to ten years on 5 November. There has been no public word of the Ambassador being summoned.",
    "Britain signed the Joint Declaration in 1984 and guaranteed Hong Kong’s freedoms for fifty years. Joshua Wong only asked us to keep our word. He has now been sentenced to ten years.",
]

def video():
    h = head("What has the Prime Minister done for Joshua?",
             "A short video from the Free Joshua Wong campaign. Watch, download and share it.", "video.html")
    if os.path.exists(os.path.join(ROOT, REEL_IMAGE)):
        h = h.replace(f"{SITE}/images/share-card.jpg", f"{SITE}/{REEL_IMAGE}")
    if REEL_UNLISTED:
        h = h.replace("<title>", '<meta name="robots" content="noindex">\n<title>', 1)
    has = lambda f: bool(f) and (f.startswith("http") or os.path.exists(os.path.join(ROOT, f.split("?")[0])))
    dl = f'<a class="btn" href="{REEL_DOWNLOAD}" download="Free-Joshua-Wong-video.mp4">Download the video (MP4, with captions)</a>' if has(REEL) else ""
    if has(REEL_CAPTIONED):
        dl += f'\n        <a class="btn" href="{REEL_CAPTIONED}" download>Download with captions (MP4)</a>'
    if has(REEL_IMAGE):
        dl += f'\n        <a class="btn ghost" href="{REEL_IMAGE}" download>Download the share image</a>'
    poster = f' poster="{REEL_POSTER}"' if has(REEL_POSTER) else ""
    player = (f'<div class="reel-player"><video controls preload="metadata" playsinline{poster}><source src="{REEL}" type="video/mp4">Your browser can’t play this video. <a href="{REEL_DOWNLOAD}" download="Free-Joshua-Wong-video.mp4">Download it instead.</a></video></div>'
              if has(REEL) else '<div class="screen" style="display:flex;align-items:center;justify-content:center;aspect-ratio:16/9;background:var(--ink-2)"><p style="margin:0;font-size:20px">The video will be here shortly.</p></div>')
    posts = "".join(
        f'\n        <div class="post"><p>{t} <b>#FreeJoshuaWong #JoshuaWong</b></p><button class="copy" type="button">Copy</button></div>'
        for t in REEL_POSTS)
    return h + nav("video.html") + page_head(
        "Campaign video", "What has the Prime Minister<br><em>done for Joshua?</em>",
        "Joshua Wong has been in prison since 23 November 2020. On 5 November 2026 he was given ten more years. Watch the video, download it and share it.") + f"""
<section class="reel-sec">
  <div class="wrap reel-wrap">
    {player}
    <div class="reel-side">
      <div class="label">Watch. Download. Post.</div>
      <h3 class="reel-h">Post it.<br><span>Tag your MP.</span></h3>
      <p class="reel-p">Download the video and post it on your own channels, with a line in your own words, or copy one of ours.</p>
      <div class="video-dl">
        {dl}
      </div>
      <p class="reel-note">On a phone, if it opens instead of downloading, press and hold the button and choose “Save”.</p>
      <div class="reel-posts">{posts}
      </div>
      <div data-share data-url="{REEL_URL}" data-text="What has the Prime Minister done for Joshua Wong?"></div>
      <p class="reel-more">Want to do more? <a href="act.html#mp">Ask your MP to raise Joshua’s case</a>, or see what ministers have been <a href="index.html#asked">asked and what they have said</a>.</p>
    </div>
  </div>
</section>
""" + CTA.replace("{up}", "") + footer()

# ---------------- CONTACT ----------------
# Messages are sent by Web3Forms to the inbox tied to this key (the address itself never appears on the site).
FORM_KEY = "18ce9861-069f-475d-8545-d5e5ece43276"   # paste the Web3Forms access key here
CONTACT_TOPICS = [("press", "Press or media enquiry"), ("interview", "Interview request"), ("screening", "Screening request"),
                  ("parliament", "Parliament or government"), ("other", "Something else")]

def contact():
    opts = "".join(f'<option value="{label}" data-k="{k}">{label}</option>' for k, label in CONTACT_TOPICS)
    return head("Contact", "Contact the Free Joshua Wong campaign.", "contact.html") + nav("contact.html") + page_head(
        "Contact", "Get in <em>touch</em>",
        "Press, interviews, screenings, Parliament, or anything else. Send us a message and we’ll reply by email.") + f"""
<section class="contact-sec">
  <div class="wrap">
    <form class="contact-form" id="contact-form" action="https://api.web3forms.com/submit" method="POST">
      <input type="hidden" name="access_key" value="{FORM_KEY}">
      <input type="hidden" name="subject" value="Free Joshua Wong website: new message">
      <input type="hidden" name="from_name" value="freejoshuawong.org">
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <label>What is it about?<select name="topic" id="cf-topic">{opts}</select></label>
      <label>Your name<input type="text" name="name" required autocomplete="name"></label>
      <label>Your email<input type="email" name="email" required autocomplete="email"></label>
      <label>Organisation <small>(optional)</small><input type="text" name="organisation" autocomplete="organization"></label>
      <label>Message<textarea name="message" rows="7" required></textarea></label>
      <button class="btn" type="submit">Send message</button>
      <p class="cf-status" id="cf-status" role="status" aria-live="polite"></p>
      <p class="cf-small">We only use your details to reply to you.</p>
    </form>
  </div>
</section>
<script>
(function () {{
  var f = document.getElementById('contact-form'), st = document.getElementById('cf-status'), sel = document.getElementById('cf-topic');
  var t = new URLSearchParams(location.search).get('topic');
  if (t) {{ for (var i = 0; i < sel.options.length; i++) if (sel.options[i].getAttribute('data-k') === t) sel.selectedIndex = i; }}
  f.addEventListener('submit', function (e) {{
    e.preventDefault();
    var b = f.querySelector('button'); b.disabled = true; st.textContent = 'Sending…';
    fetch(f.action, {{ method: 'POST', headers: {{ 'Accept': 'application/json' }}, body: new FormData(f) }})
      .then(function (r) {{ return r.json(); }})
      .then(function (d) {{
        if (d.success) {{ f.reset(); st.textContent = 'Thank you. Your message has been sent and we’ll reply by email.'; }}
        else {{ st.textContent = 'Sorry, that didn’t send. Please try again in a moment.'; }}
        b.disabled = false;
      }})
      .catch(function () {{ st.textContent = 'Sorry, that didn’t send. Please check your connection and try again.'; b.disabled = false; }});
  }});
}})();
</script>
""" + footer()

PAGES = {
    "index.html": home, "case.html": case, "film.html": film, "newsroom.html": newsroom,
    "resources.html": resources, "act.html": act, "zh.html": zh, "write.html": write, "messages-print.html": messages_print, "parliament.html": parliament, "voices.html": voices, "socials.html": socials, "video.html": video, "contact.html": contact,
    "letters/open-letter-prime-minister-sept-2026.html": letter_pm,
    "letters/times-letter-nov-2026.html": letter_times,
}

def bake_numbers(html):
    """Write today's counts into the page so they are right even before the page's script runs."""
    import re, datetime
    from sharecard import days_inside, uk_today
    today = uk_today()
    def since(m):
        y, mo, d = map(int, m.group(1).split("-"))
        return f'data-since="{m.group(1)}">{(today - datetime.date(y, mo, d)).days}<'
    html = re.sub(r'data-since="(\d{4}-\d{2}-\d{2})">[^<]*<', since, html)
    html = re.sub(r'(id="days" data-jailed="[^"]*">)[^<]*(<)', lambda m: f"{m.group(1)}{days_inside():,}{m.group(2)}", html)
    return html

if __name__ == "__main__":
    import sys, datetime
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import sharecard, covers
    print("share card:", sharecard.make())
    covers.make_all()
    import quotecards
    for v in quotecards.make_all():
        PAGES[f"voices/{v['slug']}.html"] = (lambda v=v: quote_page(v))
    import hashlib
    ASSET_V = hashlib.md5(b"".join(open(os.path.join(ROOT, "assets", a), "rb").read() for a in ["site.css","site.js","press.js","voices.js","socials.js"])).hexdigest()[:8]
    for path, fn in PAGES.items():
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        html = bake_numbers(fn()).replace("https://freejoshuawong.org", SITE)
        html = _re.sub(r'(assets/(?:site\.css|site\.js|press\.js|voices\.js|socials\.js))"', lambda m: m.group(1) + "?v=" + ASSET_V + '"', html)
        with open(out, "w") as f:
            f.write(html)
        print("wrote", path)
