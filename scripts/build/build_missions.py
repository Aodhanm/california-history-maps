#!/usr/bin/env python3
"""Build data/missions-establishments.json — the 21 Franciscan missions, their
asistencias/estancias, the Russian establishments (Ross, Port Rumiantsev, the
company ranches), and New Helvetia (Sutter's Fort). Founding years standard
(Bancroft/Engelhardt); mission sites exact, ranch sites approximate."""
import json, os, re, unicodedata

REPO = os.path.expanduser("~/california-history-maps")

def slug(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

STD = "Founding dates per the standard accounts (Bancroft, Hist. Cal.; Engelhardt)."

MISSIONS = [
 ("San Diego de Alcalá", 1769, [32.7419, -117.1067], "First of the chain; destroyed in the 1775 revolt and rebuilt at this valley site."),
 ("San Carlos Borromeo (Carmel)", 1770, [36.5433, -121.9190], "Serra's headquarters and burial place; moved from Monterey to Carmel in 1771."),
 ("San Antonio de Padua", 1771, [36.0144, -121.2497], "The upper Salinas valley mission, in Salinan country."),
 ("San Gabriel Arcángel", 1771, [34.0967, -118.1067], "The richest of the southern missions; Toypurina's 1785 revolt; the gateway of the overland routes."),
 ("San Luis Obispo de Tolosa", 1772, [35.2810, -120.6640], "Founded on the strength of the Portolá expedition's bear hunts in the Cañada de los Osos."),
 ("San Francisco de Asís (Dolores)", 1776, [37.7644, -122.4269], "The Bay's first mission; its neophyte flights across the water drove the 1795–97 East Bay expeditions."),
 ("San Juan Capistrano", 1776, [33.5017, -117.6628], "Founded twice, 1775 and 1776, after the San Diego revolt interrupted the first attempt."),
 ("Santa Clara de Asís", 1777, [37.3496, -121.9390], "Paired with the pueblo of San José, whose fields bordered too closely for the friars' comfort."),
 ("San Buenaventura", 1782, [34.2805, -119.2945], "The Channel mission Serra founded last in person; armed with cannon in the 1798 census."),
 ("Santa Bárbara", 1786, [34.4378, -119.7137], "The 'Queen of the Missions,' beside the presidio; a center of the 1824 Chumash revolt."),
 ("La Purísima Concepción", 1787, [34.6724, -120.4239], "Seized by Chumash rebels for a month in 1824; rebuilt after the 1812 earthquake at the present site."),
 ("Santa Cruz", 1791, [36.9797, -122.0308], "Across the river from the villa of Branciforte, whose settlers the friars blamed for most of their troubles."),
 ("Nuestra Señora de la Soledad", 1791, [36.3969, -121.3344], "The lonely Salinas valley mission; two governors died within its walls."),
 ("San José", 1797, [37.5333, -121.9190], "Base of the East Bay and Delta frontier; Estanislao was its alcalde before his 1829 revolt."),
 ("San Juan Bautista", 1797, [36.8455, -121.5370], "Sited at 'San Benito' per Lasuén's 1796 reconnaissance synthesis (C-A 50); the 1798 Talholostl battle was fought nearby."),
 ("San Miguel Arcángel", 1797, [35.7472, -120.6960], "Sited at 'las Pozas' in the same 1795–96 siting campaign."),
 ("San Fernando Rey", 1797, [34.2733, -118.4620], "The valley mission on the LA road; armed with 2-pounders in the 1805 census."),
 ("San Luis Rey de Francia", 1798, [33.2318, -117.3178], "Founded 13 Jun 1798, 54 children baptized that day (C-A 24 Doc 277); the largest mission population; Duflot drew its plan in the gallery."),
 ("Santa Inés", 1804, [34.5964, -120.1370], "The last Channel mission; the 1824 revolt began here."),
 ("San Rafael Arcángel", 1817, [37.9735, -122.5311], "Begun as a hospital asistencia of Dolores, raised to full mission in 1822; the northern frontier's answer to sickness and to Ross."),
 ("San Francisco Solano (Sonoma)", 1823, [38.2939, -122.4581], "The last and northernmost mission, founded under Mexican rule partly to face the Russians; seed of Vallejo's Sonoma."),
]

ASISTENCIAS = [
 ("Santa Margarita de Cortona (asistencia)", 1787, [35.3900, -120.6070], "San Luis Obispo",
  "Grain-station and chapel over the cuesta from San Luis Obispo; the rancho kept the name."),
 ("San Antonio de Pala (asistencia)", 1816, [33.3653, -117.0781], "San Luis Rey",
  "The inland asistencia of San Luis Rey; uniquely, still a functioning mission chapel serving a Native community today."),
 ("Las Flores (asistencia)", 1823, [33.2900, -117.4560], "San Luis Rey",
  "The coast station between San Luis Rey and San Juan Capistrano; later the Pico brothers' rancho."),
 ("Santa Ysabel (asistencia)", 1818, [33.1300, -116.6740], "San Diego",
  "San Diego's mountain asistencia in Kumeyaay country; the same district as the register's Santa Isabel fight of 1826."),
 ("San Bernardino de Sena (estancia)", 1830, [34.0455, -117.2260], "San Gabriel",
  "San Gabriel's estancia at the foot of the pass; the rancho outpost end of the mission system, in the raiding corridor."),
]

RUSSIAN = [
 ("Colony Ross", 1812, [38.5144, -123.2444], "exact",
  "The Russian-American Company's fort and village on Kashaya land, 1812 to 1841. The Presidial System map carries its strength series; Vallejo's 1833 reconnaissance (C-A 53 Doc 45) describes it in full."),
 ("Port Rumiantsev (Bodega)", 1809, [38.3100, -123.0450], "exact",
  "The company's anchorage and warehouses at Bodega Bay, in use from about 1809. The port the Spanish discovered in 1775, working under a Russian name."),
 ("Kostromitinov Ranch", 1833, [38.4500, -123.1000], "area",
  "Company farm on the Russian River plain, one of the three ranches feeding Ross in its last decade. Location approximate."),
 ("Khlebnikov Ranch", 1833, [38.3450, -123.0200], "area",
  "Company farm inland from Bodega, named for the RAC agent. Location approximate."),
 ("Chernykh Ranch", 1836, [38.3800, -122.9500], "area",
  "The agronomist Chernykh's farm; Voznesensky sketched it in 1841 (the sketch is in this site's gallery). Location approximate."),
]

features = []
for name, yr, coords, blurb in MISSIONS:
    features.append({
        "id": "m-" + slug(name), "register_no": None, "name": "Mission " + name if not name.startswith("San Francisco Solano") else "Mission San Francisco Solano (Sonoma)",
        "date": {"iso": str(yr), "display": "founded " + str(yr), "confidence": "year"},
        "coords": coords, "coord_precision": "exact", "type": "mission", "layer": "missions",
        "summary": blurb, "result": "", "quote": None,
        "sources": [{"citation": STD, "ca_record": None, "ia_leaf_url": None}],
        "native_groups": [], "tags": [], "notes": ""})
for name, yr, coords, parent, blurb in ASISTENCIAS:
    features.append({
        "id": "a-" + slug(name), "register_no": None, "name": name,
        "date": {"iso": str(yr), "display": "est. " + str(yr), "confidence": "year"},
        "coords": coords, "coord_precision": "place", "type": "mission", "layer": "asistencias",
        "summary": blurb + " Sub-station of Mission " + parent + ".",
        "result": "", "quote": None,
        "sources": [{"citation": STD, "ca_record": None, "ia_leaf_url": None}],
        "native_groups": [], "tags": [], "notes": ""})
for name, yr, coords, prec, blurb in RUSSIAN:
    features.append({
        "id": "r-" + slug(name), "register_no": None, "name": name,
        "date": {"iso": str(yr), "display": "est. " + str(yr), "confidence": "year"},
        "coords": coords, "coord_precision": prec, "type": "settlement", "layer": "russian",
        "summary": blurb, "result": "", "quote": None,
        "sources": [{"citation": "Russian establishments per the RAC literature (Gibson; Istomin) and the Spanish-Mexican reconnaissance record (C-A 12, C-A 53).", "ca_record": None, "ia_leaf_url": None}],
        "native_groups": [], "tags": [], "notes": ""})
OUTSTATIONS = [
 ("Suisun outstation (Solano)", [38.2320, -122.1240], "San Francisco Solano",
  "The Sonoma mission's grazing outstation in the Suisun Valley, at the Rockville and Cordelia end rather than the later town of Fairfield; in the country of the Suisun Patwin, and absorbed into the Vallejo-era ranchos after secularization."),
 ("Napa outstation (Solano)", [38.2971, -122.2855], "San Francisco Solano",
  "The mission's station in the lower Napa Valley, likewise folded into private ranchos in the 1830s."),
 ("San Pedro y San Pablo (San Mateo)", [37.5630, -122.3244], "San Francisco de Asís",
  "Mission Dolores' farm outstation on the peninsula, established in the 1780s; the 1830 SF padron still lists San Mateo among the jurisdiction's ranchos (C-A 50 Doc 425)."),
 ("Rancho San Francisco Xavier", [34.4400, -118.6200], "San Fernando",
  "San Fernando's northern stock rancho in the Santa Clarita valley; the same Rancho San Francisco where 18 Indians were killed in 1846 (military register #117)."),
 ("Santa Ysabel rancho (San Miguel)", [35.6200, -120.6000], "San Miguel",
  "One of San Miguel's named ranchos with an adobe, up the Salinas from the mission."),
 ("San Simeon rancho (San Miguel)", [35.6430, -121.1890], "San Miguel",
  "San Miguel's coast station at San Simeon bay."),
 ("Temecula station (San Luis Rey)", [33.4930, -117.1490], "San Luis Rey",
  "San Luis Rey's inland station among the Luiseno communities of the Temecula valley."),
 ("San Jacinto rancho (San Luis Rey)", [33.7840, -116.9600], "San Luis Rey",
  "The mission's easternmost stock rancho, toward the pass country."),
 ("San Gorgonio estancia (San Gabriel)", [33.9280, -116.8760], "San Gabriel",
  "San Gabriel's furthest estancia, in the pass between the mountains; the raiding corridor's doorstep."),
]
for name, coords, parent, blurb in OUTSTATIONS:
    features.append({
        "id": "o-" + slug(name), "register_no": None, "name": name,
        "date": {"iso": None, "display": "Mexican-era estate", "confidence": "circa"},
        "coords": coords, "coord_precision": "area", "type": "settlement", "layer": "outstations",
        "summary": blurb + " Outstation of Mission " + parent + ".",
        "result": "", "quote": None,
        "sources": [{"citation": "Mission-estate outstations per the standard accounts (Engelhardt; county histories); locations approximate. Selected, not exhaustive: the missions ran many more ranchos.", "ca_record": None, "ia_leaf_url": None}],
        "native_groups": [], "tags": [],
        "notes": "Verify against the 1834-36 secularization inventories (C-A 50-53) for the documented estate lists."})

features.append({
    "id": "s-sutters-fort-new-helvetia", "register_no": None, "name": "Sutter's Fort (New Helvetia)",
    "date": {"iso": "1839", "display": "est. 1839", "confidence": "year"},
    "coords": [38.5722, -121.4700], "coord_precision": "exact", "type": "settlement", "layer": "sutter",
    "summary": ("Sutter's Mexican land-grant colony at the Sacramento-American confluence, founded 1839. "
                "Buyer of Ross's movable property in 1841, magnet for the overland emigrants, and the "
                "hinge between the mission-rancho world and the American conquest. The anti-Micheltorena "
                "revolt charged the governor with his 'relaciones secretas' with Sutter (C-A 61)."),
    "result": "", "quote": None,
    "sources": [{"citation": "Standard accounts (Bancroft, Hist. Cal., IV); cf. Leg. Rec. (C-A 61) Doc 19", "ca_record": None, "ia_leaf_url": None}],
    "native_groups": [], "tags": [], "notes": ""})

out = {
    "id": "missions-establishments",
    "title": "Missions & Establishments",
    "subtitle": "The 21 missions, their sub-stations, the Russian colony, and New Helvetia, 1769–1846",
    "abstract": ("Every fixed establishment of colonial California on one map: the 21 Franciscan "
                 "missions with founding years, the asistencias and estancias that extended them "
                 "inland, a selected layer of the missions' named ranchos and outstations (Suisun "
                 "and Napa for Sonoma, San Mateo for Dolores, Temecula and San Jacinto for San Luis "
                 "Rey, and more), the Russian-American Company's fort, port, and farm ranches on "
                 "the Sonoma coast, and Sutter's New Helvetia on the Sacramento. The outstation "
                 "list is selected, not exhaustive: the missions ran many more ranchos. Use the "
                 "timeline to watch the chain grow north and the rivals appear. Outstation and "
                 "ranch locations are approximate; mission sites are exact."),
    "date_range": [1769, 1846],
    "center": [36.2, -119.8],
    "zoom": 6,
    "cite_key": "establishments",
    "last_updated": "2026-07-15",
    "layers": [
        {"id": "missions", "label": "Franciscan Missions (21)", "color": "#7a2e2e"},
        {"id": "asistencias", "label": "Asistencias & Estancias", "color": "#b7791f"},
        {"id": "outstations", "label": "Mission Ranchos & Outstations (selected)", "color": "#2e5a4b"},
        {"id": "russian", "label": "Russian Establishments", "color": "#8e44ad"},
        {"id": "sutter", "label": "New Helvetia (Sutter)", "color": "#275d7a"},
    ],
    "features": features
}
path = os.path.join(REPO, "data", "missions-establishments.json")
json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
print("features:", len(features), "->", path)
