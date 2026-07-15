#!/usr/bin/env python3
"""QA sweep: internal link/asset integrity + DB deep-link validity + page basics."""
import json, re, os, glob, csv, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fail = 0
def err(m):
    global fail; fail += 1; print("FAIL:", m)

# 1. every internal href/src in every html resolves to a file
for page in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    rel = os.path.relpath(page, ROOT)
    html = open(page).read()
    html = re.sub(r"<script[\s\S]*?</script>", "", html)  # skip JS template strings
    base = os.path.dirname(page)
    for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
        u = m.group(1)
        if u.startswith(("http", "#", "mailto:", "data:")) or u == "":
            continue
        u = u.split("#")[0].split("?")[0]
        if not u:
            continue
        if u.startswith("/california-history-maps/"):  # Pages site-root absolute
            target = os.path.normpath(os.path.join(ROOT, u[len("/california-history-maps/"):]) or ROOT)
            if u.endswith("/"): target = os.path.join(target, "index.html") if os.path.isdir(target) else target
        else:
            target = os.path.normpath(os.path.join(base, u))
        if os.path.isdir(target) and os.path.exists(os.path.join(target, "index.html")):
            continue
        if not os.path.exists(target):
            err(f"{rel}: broken link {u}")

# 2. ca_record deep links exist in the archive catalog
ids = set()
with open(os.path.expanduser("~/archives-of-california/ca-catalog-export.csv"), encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        ids.add(f"ca{row['ca_volume']}-d{row['doc_id']}")
n_links = 0
for p in glob.glob(os.path.join(ROOT, "data", "*.json")):
    d = json.load(open(p))
    feats = list(d.get("features", []))
    for r in d.get("routes", []):
        feats.extend(r.get("stops", []))
    for f in feats:
        for s in (f.get("sources") or []):
            if s.get("ca_record"):
                n_links += 1
                if s["ca_record"] not in ids:
                    err(f"{os.path.basename(p)}: {f['id']} dead deep link {s['ca_record']}")
print(f"deep links checked: {n_links}")

# 3. every map shell's data file exists; every data map has a shell + landing card
index = open(os.path.join(ROOT, "index.html")).read()
for shell in glob.glob(os.path.join(ROOT, "maps", "*.html")):
    mid = re.search(r'data-map="([^"]+)"', open(shell).read())
    if not mid:
        err(f"{shell}: no data-map attr"); continue
    if not os.path.exists(os.path.join(ROOT, "data", mid.group(1) + ".json")):
        err(f"{shell}: missing data file {mid.group(1)}.json")
for p in glob.glob(os.path.join(ROOT, "data", "*.json")):
    d = json.load(open(p))
    if "id" not in d or "features" not in d:
        continue
    if not os.path.exists(os.path.join(ROOT, "maps", d["id"] + ".html")):
        err(f"{d['id']}: no shell page")
    if d["id"] + ".html" not in index:
        err(f"{d['id']}: no landing card")
    if f'"{d["id"]}"' not in index:
        err(f"{d['id']}: missing from landing stats array")
    if not os.path.exists(os.path.join(ROOT, "assets", "previews", d["id"] + ".jpg")):
        err(f"{d['id']}: missing preview")
    if not os.path.exists(os.path.join(ROOT, "downloads", d["id"] + ".geojson")):
        err(f"{d['id']}: missing geojson download")

# 4. gallery integrity: every item's img + thumb exist; every img/thumb is listed
g = json.load(open(os.path.join(ROOT, "gallery", "gallery-data.json")))
listed = set()
for it in g["items"]:
    listed.add(it["file"])
    for sub in ("img", "thumb"):
        if not os.path.exists(os.path.join(ROOT, "gallery", sub, it["file"])):
            err(f"gallery {sub} missing: {it['file']}")
for sub in ("img", "thumb"):
    for f in os.listdir(os.path.join(ROOT, "gallery", sub)):
        if f.endswith(".jpg") and f not in listed:
            err(f"gallery orphan {sub}/{f}")
print(f"gallery items: {len(g['items'])}")

# 5. page head basics
for page in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    rel = os.path.relpath(page, ROOT)
    if rel.startswith(("california-military", "borderlands", "moraga-exped", "zalvidea")):
        continue  # redirect stubs
    h = open(page).read()
    if "<title>" not in h: err(f"{rel}: no title")
    if 'name="viewport"' not in h and "404" not in rel: err(f"{rel}: no viewport meta")

print("QA:", "FAIL " + str(fail) if fail else "ALL GREEN")
sys.exit(1 if fail else 0)
