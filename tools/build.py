#!/usr/bin/env python3
"""Builds the Free Joshua Wong site pages from shared header/footer.
Run from the repo root:  python3 tools/build.py
Edit page content in this file, then re-run. Output: *.html in the repo root and letters/."""
import os

SITE = "https://freejoshuawong.org"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import re as _re
PRESS_COUNT = len(_re.findall(r'^\s*\{date:', open(os.path.join(ROOT, "assets/press.js")).read(), _re.M))

NAV = [("case.html", "The case"), ("film.html", "Watch"), ("newsroom.html", "Newsroom"), ("parliament.html", "Parliament"), ("voices.html", "Voices"), ("socials.html", "Socials"), ("resources.html", "Resources")]

def head(title, desc, path, depth=0):
    up = "../" * depth
    full = "Free Joshua Wong" if title == "Free Joshua Wong" else f"{title} — Free Joshua Wong"
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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
</head>
<body>
"""

def nav(current, depth=0):
    up = "../" * depth
    links = "".join(
        f'<a href="{up}{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV)
    return f"""<nav class="top" aria-label="Main">
  <div class="wrap">
    <a class="brand" href="{up}index.html">Free <span>Joshua Wong</span></a>
    <div class="links">{links}<a href="{up}act.html" class="mob-only"{" aria-current=\"page\"" if current == "act.html" else ""}>Take action</a></div>
    <a class="btn" href="{up}act.html">Take action</a>
    <button class="menu-btn" type="button" aria-expanded="false">Menu</button>
  </div>
</nav>
"""

COLLEAGUES = [
    ("Hong Kong Watch", "https://www.hongkongwatch.org"),
    ("Committee for Freedom in Hong Kong Foundation", "https://www.cfhk.org"),
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
        <a href="{up}resources.html">Resources</a><a href="{up}act.html">Take action</a>
      </nav>
      <div>
        <p style="font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:11px;color:var(--accent);margin:0">Press enquiries</p>
        <p>press@freejoshuawong.org</p>
      </div>
    </div>
  </div>
</footer>
{scripts}<script src="{up}assets/site.js"></script>
</body>
</html>
"""

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
      <div class="ask"><h3>Raise Joshua’s case with the Chinese Ambassador</h3><p>The Prime Minister should call in the Ambassador and raise Joshua and the others imprisoned for standing up for democracy, by name.</p></div>
      <div class="ask"><h3>Review the Hong Kong trade office’s privileges</h3><p>The Hong Kong Economic and Trade Office in London keeps diplomatic-style privileges, even after a senior manager there was convicted of spying on Hong Kongers in Britain.</p></div>
      <div class="ask"><h3>Sanction those responsible</h3><p>Hold to account the officials behind National Security Law prosecutions, working with Britain’s allies.</p></div>
    </div>"""

FACTS = """<section class="facts" aria-label="Key facts">
  <div class="wrap">
    <div class="fact"><div class="n">Nov 2020</div><div class="t">In prison continuously since</div></div>
    <div class="fact"><div class="n">Jan 2027</div><div class="t">When he was due to walk free</div></div>
    <div class="fact"><div class="n">10 years</div><div class="t">New sentence, handed down on 5 November 2026</div></div>
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
PLAYER = '''<div class="screen vid"><video controls preload="none" playsinline poster="images/film-poster.jpg"><source src="media/joshua-prisoner-vs-superpower.mp4" type="video/mp4">Your browser can’t play this video.</video></div>'''

FLAGS = ["UK","US","Australia","Canada","France","Germany","Italy","Japan","Netherlands","New Zealand"]

def life_bar():
    cells, labels = [], []
    marks = {1996:"Born", 2012:"Age 15", 2020:"Age 24, jailed", 2027:"Was due out", 2036:"Age 40, possible release"}
    for i, y in enumerate(range(1996, 2037)):
        state = "s-free" if y < 2020 else ("s-in" if y <= 2026 else "s-ahead")
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
<header class="h4-hero" id="top">
  <div class="h4-text">
    <h1 class="fit"><span>Free Joshua Wong</span></h1>
    <div class="h4-titles" aria-label="The film: in 2017, Teenager vs. Superpower; in 2026, Prisoner vs. Superpower">
      <div class="r then"><span class="y">2017</span><s>Teenager vs. Superpower</s></div>
      <div class="r now"><span class="y">2026</span><b>Prisoner vs. Superpower</b></div>
      <div class="r cell-row"><span class="y">Now</span>
        <div class="cell" role="timer" aria-label="Days Joshua Wong has spent in prison">
          <div class="cell-in"><span class="n" id="days">2,181</span><span class="u">days<br>behind bars</span></div>
        </div>
      </div>
    </div>
    <p class="h4-lead">He was due out in January 2027. Instead, he has been given ten more years.</p>
    <div class="h4-cta">
      <a class="btn" href="act.html#mp">Write to your MP</a>
      <a class="btn ghost" href="#film">Watch the film</a>
    </div>
  </div>
  <figure class="h4-pic">
    <img src="images/joshua.jpg" alt="Joshua Wong raising a two-fingered salute beneath an umbrella during the 2014 Umbrella Movement">
    <figcaption>Hong Kong, 2014</figcaption>
  </figure>
</header>

<section class="h4-life" aria-labelledby="life-h">
  <div class="wrap">
    <h2 id="life-h">His life, year by year</h2>
    <p class="h4-sub">If the sentence stands, Joshua will spend the years from 24 to 40 in prison: his late twenties and almost all of his thirties.</p>
    <div class="lifebar" role="img" aria-label="A bar of 41 years from 1996 to 2036. 1996 to 2019 free; 2020 to 2026 in prison; 2027 to 2036 still to serve.">""" + cells + """</div>
    <div class="lifemarks" aria-hidden="true">""" + labels + """</div>
    <ul class="key"><li><i class="s-free"></i>Free</li><li><i class="s-in"></i>In prison</li><li><i class="s-ahead"></i>Still to serve</li></ul>
  </div>
</section>

<section class="h4-words">
  <div class="wrap">
    <blockquote>“The only thing I worry about is that people will forget Hong Kong.”</blockquote>
    <p class="by">Joshua Wong, in a letter to a friend from prison, published in November 2026</p>
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
      <a href="newsroom.html#statements"><b>11</b><span>governments, plus the EU, condemned his sentence</span></a>
      <a href="letters/open-letter-prime-minister-sept-2026.html"><b>""" + str(len(SIGNATORIES)) + """</b><span>MPs, peers and rights leaders signed the open letter to the Prime Minister</span></a>
      <a href="parliament.html"><b>""" + str(sum(1 for r in RECORD if r[1] != "event")) + """</b><span>times raised in Parliament since the new charge in June 2025</span></a>
      <a href="newsroom.html"><b>""" + str(PRESS_COUNT) + """</b><span>reports, podcasts and editorials since June 2025</span></a>
    </div>
  </div>
</section>

<section class="h4-asks">
  <div class="wrap">
    <h2>What Britain should do</h2>
    <p class="h4-sub">Britain guaranteed Hong Kong’s freedoms in 1984. Ten governments, including our own, signed a joint statement condemning Joshua’s sentence. Now words need to become action.</p>
    <div class="asklist">
      <div><h3>Raise his case with China’s ambassador</h3><p>The Prime Minister should call in the Ambassador and name Joshua and the others jailed for standing up for democracy.</p></div>
      <div><h3>Review the Hong Kong trade office</h3><p>Its London office keeps diplomatic-style privileges, even after a senior manager there was convicted of spying on Hong Kongers in Britain.</p></div>
      <div><h3>Sanction those responsible</h3><p>Hold the officials behind National Security Law prosecutions to account, together with Britain’s allies.</p></div>
    </div>
    <div class="waiting h4-wait">
      <h3>Still waiting for an answer</h3>
      <div class="wait-row">
        <div class="wait-n"><span data-since="2026-09-01">73</span><small>days, no update</small></div>
        <div><h4>The Foreign Secretary said he would take up Joshua’s case</h4><p>Ed Miliband, answering Sir Iain Duncan Smith in the Commons on 1 September 2026. <a href="parliament.html">Watch the exchange</a></p></div>
      </div>
      <div class="wait-row">
        <div class="wait-n"><span data-since="2026-09-13">61</span><small>days, no reply</small></div>
        <div><h4>31 MPs, peers and rights leaders signed an open letter to the Prime Minister</h4><p>Their open letter to Andy Burnham, sent on 13 September 2026. <a href="letters/open-letter-prime-minister-sept-2026.html">Read the letter</a></p></div>
      </div>
    </div>
    <p class="h4-more"><a href="case.html">Read the full case</a></p>
  </div>
</section>

<section class="h4-act">
  <div class="wrap">
    <h2>Ask your MP to raise Joshua’s case</h2>
    <p>It takes two minutes. We give you the letter; you add your name and send it.</p>
    <a class="btn dark" href="act.html#mp">Write to your MP</a>
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
(function(){
  var start=Date.UTC(2020,10,22,16,0,0), el=document.getElementById('days'), clock=document.getElementById('clock');
  if(!el) return;
  var fmt=function(n){return n.toLocaleString('en-GB');}, pl=function(n,w){return n+' '+w+(n===1?'':'s');};
  var total=Math.floor((Date.now()-start)/864e5);
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){el.textContent=fmt(total);}
  else{var t0=null;(function step(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/1600);k=1-Math.pow(1-k,3);el.textContent=fmt(Math.round(total*k));if(k<1)requestAnimationFrame(step);})(performance.now());}
  setInterval(function(){el.textContent=fmt(Math.floor((Date.now()-start)/864e5));},60000);
})();
</script>
""" + footer(0)

LATEST = [
    ("The Times · Letters", "Unjust prosecution: MPs and peers ask what Britain will do for Joshua Wong", "11 Nov 2026", "letters/times-letter-nov-2026.html"),
    ("The Guardian · Today in Focus", "Podcast: Teen prodigy, Netflix star, prisoner, with Nathan Law", "13 Nov 2026", "https://podcasts.apple.com/gb/podcast/today-in-focus/id1440133626"),
    ("House of Commons", "Emily Darlington MP asks the Government to call for Joshua’s release", "10 Nov 2026", "parliament.html#exchange-nov"),
    ("Taipei Times", "Editorial: Joshua Wong was due for release in January", "7 Nov 2026", "https://www.taipeitimes.com/News/editorials/archives/2026/11/07/2003867296"),
    ("Reuters / CTV", "Canada, US, UK and others condemn 10-year sentence for Joshua Wong", "6 Nov 2026", "https://www.ctvnews.ca/world/article/canada-us-uk-and-others-condemn-10-year-sentence-for-hong-kong-activist-joshua-wong/"),
]

# ---------------- THE CASE ----------------
TIMELINE = [
    ("Born", "Oct 1996", "", "Born in Hong Kong", "Joshua Wong Chi-fung grows up in a city promised a high degree of autonomy until 2047."),
    ("15", "Sep 2012", "", "Defeats “national education”", "With the student group Scholarism, which he co-founded at 14, he leads the protests that force the Hong Kong government to shelve a compulsory “national education” curriculum."),
    ("17", "Sep 2014", "", "The Umbrella Movement", "His arrest at Civic Square helps spark 79 days of street occupation demanding genuine universal suffrage. <em>Time</em> puts him on its cover."),
    ("19", "Oct 2016", "", "Detained at Bangkok airport", "Held and deported by Thai authorities on his way to speak at a university, an early sign of how far Beijing’s pressure would reach."),
    ("20", "2017", "", "First prison sentence, and the film", "Jailed over the 2014 Civic Square protest; Hong Kong’s top court later quashes the sentence. <em>Joshua: Teenager vs. Superpower</em> premieres at Sundance and wins the audience award."),
    ("22", "Sep 2019", "", "Testifies to the US Congress", "Gives evidence to the Congressional-Executive Commission on China on human rights in Hong Kong. Years later, prosecutors cite his lobbying in Washington against him."),
    ("23", "Jun 2020", "", "The National Security Law", "Beijing imposes the National Security Law on Hong Kong. His party, Demosistō, disbands the same day."),
    ("24", "Nov 2020", "", "Into prison, where he remains", "Jailed over a 2019 protest outside police headquarters. He has not been free since."),
    ("24", "Jan 2021", "", "Arrested as one of the Hong Kong 47", "Arrested in his cell under the National Security Law for taking part in an unofficial pro-democracy primary election, and charged with subversion in February."),
    ("28", "Nov 2024", "", "Sentenced to 4 years 8 months", "Sentenced in the largest national security trial in Hong Kong’s history. His release date is set for early 2027."),
    ("28", "Jun 2025", "", "Charged again from his cell", "Charged with conspiracy to collude with foreign forces, carrying a maximum of life imprisonment. The evidence is his own advocacy and public statements."),
    ("29", "Sep 2026", "", "Raised in Parliament, then a guilty plea", "On 1 September Sir Iain Duncan Smith raises his case in the Commons and the Foreign Secretary says he will take it up. The next day Joshua pleads guilty. On 13 September, 31 MPs, peers and rights leaders sign an open letter to the Prime Minister."),
    ("30", "13 Oct 2026", "", "Turns thirty in prison", "Parliamentarians mark his birthday with a screening of the new film in the Houses of Parliament."),
    ("30", "5 Nov 2026", "", "Ten more years", "A Hong Kong court sentences him to ten years. Ten governments, including the UK, condemn the sentence the next day."),
    ("30", "10 Nov 2026", "", "Raised again in the Commons", "Five days after the sentence, Emily Darlington MP asks the Government to summon the Chinese Ambassador and call for Joshua’s release. The next day she and seven other MPs and peers set out the same demands in a letter to The Times."),
    ("40", "c. 2036", "future", "Release, if nothing changes", "Unless governments act, Joshua may not walk free until he is around 40, having spent most of his adult life in prison."),
]

def case():
    items = "".join(
        f'<div class="titem{" future" if fut else ""}"><div class="d">{d}<span class="age">{age if age=="Born" else "Age " + age}</span></div><div><h3>{h}</h3><p>{p}</p></div></div>'
        for age, d, fut, h, p in TIMELINE)
    return head("The case", "Who Joshua Wong is, what he is charged with, and why Britain has a responsibility to act.", "case.html") + nav("case.html") + page_head(
        "The case", "He kept his word.<br><em>Will we?</em>",
        "Joshua Wong has spent his adult life asking Beijing to keep the promises it made to Hong Kong. He is now serving ten more years for it.") + """
""" + FACTS + """
<section>
  <div class="wrap">
    <div class="two">
      <div>
        <h3>Who he is</h3>
        <p>Joshua Wong has campaigned for democracy in Hong Kong since he was a schoolboy. At fifteen he stopped a Beijing-backed “national education” curriculum; at seventeen he was the face of the Umbrella Movement; at twenty he was the subject of an award-winning Netflix documentary.</p>
      </div>
      <div>
        <h3>What he is charged with</h3>
        <p>“Conspiracy to collude with foreign forces” under the National Security Law, a law imposed by Beijing in 2020.</p>
        <ul>
          <li><strong>The evidence is his own words:</strong> his meetings with foreign politicians, social media posts, op-eds and interviews.</li>
          <li><strong>Much of it predates the law:</strong> prosecutors relied on his lobbying from before the law existed, and on later posts and interviews to argue it carried on.</li>
          <li><strong>He was already in prison:</strong> he was charged from his cell, while still serving another sentence.</li>
          <li><strong>The result:</strong> ten more years, handed down on 5 November 2026.</li>
        </ul>
      </div>
    </div>
    <p class="pull">He is serving a sentence for believing us.</p>
    <div class="why">
      <div><div class="k">1984</div><h4>Britain gave its word</h4><p>The UK signed the Joint Declaration and guaranteed Hong Kong’s freedoms for fifty years. The Government has itself declared China in breach of it.</p></div>
      <div><div class="k">2026</div><h4>It has reached our streets</h4><p>Two men were convicted at the Old Bailey this year of spying on Hong Kong dissidents in Britain, and jailed. Hong Kongers settled here have bounties on their heads.</p></div>
      <div><div class="k">BN(O)</div><h4>It is a test of what we stand for</h4><p>Human beings must come before commercial interests. If Britain stays quiet about Joshua, what is its promise to Hong Kongers worth?</p></div>
    </div>
  </div>
</section>

<section id="timeline">
  <div class="wrap">
    <div class="sec-head">
      <div><div class="label">His life so far</div><h2 class="sec">From 15 <em>to 40</em></h2></div>
      <a class="btn ghost" href="resources.html#factsheet">Download the fact sheet</a>
    </div>
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
      <div class="screen vid"><video controls preload="none" playsinline poster="images/film-poster.jpg"><source src="media/joshua-prisoner-vs-superpower.mp4" type="video/mp4">Your browser can’t play this video.</video></div>
      <div class="film-copy">
        <div class="label dim">Producer Andrew Duncan</div>
        <h3>Joshua: <span>Prisoner</span> vs. Superpower</h3>
        <p>A new short film from the team behind <em>Joshua: Teenager vs. Superpower</em>. Archive, new interviews, and the six years since the cameras stopped.</p>
        <p>First shown to parliamentarians in Committee Room 15, Houses of Parliament, on 13 October 2026, Joshua’s 30th birthday.</p>
        <div data-share data-url="https://freejoshuawong.org/film.html" data-text="Joshua: Prisoner vs. Superpower — the second chapter"></div>
      </div>
    </div>

    <div class="watch-wall" id="watch">
      <div class="sec-head"><div><div class="label">Watch and listen</div><h2 class="sec">Interviews, clips and <em>podcasts</em></h2></div></div>
      <div class="vwall">""" + video_cards(skip_film=True) + """</div>
    </div>

    <div class="film-note">
      <div class="big">#1</div>
      <p>In September 2026, Hong Kong’s Security Bureau said it was taking “follow-up action” over the original documentary, which is still on Netflix in the city. Hong Kongers responded by sending it to the top of Netflix’s most-watched list there.</p>
    </div>

    <div class="res-grid">
      <div class="res"><div class="label">The original</div><h3>Teenager vs. Superpower</h3><p>The 2017 documentary, winner of the Sundance World Cinema Documentary Audience Award. Available on Netflix.</p></div>
      <div class="res"><div class="label">For social</div><h3>Trailer clip</h3><p>A short clip for sharing on X, Instagram and WhatsApp.</p><span class="soon">Coming soon</span></div>
      <div class="res"><div class="label">Screenings</div><h3>Host a screening</h3><p>Parliamentarians, universities and community groups can request a screening with a short panel.</p><p><strong>press@freejoshuawong.org</strong></p></div>
    </div>
  </div>
</section>
""" + footer()

# ---------------- NEWSROOM ----------------
STATEMENTS = """<div class="timeline">
      <div class="titem"><div class="d">10 Nov 2026</div><div>
          <div class="who">House of Commons · Urgent question on China</div>
          <div class="flags"><span>UK</span></div>
          <h3>Emily Darlington MP asks the Government to call for Joshua’s release</h3>
          <p>At an urgent question secured by Sir Iain Duncan Smith, she asked ministers to summon the Chinese Ambassador and call for Joshua’s release, as they did for Jimmy Lai. Security Minister Dan Jarvis replied that the Government share the concerns about Joshua and Jimmy Lai. Shadow Minister Alicia Kearns said both remain imprisoned for speaking out for democracy.</p>
          <a class="src" href="parliament.html#exchange-nov">Watch the clip</a> &nbsp; <a class="src" href="https://hansard.parliament.uk/Commons/2026-11-10/debates/580a4a8b-77d1-4dad-b849-9f1d47824e1c/CommonsChamber" target="_blank" rel="noopener">Hansard</a></div></div>
      <div class="titem"><div class="d">6 Nov 2026</div><div>
          <div class="who">Joint statement · 10 foreign ministries</div>
          <h3>Ten governments, including the UK, condemn the sentence</h3>
          <div class="flags"><span>UK</span><span>US</span><span>Australia</span><span>Canada</span><span>France</span><span>Germany</span><span>Italy</span><span>Japan</span><span>Netherlands</span><span>New Zealand</span></div>
          <p>The day after sentencing, the foreign ministries said the case shows how the National Security Law is used to target people for political expression. They called for an end to unjust NSL prosecutions and for the rights promised under the 1984 Sino-British Joint Declaration to be honoured.</p>
          <a class="src" href="https://www.dfat.gov.au/news/statement-sentencing-joshua-wong" target="_blank" rel="noopener">Read the statement</a></div></div>
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
          <div class="who">UK Foreign Secretary · Report to Parliament</div>
          <div class="flags"><span>UK</span></div>
          <h3>Named in the Six-monthly Report on Hong Kong</h3>
          <p>The Government’s report to Parliament cites developments in Joshua’s case as reinforcing concerns about the increasingly broad application of national security legislation.</p>
          <a class="src" href="https://www.gov.uk/government/publications/six-monthly-report-on-hong-kong-january-to-june-2026/six-monthly-report-on-hong-kong-1-january-to-30-june-2026" target="_blank" rel="noopener">GOV.UK</a></div></div>
      <div class="titem"><div class="d">2 Sep 2026</div><div>
          <div class="who">US House of Representatives</div>
          <div class="flags"><span>US</span></div>
          <h3>Nancy Pelosi calls for his freedom on the House floor</h3>
          <blockquote>“We must speak out for freedom. We must not let this be ignored.”</blockquote>
          <a class="src" href="https://pelosi.house.gov/news/press-releases/pelosi-calls-joshua-wongs-freedom-house-floor-we-want-be-sure-they-know-we" target="_blank" rel="noopener">Speaker Emerita Pelosi</a></div></div>
      <div class="titem"><div class="d">1 Sep 2026</div><div>
          <div class="who">House of Commons</div>
          <div class="flags"><span>UK</span></div>
          <h3>Raised by Sir Iain Duncan Smith; the Foreign Secretary says he will take up the case</h3>
          <p>The day before Joshua’s plea hearing, Sir Iain Duncan Smith raised his case at Foreign Office Questions. Foreign Secretary Ed Miliband said he would take it up. There has been no public update since.</p>
          <a class="src" href="parliament.html">Watch the exchange</a></div></div>
      <div class="titem"><div class="d">28 Oct 2025</div><div>
          <div class="who">House of Commons · FCDO oral questions</div>
          <div class="flags"><span>UK</span></div>
          <h3>Raised in the Commons</h3>
          <p>MPs pressed ministers on Hong Kong human rights, noting that Joshua had been rearrested and faced further charges under the National Security Law.</p>
          <a class="src" href="https://hansard.parliament.uk/Commons/2025-10-28/debates/FCFA35AB-A007-4F6D-BF8A-3D80321D4046/HongKongHumanRightsViolations" target="_blank" rel="noopener">Hansard</a></div></div>
      <div class="titem"><div class="d">23 Oct 2025</div><div>
          <div class="who">UK Foreign Secretary · Report to Parliament</div>
          <div class="flags"><span>UK</span></div>
          <h3>His re-arrest recorded in the Six-monthly Report on Hong Kong</h3>
          <p>The Government’s report to Parliament for January to June 2025 records Joshua’s re-arrest on 6 June on suspicion of collusion with foreign forces.</p>
          <a class="src" href="https://www.gov.uk/government/publications/six-monthly-report-on-hong-kong-january-to-june-2025/six-monthly-report-on-hong-kong-1-january-to-30-june-2025" target="_blank" rel="noopener">GOV.UK</a></div></div>
      <div class="titem" style="padding-bottom:0"><div class="d">3 Jul 2025</div><div>
          <div class="who">Written question · Alicia Kearns MP</div>
          <div class="flags"><span>UK</span></div>
          <h3>The UK is “deeply concerned”</h3>
          <p>Answering Alicia Kearns MP, the Foreign Office said it was deeply concerned by the news of further charges against Joshua.</p>
          <a class="src" href="https://www.parallelparliament.co.uk/question/63014/hong-kong-politics-and-government" target="_blank" rel="noopener">Parliamentary answer</a></div></div>
    </div>"""

def newsroom():
    return head("Newsroom", "Press coverage, government statements, letters and releases on Joshua Wong’s case.", "newsroom.html") + nav("newsroom.html") + page_head(
        "Newsroom", "The world is <em>watching</em>",
        "Coverage of Joshua’s case, what governments have said on the record, and the campaign’s letters and releases.") + """
<section style="border-top:0;padding-top:20px">
  <div class="wrap">
    <div class="tabs" role="tablist">
      <a href="#coverage" role="tab">Coverage</a>
      <a href="#statements" role="tab">Government statements</a>
      <a href="#letters" role="tab">Letters &amp; releases</a>
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

    <div class="panel" id="panel-statements" hidden>
      <p class="lede" style="margin-bottom:40px">Joshua’s case has been raised in the House of Commons, in the US Congress and by foreign ministries on three continents.</p>
      <div class="waiting">
        <h3>Still waiting for an answer</h3>
        <div class="wait-row">
          <div class="wait-n"><span data-since="2026-09-01">73</span><small>days</small></div>
          <div><h4>The Foreign Secretary’s promise to take up Joshua’s case</h4><p>Raised in the Commons by Sir Iain Duncan Smith on 1 September 2026. Ed Miliband said he would take up the case. No update since. <a href="parliament.html">Watch the exchange</a></p></div>
        </div>
        <div class="wait-row">
          <div class="wait-n"><span data-since="2026-09-13">61</span><small>days, no reply</small></div>
          <div><h4>The open letter to the Prime Minister</h4><p>Sent to the Prime Minister, Andy Burnham, on 13 September 2026, signed by 31 MPs, peers, former Foreign Secretaries and human rights leaders and organisations. No reply yet. <a href="letters/open-letter-prime-minister-sept-2026.html">Read the letter</a></p></div>
        </div>
      </div>
      """ + STATEMENTS + """
    </div>

    <div class="panel" id="panel-letters" hidden>
      <p class="lede" style="margin-bottom:34px">Letters sent by the campaign and its supporters, and our statements to the media.</p>
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
SIGNATORIES = [
    ("Lord Alton of Liverpool", ""), ("Baroness Bennett of Manor Castle", ""), ("Bob Blackman CBE MP", ""),
    ("Sir Bill Browder KCMG", ""), ("The Rt Hon Alistair Carmichael MP", ""),
    ("Mark Clifford", "President, The Committee for Freedom in Hong Kong Foundation"), ("Graeme Downie MP", ""),
    ("Andrew Duncan", "Co-Founder, RT Weatherman Foundation"), ("The Rt Hon Sir Iain Duncan Smith MP", ""),
    ("Jamie Fly", "CEO, Freedom House"), ("Fortify Rights", ""), ("The Rt Hon the Baroness Foster of Aghadrumsee DBE", ""),
    ("Hong Kong Watch", ""), ("The Rt Hon Sir Jeremy Hunt MP", "Former Foreign Secretary"),
    ("Alicia Kearns MP", "Shadow Minister for Foreign Affairs"), ("Baroness Kennedy of The Shaws KC", ""),
    ("Tim Loughton", "Chair, Conservative Party Human Rights Commission"), ("The Rt Hon Sir Andrew Mitchell KCMG MP", ""),
    ("Meaghan Mobbs", "President, RT Weatherman Foundation"), ("James Naish MP", ""), ("Sir Geoffrey Nice KC", ""),
    ("The Rt Hon the Lord Patten of Barnes KG CH", ""), ("The Rt Hon Sir Malcolm Rifkind KCMG KC", ""),
    ("Benedict Rogers", "Co-founder and Chair, Hong Kong Watch; Senior Director, Fortify Rights"), ("Jemimah Steinfeld", "Chief Executive, Index on Censorship"),
    ("The Rt Hon Tom Tugendhat MBE VR MP", "Shadow Foreign Secretary"), ("Bess Weatherman", "Co-Founder, RT Weatherman Foundation"),
    ("Sara Wilbourne", "ARTICLE 19"), ("Bobby Dean MP", ""), ("Lord Garnier KC", ""), ("Alex Barros-Curtis MP", ""),
]

def letter_pm():
    sig = "".join(f"<li>{n}{f'<small>{r}</small>' if r else ''}</li>" for n, r in SIGNATORIES)
    return head("Open letter to the Prime Minister", "Parliamentarians and human rights organisations ask the Prime Minister to raise Joshua Wong’s case with the Chinese Ambassador.", "letters/open-letter-prime-minister-sept-2026.html", 1) + nav("newsroom.html", 1) + page_head(
        "", "Britain should <em>stand for something</em>",
        "An open letter to the Prime Minister, Andy Burnham, sent on 13 September 2026.",
        crumbs='<a href="../newsroom.html#letters">Newsroom</a> &nbsp;/&nbsp; Letters &amp; releases') + """
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
        <p class="no-print" style="font-family:var(--label);font-size:14px">Published by <a href="https://www.hongkongwatch.org/all-posts/2026/9/14/cross-party-coalition-of-parliamentarians-and-human-rights-leaders-calls-on-prime-minister-to-act-on-hong-kong" target="_blank" rel="noopener">Hong Kong Watch</a> · <a href="https://static1.squarespace.com/static/58ecfa82e3df284d3a13dd41/t/6aa7a88c44264858a83ca2a9/1789372557008/Open+Letter+to+PM+-+Joshua+Wong.pdf" target="_blank" rel="noopener">Download the original letter (PDF)</a></p>
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
    return head("Resources", "Fact sheet, press kit and policy briefs on Joshua Wong’s case, for journalists and parliamentary offices.", "resources.html") + nav("resources.html") + page_head(
        "Resources", "For journalists <em>and MPs’ offices</em>",
        "Everything you need on Joshua’s case in one place: the key facts, approved images and our policy work.") + """
<section style="border-top:0;padding-top:20px" id="factsheet">
  <div class="wrap">
    <div class="facts-sheet">
      <h2>Joshua Wong: fact sheet</h2>
      <div class="sub">Updated 13 November 2026</div>
      <dl>
        <dt>Who</dt><dd>Joshua Wong Chi-fung, born 13 October 1996, Hong Kong. Democracy campaigner since age 14; leader of the 2012 campaign against a Beijing-backed “national education” curriculum and a face of the 2014 Umbrella Movement.</dd>
        <dt>In prison since</dt><dd>November 2020, continuously.</dd>
        <dt>Latest sentence</dt><dd>Ten years, handed down 5 November 2026, for “conspiracy to collude with foreign forces” under the National Security Law.</dd>
        <dt>Previous release date</dt><dd>January 2027, at the end of his 4 year 8 month sentence in the Hong Kong 47 case.</dd>
        <dt>Possible release</dt><dd>Around 2036, when he will be about 40.</dd>
        <dt>The evidence</dt><dd>His own advocacy: meetings with foreign politicians, social media posts, op-eds and interviews, much of it from before the law existed.</dd>
        <dt>International response</dt><dd>Joint statement of 6 November 2026 by Australia, Canada, France, Germany, Italy, Japan, the Netherlands, New Zealand, the UK and the US condemning the sentence.</dd>
        <dt>Why the UK</dt><dd>The UK signed the 1984 Joint Declaration guaranteeing Hong Kong’s freedoms for fifty years, and has declared China in breach of it.</dd>
        <dt>The asks</dt><dd>Raise Joshua’s case with the Chinese Ambassador; review the privileges of the Hong Kong Economic and Trade Office in London; sanction officials responsible for NSL prosecutions, with allies.</dd>
        <dt>Press contact</dt><dd>press@freejoshuawong.org</dd>
      </dl>
      <p class="no-print" style="margin:26px 0 0;font-family:var(--label);font-size:13px;color:rgba(12,12,11,.65)">To save as a PDF, use your browser’s Print option and choose “Save as PDF”.</p>
    </div>

    <div class="res-grid">
      <div class="res" id="press-kit"><div class="label">Press kit</div><h3>Photos &amp; stills</h3><p>Approved images of Joshua and stills from <em>Prisoner vs. Superpower</em>, cleared for editorial use.</p><p>Available on request: <strong>press@freejoshuawong.org</strong></p></div>
      <div class="res" id="briefs"><div class="label">Policy briefs</div><h3>Transnational repression</h3><p>How Beijing’s National Security Law reaches Hong Kongers in Britain, and what the UK can do about it.</p><span class="soon">Coming soon</span></div>
      <div class="res"><div class="label">Interviews</div><h3>Speak to us</h3><p>Interviews with the film’s producer and campaign spokespeople can be arranged.</p><p><strong>press@freejoshuawong.org</strong></p></div>
    </div>
  </div>
</section>
""" + footer()

# ---------------- TAKE ACTION ----------------
def act():
    return head("Take action", "Write to your MP about Joshua Wong and share his story.", "act.html") + nav("act.html") + page_head(
        "Take action", "Don’t let him <em>be forgotten</em>",
        "“The only thing I worry about is that people will forget Hong Kong.” Joshua, in a letter to a friend from prison, 2026.") + """
<section style="border-top:0;padding-top:30px" id="mp">
  <div class="wrap">
    <div class="mp" style="margin-top:0">
      <div>
        <div class="label" style="color:#6f6a2a">In the UK</div>
        <h3>Write to your MP</h3>
        <p>Ask them to raise Joshua’s case with the Foreign Secretary. Copy the letter, then find your MP with your postcode and paste it in.</p>
        <a class="btn dark" href="https://www.writetothem.com" target="_blank" rel="noopener">Find my MP</a>
        <p style="font-size:14px;margin-top:16px;color:rgba(12,12,11,.65)">WriteToThem is run independently by mySociety. We don’t see or store anything you send.</p>
      </div>
      <div>
        <div class="tpl" id="tpl">Dear [MP name],

I am writing as your constituent about Joshua Wong, the Hong Kong democracy campaigner who on 5 November was sentenced to a further ten years in prison under the National Security Law.

Britain guaranteed Hong Kong’s freedoms in the Joint Declaration. Joshua only ever asked that this promise be kept.

On 1 September the Foreign Secretary told the House of Commons he would take up Joshua’s case. There has been no public update since.

Please ask the Foreign Secretary to raise his case directly with the Chinese Ambassador, and tell me what the Government is doing to secure his release.

Yours sincerely,
[Name, address]</div>
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
        <p class="lede" style="font-size:18px">Copy a line, add your MP’s handle, and use #FreeJoshuaWong.</p>
        <div data-share data-url="https://freejoshuawong.org" data-text="Joshua Wong spoke up for Hong Kong. Now he faces ten more years."></div>
      </div>
      <div>
        <div class="post"><p>Joshua Wong was two months from freedom. Hong Kong has given him ten more years for speaking up to foreign parliaments. <b>#FreeJoshuaWong</b></p><button class="copy" type="button">Copy</button></div>
        <div class="post"><p>Britain guaranteed Hong Kong’s freedoms for fifty years. Joshua Wong only asked us to keep our word. <b>#FreeJoshuaWong</b></p><button class="copy" type="button">Copy</button></div>
        <div class="post"><p>He has been in prison since he was 24. He may not walk free until he is 40. <b>#FreeJoshuaWong</b></p><button class="copy" type="button">Copy</button></div>
      </div>
    </div>

    <div class="voices" style="margin-top:70px">
      <div class="voice"><q>The harsh sentence on baseless charges against Joshua Wong is cruel and unjust.</q><div class="by"><a href="https://www.hrw.org/news/2026/11/05/hong-kong-joshua-wong-gets-nearly-10-more-years-in-prison" target="_blank" rel="noopener">Elaine Pearson</a><small>Asia Director, Human Rights Watch</small></div></div>
      <div class="voice"><q>Joshua Wong’s bravery in speaking truth to power should be commended.</q><div class="by"><a href="https://www.amnestyusa.org/press-releases/hong-kong-cruel-joshua-wong-sentence-a-grim-reminder-of-authorities-disdain-for-human-rights/" target="_blank" rel="noopener">Sarah Brooks</a><small>Amnesty International</small></div></div>
      <div class="voice"><q>Joshua Wong deserves to be honoured and applauded, not jailed.</q><div class="by"><a href="https://www.spectator.com.au/?p=10947071" target="_blank" rel="noopener">Benedict Rogers</a><small>Hong Kong Watch, in The Spectator</small></div></div>
    </div>
    <div class="hashtag">#FreeJoshuaWong</div>
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
    ("2026-11-10", "commons", "“Calling for Joshua Wong’s release”", "Urgent question on China · House of Commons",
     "At an urgent question secured by Sir Iain Duncan Smith on China obtaining MPs’ phone and financial records, Emily Darlington MP asked the Government to summon the Chinese Ambassador and call for Joshua’s release, as it did for Jimmy Lai. Security Minister Dan Jarvis replied that the Government share the concerns about Joshua and Jimmy Lai. For the Opposition, Alicia Kearns MP said both remain imprisoned for speaking out for democracy. <a href=\"https://hansard.parliament.uk/Commons/2026-11-10/debates/580a4a8b-77d1-4dad-b849-9f1d47824e1c/CommonsChamber\" target=\"_blank\" rel=\"noopener\">Read it in Hansard</a>",
     "#exchange-nov", "Watch the clip", ""),
    ("2026-11-10", "written", "What is the Government doing for Joshua?", "Written question · Richard Holden MP",
     "Richard Holden MP asked the Foreign Secretary what diplomatic steps he is taking on Joshua’s detention following the new ten-year sentence. Tabled 10 November for answer on 12 November.",
     "https://commonsbusiness.parliament.uk/Document/108853/Html?subType=Standard", "Order Paper", ""),
    ("2026-10-22", "report", "Six-monthly Report on Hong Kong", "Foreign Secretary · Report to Parliament",
     "The Government’s report for January to June 2026 cites developments in Joshua’s case as reinforcing concerns about the broad use of national security legislation.",
     "https://www.gov.uk/government/publications/six-monthly-report-on-hong-kong-january-to-june-2026/six-monthly-report-on-hong-kong-1-january-to-30-june-2026", "GOV.UK", ""),
    ("2026-10-13", "event", "The film is shown in Parliament", "Committee Room 15 · Houses of Parliament",
     "<em>Joshua: Prisoner vs. Superpower</em> was first shown to parliamentarians on Joshua’s 30th birthday.",
     "film.html", "Watch the film", ""),
    ("2026-09-01", "commons", "“Enough is enough”", "Foreign Office Questions · House of Commons",
     "Sir Iain Duncan Smith urged the Government to raise Joshua’s case with Beijing. Foreign Secretary Ed Miliband said he would take it up. No update has been made public since.",
     "#exchange", "Watch the exchange", "2026-09-01"),
    ("2025-12-17", "lords", "Named in the Lords after Jimmy Lai’s conviction", "Jimmy Lai Conviction · House of Lords",
     "Lord Alton asked what the Government is doing to raise the cases of pro-democracy prisoners “such as Joshua Wong and Andy Li”.",
     "https://parallelparliament.co.uk/debate/2025-12-17/lords/lords-chamber/jimmy-lai-conviction", "Read the debate", ""),
    ("2025-10-28", "commons", "Hong Kong human rights violations", "House of Commons",
     "MPs pressed ministers on Hong Kong, noting that Joshua had been rearrested and faced new charges under the National Security Law.",
     "https://hansard.parliament.uk/Commons/2025-10-28/debates/FCFA35AB-A007-4F6D-BF8A-3D80321D4046/HongKongHumanRightsViolations", "Hansard", ""),
    ("2025-10-23", "report", "His re-arrest on the record", "Foreign Secretary · Report to Parliament",
     "The six-monthly report for January to June 2025 records Joshua’s re-arrest on 6 June on suspicion of collusion with foreign forces.",
     "https://www.gov.uk/government/publications/six-monthly-report-on-hong-kong-january-to-june-2025/six-monthly-report-on-hong-kong-1-january-to-30-june-2025", "GOV.UK", ""),
    ("2025-07-03", "written", "The UK is “deeply concerned”", "Written question · Alicia Kearns MP",
     "Answering Alicia Kearns MP, the Foreign Office said it was deeply concerned by the further charges against Joshua.",
     "https://www.parallelparliament.co.uk/question/63014/hong-kong-politics-and-government", "Parliamentary answer", ""),
]
KINDS = [("commons", "Commons"), ("lords", "Lords"), ("written", "Written questions"), ("report", "Government reports"), ("event", "In Parliament")]
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

VIDEOS = [
    ("film.html", "Film", "Joshua: Prisoner vs. Superpower", "The new short film, first shown in Parliament on 13 October 2026.", "images/film-poster.jpg", False),
    ("#exchange-nov", "House of Commons · 10 Nov 2026", "Emily Darlington MP", "Asks the Government to call for Joshua’s release, five days after his sentence.", "images/commons-2026-11-10-poster.jpg", False),
    ("#exchange-kearns", "House of Commons · 10 Nov 2026", "Alicia Kearns MP", "For the Opposition: Joshua and Jimmy Lai remain imprisoned for speaking out for democracy.", "images/commons-2026-11-10-kearns-poster.jpg", False),
    ("https://podcasts.apple.com/gb/podcast/today-in-focus/id1440133626", "The Guardian · Today in Focus · 13 Nov 2026", "Teen prodigy, Netflix star, prisoner", "Podcast: Nathan Law and journalist Danny Vincent on Joshua’s story and his new sentence.", "images/covers/guardian-podcast.jpg", True),
    ("https://www.facebook.com/skynews/videos/friend-of-joshua-wong-nathan-law/2072604186823325/", "Sky News · 5 Nov 2026", "Nathan Law on Sky News", "On the day of the sentence, Nathan tells Yalda Hakim that democracy and human rights are “losing ground globally”.", "images/stills/sky-nathan.jpg", True),
    ("https://www.youtube.com/watch?v=gwQ1bK0KSJE", "Byline Times TV", "Andrew Duncan on Joshua’s story", "Video: the filmmaker behind both Joshua films on where Joshua is now.", "images/covers/byline-tv.jpg", True),
    ("#exchange", "House of Commons · 1 Sep 2026", "Duncan Smith and the Foreign Secretary", "The exchange at Foreign Office Questions, the day before Joshua’s plea.", "images/commons-poster.jpg", False),
    ("https://podcasts.apple.com/gb/podcast/byline-times-podcast/id1522910878", "Byline Times Podcast · 26 Oct 2026", "China vs Joshua Wong", "Podcast: filmmaker Andrew Duncan tells Joshua’s story to Adrian Goldberg.", "images/covers/byline-podcast.jpg", True),
    ("https://www.channel4.com/news/hong-kong-pro-democracy-activist-joshua-wong-pleads-guilty-to-colluding-with-foreign-entities", "Channel 4 News · 2 Sep 2026", "Joshua pleads guilty", "Channel 4 News reports on the plea, with analysis on China and the UK.", "images/covers/c4-plea.jpg", True),
    ("https://pelosi.house.gov/news/press-releases/pelosi-calls-joshua-wongs-freedom-house-floor-we-want-be-sure-they-know-we", "US House of Representatives · 2 Sep 2026", "Pelosi on the House floor", "Speaker Emerita Nancy Pelosi calls for Joshua’s freedom.", "images/covers/pelosi-floor.jpg", True),
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
        <div class="vc-img">{art}<span class="vc-play"></span>{'<span class="vc-ext">Opens on '+ ('YouTube' if 'youtube' in url else 'Apple Podcasts' if 'podcasts.apple' in url else 'Facebook' if 'facebook.com' in url else 'their site') +'</span>' if ext else ''}</div>
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
        <div><div class="rec-who">{who}</div><h3>{title}</h3><p>{body}</p>{wait}<a class="src" href="{url}"{tgt}>{link}</a></div>
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
          <p>At an urgent question secured by Sir Iain Duncan Smith on China obtaining MPs’ data, five days after Joshua was sentenced, she asked the Government to summon the Chinese Ambassador and call for his release, as it did for Jimmy Lai.</p>
        </div>
        <div class="px-sp">
          <div class="px-name">Dan Jarvis MP</div>
          <div class="px-role">Minister of State for Security</div>
          <p>Replying to her: “The Government share the concerns about Mr Wong and Jimmy Lai.”</p>
        </div>

        <p class="px-link"><a href="https://hansard.parliament.uk/Commons/2026-11-10/debates/580a4a8b-77d1-4dad-b849-9f1d47824e1c/CommonsChamber" target="_blank" rel="noopener">Read the exchange in Hansard</a></p>
        <div data-share data-url="https://freejoshuawong.org/parliament.html#exchange-nov" data-text="In the Commons, Emily Darlington MP asked the Government to call for Joshua Wong’s release. #FreeJoshuaWong"></div>
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
        <p class="px-link"><a href="https://hansard.parliament.uk/Commons/2026-11-10/debates/580a4a8b-77d1-4dad-b849-9f1d47824e1c/CommonsChamber" target="_blank" rel="noopener">Read it in Hansard</a></p>
        <div data-share data-url="https://freejoshuawong.org/parliament.html#exchange-kearns" data-text="Alicia Kearns MP in the Commons: Jimmy Lai and Joshua Wong remain imprisoned for speaking out for democracy. #FreeJoshuaWong"></div>
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
          <p>Asked the Government to raise Joshua’s case with Beijing.</p>
        </div>
        <div class="px-sp">
          <div class="px-name">Ed Miliband</div>
          <div class="px-role">Foreign Secretary</div>
          <p>Said he would take up Joshua’s case.</p>
        </div>
        <div class="px-count"><b data-since="2026-09-01">73</b><span>days since that promise.<br>No update has been made public.</span></div>
        <div data-share data-url="https://freejoshuawong.org/parliament.html" data-text="The Foreign Secretary promised to take up Joshua Wong’s case. No update since. #FreeJoshuaWong"></div>
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
    <p class="rec-note">Know of a mention we’ve missed? Tell us at press@freejoshuawong.org.</p>
  </div>
</section>
""" + CTA.replace("{up}", "") + footer()

# ---------------- VOICES ----------------
def voices():
    return head("Voices", "What parliamentarians, governments and human rights leaders are saying about Joshua Wong.", "voices.html") + nav("voices.html") + page_head(
        "Voices", "They are <em>speaking up</em>",
        "Parliamentarians, governments and human rights leaders, in their own words. Every quote links to where it was said.") + """
<section class="voices-page" style="border-top:0;padding-top:0">
  <div class="wrap">
    <div class="v-stats" id="v-stats"></div>
    <a class="to-socials" href="socials.html"><b>On social media</b><span>See what MPs, ministers, governments and campaigners are posting about Joshua</span></a>
    <div class="v-sec"><h2 class="sec">On the <em>record</em></h2><p>In Parliament, in Congress, and in official statements.</p></div>
    <div class="filters v-bar" role="group" aria-label="Filter voices">
      <button class="chip" data-k="all" aria-pressed="true">Everyone</button>
      <button class="chip" data-k="parliament" aria-pressed="false">Parliamentarians</button>
      <button class="chip" data-k="government" aria-pressed="false">Governments</button>
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
        <p class="lede">Copy a line, add your MP’s handle, and post it with #FreeJoshuaWong. If you are a parliamentarian or public figure and have spoken about Joshua, tell us at press@freejoshuawong.org and we’ll add you here.</p>
      </div>
      <div class="av-posts">
        <div class="post"><p>Joshua Wong was two months from freedom. Hong Kong has given him ten more years for speaking up to foreign parliaments. <b>#FreeJoshuaWong</b></p><button class="copy" type="button">Copy</button><a class="sh-x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=Joshua%20Wong%20was%20two%20months%20from%20freedom.%20Hong%20Kong%20has%20given%20him%20ten%20more%20years%20for%20speaking%20up%20to%20foreign%20parliaments.%20%23FreeJoshuaWong&url=https%3A%2F%2Ffreejoshuawong.org">Post on X</a></div>
        <div class="post"><p>The Foreign Secretary promised to take up Joshua Wong’s case on 1 September. We’re still waiting. <b>#FreeJoshuaWong</b></p><button class="copy" type="button">Copy</button><a class="sh-x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=The%20Foreign%20Secretary%20promised%20to%20take%20up%20Joshua%20Wong%E2%80%99s%20case%20on%201%20September.%20We%E2%80%99re%20still%20waiting.%20%23FreeJoshuaWong&url=https%3A%2F%2Ffreejoshuawong.org%2Fparliament.html">Post on X</a></div>
        <div class="post"><p>He has been in prison since he was 24. He may not walk free until he is 40. <b>#FreeJoshuaWong</b></p><button class="copy" type="button">Copy</button><a class="sh-x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=He%20has%20been%20in%20prison%20since%20he%20was%2024.%20He%20may%20not%20walk%20free%20until%20he%20is%2040.%20%23FreeJoshuaWong&url=https%3A%2F%2Ffreejoshuawong.org">Post on X</a></div>
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
    page = head(title, f"{v['who']} on Joshua Wong. #FreeJoshuaWong", f"voices/{v['slug']}.html", 1)
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
    <p class="rec-note">Seen a post we’ve missed? Send the link to press@freejoshuawong.org. We link to posts rather than embedding them, so your visit here isn’t tracked by social media companies.</p>
  </div>
</section>

<section class="add-voice">
  <div class="wrap">
    <div class="av">
      <div>
        <div class="label">Add your voice</div>
        <h2 class="sec">Post it. <em>Tag your MP.</em></h2>
        <p class="lede">Copy a line, add your MP’s handle, and post it with #FreeJoshuaWong.</p>
      </div>
      <div class="av-posts">
        <div class="post"><p>Joshua Wong was two months from freedom. Hong Kong has given him ten more years for speaking up to foreign parliaments. <b>#FreeJoshuaWong</b></p><button class="copy" type="button">Copy</button><a class="sh-x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=Joshua%20Wong%20was%20two%20months%20from%20freedom.%20Hong%20Kong%20has%20given%20him%20ten%20more%20years%20for%20speaking%20up%20to%20foreign%20parliaments.%20%23FreeJoshuaWong&url=https%3A%2F%2Ffreejoshuawong.org">Post on X</a></div>
        <div class="post"><p>The Foreign Secretary promised to take up Joshua Wong’s case on 1 September. We’re still waiting. <b>#FreeJoshuaWong</b></p><button class="copy" type="button">Copy</button><a class="sh-x" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=The%20Foreign%20Secretary%20promised%20to%20take%20up%20Joshua%20Wong%E2%80%99s%20case%20on%201%20September.%20We%E2%80%99re%20still%20waiting.%20%23FreeJoshuaWong&url=https%3A%2F%2Ffreejoshuawong.org%2Fparliament.html">Post on X</a></div>
      </div>
    </div>
  </div>
</section>
""" + footer(0, '<script src="assets/socials.js"></script>\n')

# ---------------- LETTER TO THE TIMES ----------------
TIMES_SIGNATORIES = ["Emily Darlington MP", "Bobby Dean MP", "Lord David Alton of Liverpool", "Lord Patten of Barnes",
    "Sir Geoffrey Nice KC", "Sir Malcolm Rifkind", "Lord Shinkwin", "Baroness Bennett of Manor Castle"]

def letter_times():
    sig = "".join(f"<li>{n}</li>" for n in TIMES_SIGNATORIES)
    return head("Unjust prosecution: letter to The Times", "MPs and peers write to The Times: Britain should summon the Chinese ambassador, sanction those responsible and say what further consequences will follow.", "letters/times-letter-nov-2026.html", 1) + nav("newsroom.html", 1) + page_head(
        "", "Unjust <em>prosecution</em>",
        "A letter to the editor of The Times from MPs and peers across the parties, published on 11 November 2026.",
        crumbs='<a href="../newsroom.html#letters">Newsroom</a> &nbsp;/&nbsp; Letters &amp; releases') + """
<section class="letters letter-page" style="border-top:0">
  <div class="wrap">
    <div class="letter">
      <article class="paper">
        <div class="head">Letter to the editor · The Times · 11 November 2026</div>
        <p style="margin-top:22px">Sir,</p>
        <p>Your leading article is right to ask what Britain will do for Joshua Wong (“Supine Silence”, Nov 6). The government has joined nine allies in calling for an end to “unjust prosecutions” under Hong Kong’s national security law, but condemnation is a statement, not a policy. Joshua Wong, who has been sentenced to ten years’ imprisonment, stood up for the Sino-British joint declaration, a treaty Britain signed and registered at the United Nations, which our own government says China has breached. <strong>A treaty broken without cost invites the next breach.</strong></p>
        <p>The government should summon the Chinese ambassador, as it did for Jimmy Lai; sanction those responsible for national security law prosecutions, as the US has; and tell parliament what further consequences will follow if Jimmy Lai, Joshua Wong and Benny Tai are not freed.</p>
        <p class="no-print" style="font-family:var(--label);font-size:14px">Published in The Times: <a href="https://www.thetimes.com/comment/letters-to-editor/article/times-letters-civil-service-needs-urgent-reform-wq3bcj955" target="_blank" rel="noopener">read it on thetimes.com</a> (subscription may be needed). The letter responds to The Times’s leading article, <a href="https://www.thetimes.com/comment/the-times-view/article/joshua-wong-jailed-hong-kong-uk-china-nn9c6vpzc" target="_blank" rel="noopener">“Supine Silence”</a>.</p>
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

PAGES = {
    "index.html": home, "case.html": case, "film.html": film, "newsroom.html": newsroom,
    "resources.html": resources, "act.html": act, "parliament.html": parliament, "voices.html": voices, "socials.html": socials,
    "letters/open-letter-prime-minister-sept-2026.html": letter_pm,
    "letters/times-letter-nov-2026.html": letter_times,
}

def bake_numbers(html):
    """Write today's counts into the page so they are right even before the page's script runs."""
    import re, datetime
    from sharecard import days_inside
    today = datetime.date.today()
    def since(m):
        y, mo, d = map(int, m.group(1).split("-"))
        return f'data-since="{m.group(1)}">{(today - datetime.date(y, mo, d)).days}<'
    html = re.sub(r'data-since="(\d{4}-\d{2}-\d{2})">[^<]*<', since, html)
    html = re.sub(r'(id="days">)[^<]*(<)', lambda m: f"{m.group(1)}{days_inside():,}{m.group(2)}", html)
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
    for path, fn in PAGES.items():
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            f.write(bake_numbers(fn()))
        print("wrote", path)
