#!/usr/bin/env python3
"""Post-process native-california.json (run AFTER build_native_poly.py):
1. add the Subgroups labels layer (default off)
2. apply the refined Carquinez edit: Karkin (Ohlone) strip on the north shore of the
   strait only — Crockett to Benicia, ~2 miles inland (to 38.09 N), NOT all of Vallejo.
Idempotent pipeline: rebuild + rerun this to regenerate the map from scratch."""
import json, os, re, unicodedata

p = os.path.expanduser("~/california-history-maps/data/native-california.json")
d = json.load(open(p))

def slug(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

CITE = ("Subgroup names and approximate locations after the Handbook of North American Indians, "
        "vol. 8 (1978) chapters and standard references; label positions approximate, no boundaries implied.")

SUBS = [
 ("Karkin", "Ohlone", [38.06, -122.18], "The Ohlone people of the Carquinez Strait, shown here holding both shores of the narrows, a coastal strip from Crockett past Benicia. Mission-era records write them as Carquin; the strait keeps their name."),
 ("Ramaytush", "Ohlone", [37.72, -122.44], "The San Francisco peninsula Ohlone; the people of Mission Dolores' home shore."),
 ("Chochenyo", "Ohlone", [37.70, -122.05], "The East Bay Ohlone, from the Oakland shore to Mission San José's country."),
 ("Tamyen", "Ohlone", [37.32, -121.90], "The Santa Clara Valley Ohlone, around Mission Santa Clara and the pueblo of San José."),
 ("Awaswas", "Ohlone", [37.00, -122.05], "The Santa Cruz coast Ohlone."),
 ("Mutsun", "Ohlone", [36.85, -121.55], "The San Juan Bautista country Ohlone; their language is among the best documented."),
 ("Rumsen", "Ohlone", [36.55, -121.90], "The Monterey and Carmel Ohlone; the people the Portolá expedition and Mission San Carlos met first."),
 ("Chalon", "Ohlone", [36.55, -121.20], "The inland Ohlone of the upper Salinas tributaries, toward Soledad."),
 ("Kashaya", "Pomo", [38.58, -123.30], "The southwestern Pomo of the Fort Ross coast; the people on whose land the Russian colony was built."),
 ("Southern Pomo", "Pomo", [38.45, -122.95], "The lower Russian River country."),
 ("Central Pomo", "Pomo", [39.00, -123.35], "The coast and river country around Point Arena and Hopland."),
 ("Northern Pomo", "Pomo", [39.40, -123.35], "The upper Russian River and the Willits country."),
 ("Eastern Pomo", "Pomo", [39.05, -122.90], "The western Clear Lake shore."),
 ("Southeastern Pomo", "Pomo", [39.00, -122.65], "The island towns of eastern Clear Lake."),
 ("Olamentko (Bodega Miwok)", "Coast Miwok", [38.335, -123.00], "The Coast Miwok of Bodega Bay itself; the communities the 1775 and 1793 Spanish expeditions and the Russians at Port Rumiantsev all dealt with."),
 ("Lekahtewutko (Marin Miwok)", "Coast Miwok", [38.05, -122.70], "The Coast Miwok of the Marin peninsula and Tomales Bay."),
 ("Suisun", "Patwin", [38.25, -122.00], "The southern Patwin of the Suisun plain; Moraga's 1810 campaign and Chief Solano's later prominence made them the best-recorded Patwin community."),
 ("Napa Patwin", "Patwin", [38.22, -122.29], "The southern Patwin of the lower Napa Valley."),
 ("Northern Sierra Miwok", "Eastern Miwok", [38.30, -120.65], "The Mokelumne and Calaveras high country."),
 ("Central Sierra Miwok", "Eastern Miwok", [37.95, -120.30], "The Stanislaus and Tuolumne foothills; the Southern Mines country of the Gold Rush."),
 ("Southern Sierra Miwok", "Eastern Miwok", [37.55, -119.95], "The Merced and Mariposa country toward Yosemite."),
 ("Tachi", "Yokuts", [36.15, -119.85], "Southern Valley Yokuts of the Tulare Lake shore; frequent in the mission-era expedition records."),
 ("Chowchilla", "Yokuts", [37.15, -120.25], "Northern Valley Yokuts of the Chowchilla River; their name marks the river and town."),
 ("Chunut", "Yokuts", [36.05, -119.60], "Southern Valley Yokuts of Tulare Lake's eastern shore."),
 ("Yauelmani", "Yokuts", [35.55, -119.20], "Southern Valley Yokuts of the Kern delta country."),
 ("Obispeño", "Chumash", [35.28, -120.66], "The northernmost Chumash, around San Luis Obispo."),
 ("Purisimeño", "Chumash", [34.67, -120.45], "The Chumash of the Lompoc country around Mission La Purísima."),
 ("Ineseño (Samala)", "Chumash", [34.60, -120.10], "The Chumash of the Santa Ynez Valley; Samala is the community's own name."),
 ("Barbareño", "Chumash", [34.43, -119.70], "The Chumash of the Santa Barbara coast."),
 ("Ventureño", "Chumash", [34.30, -119.20], "The Chumash of the Ventura River and coast."),
 ("Island Chumash", "Chumash", [34.00, -119.75], "The Chumash of Santa Cruz, Santa Rosa, and San Miguel islands, removed to the mainland missions by the 1820s."),
 ("Mountain Cahuilla", "Cahuilla", [33.55, -116.60], "The San Jacinto and Santa Rosa mountain villages."),
 ("Desert Cahuilla", "Cahuilla", [33.55, -116.10], "The Coachella Valley and the wells of the desert floor."),
 ("Pass Cahuilla", "Cahuilla", [33.90, -116.80], "The San Gorgonio Pass villages."),
]

feats = d["features"]
for label, parent, coords, blurb in SUBS:
    feats.append({
        "id": "sub-" + slug(label), "register_no": None,
        "name": label + " (" + parent + ")",
        "date": {"iso": None, "display": "", "confidence": "exact"},
        "coords": coords, "coord_precision": "area", "label_only": True,
        "type": "event", "layer": "subgroups",
        "summary": blurb, "result": "", "quote": None,
        "sources": [{"citation": CITE, "ca_record": None, "ia_leaf_url": None}],
        "native_groups": [], "tags": [],
        "notes": "A label, not a boundary: the position is an approximate center within the parent nation's territory."})

d["layers"].append({"id": "subgroups", "label": "Subgroups & communities (labels)",
                    "color": "#4a4238", "default_off": True})

# ── refined Carquinez edit ──
# Karkin coastal strip: north shore of the strait, Crockett (-122.30) to past Benicia
# (-122.05), up to 38.09 N (~2 miles inland). Vallejo proper stays Patwin.
W, E, TOP = -122.30, -122.05, 38.09
oh = pa = 0
for f in feats:
    if f["id"] == "t-ohlone-costanoan":
        for ring in f.get("polygon", []):
            for v in ring:
                if 37.92 <= v[0] < TOP and W <= v[1] <= E:
                    v[0] = TOP; oh += 1
        f["summary"] = (f.get("summary", "") + " Shown here holding both shores of Carquinez "
                        "Strait through the Karkin: a coastal strip about two miles deep on the "
                        "north shore, from Crockett past Benicia. An editorial departure from the "
                        "Handbook plate, which ends Costanoan territory at the south shore.").strip()
        f["notes"] = (f.get("notes", "") + " Editorial deviation at Carquinez, drawn and flagged; "
                      "Vallejo and the Napa plain remain Patwin.").strip()
    if f["id"] == "t-patwin":
        for ring in f.get("polygon", []):
            for v in ring:
                if v[0] < TOP and W <= v[1] <= E:
                    v[0] = TOP; pa += 1
        f["notes"] = (f.get("notes", "") + " Editorial deviation: a coastal strip on the strait's "
                      "north shore (Crockett to Benicia, to about two miles inland) is assigned to "
                      "the Karkin (Ohlone); Vallejo and the Suisun plain remain Patwin.").strip()
# dedupe consecutive identical vertices
for f in feats:
    for ri, ring in enumerate(f.get("polygon", []) or []):
        out = [ring[0]]
        for v in ring[1:]:
            if v != out[-1]:
                out.append(v)
        f["polygon"][ri] = out

d["abstract"] += (" A toggleable Subgroups layer adds the prominent regional communities and "
                  "languages within the larger nations; these are labels at approximate centers, "
                  "not bounded territories. One editorial deviation from the Handbook plate is "
                  "drawn and flagged: the Karkin (Ohlone) are shown holding a coastal strip on "
                  "both shores of Carquinez Strait.")
json.dump(d, open(p, "w"), ensure_ascii=False)
print("subgroups:", len(SUBS), "| carquinez raised — ohlone:", oh, "patwin:", pa,
      "| features:", len(feats))
