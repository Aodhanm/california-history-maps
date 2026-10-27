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

    // mission church — establishment-system artwork (panels-engine.js)
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

    // pueblo — establishment-system artwork
    pueblo:
      '<path d="M2.2 20.8v-7.6l4.9-3.2 4.9 3.2v7.6z"/>' +
      '<path d="M12.6 20.8v-6.1l4.1-2.7 4.1 2.7v6.1z"/>' +
      '<path fill="#fff" d="M5.8 20.8v-3.9c0-.8.55-1.3 1.3-1.3s1.3.5 1.3 1.3v3.9z"/>' +
      '<rect fill="#fff" x="15.6" y="16" width="2.2" height="2.2"/>',

    // outstation house — Spanish outstations and Russian farm ranches alike
    house:
      '<path d="M2.6 12.8 12 6.4l9.4 6.4-1.3 1.9L12 9.1l-8.1 5.6z"/>' +
      '<path fill-rule="evenodd" d="M5 14.2 12 9.4l7 4.8V21H5zM10.9 15.4h2.2V21h-2.2z"/>',

    // Russian-American Company double-headed eagle — establishment-system artwork
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

    // longhorn — hacienda/rancho headquarters, establishment-system artwork
    longhorn:
      '<path d="M9.7 12.2c0-2.1 1-3.6 2.3-3.6s2.3 1.5 2.3 3.6c0 2.7-1 5.2-2.3 5.2s-2.3-2.5-2.3-5.2z"/>' +
      '<path d="M10.9 9.4C8 8.9 5.3 7.4 4 4.9c2.7-.2 5.5.7 7.5 2.4z"/>' +
      '<path d="M13.1 9.4c2.9-.5 5.6-2 6.9-4.5-2.7-.2-5.5.7-7.5 2.4z"/>',

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

    // sailing ship — a vessel's visit, sighting, or action on the coast
    ship:
      '<path d="M2.2 17.2h19.6l-2.6 4.4H4.8z"/>' +
      '<path d="M11.2 2.2h1.2v15h-1.2z"/>' +
      '<path d="M12.8 3.2c3.6 1.6 5.4 4.6 5.4 8.6 0 .6 0 1.2-.1 1.8h-5.3z"/>' +
      '<path d="M10.8 5.4c-2.8 1.3-4.3 3.7-4.3 6.8 0 .5 0 .9.1 1.4h4.2z"/>',

    // baidarka — a Russian-Aleut hunting party afloat
    kayak:
      '<path d="M1 16.6c3.6 1.6 8 2.4 11 2.4s7.4-.8 11-2.4c-1.6 2.4-6 4-11 4s-9.4-1.6-11-4z"/>' +
      '<circle cx="12" cy="12.2" r="1.7"/>' +
      '<path d="M11.2 14h1.6v3.4h-1.6z"/>' +
      '<path d="M5.6 10.2 17.8 16l-.5 1.1L5.1 11.3z"/>',

    // parish / presidio chapel (secular church): nave with a square bell TOWER —
    // distinct from the mission's espadaña bell-wall
    parish:
      '<path d="M1.8 21v-7.6h13.4V21z"/>' +
      '<path d="M1 13.6l7.5-4.4 7.5 4.4-.9 1.5-6.6-3.9-6.6 3.9z"/>' +
      '<path d="M15.8 21V8.2h6V21z"/>' +
      '<path d="M15.2 8.6l3.6-3 3.6 3z"/>' +
      '<path fill="#fff" d="M17.6 10.4h2.4v3h-2.4zM6.4 16h3v5h-3z"/>' +
      '<path d="M18.1 2h1.4v2.6h-1.4z"/><path d="M17.2 2.9h3.2v1h-3.2z"/>',

    // rancheria — a Native polity or village: domed tule houses
    rancheria:
      '<path d="M3.4 18.6c0-4.6 3-7.8 6.8-7.8s6.8 3.2 6.8 7.8v1.8H3.4z"/>' +
      '<path d="M15.4 20.4v-1.2c0-3.2 2-5.4 4.6-5.4 1.4 0 2.6.6 3.4 1.7-.5 1.9-.7 3.3-.7 4.9z" transform="translate(-1.4 0)"/>' +
      '<path fill="#fff" d="M8.6 20.4v-3.4c0-1.1.7-1.8 1.6-1.8s1.6.7 1.6 1.8v3.4z"/>',

    // scroll — a decree, order, or report: rolled head and foot, text between
    scroll:
      '<path d="M4.2 3.2h15.6a2.1 2.1 0 010 4.2H4.2a2.1 2.1 0 010-4.2z"/>' +
      '<path d="M5.6 7.4h12.8v9.2H5.6z"/>' +
      '<path d="M4.2 16.6h15.6a2.1 2.1 0 010 4.2H4.2a2.1 2.1 0 010-4.2z"/>' +
      '<path fill="#fff" d="M7.4 9.4h9.2v1.3H7.4zM7.4 12h9.2v1.3H7.4zM7.4 14.6h6.2v1.3H7.4z"/>',

    // flame — a raid or burning
    flame:
      '<path d="M12.6 1.6c.6 3 2.8 4.6 4.6 6.8 1.6 2 2.6 4 2.6 6.2 0 4.4-3.4 7.8-7.8 7.8s-7.8-3.4-7.8-7.8c0-2.9 1.5-5 3.1-7 .3 1.2.9 2.1 1.9 2.8-.3-3.4.8-6.3 3.4-8.8z"/>' +
      '<path fill="#fff" d="M12.1 20.6c-2 0-3.6-1.6-3.6-3.7 0-1.5.8-2.5 1.7-3.6.3.9.8 1.4 1.6 1.8-.2-1.6.3-3 1.4-4.2.4 1.7 1.4 2.6 2.2 3.7.6.9 1 1.6 1 2.5 0 2-1.6 3.5-4.3 3.5z"/>',

    // parallel sabers, not crossed — an armed standoff without battle
    standoff:
      '<path d="M2.2 4.4 13.8 15l-1.5 1.6L.7 6z"/>' +
      '<path d="M13.6 13.8l3.2 2.9-1.1 1.3-1.3-.5-.5 1.3-1.3 1.1-2.9-3.2z"/>' +
      '<path d="M9.2 2.2 20.8 12.8l-1.5 1.6L7.7 3.8z"/>' +
      '<path d="M20.6 11.6l3.2 2.9-1.1 1.3-1.3-.5-.5 1.3-1.3 1.1-2.9-3.2z"/>',

    // beacon — a minor light or fog signal
    beacon:
      '<path d="M11 8h2v13h-2z"/>' +
      '<path d="M8 21h8v1.6H8z"/>' +
      '<path d="M9.4 3h5.2v5H9.4z"/>' +
      '<path d="M7.9 1.6h8.2v1.2H7.9z"/>' +
      '<path d="M4.6 4.2l3 1.2v1.4l-3 1.2zM19.4 4.2l-3 1.2v1.4l3 1.2z"/>',

    // dwelling-style light: keeper's house carrying the lantern on its roof
    lhhouse:
      '<path d="M3 21.2v-7.8h12v7.8z"/>' +
      '<path d="M1.8 13.8 9 8.6l7.2 5.2-1 1.4L9 10.9l-6.2 4.3z"/>' +
      '<path fill="#fff" d="M6.6 21.2v-4h2.6v4zM10.8 15.6h2.2v2.6h-2.2z"/>' +
      '<path d="M16.6 21.2V10.4h4.2v10.8z"/>' +
      '<path d="M16 10.6V7.2h5.4v3.4z"/>' +
      '<path fill="#fff" d="M17.2 8h3v1.8h-3z"/>' +
      '<path d="M15.5 7.4h6.4v1h-6.4z"/><path d="M17.8 4.8h1.8v2.4h-1.8z"/>',

    // crossed sabers — a battle or armed engagement
    swords:
      '<path d="M3.2 2.6 18.6 16.4l-1.6 1.8L1.8 4.8z"/>' +
      '<path d="M18.4 15.2 22 18.4l-1.2 1.4-1.4-.6-.6 1.4-1.4 1.2-3.2-3.6z"/>' +
      '<path d="M20.8 2.6 5.4 16.4l1.6 1.8L22.2 4.8z"/>' +
      '<path d="M5.6 15.2 2 18.4l1.2 1.4 1.4-.6.6 1.4 1.4 1.2 3.2-3.6z"/>',

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
    /* ---------------- possession-acts map (2026-10-26 prototype) ---------------- */

    // planted possession cross on its stone cairn (formulario arts. X-XI)
    cross:
      '<path d="M10.9 2h2.2v15.5h-2.2z"/>' +
      '<path d="M5.2 5.9h13.6v2.3H5.2z"/>' +
      '<path d="M4 22c1.4-3.6 4.2-5.6 8-5.6s6.6 2 8 5.6z"/>',

    // royal crown - British claims
    crown:
      '<path d="M3.8 16.2 5 8l4.6 4.2L12 5.4l2.4 6.8L19 8l1.2 8.2z"/>' +
      '<path d="M3.8 17.4h16.4v3.4H3.8z"/>' +
      '<circle cx="5" cy="6.6" r="1.4"/><circle cx="12" cy="4" r="1.4"/><circle cx="19" cy="6.6" r="1.4"/>',

    // flag on its pole - American claims (Jones 1842, Sloat 1846)
    flagus:
      '<path d="M4.4 3.4h1.8V22H4.4z"/>' +
      '<circle cx="5.3" cy="2.4" r="1.3"/>' +
      '<path d="M6.6 4.2c4.8-1.6 8.6 1.8 13.8.2l-1.4 3.4 1.4 3.6c-5.2 1.6-9-1.8-13.8-.2z"/>',

    // fleur-de-lis - French claims (Laperouse 1786)
    fleur:
      '<path d="M12 1.8c-2.6 3.8-2.6 7.4 0 10.6 2.6-3.2 2.6-6.8 0-10.6z"/>' +
      '<path d="M10.4 11.2C6.2 7.6 3 9.2 4 12.8c.8 2.6 3.8 3 6.8 1.4z"/>' +
      '<path d="M13.6 11.2c4.2-3.6 7.4-2 6.4 1.6-.8 2.6-3.8 3-6.8 1.4z"/>' +
      '<path d="M8.6 14.6h6.8v2.4H8.6z"/>' +
      '<path d="M12 17.4c-1.6 1.8-1.6 3.2 0 4.6 1.6-1.4 1.6-2.8 0-4.6z"/>',

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
