# Map data schema (v2, 2026-07-14)

Every map = one JSON file in `data/`, rendered by `assets/js/map-engine.js`. Adding a map = writing one of these files + a 10-line shell page (see `ADD-A-MAP.md`).

## Top level

```json
{
  "id": "military-engagements",          // = shell filename + permalink base
  "title": "Military Engagements in Spanish and Mexican California",
  "subtitle": "1769–1848",
  "abstract": "One-paragraph scholarly abstract shown in the About panel.",
  "date_range": [1769, 1848],
  "center": [36.5, -120.5],
  "zoom": 6,
  "cite_key": "military",                 // used by the Cite button
  "last_updated": "2026-07-14",
  "layers": [ {"id": "phase1", "label": "San Diego & Coastal Resistance (1769–1790)", "color": "#c0392b"} ],
  "legend_note": "optional extra legend text",
  "features": [ ... ],
  "routes": [ ... ]                        // optional
}
```

## Feature

```json
{
  "id": "reg-121-jacum",                  // stable slug — THE permalink (#reg-121-jacum)
  "register_no": "121",                   // military-register # where applicable, else null
  "name": "The Jacum battle — capitanejo Charagui defeats the San Diego column",
  "date": {"iso": "1837-05", "display": "May 1837", "confidence": "month"},
       // confidence: exact | month | year | circa | range
  "coords": [32.62, -116.19],
  "coord_precision": "place",             // exact | place | area | conjectural
       // exact = the source pins the spot; place = known settlement/feature;
       // area = right district, spot approximated; conjectural = educated guess, styled hollow
  "type": "battle",                       // battle | raid | revolt | standoff | expedition-leg |
                                           // settlement | mission | presidio | port | event | document
  "layer": "phase6",
  "summary": "1–3 verified sentences.",
  "result": "Indigenous victory",         // short characterization, must match the register
  "quote": {"es": "…", "en": "…", "source": "C-A 37 Doc 188"},   // optional, verbatim per Savage
  "sources": [
    {"citation": "Dep. St. Pap., Angeles (C-A 37), orig. pp. 420–424 (Savage 86–89)",
     "ca_record": "ca37-d188",            // archives-of-california record id, or null
     "ia_leaf_url": "https://archive.org/details/.../page/n87"}   // or null
  ],
  "native_groups": ["Kumeyaay"],          // named polities/leaders where the sources allow
  "tags": ["indian-war-1837"],
  "notes": "uncertainty / editorial remarks, shown small in the popup"
}
```

## Route (expedition paths)

```json
{
  "id": "moraga-1806",
  "label": "Moraga's First Interior Expedition (Sep–Oct 1806)",
  "layer": "exp1806",
  "color": "#8B2500",
  "dash": null,                            // or "6 6" for uncertain path segments
  "stops": [ <feature objects with type: "expedition-leg"> ],
  "path_confidence": "reconstructed"       // documented | reconstructed | conjectural
}
```
Routes draw a polyline through their stops' coords, in order. `path_confidence` ≠ "documented" renders dashed and says so in the legend — a reconstructed line means "he passed roughly this way," never a surveyed track.

## Rules
1. Every feature traces to the military register row or a vault source file. No inference-as-fact; vague sourcing → `coord_precision: "conjectural"` + a note.
2. Citations use the field-standard form (series, tomo, ORIGINAL page) and record the Savage/scan page too.
3. Spanish quotes verbatim as Savage wrote them; concerns go in `notes`, never silent fixes.
4. Counts on the landing page are computed from these files, never hand-typed.
5. `scripts/check_counts.py` must pass before any commit that touches `data/`.

## Optional feature/map fields added 2026-09-13 (lumber-ports; all data-gated, other maps unaffected)

- `feature.radius` — circleMarker radius override (pin size = port class on lumber-ports).
- `feature.active` — `{first, last}` years; when present the year slider filters by RANGE OVERLAP
  instead of point-year containment (right model for long-lived ports).
- `feature.facts` — `[["Label", "value"], …]` rendered as a small table in the popup.
- `feature.photo` — `{url, credit, alt}` optional historic photo in the popup.
- `map.era_presets` — `[{label, from, to}]` buttons that snap the year window to a named period.
- `map.attribute_filters` — `[{key, label, values?, value_labels?}]` dropdown filters over feature
  fields (string or array valued, e.g. `port_class`, `cargo`, `company`); values derived from the
  data when omitted.
- `map.unlocated` — features documented but deliberately NOT pinned (no coords); listed in the
  About panel. The engine ignores this key; check_counts does not require coords for it.
- `route.path` — optional dense `[[lat,lon], …]` polyline following the real corridor; when
  present it replaces the stop-to-stop line (stops keep their markers). Added for lumber-ports
  railroads 2026-09-13.
