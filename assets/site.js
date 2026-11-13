// Free Joshua Wong — shared scripts
(function () {
  // Mobile menu
  var nav = document.querySelector('nav.top');
  var mb = document.querySelector('.menu-btn');
  if (nav && mb) mb.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    mb.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Copy buttons: data-target="id" copies that element's text; otherwise the sibling <p>; data-copy copies a literal value
  document.querySelectorAll('.copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var t = btn.getAttribute('data-target');
      var text = btn.getAttribute('data-copy') ||
        (t ? document.getElementById(t).innerText : btn.parentNode.querySelector('p').innerText);
      flashCopy(btn, text);
    });
  });

  function flashCopy(btn, text) {
    var orig = btn.textContent;
    function ok() { btn.textContent = 'Copied'; btn.classList.add('done'); setTimeout(function () { btn.textContent = orig; btn.classList.remove('done'); }, 1600); }
    try { navigator.clipboard.writeText(text).then(ok, function () { btn.textContent = 'Select & copy'; }); }
    catch (e) { btn.textContent = 'Select & copy'; }
  }

  // Film: load YouTube only when someone presses play (privacy-enhanced, no cookies until then)
  document.querySelectorAll('.screen.yt').forEach(function (b) {
    b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + b.getAttribute('data-yt') + '?autoplay=1&rel=0';
      f.title = 'Joshua: Prisoner vs. Superpower';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      f.className = 'yt-frame';
      b.replaceWith(f);
    });
  });

  // Share links
  window.shareRow = function (url, text) {
    var u = encodeURIComponent(url), t = encodeURIComponent(text + ' #FreeJoshuaWong');
    return '<div class="share-row"><span class="lbl">Share</span>' +
      '<a class="sh" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text=' + t + '&url=' + u + '">X</a>' +
      '<a class="sh" target="_blank" rel="noopener" href="https://wa.me/?text=' + t + '%20' + u + '">WhatsApp</a>' +
      '<a class="sh" target="_blank" rel="noopener" href="https://www.linkedin.com/sharing/share-offsite/?url=' + u + '">LinkedIn</a>' +
      '<button class="sh" type="button" data-link="' + url.replace(/"/g, '&quot;') + '">Copy link</button></div>';
  };
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('button.sh[data-link]');
    if (b) flashCopy(b, b.getAttribute('data-link'));
  });

  // Static share rows: <div data-share data-url="" data-text=""></div>
  document.querySelectorAll('[data-share]').forEach(function (el) {
    el.innerHTML = window.shareRow(el.getAttribute('data-url') || location.href, el.getAttribute('data-text') || document.title);
  });

  // Press cards
  var grid = document.getElementById('press-grid');
  if (grid && window.PRESS) {
    var limit = parseInt(grid.getAttribute('data-limit') || '0', 10);
    var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var render = function (f) {
      var items = window.PRESS.filter(function (p) { return f === 'all' || p.type === f; });
      if (f === 'all' && !limit) { // one featured piece at the top, the rest newest first
        var fi = items.findIndex(function (p) { return p.feature; });
        if (fi > 0) items = [items[fi]].concat(items.slice(0, fi), items.slice(fi + 1));
      }
      if (limit) items = items.slice(0, limit);
      grid.innerHTML = items.map(function (p, i) {
        var label = { opinion: 'Opinion', news: 'News', rights: 'Rights groups' }[p.type];
        var feat = p.feature && f === 'all' && !limit;
        return '<article class="pcard' + (feat ? ' feature' : '') + '">' +
          '<div class="outlet">' + esc(p.outlet) + (p.paywall ? '<span class="pay" title="This outlet may ask you to subscribe">Subscription</span>' : '') + '</div>' +
          '<div class="meta">' + esc(p.date) + ' · ' + label + (p.by ? ' · ' + esc(p.by) : '') + '</div>' +
          '<h3><a href="' + esc(p.url) + '" target="_blank" rel="noopener">' + esc(p.title) + '</a></h3>' +
          '<div class="foot"><a class="read" href="' + esc(p.url) + '" target="_blank" rel="noopener">Read at ' + esc(p.outlet) + ' →</a>' +
          window.shareRow(p.url, p.title) + '</div></article>';
      }).join('');
    };
    render('all');
    document.querySelectorAll('.chip').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('.chip').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true'); render(b.getAttribute('data-f'));
      });
    });
  }

  // Tabs (newsroom): #coverage, #statements, #letters
  var tabs = document.querySelectorAll('.tabs a');
  if (tabs.length) {
    var show = function () {
      var id = (location.hash || '#' + tabs[0].getAttribute('href').slice(1)).slice(1);
      if (!document.getElementById('panel-' + id)) id = tabs[0].getAttribute('href').slice(1);
      tabs.forEach(function (a) { a.setAttribute('aria-selected', a.getAttribute('href') === '#' + id ? 'true' : 'false'); });
      document.querySelectorAll('.panel').forEach(function (p) { p.hidden = p.id !== 'panel-' + id; });
    };
    window.addEventListener('hashchange', show); show();
  }
})();

// ===== Coverage wall (newsroom) =====
(function () {
  var list = document.getElementById('cov-list');
  if (!list || !window.PRESS) return;
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  var nice = function (d) { var p = d.split('-'); return (+p[2]) + ' ' + months[+p[1] - 1] + ' ' + p[0]; };
  var label = { news: 'News', opinion: 'Opinion', rights: 'Rights group' };
  var items = window.PRESS.slice().sort(function (a, b) { return a.date < b.date ? 1 : a.date > b.date ? -1 : 0; });
  var state = { moment: 'all', type: 'all' };

  // headline numbers
  var outlets = {}; items.forEach(function (p) { outlets[p.outlet.split(' / ')[0]] = 1; });
  var regions = {}; items.forEach(function (p) { if (p.region !== 'Global') regions[p.region] = 1; });
  document.getElementById('cov-stats').innerHTML =
    '<div><b>' + items.length + '</b><span>reports</span></div>' +
    '<div><b>' + Object.keys(outlets).length + '</b><span>outlets</span></div>' +
    '<div><b>' + Object.keys(regions).length + '</b><span>regions of the world</span></div>' +
    '<div><b>' + (+items[items.length - 1].date.slice(0, 4)) + '</b><span>covered since</span></div>';

  // ticker: newest twelve headlines, doubled for a seamless loop
  var tk = items.slice(0, 12).map(function (p) { return '<span class="tk"><b>' + esc(p.outlet) + '</b>' + esc(p.title) + '</span>'; }).join('');
  document.getElementById('ticker').innerHTML = tk + tk;

  // moment buttons with counts
  var mEl = document.getElementById('moments');
  var count = function (id) { return items.filter(function (p) { return id === 'all' || p.moment === id; }).length; };
  mEl.innerHTML = '<button class="mo" data-m="all" aria-pressed="true"><span class="w">June 2025 to now</span><span class="l">Everything</span><span class="c">' + count('all') + '</span></button>' +
    window.MOMENTS.slice().reverse().map(function (m) {
      return '<button class="mo" data-m="' + m.id + '" aria-pressed="false"><span class="w">' + m.when + '</span><span class="l">' + m.label + '</span><span class="c">' + count(m.id) + '</span></button>';
    }).join('');

  function render() {
    var shown = items.filter(function (p) { return (state.moment === 'all' || p.moment === state.moment) && (state.type === 'all' || p.type === state.type); });
    var feat = document.getElementById('cov-feature');
    var f = (state.moment === 'all' || state.moment === 'sentence') && state.type !== 'news' && state.type !== 'rights' ? items.filter(function (p) { return p.feature; })[0] : null;
    feat.innerHTML = f ? '<a class="cov-feat" href="' + esc(f.url) + '" target="_blank" rel="noopener"><span class="o">' + esc(f.outlet) + (f.by ? ', ' + esc(f.by) : '') + '</span><span class="h">' + esc(f.title) + '</span><span class="d">' + nice(f.date) + (f.paywall ? '<span class="pay">Subscription</span>' : '') + '</span></a>' : '';
    if (f) shown = shown.filter(function (p) { return p !== f; });
    var html = '', last = '';
    shown.forEach(function (p) {
      if (p.date !== last) {
        var n = shown.filter(function (q) { return q.date === p.date; }).length;
        html += (last ? '</div>' : '') + '<div class="day"><h3 class="day-h">' + nice(p.date) + '<span>' + n + (n === 1 ? ' report' : ' reports') + '</span></h3>';
        last = p.date;
      }
      html += '<article class="row"><div class="o">' + esc(p.outlet) + '<span class="tag">' + label[p.type] + ' · ' + esc(p.region) + '</span></div>' +
        '<h4><a href="' + esc(p.url) + '" target="_blank" rel="noopener">' + esc(p.title) + '</a>' + (p.paywall ? '<span class="pay">Subscription</span>' : '') + (p.by ? '<span class="by">' + esc(p.by) + '</span>' : '') + '</h4>' +
        window.shareRow(p.url, p.title) + '</article>';
    });
    list.innerHTML = html ? html + '</div>' : '<p class="empty">Nothing here yet for that combination. Try Everything.</p>';
  }
  render();
  mEl.addEventListener('click', function (e) {
    var b = e.target.closest('.mo'); if (!b) return;
    mEl.querySelectorAll('.mo').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
    b.setAttribute('aria-pressed', 'true'); state.moment = b.getAttribute('data-m'); render();
  });
  document.querySelectorAll('.cov-bar .chip').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.cov-bar .chip').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      b.setAttribute('aria-pressed', 'true'); state.type = b.getAttribute('data-t'); render();
    });
  });
})();

// ===== "Still waiting" day counters =====
document.querySelectorAll('[data-since]').forEach(function (el) {
  var p = el.getAttribute('data-since').split('-');
  var d = Math.floor((Date.now() - Date.UTC(+p[0], +p[1] - 1, +p[2])) / 864e5);
  if (d >= 0) el.textContent = d;
});

/* Parliament record filter */
(function () {
  var chips = document.querySelectorAll('.rec-bar .chip');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var k = c.getAttribute('data-k');
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      document.querySelectorAll('.rec').forEach(function (r) { r.hidden = k !== 'all' && r.getAttribute('data-k') !== k; });
    });
  });
})();

/* Voices wall */
(function () {
  var wall = document.getElementById('vwall');
  if (!wall || !window.VOICES) return;
  var V = window.VOICES.slice().sort(function (a, b) { return a.date < b.date ? 1 : -1; });
  var M = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var KIND = {parliament:'Parliamentarian', government:'Government', rights:'Rights group', social:'On social media'};
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function d(s) { var p = s.split('-'); return +p[2] + ' ' + M[+p[1] - 1] + ' ' + p[0]; }
  var countries = {}; V.forEach(function (v) { if (v.country && v.country !== 'Global') countries[v.country] = 1; });
  var st = document.getElementById('v-stats');
  if (st) st.innerHTML = '<b>' + V.length + '</b> voices &nbsp;·&nbsp; <b>' + Object.keys(countries).length + '</b> countries and blocs, plus global rights groups';
  function card(v) {
      var size = v.quote.length < 40 ? ' big' : (v.quote.length < 75 ? ' mid' : '');
      var ext = /^https?:/.test(v.url) ? ' target="_blank" rel="noopener"' : '';
      var slug = v.id || (v.who + '-' + v.date).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      var page = 'voices/' + slug + '.html', full = 'https://freejoshuawong.org/' + page;
      var t = '“' + v.quote + '” — ' + v.who + ' #FreeJoshuaWong';
      return '<figure class="vq k-' + v.kind + size + '">' +
        '<div class="vq-top"><span class="vq-where">' + esc(v.where) + '</span><span class="vq-date">' + d(v.date) + '</span></div>' +
        '<a class="vq-q" href="' + page + '"><blockquote>' + esc(v.quote) + '</blockquote></a>' +
        '<figcaption><b>' + esc(v.who) + '</b><span>' + esc(v.role) + (v.country && v.country !== 'Global' ? ' · ' + esc(v.country) : '') + '</span></figcaption>' +
        '<div class="vq-links"><a href="' + esc(v.url) + '"' + ext + '>' + (v.via ? 'As reported by ' + esc(v.via) : (/On (X|Twitter)/.test(v.where) ? 'See the post' : 'Original')) + '</a>' +
        (v.watch ? '<a href="' + esc(v.watch) + '">Watch</a>' : '') +
        '</div><div class="vq-share"><span>Share</span>' +
        '<a href="https://twitter.com/intent/tweet?text=' + encodeURIComponent(t) + '&url=' + encodeURIComponent(full) + '" target="_blank" rel="noopener">X</a>' +
        '<a href="https://wa.me/?text=' + encodeURIComponent(t + ' ' + full) + '" target="_blank" rel="noopener">WhatsApp</a>' +
        '<a href="https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(full) + '" target="_blank" rel="noopener">LinkedIn</a>' +
        '<button type="button" class="sh" data-link="' + full + '">Copy link</button>' +
        '<a href="images/quotes/' + slug + '.jpg" download>Image</a></div></figure>';
  }
  var soc = document.getElementById('vsocial');
  if (soc) soc.innerHTML = V.filter(function (v) { return v.kind === 'social'; }).map(card).join('');
  function render(k) {
    wall.innerHTML = V.filter(function (v) { return v.kind !== 'social' && (k === 'all' || v.kind === k); }).map(card).join('');
  }
  var chips = document.querySelectorAll('.v-bar .chip');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      render(c.getAttribute('data-k'));
    });
  });
  render('all');
})();

/* Socials wall */
(function () {
  var wall = document.getElementById('s-wall');
  if (!wall || !window.SOCIALS) return;
  var S = window.SOCIALS.slice().sort(function (a, b) { return a.date < b.date ? 1 : -1; });
  var M = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var G = {uk:'UK politicians', world:'Politicians worldwide', gov:'Governments', campaign:'Campaigners & rights groups', media:'Media'};
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function d(s) { var p = s.split('-'), y = +p[0]; return +p[2] + ' ' + M[+p[1] - 1] + (y !== 2026 ? ' ' + y : ''); }
  function initials(n) { return n.replace(/\(.*?\)|Sir |Lord |Senator |Secretary |The /g, '').split(/\s+/).filter(Boolean).slice(0, 2).map(function (w) { return w[0]; }).join('').toUpperCase(); }
  function body(t) {
    return esc(t).replace(/(#\w+)/g, '<span class="s-tag">$1</span>').replace(/(@\w+)/g, '<span class="s-tag">$1</span>')
      .replace(/Joshua Wong/g, '<mark>Joshua Wong</mark>').replace(/\n/g, '<br>');
  }
  function card(p, lead) {
    var link = p.url || (p.handle ? 'https://x.com/' + p.handle : p.profile);
    var here = 'https://freejoshuawong.org/socials.html#' + p.id;
    var t = p.name + ' on #FreeJoshuaWong';
    var src = p.via
      ? '<a href="' + esc(p.viaUrl) + '" target="_blank" rel="noopener">Posted on X · as reported by ' + esc(p.via) + '</a>'
      : '<a href="' + esc(link) + '" target="_blank" rel="noopener">' + (p.url ? 'See the post on X' : (p.handle ? 'See @' + esc(p.handle) + ' on X' : 'Visit their site')) + '</a>';
    var lk = p.link ? (p.link.url
      ? '<a class="s-link" href="' + esc(p.link.url) + '"' + (/^https?:/.test(p.link.url) ? ' target="_blank" rel="noopener"' : '') + '><small>' + esc(p.link.site) + '</small>' + esc(p.link.title) + '</a>'
      : '<div class="s-link"><small>' + esc(p.link.site) + '</small>' + esc(p.link.title) + '</div>') : '';
    return '<article class="s-post g-' + p.group + (lead ? ' s-lead' : '') + '" id="' + esc(p.id) + '">' +
      (lead ? '<div class="s-lead-k">In his own words · a letter from prison</div>' : '') +
      '<header><span class="s-av">' + initials(p.name) + '</span><div><b>' + esc(p.name) + '</b><span>' +
      (p.handle ? '@' + esc(p.handle) + ' · ' : '') + d(p.date) + '</span>' + (p.role ? '<em>' + esc(p.role) + '</em>' : '') + '</div></header>' +
      '<p class="s-text">' + body(p.text) + '</p>' + lk +
      '<footer>' + src + '<span class="s-sh">' +
      '<a href="https://twitter.com/intent/tweet?text=' + encodeURIComponent(t) + '&url=' + encodeURIComponent(here) + '" target="_blank" rel="noopener">Share</a>' +
      '<button type="button" class="sh" data-link="' + here + '">Copy link</button></span></footer></article>';
  }
  var lead = S.filter(function (p) { return p.joshua; })[0];
  if (lead) document.getElementById('s-lead').innerHTML = card(lead, true);
  var rest = S.filter(function (p) { return p !== lead; });
  var counts = {}; rest.forEach(function (p) { counts[p.group] = (counts[p.group] || 0) + 1; });
  var bar = document.getElementById('s-bar');
  bar.innerHTML = '<button class="chip" data-g="all" aria-pressed="true">Everyone <i>' + rest.length + '</i></button>' +
    Object.keys(G).filter(function (g) { return counts[g]; }).map(function (g) { return '<button class="chip" data-g="' + g + '" aria-pressed="false">' + G[g] + ' <i>' + counts[g] + '</i></button>'; }).join('');
  var pol = rest.filter(function (p) { return p.group === 'uk' || p.group === 'world'; }).length;
  document.getElementById('s-stats').innerHTML = '<b>' + rest.length + '</b> posts &nbsp;·&nbsp; <b>' + pol + '</b> from parliamentarians';
  function render(g) { wall.innerHTML = rest.filter(function (p) { return g === 'all' || p.group === g; }).map(function (p) { return card(p); }).join(''); }
  bar.addEventListener('click', function (e) {
    var c = e.target.closest('.chip'); if (!c) return;
    bar.querySelectorAll('.chip').forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
    render(c.getAttribute('data-g'));
  });
  render('all');
  if (location.hash) { var el = document.getElementById(location.hash.slice(1)); if (el) { el.classList.add('s-hl'); el.scrollIntoView({block: 'center'}); } }
})();
