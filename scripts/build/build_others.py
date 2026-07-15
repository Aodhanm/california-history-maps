#!/usr/bin/env python3
# ARCHIVAL/one-time or session-built script, kept for provenance and reproducibility.
# Paths referencing the original session scratchpad will need adjusting to rerun.
"""Build borderlands-frontier, moraga-expeditions, zalvidea-moraga-1806 JSONs from drafts."""
import json, re, os, unicodedata

SCRATCH = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.expanduser("~/california-history-maps")
MONTHS = {m: i for i, m in enumerate(
    "january february march april may june july august september october november december".split(), 1)}

def slug(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:48].rstrip("-")

def parse_date(disp):
    d = (disp or "").strip()
    m = re.match(r"^([A-Za-z]+)\s+(\d{1,2})(?:[–-]\d+)?,\s*(\d{4})$", d)
    if m and m.group(1).lower() in MONTHS:
        return ("%s-%02d-%02d" % (m.group(3), MONTHS[m.group(1).lower()], int(m.group(2))), "exact")
    m = re.match(r"^([A-Za-z]+)\s+(\d{4})$", d)
    if m and m.group(1).lower() in MONTHS:
        return ("%s-%02d" % (m.group(2), MONTHS[m.group(1).lower()]), "month")
    if re.match(r"^\d{4}$", d):
        return (d, "year")
    m = re.search(r"(\d{4})", d)
    if m:
        return (m.group(1), "range" if re.search(r"[–—-]|/", d) else "circa")
    return (None, "circa")

def spanishish(s):
    return bool(re.search(r"[áéíóúñ¿¡]", s))

def mkfeat(fid, name, disp, coords, prec, typ, layer, summary, result="", quote_raw="",
           source_raw="", note="", tags=None, seen=None):
    iso, conf = parse_date(disp)
    quote = None
    if quote_raw and quote_raw.strip():
        q = quote_raw.strip()
        quote = {"es": q, "en": "", "source": ""} if spanishish(q) else {"es": "", "en": q, "source": ""}
    base = fid; n = 2
    while fid in seen:
        fid = f"{base}-{n}"; n += 1
    seen.add(fid)
    return {
        "id": fid, "register_no": None, "name": name,
        "date": {"iso": iso, "display": disp or "", "confidence": conf},
        "coords": coords, "coord_precision": prec, "type": typ, "layer": layer,
        "summary": summary or "", "result": result or "", "quote": quote,
        "sources": [{"citation": source_raw.strip(), "ca_record": None, "ia_leaf_url": None}] if source_raw and source_raw.strip() else [],
        "native_groups": [], "tags": tags or [], "notes": note or ""
    }

# ══════════ 1. BORDERLANDS ══════════
d = json.load(open(f"{SCRATCH}/extracted/borderlands-frontier.draft.json"))
seen = set()
# layer meta verified against the source file's section comments:
LAYERS = [
    {"id": "spanMil", "label": "Spanish Military Expeditions", "color": "#2e6f40"},
    {"id": "british", "label": "British Naval & Military", "color": "#c0392b"},
    {"id": "russian", "label": "Russian Naval & Hunting", "color": "#2980b9"},
    {"id": "american", "label": "American Encounters", "color": "#1a5276"},
    {"id": "bouchard", "label": "Bouchard Raid (1818)", "color": "#e67e22"},
    {"id": "french", "label": "French Visits", "color": "#7d3c98"},
    {"id": "indigenous", "label": "Indigenous Agency", "color": "#d4ac0d"},
    {"id": "intel", "label": "Intelligence & Defense Decay", "color": "#8e44ad"},
    {"id": "spanSet", "label": "Spanish/Mexican Settlements (reference)", "color": "#6b6257"},
    {"id": "rusSet", "label": "Russian Settlements (reference)", "color": "#1B4F72"},
    {"id": "modern", "label": "Modern City Labels", "color": "#9a938a"},
]
known = {l["id"] for l in LAYERS}
feats = []
missing_layers = set()
for f in d["features"]:
    ly = f["layer_var"]
    if ly not in known:
        missing_layers.add(ly)
    feats.append(mkfeat(
        slug(f["name"]), f["name"], f["date_display"], f["coords"], "place",
        "event", ly, f["summary"], f["result"], f["quote_raw"], f["source_raw"], seen=seen))
# reference arrays: re-extract ALL of them (Phase-0 draft only had 3 of 7)
import importlib
srcb = open(os.path.expanduser("~/california-history-maps/borderlands-imperial-frontier.html")).read()
def jsarr(name):
    m = re.search(r"const\s+" + name + r"\s*=\s*(\[[^;]*?\]);", srcb, re.S)
    if not m: return []
    t = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', m.group(1))
    t = re.sub(r",\s*([\]}])", r"\1", t)
    return json.loads(t)
REF_ARRS = (("presidios", "presidio", "spanSet"), ("missions", "mission", "spanSet"),
            ("pueblos", "settlement", "spanSet"), ("outposts", "settlement", "spanSet"),
            ("ranchos", "settlement", "spanSet"), ("rusSettlements", "settlement", "rusSet"),
            ("modernLabels", "settlement", "modern"))
for arr, typ, layer in REF_ARRS:
    for r in jsarr(arr):
        pref = "label-" if layer == "modern" else "ref-"
        feats.append(mkfeat(pref + slug(r["name"]), r["name"], "", [r["lat"], r["lng"]],
                            "exact", typ, layer, r.get("note", ""), tags=["reference"], seen=seen))
print("borderlands unknown layer vars:", missing_layers)
out = {
    "id": "borderlands-frontier",
    "title": "The Bay Area Imperial Frontier",
    "subtitle": "Spain, Russia, Britain, and Native polities north of San Francisco Bay, 1775–1841",
    "abstract": ("Spain's northern frontier as a contested borderland: Spanish expeditions and "
                 "defensive works, Russian hunting and Fort Ross, British and American visits, and the "
                 "Native peoples whose knowledge and choices shaped all of it. Compiled from the C-A "
                 "transcripts, Wagner, and the printed voyage accounts."),
    "date_range": [1775, 1841], "center": [38.15, -122.6], "zoom": 8,
    "cite_key": "borderlands", "last_updated": "2026-07-14",
    "layers": LAYERS, "features": feats
}
json.dump(out, open(f"{REPO}/data/borderlands-frontier.json", "w"), indent=1, ensure_ascii=False)
print("borderlands:", len(feats))

# ══════════ 2. MORAGA MASTER ══════════
d = json.load(open(f"{SCRATCH}/extracted/moraga-expeditions.draft.json"))
seen = set()
ROUTE_META = {
    "r1807": ("Moraga 1807 — San Joaquin Reconnaissance", "#b7791f", "reconstructed"),
    "r1810a": ("Viader–Moraga August 1810 (Delta)", "#275d7a", "reconstructed"),
    "r1810b": ("Viader–Moraga October 1810", "#16a085", "reconstructed"),
    "rSuisun": ("Moraga May 1810 — Suisun Campaign", "#c0392b", "reconstructed"),
    "rBodega": ("Moraga October 1810 — Bodega Reconnaissance", "#8e44ad", "reconstructed"),
    "rRoss1812": ("Moraga 1812 — First Visit to Ross", "#8B2500", "reconstructed"),
    "rRoss1813": ("Moraga 1813 — Second Ross Mission", "#e67e22", "reconstructed"),
    "rSanRafael": ("Moraga 1817 — San Rafael Founding Escort", "#2e6f40", "reconstructed"),
}
layers = [{"id": k, "label": v[0], "color": v[1]} for k, v in ROUTE_META.items()]
layers.append({"id": "refs", "label": "Missions (reference)", "color": "#6b6257"})
layers.append({"id": "modern", "label": "Modern City Labels", "color": "#9a938a"})
routes = []
for rid, (label, color, confc) in ROUTE_META.items():
    stops_raw = d["object_arrays"].get(rid) or []
    stops = []
    for s in stops_raw:
        stops.append(mkfeat(
            f"{slug(rid)}-{s.get('n', len(stops)+1)}-{slug(s['name'])}",
            s["name"], "", [s["lat"], s["lng"]],
            "area", s.get("type", "expedition-leg"), rid,
            s.get("d", s.get("detail", "")), "", s.get("q", ""), s.get("c", ""), seen=seen))
    # route-level citation = the most common stop citation (stops without their own inherit it)
    from collections import Counter
    cites = Counter(s["sources"][0]["citation"] for s in stops if s["sources"])
    routes.append({"id": slug(rid), "label": label, "layer": rid, "color": color,
                   "path_confidence": confc,
                   "citation": cites.most_common(1)[0][0] if cites else "",
                   "stops": stops})
feats = []
for r in d["object_arrays"].get("missions") or []:
    feats.append(mkfeat("ref-" + slug(r["name"]), r["name"], "", [r["lat"], r["lng"]],
                        "exact", "mission", "refs", r.get("note", ""), tags=["reference"], seen=seen))
for r in d["object_arrays"].get("modernLabels") or []:
    feats.append(mkfeat("label-" + slug(r["name"]), r["name"], "", [r["lat"], r["lng"]],
                        "exact", "settlement", "modern", "", tags=["reference"], seen=seen))
for r in d["object_arrays"].get("villages") or []:
    feats.append(mkfeat("village-" + slug(r["name"]), r["name"], "", [r["lat"], r["lng"]],
                        "area", "settlement", "refs",
                        (("Population " + r["pop"] + ". ") if r.get("pop") else "") + r.get("note", ""),
                        source_raw="Muñoz diary / Cook, Colonial Expeditions (village locations approximate)",
                        seen=seen))
out = {
    "id": "moraga-expeditions",
    "title": "Gabriel Moraga's Expeditions",
    "subtitle": "Interior and northern reconnaissance, 1806–1817",
    "abstract": ("All of Gabriel Moraga's documented expeditions on one map: the 1806–07 interior "
                 "reconnaissances, the 1810 Suisun and Bodega operations, the 1812–13 Ross missions, and "
                 "the 1817 San Rafael founding escort. Routes are RECONSTRUCTED from diaries and reports — "
                 "dashed lines mean 'he passed roughly this way,' not a surveyed track. Village locations "
                 "follow Cook's identifications and are approximate."),
    "date_range": [1806, 1817], "center": [37.9, -121.5], "zoom": 7,
    "cite_key": "moraga", "last_updated": "2026-07-14",
    "layers": layers, "features": feats, "routes": routes
}
json.dump(out, open(f"{REPO}/data/moraga-expeditions.json", "w"), indent=1, ensure_ascii=False)
print("moraga:", len(feats), "features,", len(routes), "routes,", sum(len(r['stops']) for r in routes), "stops")

# ══════════ 3. ZALVIDEA-MORAGA 1806 ══════════
d = json.load(open(f"{SCRATCH}/extracted/zalvidea-moraga-1806.draft.json"))
seen = set()
R = {
    "zalvideaStops": ("zalvidea", "Zalvidea Expedition (Jul–Aug 1806)", "#b87333"),
    "moragaNorthStops": ("moraga-north", "Moraga — Northbound (Sep–Oct 1806)", "#8B2500"),
    "moragaSouthStops": ("moraga-south", "Moraga — Southbound Return (Oct–Nov 1806)", "#1a5276"),
}
layers = [{"id": rid, "label": lab, "color": col} for (rid, lab, col) in R.values()]
layers += [{"id": "refs", "label": "Missions (reference)", "color": "#6b6257"},
           {"id": "villages", "label": "Native Villages (per Cook)", "color": "#16a085"},
           {"id": "modern", "label": "Modern City Labels", "color": "#9a938a"}]
routes = []
for arr, (rid, label, color) in R.items():
    stops = []
    for s in d["object_arrays"].get(arr) or []:
        note = s.get("note", "")
        stops.append(mkfeat(
            f"{rid}-{s.get('n', len(stops)+1)}-{slug(s['name'])}",
            s["name"], "", [s["lat"], s["lng"]], "area", "expedition-leg", rid,
            s.get("detail", ""), "", "",
            "Muñoz/Zalvidea diaries via Cook, Colonial Expeditions" + (f" ({note})" if note else ""),
            seen=seen))
    from collections import Counter
    cites = Counter(s["sources"][0]["citation"] for s in stops if s["sources"])
    routes.append({"id": rid, "label": label, "layer": rid, "color": color,
                   "path_confidence": "reconstructed",
                   "citation": cites.most_common(1)[0][0] if cites else
                               "Muñoz/Zalvidea diaries via Cook, Colonial Expeditions",
                   "stops": stops})
feats = []
for r in d["object_arrays"].get("missions") or []:
    feats.append(mkfeat("ref-" + slug(r["name"]), r["name"], "", [r["lat"], r["lng"]],
                        "exact", "mission", "refs", r.get("note", ""), tags=["reference"], seen=seen))
for r in d["object_arrays"].get("villages") or []:
    feats.append(mkfeat("village-" + slug(r["name"]), r["name"], "", [r["lat"], r["lng"]],
                        "area", "settlement", "villages", r.get("note", ""),
                        source_raw="Cook, Colonial Expeditions (village identifications approximate)", seen=seen))
for r in d["object_arrays"].get("modernLabels") or []:
    feats.append(mkfeat("label-" + slug(r["name"]), r["name"], "", [r["lat"], r["lng"]],
                        "exact", "settlement", "modern", "", tags=["reference"], seen=seen))
out = {
    "id": "zalvidea-moraga-1806",
    "title": "The 1806 Interior Expeditions — Zalvidea & Moraga",
    "subtitle": "Two probes into the Central Valley, July–November 1806",
    "abstract": ("The 1806 expeditions of Fr. José María de Zalvidea (Santa Ynez to San Gabriel through "
                 "the southern valley) and Gabriel Moraga with Fr. Pedro Muñoz (San Juan Bautista through "
                 "the San Joaquin Valley), stop by stop from the diaries as identified by Cook. Routes are "
                 "reconstructed; village locations approximate."),
    "date_range": [1806, 1806], "center": [35.6, -119.6], "zoom": 7,
    "cite_key": "1806", "last_updated": "2026-07-14",
    "layers": layers, "features": feats, "routes": routes
}
json.dump(out, open(f"{REPO}/data/zalvidea-moraga-1806.json", "w"), indent=1, ensure_ascii=False)
print("zalvidea:", len(feats), "features,", sum(len(r['stops']) for r in routes), "stops")
