#!/usr/bin/env python3
"""Build data/population-californias.json — every population count extracted from the
C-A survey catalogs (verified against the survey files 2026-07-15; citations = C-A vol + Doc).
Units and categories are the documents' own (almas, gente de razon, neofitos, castas)."""
import json, os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def F(fid, name, coords, prec, typ, layer, summary, series, result="", notes="", founded=""):
    return {
        "id": fid, "register_no": None, "name": name,
        "date": {"iso": None, "display": founded, "confidence": "exact"},
        "coords": coords, "coord_precision": prec, "type": typ, "layer": layer,
        "summary": summary, "series": series, "series_label": "Counted",
        "result": result, "quote": None,
        "sources": [{"citation": "All rows from the Archives of California survey catalogs; C-A 50 unless noted. Figures are the documents' own.", "ca_record": None, "ia_leaf_url": None}],
        "native_groups": [], "tags": [], "notes": notes
    }

features = [
    F("prov-alta", "Alta California (province-wide counts)", [36.6002, -121.8947], "exact", "event", "province",
      "The whole colony, counted. In 1790 the entire Spanish population of Alta California was 910 people, inside a mission population of 7,353. Duran's 1833 ledger then states the mission system's demographic arithmetic in three numbers: 82,882 baptized since founding, 58,417 dead, 10,482 living.",
      [["1790 Jul 1", "8,323 souls total: 910 gente de razon + 7,353 Indios (per-establishment table)", "C-A 50 Doc 32"],
       ["1817", "mission ledger: 64,675 baptized / 41,767 died / 20,238 living since founding", "C-A 50 Doc 387"],
       ["1822 Apr", "24,990 habitantes: 21,196 neophytes in the 20 missions, 2,994 gente de razon — read into the Diputacion's founding session", "Leg. Rec. (C-A 59) Doc 4"],
       ["1827", "'under 25,000, mostly Indians'; ~4,000 gente de razon, ~1,800 able to bear arms", "Dep. Rec. (C-A 48) Doc 29 — abstract"],
       ["1829", "school census: 11 schools, ~389 students in the whole territory", "St. Pap. Missions (C-A 51) Doc 3"],
       ["1833 Dec", "Duran's cumulative Cuadro Estadistico: 82,882 baptized / 58,417 died / 10,482 living", "C-A 50 Doc 427"]],
      result="One province, three generations, counted into decline",
      notes="Placed at Monterey as the capital; the counts are province-wide.",
      founded="1769–1846"),
    F("prov-baja", "Antigua (Baja) California (province-wide)", [26.0115, -111.3486], "exact", "event", "province",
      "The old province counted alongside the new: Arrillaga's 1791 census tables cover 18 poblaciones, presidio and missions, with the men, women, and children of each.",
      [["1782", "per-mission families/souls table, ~17 missions (Loreto mission 76 souls…)", "C-A 50 Doc 6"],
       ["1791 Dec", "province-wide censo y castas table, 18 poblaciones", "C-A 50 Doc 38"],
       ["1792", "the Dominican Prior's estado: 4,442 souls in the Baja missions", "Misc. (C-A 62) Doc 24"],
       ["1795", "4,337 almas per the P. Presidente's mission states", "Prov. St. Pap. (C-A 10) Doc 19"]],
      notes="Placed at Loreto; see the individual Baja pins for 1790 figures.",
      founded="context"),
    # ── PUEBLOS ──
    F("pu-san-jose", "Pueblo San José de Guadalupe", [37.3382, -121.8863], "exact", "settlement", "pueblos",
      "The first pueblo, counted at 78 souls in 1790 — one europeo, 33 espanoles, 8 indios, 8 mulatos, 28 otras castas. Four decades later it had grown to 602.",
      [["1777 Nov", "founded with 14 vecinos, 66 souls (Neve's own report)", "Prov. Rec. (C-A 22), tomo pp. 8-9, 17-21"],
       ["1790", "78 souls (1 europeo, 33 espanoles, 8 indios, 8 mulatos, 28 otras castas)", "C-A 50 Doc 20; nominal roll Doc 19"],
       ["1793", "nominal padron of the pueblo (named households)", "Prov. Rec. (C-A 24), Sav 319-322"],
       ["1800 Dec", "Padron General by Macario de Castro: 30 households, nominal, with demographic columns", "Prov. St. Pap. (C-A 11), n181-183"],
       ["1823 Jun", "345 souls (9 born, 3 died); Branciforte 67 and Los Ranchos 50 counted alongside", "Dep. St. Pap. (C-A 27) Doc 26"],
       ["1823 Dec", "391 total: 59 men, 114 parvulos, 184 women and girls; + Rancho San Ysidro 66", "Dep. St. Pap. (C-A 27) Docs 22-23"],
       ["1834 Dec 31", "602 souls: 431 gente de razon + 171 indigenas avecindados (two independent returns)", "DSP Ben. (C-A 42) Doc 184; St. Pap. M&C (C-A 53) Doc 49"]],
      founded="founded 1777"),
    F("pu-los-angeles", "Pueblo de Los Ángeles", [34.0537, -118.2428], "exact", "settlement", "pueblos",
      "The pueblo's whole arc in five counts: 139 souls in the 1790 province table, 148 in 1792, 274 in 1817, then the Mexican-era growth to over a thousand — with the padrones counting Indians separately, in the pueblo and on its ranchos.",
      [["1781 Nov", "the founding padron de pobladores, each vecino by name with casta ('fundado el 4 de Set.e de 1781')", "St. Pap. M&C (C-A 52) Doc 26"],
       ["1784", "'el pueblo de los Angeles se compone de 8 habitantes' (vecino-pobladores, 3 years in)", "Prov. Rec. (C-A 23) Doc 58"],
       ["1785", "pobladores census: 12 households with casta, age, occupation", "Prov. St. Pap. (C-A 14), n325-326"],
       ["1789", "pobladores + agregados roll (named)", "C-A 50 Doc 31"],
       ["1790 Aug", "nominal household roll: 31 families, 141 souls, with oficio/casta/age/birthplace", "Prov. St. Pap. (C-A 5) Doc 96"],
       ["1790", "139 souls (province table); estado of population + property, named pobladores", "C-A 50 Docs 32, 30"],
       ["1792", "148 souls (2 europeos, 57 espanoles, 17 mestizos, 15 indios, 57 mulatos)", "C-A 50 Doc 71"],
       ["1817", "274 souls in the pueblo, 537 in the jurisdiction ('no especifica los indios')", "C-A 50 Doc 382"],
       ["1828", "pueblo 1,219 + 388 Indians; jurisdiction 1,361 + 354 Indians", "C-A 50 Doc 417"],
       ["1830", "pueblo 835 + 71 Indians; jurisdiction 1,158 + 157 Indians (ranchos named)", "C-A 50 Doc 430"]],
      notes="The 1790 counts disagree: the province table says 139, the pueblo's own August roll 141 — both shown. The 1828 vs 1830 drop reflects changing padron scope as much as population.",
      founded="founded 1781"),
    F("pu-branciforte", "Villa de Branciforte", [36.9797, -122.0260], "exact", "settlement", "pueblos",
      "The third and smallest pueblo, founded 1797 across the river from Mission Santa Cruz. The 1823 padrones catch it at 128 souls, or 67 by the summer count — the two returns are shown as recorded.",
      [["1823 Jun", "67 (counted beside San Jose's 345)", "Dep. St. Pap. (C-A 27) Doc 26"],
       ["1823 Dec", "128 souls: 66 men, 62 women", "Dep. St. Pap. (C-A 27) Doc 24"]],
      notes="The June and December 1823 figures differ in scope; both preserved.", founded="founded 1797"),
    F("tw-monterey", "Monterey (town & jurisdiction)", [36.6002, -121.8947], "exact", "settlement", "pueblos",
      "The capital counted as a town: the 1826 vecindario census breaks out gente de razon by sex and age beside the Indians living among them; by 1829 the town and its named ranchos held 867.",
      [["1826 May", "vecindario: gente de razon 75 men, 98 women, 82 boys, 56 girls (= 311) + Indians counted alongside", "St. Pap. M&C (C-A 53) Doc 24"],
       ["1827 May", "rancho census of the jurisdiction: 24 vecino-ranchos with titles", "St. Pap. M&C (C-A 53) Doc 20"],
       ["1829", "Monterey 502 souls + named ranchos 365 = 867", "St. Pap. Missions (C-A 51) Doc 5"]],
      founded="capital"),
    F("sac-1847", "Sacramento District (New Helvetia)", [38.5722, -121.4700], "exact", "settlement", "pueblos",
      "The arc's endpoint: the December 1847 statistics of population of the Sacramento district, compiled at Sutter's fort in the first American winter — the count that closes the era this map covers.",
      [["1847 Dec", "the Sacramento-district census table ('Statistics of Population &c')", "Unbound Docs (C-A 63) Doc 426"]],
      founded="est. 1839"),
    # ── PRESIDIOS ──
    F("pr-san-francisco", "Presidio of San Francisco", [37.7899, -122.4585], "exact", "presidio", "presidios",
      "The 1790 padron names every household of the company with casta, birthplace, age, wife, and children — 144 souls at the Golden Gate. By 1830 the whole SF jurisdiction, missions included, counted 5,469, of whom 5,240 were Indians.",
      [["1790 Oct", "144 souls (1 europeo, 78 espanoles, 16 indios, 5 mulatos, 44 castas); nominal padron", "C-A 50 Docs 53, 52"],
       ["1830 Dec", "jurisdiction-wide: 5,469 souls / 5,240 Indians (ranchos + 6 missions named)", "C-A 50 Doc 425"]],
      founded="founded 1776"),
    F("pr-santa-barbara", "Presidio of Santa Bárbara", [34.4221, -119.6989], "exact", "presidio", "presidios",
      "The 1785 padron is a nominal roll of 67 heads of household — officers, sergeants, corporals, soldiers, vecinos, and the San Blas paquebot's servants — with casta, age, and family.",
      [["1785 Dec", "67 heads of household, nominal roll with casta and family", "C-A 50 Doc 2"],
       ["1801", "garrison census: 189 total population", "Prov. St. Pap. (C-A 11), n48-49"]],
      founded="founded 1782"),
    F("pr-san-diego", "Presidio & town of San Diego", [32.7573, -117.1966], "exact", "presidio", "presidios",
      "San Diego's late-Mexican padrones count the men who could bear arms: 53 in 1845, 73 in 1846 — the municipality on the eve of the conquest.",
      [["1845 Sep", "padron: 53 individuals aged 15-60 (militia-age)", "DSP Ben. (C-A 42) Doc 356"],
       ["1846 Jul", "padron: 73 citizens aged 15-60", "DSP Ben. (C-A 42) Doc 590"]],
      founded="founded 1769"),
    F("pr-loreto", "Presidio of Loreto (Baja)", [26.0115, -111.3486], "exact", "presidio", "presidios",
      "The old capital counted in 1790: 399 souls, a fifth of them under the fuero militar.",
      [["1790 Dec", "399 souls (3 europeos, 73 espanoles, 152 indios, 10 mulatos, 158 otras castas)", "C-A 50 Doc 39"]],
      founded="founded 1697"),
    F("ba-real-santa-ana", "Real de Santa Ana (Baja mining district)", [23.6900, -110.0800], "place", "settlement", "presidios",
      "The southern mining district, the most casta-diverse place in either California: 696 souls with 5 miners, 16 rancheros, and 93 others by trade.",
      [["1790", "696 souls (3 europeos, 133 espanoles, 178 indios, 157 mulatos, 204 castas)", "C-A 50 Doc 29"]],
      founded="context"),
]

# ── ALTA MISSIONS: the almas series (registro years) + 1790 censos ──
M = [
 ("San Carlos (Carmel)", [36.5433, -121.9190],
  [["1785","711 almas (171 familias)","C-A 50 Doc 10"],["1787","707","Doc 14"],["1788","720","Doc 16"],["1789","752","Doc 18"]], "founded 1770"),
 ("San Diego", [32.7419, -117.1067],
  [["1784","786","C-A 50 Doc 8"],["1789","940","Doc 18"],["1790 Oct","856 souls (853 indios; censo y castas)","Doc 47"]], "founded 1769"),
 ("San Juan Capistrano", [33.5017, -117.6628],
  [["1784","431","C-A 50 Doc 8"],["1789","771","Doc 18"]], "founded 1776"),
 ("San Gabriel", [34.0967, -118.1067],
  [["1784","739","C-A 50 Doc 8"],["1788","~1,000","Doc 16"],["1789","1,044","Doc 18"],
   ["1839","ex-mission padron: 587 souls","St. Pap. Missions (C-A 51) Doc 1"]], "founded 1771"),
 ("San Antonio de Padua", [36.0144, -121.2497],
  [["1784","774","C-A 50 Doc 8"],["1785","850","Doc 10"],["1787","979","Doc 14"],["1788","1,028","Doc 16"],["1790 Oct","1,088 souls (1,078 indios)","Doc 55"]], "founded 1771"),
 ("San Luis Obispo", [35.2810, -120.6640],
  [["1785","492","C-A 50 Doc 10"],["1787","531","Doc 14"],["1788","578","Doc 16"]], "founded 1772"),
 ("San Francisco (Dolores)", [37.7644, -122.4269],
  [["1785","250","C-A 50 Doc 10"],["1787","476","Doc 14"]], "founded 1776"),
 ("Santa Clara", [37.3496, -121.9390],
  [["1785","472","C-A 50 Doc 10"],["1787","608","Doc 14"],["1790 Sep","927 souls (925 indios)","Doc 48"]], "founded 1777"),
 ("San Buenaventura", [34.2805, -119.2945],
  [["1789","380","C-A 50 Doc 18"]], "founded 1782"),
 ("Santa Bárbara (mission)", [34.4378, -119.7137],
  [["1787","183 (first inventory)","C-A 50 Doc 14"],["1788","361","Doc 16"],["1789","525","Doc 18"],
   ["1827","SB-jurisdiction missions together: 2,061 Indian men + 1,739 women","St. Pap. Sac. (C-A 56) Doc 446"]], "founded 1786"),
 ("Santa Cruz", [36.9797, -122.0308],
  [["1797 Dec","509 souls: 173 men, 189 women, 108 boys, 99 girls","Prov. Rec. (C-A 24), Sav 394"]], "founded 1791"),
 ("San Juan Bautista", [36.8455, -121.5370],
  [["1798","288 souls (63 marriages; 80 boys, 39 girls)","St. Pap. Sac. (C-A 54) Doc III-14"]], "founded 1797"),
 ("San Luis Rey", [33.2318, -117.3178],
  [["1839 Jul","40 Indians resident: 29 men, 11 women — the largest mission population in the province, five years after secularization","DSP Angeles (C-A 35) Doc 150"]], "founded 1798"),
 ("La Purísima", [34.6724, -120.4239],
  [["1788","95 (first inventory)","C-A 50 Doc 16"],["1789","151","Doc 18"],["1790","151 (province table)","Doc 32"]], "founded 1787"),
]
for name, coords, series, founded in M:
    fid = "mi-" + name.lower().split(" (")[0].replace(" ", "-")
    features.append(F(fid, "Mission " + name, coords, "exact", "mission", "missions",
        "Neophyte population as the annual registros and the 1790 censo campaign recorded it.",
        series, founded=founded,
        notes="The counts are of people living AT the mission when counted; flight, death, and new baptism churn beneath every figure. A 1795 nominal padron of the Monterey-district missions exists (C-A 50 Doc 54)."))

# ── BAJA MISSIONS (1790 censo series, Dominican frontier context) ──
B = [
 ("San Francisco de Borja", [28.7440, -113.7530], "614 souls (612 indios) — the largest Baja mission", "C-A 50 Doc 26"),
 ("San Fernando Velicatá", [29.9710, -115.2360], "479 souls (475 indios)", "C-A 50 Doc 28"),
 ("El Rosario", [30.0620, -115.7230], "348 souls (338 indios)", "C-A 50 Doc 45"),
 ("San Vicente", [31.3330, -116.2500], "257 souls (251 indios)", "C-A 50 Doc 43"),
 ("Santo Domingo", [30.7690, -115.9370], "205 souls (196 indios)", "C-A 50 Doc 44"),
 ("San Miguel de la Frontera", [32.0960, -116.8480], "127 souls", "C-A 50 Doc 46"),
]
for name, coords, fig, cite in B:
    fid = "bm-" + name.lower().replace(" ", "-")
    features.append(F(fid, "Mission " + name + " (Baja)", coords, "place", "mission", "baja",
        "The Dominican frontier counted in the same 1790 campaign.",
        [["1790", fig, cite]], founded="context"))

out = {
    "id": "population-californias",
    "title": "Population of the Californias",
    "subtitle": "Every count in the archive: padrones, censos, and mission registros, 1777–1847",
    "abstract": ("The population counts of Spanish and Mexican California, settlement by settlement, "
                 "as the archive recorded them. A note on what these numbers are: they are the counts "
                 "of a colonial bureaucracy. Padrones undercount, categories like gente de razon and "
                 "neofito are the empire's constructs, and Native people appear only when and how the "
                 "state counted them — inside missions, pueblos, and jurisdictions. The map shows what "
                 "the documents say, in their own units, not how many people lived in California; the "
                 "nations of the Native California map were mostly never counted at all. Every row "
                 "cites its document. The headline: in 1790 the entire Spanish population of Alta "
                 "California was 910 people."),
    "date_range": [1777, 1847],
    "center": [33.5, -117.5],
    "zoom": 6,
    "cite_key": "population",
    "last_updated": "2026-07-15",
    "layers": [
        {"id": "missions", "label": "Alta Missions (neophyte counts)", "color": "#7a2e2e"},
        {"id": "pueblos", "label": "Pueblos", "color": "#b7791f"},
        {"id": "presidios", "label": "Presidios & Real", "color": "#275d7a"},
        {"id": "province", "label": "Province-wide Counts", "color": "#2e5a4b"},
        {"id": "baja", "label": "Baja Missions, 1790 (context)", "color": "#8e44ad"},
    ],
    "legend_note": "Figures are the documents' own; categories are the colonial state's.",
    "features": features
}
path = os.path.join(REPO, "data", "population-californias.json")
json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
print("features:", len(features), "->", path)
