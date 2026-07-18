#!/usr/bin/env python3
"""Build data/peoples.json — the Native peoples index — from all map datasets.

Design (how it decides what to list):
- NATIONS: every distinct Native nation with a territory on the Native California
  map is listed, using that map's own `summary` as its blurb and linking to its
  polygon. Nations that also ACT in mapped events (curated entries in the prior
  hand-built index) keep their richer blurb and all their cross-map event pins,
  and are shown FIRST as "featured". Multiple polygon pieces of one nation
  ("... (detached area)") collapse to a single entry. Name variants are merged
  (e.g. map "Mohave" == curated "Mojave (Amajava)").
- LEADERS (people): kept exactly as curated. Named individuals live in event
  prose, not a structured field, so they are curated by hand — auto-extraction
  would produce garbage. This script never invents people.

Idempotent: re-run whenever the datasets change. Preserves the curated blurbs
and pins already in data/peoples.json.
"""
import json, glob, os, re

REPO = os.path.expanduser("~/california-history-maps")
os.chdir(REPO)

# ---- load datasets ----
DATA = {}
for fn in glob.glob("data/*.json"):
    key = os.path.basename(fn)[:-5]
    if key == "peoples":
        continue
    d = json.load(open(fn))
    feats = d["features"] if isinstance(d, dict) and "features" in d else d
    title = d.get("title", key) if isinstance(d, dict) else key
    DATA[key] = {"title": title, "feats": feats}

# ---- preserve curated index ----
cur = json.load(open("data/peoples.json"))
curated_people = [p for p in cur.get("people", []) if not p.get("auto")]
# only HAND-curated nations count as the base (idempotent: skip prior auto roster)
curated_nations = [n for n in cur.get("nations", []) if not n.get("auto")]
curated_order = [n["name"] for n in curated_nations]           # keep their order
nations = {n["name"]: json.loads(json.dumps(n)) for n in curated_nations}  # deep copy

def has_pin(entry, mapkey, pid):
    return any(p["map"] == mapkey and p["id"] == pid for p in entry["pins"])

# map "Native California" polygon name -> curated nation name (variant reconciliation)
VARIANT = {
    "Mohave": "Mojave (Amajava)",
    "Quechan": "Quechan (Yuma)",
    "Ipai (Kumeyaay)": "Kumeyaay",
    "Tipai (Kumeyaay)": "Kumeyaay",
}

def canon(name):
    return re.sub(r"\s*\(detached area\)\s*$", "", name).strip()

# ---- build nation roster from Native California polygons ----
nc = DATA["native-california"]
poly_by_canon = {}   # canonical name -> {summary, ids[]}
for f in nc["feats"]:
    if f.get("label_only"):
        continue
    c = canon(f["name"])
    slot = poly_by_canon.setdefault(c, {"summary": "", "ids": [], "detached_only": True})
    slot["ids"].append(f["id"])
    if "(detached area)" not in f["name"]:
        slot["summary"] = f.get("summary", "") or slot["summary"]
        slot["detached_only"] = False
    elif not slot["summary"]:
        slot["summary"] = f.get("summary", "") or ""

for c, slot in poly_by_canon.items():
    target = VARIANT.get(c, c)
    pin = {"map": "native-california", "map_title": nc["title"],
           "id": slot["ids"][0], "name": f"{target} territory"}
    if target in nations:                       # merge into curated entry
        if not has_pin(nations[target], "native-california", pin["id"]):
            nations[target]["pins"].append(pin)
    else:                                       # new roster entry (auto-generated)
        nations[c] = {"name": c, "blurb": slot["summary"] or
                      "A Native nation of California; territory shown on the Native California map.",
                      "pins": [pin], "auto": True}

# ---- add real event pins via the structured native_groups field (sparse but exact) ----
GROUP_TO_NATION = {
    "Kumeyaay": "Kumeyaay", "Cahuilla": "Cahuilla",
    "Quechan (Yuma)": "Quechan (Yuma)",
    "Chaguanoso (mixed raiding bands)": "Chaguanoso raiders",
    "Unangan/Alutiiq (Aleut) hunters": "Unangan & Alutiiq (Aleut) hunters",
}
for key, ds in DATA.items():
    if key == "native-california":
        continue
    for f in ds["feats"]:
        groups = f.get("native_groups")
        if isinstance(groups, str):
            groups = [groups]
        for g in (groups or []):
            nat = GROUP_TO_NATION.get(g)
            if nat and nat in nations and not has_pin(nations[nat], key, f["id"]):
                nations[nat]["pins"].append(
                    {"map": key, "map_title": ds["title"], "id": f["id"], "name": f.get("name", "")})

# ---- order: featured (curated OR acts off the native map) first, then roster A-Z ----
def is_featured(entry):
    return entry["name"] in curated_order or any(p["map"] != "native-california" for p in entry["pins"])

featured = [nations[n] for n in curated_order if n in nations]                 # curated order first
seen = {e["name"] for e in featured}
extra_featured = sorted((e for n, e in nations.items()
                         if n not in seen and is_featured(e)), key=lambda e: e["name"])
roster = sorted((e for n, e in nations.items()
                 if n not in seen and not is_featured(e)), key=lambda e: e["name"])
ordered = featured + extra_featured + roster

# ---- validate every pin: remap stale ids by name, drop the unrecoverable ----
# (the hand-built index carried route-stop ids that changed when maps were rebuilt)
id_sets = {k: set(f.get("id") for f in ds["feats"]) for k, ds in DATA.items()}
name_index = {}   # map -> {normalized name: id}
for k, ds in DATA.items():
    name_index[k] = {}
    for f in ds["feats"]:
        nm = (f.get("name") or "").strip().lower()
        if nm:
            name_index[k].setdefault(nm, f["id"])

def fix_pins(entries):
    dropped = 0
    for e in entries:
        good = []
        for pin in e["pins"]:
            m = pin["map"]
            if pin["id"] in id_sets.get(m, set()):
                good.append(pin)
            else:
                alt = name_index.get(m, {}).get((pin.get("name") or "").strip().lower())
                if alt:
                    pin["id"] = alt
                    good.append(pin)
                else:
                    dropped += 1
        e["pins"] = good
    return dropped

dropped = fix_pins(ordered) + fix_pins(curated_people)

out = {"updated": "2026-07-17", "people": curated_people, "nations": ordered}
json.dump(out, open("data/peoples.json", "w"), indent=1, ensure_ascii=False)
print(f"people (curated): {len(curated_people)}")
print(f"nations: {len(ordered)}  (featured {len(featured)+len(extra_featured)} + roster {len(roster)})")
print(f"total pins on nations: {sum(len(n['pins']) for n in ordered)}")
print(f"stale pins dropped (unrecoverable): {dropped}")
