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
