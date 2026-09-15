# Map symbol prototype — pictorial silhouettes

Built 2026-09-14. **Nothing here has been applied to the live site.** Every published file
in `~/california-history-maps` was reverted; HEAD stayed at `12d0c0f`.

## Run it

```sh
cd ~/map-symbol-demo
python3 -m http.server 8479
```

Then open:

| page | what it shows |
|---|---|
| `glyph-sheet.html` | **start here** — all 23 symbols, large, and over land / water / a dark ground |
| `maps/demo-lumber.html` | lumber ports, whole coast (the zoom-tiering: minor ports drop to dots) |
| `maps/demo-lumber-detail.html` | lumber ports, Mendocino coast — the symbol variety reads here |
| `maps/demo-ordnance-detail.html` | coastal defence, the Golden Gate |
| `maps/demo-ordnance-landsend.html` | Lands End, Fort Miley, Fort Funston |
| `maps/demo-ordnance-alcatraz.html` | Alcatraz, Fort Mason, Yerba Buena Island |
| `maps/demo-ordnance-angel.html` | Angel Island |
| `maps/demo-ordnance-carquinez.html` | Carquinez Strait and Mare Island |
| `maps/demo-ordnance-bay.html` | the whole system, Gate to the Travis ring |

`screenshots/` has all nine views as images, numbered, in case you just want to look
without booting the server — `00-symbol-sheet.jpg` first.

Note: these eight map pages are only **two datasets**. The six ordnance pages are the same
map opened at different places, not six different maps.

## What is where

- `assets/js/glyphs.js` — **the actual deliverable.** 23 silhouettes plus the rendering.
  Self-contained, no dependencies. This is the file to lift into the site when the time comes.
- `assets/js/map-engine.js` — a COPY of the site engine with the symbol hooks patched in.
  Do not copy this over the live engine wholesale; it has drifted. Port the hooks.
- `build_ordnance_demo.py` — rebuilds the ordnance demo data from the live
  `data/bay-coastal-defense.json`. Reads that file, writes only into this folder.
- `bearings-PARTIAL.json` — see the warning below.

## How a feature opts in

All data-gated. A feature with no `symbol` key renders exactly as before.

```json
{
  "symbol": "cannon",        // one of the 23 names in glyphs.js
  "symbol_count": 3,         // repeats the glyph, max 4 — magnitude
  "symbol_major": true,      // keeps its glyph below the dot-tier zoom
  "symbol_min_zoom": 11,     // per-feature override
  "unbuilt": true            // draws hollow: white fill, coloured outline
}
```

A feature whose `coord_precision` is `conjectural` also draws hollow automatically, with no
extra key — so an uncertain position looks uncertain. Point Blunt's AMTB battery on Angel
Island is the live example.

## ⚠ bearings-PARTIAL.json — UNVERIFIED, do not publish

A research pass on where the Bay batteries' guns actually bore was **stopped part-way**
on Aodhan's instruction (orientation is not wanted for now). 101 battery records, 53
carrying a bearing, some with documented traverse arcs and ranges.

**The adversarial verification stage never ran on any of it.** Nothing in this file has been
checked. It is kept only so the work is not lost. If orientation is ever picked back up,
re-run the verification before a single bearing goes on a map.

The rendering side is already written and working: a feature carrying `bearing` (true
azimuth) draws a wedge on its symbol, an optional `arc: [left, right]` draws the documented
traverse instead of a spike, and `range_m` draws a real geographic sector of fire at the
gun's actual range.

## Known problems, to fix before this ships

1. The repeated-glyph magnitude row is wider than a dot, so the visual mass hangs to one
   side of the true anchor point. Centre it.
2. Four-glyph rows are too wide at the Golden Gate, where a dozen Endicott batteries sit
   within a few hundred metres. A number badge above three would probably be better.
3. `unbuilt` and `fort` currently share a shape (the bastioned star), distinguished only by
   hollow-vs-solid. Fine in isolation, worth a second look side by side.
