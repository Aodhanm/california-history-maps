/* California History Maps — shared map engine (v2, 2026-07-14)
   Renders a map page from a data/*.json file. See data/schema.md.
   Vanilla JS + Leaflet (pinned CDN, loaded by the shell page). */
(function () {
  'use strict';

  var MAP_ID = document.body.getAttribute('data-map');
  var DATA_URL = '../data/' + MAP_ID + '.json';
  var CLUSTER_THRESHOLD = 75;

  var state = {
    data: null, map: null, allMarkers: [],  // {feature, marker, layerId}
    layerGroups: {}, routeLines: [],
    yearMin: null, yearMax: null, query: ''
  };

  // ---------- helpers ----------
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function featureYear(f) {
    var m = /^(\d{4})/.exec(f.date && f.date.iso || '');
    return m ? +m[1] : null;
  }

  // ---------- markers ----------
  var PRECISION_LABEL = {
    exact: 'located precisely',
    place: 'place-level precision',
    area: 'approximate location within the district',
    conjectural: 'CONJECTURAL location'
  };

  function markerFor(f, color) {
    var precision = f.coord_precision || 'place';
    var opts = {
      radius: 7, weight: 2, color: color, fillColor: color, fillOpacity: 0.85
    };
    if (precision === 'area') { opts.fillOpacity = 0.45; opts.dashArray = '3 3'; }
    if (precision === 'conjectural') { opts.fillOpacity = 0; opts.dashArray = '4 3'; }
    if (f.type === 'settlement' || f.type === 'mission' || f.type === 'presidio') {
      opts.radius = 5; opts.weight = 1.5;
    }
    var m = L.circleMarker(f.coords, opts);
    m.bindPopup(popupHtml(f), { maxWidth: 380 });
    return m;
  }

  function popupHtml(f) {
    var h = '<div class="popup">';
    h += '<h3>' + esc(f.name) + '</h3>';
    var badges = [];
    if (f.register_no) badges.push('<span class="badge reg" title="Military-register number">#' + esc(f.register_no) + '</span>');
    if (f.type) badges.push('<span class="badge type">' + esc(f.type) + '</span>');
    if (f.date && f.date.display) badges.push('<span class="badge date">' + esc(f.date.display) +
      (f.date.confidence && f.date.confidence !== 'exact' ? ' <em>(' + esc(f.date.confidence) + ')</em>' : '') + '</span>');
    if (badges.length) h += '<p class="badges">' + badges.join(' ') + '</p>';
    if (f.summary) h += '<p>' + esc(f.summary) + '</p>';
    if (f.result) h += '<p class="result"><strong>' + esc(f.result) + '</strong></p>';
    if (f.quote && f.quote.es) {
      h += '<blockquote lang="es">' + esc(f.quote.es) + '</blockquote>';
      if (f.quote.en) h += '<p class="quote-en">(' + esc(f.quote.en) + ')</p>';
    }
    if (f.native_groups && f.native_groups.length)
      h += '<p class="native">Native peoples named in the sources: ' + esc(f.native_groups.join(', ')) + '</p>';
    (f.sources || []).forEach(function (s) {
      h += '<p class="source">' + esc(s.citation);
      if (s.ca_record) h += ' — <a href="https://aodhanm.github.io/archives-of-california/?record=' +
        encodeURIComponent(s.ca_record) + '" target="_blank" rel="noopener">View the record →</a>';
      else if (s.ia_leaf_url) h += ' — <a href="' + esc(s.ia_leaf_url) + '" target="_blank" rel="noopener">manuscript leaf →</a>';
      h += '</p>';
    });
    var pl = PRECISION_LABEL[f.coord_precision || 'place'];
    if (f.coord_precision && f.coord_precision !== 'exact')
      h += '<p class="precision">📍 ' + esc(pl) + '</p>';
    if (f.notes) h += '<p class="notes">' + esc(f.notes) + '</p>';
    h += '<p class="permalink"><a href="#' + encodeURIComponent(f.id) + '" onclick="navigator.clipboard&&navigator.clipboard.writeText(location.href.split(\'#\')[0]+\'#' + esc(f.id) + '\');return false;" title="Copy permalink">🔗 permalink</a></p>';
    return h + '</div>';
  }

  // ---------- filtering ----------
  function applyFilters() {
    var q = state.query.toLowerCase();
    var shown = 0;
    state.allMarkers.forEach(function (rec) {
      var f = rec.feature;
      var y = featureYear(f);
      var okYear = y == null || (y >= state.yearMin && y <= state.yearMax);
      var hay = (f.name + ' ' + (f.summary || '') + ' ' + (f.tags || []).join(' ') + ' ' +
                 (f.native_groups || []).join(' ')).toLowerCase();
      var okQuery = !q || hay.indexOf(q) !== -1;
      var group = state.layerGroups[rec.layerId];
      var on = okYear && okQuery;
      if (group) {
        if (on && !group.hasLayer(rec.marker)) group.addLayer(rec.marker);
        if (!on && group.hasLayer(rec.marker)) group.removeLayer(rec.marker);
      }
      if (on) shown++;
    });
    var c = document.getElementById('feature-count');
    if (c) c.textContent = shown + ' of ' + state.allMarkers.length + ' features shown';
  }

  // ---------- controls ----------
  function buildControls(data) {
    var bar = document.getElementById('controls');
    if (!bar) return;

    // search
    var search = el('input', 'search');
    search.type = 'search';
    search.placeholder = 'Search names, summaries, peoples…';
    search.setAttribute('aria-label', 'Search features');
    search.addEventListener('input', function () { state.query = this.value; applyFilters(); });
    bar.appendChild(search);

    // timeline slider (dual range via two inputs)
    var years = state.allMarkers.map(function (r) { return featureYear(r.feature); })
      .filter(function (y) { return y != null; });
    var lo = data.date_range ? data.date_range[0] : Math.min.apply(null, years);
    var hi = data.date_range ? data.date_range[1] : Math.max.apply(null, years);
    state.yearMin = lo; state.yearMax = hi;
    var wrap = el('div', 'timeline');
    var lbl = el('span', 'timeline-label', lo + '–' + hi);
    function slider(val) {
      var s = el('input');
      s.type = 'range'; s.min = lo; s.max = hi; s.value = val;
      s.setAttribute('aria-label', 'Year filter');
      return s;
    }
    var s1 = slider(lo), s2 = slider(hi);
    function upd() {
      state.yearMin = Math.min(+s1.value, +s2.value);
      state.yearMax = Math.max(+s1.value, +s2.value);
      lbl.textContent = state.yearMin + '–' + state.yearMax;
      applyFilters();
    }
    s1.addEventListener('input', upd); s2.addEventListener('input', upd);
    wrap.appendChild(s1); wrap.appendChild(s2); wrap.appendChild(lbl);
    bar.appendChild(wrap);

    // count + cite
    bar.appendChild(el('span', 'count', '<span id="feature-count"></span>'));
    var cite = el('button', 'cite-btn', 'Cite this map');
    cite.addEventListener('click', function () { showCite(data); });
    bar.appendChild(cite);
  }

  function showCite(data) {
    var today = new Date().toISOString().slice(0, 10);
    var url = location.href.split('#')[0];
    var txt = 'Coyne, Aodhan. “' + data.title + '.” California History Maps. ' +
      'Interactive map. Last updated ' + (data.last_updated || today) + '. ' + url +
      ' (accessed ' + today + ').';
    var box = document.getElementById('cite-box');
    if (!box) {
      box = el('div', 'cite-box'); box.id = 'cite-box';
      document.body.appendChild(box);
    }
    box.innerHTML = '<p>' + esc(txt) + '</p><button onclick="navigator.clipboard&&navigator.clipboard.writeText(' +
      JSON.stringify(JSON.stringify(txt)) + ');this.textContent=\'Copied\'">Copy</button>' +
      '<button onclick="this.parentNode.style.display=\'none\'">Close</button>';
    box.style.display = 'block';
  }

  // ---------- init ----------
  function init(data) {
    state.data = data;
    document.title = data.title + ' · California History Maps';
    var h = document.getElementById('map-title');
    if (h) h.textContent = data.title;
    var sub = document.getElementById('map-subtitle');
    if (sub) sub.textContent = data.subtitle || '';
    var ab = document.getElementById('map-abstract');
    if (ab && data.abstract) ab.textContent = data.abstract;

    var map = L.map('map', { center: data.center || [36.5, -120.5], zoom: data.zoom || 6 });
    state.map = map;
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png', {
      maxZoom: 17,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    }).addTo(map);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}{r}.png',
      { maxZoom: 17, pane: 'shadowPane' }).addTo(map);

    var layerColors = {};
    var overlays = {};
    var useCluster = (data.features || []).length > CLUSTER_THRESHOLD && window.L.markerClusterGroup;
    (data.layers || []).forEach(function (ly) {
      layerColors[ly.id] = ly.color;
      var g = useCluster
        ? L.markerClusterGroup({ maxClusterRadius: 36, disableClusteringAtZoom: 9 })
        : L.layerGroup();
      state.layerGroups[ly.id] = g;
      g.addTo(map);
      overlays['<span class="swatch" style="background:' + ly.color + '"></span> ' + esc(ly.label)] = g;
    });

    (data.features || []).forEach(function (f) {
      var color = layerColors[f.layer] || '#555';
      var m = markerFor(f, color);
      state.allMarkers.push({ feature: f, marker: m, layerId: f.layer });
      var g = state.layerGroups[f.layer];
      if (g) g.addLayer(m);
    });

    (data.routes || []).forEach(function (r) {
      var coords = (r.stops || []).map(function (s) { return s.coords; });
      var line = L.polyline(coords, {
        color: r.color || '#444', weight: 3, opacity: 0.8,
        dashArray: (r.path_confidence && r.path_confidence !== 'documented') ? '8 6' : (r.dash || null)
      });
      var g = state.layerGroups[r.layer];
      (g || map).addLayer ? (g ? g.addLayer(line) : line.addTo(map)) : line.addTo(map);
      state.routeLines.push(line);
      (r.stops || []).forEach(function (s) {
        var m = markerFor(s, r.color || '#444');
        state.allMarkers.push({ feature: s, marker: m, layerId: r.layer });
        if (g) g.addLayer(m); else m.addTo(map);
      });
    });

    L.control.layers(null, overlays, { collapsed: window.innerWidth < 700 }).addTo(map);
    buildControls(data);
    applyFilters();

    // permalink: #feature-id opens + pans
    function openHash() {
      var id = decodeURIComponent(location.hash.slice(1));
      if (!id) return;
      state.allMarkers.some(function (rec) {
        if (rec.feature.id === id) {
          map.setView(rec.feature.coords, Math.max(map.getZoom(), 10));
          var g = state.layerGroups[rec.layerId];
          if (g && g.zoomToShowLayer && g.hasLayer(rec.marker)) {
            // marker may be inside a cluster — expand it first
            g.zoomToShowLayer(rec.marker, function () { rec.marker.openPopup(); });
          } else {
            rec.marker.openPopup();
          }
          return true;
        }
      });
    }
    window.addEventListener('hashchange', openHash);
    openHash();
  }

  fetch(DATA_URL).then(function (r) {
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }).then(init).catch(function (e) {
    document.getElementById('map').innerHTML =
      '<p class="load-error">Could not load map data (' + esc(e.message) + ').</p>';
  });
})();
