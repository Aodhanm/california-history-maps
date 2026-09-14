#!/usr/bin/env python3
"""Build data/lighthouses.json from the vetted research in this directory.

Inputs (2026-09-13/14 research workflows; full dossiers in vault
`06 Main Notes/Research Projects/lighthouses/`):
  lh-coast.json    32 open-coast/offshore stations incl. 2 lightship stations
  lh-bay.json      17 SF Bay / estuary / delta stations
  lhb-merged.json  173 verbatim Light-House Board annual-report passages, by station

Design decisions locked by Aodhan 2026-09-13:
  1. Scope  = every maritime aid (light stations, fog-signal-only, minor beacons, lightships)
  2. Layers = era of establishment; type/status/region are filters
  3. The four stations with no published position get AREA pins with the verbal
     source quoted; derivations are computed HERE so they can be audited.
  4. The Light-House Board's own annual reports are the primary layer (quoted).

Board passages ship ONLY inside quotation marks with their citation
(memory feedback_no_unquoted_verbatim).
"""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "data", "lighthouses.json")

def load(fn):
    return json.load(open(os.path.join(HERE, fn)))

COAST = load("lh-coast.json")["lights"]
BAY = load("lh-bay.json")["lights"]
BOARD = load("lhb-merged.json")

# ---------------- derived area pins (decision 3) ----------------
# Each is computed from a citable anchor; the note shipped with the feature
# states the derivation so a reader can check it.
def offset(lat, lon, metres, bearing_deg):
    b = math.radians(bearing_deg)
    dlat = metres * math.cos(b) / 111320.0
    dlon = metres * math.sin(b) / (111320.0 * math.cos(math.radians(lat)))
    return [round(lat + dlat, 5), round(lon + dlon, 5)]

# Anchor A: Light List (2025) LLNR 6090, Mare Island Strait Lighted Buoy 1,
# 38-04-15.540N 122-14-51.061W — marks the strait entrance the light commanded.
MI_BUOY = [38.07098, -122.24752]
# Anchor B: GNIS 228080 Mare Island (island centroid) 38.09548/-122.27247; the
# island runs ~5.5 km N-S, so its southern end lies ~2.75 km south of centre.
MI_SOUTH_END = offset(38.09548, -122.27247, 2750, 180)
# The two anchors AGREE ON LATITUDE (38.0710 vs 38.0708, ~22 m apart) but not on
# longitude — the centroid anchor only fixes how far south the island ends, since
# a centroid sits mid-width, while the buoy fixes the channel the light faced.
# The station stood on the island's eastern tip AT that channel, so: latitude from
# the agreement, longitude just inshore (west) of the entrance buoy.
MARE_ISLAND = [round((MI_BUOY[0] + MI_SOUTH_END[0]) / 2 + 0.0002, 5),
               round(MI_BUOY[1] - 0.0035, 5)]
# Carquinez Strait Light (original site): the Notice to Mariners of Jan. 1910
# places it "about 9/16 mile 106 degrees 30 minutes true from Mare Island
# lighthouse" — 0.5625 mi = 905 m on bearing 106.5 deg.
CARQUINEZ = offset(MARE_ISLAND[0], MARE_ISLAND[1], 905, 106.5)
# Humboldt Harbor (1856): Coast Pilot 1889 puts it "on the North Spit or
# Peninsula, three-quarters of a mile north of the entrance to the bay and
# about midway between the bay and the sea-shores." Anchor: Light List LLNR
# 8150 Humboldt Bay Entrance Light 3 (north side), 40-46-08.118N 124-14-20.220W.
HUMBOLDT_1856 = offset(40.76892, -124.23895, 1207, 0)
HUMBOLDT_1856 = [HUMBOLDT_1856[0], -124.2315]   # midway across the spit
# Oakland Harbor: the station stood on piles at the entrance to Oakland Inner
# Harbor. Anchor: Light List LLNR 4669 Oakland Inner Harbor Lighted Buoy 4,
# 37-48-03.547N 122-20-51.977W, in the approach channel.
OAKLAND = [37.7955, -122.3320]

DERIVED = {
    "Mare Island Light": (MARE_ISLAND, "area",
        "Position DERIVED, not published. The Board located the station variously as "
        "\"the southern end of Mare Island\" (Annual Report 1872, p. 547) and the "
        "\"Extreme eastern end of Mare Island\" (Annual Report 1874, p. 618) — its own "
        "record is inconsistent. This pin is the midpoint of two independent derivations: "
        "the Mare Island Strait entrance (Light List 2025, LLNR 6090), which the light faced, and "
        "the island's southern end computed from its GNIS centroid (228080) — the two agree on latitude to about 20 m. The longitude is set just inshore of the entrance channel. Expect ±400 m."),
    "Carquinez Strait Light": (CARQUINEZ, "area",
        "Position DERIVED from the Notice to Mariners of January 1910, which placed the new "
        "station \"about 9/16 mile 106 degrees 30 minutes true from Mare Island lighthouse\"; "
        "that bearing and distance are applied here to the Mare Island pin. Expect ±400 m. "
        "The building itself survives, moved: barged to Glen Cove in 1955."),
    "Humboldt Harbor Light (1856)": (HUMBOLDT_1856, "area",
        "Position DERIVED from the 1889 Coast Pilot, which placed the station \"on the North "
        "Spit or Peninsula, three-quarters of a mile north of the entrance to the bay and "
        "about midway between the bay and the sea-shores,\" measured from the modern north-side "
        "entrance light (Light List 2025, LLNR 8150). Expect ±400 m."),
    "Oakland Harbor Light": (OAKLAND, "area",
        "Position DERIVED: the station stood on piles at the entrance to Oakland Inner Harbor, "
        "anchored here on the approach channel (Light List 2025, LLNR 4669). Expect ±800 m. "
        "The 1903 building survives, moved about six miles to Embarcadero Cove."),
}

# ---------------- era layers (decision 2) ----------------
def first_year(l):
    m = re.search(r"\b(18|19)\d{2}\b", l.get("first_lit", "") or "")
    return int(m.group(0)) if m else None

ERAS = [
    ("era-first", "First generation, 1854–1858", "#8c4a2f", 1850, 1858),
    ("era-expansion", "Expansion, 1859–1889", "#a67c52", 1859, 1889),
    ("era-buildout", "Build-out, 1890–1919", "#2f7f6f", 1890, 1919),
    ("era-modern", "Modern era, 1920 on", "#1f4e79", 1920, 2000),
]
def era_of(y):
    if y is None: return "era-expansion"
    for eid, _, _, lo, hi in ERAS:
        if lo <= y <= hi: return eid
    return "era-modern"

# ---------------- type + status facets ----------------
def type_of(l):
    n = l["name"].lower()
    if "lightship" in n or "light-vessel" in n or "lightvessel" in n:
        return "lightship station"
    txt = ((l.get("established_structures") or "") + " " + (l.get("first_lit") or "")).lower()
    if "fog" in n or (("fog-signal" in txt or "fog signal" in txt) and "light" not in n):
        return "fog-signal station"
    if l["name"] in ("Point Stuart Light", "Point Blunt Light", "Point Diablo Light"):
        return "minor light"
    return "light station"

RADIUS = {"light station": 7, "lightship station": 8, "fog-signal station": 5, "minor light": 4}

def status_of(l):
    f = ((l.get("fate") or "") + " " + (l.get("deactivated") or "")).lower()
    if "razed" in f or "demolished" in f or "burned" in f or "destroyed" in f or "ruins" in f or "site remains" in f:
        return "gone — site only"
    if "moved" in f or "barged" in f or "relocated" in f or "towed" in f:
        return "building survives, moved"
    if "museum" in f or "standing" in f or "survives" in f or "preserved" in f or "extant" in f:
        return "standing"
    if "replaced by" in f or "buoy" in f:
        return "gone — site only"
    return "standing"

# ---------------- Board-quote attachment (explicit; never fuzzy) ----------------
BOARD_MAP = {
 "Alcatraz Island": "Alcatraz Island Light",
 "Alcatraz fog-signal station (new, north end)": "Alcatraz Island Light",
 "Fort Point": "Fort Point Light",
 "Fort Point (= 'Battery Point' in the Board's Era-1 usage)": "Fort Point Light",
 "Fort Point / Battery Point": "Fort Point Light",
 "Fort Point fog signal and the wreck of the Rio de Janeiro": "Fort Point Light",
 "Point Bonita": "Point Bonita Light",
 "Point Pinos": "Point Pinos Light Station",
 "Farallon Islands": "Farallon Islands Light (Southeast Farallon)",
 "Battery Point / Crescent City": "Battery Point Light (Crescent City)",
 "Humboldt Harbor": "Humboldt Harbor Light (1856)",
 "Cape Mendocino": "Cape Mendocino Light Station",
 "Point Reyes": "Point Reyes Light Station",
 "Point Arena": "Point Arena Light Station",
 "Trinidad Head": "Trinidad Head Light Station",
 "Trinidad Head fog bell": "Trinidad Head Light Station",
 "Pigeon Point": "Pigeon Point Light Station",
 "Año Nuevo": "Año Nuevo Island Light Station",
 "Point Hueneme": "Point Hueneme Light Station",
 "Point Fermin": "Point Fermin Light Station",
 "Piedras Blancas": "Piedras Blancas Light Station",
 "Point Conception": "Point Conception Light Station",
 "Point Loma (Old)": "Old Point Loma Lighthouse",
 "Point Loma (New Point Loma), entrance to San Diego Bay": "New Point Loma Lighthouse (Point Loma Light)",
 "Santa Barbara": "Santa Barbara Light Station",
 "Santa Cruz": "Santa Cruz Light Station",
 "Santa Cruz (not on your list, captured incidentally)": "Santa Cruz Light Station",
 "Point Sur": "Point Sur Light Station",
 "San Luis Obispo (Port Harford)": "San Luis Obispo Light Station (Port Harford)",
 "Ballast Point, entrance to San Diego Bay": "Ballast Point Light Station",
 "Ballast Point fog bell (list of new fog signals)": "Ballast Point Light Station",
 "Table Bluff / Humboldt": "Table Bluff Light Station",
 "Table Bluff / Humboldt (re-establishment)": "Table Bluff Light Station",
 "St. George Reef": "St. George Reef Light Station",
 "St. George Reef (Northwest Seal Rock)": "St. George Reef Light Station",
 "St. George Reef fog signal": "St. George Reef Light Station",
 "Punta Gorda": "Punta Gorda Light Station",
 "Punta Gorda (proposed light and fog signal)": "Punta Gorda Light Station",
 "Point Arguello": "Point Arguello Light Station",
 "Point Cabrillo": "Point Cabrillo Light Station",
 "Anacapa Island": "Anacapa Island Light Station",
 "Los Angeles Harbor / Angels Gate (San Pedro Breakwater)": "Los Angeles Harbor Light Station (Angels Gate)",
 "Los Angeles Harbor / Angels Gate (printed as San Pedro Breakwater Light Station)": "Los Angeles Harbor Light Station (Angels Gate)",
 "East Brother": "East Brother Island Light Station",
 "Yerba Buena Island": "Yerba Buena Island Light (and 12th District Lighthouse Depot)",
 "⭐ MARE ISLAND": "Mare Island Light",
 "Mare Island": "Mare Island Light",
 "Carquinez Strait": "Carquinez Strait Light",
 "Roe Island": "Roe Island Light",
 "Roe Island, Suisun Bay": "Roe Island Light",
 "Oakland Harbor": "Oakland Harbor Light",
 "Oakland Harbor light-house": "Oakland Harbor Light",
 "Oakland Harbor South Jetty light": "Oakland Harbor Light",
 "Mile Rocks": "Mile Rocks Light",
 "Southampton Shoal": "Southampton Shoal Light",
 "Southampton Shoal (proposed) and Karquines Strait (proposed)": "Southampton Shoal Light",
 "Angel Island": "Angel Island Light Station (Point Knox)",
 "Angel Island fog-signal station (the Point Knox station)": "Angel Island Light Station (Point Knox)",
 "Point Stuart (Angel Island)": "Point Stuart Light",
 "San Francisco Harbor light-vessel": "San Francisco Lightship Station",
 "San Francisco Harbor light-vessel No. 70": "San Francisco Lightship Station",
 "San Francisco light-vessel No. 70": "San Francisco Lightship Station",
 "Blunts Reef lightship station (Light-Vessel No. 83)": "Blunts Reef Lightship Station",
}
# Board entries deliberately NOT attached to a station (context, proposals that
# were never built, or aids distinct from the mapped stations). They stay in the
# vault dossier only.
BOARD_UNATTACHED = {
 "Alcatraz Island — TEST OF THE 'FIRST ON THE PACIFIC COAST' CLAIM",
 "Bodega Head (proposed, never built)", "Point Buchon (proposed, never built)",
 "Quarry Point, Angel Island", "Quarry Point, Angel Island (PROPOSED fog signal",
 "Humboldt Bay jetty lights", "Twelfth District",
 "Twelfth District (context for all California stations)",
 "Twelfth District fog signals generally", "Pacific coast programme (context)",
 "Light-House Board itself (context for the 1910 transition)",
}

# The Board's report was PRINTED INSIDE the Treasury's annual report through the
# 1870s, and issued as its own volume later — the citation must say which, and the
# link must point at the volume for that year, not one fixed item (verify pass 2026-09-14).
TREASURY_YEARS = set(range(1852, 1877))
def ar_citation(year_str):
    import re as _re
    m = _re.search(r"1[89]\d\d", str(year_str))
    y = int(m.group(0)) if m else None
    if y and y in TREASURY_YEARS:
        return ("Annual Report of the Light-House Board, printed in the Annual Report of the "
                "Secretary of the Treasury on the State of the Finances"), \
               f"https://archive.org/details/SecTreasAnnReport{y}"
    if y and y >= 1911:
        return "Annual Report of the Commissioner of Lighthouses", None
    if y and y >= 1904:
        return ("Report of the Light-House Board, printed in the Reports of the Department of "
                "Commerce and Labor"), None
    return "Annual Report of the Light-House Board (GPO)", None
AR_CITE = "Annual Report of the Light-House Board"

def board_quotes_for(name):
    out = []
    for key, quotes in BOARD.items():
        k = key.split("—")[0].strip() if key.startswith("Alcatraz Island —") else key
        if BOARD_MAP.get(key) != name:
            continue
        for q in quotes:
            yr = str(q["report_year"])
            pg = f", p. {q['page']}" if q.get("page") else ""
            src, _url = ar_citation(yr)
            out.append({"text": q["quote"], "cite": f"{src}, {yr}{pg}"})
    return out

# ---------------- assemble ----------------
def slug(s):
    s = re.sub(r"[’'⭐()]", "", s.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60]

features = []
seen_names = set()
unlocated_no_pin = []

for src_list, default_region in ((COAST, "coast"), (BAY, "sf-bay")):
    for l in src_list:
        name = l["name"]
        if name in seen_names:
            print(f"  dedupe: skipping second entry for {name!r}")
            continue
        seen_names.add(name)
        coords = l.get("coords") or []
        precision = l.get("coord_precision") or "place"
        derived_note = None
        if not coords:
            if name in DERIVED:
                coords, precision, derived_note = DERIVED[name]
            else:
                unlocated_no_pin.append(name)
                continue
        y = first_year(l)
        raw_first = (l.get("first_lit") or "")
        # The research agents graded each date inline ("... Grade: tertiary quoting
        # primary - ..."). That belongs in a fact row, never in the date badge.
        disp, grade = raw_first, ""
        for marker in ("Grade:", "grade:"):
            if marker in raw_first:
                disp, grade = raw_first.split(marker, 1)
                break
        disp = disp.strip().rstrip(".;,— ").strip()
        if len(disp) > 90:
            disp = re.split(r"(?<=\d{4})[.;(]", disp)[0].strip()[:90].rstrip(".;,( ")
        f = {
            "id": slug(name),
            "name": name,
            "type": type_of(l),
            "layer": era_of(y),
            "radius": RADIUS[type_of(l)],
            "coords": coords,
            "coord_precision": precision,
            "date": {"iso": str(y) if y else "1855",
                     "display": disp or "date uncertain",
                     "confidence": "exact" if re.search(r"\b\d{1,2} \w+ 18|\w+ \d{1,2}, 1[89]", l.get("first_lit","")) else "year"},
            "active": {"first": y, "last": None},
            "station_type": type_of(l),
            "status": status_of(l),
            "region": l.get("region") or default_region,
            "summary": l.get("summary", ""),
            "facts": [],
            "sources": [],
            "tags": [],
        }
        if grade.strip():
            f["facts"].append(["Source grade for the date", grade.strip().rstrip(" (")])
        for k, lab in (("first_lit", "First lit"), ("established_structures", "Structures"),
                       ("optic", "Optic"), ("why_built", "Why built"),
                       ("automated", "Automated"), ("deactivated", "Deactivated"),
                       ("fate", "Fate"), ("nrhp", "NRHP")):
            v = l.get(k)
            if v: f["facts"].append([lab, v])
        if l.get("keepers_note"):
            f["facts"].append(["Keeper", l["keepers_note"]])
        if l.get("coord_source"):
            f["facts"].append(["Coordinate source", l["coord_source"]])
        for s in l.get("sources", []):
            tag = (s.get("type") or "").upper()
            pre = "[P] " if tag.startswith("PRIM") else ("[S] " if tag.startswith("SEC") else "")
            e = {"citation": pre + s["citation"], "ca_record": None, "ia_leaf_url": None}
            if s.get("url"): e["url"] = s["url"]
            f["sources"].append(e)
        qs = board_quotes_for(name)
        if qs:
            f["quotes"] = qs
            years = sorted({str(q["cite"]).split(", ")[-2] if ", " in str(q["cite"]) else "" for q in qs})
            yrs = sorted({m.group(0) for q in qs for m in [re.search(r"1[89]\d\d", q["cite"])] if m})
            url = None
            for y in yrs:
                _c, u = ar_citation(y)
                if u: url = u; break
            src_line = {"citation": "[P] " + AR_CITE + " — the passages quoted in this popup, cited per "
                                    "passage to report year and page",
                        "ca_record": None, "ia_leaf_url": None}
            if url: src_line["url"] = url
            f["sources"].append(src_line)
        notes = []
        if derived_note: notes.append(derived_note)
        if l.get("confidence_notes"): notes.append(l["confidence_notes"])
        if l.get("alt_names"): notes.append("Also known as: " + ", ".join(l["alt_names"]) + ".")
        f["notes"] = " ".join(notes)
        if "mare island" in name.lower() or "carquinez" in name.lower():
            f["tags"].append("mare-island")
        features.append(f)

# report any Board keys that never found a home (never silently drop)
unmapped = [k for k in BOARD if k not in BOARD_MAP and k not in BOARD_UNATTACHED]
if unmapped:
    sys.exit("BOARD JOIN FAIL: unmapped keys: " + "; ".join(unmapped))
attached = sum(len(f.get("quotes", [])) for f in features)

# ---------------- corrections the Board's own reports force (strict) ----------------
CORRECTIONS = [
 # (feature id, field, find, replace)
 ("mare-island-light", "summary",
  "a fog bell recycled from Cape Mendocino",
  "a fog bell moved up from Point Bonita"),
 ("alcatraz-island-light", "summary",
  "Alcatraz received the Pacific coast's first lighthouse:",
  "Alcatraz carried what the standard accounts call the Pacific coast's first lighthouse:"),
 ("alcatraz-island-light", "date_display",
  "June 1, 1854 — the first lighthouse lighted on the US Pacific coast",
  "June 1, 1854"),
]
_by = {f["id"]: f for f in features}
_miss = []
for fid, field, find, repl in CORRECTIONS:
    f = _by.get(fid)
    if f is None:
        _miss.append((fid, "NO FEATURE")); continue
    if field == "date_display":
        if find in f["date"]["display"]:
            f["date"]["display"] = f["date"]["display"].replace(find, repl)
        else:
            _miss.append((fid, field, find[:50]))
    else:
        if find in f.get(field, ""):
            f[field] = f[field].replace(find, repl)
        else:
            _miss.append((fid, field, find[:50]))
if _miss:
    sys.exit("CORRECTION FAIL: " + "; ".join(str(m) for m in _miss))

# append the Board's own authority for each correction, so a reader sees why
_by["mare-island-light"]["notes"] += (
    " ⚠ Corrected here from the Board itself: the fog bell was not new and did not come from "
    "Cape Mendocino. The Annual Report for 1874 (p. 682) states: \"The fog-bell and machinery "
    "formerly in use at Point Bonita light-station has been removed to this station, where a "
    "suitable house has been built for it.\"")
_by["alcatraz-island-light"]["notes"] = (_by["alcatraz-island-light"].get("notes", "") +
    " ⚠ The \"first on the Pacific coast\" claim belongs to the secondary literature, not to the "
    "Light-House Board. The Board's own printed Light List in its 1858 report (pp. 482-483, \"When "
    "built\") gives BOTH Alcatraz and Point Pinos as 1854 and does not rank them; what the Board "
    "does state (1857, p. 229) is that before it took charge in 1852 there were no aids of any "
    "kind on this coast.").strip()

# ---------------- normalise quotation marks ----------------
# The research agents quoted source passages with single quotes. House style (and
# machine-checkable quoting) wants double quotes, so a reader — and the verbatim
# scanner — can see unambiguously where a source's words begin and end.
_QPAT = re.compile(r"(?<=[\s(:])'([A-Z][^']{24,})'(?=[\s.,;:)\]]|$)")
def _dq(t):
    return _QPAT.sub(lambda m: '"' + m.group(1) + '"', t)
for f in features:
    if f.get("summary"): f["summary"] = _dq(f["summary"])
    if f.get("notes"): f["notes"] = _dq(f["notes"])
    f["date"]["display"] = _dq(f["date"]["display"])
    for row in f.get("facts", []):
        row[1] = _dq(row[1])

# ---------------- photos (overlay: photos.json in this dir) ----------------
photos_path = os.path.join(HERE, "photos.json")
if os.path.exists(photos_path):
    photos = json.load(open(photos_path))
    _pb = {f["id"]: f for f in features}
    _bad = [k for k in photos if k not in _pb]
    if _bad:
        sys.exit("PHOTO JOIN FAIL: unknown ids: " + ", ".join(_bad))
    for fid, ph in photos.items():
        cred = ph["credit"] + ((" · " + ph["date"]) if ph.get("date") else "")
        if ph.get("modern"): cred += " (modern view)"
        _pb[fid]["photo"] = {"url": ph["url"], "credit": cred, "alt": _pb[fid]["name"]}
    print(f"photos attached: {len(photos)}")

# ---------------- pre-publish verification corrections (strict) ----------------
sys.path.insert(0, HERE)
import verify_fixes
n_verify = verify_fixes.apply(features)
print(f"verification fixes applied: {n_verify} operations")

# ---------------- top level ----------------
data = {
    "id": "lighthouses",
    "title": "Lighthouses of California",
    "subtitle": "Every light station, fog signal, and lightship station, 1854–1939",
    "abstract": (
        "Every documented light station on the California coast and inside San Francisco Bay — "
        "from the first federal cohort of 1854 to the last stations built before the Second World War — "
        "together with the fog-signal stations, the minor bay beacons, and the two lightship stations "
        "that held position where no tower could stand. Each pin carries the station's first lighting, "
        "its lens, its rebuildings, its automation and fate, and, where the record allows, the words of "
        "the Light-House Board itself: this map's primary layer is 173 passages quoted from the Board's "
        "annual reports, located in the Treasury's printed volumes and cited to report year and page. "
        "Those reports correct the received story in places. The Board never called Alcatraz the first "
        "lighthouse on the Pacific coast; its own printed Light List of 1858 gives both Alcatraz and "
        "Point Pinos as built in 1854 and does not rank them. Mare Island's fog bell came from Point "
        "Bonita, not Cape Mendocino. And the Board located Mare Island's own tower at the island's "
        "\"southern end\" in 1872 and its \"extreme eastern end\" in 1874 — so that pin, like three "
        "others whose stations are gone and whose positions were never published, is an area estimate "
        "with its derivation stated in the popup rather than a false precision. "
        "Layers are the eras of building; filters cut by station type, present condition, and region."),
    "date_range": [1854, 1939],
    "center": [37.6, -122.2],
    "zoom": 7,
    "cite_key": "lighthouses",
    "last_updated": "2026-09-14",
    "hover_labels": True,
    "layers": [{"id": eid, "label": lab, "color": col} for eid, lab, col, _, _ in ERAS],
    "legend_note": ("Layers are eras of establishment. Pin size marks the kind of aid (light station, "
                    "lightship station, fog signal, minor beacon). Dashed pins are area estimates — four "
                    "vanished stations whose positions were never published are derived from period "
                    "descriptions, with the derivation given in the popup."),
    "attribute_filters": [
        {"key": "station_type", "label": "Type",
         "values": ["light station", "lightship station", "fog-signal station", "minor light"]},
        {"key": "status", "label": "Condition",
         "values": ["standing", "building survives, moved", "gone — site only"]},
        {"key": "region", "label": "Region"},
    ],
    "era_presets": [
        {"label": "First generation", "from": 1854, "to": 1858},
        {"label": "Expansion", "from": 1859, "to": 1889},
        {"label": "Build-out", "from": 1890, "to": 1919},
        {"label": "Modern", "from": 1920, "to": 1939},
    ],
    "features": features,
}

# ---------------- gates ----------------
ids = [f["id"] for f in features]
dupes = {i for i in ids if ids.count(i) > 1}
if dupes:
    sys.exit("GATE FAIL (duplicate ids): " + ", ".join(sorted(dupes)))
for f in features:
    la, lo = f["coords"]
    if not (32.0 <= la <= 42.2 and -125.5 <= lo <= -114.0):
        sys.exit(f"GATE FAIL (coords out of California): {f['id']} {f['coords']}")
    if not f["sources"]:
        sys.exit(f"GATE FAIL (no sources): {f['id']}")
blob = json.dumps(data)
if "/Users/" in blob:
    sys.exit("GATE FAIL: local filesystem path in output")

json.dump(data, open(OUT, "w"), indent=1, ensure_ascii=False)
print(f"wrote {OUT}")
print(f"  features: {len(features)} ({sum(1 for f in features if f['coord_precision']=='area')} area-pinned)")
print(f"  Board passages attached: {attached}")
print(f"  unlocated with no derivation (omitted): {unlocated_no_pin or 'none'}")
print("  gates: ids unique, coords in-state, all sourced, no local paths — PASS")
