#!/usr/bin/env python3
"""Build data/lumber-ports.json from the vetted research JSONs in this directory.

Inputs (all produced + gate-validated 2026-09-13, see vault
`06 Main Notes/Research Projects/lumber-ports/coordinates-register.md`):
  agent-sonoma-mendocino-ports.json   gazetteer content (46 ports, sourced)
  agent-north-central-ports.json      gazetteer content (29 features, sourced)
  p3-coords-sonoma-mendocino.json     coordinates w/ provenance (57 canon features)
  p3-coords-north-central.json        coordinates w/ provenance (36 features)
  p3-railroads-routes.json            15 rail routes w/ sourced waypoints

Authority for the canonical 57 (names, aliases, circa dates) = the NRHP doghole
MPDF draft 2021 via the vault alias-concordance. Join tables below are EXPLICIT:
every port names its gazetteer key and its coords key, so a wrong join is
visible in this file, not hidden in fuzzy matching. The script re-runs the
north->south monotonic gate on its own output and refuses to write on failure.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "data", "lumber-ports.json")

def load(fn):
    return json.load(open(os.path.join(HERE, fn)))

GAZ_SM = {p["name"]: p for p in load("agent-sonoma-mendocino-ports.json")["ports"]}
GAZ_NC = {p["name"]: p for p in load("agent-north-central-ports.json")["ports"]}
P3_SM  = {f["name"]: f for f in load("p3-coords-sonoma-mendocino.json")["features"]}
P3_NC  = {f["name"]: f for f in load("p3-coords-north-central.json")["features"]}
RAILS  = load("p3-railroads-routes.json")["routes"]

MPDF = ("Marx & Jaffke, Northern California Doghole Ports Maritime Cultural "
        "Landscape, NRHP MPDF draft (CA DPR, 2021)")
MPDF_URL = ("https://ohp.parks.ca.gov/pages/1067/files/CA_Sonoma%20and%20Mendocino"
            "%20Counties_%20Nor%20Cal%20Doghole%20Ports_MPDF_Draft.pdf")

# ---- classes -> layer, pin radius, filter label ----
CLASSES = {
    "chute":     ("class-chute",     5,  "chute-only doghole"),
    "pier":      ("class-pier",      7,  "doghole with pier"),
    "river-bar": ("class-river-bar", 8,  "river bar harbor"),
    "deepwater": ("class-deepwater", 10, "deepwater / major wharf"),
}

# cargo keyword -> canonical value
CARGO_MAP = [
    ("tanbark", "tanbark"), ("tan bark", "tanbark"), ("tie", "railroad ties"),
    ("post", "posts & split stuff"), ("shingle", "posts & split stuff"),
    ("shake", "posts & split stuff"), ("picket", "posts & split stuff"),
    ("lath", "posts & split stuff"), ("stave", "posts & split stuff"),
    ("fencing", "posts & split stuff"), ("cordwood", "cordwood & firewood"),
    ("firewood", "cordwood & firewood"), ("wood (", "cordwood & firewood"),
    ("fir", "Douglas fir"), ("potato", "farm produce"), ("produce", "farm produce"),
    ("dairy", "farm produce"), ("grain", "farm produce"), ("fruit", "farm produce"),
    ("hog", "farm produce"), ("wool", "farm produce"), ("butter", "farm produce"),
    ("lumber", "redwood lumber"), ("redwood", "redwood lumber"),
]
def cargo_of(products):
    out = []
    for p in products or []:
        pl = p.lower()
        for k, v in CARGO_MAP:
            if k in pl and v not in out:
                out.append(v)
    return out or ["redwood lumber"]

# company keyword -> canonical filterable name (multi-port majors + notable firms)
COMPANY_MAP = [
    ("mendocino lumber", "Mendocino Lumber Co."), ("caspar lumber", "Caspar Lumber Co."),
    ("jackson", "Caspar Lumber Co."), ("union lumber", "Union Lumber Co."),
    ("c.r. johnson", "Union Lumber Co."), ("albion lumber", "Albion Lumber Co."),
    ("southern pacific", "Albion Lumber Co. (SP)"), ("l.e. white", "L.E. White Lumber Co."),
    ("white lumber", "L.E. White Lumber Co."), ("goodyear", "Goodyear Redwood Co."),
    ("gualala mill", "Gualala Mill Co."), ("dollar", "Robert Dollar Co."),
    ("usal redwood", "Robert Dollar Co."), ("bear harbor lumber", "Bear Harbor Lumber Co."),
    ("finkbine", "Finkbine-Guild Lumber Co."), ("richardson", "Richardson family (Stewarts Point)"),
    ("duncan", "Duncan brothers"), ("hobbs", "Hobbs, Wall & Co."),
    ("dolbeer", "Dolbeer & Carson"), ("pacific lumber", "Pacific Lumber Co."),
    ("hammond", "Hammond Lumber Co."), ("e.k. wood", "E.K. Wood Lumber Co."),
    ("vance", "Hammond Lumber Co."), ("korbel", "Korbel / Humboldt Lumber Mill Co."),
    ("bendixsen", "Bendixsen shipyard"), ("stephen smith", "Stephen Smith (Bodega mill)"),
    ("western redwood", "Western Redwood Lumber Co."), ("funcke", "Funcke & Gerstle (tanbark)"),
    ("gerstle", "Funcke & Gerstle (tanbark)"), ("call", "Call family (Fort Ross)"),
    ("monroe lumber", "Monroe Lumber Co."), ("hihn", "F.A. Hihn Co."),
    ("notley", "Notley brothers"), ("kelley", "Caspar Lumber Co."),
]
def companies_of(raw_list):
    out = []
    for c in raw_list or []:
        cl = c.lower()
        for k, v in COMPANY_MAP:
            if k in cl and v not in out:
                out.append(v)
    return out

# MPDF per-port historic vessel-loss counts (tech dossier + regex extraction)
WRECKS = {
    "stewarts-point": 18, "fish-rock": 16, "bourns-landing": 16, "albion": 10,
    "iversons-landing": 10, "westport": 8, "noyo": 8, "cuffeys-cove": 8,
    "navarro": 8, "salt-point": 8, "arena-cove": 7, "little-river": 7,
    "whitesboro": 7, "fort-ross": 7, "bridgeport-landing": 3,
}

def slug(s):
    s = re.sub(r"[’']", "", s.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def date_of(first, last, display, conf="circa"):
    return {"iso": str(first) if first else str(last), "display": display, "confidence": conf}

# ---------------- the canonical 57 (MPDF north->south) ----------------
# (no, authority name, aliases, first, last, class, gaz_key, gaz_src, p3_key, p3_src, flags)
# gaz_src / p3_src: SM | NC | None(inline addendum content)
CANON = [
 (1,"Needle Rock Landing",[],1873,1930,"chute","Needle Rock Landing","NC","Needle Rock landing","NC",{}),
 (2,"Bear Harbor Landing",[],1884,1909,"pier","Bear Harbor Landing","NC","Bear Harbor landing (second/main site, Cluster Cone Rocks)","NC",{}),
 (3,"Northport Landing",["Anderson's Landing"],1872,1883,"chute",None,None,"Northport / Anderson's Landing","SM",{}),
 (4,"Monroe Landing",["Hale's Grove Landing","Usal Landing (alias only)"],1905,1911,"pier",None,None,None,None,{"unlocated":True}),
 (5,"Devilbliss Landing",[],1895,1896,"chute",None,None,None,None,{"unlocated":True}),
 (6,"Rockport Landing",["Cottoneva Cove","Miller's Chute","Summer Anchorage"],1877,1940,"pier","Rockport (Cottoneva Cove)","SM","Rockport (Cottaneva Cove / Miller's Chute)","SM",{}),
 (7,"Hardy Creek Landing",[],1895,1920,"chute","Hardy Creek","SM","Hardy Creek Landing","SM",{}),
 (8,"Union Landing",["McFaul's Landing"],1899,1920,"pier","Union Landing","SM","Union Landing / McFaul's","SM",{}),
 (9,"Westport Landing",["Switzer's Chute","Beall's","Helmke's"],1865,1930,"pier","Westport","SM","Westport Landing","SM",{}),
 (10,"Kibesilah Landing",["Ackermann's Landing"],1880,1890,"pier","Kibesillah","SM","Kibesilah / Ackermann's Landing","SM",{}),
 (11,"Newport Landing",[],1880,1900,"chute","Newport","SM","Newport Landing (Mendocino)","SM",{}),
 (12,"Laguna Landing",["Cleone Landing"],1883,1920,"pier","Cleone (Laguna Point)","SM","Laguna / Cleone Landing","SM",{}),
 (13,"Fort Bragg Landing",["Soldiers Harbor"],1885,1930,"pier","Fort Bragg (Soldiers Harbor)","SM","Fort Bragg Landing (Soldiers Harbor / mill pier)","SM",{}),
 (14,"Noyo Landing",["Noyo Anchorage"],1860,1930,"river-bar","Noyo River","SM","Noyo Landing / Noyo Anchorage","SM",{}),
 (15,"Pallas Bay Landing",["Palace Bay Harbor"],1880,1887,"chute",None,None,"Pallas Bay Landing","SM",{}),
 (16,"Bromley Gulch Landing",[],1884,1889,"chute",None,None,"Bromley Gulch Landing","SM",{"never_active":True}),
 (17,"Caspar Landing",["Caspar Anchorage"],1864,1935,"pier","Caspar","SM","Caspar Landing","SM",{}),
 (18,"Russian Gulch Landing (Mendocino)",[],1875,1920,"chute","Russian Gulch (Mendocino)","SM","Russian Gulch Landing (MENDOCINO)","SM",{}),
 (19,"Mendocino Landing",["Big River Landing"],1852,1940,"river-bar","Mendocino (Big River)","SM","Mendocino Landing / Big River","SM",{}),
 (20,"Little River Landing",["Bell's Landing","Kents Cove"],1860,1917,"pier","Little River","SM","Little River Landing","SM",{}),
 (21,"Big Gulch Landing",["Pullen's Landing"],1874,1885,"chute",None,None,"Big Gulch / Pullen's Landing","SM",{}),
 (22,"Albion Landing",["Albion Harbor"],1860,1930,"river-bar","Albion","SM","Albion Landing","SM",{}),
 (23,"Henley's Landing",["Handley's Chute"],1868,1900,"chute",None,None,"Henley's Landing (Handley's Chute)","SM",{}),
 (24,"Whitesboro Landing",["Salmon Creek"],1870,1902,"pier","Whitesboro (Salmon Creek)","SM","Whitesboro Landing","SM",{}),
 (25,"Navarro Landing",["Navarro Harbor"],1860,1917,"river-bar","Navarro (Navarro-by-the-Sea)","SM","Navarro Landing","SM",{}),
 (26,"Cuffey's Cove Landing",[],1868,1909,"chute","Cuffey's Cove","SM","Cuffey's Cove Landing","SM",{}),
 (27,"Chisholm Landing",[],1870,1889,"chute",None,None,"Chisholm Landing","SM",{}),
 (28,"Greenwood Creek Landing",["Greenwood","Elk"],1886,1917,"pier","Greenwood (Elk)","SM","Greenwood Creek Landing (Elk)","SM",{}),
 (29,"Unnamed Landing (near Uncle Abe's)",[],None,1889,"chute",None,None,None,None,{"unlocated":True}),
 (30,"Uncle Abe's Landing",[],1876,1889,"chute",None,None,None,None,{"unlocated":True}),
 (31,"Bridgeport Landing",["Hoag's Landing","Field's Landing (Mendocino)","Kimball's Chute"],1871,1892,"chute","Bridgeport Landing","SM","Bridgeport Landing (Hoag's / Field's / Kimball's)","SM",{}),
 (32,"New Haven Landing",[],1886,1892,"chute","New Haven Landing (with Mal Paso)","SM","New Haven Landing","SM",{}),
 (33,"Arena Cove Landing",["Point Arena"],1866,1930,"pier","Point Arena / Arena Cove","SM","Arena Cove Landing","SM",{}),
 (34,"Buster's Landing",["France's Landing"],1871,1874,"chute",None,None,None,None,{"unlocated":True}),
 (35,"Scott's Landing",["Slide Rock","Scoutt's Landing"],1870,1890,"chute",None,None,None,None,{"unlocated":True}),
 (36,"Saunders' Landing",["Hearn's Landing"],1877,1895,"chute","Saunders Landing","SM","Saunders' Landing (Hearn's)","SM",{}),
 (37,"Iverson's Landing",["Fergusons Cove","Rough and Ready"],1880,1911,"chute","Iversen's Landing (Fergusons Cove / Rough and Ready)","SM","Iverson's Landing (Fergusons Cove / Rough and Ready)","SM",{}),
 (38,"Steen's Landing",["Hardscratch","Signal Port"],1882,1890,"chute","Signal Port (Steens Landing)","SM","Steen's Landing (Hardscratch / Signal Port)","SM",{}),
 (39,"Nip and Tuck Landing",["Phelp's","Bryne's","Peter's","Beadle's"],1879,1903,"chute","Nip and Tuck Landing","SM","Nip and Tuck Landing (Phelp's / Beadle's)","SM",{}),
 (40,"Fish Rock Landing",["Haven's Anchorage","Anchor Bay"],1870,1914,"chute","Fish Rock (Havens Anchorage / Anchor Bay)","SM","Fish Rock Landing / Havens Anchorage","SM",{}),
 (41,"Collin's Landing",["St. Ores"],1869,1900,"pier","Collins Landing","SM","Collin's Landing (St. Ores)","SM",{}),
 (42,"Bourn's Landing",["Bowens Landing","Bourne's","Bone's"],1862,1920,"pier","Bourns Landing","SM","Bourn's Landing (Bowens / Bourne's)","SM",{}),
 (43,"Gualala Landing",["Walalla","Robinson's","Rutherford's"],1865,1884,"chute","Gualala","SM","Gualala Landing (Walalla / Robinson's / Rutherford's)","SM",{}),
 (44,"Joe Tongue's Landing",["Joe Tonga's"],1880,1900,"chute",None,None,"Joe Tongue's Landing (candidate only)","SM",{}),
 (45,"Del Mar Landing",[],1898,1926,"chute","Del Mar Landing","SM","Del Mar Landing","SM",{}),
 (46,"Bihler Landing",["Black Point"],1875,1926,"chute","Bihler Landing (Black Point)","SM","Bihler Landing (Black Point)","SM",{}),
 (47,"Stewarts Point Landing",["Fisherman's Bay"],1875,1925,"chute","Stewarts Point","SM","Stewarts Point Landing (Fisherman's Bay)","SM",{}),
 (48,"Fisk Mill Landing",[],1860,1910,"chute","Fisk Mill Cove","SM","Fisk Mill Cove Landing","SM",{}),
 (49,"Salt Point Landing",["Gerstle Cove"],1853,1917,"pier","Salt Point / Gerstle Cove","SM","Salt Point Landing (Gerstle Cove)","SM",{}),
 (50,"Walsh Landing",["Ocean Cove"],1889,1912,"chute","Walsh Landing (Ocean Cove)","SM","Walsh Landing (Ocean Cove)","SM",{}),
 (51,"Stockhoff Cove Landing",[],1870,1906,"chute",None,None,"Stockhoff Cove Landing","SM",{}),
 (52,"Stillwater Cove Landing",[],1868,1889,"chute","Stillwater Cove","SM","Stillwater Cove Landing","SM",{}),
 (53,"Timber Cove Landing",[],1856,1925,"chute","Timber Cove","SM","Timber Cove Landing","SM",{}),
 (54,"Fort Ross Landing",[],1867,1921,"pier","Fort Ross Cove","SM","Fort Ross Cove Landing","SM",{}),
 (55,"Russian Gulch Landing (Sonoma)",[],1875,1910,"chute","Russian Gulch Landing (Sonoma)","SM","Russian Gulch Landing (SONOMA)","SM",{}),
 (56,"Rule's Landing",["Rules Head"],1877,1884,"chute","Rule's Landing","SM","Rule's Landing (Rule's Head)","SM",{}),
 (57,"Duncan's Landing",[],1860,1889,"chute","Duncan's Landing","SM","Duncan's Landing","SM",{}),
]

# inline summaries for the 14 MPDF-addendum ports (sourced to the MPDF; the
# vault gazetteer addendum holds the fuller entries)
ADDENDUM = {
 3:("Wire chute built 1872 by Robert Anderson on Mistake Point at the mouth of Little Jackass Creek — one of the earliest wire chutes on the coast; abandoned 1883. Most business was tanbark, loaded by a cage lowered from the cliff landing stage.","Davidson 1889:289; California State Parks 2019, via the MPDF"),
 4:("Location unknown — south of Usal, possibly within Sinkyone Wilderness SP. Monroe Lumber Co. reportedly building a new pier at Devilbliss Ranch in 1904; newspaper cargoes of shingles, lumber, and laths 1905-1911. The alias 'Usal Landing' does NOT mean Usal wharf proper.","Jackson 1977; Carpenter & Millberry 1914:548-549; Ukiah Republican Press July 29, 1904, via the MPDF"),
 5:("Location unknown. In Jackson's doghole list with a wire chute; appears in SF shipping intelligence 1895-96 only. Named for George Devilbliss of Cottoneva Creek, lumberman and Westport storekeeper to 1895.","Jackson 1977:18; Carpenter & Millberry 1914, via the MPDF"),
 15:("One trough chute from the north shore at the mouth of Hare Creek, built c.1880 for Blumberg & Hardy's railroad-tie operation. Mooring buoys removed by 1885; the 1884 railroad from Hare Creek to Caspar's mill diverted the traffic; last shipment 1887.","Davidson 1889:287; Mendocino Beacon July 20, 2006; Carranco & Labbe 1975, via the MPDF"),
 16:("NEVER ACTIVE: a trough chute was built in 1884 on the south side of the tiny cove at the mouth of Bromley's Gulch (Jug Handle State Natural Reserve), but no shelter and no mooring anchors were ever placed, so no vessel ever used it. The coast's built-but-unused exemplar.","Davidson 1889:286; Jackson 1977, via the MPDF"),
 21:("Single trough chute at the mouth of Dark Gulch, under a mile north of Albion. Two schooners loaded in 1882, none in 1883; marked out of repair 1883 and dead by 1885. Newspaper cargoes were railroad ties only.","Davidson 1889:281, via the MPDF"),
 23:("Chute on the south side of Albion Cove built by settler William Handley (arrived 1865); on the 1872 and 1886 maps and in the 1889 Coast Pilot. One mooring anchor and four shore fasteners; loaded railroad ties and posts from surrounding mills.","Munro-Fraser 1880a; Davidson 1889:280; Peterson 1886, via the MPDF"),
 27:("Single trough chute ('Chisholm chute' on the 1870 USC&GS survey) running from the cliff across the water to a rocky island, between Greenwood Landing and Cuffey's Cove. Already inactive when Davidson described it in 1889.","1870 USC&GS T-sheet; Davidson 1889:277, via the MPDF"),
 29:("An abandoned trough chute one-third of a mile northwest of Uncle Abe's Landing, already torn down when Davidson recorded it in 1889. Nothing else is known, including its exact location.","Davidson 1889:275, via the MPDF"),
 30:("Single trough chute under a mile northwest of Elk Creek; two rock fasteners and two mooring anchors. Seven vessels loaded in 1882, one in 1883. Shipped lumber, shingles, posts, ties, firewood, and tanbark. Not on historic charts; exact location unknown.","Davidson 1889:275, via the MPDF"),
 34:("Location undetermined. Jackson places it a mile north of Scott's; the 1889 chart 661 shows one unnamed trough chute about two miles south of Arena Cove. SF newspapers record schooners loading railroad ties, posts, and cordwood 1871-74.","Jackson 1977:18; USC&GS chart 661 (1889), via the MPDF"),
 35:("Location undetermined. A 20-year franchise of 100 ft of shore was granted to Lew Gerlock in 1870. Jackson places it north of Saunders'; shares the same unnamed-chute chart evidence as Buster's — possibly the same site.","Jackson 1977:18; Munro-Fraser 1880a; USC&GS chart 661 (1889), via the MPDF"),
 44:("A modified wire chute with a steam-powered swinging boom, built in the 1880s by farmer Joe Tongue of Gualala on leased Rutherford ranch land (Sea Ranch area); shipped grain and fruit. Candidate site: the end of Fish Rock Road behind Rutherford's barn. The farm-cargo edge case of the chute system.","Clark 2016; Clark 2009:17, via the MPDF"),
 51:("Landing or anchorage (possibly a wire chute) at Stockhoff Cove, now Stillwater Cove Regional Park. The Stockhoff homestead (late 1860s) lived by lumbering, ranching, and farming; potatoes and produce loaded here or at neighboring chutes.","Rudy 2009:55; Rudy 2015:40, via the MPDF"),
}

features = []
unlocated = []

def gaz_for(no, key, src):
    if src == "SM": return GAZ_SM.get(key)
    if src == "NC": return GAZ_NC.get(key)
    return None

def p3_for(key, src):
    if src == "SM": return P3_SM.get(key)
    if src == "NC": return P3_NC.get(key)
    return None

def build_sources(gaz, extra_mpdf=True):
    out = []
    for s in (gaz.get("sources") if gaz else []) or []:
        e = {"citation": ("[P] " if s.get("type") == "primary" else "") + s["citation"], "ca_record": None, "ia_leaf_url": None}
        if s.get("url"): e["url"] = s["url"]
        out.append(e)
    if extra_mpdf and not any("MPDF" in s["citation"] or "Doghole Ports" in s["citation"] for s in out):
        out.append({"citation": MPDF, "ca_record": None, "ia_leaf_url": None, "url": MPDF_URL})
    return out

for (no, name, aliases, first, last, cls, gk, gsrc, pk, psrc, flags) in CANON:
    gaz = gaz_for(no, gk, gsrc)
    if gk and gaz is None:
        sys.exit(f"JOIN FAIL: gazetteer key not found for #{no} {name}: {gk!r}")
    p3 = p3_for(pk, psrc)
    if pk and p3 is None:
        sys.exit(f"JOIN FAIL: p3 key not found for #{no} {name}: {pk!r}")
    disp_name = name + (" (" + ", ".join(aliases[:2]) + ")" if aliases else "")
    layer, radius, cls_label = CLASSES[cls]
    dates_disp = ("never used" if flags.get("never_active")
                  else "c.%s–%s" % (first if first else "?", last))
    entry = {
        "id": slug(name), "name": disp_name, "type": "port",
        "layer": layer, "radius": radius,
        "port_class": cls_label,
        "canon_no": no,
        "date": date_of(first, last, dates_disp),
        "active": {"first": first, "last": last},
        "aliases": aliases,
    }
    if flags.get("never_active"):
        entry["port_class"] = cls_label
        entry["tags"] = ["never-active"]
    if gaz:
        entry["coords"] = p3["coords"]
        entry["coord_precision"] = p3["precision"]
        entry["summary"] = gaz["summary"]
        entry["cargo"] = cargo_of(gaz.get("products"))
        entry["company"] = companies_of(gaz.get("companies"))
        facts = []
        if gaz.get("loading_method"): facts.append(["Loading", gaz["loading_method"]])
        if gaz.get("wharf") and gaz["wharf"].lower() not in ("no", "unknown"):
            facts.append(["Wharf/pier", gaz["wharf"]])
        if gaz.get("railroad") and "none" not in gaz["railroad"].lower():
            facts.append(["Rail", gaz["railroad"]])
        if gaz.get("companies"): facts.append(["Operators", "; ".join(gaz["companies"])])
        entry["facts"] = facts
        entry["sources"] = build_sources(gaz)
        notes = []
        if gaz.get("confidence_notes"): notes.append(gaz["confidence_notes"])
        notes.append("Coordinate source: " + p3["coord_source"])
        entry["notes"] = " ".join(notes)
    elif no in ADDENDUM:
        summary, cite = ADDENDUM[no]
        entry["summary"] = summary
        entry["cargo"] = cargo_of([summary])
        entry["company"] = companies_of([summary])
        entry["facts"] = []
        entry["sources"] = [{"citation": cite, "ca_record": None, "ia_leaf_url": None},
                            {"citation": MPDF, "ca_record": None, "ia_leaf_url": None, "url": MPDF_URL}]
        if p3:
            entry["coords"] = p3["coords"]
            entry["coord_precision"] = p3["precision"]
            entry["notes"] = "Coordinate source: " + p3["coord_source"]
        entry.setdefault("notes", "")
    if flags.get("unlocated"):
        entry.pop("coords", None); entry.pop("coord_precision", None)
        entry.pop("layer", None); entry.pop("radius", None)
        entry["reason"] = "Exact location unknown or undetermined (MPDF); shown here, not pinned on the map."
        unlocated.append(entry)
        continue
    if "coords" not in entry or not entry["coords"]:
        sys.exit(f"BUILD FAIL: #{no} {name} has no coords and is not marked unlocated")
    w = WRECKS.get(entry["id"])
    if w:
        entry["facts"].append(["Recorded wrecks", f"{w} historic vessel losses near the landing (MPDF inventory)"])
        entry["wreck_count"] = w
    features.append(entry)

# ---------------- non-canonical ports (north/central/southern + receiving) ----------------
# (gaz name key | None, p3 key, class, layer override, extra note)
NC_PORTS = [
 ("Shelter Cove", "Shelter Cove pier site", "pier", None, None),
 ("Mattole Wharf (Sea Lion Rock)", "Mattole Wharf (Sea Lion Rock)", "pier", None, None),
 ("Eureka (Humboldt Bay) - the deepwater lumber capital", "Eureka waterfront (historic mill district)", "deepwater", None, None),
 ("Bucksport", "Bucksport", "deepwater", None, None),
 ("Fields Landing", "Fields Landing (Humboldt Bay)", "deepwater", None,
  "Not to be confused with 'Field's Landing', an alias of Bridgeport Landing on the Mendocino coast."),
 ("Samoa", "Samoa mill", "deepwater", None, None),
 ("Arcata Wharf", "Arcata Wharf (2-mi wharf across the flats)", "deepwater", None, None),
 ("Trinidad", "Trinidad wharf (Hooper's Wharf) / harbor", "pier", None, None),
 ("Klamath River mouth / Requa", "Requa / Klamath mouth", "river-bar", None, None),
 ("Crescent City", "Crescent City wharf (Hobbs Wall)", "deepwater", None, None),
 ("Smith River (mouth)", "Smith River mill site", "river-bar", None, None),
 ("Bolinas", "Bolinas (Bolinas Lagoon schooner channel)", "river-bar", None, None),
 ("Corte Madera Creek landings (Ross Landing / Baltimore wharf)", "Corte Madera / Ross Landing", "river-bar", None, None),
 ("Tomales (Keys Creek)", "Tomales (Keys Creek head of navigation)", "river-bar", None, None),
 ("Año Nuevo (Point New Year Wharf / Crescent Bay-Cove Beach)", "Año Nuevo / New Year's Point wharf", "pier", None,
  "One structure with two names: Davidson 1889 explicitly equates the Point New Year Wharf with 'Waddell's Landing.'"),
 ("Pigeon Point (+ Gazos Creek traffic)", "Pigeon Point chute/wharf", "pier", None, None),
 ("Gordon's Chute (Tunitas Creek)", "Gordon's Chute (Tunitas Creek)", "chute", None, None),
 ("Davenport Landing", "Davenport Landing", "pier", None, None),
 ("Santa Cruz wharves", "Santa Cruz wharves (Railroad Wharf / Powder Mill Wharf area)", "deepwater", None, None),
 ("Redwood City embarcadero (bayside reference point)", None, "river-bar", None, None),
 ("San Simeon", "San Simeon wharf", "pier", None, None),
 ("Leffingwell Landing (Cambria)", "Leffingwell Landing (Cambria)", "chute", None, None),
 ("San Francisco lumber wharves and yards (the receiving end)", "SF Mission Creek / Channel St lumber district", "deepwater", "receiving",
  "E.K. Wood's docks at the head of Channel/Mission Creek are where C.A. Thayer discharged her Grays Harbor cargoes, including in June 1906 two months after the earthquake."),
 ("Oakland (estuary lumber yards)", "Oakland E.K. Wood lumber yard (estuary)", "deepwater", "receiving", None),
]
REDWOOD_CITY = [37.50188, -122.22232]  # GNIS 277556 Redwood City PP; embarcadero at Redwood Creek

for (gk, pk, cls, layer_override, note) in NC_PORTS:
    gaz = GAZ_NC.get(gk)
    if gaz is None:
        sys.exit(f"JOIN FAIL (NC): gazetteer key not found: {gk!r}")
    p3 = P3_NC.get(pk) if pk else None
    if pk and p3 is None:
        sys.exit(f"JOIN FAIL (NC): p3 key not found: {pk!r}")
    layer, radius, cls_label = CLASSES[cls]
    if layer_override: layer = layer_override
    coords = p3["coords"] if p3 else REDWOOD_CITY
    prec = p3["precision"] if p3 else "area"
    nm = gaz["name"].split(" - ")[0]
    entry = {
        "id": slug(nm), "name": nm, "type": "port",
        "layer": layer, "radius": radius, "port_class": cls_label,
        "coords": coords, "coord_precision": prec,
        "date": date_of(None, None, gaz.get("active_years", "dates uncertain")),
        "summary": gaz["summary"],
        "cargo": cargo_of(gaz.get("products")),
        "company": companies_of(gaz.get("companies")),
        "facts": [], "sources": build_sources(gaz, extra_mpdf=False),
    }
    yrs = [int(y) for y in re.findall(r"1[89]\d\d", gaz.get("active_years", ""))]
    if yrs:
        # first = the stated opening year; last = the LATEST year in the string
        # (a trailing parenthetical about an earlier mill must not become the end date)
        entry["date"]["iso"] = str(yrs[0])
        entry["active"] = {"first": yrs[0], "last": max(yrs) if max(yrs) > yrs[0] else None}
    if gaz.get("loading_method"): entry["facts"].append(["Loading", gaz["loading_method"]])
    if gaz.get("wharf") and str(gaz["wharf"]).lower() not in ("no", "unknown"):
        entry["facts"].append(["Wharf/pier", gaz["wharf"]])
    if gaz.get("railroad") and "none" not in str(gaz.get("railroad", "")).lower():
        entry["facts"].append(["Rail", gaz["railroad"]])
    if gaz.get("companies"): entry["facts"].append(["Operators", "; ".join(gaz["companies"])])
    notes = [gaz.get("confidence_notes") or ""]
    if p3: notes.append("Coordinate source: " + p3["coord_source"])
    if note: notes.append(note)
    entry["notes"] = " ".join(n for n in notes if n)
    if "thayer" in (entry["notes"] + entry["summary"]).lower() or "Thayer" in (note or ""):
        entry.setdefault("tags", []).append("thayer")
    features.append(entry)

# Bodega Bay + Usal: in the Sonoma-Mendocino gazetteer but OUTSIDE the canonical 57
for (gk, pk, cls, first, last, extra_note) in [
    ("Bodega Bay", "Bodega Bay (Bodega Port village site)", "river-bar", 1843, 1900,
     "Not one of the MPDF's 57 doghole ports; a lagoon anchorage rather than a chute port. "
     "Its lumber significance is early: Stephen Smith's 1843 steam sawmill, California's first."),
    ("Usal", "Usal", "pier", 1889, 1902,
     "Not one of the MPDF's 57 (its 'Usal Landing' is an alias of Monroe Landing, a different site). "
     "Robert Dollar's purchase of the Usal operation in 1894 and the steam schooner Newsboy he bought "
     "to serve it were the seed of the Dollar Steamship empire."),
]:
    gaz = GAZ_SM.get(gk)
    if gaz is None:
        sys.exit(f"JOIN FAIL (extra): gazetteer key not found: {gk!r}")
    p3 = P3_SM.get(pk)
    if p3 is None:
        sys.exit(f"JOIN FAIL (extra): p3 key not found: {pk!r}")
    layer, radius, cls_label = CLASSES[cls]
    entry = {
        "id": slug(gk), "name": gaz["name"], "type": "port",
        "layer": layer, "radius": radius, "port_class": cls_label,
        "coords": p3["coords"], "coord_precision": p3["precision"],
        "date": date_of(first, last, "c.%s–%s" % (first, last)),
        "active": {"first": first, "last": last},
        "summary": gaz["summary"],
        "cargo": cargo_of(gaz.get("products")),
        "company": companies_of(gaz.get("companies")),
        "facts": [], "sources": build_sources(gaz, extra_mpdf=False),
    }
    if gaz.get("loading_method"): entry["facts"].append(["Loading", gaz["loading_method"]])
    if gaz.get("wharf") and str(gaz["wharf"]).lower() not in ("no", "unknown"):
        entry["facts"].append(["Wharf/pier", gaz["wharf"]])
    if gaz.get("railroad") and "none" not in str(gaz.get("railroad", "")).lower():
        entry["facts"].append(["Rail", gaz["railroad"]])
    if gaz.get("companies"): entry["facts"].append(["Operators", "; ".join(gaz["companies"])])
    entry["notes"] = extra_note + " Coordinate source: " + p3["coord_source"]
    features.append(entry)

# Port Kenyon (from the completeness critique; not in the gazetteer sweep)
features.append({
    "id": "port-kenyon", "name": "Port Kenyon (Salt River, Ferndale)", "type": "port",
    "layer": "class-river-bar", "radius": 8, "port_class": "river bar harbor",
    "coords": P3_NC["Port Kenyon (Salt River nr Ferndale)"]["coords"], "coord_precision": "place",
    "date": date_of(1876, 1909, "c.1876–1900s"), "active": {"first": 1876, "last": 1909},
    "summary": "River port on the Salt River near Ferndale, founded 1876 by John Gardner Kenyon, with wharf and warehouses from August 1876 and regular steamer traffic (the Thos. A. Whitelaw was built in 1878 for this trade). The town had a lumber mill, but the cargo was predominantly Eel-delta dairy; silting of the Salt and Eel rivers killed the port. Included under the all-landings rule with its cargo stated honestly.",
    "cargo": ["farm produce", "redwood lumber"], "company": [],
    "facts": [["Cargo note", "predominantly dairy/butter; mill town, lumber secondary"]],
    "sources": [
        {"citation": "Cal Poly Humboldt Special Collections, 'Brief History of Port Kenyon'", "url": "https://www.humboldt.edu/special-collections/brief-history-port-kenyon", "ca_record": None, "ia_leaf_url": None},
        {"citation": "Wikipedia, 'Port Kenyon, California'", "url": "https://en.wikipedia.org/wiki/Port_Kenyon,_California", "ca_record": None, "ia_leaf_url": None}],
    "notes": "Coordinate source: " + P3_NC["Port Kenyon (Salt River nr Ferndale)"]["coord_source"],
})

# Big Sur tanbark landings (from the completeness critique; period confirmation pending)
features.append({
    "id": "notleys-landing", "name": "Notley's Landing (Palo Colorado)", "type": "port",
    "layer": "class-chute", "radius": 5, "port_class": "chute-only doghole",
    "coords": P3_NC["Notley's Landing (Palo Colorado mouth)"]["coords"], "coord_precision": "place",
    "date": date_of(1898, 1907, "c.1898–1907"), "active": {"first": 1898, "last": 1907},
    "summary": "Doghole landing at the Palo Colorado River mouth built by William and Godfrey Notley; a village stood here 1898-1907, with heavy use 1903-1907 shipping tanbark and lumber by cable and chute to schooners including the Confianza and Acme. The settlement emptied once the surrounding slopes were cut over.",
    "cargo": ["tanbark", "redwood lumber"], "company": ["Notley brothers"],
    "facts": [["Loading", "cable/chute over the shore rocks"]],
    "sources": [
        {"citation": "Wikipedia, 'Notleys Landing, California'", "url": "https://en.wikipedia.org/wiki/Notleys_Landing,_California", "ca_record": None, "ia_leaf_url": None},
        {"citation": "SFGate, 'Big Sur Trust buys historic overlook / Notley's Landing was important in timber trade'", "url": "https://www.sfgate.com/bayarea/article/Big-Sur-Trust-buys-historic-overlook-Notley-s-2919451.php", "ca_record": None, "ia_leaf_url": None}],
    "notes": "Secondary sourcing; period-source confirmation still pending (Coast Pilot 1909 southern pages, Monterey county histories). Coordinate source: " + P3_NC["Notley's Landing (Palo Colorado mouth)"]["coord_source"],
})
features.append({
    "id": "partington-cove", "name": "Partington Cove (Big Sur)", "type": "port",
    "layer": "class-chute", "radius": 5, "port_class": "chute-only doghole",
    "coords": P3_NC["Partington Cove"]["coords"], "coord_precision": "place",
    "date": date_of(1880, 1900, "c.1880s–1890s"), "active": {"first": 1880, "last": 1900},
    "summary": "John Partington's tanbark landing of the 1880s: a 200-foot tunnel cut through the headland to a timber ship's landing bolted to the bedrock of the west cove, from which tanoak bark from the canyons above was slung to waiting coasters. Structural remnants survive in Julia Pfeiffer Burns State Park.",
    "cargo": ["tanbark"], "company": [],
    "facts": [["Loading", "tunnel + hoist/chute to a rock-bolted landing"]],
    "sources": [{"citation": "Convergent popular accounts (hikinginbigsur.com; Lonely Planet; CA State Parks interpretive material)", "url": "https://hikinginbigsur.com/hikes_partingtoncove.html", "ca_record": None, "ia_leaf_url": None}],
    "notes": "Popular sourcing only; verify dates against Monterey county histories before citing in print. Coordinate source: " + P3_NC["Partington Cove"]["coord_source"],
})

# ---------------- shipyards + feeder mills (industry layer) ----------------
features.append({
    "id": "bendixsen-shipyard-fairhaven", "name": "Bendixsen shipyard, Fairhaven — birthplace of C.A. Thayer", "type": "shipyard",
    "layer": "industry", "radius": 6,
    "coords": P3_NC["Fairhaven / Bendixsen shipyard site (North Spit)"]["coords"], "coord_precision": "place",
    "date": date_of(1875, 1920, "1875–c.1920"), "active": {"first": 1875, "last": 1920},
    "summary": "Hans Ditlev Bendixsen's yard on the North Spit built over one hundred vessels for the lumber trade — 39 two-masted, 35 three-masted, and 11 four-masted schooners among them. The three-masted schooner C.A. Thayer, launched here 9 July 1895 for the E.K. Wood Lumber Co., survives at San Francisco's Hyde Street Pier as the last of the West Coast sailing lumber fleet.",
    "cargo": [], "company": ["Bendixsen shipyard", "E.K. Wood Lumber Co."],
    "facts": [["Output", "100+ vessels incl. 85 lumber schooners (Kortum, in Martin 1983)"], ["C.A. Thayer", "launched 2:09 pm, 9 July 1895; 453 GT; 575,000 board feet capacity"]],
    "sources": [
        {"citation": "HAER No. CA-61, C.A. Thayer (1988), data pages, quoting Daily Humboldt Times, July 10, 1895", "url": "https://www.loc.gov/item/ca1201/", "ca_record": None, "ia_leaf_url": None},
        {"citation": "Karl Kortum, foreword to Wallace E. Martin, comp., Sail and Steam on the Northern California Coast (1983)", "ca_record": None, "ia_leaf_url": None}],
    "tags": ["thayer"],
    "notes": "Coordinate source: " + P3_NC["Fairhaven / Bendixsen shipyard site (North Spit)"]["coord_source"],
})
features.append({
    "id": "peterson-shipyard-little-river", "name": "Thomas Peterson shipyard, Little River", "type": "shipyard",
    "layer": "industry", "radius": 6,
    "coords": P3_NC["Thomas Peterson shipyard, Little River"]["coords"], "coord_precision": "area",
    "date": date_of(1868, 1885, "c.1868–1880s"), "active": {"first": 1868, "last": 1885},
    "summary": "Thomas H. Peterson, 'Dean of Mendocino County shipbuilders,' built two-masted lumber schooners on the shore of Little River cove in the 1868-1879 years — thirteen doghole schooners launched from a beach yard directly below the bluff, for the very trade the cove's chutes served.",
    "cargo": [], "company": [],
    "facts": [["Output", "13 two-masted schooners, 1868–1879 (NOAA GFNMS; Kelley House)"]],
    "sources": [
        {"citation": "NOAA GFNMS doghole-ports pages (Little River shipbuilding)", "url": "https://farallones.noaa.gov/heritage/doghole.html", "ca_record": None, "ia_leaf_url": None},
        {"citation": "Louis Hough, 'Thomas H. Petersen, Master Shipbuilder' (Kelley House Museum, 2015)", "ca_record": None, "ia_leaf_url": None}],
    "notes": "Coordinate source: " + P3_NC["Thomas Peterson shipyard, Little River"]["coord_source"],
})
FEEDERS = [
 ("DeHaven", [39.66016, -123.78502], "GNIS 1658380 DeHaven (populated place)", "Westport Landing",
  "Mill settlement at DeHaven Creek. The MPDF is explicit that lumber from the DeHaven-area mills was hauled to Westport Landing for shipment — no chute of its own."),
 ("Howard Creek", [39.67794, -123.79085], "GNIS 225696 Howard Creek mouth (Westport quad)", "Union Landing / Westport",
  "Mills on Howard Creek (c.1903-1924); output moved by rail to Union Landing and by road to Westport — a feeder site, not a port."),
 ("Schooner Gulch", [38.86660, -123.65554], "GNIS 232695 Schooner Gulch (valley mouth)", "Saunders' Landing",
  "Despite the name, the MPDF (citing Davidson 1889:268) records that lumber from the Schooner Gulch mill was moved to Saunders' Landing for loading — a feeder mill, not a loading site."),
]
for (nm, coords, src, via, summary) in FEEDERS:
    features.append({
        "id": slug(nm) + "-feeder", "name": nm + " (feeder mill — shipped via " + via + ")",
        "type": "feeder-mill", "layer": "industry", "radius": 4,
        "coords": coords, "coord_precision": "place",
        "date": date_of(None, None, "see summary", "circa"),
        "summary": summary, "cargo": [], "company": [],
        "facts": [["Shipped via", via]],
        "sources": [{"citation": MPDF + " (feeder attribution: Davidson 1889; Sullenberger 1980)", "url": MPDF_URL, "ca_record": None, "ia_leaf_url": None}],
        "notes": "Coordinate source: " + src,
    })
# Big Lagoon: rail-served logging outpost, no ocean shipping (registered null)
big_lagoon = GAZ_NC.get("Big Lagoon")
if big_lagoon:
    features.append({
        "id": "big-lagoon-feeder", "name": "Big Lagoon (logging outpost — no ocean shipping)",
        "type": "feeder-mill", "layer": "industry", "radius": 4,
        "coords": [41.16537, -124.12823], "coord_precision": "area",
        "date": date_of(1908, 1945, "c.1908–1945"), "active": {"first": 1908, "last": 1945},
        "summary": big_lagoon["summary"], "cargo": [], "company": companies_of(big_lagoon.get("companies")),
        "facts": [["Status", "rail-served logging outpost; NOT an ocean shipping point"]],
        "sources": build_sources(big_lagoon, extra_mpdf=False),
        "notes": "Coordinate = GNIS Big Lagoon (waterbody) vicinity; included to preempt the assumption that every named coastal lumber site shipped by sea.",
    })

# ---------------- lighthouses (context layer) ----------------
LIGHTS = [
 ("Point Arena Lighthouse", "Point Arena Lighthouse", 1870,
  "First lit 1 May 1870, sited after the surge of Mendocino-coast wrecks in the 1860s; rebuilt after the 1906 earthquake. The tall tower marks the turning point of the doghole coast.",
  "USCG Historian's Office; lighthousefriends.com (ID 65)"),
 ("Trinidad Head Lighthouse", "Trinidad Head Lighthouse", 1871,
  "First lit December 1871 as Trinidad became an important lumber-shipping roadstead; the little tower still stands on the head above the wharf site.",
  "Trinidad Museum; USCG Historian's Office; lighthousefriends.com (ID 61)"),
 ("St. George Reef Lighthouse", "St. George Reef Lighthouse (Northwest Seal Rock)", 1892,
  "Built 1882-92 on Northwest Seal Rock after the sidewheeler Brother Jonathan was lost on the reef in 1865 with some 225 lives — the costliest American lighthouse of its day ($752,000), its granite quarried and finished on Humboldt Bay.",
  "Del Norte County Historical Society; lighthousefriends.com (ID 26); NR #93001373"),
 ("Point Cabrillo Lighthouse", "Point Cabrillo Lighthouse", 1909,
  "First lit 10 June 1909, built — in the station's own words — to protect the doghole schooners of the redwood trade; it stands beside Frolic Cove, where the 1850 wreck of the brig Frolic set off the discovery of the Mendocino timber.",
  "Point Cabrillo Light Station (pointcabrillo.org); U.S. Lighthouse Society Keeper's Log"),
 ("Punta Gorda Lighthouse", "Punta Gorda Lighthouse", 1912,
  "Lit 15 January 1912 after a decade of Lost Coast wrecks, including the 1907 collision that sank the liner Columbia with the lumber steamer San Pedro off Shelter Cove; abandoned 1951, the tower still stands on the loneliest stretch of the coast.",
  "lighthousefriends.com (ID 63); historic-structures.com"),
]
for (nm, p3key, yr, summary, cite) in LIGHTS:
    p3 = P3_NC[p3key.split(" (")[0]] if p3key.split(" (")[0] in P3_NC else P3_NC.get(p3key)
    if p3 is None:
        # keys in P3_NC use base names
        base = {"Point Arena Lighthouse": "Point Arena Lighthouse",
                "Trinidad Head Lighthouse": "Trinidad Head Lighthouse",
                "St. George Reef Lighthouse": "St. George Reef Lighthouse (Northwest Seal Rock)",
                "Point Cabrillo Lighthouse": "Point Cabrillo Lighthouse",
                "Punta Gorda Lighthouse": "Punta Gorda Lighthouse"}[nm]
        p3 = P3_NC[base]
    features.append({
        "id": slug(nm), "name": nm, "type": "lighthouse", "layer": "lighthouses", "radius": 5,
        "coords": p3["coords"], "coord_precision": p3["precision"],
        "date": date_of(yr, None, "first lit " + str(yr), "year"),
        "summary": summary, "sources": [{"citation": cite, "ca_record": None, "ia_leaf_url": None}],
        "notes": "Coordinate source: " + p3["coord_source"],
    })

# ---------------- railroads (routes) ----------------
# Real-corridor geometry (rigor pass 2026-09-13): join by explicit prefix mapping,
# old p3 route name -> new rail-alignments name. "Fort Bragg Railroad 1885" folds
# into the Glen Blair branch notes (same Pudding Creek trackage origin).
PATHS = {}
_rp = load("rigor-rails.json")["routes"]
_by_new = {r["name"]: r for r in _rp}
PATH_JOIN = {
    "Bear Harbor & Eel River Railroad (Bear Harbor Lumber Co. → Southern Humboldt Lumber Co.)": "Bear Harbor & Eel River Railroad",
    "California Western Railroad (ex-Fort Bragg Railroad; the Skunk Train)": "California Western Railroad (Fort Bragg-Willits)",
    "Caspar, South Fork & Eastern Railroad (Caspar Lumber Co.; ex-Jughandle RR, ex-Caspar & Hare Creek RR)": "Caspar, South Fork & Eastern Railroad",
    "Mendocino Lumber Co. Railroad (Big River)": "Mendocino Lumber Co. Railroad (Big River)",
    "Albion Lumber Co. line / Albion & Southeastern / Fort Bragg & Southeastern (Albion River to Wendling)": "Albion & Southeastern / Albion River Railroad",
    "Glen Blair branch (Fort Bragg Railroad 1885 / Glen Blair Lumber Co., junction with CWR)": "Glen Blair Redwood Co. Railroad",
    "Usal Railroad (Usal Redwood Co. / Robert Dollar)": "Usal Railroad",
    "Crescent City & Smith River Railroad (Hobbs, Wall & Co.)": "Crescent City & Smith River Railroad (Hobbs Wall)",
    "Arcata & Mad River Railroad (ex-Union Plank Walk, Rail Track & Wharf Co.)": "Arcata & Mad River Railroad",
    "Humboldt Bay & Eel River Railroad / Pacific Lumber Co. (Scotia-Alton-Humboldt Bay)": "Humboldt Bay & Eel River Railroad / Pacific Lumber",
    "Dolbeer & Carson Lumber Co. — Bucksport & Elk River Railroad": "Dolbeer & Carson / Bucksport & Elk River Railroad",
    "Salt Point horse railroad (quarry/mill to Gerstle Cove landing)": "Salt Point horse tramway",
    "Duncan's Landing horse tram (Duncans Mills Land & Lumber Co., Wright Ranch)": "Duncan's Landing horse tram",
    "North Pacific Coast Railroad (Sausalito-Duncans Mills narrow gauge)": "North Pacific Coast Railroad (Sausalito-Duncans Mills)",
}
for old_name, new_name in PATH_JOIN.items():
    if new_name not in _by_new:
        sys.exit(f"RAIL JOIN FAIL: {new_name!r} missing from rigor-rails.json")
    PATHS[old_name] = _by_new[new_name]

routes = []
RAIL_COLOR = "#7f2020"
for r in RAILS:
    stops = []
    for w in r["waypoints"]:
        if not w.get("coords"): continue
        stops.append({
            "id": slug(r["name"])[:40] + "-" + slug(w["name"])[:40],
            "name": w["name"], "type": "rail-point", "coords": w["coords"],
            "coord_precision": "place",
            "date": date_of(None, None, r["years"][:60], "circa"),
            "summary": w["name"] + ".",
            "notes": "Waypoint source: " + w["source"],
        })
    if len(stops) < 2: continue
    entry = {
        "id": slug(r["name"])[:60],
        "label": r["name"] + " — " + r["gauge"].split("—")[0].strip()[:60],
        "layer": "rails", "color": RAIL_COLOR,
        "path_confidence": ("documented" if r["path_confidence"].startswith("documented") else "reconstructed"),
        "citation": "; ".join(r["sources"])[:400],
        "stops": stops,
        "notes": (r.get("notes") or "")[:500],
    }
    rp = PATHS.get(r["name"])
    if rp:
        entry["path"] = rp["path"]
        entry["path_confidence"] = rp["confidence"] if rp["confidence"] in ("documented", "reconstructed", "conjectural") else entry["path_confidence"]
        entry["citation"] = ("; ".join(rp["sources"] + r["sources"]))[:500]
        entry["notes"] = ("Alignment: " + rp["path_source"][:260] + ". " + (rp.get("notes") or "")[:200] + " " + (r.get("notes") or ""))[:700]
    routes.append(entry)

# ---------------- Reed's sawmill: the Mexican-period prelude (rigor pass 2026-09-13) ----------------
features.append({
    "id": "reeds-sawmill-mill-valley", "name": "Reed's Sawmill (Rancho Corte Madera del Presidio) — the Mexican-period prelude",
    "type": "mill", "layer": "industry", "radius": 6,
    "coords": [37.9056, -122.5522], "coord_precision": "place",
    "date": {"iso": "1834", "display": "c.1834–1843 (construction date disputed)", "confidence": "circa"},
    "active": {"first": 1834, "last": 1849},
    "summary": ("The first sawmill in Marin County: John Thomas Reed (Juan Read), grantee of Rancho Corte Madera "
        "del Presidio (Figueroa, 2 Oct 1834), built a water-powered sash-saw mill in the ravine of Cascade Creek. "
        "Its construction date is genuinely disputed: the landmark tradition (CHL No. 207) says about 1833-34, "
        "while Munro-Fraser's detailed 1880 account says Reed 'erected his saw-mill in 1843, and had but just got "
        "it in operation when he died' — cutting lumber for his own adobe. The rancho's name ('cut wood for the "
        "Presidio') records the older pre-grant woodcutting trade that supplied timbers to the Presidio and Yerba "
        "Buena, not the mill's output. No Mexican-period landing or embarcadero for the mill is attested; the "
        "documented rafting of Richardson Bay timber is American-period (1849 on). The structure standing in Old "
        "Mill Park today is a 1991 reconstruction."),
    "cargo": ["redwood lumber"], "company": [],
    "facts": [["Mill type", "water-powered sash saw (Munro-Fraser 1880:388-389)"],
               ["Grant", "Rancho Corte Madera del Presidio, 2 Oct 1834; judicial possession 28 Nov 1835 (Hoffman's Reports, Land Case 183 ND)"],
               ["Date dispute", "c.1833-34 (CHL 207, 1935) vs 1843 (Munro-Fraser 1880 township chapter)"]],
    "sources": [
        {"citation": "[P] Hoffman's Reports of Land Cases (1862), U.S. v. Heirs of Juan Read, quoted in Munro-Fraser 1880:189", "ca_record": None, "ia_leaf_url": None},
        {"citation": "J.P. Munro-Fraser, History of Marin County (San Francisco: Alley, Bowen & Co., 1880), pp. 110-111, 385-389", "url": "https://archive.org/details/historyofmarinco00munr", "ca_record": None, "ia_leaf_url": None},
        {"citation": "Bancroft, History of California, V, Pioneer Register, s.v. 'Read (John)'", "ca_record": None, "ia_leaf_url": None},
        {"citation": "California Historical Landmark No. 207 (registered 20 June 1935); Mill Valley Historic Resources Inventory (2021), fn. 7", "ca_record": None, "ia_leaf_url": None}],
    "notes": ("Coordinate = the reconstructed mill in Old Mill Park (the original site 'in the ravine' is conventionally "
        "identified with it; the CHL plaque stands elsewhere, at Blithedale Ave & Tower Dr — do not confuse). Both "
        "rancho diseños examined (Bancroft Land Case Maps) show no molino and no landing. Full dossier in the project research files."),
    "tags": ["mexican-period"],
})

# ---------------- source upgrades from the audit (rigor pass 2026-09-13) ----------------
_audit = load("rigor-audit.json")["weak_features"]
_by_id = {f["id"]: f for f in features}
_missing_audit = [w["id"] for w in _audit if w["id"] not in _by_id]
if _missing_audit:
    sys.exit("AUDIT JOIN FAIL: unknown ids: " + ", ".join(_missing_audit))
for w in _audit:
    f = _by_id[w["id"]]
    have = {s["citation"] for s in f["sources"]}
    for s in w["better_sources"]:
        cite = ("[P] " if s["type"].startswith("primary") or s["type"] == "P" else "[S] ") + s["citation"]
        if cite not in have:
            e = {"citation": cite, "ca_record": None, "ia_leaf_url": None}
            if s.get("url"): e["url"] = s["url"]
            f["sources"].append(e)
# audit page-cite correction: Mattole's Davidson reference
mf = _by_id.get("mattole-wharf-sea-lion-rock")
if mf:
    for s in mf["sources"]:
        s["citation"] = s["citation"].replace("p. ~280", "pp. ~300-301 (page cite corrected in the 2026-09-13 audit)")
# Corte Madera feature: hedge the Reed mill date per the rigor findings
cm = _by_id.get("corte-madera-creek-landings-ross-landing-baltimore-wharf")
if cm:
    cm["notes"] = (cm.get("notes", "") + " Reed's mill date is disputed (c.1834 landmark tradition vs 1843 in "
                   "Munro-Fraser's detailed account) — see the Reed's Sawmill feature.")

# ---------------- photos (optional overlay: photos.json in this dir) ----------------
# {feature_id: {"url": direct-or-repo-relative, "credit": "...", "date": "...", "rights": "...", "modern": bool}}
photos_path = os.path.join(HERE, "photos.json")
if os.path.exists(photos_path):
    photos = json.load(open(photos_path))
    by_id = {f["id"]: f for f in features}
    missing = [k for k in photos if k not in by_id]
    if missing:
        sys.exit("PHOTO JOIN FAIL: unknown feature ids: " + ", ".join(missing))
    for fid, p in photos.items():
        cred = p["credit"] + ((" · " + p["date"]) if p.get("date") else "")
        if p.get("modern"): cred += " (modern view)"
        by_id[fid]["photo"] = {"url": p["url"], "credit": cred, "alt": by_id[fid]["name"]}
    print(f"photos attached: {len(photos)}")

# ---------------- top level ----------------
era_presets = [
    {"label": "Pioneer era", "from": 1834, "to": 1869},
    {"label": "Chute boom", "from": 1870, "to": 1889},
    {"label": "Steam-schooner era", "from": 1890, "to": 1913},
    {"label": "Decline", "from": 1914, "to": 1945},
]

data = {
    "id": "lumber-ports",
    "title": "Lumber Ports of the California Coast",
    "subtitle": "Doghole chutes to deepwater harbors, c.1850–1940 — with the railroads that fed them",
    "abstract": ("Every documented lumber shipping point on the California coast, from chute-only "
        "dogholes where two-masted schooners moored under a cliff to the deepwater mills of Humboldt Bay — "
        "with the loading technology (trough chute, wire chute, pier), the operating companies, the cargo "
        "streams (sawn redwood, railroad ties, tanoak bark, split stuff, cordwood, Douglas fir, farm produce), "
        "the logging railroads that reached tidewater, and the lighthouses this deadly trade built. "
        "Pin size shows the four-tier port classification; filters cut by class, cargo, and company; era "
        "buttons snap the timeline to the trade's four periods. "
        "The Sonoma-Mendocino core follows the NRHP Northern California Doghole Ports Maritime Cultural "
        "Landscape inventory (57 ports, draft 2021) with dates keyed to the U.S. Coast Pilot editions "
        "(1869, 1889, 1909); dates are circa and lag reality by their source's edition. Coordinates carry "
        "per-pin provenance (GNIS records, Coast Pilot verbal geometry, NRHP archaeology) and were validated "
        "against the inventory's own north-to-south ordering and Davidson's stated inter-port distances. "
        "COVERAGE IS ASYMMETRIC: no inventory of comparable rigor exists for Humboldt, Del Norte, or the "
        "coast south of the Golden Gate; those zones are assembled from county histories, NPS studies, and "
        "the Coast Pilots, and are necessarily less complete. Six documented ports have no confirmed "
        "location and are deliberately not pinned: Monroe, Devilbliss, the Unnamed Landing near Uncle "
        "Abe's, Uncle Abe's, Buster's, and Scott's (the last two may be one site). "
        "The sailing lumber fleet these ports loaded survives in exactly one vessel: the schooner "
        "C.A. Thayer (Bendixsen yard, Fairhaven, 1895 — search 'thayer' to follow her thread), "
        "preserved at San Francisco's Hyde Street Pier. "
        "Full apparatus: see the Sources & Method page linked above the map."),
    "date_range": [1834, 1945],
    "center": [39.3, -123.0],
    "zoom": 7,
    "cite_key": "lumberports",
    "last_updated": "2026-09-13",
    "hover_labels": True,
    "layers": [
        {"id": "class-chute", "label": "Chute-only dogholes", "color": "#a67c52"},
        {"id": "class-pier", "label": "Dogholes with a pier", "color": "#8c4a2f"},
        {"id": "class-river-bar", "label": "River bar harbors", "color": "#2f7f6f"},
        {"id": "class-deepwater", "label": "Deepwater & major wharf ports", "color": "#1f4e79"},
        {"id": "rails", "label": "Lumber railroads to tidewater", "color": RAIL_COLOR},
        {"id": "lighthouses", "label": "Lighthouses of the trade", "color": "#c9a227", "default_off": True},
        {"id": "industry", "label": "Shipyards, mills & feeder sites", "color": "#6b4f82", "default_off": True},
        {"id": "receiving", "label": "The receiving end (SF Bay)", "color": "#556b2f"},
    ],
    "legend_note": ("Pin size = port class (doghole → deepwater). Dashed/hollow pins are approximate. "
        "Six documented ports with unknown locations are listed in the About panel, not pinned. "
        "Dashed rail lines are reconstructed corridors between documented points, not surveyed alignments."),
    "era_presets": era_presets,
    "attribute_filters": [
        {"key": "port_class", "label": "Port class",
         "values": ["chute-only doghole", "doghole with pier", "river bar harbor", "deepwater / major wharf"]},
        {"key": "cargo", "label": "Cargo",
         "values": ["redwood lumber", "railroad ties", "tanbark", "posts & split stuff",
                     "cordwood & firewood", "Douglas fir", "farm produce"]},
        {"key": "company", "label": "Company"},
    ],
    "features": features,
    "routes": routes,
    "unlocated": unlocated,
}

# ---------------- output gates ----------------
# Gate: canonical north->south monotonic latitude on OUR OWN OUTPUT
canon_feats = sorted([f for f in features if f.get("canon_no")], key=lambda f: f["canon_no"])
viol = []
prev = None
for f in canon_feats:
    lat = f["coords"][0]
    if prev and lat > prev[1] + 0.002:
        viol.append(f"{f['name']} ({lat}) north of {prev[0]}")
    prev = (f["name"], lat)
if viol:
    sys.exit("OUTPUT GATE FAIL (north->south): " + "; ".join(viol))

ids = [f["id"] for f in features] + [s["id"] for r in routes for s in r["stops"]]
dupes = {i for i in ids if ids.count(i) > 1}
if dupes:
    sys.exit("OUTPUT GATE FAIL (duplicate ids): " + ", ".join(sorted(dupes)))

json.dump(data, open(OUT, "w"), indent=1, ensure_ascii=False)
print(f"wrote {OUT}")
print(f"  features: {len(features)} ({len(canon_feats)} canonical) + {len(unlocated)} unlocated (listed, unpinned)")
print(f"  routes: {len(routes)} with {sum(len(r['stops']) for r in routes)} waypoints")
print("  north->south gate: PASS; unique-id gate: PASS")
