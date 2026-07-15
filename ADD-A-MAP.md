# How to add a map (checklist)

Cold-start instructions; no tooling beyond Python 3 needed.

1. **Write the dataset** `data/<map-id>.json` following [`data/schema.md`](data/schema.md).
   - Every feature: verified source citation (series + tomo + ORIGINAL page, Savage/scan
     page too), honest `coord_precision` and `date.confidence`.
   - Expedition paths go in `routes` (stops inherit the route `citation`).
   - Spanish quotes verbatim; editorial concerns in `notes`.
2. **Run the guard:** `python3 scripts/check_counts.py` — must pass.
3. **Create the shell:** copy `maps/military-engagements.html` to `maps/<map-id>.html`;
   change `data-map`, `<title>`, the two descriptions, and the `<h1>`.
4. **Add a landing card** in `index.html` (`.card-grid`) and append the map id to the
   `maps` array in the stats script at the bottom of `index.html`.
5. **Commit** data + shell + card together; push to `main` (Pages redeploys automatically).
6. **Vault:** add/update the map's landing note in `~/vault/maps/`, cross-link, and note
   the addition in the progress/registry files.
