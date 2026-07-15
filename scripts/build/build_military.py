#!/usr/bin/env python3
# ARCHIVAL/one-time or session-built script, kept for provenance and reproducibility.
# Paths referencing the original session scratchpad will need adjusting to rerun.
"""Build data/military-engagements.json from the Phase-0 draft + Phase-1 register additions."""
import json, re, os, unicodedata

SCRATCH = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.expanduser("~/california-history-maps")
draft = json.load(open(f"{SCRATCH}/extracted/military-engagements.draft.json"))

MONTHS = {m: i for i, m in enumerate(
    "january february march april may june july august september october november december".split(), 1)}

def slugify(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:48].rstrip("-")

def parse_date(disp):
    """'November 5, 1775' / 'August 1769' / 'May–Jun 1829' / '1826' → (iso, confidence)"""
    d = disp.strip()
    m = re.match(r"^([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})$", d)
    if m and m.group(1).lower() in MONTHS:
        return ("%s-%02d-%02d" % (m.group(3), MONTHS[m.group(1).lower()], int(m.group(2))), "exact")
    m = re.match(r"^([A-Za-z]+)\s+(\d{4})$", d)
    if m and m.group(1).lower() in MONTHS:
        return ("%s-%02d" % (m.group(2), MONTHS[m.group(1).lower()]), "month")
    m = re.match(r"^(\d{4})$", d)
    if m:
        return (m.group(1), "year")
    m = re.search(r"(\d{4})", d)
    if m:
        conf = "range" if re.search(r"[–—-]|/", d) else "circa"
        return (m.group(1), conf)
    return (None, "circa")

def spanishish(s):
    return bool(re.search(r"[áéíóúñ¿¡]|\b(el|la|los|de|que|con|por)\b", s))

TYPE_MAP = {"typeGroups.battles": "battle", "typeGroups.raids": "raid",
            "typeGroups.standoffs": "standoff", "typeGroups.defenses": "defense"}

features = []
seen_ids = set()
for f in draft["features"]:
    m = re.match(r"#(\d+[a-z½¾]*)\s*[—–-]\s*(.*)", f["name"])
    reg_no = m.group(1) if m else None
    title = (m.group(2) if m else f["name"]).strip()
    fid = ("reg-" + reg_no + "-" if reg_no else "") + slugify(title)
    base = fid; n = 2
    while fid in seen_ids:
        fid = f"{base}-{n}"; n += 1
    seen_ids.add(fid)
    iso, conf = parse_date(f["date_display"])
    result = f["result"]
    # Phase-1 correction: #31 overclaimed vs register
    if reg_no == "31":
        result = "Standoff — Spanish retreated"
    quote = None
    if f["quote_raw"].strip():
        q = f["quote_raw"].strip()
        quote = {"es": q, "en": "", "source": ""} if spanishish(q) else {"es": "", "en": q, "source": ""}
    feat = {
        "id": fid,
        "register_no": reg_no,
        "name": title,
        "date": {"iso": iso, "display": f["date_display"], "confidence": conf},
        "coords": f["coords"],
        "coord_precision": "place",
        "type": TYPE_MAP.get(f["type_group"], "event"),
        "layer": f["layer_var"],
        "summary": f["summary"],
        "result": result,
        "quote": quote,
        "sources": [{"citation": f["source_raw"], "ca_record": None, "ia_leaf_url": None}] if f["source_raw"].strip() else [],
        "native_groups": [],
        "tags": [],
        "notes": ""
    }
    features.append(feat)

# ---- Phase-1 additions: register rows verified 2026-07-14 ----
def NF(reg, name, iso, disp, conf, coords, prec, typ, layer, summary, result, cites, native=None, notes="", tags=None):
    fid = "reg-" + slugify(reg) + "-" + slugify(name)
    return {
        "id": fid, "register_no": reg, "name": name,
        "date": {"iso": iso, "display": disp, "confidence": conf},
        "coords": coords, "coord_precision": prec, "type": typ, "layer": layer,
        "summary": summary, "result": result, "quote": None,
        "sources": [{"citation": c, "ca_record": None, "ia_leaf_url": None} for c in cites],
        "native_groups": native or [], "tags": tags or [], "notes": notes
    }

additions = [
    NF("5¾", "Spanish Yuma Punitive Campaign", "1782-09", "Sep–Oct 1782", "range",
       [32.73, -114.62], "place", "battle", "yuma",
       "Neve and Capt. José Antonio Romeu (108 men) march down the Colorado; Romeu with 40 men and 12 Indian allies (Jalchedunes/Cocomaricopas) routs the Yuma cavalry ('crecida mortandad'), 4 soldiers wounded; Fages escorts the rescued captives. An abortive plan to re-fortify the crossing follows. Neve's 'Antecedentes de una mortandad' names the revolt's causes: gifts withheld from Palma, women seized, mules destroying the mesquite.",
       "Spanish reprisal after the 1781 Yuma victory",
       ["Prov. Rec. (C-A 22), survey Entry 25"], native=["Quechan (Yuma)", "Jalchedun", "Cocomaricopa"]),
    NF("45", "Tule balsa shipwreck at the Farallones", "1794", "1794", "year",
       [37.699, -123.003], "place", "event", "phase2",
       "Mission San Francisco Indians navigated by sea in tule balsas to evangelize gentiles on the opposite shore; currents carried one balsa onto the Farallones, where 2 of the 4 Indians drowned. Not a military engagement — an indigenous open-water navigation datum at the Bay mouth.",
       "Maritime accident — 2 drowned",
       ["Prov. St. Pap. (C-A 7), n29, pp. 72–73"]),
    NF("103", "Horse-theft raid & punitive expedition (140-head caballada)", "1824-06", "Jun–Jul 1824", "range",
       [36.5, -121.2], "conjectural", "raid", "mexican",
       "'Indios malhechores' drove off a caballada of 140 head from the national rancho; Gov. Argüello sent Alf. Santiago Argüello with 34 troops to punish the raiders and the rancherías that harbor them ('por cortar de raiz los daños'). In a related San Diego–frontier action, 14 of 15 neophyte auxiliaries who fought were killed, and ~40 raiders later burned a San Diego rancho.",
       "Stock raid + collective punishment",
       ["Dep. Rec. (C-A 46), Doc 97; Doc 88"],
       notes="Rancherías not located in the abstract — pin placed in the Monterey-district interior, conjectural. Verbatim re-read flagged in the register."),
    NF("104", "Surrender of the Spanish squadron at Monterey", "1825-04-27", "Apr–May 1825", "range",
       [36.605, -121.89], "place", "event", "mexican",
       "The Spanish ship-of-the-line Asia and brig Constante — Spain's last Pacific force after the loss of Peru — put into Monterey and capitulated to the Mexican Nation, their crews swearing 'el solemne juramento de sujetarse á las leyes de los Estados Unidos Mejicanos.' Argüello tapped the Asia's powder to arm the near-empty San Francisco and Monterey batteries; pilot Juan Malarín carried the acta de Capitulación to Mexico City.",
       "Naval capitulation (no combat)",
       ["Dep. Rec. (C-A 46), Docs 49–52, 102; cf. Bancroft, Hist. Cal., III"]),
    NF("105", "The anti-Victoria revolt — the Cahuenga encounter", "1831-12", "Nov 1831–Feb 1832", "range",
       [34.128, -118.357], "place", "battle", "mexican",
       "California's first successful gubernatorial overthrow. The Plan of San Diego (29 Nov 1831) pronounced against Gov. Manuel Victoria 'por recobrar la representación popular'; Victoria was wounded at the Cahuenga encounter ('estado moribundo') and deported on the Pocahontas. The interregnum then splintered — the Diputación installed Pío Pico, Los Angeles proclaimed Echeandía, Zamorano rose in the north — 'casi inevitable el derramamiento de sangre.'",
       "Rebel victory — the governor deposed",
       ["Leg. Rec. (C-A 59), Docs 37, 40–53"],
       notes="Pin at Cahuenga Pass, the revolt's one armed encounter; the movement spanned San Diego to Monterey. Verbatim re-read flagged."),
    NF("106", "The anti-Micheltorena revolt — Cahuenga/Providencia", "1845-02", "1844–Feb 1845", "range",
       [34.156, -118.34], "place", "battle", "mexican",
       "The last Californio overthrow of a Mexican-appointed governor. The Asamblea Departamental 'desconoce la autoridad… de M. Micheltorena,' charging his 'relaciones secretas con el extranjero Sutter' (Sutter marched for Micheltorena; M.G. Vallejo corresponded against him). Micheltorena and his cholo battalion were defeated and expelled after the Battle of Cahuenga/Providencia, installing the native-born Pío Pico as California's last Mexican governor.",
       "Rebel victory — Micheltorena expelled",
       ["Leg. Rec. (C-A 61), Docs 19, 24"],
       notes="The Sutter alliance prefigures the American takeover 16 months later. Verbatim re-read flagged (incl. the deposition-session date)."),
    NF("107", "Ambush of the San Diego pursuit party (Dominican frontier)", "1824-06-21", "21 Jun 1824", "exact",
       [32.2, -116.6], "conjectural", "battle", "frontera",
       "A San Diego troop detachment pursuing Dominican-mission cimarrones (runaway neophytes) was ambushed on the Baja frontier; the action left 15 Indians dead, including a leader from Mission San Miguel — a frontier engagement in the same season as the Chumash Revolt further north.",
       "Indigenous tactical victory over a presidial party",
       ["Dep. St. Pap. (C-A 27), doc 43 (n36)"],
       notes="Ambush site not located in the abstract — pin placed on the Dominican-mission frontier, conjectural."),
    NF("108", "Gentile attack on mission neophytes — '21 neophytes killed'", "1826", "1826", "year",
       [33.0, -116.5], "conjectural", "raid", "frontera",
       "A report of 21 neophytes killed by gentiles on the interior frontier of the San Diego district — evidence for the raiding-economy pressure on mission populations in the 1820s, and for inter-indigenous violence between mission and independent communities.",
       "Gentile raid — 21 neophytes killed",
       ["Dep. St. Pap. (C-A 27), doc 134"],
       notes="Location not given in the abstract — conjectural pin in the SD interior."),
    NF("109", "Martínez's 'campaña en los Ríos'", "1827", "1827", "year",
       [37.95, -121.5], "area", "battle", "mexican",
       "Ignacio Martínez's 1827 campaign into the Delta rivers against the runaway and rebel Indians of Missions San José and Santa Clara — 2 soldiers killed. The precursor operation to the 1829 Estanislao campaigns, in the same theater.",
       "Early Delta campaign — 2 soldiers killed",
       ["St. Pap., Missions & Colonization (C-A 53), Doc 8, tomo pp. 21–23"]),
    NF("111", "Vallejo's & Sánchez's punitive horse-raid expeditions", "1829-04", "Apr 1829", "month",
       [36.7, -121.1], "conjectural", "raid", "mexican",
       "Stock-raid reprisal operations by Vallejo and Sánchez in the Monterey district interior, mounted while the Monterey troops were destitute (the pay-mutiny backdrop, six months before the Solís revolt).",
       "Spanish-Mexican reprisal expeditions",
       ["Dep. Rec. (C-A 48), Doc 31"],
       notes="Routes not located in the abstract — conjectural pin in the Monterey interior."),
    NF("112", "The great 1840 horse-raid campaign ('agua de Ramón')", "1840-05", "May–Jun 1840", "range",
       [34.31, -117.47], "area", "raid", "mexican",
       "A multi-week mounted campaign, not a single skirmish. Chaguanosos drove off three mare-herds from Mission San Gabriel (14 May); the LA vecino-militia mobilized (13→36 men, 4 muskets, 19 lances); Ignacio Palomares's ~23-man party was routed; relief columns held the Puerta del Cajón and recovered the herds at the 'agua de Ramón' surprise. Leandri's report: the rearguard was '20 hombres Ciudadanos de los Estados Unidos; pero tenían á más otra gente,' driving 1,000+ head, ~1,500 driven to death in flight.",
       "Raiders routed one militia party; herds recovered at agua de Ramón",
       ["Dep. St. Pap., Angeles (C-A 34), E29 (Docs 1285–1293, 1305–1308, 1321, 1336)"],
       native=["Chaguanoso (mixed raiding bands)"],
       notes="Pin at Cajon Pass, the campaign's hinge; 'agua de Ramón' itself is unlocated (secondary lit puts the fight at Resting Springs — the partes' 'Ramón' is a datum to weigh vs Bancroft IV:77, not to harmonize)."),
    NF("113", "Plaza firefight (Alvarado civil war)", "1838", "1838", "year",
       [34.42, -119.70], "conjectural", "battle", "mexican",
       "Californio-vs-Californio action of the 1838 civil war (the Alvarado–Carrillo contest for the governorship): per José Castro's abstracted report, a 160-man force garrisoning 'la plaza' abandoned it by night after a 2-day continuous firefight with only 1 dead, pursued by cavalry; two bronze cannon at the Castillo were transferred to José Estrada.",
       "Garrison abandoned 'la plaza' after a 2-day firefight",
       ["Dep. St. Pap., Monterey (C-A 43), Doc 4 (n420, tomo 41)"],
       notes="'La plaza' is not named on the leaf — probably Santa Bárbara or a southern plaza. Conjectural pin; transcribe the parte before locating or quoting."),
    NF("114", "Ibarra's punitive battle at Santa Isabel ('veinte pares de orejas')", "1826", "1826", "year",
       [33.11, -116.67], "place", "battle", "frontera",
       "A punitive action against ~100 or more hostile Indians, routed 4 leguas to San Felipe with Kumeyaay/Cahuilla auxiliaries; 28 killed, '20 pares de orejas' cut from the dead as proof, plus a prisoner summarily executed.",
       "Spanish-Mexican punitive victory — 28 killed",
       ["Dep. St. Pap. Ben., Pref. y Juzg. (C-A 42), Doc 914 (Expanded Entry 26)"],
       native=["Kumeyaay", "Cahuilla"],
       notes="Abstract — transcribe the parte before quoting the orejas line."),
    NF("115", "José Castro's 120-man northern expedition 'contra los bárbaros'", "1839-05", "May 1839", "month",
       [38.6, -121.4], "conjectural", "raid", "mexican",
       "A late-Mexican state campaign against interior raiders — 120 men under Castro 'contra los bárbaros que invaden los puntos del norte.'",
       "State campaign (outcome not recorded in the abstract)",
       ["Dep. St. Pap. Ben., Pref. y Juzg. (C-A 42), Doc 1228"],
       notes="'Los puntos del norte' unlocated — conjectural pin on the northern frontier."),
    NF("116", "The Gavilán (Hawk's Peak) standoff", "1846-03", "Mar 1846", "month",
       [36.760, -121.505], "exact", "standoff", "mexican",
       "Frémont fortifies Gavilán Peak and raises the US flag; Castro musters the militia at San Juan; Frémont withdraws north by night without an engagement — the armed face-off that preceded the conquest by three months, with the prefecture's intelligence file (the Guerrero/neophyte-Antonio reports on the '200 armed foreigners').",
       "Standoff — Frémont withdrew without an engagement",
       ["Dep. St. Pap. Ben., Pref. y Juzg. (C-A 42), Docs 361–363 (Expanded Entry 22)"]),
    NF("117", "The Rancho San Francisco killing of 18 'indios ladrones'", "1846-03", "1846", "year",
       [34.44, -118.62], "place", "event", "mexican",
       "Twenty-one armed Indians were disarmed 'mañosamente,' revolted with stones and knives, and were shot — 18 dead, 2 wounded, 1 escaped: the anti-raiding apparatus at its most lethal, weeks before the conquest.",
       "18 Indians killed",
       ["Dep. St. Pap. Ben., Pref. y Juzg. (C-A 42), Doc 1219 (n412)"],
       notes="District-court abstract — verify vs leaf before quoting."),
    NF("118", "San Pedro Mártir Indian revolt (Dominican frontier)", "1796-09", "Sep 1796–Aug 1797", "range",
       [30.85, -115.47], "place", "revolt", "frontera",
       "Mission Indians revolt ('el alboroto'); the officer blamed for causing it is imprisoned at San Vicente on Borica's approval; rebels are seized and prosecuted via sumaria (Bernal spends 24 days at the mission); the investigation runs into 1797 (declarations of the indio José Manuel, later freed); the mission's interpreter is killed by mid-1797.",
       "Revolt suppressed judicially; the blamed officer imprisoned",
       ["Prov. Rec. (C-A 24), Docs 308 (Sav 266), 309 (Sav 267), 321 (Sav 279), 328"],
       notes="A revolt + judicial-military response arc, not a field battle."),
    NF("119", "Río Colorado engagement ('atacar la fuerza con la fuerza')", "1796-11-17", "reported 17 Nov 1796", "circa",
       [32.5, -114.8], "conjectural", "battle", "frontera",
       "The commander, met with insults from 'una colonia numerosa' of Indians on all sides in bad terrain, 'se vió precisado á atacar la fuerza con la fuerza.' Losses: Spanish, a mule and 7–8 horses; Indian, 7 gandules killed. Reported to the Viceroy as proof the Sonora communication could not be secured without real garrisons; the Viceroy later reviewed a printed account of the engagement.",
       "Spanish column fought through — 7 Indians killed",
       ["Prov. Rec. (C-A 24), Doc 313 (n270, Sav 271, tomo p. 697)"],
       notes="Site unlocated — conjectural pin near the lower Colorado. Abstract — transcribe before quoting."),
    NF("120", "Punitive battle near San Juan Bautista — death of captain 'Talholostl'[?]", "1798-11-21", "21 Nov 1798", "exact",
       [36.90, -121.50], "area", "battle", "phase2",
       "Gentiles 'de la otra banda' killed 5 Indians and 2 women of the mission rancherías; Borica sent Sgt. Macario Castro with 10 cuera soldiers, 8 Christian Indians, and 24 aggrieved gentiles; the column caught the malefactors, killed the enemy captain 'Talholostl'[?], recovered 2 women, and captured 2 — a mixed Spanish–Native punitive force whose gentile allies were the majority.",
       "Punitive column killed the enemy captain",
       ["Prov. Rec. (C-A 24), Sav 430 (probe n431) — Borica → Viceroy, 'Pelea con Indios'"],
       notes="The indigenous name is uncertain on the leaf — verbatim transcription needed."),
    NF("121", "The Jacum battle — capitanejo Charagui defeats the San Diego column", "1837-05", "May 1837", "month",
       [32.617, -116.19], "place", "battle", "frontera",
       "Twenty-five soldados and 50 gentiles auxiliares struck Jacum; 'el capitanejo Charagui… cargó con toda su gente y rodeando nuestras tropas nos las hicieron retirar, hiriéndonos á 9 soldados y 17 indios de los auxiliares… quedó el campo pr los enemigos.' The raiders had already run off the Misión San Diego caballada. Embedded in Zamorano's extermination-rhetoric letter; aftermath, Alvarado ordered all aid to Capt. Portilla for the pursuit (Aug 1837).",
       "Indigenous victory — the field held by Charagui's force",
       ["Dep. St. Pap., Angeles (C-A 37), Doc 188 (n87–n90, Sav 86–89, orig. pp. 420–424); aftermath Doc 193"],
       notes="Charagui's people are named only as gentiles of the Jacum region in the abstract."),
]
for a in additions:
    if a["id"] in seen_ids:
        raise SystemExit("dup id " + a["id"])
    seen_ids.add(a["id"])
features.extend(additions)

out = {
    "id": "military-engagements",
    "title": "Military Engagements in Spanish and Mexican California",
    "subtitle": "Battles, raids, revolts, and standoffs, 1769–1848 — from the military register",
    "abstract": ("Every engagement plotted here is documented in the project's military register, "
                 "compiled from the C-A transcripts (Archives of California), Bancroft, Cook, and "
                 "printed primary collections. Hollow or dashed markers mean the location is approximate "
                 "or conjectural — the source names a district, not a spot. Register numbers (#) key each "
                 "pin to the register's fuller entry and sources."),
    "date_range": [1769, 1848],
    "center": [36.2, -119.6],
    "zoom": 6,
    "cite_key": "military",
    "last_updated": "2026-07-14",
    "layers": [
        {"id": "phase1", "label": "San Diego & Coastal Resistance (1769–1790)", "color": "#c0392b"},
        {"id": "yuma", "label": "Yuma & Colorado River (1781–1820)", "color": "#e67e22"},
        {"id": "phase2", "label": "Bay Area & Central Coast Resistance (1790–1805)", "color": "#2980b9"},
        {"id": "phase3a", "label": "Moraga Interior Campaigns (1806–1810)", "color": "#2e6f40"},
        {"id": "phase3b", "label": "Later Interior Campaigns (1811–1820)", "color": "#8B2500"},
        {"id": "maritime", "label": "Maritime & Foreign Defense", "color": "#16a085"},
        {"id": "infra", "label": "Military Infrastructure", "color": "#7f8c8d"},
        {"id": "mexican", "label": "Mexican Period (1821–1848)", "color": "#9b59b6"},
        {"id": "frontera", "label": "Dominican & Colorado Frontier", "color": "#a8763e"},
        {"id": "missionLayer", "label": "Missions & Presidios (reference)", "color": "#6b6257"},
        {"id": "modernLayer", "label": "Modern City Labels", "color": "#9a938a"}
    ],
    "features": features
}
path = os.path.join(REPO, "data", "military-engagements.json")
json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
print("features:", len(features), "->", path)
print("layers used:", sorted({f["layer"] for f in features}))
