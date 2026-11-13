#!/usr/bin/env python3
"""Builds the Free Joshua Wong site pages from shared header/footer.
Run from the repo root:  python3 tools/build.py
Edit page content in this file, then re-run. Output: *.html in the repo root and letters/."""
import os

SITE = "https://freejoshuawong.org"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV = [("case.html", "The case"), ("film.html", "Film"), ("newsroom.html", "Newsroom"), ("resources.html", "Resources")]

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
<meta property="og:image" content="{SITE}/images/joshua.jpg">
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
    </div>
    <div class="cols">
      <nav aria-label="Footer">
        <a href="{up}case.html">The case</a><a href="{up}film.html">Film</a><a href="{up}newsroom.html">Newsroom</a>
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
    <div class="fact"><div class="n">+10 years</div><div class="t">Added on 5 November 2026</div></div>
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
          <div class="cell-clock" id="clock">and counting</div>
        </div>
      </div>
    </div>
    <p class="h4-lead">The Hong Kong democracy campaigner was due to walk free in January 2027. On 5 November, a court gave him ten more years.</p>
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
    <p class="by">Joshua Wong, in a letter from prison after his sentence</p>
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

<section class="h4-asks">
  <div class="wrap">
    <h2>What Britain should do</h2>
    <p class="h4-sub">Britain guaranteed Hong Kong’s freedoms in 1984. Ten governments, including our own, have condemned Joshua’s sentence. Now words need to become action.</p>
    <div class="asklist">
      <div><h3>Raise his case with China’s ambassador</h3><p>The Prime Minister should call in the Ambassador and name Joshua and the others jailed for standing up for democracy.</p></div>
      <div><h3>Review the Hong Kong trade office</h3><p>Its London office keeps diplomatic-style privileges, even after a senior manager there was convicted of spying on Hong Kongers in Britain.</p></div>
      <div><h3>Sanction those responsible</h3><p>Hold the officials behind National Security Law prosecutions to account, together with Britain’s allies.</p></div>
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
  function tick(){var ms=Date.now()-start, s=Math.floor(ms/1000)%86400;
    clock.textContent=pl(Math.floor(s/3600),'hour')+', '+pl(Math.floor(s%3600/60),'minute')+' and '+pl(s%60,'second')+', and counting';}
  var total=Math.floor((Date.now()-start)/864e5);
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){el.textContent=fmt(total);}
  else{var t0=null;(function step(ts){if(!t0)t0=ts;var k=Math.min(1,(ts-t0)/1600);k=1-Math.pow(1-k,3);el.textContent=fmt(Math.round(total*k));if(k<1)requestAnimationFrame(step);})(performance.now());}
  tick(); setInterval(function(){tick(); el.textContent=fmt(Math.floor((Date.now()-start)/864e5));},1000);
})();
</script>
""" + footer(0)

LATEST = [
    ("Taipei Times", "Editorial: Joshua Wong was due for release in January", "7 Nov 2026", "https://www.taipeitimes.com/News/editorials/archives/2026/11/07/2003867296"),
    ("Reuters / CTV", "Canada, US, UK and others condemn 10-year sentence for Joshua Wong", "6 Nov 2026", "https://www.ctvnews.ca/world/article/canada-us-uk-and-others-condemn-10-year-sentence-for-hong-kong-activist-joshua-wong/"),
    ("The Spectator", "Joshua Wong’s imprisonment shows China is running scared", "5 Nov 2026", "https://www.spectator.com.au/?p=10947071"),
    ("Human Rights Watch", "Joshua Wong gets nearly 10 more years in prison", "5 Nov 2026", "https://www.hrw.org/news/2026/11/05/hong-kong-joshua-wong-gets-nearly-10-more-years-in-prison"),
]

# ---------------- THE CASE ----------------
TIMELINE = [
    ("Born", "Oct 1996", "", "Born in Hong Kong", "Joshua Wong Chi-fung grows up in a city promised a high degree of autonomy until 2047."),
    ("15", "Sep 2012", "", "Defeats a Beijing curriculum", "With the student group Scholarism, which he co-founded at 14, he leads the protests that force the Hong Kong government to shelve a compulsory “national education” curriculum."),
    ("17", "Sep 2014", "", "The Umbrella Movement", "His arrest at Civic Square helps spark 79 days of street occupation demanding genuine universal suffrage. <em>Time</em> puts him on its cover."),
    ("19", "Oct 2016", "", "Detained at Bangkok airport", "Held and deported by Thai authorities on his way to speak at a university, an early sign of how far Beijing’s pressure would reach."),
    ("20", "2017", "", "First prison sentence, and the film", "Jailed over the 2014 Civic Square protest; Hong Kong’s top court later quashes the sentence. <em>Joshua: Teenager vs. Superpower</em> premieres at Sundance and wins the audience award."),
    ("22", "Sep 2019", "", "Testifies to the US Congress", "Gives evidence to the Congressional-Executive Commission on China on human rights in Hong Kong. Years later, testimony like this is cited as evidence against him."),
    ("23", "Jun 2020", "", "The National Security Law", "Beijing imposes the National Security Law on Hong Kong. His party, Demosistō, disbands the same day."),
    ("24", "Nov 2020", "", "Into prison, where he remains", "Jailed over a 2019 protest outside police headquarters. He has not been free since."),
    ("24", "Jan 2021", "", "Charged as one of the Hong Kong 47", "Arrested under the National Security Law for taking part in an unofficial pro-democracy primary election."),
    ("28", "Nov 2024", "", "Sentenced to 4 years 8 months", "Sentenced in the largest national security trial in Hong Kong’s history. His release date is set for early 2027."),
    ("28", "Jun 2025", "", "Charged again from his cell", "Charged with conspiracy to collude with foreign forces, carrying a maximum of life imprisonment. The evidence is his own advocacy and public statements."),
    ("30", "13 Oct 2026", "", "Turns thirty in prison", "Parliamentarians mark his birthday with a screening of the new film in the Houses of Parliament."),
    ("30", "5 Nov 2026", "", "Ten more years", "A Hong Kong court sentences him to ten years. Ten governments, including the UK, condemn the sentence the next day."),
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
        <p>Joshua Wong has campaigned for democracy in Hong Kong since he was a schoolboy. At fifteen he stopped a Beijing-written curriculum; at seventeen he was the face of the Umbrella Movement; at twenty he was the subject of an award-winning Netflix documentary.</p>
      </div>
      <div>
        <h3>What he is charged with</h3>
        <p>“Conspiracy to collude with foreign forces” under the National Security Law, a law imposed by Beijing in 2020.</p>
        <ul>
          <li><strong>The evidence is his own words:</strong> testimony to parliaments and human rights bodies, interviews and op-eds.</li>
          <li><strong>Much of it predates the law:</strong> the prosecution relies largely on advocacy from before the law existed.</li>
          <li><strong>He was already in prison:</strong> he was charged from his cell, while still serving another sentence.</li>
          <li><strong>The result:</strong> ten more years, handed down on 5 November 2026.</li>
        </ul>
      </div>
    </div>
    <p class="pull">He is serving a sentence for believing us.</p>
    <div class="why">
      <div><div class="k">1984</div><h4>Britain gave its word</h4><p>The UK signed the Joint Declaration and guaranteed Hong Kong’s freedoms for fifty years. The Government has itself declared China in breach of it.</p></div>
      <div><div class="k">2026</div><h4>It has reached our streets</h4><p>Two men were jailed at the Old Bailey this year for spying on Hong Kong dissidents in Britain. Hong Kongers settled here have bounties on their heads.</p></div>
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
    return head("Film", "Joshua: Prisoner vs. Superpower — a new short film from the team behind the 2017 Sundance award winner.", "film.html") + nav("film.html") + page_head(
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
        <p><a class="btn" href="film.html">More on the film</a></p>
        <div data-share data-url="https://freejoshuawong.org/film.html" data-text="Joshua: Prisoner vs. Superpower — the second chapter"></div>
      </div>
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
      <div class="titem"><div class="d">6 Nov 2026</div><div>
          <div class="who">Joint statement · 10 foreign ministries</div>
          <h3>Ten governments, including the UK, condemn the sentence</h3>
          <div class="flags"><span>UK</span><span>US</span><span>Australia</span><span>Canada</span><span>France</span><span>Germany</span><span>Italy</span><span>Japan</span><span>Netherlands</span><span>New Zealand</span></div>
          <p>The day after sentencing, the foreign ministries said the case shows how the National Security Law is used to target people for political expression. They called for an end to unjust NSL prosecutions and for the rights promised under the 1984 Sino-British Joint Declaration to be honoured.</p>
          <a class="src" href="https://www.dfat.gov.au/news/statement-sentencing-joshua-wong" target="_blank" rel="noopener">Read the statement →</a></div></div>
      <div class="titem"><div class="d">5 Nov 2026</div><div>
          <div class="who">US Consulate General, Hong Kong</div>
          <div class="flags"><span>US</span></div>
          <h3>“Unjustly imprisoned”</h3>
          <p>The US Consulate said Joshua has been unjustly imprisoned since late 2020, and that Beijing will go to extraordinary lengths to silence those who advocate for fundamental freedoms.</p>
          <a class="src" href="https://www.wamc.org/2026-11-05/hong-kong-activist-joshua-wong-is-sentenced-to-10-more-years-in-prison" target="_blank" rel="noopener">AP report →</a></div></div>
      <div class="titem"><div class="d">22 Oct 2026</div><div>
          <div class="who">UK Foreign Secretary · Report to Parliament</div>
          <div class="flags"><span>UK</span></div>
          <h3>Named in the Six-monthly Report on Hong Kong</h3>
          <p>The Government’s report to Parliament cites developments in Joshua’s case as reinforcing concerns about the increasingly broad application of national security legislation.</p>
          <a class="src" href="https://www.gov.uk/government/publications/six-monthly-report-on-hong-kong-january-to-june-2026/six-monthly-report-on-hong-kong-1-january-to-30-june-2026" target="_blank" rel="noopener">GOV.UK →</a></div></div>
      <div class="titem"><div class="d">2 Sep 2026</div><div>
          <div class="who">US House of Representatives</div>
          <div class="flags"><span>US</span></div>
          <h3>Nancy Pelosi calls for his freedom on the House floor</h3>
          <blockquote>“We must speak out for freedom. We must not let this be ignored.”</blockquote>
          <a class="src" href="https://pelosi.house.gov/news/press-releases/pelosi-calls-joshua-wongs-freedom-house-floor-we-want-be-sure-they-know-we" target="_blank" rel="noopener">Speaker Emerita Pelosi →</a></div></div>
      <div class="titem"><div class="d">28 Oct 2025</div><div>
          <div class="who">House of Commons · FCDO oral questions</div>
          <div class="flags"><span>UK</span></div>
          <h3>Raised in the Commons</h3>
          <p>MPs pressed ministers on Hong Kong human rights, noting that Joshua had been rearrested and faced further charges under the National Security Law.</p>
          <a class="src" href="https://hansard.parliament.uk/Commons/2025-10-28/debates/FCFA35AB-A007-4F6D-BF8A-3D80321D4046/HongKongHumanRightsViolations" target="_blank" rel="noopener">Hansard →</a></div></div>
      <div class="titem" style="padding-bottom:0"><div class="d">Jun 2025</div><div>
          <div class="who">Written question · Alicia Kearns MP</div>
          <div class="flags"><span>UK</span></div>
          <h3>The UK is “deeply concerned”</h3>
          <p>Answering Alicia Kearns MP, the Foreign Office said it was deeply concerned by the news of further charges against Joshua.</p>
          <a class="src" href="https://www.parallelparliament.co.uk/question/63014/hong-kong-politics-and-government" target="_blank" rel="noopener">Parliamentary answer →</a></div></div>
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
      <div class="sec-head" style="margin-bottom:28px">
        <p class="lede" style="max-width:56ch">Newest first. We link to the original article; some outlets may ask you to subscribe.</p>
        <div class="filters" role="group" aria-label="Filter coverage">
          <button class="chip" data-f="all" aria-pressed="true">All</button>
          <button class="chip" data-f="opinion" aria-pressed="false">Opinion</button>
          <button class="chip" data-f="news" aria-pressed="false">News</button>
          <button class="chip" data-f="rights" aria-pressed="false">Rights groups</button>
        </div>
      </div>
      <div class="press-grid" id="press-grid"></div>
    </div>

    <div class="panel" id="panel-statements" hidden>
      <p class="lede" style="margin-bottom:44px">Joshua’s case has been raised in the House of Commons, in the US Congress and by foreign ministries on three continents.</p>
      """ + STATEMENTS + """
    </div>

    <div class="panel" id="panel-letters" hidden>
      <p class="lede" style="margin-bottom:34px">Letters sent by the campaign and its supporters, and our statements to the media.</p>
      <div class="rel">
        <div class="d">Sep 2026</div>
        <div>
          <div class="type">Open letter · to the Prime Minister</div>
          <h3><a href="letters/open-letter-prime-minister-sept-2026.html">Britain should stand for something</a></h3>
          <p>Parliamentarians from every major party, two former Foreign Secretaries and leading human rights organisations ask the Prime Minister to raise Joshua’s case with the Chinese Ambassador.</p>
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
    ("Benedict Rogers", "Co-founder and Chair, Hong Kong Watch"), ("Jemimah Steinfeld", "Chief Executive, Index on Censorship"),
    ("The Rt Hon Tom Tugendhat MBE VR MP", "Shadow Foreign Secretary"), ("Bess Weatherman", "Co-Founder, RT Weatherman Foundation"),
]

def letter_pm():
    sig = "".join(f"<li>{n}{f'<small>{r}</small>' if r else ''}</li>" for n, r in SIGNATORIES)
    return head("Open letter to the Prime Minister", "Parliamentarians and human rights organisations ask the Prime Minister to raise Joshua Wong’s case with the Chinese Ambassador.", "letters/open-letter-prime-minister-sept-2026.html", 1) + nav("newsroom.html", 1) + page_head(
        "", "Britain should <em>stand for something</em>",
        "An open letter to the Prime Minister, September 2026.",
        crumbs='<a href="../newsroom.html#letters">Newsroom</a> &nbsp;/&nbsp; Letters &amp; releases') + """
<section class="letters letter-page" style="border-top:0">
  <div class="wrap">
    <div class="letter">
      <article class="paper">
        <div class="meta"><span class="status" style="margin:0"><i></i> Awaiting a reply from Downing Street</span></div>
        <div class="head">Open letter to the Prime Minister · September 2026</div>
        <p style="margin-top:22px">Dear Prime Minister,</p>
        <p>This week, you said ‘it is more important than ever that Britain stands for something.’ The Foreign Secretary went further: that governments ‘have to make our own decisions about legality, values’ and act on them.</p>
        <p>We agree. We are asking you to apply that principle to Hong Kong and the Joint Declaration, and hold China to account for its abusive use of the National Security Law, criminalising peaceful democratic activity.</p>
        <p>Joshua Wong has been a pro-democracy advocate since he was a child. At 15 he founded a movement to resist Beijing’s education law and went on to become the face of the Umbrella Movement. His work always sought to hold Beijing to the 1997 agreement, ‘One Country, Two Systems’, agreed between the UK and China. But in 2020 he was arrested and detained. Now, like British Citizen Jimmy Lai, he faces the prospect of life in prison.</p>
        <p>This is not a distant problem. Two men were convicted at the Old Bailey this year for spying on Hong Kong dissidents in Britain, reportedly also monitoring British parliamentarians. Police are investigating footage appearing to show Chinese embassy security in London brandishing banned electroshock weapons at peaceful protesters. Hong Kongers settled in the UK have bounties on their heads. China’s National Security Law is felt on the streets of Britain.</p>
        <p>The UK has a moral and diplomatic responsibility, arising from the 1997 handover and the Joint Declaration, to speak out for those who stood up for the treaty it guaranteed. The UK Government has already found China in breach of the treaty. In December, the last Foreign Secretary told the Commons plainly: “China breached the Joint Declaration by imposing its National Security Law on the city.”</p>
        <p>It is time that you called the Chinese Ambassador to raise Joshua’s case and that of the others imprisoned for standing up for democracy.</p>
        <p><strong>Britain signed the Joint Declaration and guaranteed Hong Kong’s freedoms for fifty years. Joshua Wong only ever asked his government to keep its word. We are asking ours to keep it too.</strong></p>
        <p class="sign">Written before Joshua was sentenced on 5 November 2026.</p>
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
        <dt>Who</dt><dd>Joshua Wong Chi-fung, born 13 October 1996, Hong Kong. Democracy campaigner since age 14; leader of the 2012 campaign against a Beijing-written curriculum and a face of the 2014 Umbrella Movement.</dd>
        <dt>In prison since</dt><dd>November 2020, continuously.</dd>
        <dt>Latest sentence</dt><dd>Ten years, handed down 5 November 2026, for “conspiracy to collude with foreign forces” under the National Security Law.</dd>
        <dt>Previous release date</dt><dd>January 2027, at the end of his 4 year 8 month sentence in the Hong Kong 47 case.</dd>
        <dt>Possible release</dt><dd>Around 2036, when he will be about 40.</dd>
        <dt>The evidence</dt><dd>His own advocacy: testimony to parliaments and human rights bodies, interviews and op-eds, much of it from before the law existed.</dd>
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
        "“The only thing I worry about is that people will forget Hong Kong.” Joshua, writing from prison after his sentence.") + """
<section style="border-top:0;padding-top:30px" id="mp">
  <div class="wrap">
    <div class="mp" style="margin-top:0">
      <div>
        <div class="label" style="color:#6f6a2a">In the UK</div>
        <h3>Write to your MP</h3>
        <p>Ask them to raise Joshua’s case with the Foreign Secretary. Copy the letter, then find your MP with your postcode and paste it in.</p>
        <a class="btn dark" href="https://www.writetothem.com" target="_blank" rel="noopener">Find my MP →</a>
        <p style="font-size:14px;margin-top:16px;color:rgba(12,12,11,.65)">WriteToThem is run independently by mySociety. We don’t see or store anything you send.</p>
      </div>
      <div>
        <div class="tpl" id="tpl">Dear [MP name],

I am writing as your constituent about Joshua Wong, the Hong Kong democracy campaigner who on 5 November was sentenced to a further ten years in prison under the National Security Law.

Britain guaranteed Hong Kong’s freedoms in the Joint Declaration. Joshua only ever asked that this promise be kept.

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

PAGES = {
    "index.html": home, "case.html": case, "film.html": film, "newsroom.html": newsroom,
    "resources.html": resources, "act.html": act,
    "letters/open-letter-prime-minister-sept-2026.html": letter_pm,
}

if __name__ == "__main__":
    for path, fn in PAGES.items():
        out = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            f.write(fn())
        print("wrote", path)
