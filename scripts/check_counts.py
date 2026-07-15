#!/usr/bin/env python3
"""Data integrity check for California History Maps. Run before any commit touching data/.

Checks every data/*.json against the schema's hard rules:
 - unique feature ids (site-wide, since permalinks are per page but ids double as anchors)
 - coords in plausible range, coord_precision & date.confidence from the allowed vocab
 - every non-reference feature has at least one source citation
 - layer references resolve
Exits non-zero on any failure. Also prints per-map counts for the landing page.
"""
import json, sys, glob, os

PREC = {"exact", "place", "area", "conjectural"}
CONF = {"exact", "month", "year", "circa", "range"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fail = 0

def err(msg):
    global fail
    fail += 1
    print("FAIL:", msg)

for path in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
    data = json.load(open(path))
    name = os.path.basename(path)
    ids = set()
    layers = {l["id"] for l in data.get("layers", [])}
    feats = list(data.get("features", []))
    for r in data.get("routes", []):
        feats.extend(r.get("stops", []))
        if r.get("layer") and r["layer"] not in layers:
            err(f"{name}: route {r.get('id')} references unknown layer {r['layer']}")
    n_src = 0
    for f in feats:
        fid = f.get("id")
        if not fid:
            err(f"{name}: feature without id: {f.get('name')}"); continue
        if fid in ids:
            err(f"{name}: duplicate id {fid}")
        ids.add(fid)
        c = f.get("coords")
        if (not isinstance(c, list) or len(c) != 2 or
                not (22 <= c[0] <= 45) or not (-127 <= c[1] <= -108)):
            # 22°N reaches Cabo San Lucas (Cochrane's 1822 Baja raids are registered)
            err(f"{name}: {fid} coords out of range: {c}")
        if f.get("coord_precision") not in PREC:
            err(f"{name}: {fid} bad coord_precision {f.get('coord_precision')}")
        conf = (f.get("date") or {}).get("confidence")
        if conf not in CONF:
            err(f"{name}: {fid} bad date confidence {conf}")
        if f.get("layer") and f["layer"] not in layers:
            err(f"{name}: {fid} references unknown layer {f['layer']}")
        is_ref = "reference" in (f.get("tags") or [])
        if not is_ref and not f.get("sources"):
            err(f"{name}: {fid} has no sources")
        if f.get("sources"):
            n_src += 1
    print(f"OK counts {name}: {len(feats)} features ({n_src} sourced), "
          f"{len(data.get('routes', []))} routes, {len(layers)} layers")

sys.exit(1 if fail else 0)
