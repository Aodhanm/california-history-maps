#!/usr/bin/env python3
"""Regenerate downloads/ (per-map GeoJSON + combined CSV) from data/*.json."""
import json, csv, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(ROOT, "downloads"), exist_ok=True)
rows = []
for path in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
    d = json.load(open(path))
    feats = list(d.get("features", []))
    for r in d.get("routes", []):
        feats.extend(r.get("stops", []))
    gj = {"type": "FeatureCollection", "features": []}
    for f in feats:
        gj["features"].append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [f["coords"][1], f["coords"][0]]},
            "properties": {k: v for k, v in f.items() if k != "coords"}})
        rows.append({
            "map": d["id"], "id": f["id"], "register_no": f.get("register_no") or "",
            "name": f["name"], "date_iso": (f.get("date") or {}).get("iso") or "",
            "date_display": (f.get("date") or {}).get("display") or "",
            "date_confidence": (f.get("date") or {}).get("confidence") or "",
            "lat": f["coords"][0], "lng": f["coords"][1],
            "coord_precision": f.get("coord_precision") or "",
            "type": f.get("type") or "", "layer": f.get("layer") or "",
            "summary": f.get("summary") or "", "result": f.get("result") or "",
            "native_groups": "; ".join(f.get("native_groups") or []),
            "sources": " | ".join(s.get("citation", "") for s in (f.get("sources") or [])),
            "notes": f.get("notes") or ""})
    out = os.path.join(ROOT, "downloads", d["id"] + ".geojson")
    json.dump(gj, open(out, "w"), ensure_ascii=False)
    print("wrote", out, len(gj["features"]), "features")
csvp = os.path.join(ROOT, "downloads", "california-history-maps-all.csv")
with open(csvp, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print("wrote", csvp, len(rows), "rows")
