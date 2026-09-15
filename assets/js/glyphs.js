/* Pictorial map symbols, in the manner of an engraved historical atlas.
 *
 * Each symbol is a SILHOUETTE — filled shapes, no enclosing chip. Legibility over a
 * busy basemap comes from drawing the same shapes twice: once in white with a fat
 * round-joined stroke (the halo), then again in the feature colour on top.
 *
 * Every shape is FILLED. Nothing relies on its own stroke, because the halo pass
 * would override it.
 *
 * DIRECTION. The pictorial symbols are drawn in elevation, so rotating one to a
 * bearing makes the piece look like it is toppling over. Facing is carried instead by
 * a separate needle that swings around the symbol, and — on the map itself — by a
 * sector of fire drawn in real geographic space at the gun's real range.
 */
(function (global) {
  'use strict';

  var BOX = 24;

  var GLYPHS = {

    /* ---------------- ordnance ---------------- */

    // muzzle-loading smoothbore on a wheeled carriage — Spanish, Mexican, Third System
    // Barrel TAPERS toward the muzzle and carries a muzzle swell; an arrowhead here
    // reads as an arrow, not a gun.
    cannon:
      '<path d="M3.4 5.6 18 7.6v4L3.4 13.6z"/>' +          // tapering tube
      '<path d="M17.6 6.9h2.8v5.4h-2.8z"/>' +              // muzzle swell
      '<circle cx="2.6" cy="9.6" r="1.9"/>' +              // cascabel knob at the breech
      '<path d="M5 12.4 .6 21.2h3.1L8.4 13.6z"/>' +        // trail
      '<circle cx="9.4" cy="16.4" r="4.3"/>',              // wheel

    // Endicott rifle: long tapering tube on a carriage behind a concrete parapet
    rifle:
      '<path d="M4.6 4.8 19 6.6v3.4L4.6 11.8z"/>' +
      '<path d="M18.6 5.9h2.6v4.8h-2.6z"/>' +
      '<path d="M5.4 10.6h5.2v3.6H5.4z"/>' +               // carriage
      '<path d="M1.2 14h11.4l2.6 6.8H-1.4z"/>',            // parapet

    // seacoast mortar: short, very fat tube at high angle, sunk in its pit
    mortar:
      '<path d="M8.2 13.4 13.6 3.6l6.4 3.5-5.4 9.8z"/>' +
      '<path d="M12.6 2.2 20.8 6.7l-1.2 2.2-8.2-4.5z"/>' + // wide bore mouth
      '<path d="M2.6 15.8h14.2l2.8 5.4H-.2z"/>',           // pit

    // WWII casemate: a low concrete block, gun through the embrasure
    casemate:
      '<path d="M.6 13.8 3.4 9.2h8.8l2.8 4.6v7.2H.6z"/>' +
      '<path d="M13.4 10.4 21.2 11.8v2.6l-7.8 1.4z"/>' +
      '<path d="M20.8 11.1h2.4v4h-2.4z"/>',

    // anti-aircraft: slim barrel steeply elevated on a pedestal with spread legs
    aagun:
      '<path d="M11.4 14.6 18.2 1.8l3.2 1.7-6.8 12.8z"/>' +
      '<path d="M20.6 1 23 2.3l-1.2 2.3-2.4-1.3z"/>' +
      '<path d="M7.6 14.8h6.8l1.6 3.6H6z"/>' +
      '<path d="M2 21.4 6.6 17.6l1.6 2-4.6 3.8zM16.4 19.6l1.6-2 4.6 3.8-1.6 2z"/>',

    // Nike missile on its angled launcher
    nike:
      '<path d="M6.2 15.4 15.8 5l4-1.8-1.4 4.2-9.6 10.4z"/>' +   // body and nose cone
      '<path d="M6.4 15.2 3.2 14l2.4 4.4 3-.8z"/>' +             // tail fin
      '<path d="M2.6 19.4h11l1.4 2.6H4z"/>',                     // launcher base

    // four-bastioned fort in plan — the atlas convention for a masonry work
    fort:
      '<path d="M19.9 4.1 16.2 12l3.7 7.9L12 16.2l-7.9 3.7L7.8 12 4.1 4.1 12 7.8z"/>',

    // Spanish horseshoe battery, plan
    castillo:
      '<path d="M2.2 21V13c0-5.4 4.4-9.2 9.8-9.2S21.8 7.6 21.8 13v8h-5.2v-8c0-3-2.2-5-4.6-5s-4.6 2-4.6 5v8z"/>',

    // field earthwork: a low parapet
    earthwork:
      '<path d="M.6 20.8 5.6 11.6h12.8l5 9.2z"/>',

    // presidio / garrison quadrangle, plan
    presidio:
      '<path d="M2.2 4h19.6v16H2.2zm3.4 3.4v9.2h12.8V7.4z" fill-rule="evenodd"/>',

    // contact mine — the submarine-mine defence of the channel
    mine:
      '<circle cx="12" cy="15.4" r="5.8"/>' +
      '<path d="M11 6.2h2v3.4h-2z"/>' +
      '<path d="M5.6 8.8 7.2 7.2l2.5 2.5-1.6 1.6z"/>' +
      '<path d="M18.4 8.8 16.8 7.2l-2.5 2.5 1.6 1.6z"/>',

    // anti-submarine net between buoys
    net:
      '<circle cx="3.2" cy="6.6" r="2.6"/><circle cx="20.8" cy="6.6" r="2.6"/>' +
      '<path d="M1.8 10h20.4v2H1.8z"/>' +
      '<path d="M4.2 12h1.7l2.8 8.8H7zM11.1 12h1.7l2.8 8.8h-1.7zM18 12h1.7l2.8 8.8h-1.7z"/>' +
      '<path d="M2.6 15.6h18.4v1.6H2.6z"/>',

    /* ---------------- maritime & lumber ---------------- */

    // apron or trough chute running down to the water on trestle legs
    chute:
      '<path d="M1.8 3.8 3.4 1.8 22.4 14.8l-1.6 2z"/>' +
      '<path d="M8 8h2v10.6H8zM14.4 12.4h2v6.2h-2z"/>' +
      '<path d="M.8 1.4h2.8v4.8H.8z"/>',

    // wire chute: a slung cable from the headland out over the ship
    wirechute:
      '<path d="M1.2 3.8C8.2 10.6 15.6 14.2 22.6 15.2l-.4 2.4C14.4 16.5 6.6 12.6-.4 5.4z"/>' +
      '<path d="M6.8 8.6h1.6v4.6H6.8zM12 11.8h1.6v4.6H12zM17.2 14h1.6v4.6h-1.6z"/>' +
      '<path d="M.2 2h2.8v5.6H.2z"/>',

    // wharf: a deck carried on piles
    pier:
      '<path d="M1.2 8.8h21.6v2.8H1.2z"/>' +
      '<path d="M3.6 11.6h2v9.2h-2zM8.6 11.6h2v9.2h-2zM13.6 11.6h2v9.2h-2zM18.6 11.6h2v9.2h-2z"/>',

    // river-bar harbour: the stream, and the bar across its mouth
    riverbar:
      '<path d="M10.1 1h3.8v6.6h3.2L12 12.4 6.9 7.6h3.2z"/>' +
      '<path d="M1.2 13.6c2.3-2.1 4.5-2.1 6.8 0s4.5 2.1 6.8 0 4.5-2.1 6.8 0v2.6c-2.3-2.1-4.5-2.1-6.8 0s-4.5 2.1-6.8 0-4.5-2.1-6.8 0z"/>' +
      '<path d="M1.2 18.2c2.3-2.1 4.5-2.1 6.8 0s4.5 2.1 6.8 0 4.5-2.1 6.8 0v2.6c-2.3-2.1-4.5-2.1-6.8 0s-4.5 2.1-6.8 0-4.5-2.1-6.8 0z"/>',

    // deepwater port
    anchor:
      '<path d="M12 .8a3 3 0 00-1.3 5.7v1.8H7.4v2.8h3.3v9.4c-3.2-.6-5.6-2.9-6-5.9l-2.6.7C2.9 19.9 7 23.2 12 23.2s9.1-3.3 9.9-8.3l-2.6-.7c-.4 3-2.8 5.3-6 5.9v-9.4h3.3V8.3h-3.3V6.5A3 3 0 0012 .8zm0 2.3a1 1 0 110 2 1 1 0 010-2z" fill-rule="evenodd"/>',

    // shipyard: a hull on the stocks
    shipyard:
      '<path d="M1.4 13h21.2l-3.4 6H4.8z"/>' +
      '<path d="M11 2.4h2.1v10.6H11z"/>' +
      '<path d="M13.1 3.2 19.8 7l-6.7 3.6z"/>' +
      '<path d="M2.6 19.8h18.8v2.2H2.6z"/>',

    // mill
    mill:
      '<path d="M1.6 21V10.4L9.4 5.4l7.8 5V21z"/>' +
      '<path d="M18.4 6h3.6v15h-3.6z"/>' +
      '<circle cx="22.4" cy="2.6" r="1.8"/><circle cx="19" cy="1.2" r="1.3"/>',

    lighthouse:
      '<path d="M12 .8 15.8 5H8.2z"/>' +
      '<path d="M9.2 5.4h5.6v3.8H9.2z"/>' +
      '<path d="M8.6 9.6h6.8l1.5 11.2H7.1z"/>' +
      '<path d="M5.4 20.8h13.2v2.2H5.4z"/>' +
      '<path d="M0 4.6 6.8 6.5l-.6 2.3L-.6 6.9z"/>' +
      '<path d="M24 4.6 17.2 6.5l.6 2.3 6.8-1.9z"/>',

    lightship:
      '<path d="M.6 15.6h22.8l-3.6 6.2H4.2z"/>' +          // hull
      '<path d="M8.4 11.8h7.2v3.8H8.4z"/>' +               // deckhouse
      '<path d="M11 3.2h2v8.8h-2z"/>' +                    // mast
      '<circle cx="12" cy="2.6" r="2.6"/>',                // masthead lantern

    ruin:
      '<path d="M2.8 21V8L7 5v3.8l4-3v4.2l4.2-3.4v4.6l4.4-3.6V21z"/>',

    // a work surveyed, funded or begun but never armed: the trace only
    unbuilt:
      '<path d="M19.9 4.1 16.2 12l3.7 7.9L12 16.2l-7.9 3.7L7.8 12 4.1 4.1 12 7.8z"/>'
  };

  /* ---------------- rendering ---------------- */

  function shapes(name) { return GLYPHS[name] || null; }

  /* opts: size, bearing, arc [left,right], hollow, halo */
  function glyphSvg(name, color, opts) {
    opts = opts || {};
    var s = shapes(name);
    if (!s) return null;
    var px = opts.size || 22;
    var halo = opts.halo === undefined ? 2.0 : opts.halo;
    var hasAim = opts.bearing !== null && opts.bearing !== undefined;

    // a bearing needs room around the symbol for the wedge to swing
    var pad = hasAim ? 13 : 0;
    var vb = (-pad) + ' ' + (-pad) + ' ' + (BOX + pad * 2) + ' ' + (BOX + pad * 2);
    var scale = (BOX + pad * 2) / BOX;
    var wpx = Math.round(px * scale);

    var out = '<svg width="' + wpx + '" height="' + wpx + '" viewBox="' + vb +
              '" class="sym' + (opts.hollow ? ' sym-hollow' : '') + '" aria-hidden="true">';

    if (hasAim) out += aimWedge(opts.bearing, opts.arc, color, pad);

    // halo pass
    out += '<g fill="#ffffff" stroke="#ffffff" stroke-width="' + halo +
           '" stroke-linejoin="round" stroke-linecap="round">' + s + '</g>';
    if (opts.hollow) {
      out += '<g fill="#ffffff" fill-opacity="0.85" stroke="' + color +
             '" stroke-width="1.6" stroke-linejoin="round">' + s + '</g>';
    } else {
      out += '<g fill="' + color + '">' + s + '</g>';
      out += '<g fill="none" stroke="rgba(26,22,18,0.5)" stroke-width="0.55" ' +
             'stroke-linejoin="round">' + s + '</g>';
    }
    return out + '</svg>';
  }

  /* The wedge: a sector outside the symbol, showing where the guns bore.
     TRUE bearings — 0 is north, which in svg is -y.
     Given an arc [left, right] it draws the documented traverse; given only a centre
     bearing it draws a narrow spike, so the two cases stay visually distinct. */
  function aimWedge(bearing, arc, color, pad) {
    var cx = BOX / 2, cy = BOX / 2;
    var r0 = 12.2, r1 = 12.2 + pad - 1.2;
    var l, r;
    if (arc && arc.length === 2) {
      l = arc[0]; r = arc[1];
      var span = (r - l + 360) % 360;
      if (span < 8) { l = bearing - 5; r = bearing + 5; }        // too tight to read
      if (span > 300) { l = bearing - 150; r = bearing + 150; }  // effectively all-round
    } else {
      l = bearing - 7; r = bearing + 7;
    }
    function P(deg, rad) {
      var a = (deg - 90) * Math.PI / 180;
      return (cx + rad * Math.cos(a)).toFixed(2) + ' ' + (cy + rad * Math.sin(a)).toFixed(2);
    }
    var sweep = (r - l + 360) % 360;
    var big = sweep > 180 ? 1 : 0;
    var d = 'M' + P(l, r0) + 'L' + P(l, r1) +
            'A' + r1 + ' ' + r1 + ' 0 ' + big + ' 1 ' + P(r, r1) +
            'L' + P(r, r0) +
            'A' + r0 + ' ' + r0 + ' 0 ' + big + ' 0 ' + P(l, r0) + 'Z';
    return '<path d="' + d + '" fill="' + color + '" fill-opacity="0.85" stroke="#ffffff" ' +
           'stroke-width="1.6" stroke-linejoin="round" paint-order="stroke"/>';
  }

  // repeated symbols for magnitude — three cannon is a heavier battery than one
  function glyphRow(name, color, count, opts) {
    var n = Math.max(1, Math.min(count || 1, 4)), out = '', i;
    for (i = 0; i < n; i++) out += glyphSvg(name, color, opts);
    return '<span class="sym-row">' + out + '</span>';
  }

  global.MapGlyphs = {
    BOX: BOX,
    names: function () { return Object.keys(GLYPHS); },
    svg: glyphSvg,
    row: glyphRow
  };
})(window);
