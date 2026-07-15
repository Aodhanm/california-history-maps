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
  var query = '';
  var sortMode = 'theme';   // theme | year

  function itemYear(it) {
    var m = /(1[5-9]\d\d)/.exec(it.year || '');
    return m ? +m[1] : null;
  }
  function passes(it) {
    if (query) {
      var hay = (it.title + ' ' + (it.maker || '') + ' ' + it.year + ' ' + it.caption).toLowerCase();
      if (hay.indexOf(query) === -1) return false;
    }
    return true;
  }
  function makeCard(it) {
    var card = document.createElement('a');
    card.className = 'card';
    card.href = '#' + encodeURIComponent(it.id);
    card.addEventListener('click', function (e) { e.preventDefault(); openViewer(it); });
    card.innerHTML =
      '<div class="thumb" style="background-image:url(thumb/' + esc(it.file) + ')"></div>' +
      '<div class="body"><h3>' + esc(it.title) + '</h3>' +
      '<p class="meta">' + esc((it.maker ? it.maker + ' · ' : '') + it.year) + '</p></div>';
    return card;
  }

  function render() {
    var root = document.getElementById('gallery-root');
    root.innerHTML = '';
    var shown = 0;
    if (sortMode === 'year') {
      var items = data.items.filter(function (it) {
        return (activeGroup === 'all' || it.group === activeGroup) && passes(it);
      }).sort(function (a, b) { return (itemYear(a) || 9999) - (itemYear(b) || 9999); });
      var sec = document.createElement('section');
      sec.innerHTML = '<h2>Chronological <span class="gcount">' + items.length + '</span></h2>';
      var grid = document.createElement('div');
      grid.className = 'card-grid gallery-grid';
      items.forEach(function (it) { grid.appendChild(makeCard(it)); });
      sec.appendChild(grid);
      root.appendChild(sec);
      shown = items.length;
    } else {
      data.groups.forEach(function (g) {
        if (activeGroup !== 'all' && activeGroup !== g.id) return;
        var items = data.items.filter(function (it) { return it.group === g.id && passes(it); });
        if (!items.length) return;
        var sec = document.createElement('section');
        sec.innerHTML = '<h2>' + esc(g.label) + ' <span class="gcount">' + items.length + '</span></h2>' +
          '<p class="prose gintro">' + esc(g.intro) + '</p>';
        var grid = document.createElement('div');
        grid.className = 'card-grid gallery-grid';
        items.forEach(function (it) { grid.appendChild(makeCard(it)); });
        sec.appendChild(grid);
        root.appendChild(sec);
        shown += items.length;
      });
    }
    if (!shown) root.innerHTML = '<p class="prose">Nothing matches. Clear the search.</p>';
  }

  function buildTools() {
    var bar = document.getElementById('tools');
    if (!bar) return;
    var search = document.createElement('input');
    search.type = 'search';
    search.className = 'gsearch';
    search.placeholder = 'Search titles, makers, captions…';
    search.setAttribute('aria-label', 'Search the gallery');
    search.addEventListener('input', function () { query = this.value.toLowerCase(); render(); });
    bar.appendChild(search);
    var sortBtn = document.createElement('button');
    sortBtn.className = 'chip';
    sortBtn.textContent = 'Sort: by theme';
    sortBtn.addEventListener('click', function () {
      sortMode = sortMode === 'theme' ? 'year' : 'theme';
      sortBtn.textContent = sortMode === 'theme' ? 'Sort: by theme' : 'Sort: chronological';
      render();
    });
    bar.appendChild(sortBtn);

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
    buildTools();
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
