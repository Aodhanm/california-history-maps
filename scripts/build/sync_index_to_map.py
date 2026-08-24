#!/usr/bin/env python3
"""Reconcile the searchable rancho index with the map (the source of truth).

The map (data/ranchos-experimental.json) holds the vetted grant facts. The
searchable index (gallery/ranchos-index.json) is a superset that also lists
boundary-less grants. For every grant that IS on the map, this copies the
grant facts (governor, year, grantee, acres, outcome) from the map feature
onto the matching index row, keyed by id, so the two can never disagree.

It only ever overwrites a field when the map has a real value for it, so
nothing gets blanked (e.g. presidios keep their index text). It never touches
the boundary-less rows, the diseño links, names, counties, land cases, or ids,
and it aborts without writing if any of those protected fields would change.

Usage:
    python3 scripts/build/sync_index_to_map.py [--dry-run]
"""
import json, re, copy, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "data" / "ranchos-experimental.json"
IDX = ROOT / "gallery" / "ranchos-index.json"

SYNC = ("governor", "year", "grantee", "acres", "outcome")
PROTECT = ("name", "kind", "county", "land_case", "mapped", "id", "dz_imgs", "dz_n")


def nz(v):
    return v not in (None, "", [], "None") and str(v).strip() != "" and str(v).strip().lower() != "none"


def map_year(f):
    m = re.search(r"(1[78]\d\d)", str((f.get("date") or {}).get("iso") or ""))
    return m.group(1) if m else None


def main(dry_run=False):
    idx = json.loads(IDX.read_text())
    before = copy.deepcopy(idx)
    rows = idx["rows"]
    feats = {f["id"]: f for f in json.loads(MAP.read_text())["features"]}

    synced = 0
    for r in rows:
        if not r.get("mapped"):
            continue
        f = feats.get(r.get("id"))
        if not f:
            continue
        changed = False
        mg = f.get("governor_name")
        if nz(mg) and str(r.get("governor") or "") != str(mg):
            r["governor"] = mg; changed = True
        my = map_year(f)
        if my and str(r.get("year") or "") != my:
            r["year"] = my; changed = True
        mgr = f.get("grantee")
        if nz(mgr) and str(r.get("grantee") or "") != str(mgr):
            r["grantee"] = mgr; changed = True
        ma = f.get("acres")
        if isinstance(ma, (int, float)) and ma and str(r.get("acres") or "") != str(int(round(ma))):
            r["acres"] = int(round(ma)); changed = True
        mo = f.get("outcome")
        if nz(mo) and str(r.get("outcome") or "") != str(mo):
            r["outcome"] = mo; changed = True
        if changed:
            synced += 1

    idx["confirmed"] = sum(1 for r in rows if r.get("outcome") == "Confirmed")
    idx["rejected"] = sum(1 for r in rows if r.get("outcome") == "Rejected")
    idx["updated"] = datetime.date.today().isoformat()

    # ---- integrity guards: abort rather than corrupt the index ----
    errs = []
    if len(rows) != len(before["rows"]):
        errs.append(f"row count changed {len(before['rows'])} -> {len(rows)}")
    dz_b = sum(len(r.get("dz_imgs") or []) for r in before["rows"])
    dz_a = sum(len(r.get("dz_imgs") or []) for r in rows)
    if dz_b != dz_a:
        errs.append(f"diseño image total changed {dz_b} -> {dz_a}")
    for rb, ra in zip(before["rows"], rows):
        if rb.get("id") != ra.get("id") or rb.get("name") != ra.get("name"):
            errs.append(f"row identity/order changed near {rb.get('name')}"); break
        for k in PROTECT:
            if rb.get(k) != ra.get(k):
                errs.append(f"PROTECTED field '{k}' changed on {rb.get('name')}")
        if not rb.get("mapped"):
            if rb != ra:
                errs.append(f"boundary-less row changed: {rb.get('name')}")
        else:
            for k in rb:
                if k not in SYNC and rb.get(k) != ra.get(k):
                    errs.append(f"unexpected change on mapped row {rb.get('name')} field '{k}'")
    if errs:
        print("ABORTED — integrity checks failed:")
        for e in errs[:20]:
            print("  ", e)
        sys.exit(1)

    print(f"rows synced: {synced} | total {len(rows)} | diseño imgs {dz_a} (unchanged) | "
          f"confirmed {idx['confirmed']} rejected {idx['rejected']}")
    if dry_run:
        print("dry run — nothing written")
        return
    IDX.write_text(json.dumps(idx, ensure_ascii=False, separators=(", ", ": ")))
    print(f"wrote {IDX.relative_to(ROOT)}")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
