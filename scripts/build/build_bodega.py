#!/usr/bin/env python3
# ARCHIVAL/one-time or session-built script, kept for provenance and reproducibility.
# Paths referencing the original session scratchpad will need adjusting to rerun.
"""Build data/bodega-ross-corridor.json — the Open Door article's companion map.

Strategy: reuse verified features from the live datasets (borderlands, moraga,
presidial) so every claim keeps its existing citation; retag into corridor layers;
add only a handful of new features with clean C-A record links. No claim may
exceed the referee-stress-tested prewrites (e.g. Racoon = 1814, not 1812)."""
import json, os, copy

REPO = os.path.expanduser("~/california-history-maps")
def load(name):
    return json.load(open(os.path.join(REPO, "data", name)))

border = load("borderlands-frontier.json")
moraga = load("moraga-expeditions.json")
presidial = load("presidial-system.json")

LAYERS = [
    {"id": "spanish", "label": "Spanish Surveys & the 1793 Attempt", "color": "#7a2e2e"},
    {"id": "russian", "label": "The Russians at Bodega & Ross", "color": "#8e44ad"},
    {"id": "overland", "label": "Spanish Overland Probes", "color": "#2e5a4b"},
    {"id": "indigenous", "label": "Coast Miwok & Native Agency", "color": "#b7791f"},
    {"id": "foreign", "label": "Other Foreign Visits", "color": "#275d7a"},
    {"id": "refs", "label": "Spanish Posts (reference)", "color": "#6b6257"},
]

feats = []
seen = set()
def take(f, layer, keep_id=True):
    g = copy.deepcopy(f)
    g["layer"] = layer
    if g["id"] in seen:
        g["id"] = g["id"] + "-bc"
    seen.add(g["id"])
    feats.append(g)

# ── curate from the borderlands map by feature id ──
b = {f["id"]: f for f in border["features"]}
PICK = {
    # Spanish surveys / the 1793 attempt / port operations
    "spanish": [
        "goycoechea-s-overland-expedition-to-bodega",
        "eliza-s-activo-at-bodega-spain-s-last-pacific-ex",
        "golden-gate-crossing-borrowed-launches",
        "viceroy-orders-bodega-whether-or-not-english-are",
        "english-at-bodega-con-los-canones-en-tierra",
        "zuniga-shows-bodega-plans-to-british-no-concealm",
    ],
    "russian": [
        "rac-fur-collecting-begins-at-bodega",
        "130-bidarkas-in-san-francisco-bay",
        "farallon-islands-russian-sealing-station",
        "hagemeister-treaty-with-kashaya-pomo",
        "kuskov-s-rac-letters-to-the-sf-commandant",
        "spanish-missions-supply-kuskov-at-fort-ross",
        "fort-ross-abandonment-resolved",
        "rac-parlamentario-podushkin-on-the-chirikoff-at",
        "yanovsky-s-rac-trade-overture",
        "the-suvorov-at-sf-the-rac-proclamation-to-califo",
        "rezanov-arrives-on-juno",
    ],
    "indigenous": [
        "coast-miwok-intelligence-to-sal",
        "coast-miwok-deceive-goycoechea",
        "coast-miwok-calibrated-diplomacy-at-bodega",
        "coast-miwok-bilingual-intermediaries-at-tomales",
        "guirmenes-intel-on-bodega-keep-this-indian-happy",
        "chief-valli-ela-requests-russian-flag",
    ],
    "foreign": [
        "menzies-lands-at-tomales-bay",
        "hms-raccoon-at-san-francisco",
        "kotzebue-visits-on-rurik",
        "colnett-s-argonaut-at-bodega",
        "sola-to-viceroy-san-rafael-russian-threat",
    ],
}
missing = []
for layer, idlist in PICK.items():
    for fid in idlist:
        if fid in b:
            take(b[fid], layer)
        else:
            missing.append(fid)
print("missing borderlands ids:", missing)

# Ross benchmark from the presidial map (full series popup)
ross = [f for f in presidial["features"] if f["id"] == "colony-ross"][0]
take(ross, "russian")

# reference posts
for fid, layer in (("ref-presidio-of-san-francisco", "refs"), ("ref-fort-san-joaquin-castillo-de-sf", "refs"),
                   ("ref-mission-san-rafael", "refs")):
    if fid in b:
        take(b[fid], "refs")

# ── new corridor features (verified sources) ──
def NF(fid, name, iso, disp, conf, coords, prec, typ, layer, summary, result="",
       cites=None, ca_record=None, native=None, notes=""):
    src = []
    for c in (cites or []):
        src.append({"citation": c, "ca_record": None, "ia_leaf_url": None})
    if src and ca_record:
        src[0]["ca_record"] = ca_record
    seen.add(fid)
    feats.append({
        "id": fid, "register_no": None, "name": name,
        "date": {"iso": iso, "display": disp, "confidence": conf},
        "coords": coords, "coord_precision": prec, "type": typ, "layer": layer,
        "summary": summary, "result": result, "quote": None, "sources": src,
        "native_groups": native or [], "tags": [], "notes": notes})

NF("bodega-survey-1775", "Bodega y Quadra discovers and charts the port", "1775-10", "October 1775", "month",
   [38.310, -123.045], "exact", "event", "spanish",
   "The schooner Sonora under Bodega y Quadra and pilot Francisco Mourelle charts the port on the return leg of the 1775 voyage. Their manuscript plano, with keyed points and soundings, is the founding document of the Spanish claim. The chart is in this site's gallery.",
   result="The port charted and claimed",
   cites=["Plano del Puerto del Capitan Bodega (LOC, gallery item loc-bq05); resurveyed 1793 (Cartas esfericas sheet 8)"])
NF("matute-attempt-1793", "The 1793 occupation attempt fails", "1793", "1793", "year",
   [38.317, -123.053], "place", "event", "spanish",
   "The year Spain finally moved to occupy Bodega: Matute's establishment attempt, mounted amid the Nootka crisis, was abandoned. The port Spain had claimed in 1775 stayed empty, and the re-survey of the same year became its monument. The full argument is the subject of the companion article.",
   result="Spain never occupied the port it discovered",
   cites=["C-A 55 (Matute dossier); the 1793 re-survey, Cartas esfericas sheet 8 (gallery)"],
   notes="Deliberately summary-level here; the article carries the argument and the full citations.")
NF("aleut-fleet-1811", "The 1811 Aleut otter fleet in San Francisco Bay", "1811", "1811", "year",
   [37.85, -122.40], "area", "event", "russian",
   "Russian-American Company hunting reaches inside the bay itself: an Aleut baidarka fleet works San Francisco Bay for otter in 1811, the year before Ross was founded. Spain's inner waters were already a Russian hunting ground.",
   cites=["Prov. St. Pap. (C-A 12)"], ca_record="ca12-d376b",
   native=["Unangan/Alutiiq (Aleut) hunters"])
NF("vallejo-informe-1833", "Vallejo's reconnaissance of Ross (informe reservado)", "1833-05-05", "5 May 1833", "exact",
   [38.514, -123.244], "exact", "event", "russian",
   "M. G. Vallejo's confidential report on Ross: about 300 people, a wooden stockade, cannon in the towers, and Russian-American Company intelligence gathered through Wrangel's circle. The fullest Mexican-era picture of the colony, twenty years in.",
   cites=["St. Pap., Missions & Colonization (C-A 53), Doc 45 (n97–n111)"], ca_record="ca53-d45")
NF("ross-sale-1841", "Ross sold to Sutter; the Russians withdraw", "1841-12", "December 1841", "month",
   [38.514, -123.244], "exact", "event", "russian",
   "The Russian-American Company sells the Ross establishment to John Sutter and withdraws from California, ending the colony the Spanish had watched for thirty years without ever dislodging.",
   result="The Russian era ends by sale, not by force",
   cites=["Duflot de Mofras (1844) records the post-sale coast; cf. the borderlands map's abandonment-resolved pin"])

# ── routes: Moraga's Bodega & Ross probes, reused ──
routes = []
keep_routes = {"rbodega", "rross1812", "rross1813"}
for r in moraga.get("routes", []):
    if r["id"] in keep_routes:
        rr = copy.deepcopy(r)
        rr["layer"] = "overland"
        for s in rr["stops"]:
            if s["id"] in seen:
                s["id"] += "-bc"
            seen.add(s["id"])
        routes.append(rr)
print("routes reused:", [r["id"] for r in routes])

out = {
    "id": "bodega-ross-corridor",
    "title": "The Bodega–Ross Corridor",
    "subtitle": "The port Spain discovered and never held, 1775–1841",
    "abstract": ("Companion map to a research article on the 1793 Bodega expedition. It follows one "
                 "stretch of coast for sixty-six years: Bodega y Quadra charts the port in 1775; Spain "
                 "attempts and abandons an occupation in 1793; Russian hunters and then Colony Ross "
                 "(1812) move into the vacuum; Spanish probes reconnoiter but never dislodge them; the "
                 "Russians finally leave by sale in 1841. Coast Miwok communities appear throughout as "
                 "intelligence sources, guides, and negotiators on their own account. Features are drawn "
                 "from the same verified datasets as the other maps and keep their citations."),
    "date_range": [1775, 1841],
    "center": [38.25, -122.9],
    "zoom": 9,
    "cite_key": "bodega",
    "last_updated": "2026-07-15",
    "layers": LAYERS,
    "features": feats,
    "routes": routes
}
path = os.path.join(REPO, "data", "bodega-ross-corridor.json")
json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
print("features:", len(feats), "->", path)
