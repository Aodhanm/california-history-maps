/* Panels engine — the Mission Dolores exhibit-series maps (4 standalone pages).
 * Shared by maps/sf-bay-expeditions.html, missionization.html, ranchos-by-era.html,
 * languages.html. Additive to the site: no existing map, page, or data file is
 * touched; enhanced datasets ship under new filenames.
 * Four-era series after the Mission Dolores exhibit panels, over the SFEI
 * ca.-1800 baylands. Pictorial silhouette icons follow the accepted
 * map-symbol-demo manner: filled shapes, white halo, NO enclosing chips.
 * Popup + C-A deep-link logic ported from map-engine.js v6; live site untouched. */
(function () {
  'use strict';

  // ---------- palette ----------
  var SPANISH_BROWN = '#5a3317';
  var RUSSIAN_PURPLE = '#6d3fa0';
  var BAYLANDS_FILL = {
    'Tidal / Salt Marsh':      '#cfe3a8',
    'Tidal Flat':              '#ded3b2',
    'Marsh Panne / Salt Flat': '#e9e2c8',
    'Beach':                   '#eadfba',
    'Dune':                    '#e6d8a8',
    'Lagoon':                  '#b9d2e2',
    'Shallow Water':           '#a9c8dc',
    'Deep Water':              '#8fb3cd',
    'Grassland / Savanna':     '#dde6c4'
  };

  // ---------- pictorial glyphs (24x24 silhouettes, halo drawn by double pass) ----------
  var GLYPHS = {
    // mission after Carmel: wide low nave, curved central pediment with the round
    // window, domed bell tower left, smaller tower right; cut-outs fill="#fff", last
    mission:
      '<path d="M1.6 21v-8.2h20.8V21z"/>' +
      '<path d="M8.6 12.8c0-2.3 1.3-3.8 3.4-3.8s3.4 1.5 3.4 3.8z"/>' +
      '<path d="M2.8 12.8V7.4h5.4v5.4z"/>' +
      '<path d="M3.3 7.4c0-2.1 1-3.4 2.2-3.4s2.2 1.3 2.2 3.4z"/>' +
      '<path d="M5.15 1h.7v1h.95v.7h-.95v1.4h-.7V2.7H4.2V2h.95z"/>' +
      '<path d="M16 12.8V9.2h4.4v3.6z"/>' +
      '<path d="M16.5 9.2c0-1.7.75-2.7 1.7-2.7s1.7 1 1.7 2.7z"/>' +
      '<path fill="#fff" d="M10.65 21v-3.8c0-.9.55-1.5 1.35-1.5s1.35.6 1.35 1.5V21z"/>' +
      '<circle fill="#fff" cx="12" cy="11.7" r=".9"/>' +
      '<path fill="#fff" d="M4.65 11.5V9.8c0-.7.4-1.2.85-1.2s.85.5.85 1.2v1.7z"/>' +
      '<circle fill="#fff" cx="18.2" cy="11.1" r=".7"/>' +
      '<rect fill="#fff" x="13.2" y="16.4" width="1.7" height="1.9"/><rect fill="#fff" x="17.3" y="16.4" width="1.7" height="1.9"/>',
    // asistencia: small chapel with one bell and door
    asistencia:
      '<path fill-rule="evenodd" d="M5 21v-8.4h14V21zM8.6 12.6V8.8h6.8v3.8zM11.2 15.4h1.6v3.2h-1.6zM11.2 9.8h1.6v1.8h-1.6z"/>' +
      '<path d="M11.5 4.4h1v1.1h1.1v1h-1.1v1.7h-1V6.5h-1.1v-1h1.1z"/>',
    // outstation / rancho house: low casa with long roof
    house:
      '<path d="M2.6 12.8 12 6.4l9.4 6.4-1.3 1.9L12 9.1l-8.1 5.6z"/>' +
      '<path fill-rule="evenodd" d="M5 14.2 12 9.4l7 4.8V21H5zM10.9 15.4h2.2V21h-2.2z"/>',
    // pueblo: a couple of adobe houses, low roofs, door and window cut out
    pueblo:
      '<path d="M2.2 20.8v-7.6l4.9-3.2 4.9 3.2v7.6z"/>' +
      '<path d="M12.6 20.8v-6.1l4.1-2.7 4.1 2.7v6.1z"/>' +
      '<path fill="#fff" d="M5.8 20.8v-3.9c0-.8.55-1.3 1.3-1.3s1.3.5 1.3 1.3v3.9z"/>' +
      '<rect fill="#fff" x="15.6" y="16" width="2.2" height="2.2"/>',
    // Sutter's Fort: quadrangle with its two diamond corner bastions (as built)
    sutterfort:
      '<path fill-rule="evenodd" d="M4.4 4.4h15.2v15.2H4.4zm3 3v9.2h9.2V7.4z"/>' +
      '<path d="M4.6.8 8.4 4.6 4.6 8.4.8 4.6z"/>' +
      '<path d="M19.4 15.6l3.8 3.8-3.8 3.8-3.8-3.8z"/>',
    // muzzle-loading smoothbore on a wheeled carriage (accepted glyph sheet):
    // the battery symbol, as on the San Francisco defense map
    cannon:
      '<path d="M3.4 5.6 18 7.6v4L3.4 13.6z"/>' +
      '<path d="M17.6 6.9h2.8v5.4h-2.8z"/>' +
      '<circle cx="2.6" cy="9.6" r="1.9"/>' +
      '<path d="M5 12.4 .6 21.2h3.1L8.4 13.6z"/>' +
      '<circle cx="9.4" cy="16.4" r="4.3"/>',
    // four-bastioned fort, plan (glyph sheet)
    fort:
      '<path d="M19.9 4.1 16.2 12l3.7 7.9L12 16.2l-7.9 3.7L7.8 12 4.1 4.1 12 7.8z"/>',
    // deepwater port (glyph sheet anchor)
    anchor:
      '<path d="M12 .8a3 3 0 00-1.3 5.7v1.8H7.4v2.8h3.3v9.4c-3.2-.6-5.6-2.9-6-5.9l-2.6.7C2.9 19.9 7 23.2 12 23.2s9.1-3.3 9.9-8.3l-2.6-.7c-.4 3-2.8 5.3-6 5.9v-9.4h3.3V8.3h-3.3V6.5A3 3 0 0012 .8zm0 2.3a1 1 0 110 2 1 1 0 010-2z" fill-rule="evenodd"/>',
    // Russian-American Company: imperial double-headed eagle, heraldic display —
    // two outward heads under one crown, wings of stepped feathers raised, fanned tail
    eagle:
      /* raised left wing, three feather steps */
      '<path d="M10.9 10.2C9.3 6.9 6.5 5.2 2.3 5c.5 1.3 1.2 2.4 2.2 3.2-1.3.1-2.5.5-3.7 1.2 1 1.1 2.2 1.9 3.6 2.3-1 .6-1.8 1.4-2.4 2.5 1.4.4 2.8.5 4.2.1-.6 1-.9 2-.9 3.2 2.3-.6 4-1.9 5-4z"/>' +
      /* raised right wing, mirrored */
      '<path d="M13.1 10.2c1.6-3.3 4.4-5 8.6-5.2-.5 1.3-1.2 2.4-2.2 3.2 1.3.1 2.5.5 3.7 1.2-1 1.1-2.2 1.9-3.6 2.3 1 .6 1.8 1.4 2.4 2.5-1.4.4-2.8.5-4.2.1.6 1 .9 2 .9 3.2-2.3-.6-4-1.9-5-4z"/>' +
      /* body */
      '<path d="M10.6 8.8h2.8l1 6.3-2.4 2.1-2.4-2.1z"/>' +
      /* fanned tail with notches */
      '<path d="M12 15.9l3.4 2.2 1.2 3-2.4-.8-.9 1.6-1.3-1.2-1.3 1.2-.9-1.6-2.4.8 1.2-3z"/>' +
      /* left neck + head, beak hooked outward */
      '<path d="M11.5 9c.1-2.3-.6-3.9-2.2-4.9.9-.1 1.7 0 2.4.4-.3-.9-.2-1.7.2-2.5-1.6-.2-2.9.2-3.9 1.2l-2.1-.4 1.3 1.4c-.3 1.9.5 3.4 2.4 4.6z" transform="translate(-1.2 0)"/>' +
      /* right neck + head, mirrored */
      '<path d="M12.5 9c-.1-2.3.6-3.9 2.2-4.9-.9-.1-1.7 0-2.4.4.3-.9.2-1.7-.2-2.5 1.6-.2 2.9.2 3.9 1.2l2.1-.4-1.3 1.4c.3 1.9-.5 3.4-2.4 4.6z" transform="translate(1.2 0)"/>' +
      /* single crown above, between the heads */
      '<path d="M9.9 1.9l1-1.3.6 1 .5-1 .6 1 1-1.3.6 2.1H10z"/>' +
      '<rect x="9.9" y="2.7" width="4.2" height=".8"/>',
    // parish / presidio chapel (secular church): nave with a square bell TOWER —
    // distinct from the mission's espadaña bell-wall
    parish:
      '<path d="M1.8 21v-7.6h13.4V21z"/>' +
      '<path d="M1 13.6l7.5-4.4 7.5 4.4-.9 1.5-6.6-3.9-6.6 3.9z"/>' +
      '<path d="M15.8 21V8.2h6V21z"/>' +
      '<path d="M15.2 8.6l3.6-3 3.6 3z"/>' +
      '<path fill="#fff" d="M17.6 10.4h2.4v3h-2.4zM6.4 16h3v5h-3z"/>' +
      '<path d="M18.1 2h1.4v2.6h-1.4z"/><path d="M17.2 2.9h3.2v1h-3.2z"/>',

    // Colony Ross: the company eagle knocked out of the four-bastioned fort plan
    ross:
      '<path d="M22.6 1.4 17.6 12l5 10.6L12 17.6 1.4 22.6l5-10.6-5-10.6L12 6.4z"/>' +
      '<g fill="#fff" transform="translate(12 13.1) scale(0.52) translate(-12 -12)">' +
      /* raised left wing, three feather steps */
      '<path d="M10.9 10.2C9.3 6.9 6.5 5.2 2.3 5c.5 1.3 1.2 2.4 2.2 3.2-1.3.1-2.5.5-3.7 1.2 1 1.1 2.2 1.9 3.6 2.3-1 .6-1.8 1.4-2.4 2.5 1.4.4 2.8.5 4.2.1-.6 1-.9 2-.9 3.2 2.3-.6 4-1.9 5-4z"/>' +
      /* raised right wing, mirrored */
      '<path d="M13.1 10.2c1.6-3.3 4.4-5 8.6-5.2-.5 1.3-1.2 2.4-2.2 3.2 1.3.1 2.5.5 3.7 1.2-1 1.1-2.2 1.9-3.6 2.3 1 .6 1.8 1.4 2.4 2.5-1.4.4-2.8.5-4.2.1.6 1 .9 2 .9 3.2-2.3-.6-4-1.9-5-4z"/>' +
      /* body */
      '<path d="M10.6 8.8h2.8l1 6.3-2.4 2.1-2.4-2.1z"/>' +
      /* fanned tail with notches */
      '<path d="M12 15.9l3.4 2.2 1.2 3-2.4-.8-.9 1.6-1.3-1.2-1.3 1.2-.9-1.6-2.4.8 1.2-3z"/>' +
      /* left neck + head, beak hooked outward */
      '<path d="M11.5 9c.1-2.3-.6-3.9-2.2-4.9.9-.1 1.7 0 2.4.4-.3-.9-.2-1.7.2-2.5-1.6-.2-2.9.2-3.9 1.2l-2.1-.4 1.3 1.4c-.3 1.9.5 3.4 2.4 4.6z" transform="translate(-1.2 0)"/>' +
      /* right neck + head, mirrored */
      '<path d="M12.5 9c-.1-2.3.6-3.9 2.2-4.9-.9-.1-1.7 0-2.4.4.3-.9.2-1.7-.2-2.5 1.6-.2 2.9.2 3.9 1.2l2.1-.4-1.3 1.4c.3 1.9-.5 3.4-2.4 4.6z" transform="translate(1.2 0)"/>' +
      /* single crown above, between the heads */
      '<path d="M9.9 1.9l1-1.3.6 1 .5-1 .6 1 1-1.3.6 2.1H10z"/>' +
      '<rect x="9.9" y="2.7" width="4.2" height=".8"/>' +
      '</g>',

    // rancheria — a Native polity or village: domed tule houses
    rancheria:
      '<path d="M3.4 18.6c0-4.6 3-7.8 6.8-7.8s6.8 3.2 6.8 7.8v1.8H3.4z"/>' +
      '<path d="M15.4 20.4v-1.2c0-3.2 2-5.4 4.6-5.4 1.4 0 2.6.6 3.4 1.7-.5 1.9-.7 3.3-.7 4.9z" transform="translate(-1.4 0)"/>' +
      '<path fill="#fff" d="M8.6 20.4v-3.4c0-1.1.7-1.8 1.6-1.8s1.6.7 1.6 1.8v3.4z"/>',

    // longhorn, for hacienda/rancho headquarters when pointed
    longhorn:
      '<path d="M9.7 12.2c0-2.1 1-3.6 2.3-3.6s2.3 1.5 2.3 3.6c0 2.7-1 5.2-2.3 5.2s-2.3-2.5-2.3-5.2z"/>' +
      '<path d="M10.9 9.4C8 8.9 5.3 7.4 4 4.9c2.7-.2 5.5.7 7.5 2.4z"/>' +
      '<path d="M13.1 9.4c2.9-.5 5.6-2 6.9-4.5-2.7-.2-5.5.7-7.5 2.4z"/>'
  };

  function glyphIcon(key, color, size) {
    var paths = GLYPHS[key];
    if (!paths) return null;
    size = size || 24;
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 28 28" width="' + size + '" height="' + size + '">' +
      '<g fill="#fff" stroke="#fff" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round">' + paths + '</g>' +
      '<g fill="' + color + '">' + paths + '</g></svg>';
    return L.divIcon({ className: 'glyph-marker', html: svg, iconSize: [size, size], iconAnchor: [size / 2, size / 2], popupAnchor: [0, -size / 2] });
  }
  // glyph choice per feature, data-gated with sensible defaults
  function glyphFor(f) {
    if (f.symbol) return f.symbol;
    if (f.type === 'battery') return 'cannon';
    if (f.layer === 'russian') {
      // the company's seats fly the eagle; its farm outstations take the
      // same house symbol as the Spanish outstations (Aodhan's ruling)
      return /ranch/i.test(f.name || '') ? 'house' : 'eagle';
    }
    if (f.layer === 'sutter') return 'sutterfort';
    if (f.layer === 'asistencias') return 'asistencia';
    if (f.layer === 'outstations') return 'house';
    if (f.type === 'mission') return 'mission';
    if (f.type === 'parish') return 'parish';
    if (f.type === 'presidio') return 'fort';
    if (f.type === 'pueblo') return 'pueblo';
    return null;
  }
  function glyphColor(f, fallback) {
    if (f.layer === 'russian') return RUSSIAN_PURPLE;
    if (f.layer === 'sutter') return '#4a4a4a';
    if (f.type === 'battery') return '#8a1f1f';
    if (f.type === 'mission' || f.type === 'presidio' || f.type === 'pueblo' || f.type === 'parish' ||
        f.layer === 'asistencias' || f.layer === 'outstations') return SPANISH_BROWN;
    return fallback || SPANISH_BROWN;
  }

  // ---------- C-A deep links (ported verbatim from map-engine.js) ----------
  var CA_BASE = 'https://archivesofcalifornia.com/#';
  function caUrl(rec) { return CA_BASE + encodeURIComponent(rec); }
  function citeToRecord(text, defaultVol) {
    if (!text) return null;
    var m = /C-A\s*(\d{1,2})\D{0,14}?Docs?\.?\s*(\d{1,4})/i.exec(text);
    if (m) return 'ca' + m[1] + '-d' + m[2];
    if (defaultVol) {
      var b = /^\s*Docs?\.?\s*(\d{1,4})/i.exec(text);
      if (b) return 'ca' + defaultVol + '-d' + b[1];
    }
    return null;
  }
  function recordLink(rec, label) {
    var m = /^ca(\d+)-d(\w+)$/.exec(rec || '');
    var txt = label || (m ? 'C-A ' + m[1] + ' · doc ' + m[2] : 'View the record');
    return ' <a class="ca-link" href="' + caUrl(rec) + '" target="_blank" rel="noopener">' + txt + ' →</a>';
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  var PRECISION_LABEL = {
    exact: 'located exactly', place: 'placed at a known settlement or feature',
    area: 'right district, spot approximated', conjectural: 'conjectural placement'
  };

  function buildPopup(f) {
    var h = '<div class="popup"><h3>' + esc(f.name) + '</h3>';
    var badges = [];
    if (f.type) badges.push('<span class="badge type">' + esc(f.type) + '</span>');
    if (f.date && f.date.display) badges.push('<span class="badge date">' + esc(f.date.display) +
      (f.date.confidence && f.date.confidence !== 'exact' ? ' <em>(' + esc(f.date.confidence) + ')</em>' : '') + '</span>');
    if (badges.length) h += '<p class="badges">' + badges.join(' ') + '</p>';
    if (f.summary) h += '<p>' + esc(f.summary) + '</p>';
    if (f.facts && f.facts.length) {
      h += '<table class="facts"><tbody>';
      f.facts.forEach(function (row) { h += '<tr><th>' + esc(row[0]) + '</th><td>' + esc(row[1]) + '</td></tr>'; });
      h += '</tbody></table>';
    }
    if (f.quotes && f.quotes.length) f.quotes.forEach(function (q) {
      h += '<blockquote class="src-quote">' + esc(q.text) + (q.cite ? '<cite> — ' + esc(q.cite) + '</cite>' : '') + '</blockquote>';
    });
    if (f.result) h += '<p class="result"><strong>' + esc(f.result) + '</strong></p>';
    if (f.quote && f.quote.es) {
      h += '<blockquote lang="es">' + esc(f.quote.es) + '</blockquote>';
      if (f.quote.en) h += '<p class="quote-en">(' + esc(f.quote.en) + ')</p>';
    }
    if (f.native_groups && f.native_groups.length)
      h += '<p class="native">Native peoples named in the sources: ' + esc(f.native_groups.join(', ')) + '</p>';
    (f.sources || []).forEach(function (s) {
      h += '<p class="source">' + esc(s.citation);
      var rec = s.ca_record || citeToRecord(s.citation, f.ca_volume);
      if (rec) h += ' —' + recordLink(rec);
      if (s.ia_leaf_url) h += ' — <a href="' + esc(s.ia_leaf_url) + '" target="_blank" rel="noopener">the manuscript leaf →</a>';
      if (s.url && !rec) h += ' — <a href="' + esc(s.url) + '" target="_blank" rel="noopener">source →</a>';
      h += '</p>';
    });
    if (f.coord_precision && f.coord_precision !== 'exact')
      h += '<p class="precision">📍 ' + esc(PRECISION_LABEL[f.coord_precision] || f.coord_precision) + '</p>';
    if (f.notes) h += '<p class="notes">' + esc(f.notes) + '</p>';
    return h + '</div>';
  }

  // ---------- page configs (one map per page, chosen by <body data-panel>) ----------
  var PAGES = {
    expeditions: {
      id: 'expeditions',
      note: 'The 1542-1776 approaches, after the Mission Dolores exhibit panel: five sea expeditions as coastal ribbons running on to where they came from and went, Ayala\u2019s longboat surveys inside the bay, the seven land expeditions of 1769-1776, and Moraga\u2019s 1806 Central Valley expedition. Every course is generalized and INTERPRETIVE; diary citations and C-A record anchors sit on the routes and key stops (C-A anchors are catalog-matched, leaf review pending).',
      phase2: '',
      files: [
        { f: '../data/sf-bay-expeditions.json' },
        { f: '../data/missionization-establishments.json', only: ['missions'] },
        { f: '../data/zalvidea-moraga-1806.json', only: ['moraga-north', 'moraga-south'] },
        { f: '../data/moraga-expeditions.json', off: true }
      ]
    },
    missionization: {
      id: 'missionization',
      note: 'Missions, asistencias, outstations, the pueblos, the presidios, the Spanish batteries, the crown stock ranches, and the Russian posts, in pictorial symbols. Founding orders from the C-A catalog sit on the establishments (catalog-matched, leaf review pending, except where leaf-read).',
      phase2: '',
      files: [
        { f: '../data/missionization-establishments.json' },
        { f: '../data/missionization-extras.json' }
      ]
    },
    ranchos: {
      id: 'ranchos', colorModes: true,
      note: 'The rancho portal\u2019s own boundaries (ECAI/UCSD geometry), colour by era (Spanish blue, Mexican red) or by granting governor. Every parcel links to its portal record and land case. The portal itself is unchanged.',
      phase2: '',
      files: [
        { f: '../data/ranchos-by-era.json' },
        { f: '../data/secularization-missions.json', off: true }
      ],
      spotlight: { label: 'Spotlight: Suscol', feature: 'rancho-suscol' }
    },
    languages: {
      id: 'languages',
      note: 'Language families and archive-named rancher\u00edas over the pre-1850 shoreline, as the Native California map documents them.',
      phase2: '',
      files: [{ f: '../data/native-california.json' }]
    }
  };

  // ---------- map ----------
  var map = L.map('map', { center: [37.45, -122.1], zoom: 9, zoomSnap: 0.5 });
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles © Esri — USGS, NOAA', maxZoom: 13
  }).addTo(map);
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}', {
    attribution: '', maxZoom: 13, opacity: 0.35
  }).addTo(map);
  map.createPane('baylands'); map.getPane('baylands').style.zIndex = 350;
  map.createPane('quilt');    map.getPane('quilt').style.zIndex = 390;
  map.createPane('casing');   map.getPane('casing').style.zIndex = 430;
  map.createPane('routes');   map.getPane('routes').style.zIndex = 440;

  // ---------- baylands base (fetched at runtime from the public CDFW BIOS
  // service, SFEI historical ecology ds3201 — not redistributed by this site) ----------
  var BAYLANDS_URL = 'https://services2.arcgis.com/Uq9r85Potqm3MfRV/arcgis/rest/services/biosds3201_fpu/FeatureServer/0/query' +
    '?where=' + encodeURIComponent("HEProject='Historical Baylands'") +
    '&outFields=LegLabel,ClickLabel,RGB&outSR=4326&geometryPrecision=5&maxAllowableOffset=0.0003&f=geojson&resultRecordCount=2000';
  var baylandsLayer = null, baylandsOpacity = 0.8;
  function bayStyle(ft) {
    var fill = BAYLANDS_FILL[ft.properties.LegLabel] || '#c9d8c2';
    return { stroke: false, fillColor: fill, fillOpacity: baylandsOpacity };
  }
  fetch(BAYLANDS_URL).then(function (r) { return r.json(); }).then(function (gj) {
    baylandsLayer = L.geoJSON(gj, {
      pane: 'baylands', style: bayStyle, interactive: false
    }).addTo(map);
  });
  document.getElementById('baylands-toggle').addEventListener('change', function (e) {
    if (!baylandsLayer) return;
    if (e.target.checked) baylandsLayer.addTo(map); else map.removeLayer(baylandsLayer);
  });
  document.getElementById('baylands-opacity').addEventListener('input', function (e) {
    baylandsOpacity = e.target.value / 100;
    if (baylandsLayer) baylandsLayer.setStyle(bayStyle);
  });

  // ---------- era rendering ----------
  var eraGroup = L.layerGroup().addTo(map);
  var dataCache = {}, layerGroups = {}, featureIndex = {};

  var DATA_V = '5'; // bump on every data edit — rsync'd mtimes make Chrome's heuristic cache serve stale JSON
  function loadJSON(url) {
    if (dataCache[url]) return Promise.resolve(dataCache[url]);
    return fetch(url + (url.indexOf('?') >= 0 ? '&' : '?') + 'v=' + DATA_V).then(function (r) {
      if (!r.ok) throw new Error(url + ' → ' + r.status);
      return r.json();
    }).then(function (d) { dataCache[url] = d; return d; });
  }

  function renderFeature(f, color, group) {
    var lyr = null;
    if (f.polygon) {
      lyr = L.polygon(f.polygon, { pane: 'quilt', color: color, weight: 1.1, opacity: 0.9, fillColor: color, fillOpacity: 0.16 });
    } else if (f.coords) {
      var g = glyphFor(f);
      if (g) {
        lyr = L.marker(f.coords, { icon: glyphIcon(g, glyphColor(f, color), f.layer === 'missions' || f.type === 'presidio' ? 26 : 21) });
        if (f.name && (f.layer === 'missions' || f.layer === 'russian' || f.type === 'presidio' || f.type === 'parish')) {
          var yr = (f.type === 'parish') ? '' : (f.date && f.date.display ? f.date.display.replace(/^est\.\s*/, '') : '');
          lyr.bindTooltip(esc(f.name) + (yr ? '<br>' + esc(yr) : ''), {
            permanent: true, direction: 'bottom', offset: [0, 10], className: 'est-label', opacity: 1
          });
        }
      } else {
        var hollow = f.coord_precision === 'conjectural';
        lyr = L.circleMarker(f.coords, { pane: 'routes', radius: f.radius || 4.5, color: '#fff', weight: 1.6, fillColor: color, fillOpacity: hollow ? 0.25 : 1 });
      }
    }
    if (!lyr) return 0;
    lyr.bindPopup(buildPopup(f), { maxWidth: 420 });
    group.addLayer(lyr);
    if (f.id) featureIndex[f.id] = lyr;
    return 1;
  }

  function renderRoute(rt, fallbackColor, group) {
    var color = rt.color || fallbackColor || '#444';
    var pts = rt.path || (rt.stops || []).map(function (s) { return s.coords; }).filter(Boolean);
    var n = 0;
    if (pts.length > 1) {
      var casing = L.polyline(pts, { pane: 'casing', color: '#ffffff', weight: 6.5, opacity: 0.9, dashArray: null, lineJoin: 'round' });
      var line = L.polyline(pts, { pane: 'routes', color: color, weight: 3.2, opacity: 0.95, dashArray: rt.dash || null, lineJoin: 'round' });
      line.bindPopup(buildPopup({
        name: rt.label || rt.id, summary: rt.summary || '',
        sources: rt.sources || [],
        notes: rt.path_confidence ? 'course: ' + rt.path_confidence : null
      }), { maxWidth: 420 });
      group.addLayer(casing); group.addLayer(line); n++;
    }
    (rt.ends || []).forEach(function (e) {
      if (!e.at || !e.label) return;
      var m = L.marker(e.at, { icon: L.divIcon({ className: 'route-end-anchor', html: '', iconSize: [1, 1] }), interactive: false });
      m.bindTooltip(esc(e.label), { permanent: true, direction: 'right', offset: [6, 0], className: 'route-end-label', opacity: 1 });
      group.addLayer(m);
    });
    (rt.stops || []).forEach(function (s) { n += renderFeature(s, color, group); });
    return n;
  }

  var MEXICAN_LAYERS = { echeandia: 1, figueroa: 1, interim: 1, alvarado: 1, micheltorena: 1, pico: 1, unattributed: 1 };
  function featureFill(era, f, layerColor) {
    if (era.colorModes && era._mode !== 'governor' && f.type === 'rancho') {
      if (f.layer === 'spanish') return '#5b7f92';
      if (MEXICAN_LAYERS[f.layer]) return '#c0603f';
    }
    return layerColor;
  }

  function showEra(era) {
    eraGroup.clearLayers(); layerGroups = {}; featureIndex = {};
    var noteEl = document.getElementById('panel-note');
    var modeHtml = '';
    if (era.colorModes) {
      if (!era._mode) era._mode = 'era';
      modeHtml = ' <span class="mode-switch">Colour: ' +
        '<label><input type="radio" name="rmode" value="era"' + (era._mode === 'era' ? ' checked' : '') + '> Spanish / Mexican</label> ' +
        '<label><input type="radio" name="rmode" value="governor"' + (era._mode === 'governor' ? ' checked' : '') + '> by governor</label></span>';
    }
    noteEl.innerHTML = esc(era.note) + ' <span class="phase2">' + esc(era.phase2) + '</span>' + modeHtml +
      (era.spotlight ? ' <button class="spot-chip" id="spot-btn">' + esc(era.spotlight.label) + '</button>' : '');
    if (era.colorModes) noteEl.querySelectorAll('input[name="rmode"]').forEach(function (r) {
      r.addEventListener('change', function () { era._mode = r.value; showEra(era); });
    });
    var boxes = document.getElementById('layer-boxes');
    boxes.innerHTML = '';
    var count = 0;
    Promise.all(era.files.map(function (spec) { return loadJSON(spec.f); })).then(function (datasets) {
      datasets.forEach(function (data, di) {
        var spec = era.files[di];
        var wanted = function (layerId) { return !spec.only || spec.only.indexOf(layerId) !== -1; };
        (data.layers || []).forEach(function (l) {
          if (!wanted(l.id)) return;
          var key = spec.f + '::' + l.id;
          var g = L.layerGroup();
          layerGroups[key] = { group: g, color: l.color || '#666' };
          if (!spec.off) { eraGroup.addLayer(g); }
          var lab = document.createElement('label');
          lab.innerHTML = '<input type="checkbox" ' + (spec.off ? '' : 'checked') + '> <span class="swatch" style="background:' +
            esc(l.color || '#666') + '"></span>' + esc(l.label || l.id);
          lab.querySelector('input').addEventListener('change', function (e) {
            if (e.target.checked) eraGroup.addLayer(g); else eraGroup.removeLayer(g);
          });
          boxes.appendChild(lab);
        });
        (data.features || []).forEach(function (f) {
          if (!wanted(f.layer)) return;
          var slot = layerGroups[spec.f + '::' + f.layer];
          if (!slot) { slot = layerGroups[spec.f + '::' + f.layer] = { group: L.layerGroup(), color: '#666' }; if (!spec.off) eraGroup.addLayer(slot.group); }
          count += renderFeature(f, featureFill(era, f, slot.color), slot.group);
        });
        (data.routes || []).forEach(function (rt) {
          if (!wanted(rt.layer)) return;
          var slot = layerGroups[spec.f + '::' + rt.layer];
          if (!slot) { slot = layerGroups[spec.f + '::' + rt.layer] = { group: L.layerGroup(), color: '#666' }; if (!spec.off) eraGroup.addLayer(slot.group); }
          count += renderRoute(rt, slot.color, slot.group);
        });
      });
      document.getElementById('feat-count').textContent = count + ' features · anchors in every popup';
      var sb = document.getElementById('spot-btn');
      if (sb && era.spotlight) sb.addEventListener('click', function () {
        var lyr = featureIndex[era.spotlight.feature];
        if (lyr) {
          if (lyr.getBounds) map.fitBounds(lyr.getBounds().pad(0.3)); else map.setView(lyr.getLatLng(), 11);
          lyr.openPopup();
        }
      });
    }).catch(function (err) {
      noteEl.innerHTML = '<strong>Data load failed:</strong> ' + esc(err.message);
    });
  }

  // hide establishment labels when zoomed far out
  map.on('zoomend', function () {
    document.getElementById('map').classList.toggle('labels-off', map.getZoom() < 8.5);
  });

  // ---------- boot: one page, chosen by <body data-panel> ----------
  var page = PAGES[document.body.getAttribute('data-panel')];
  if (page) showEra(page);
})();
