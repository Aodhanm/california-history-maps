#!/usr/bin/env python3
"""Rebuild data/native-california.json with REAL territory polygons from the
University of Redlands digitization of Handbook of North American Indians vol. 8
(ArcGIS item 3e2b6cd9d26c417eae75db31d6226afe, GCS NAD83). Douglas-Peucker
simplified for the web. Boundaries note: the Handbook's reconstruction, not exact."""
import json, os, re, unicodedata
import shapefile

import os as _os
SHP = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))), 'data-src', 'handbook-territories', 'ca_nativeamericanterritories')
REPO = os.path.expanduser("~/california-history-maps")

def dp(points, tol):
    """Douglas-Peucker on [(x,y)] with perpendicular-distance tolerance."""
    if len(points) < 3:
        return points
    def pd(p, a, b):
        (x, y), (x1, y1), (x2, y2) = p, a, b
        dx, dy = x2 - x1, y2 - y1
        if dx == dy == 0:
            return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
        px, py = x1 + t * dx, y1 + t * dy
        return ((x - px) ** 2 + (y - py) ** 2) ** 0.5
    dmax, idx = 0, 0
    for i in range(1, len(points) - 1):
        d = pd(points[i], points[0], points[-1])
        if d > dmax:
            dmax, idx = d, i
    if dmax > tol:
        left = dp(points[:idx + 1], tol)
        right = dp(points[idx:], tol)
        return left[:-1] + right
    return [points[0], points[-1]]

RENAME = {
    "Karok": "Karuk", "Grabrielino": "Tongva (Gabrielino)", "Gabrielino": "Tongva (Gabrielino)",
    "Diegueno": "Kumeyaay (Diegueño)", "Luiseno": "Luiseño", "Cupeno": "Cupeño",
    "Costanoan": "Ohlone (Costanoan)", "Juaneno": "Acjachemen (Juaneño)",
    "Cahuila": "Cahuilla", "Tubatulabal": "Tübatulabal",
}
FAM_LAYER = {"Athapaskan": "atha", "Hokan": "hokan", "Penutian": "penutian",
             "Uto-Aztecan": "uto", "Algonquian": "algic", "Yukian": "yukian"}

# carry over the plain blurbs from v1 where names match
BLURBS = {
 "Yurok": "Lower Klamath River and the adjacent coast.",
 "Wiyot": "Humboldt Bay and the lower Eel River.",
 "Tolowa": "The Smith River country in the far northwest corner.",
 "Hupa": "The Trinity River valley, inland from the Yurok.",
 "Karuk": "The middle Klamath River.",
 "Shasta": "The Shasta Valley and upper Klamath country.",
 "Yana": "The eastern Sacramento Valley foothills.",
 "Pomo": "The Russian River country and Clear Lake; several distinct languages share the name. The Kashaya, on whose coast Fort Ross was built, are the southwestern Pomo people.",
 "Esselen": "The Santa Lucia mountains south of Monterey.",
 "Salinan": "The upper Salinas River country; drawn into Missions San Antonio and San Miguel.",
 "Chumash": "The Santa Barbara Channel, its islands, and the coast from Malibu toward San Luis Obispo. Maritime towns, plank canoes, and the largest mission-era revolt (1824).",
 "Kumeyaay (Diegueño)": "The San Diego country and northern Baja California. From the 1775 destruction of Mission San Diego to the Jacum battle of 1837, the most persistent military resistance on the southern frontier.",
 "Quechan": "The Colorado River crossing at the Gila junction. Their 1781 victory destroyed two Spanish settlements and closed the overland road to California for the rest of the colonial period.",
 "Mojave": "The Colorado River above the Quechan; their reach extended west to the coast missions in the 1810s.",
 "Wintu": "The upper Sacramento Valley and Trinity foothills.",
 "Nomlaki": "The west side of the middle Sacramento Valley.",
 "Patwin": "The lower west side of the Sacramento Valley; the Suisun people of the 1810–17 campaigns spoke a Patwin language.",
 "Konkow": "The Feather River foothills.",
 "Nisenan": "The American, Bear, and Yuba river country.",
 "Coast Miwok": "The Marin and Bodega coast; the people who met Drake, guided and misdirected Spanish expeditions, and negotiated with the Russians at Bodega on their own account.",
 "Lake Miwok": "The Clear Lake basin's southern edge.",
 "Ohlone (Costanoan)": "The San Francisco peninsula, the East Bay, and the Monterey Bay country; the peoples of Missions Dolores, Santa Clara, San José, and Carmel.",
 "Wappo": "The Napa Valley and Mount St. Helena country.",
 "Yuki": "Round Valley and the upper Eel River; a language family unique to California.",
 "Cahto": "The Athabaskan-speaking Cahto of the upper Eel River country.",
 "Monache": "The upper San Joaquin and Kings River high country (Western Mono).",
 "Tübatulabal": "The Kern River forks.",
 "Kitanemuk": "The Tehachapi country.",
 "Tataviam": "The upper Santa Clara River, north of the San Fernando Valley.",
 "Tongva (Gabrielino)": "The Los Angeles basin and the southern Channel Islands; the people of Mission San Gabriel and of Toypurina's 1785 revolt.",
 "Serrano": "The San Bernardino mountains and the desert beyond Cajon Pass.",
 "Cahuilla": "The desert and mountain country from San Gorgonio Pass to the Salton sink; in the frontier records as both auxiliaries and raiders' targets.",
 "Luiseño": "The San Luis Rey and San Jacinto country; the people of Mission San Luis Rey.",
 "Acjachemen (Juaneño)": "The San Juan Capistrano coast.",
 "Cupeño": "The hot springs country at Warner's ranch.",
 "Chemehuevi": "The desert west of the Colorado River.",
}

CITE = ("Territory boundaries: Handbook of North American Indians, vol. 8, California "
        "(Smithsonian, 1978), as digitized by the Salton Sea Database Program, University of "
        "Redlands. Boundaries are the Handbook's scholarly reconstruction, not exact lines.")

def slug(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

sf = shapefile.Reader(SHP)
fields = [f[0] for f in sf.fields[1:]]
features = []
seen = {}
total_pts = 0
for srec in sf.iterShapeRecords():
    r = dict(zip(fields, srec.record))
    raw = r["TRIBE_NAME"].strip()
    name = RENAME.get(raw, raw)
    shp = srec.shape
    parts = list(shp.parts) + [len(shp.points)]
    rings = []
    for i in range(len(shp.parts)):
        ring = [(p[0], p[1]) for p in shp.points[parts[i]:parts[i + 1]]]
        simp = dp(ring, 0.004)  # ~400 m tolerance
        if len(simp) >= 4:
            rings.append([[round(y, 4), round(x, 4)] for x, y in simp])  # -> [lat,lng]
            total_pts += len(simp)
    if not rings:
        continue
    n = seen.get(name, 0) + 1
    seen[name] = n
    fid = "t-" + slug(name) + ("" if n == 1 else f"-{n}")
    # label point: centroid of the largest ring
    big = max(rings, key=len)
    clat = sum(p[0] for p in big) / len(big)
    clng = sum(p[1] for p in big) / len(big)
    alt = (r.get("ALT_NAME") or "").strip()
    summary = BLURBS.get(name, "")
    if alt and alt.lower() not in name.lower():
        summary = (summary + " Also recorded as " + alt + ".").strip()
    features.append({
        "id": fid, "register_no": None,
        "name": name + ("" if n == 1 else " (detached area)"),
        "date": {"iso": None, "display": "", "confidence": "exact"},
        "coords": [round(clat, 4), round(clng, 4)], "coord_precision": "area",
        "polygon": rings,
        "type": "event", "layer": FAM_LAYER[r["LINGUISTIC"]],
        "summary": summary,
        "result": "", "quote": None,
        "sources": [{"citation": CITE, "ca_record": None, "ia_leaf_url": None}],
        "native_groups": [], "tags": [],
        "notes": "Boundary follows the Handbook's map; territories interlocked and shifted, and no line here is exact. These are living nations."
    })

out = {
    "id": "native-california",
    "title": "Native California",
    "subtitle": "Territories of the nations of California at contact, after the Handbook of North American Indians",
    "abstract": ("The nations whose country the other maps on this site cross, with territory "
                 "boundaries following the standard scholarly map: the Handbook of North American "
                 "Indians, vol. 8 (1978), digitized by the University of Redlands. A note on the "
                 "lines: they are the best available reconstruction, not exact borders. Territories "
                 "interlocked, shifted over time, and are drawn differently by different scholars "
                 "and by the nations themselves. Language-family colors follow the Handbook's "
                 "groupings; the larger groupings (Hokan, Penutian) are conventional and linguists "
                 "treat them as unproven. These are living nations; names use current preferred "
                 "forms where they differ from the Handbook's. See also the Native Peoples Index "
                 "for named individuals and communities in this site's sources."),
    "date_range": [1769, 1848],
    "center": [37.3, -119.8],
    "zoom": 6,
    "cite_key": "native",
    "last_updated": "2026-07-15",
    "layers": [
        {"id": "penutian", "label": "Penutian-family peoples (conventional)", "color": "#2e5a4b"},
        {"id": "hokan", "label": "Hokan-family peoples (conventional)", "color": "#7a2e2e"},
        {"id": "uto", "label": "Uto-Aztecan-family peoples", "color": "#b7791f"},
        {"id": "atha", "label": "Athabaskan-family peoples", "color": "#275d7a"},
        {"id": "algic", "label": "Algic-family peoples", "color": "#8e44ad"},
        {"id": "yukian", "label": "Yukian-family peoples", "color": "#5a5248"},
    ],
    "legend_note": "Boundaries after the Handbook of North American Indians vol. 8 — approximate by nature.",
    "features": features
}
path = os.path.join(REPO, "data", "native-california.json")
json.dump(out, open(path, "w"), ensure_ascii=False)
print("features:", len(features), "| simplified vertices:", total_pts,
      "| size:", os.path.getsize(path) // 1024, "KB")
