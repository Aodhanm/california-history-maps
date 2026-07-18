# California History Maps

**Live: https://maps.archivesofcalifornia.com/**

Interactive, source-cited maps of Spanish and Mexican California (1769–1848),
data-driven from JSON files and a shared Leaflet engine. Companion to
[*Archives of California: A Documentary Calendar of the Savage Transcripts*](https://archivesofcalifornia.com/).

## Layout
- `data/*.json` — one dataset per map ([schema](data/schema.md))
- `assets/js/map-engine.js` — the shared renderer (uncertainty styling, timeline,
  search, permalinks, citations, DB deep links)
- `maps/*.html` — thin shells, one per map
- `gallery/` — curated public-domain historical map gallery
- `scripts/check_counts.py` — data integrity guard; run before committing data changes
- Root-level legacy filenames redirect to the new pages.

## Adding a map
See [ADD-A-MAP.md](ADD-A-MAP.md) — one JSON file, one shell page, one landing card.

## License
Content CC-BY-4.0, code MIT — see [LICENSE](LICENSE). Cite via [CITATION.cff](CITATION.cff).
