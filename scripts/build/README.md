# scripts/build — dataset builders

Reproducible pipeline (needs `pip install pyshp` for the native map):

- `build_native_poly.py` then `post_native.py` → `data/native-california.json`
  (territory polygons from `data-src/handbook-territories/`, U. of Redlands
  digitization of the Handbook of North American Indians vol. 8; then subgroups
  layer + the flagged Carquinez editorial deviation)
- `build_missions.py` → `data/missions-establishments.json`
- Others are archival: the one-time v1→v2 migration extractors and the session
  builders for the military/borderlands/expedition/presidial/corridor/gallery
  datasets, kept for provenance. The live JSONs in `data/` are canonical.

After any dataset change run, from the repo root:
`python3 scripts/check_counts.py && python3 scripts/make_downloads.py && python3 scripts/make_previews.py`
