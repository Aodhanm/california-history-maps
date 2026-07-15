/* Historical map gallery: grouped grid + OpenSeadragon overlay viewer. */
(function () {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  var data = null;
  var activeGroup = 'all';

  function render() {
    var root = document.getElementById('gallery-root');
    root.innerHTML = '';
    data.groups.forEach(function (g) {
      if (activeGroup !== 'all' && activeGroup !== g.id) return;
      var items = data.items.filter(function (it) { return it.group === g.id; });
      if (!items.length) return;
      var sec = document.createElement('section');
      sec.innerHTML = '<h2>' + esc(g.label) + ' <span class="gcount">' + items.length + '</span></h2>' +
        '<p class="prose gintro">' + esc(g.intro) + '</p>';
      var grid = document.createElement('div');
      grid.className = 'card-grid gallery-grid';
      items.forEach(function (it) {
        var card = document.createElement('a');
        card.className = 'card';
        card.href = '#' + encodeURIComponent(it.id);
        card.addEventListener('click', function (e) { e.preventDefault(); openViewer(it); });
        card.innerHTML =
          '<div class="thumb" style="background-image:url(thumb/' + esc(it.file) + ')"></div>' +
          '<div class="body"><h3>' + esc(it.title) + '</h3>' +
          '<p class="meta">' + esc((it.maker ? it.maker + ' · ' : '') + it.year) + '</p></div>';
        grid.appendChild(card);
      });
      sec.appendChild(grid);
      root.appendChild(sec);
    });
  }

  function buildChips() {
    var bar = document.getElementById('chips');
    var chips = [{ id: 'all', label: 'All (' + data.items.length + ')' }].concat(data.groups);
    chips.forEach(function (g) {
      var b = document.createElement('button');
      b.className = 'chip' + (g.id === activeGroup ? ' active' : '');
      b.textContent = g.label;
      b.addEventListener('click', function () {
        activeGroup = g.id;
        Array.prototype.forEach.call(bar.children, function (c) { c.classList.remove('active'); });
        b.classList.add('active');
        render();
      });
      bar.appendChild(b);
    });
  }

  var viewer = null;
  function openViewer(it) {
    history.replaceState(null, '', '#' + encodeURIComponent(it.id));
    var ov = document.getElementById('viewer-overlay');
    ov.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    document.getElementById('viewer-title').textContent = it.title;
    document.getElementById('viewer-meta').innerHTML =
      esc((it.maker ? it.maker + ' · ' : '') + it.year) +
      ' · <a href="' + esc(it.source_url) + '" target="_blank" rel="noopener">archival original →</a>';
    document.getElementById('viewer-caption').textContent = it.caption;
    document.getElementById('viewer-credit').textContent = it.credit;
    if (viewer) { viewer.destroy(); viewer = null; }
    viewer = OpenSeadragon({
      id: 'seadragon',
      prefixUrl: 'https://cdn.jsdelivr.net/npm/openseadragon@4.1.1/build/openseadragon/images/',
      tileSources: { type: 'image', url: 'img/' + it.file },
      maxZoomPixelRatio: 2.5,
      showNavigator: true,
      crossOriginPolicy: 'Anonymous'
    });
  }
  function closeViewer() {
    document.getElementById('viewer-overlay').style.display = 'none';
    document.body.style.overflow = '';
    history.replaceState(null, '', location.pathname);
    if (viewer) { viewer.destroy(); viewer = null; }
  }
  document.getElementById('viewer-close').addEventListener('click', closeViewer);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeViewer(); });

  fetch('gallery-data.json').then(function (r) { return r.json(); }).then(function (d) {
    data = d;
    document.getElementById('gallery-note').textContent = d.note;
    buildChips();
    render();
    var id = decodeURIComponent(location.hash.slice(1));
    if (id) {
      var it = d.items.filter(function (x) { return x.id === id; })[0];
      if (it) openViewer(it);
    }
    // wanted list
    var w = document.getElementById('wanted-list');
    d.wanted.forEach(function (t) {
      var li = document.createElement('li');
      li.textContent = t;
      w.appendChild(li);
    });
  });
})();
