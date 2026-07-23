#!/usr/bin/env python3
"""Build data/secularization-missions.json — The Secularization of the Missions, 1826-1846.

Data assembled 2026-07-23 from the vault C-A survey files (see the per-feature
citations); every ca_record deep link was verified semantically against the
archive catalog export before linking. Per-mission secularization YEARS with no
vault-documented date are [standard account] at year grain (Krell-derived, the
same convention as the missions map's founding years); wherever the vault holds
a comisionado handover or inventory the pin date follows that primary record.

Mission coordinates are read from data/missions-establishments.json (the
G1-audited values) so the two maps can never drift apart.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
me = json.load(open(os.path.join(ROOT, "data", "missions-establishments.json")))
MC = {f["id"]: f["coords"] for f in me["features"]}

STD = "Secularization year per the standard accounts (Krell; cross-checked against CA State Parks / NPS) — year grain."

def feat(fid, name, iso, display, conf, coords, prec, typ, layer, summary,
         sources, result="", series=None, series_label=None, native=None,
         tags=None, notes="", quote=None, register_no=None):
    f = {"id": fid, "register_no": register_no, "name": name,
         "date": {"iso": iso, "display": display, "confidence": conf},
         "coords": coords, "coord_precision": prec, "type": typ, "layer": layer,
         "summary": summary, "result": result, "quote": quote,
         "sources": sources, "native_groups": native or [], "tags": tags or [],
         "notes": notes}
    if series:
        f["series"] = series
        f["series_label"] = series_label or "Secularization record"
    return f

def src(citation, ca=None):
    return {"citation": citation, "ca_record": ca, "ia_leaf_url": None}

def off(mid, dlat=0.0, dlon=0.0):
    c = MC[mid]
    return [round(c[0] + dlat, 4), round(c[1] + dlon, 4)]

MTY = [36.6002, -121.8947]  # Monterey (government seat to 1845)
LA  = [34.0522, -118.2437]  # Los Angeles (Pico's seat, 1845-46)
SD  = [32.7157, -117.1611]  # San Diego (Echeandia's seat)

features = []

# ---------------- Layer: decrees (the legal arc) ----------------
D = [
 ("dec-1826-echeandia-emancipation", "Echeandía opens partial emancipation",
  "1826", "1826", "year", [SD[0], SD[1]], "place",
  "Gov. Echeandía's emancipation program begins: qualified neophytes of the southern missions may leave mission discipline, with individual segregation licenses following (Gil Riela and Andrés Ibarra among the first named). The 1826 San Diego dossier ties the friars' constitutional oath to neophyte emancipation and floats a neophyte pueblo at San Fernando or San Luis Rey.",
  [src("Dep. St. Pap. (C-A 27) Doc 127 (the 1826 oath-and-emancipation dossier).", "ca27-d127"),
   src("Dep. Rec. (C-A 47) Doc 71 (segregation of Gil Riela, 30 Apr 1826).", "ca47-d71")],
  "The proclamation's own text is not in the vault surveys; its execution is. Standard accounts date the proclamation July 1826."),
 ("dec-1827-land-inventory-bando", "Pre-secularization land census ordered",
  "1827-10-07", "October 7, 1827", "exact", [MTY[0]+0.02, MTY[1]], "place",
  "The Diputación orders every mission to report its lands and boundaries before year's end — the first territorial step toward disentailment. The resulting 1828 'Informes sobre terrenos y ganados' series, with each mission's cattle brand, survives in the State Papers: Missions volumes.",
  [src("Dep. St. Pap., Monterey (C-A 43) Doc 1 (bando, 7 Oct 1827).", "ca43-d1"),
   src("St. Pap., Missions (C-A 50) Docs 402–412, 418 (the 1828 informes).")], ""),
 ("dec-1831-echeandia-decree", "Echeandía's secularization decree",
  "1831-01-06", "January 6, 1831", "exact", [SD[0]+0.03, SD[1]+0.04], "place",
  "'Ley secularizando las Misiones, declarándolas pueblos' — 33 articles converting the missions to pueblos under the 1813 Cortes law, San Gabriel and San Carlos first, extended to all by art. 24. Read to the neophytes at the Monterey-district missions that January; suspended by Gov. Victoria within days, denounced to Mexico, and annulled by the central government in April 1832.",
  [src("Dep. Rec. (C-A 49) Doc 224 (the 33 articles, complete).", "ca49-d224"),
   src("St. Pap., Missions & Colonization (C-A 53) Doc 29 (the decree).", "ca53-d29"),
   src("Dep. St. Pap. (C-A 28) Docs 3–5 (promulgation to the neophytes, Jan 1831).", "ca28-d3")],
  "The C-A 49 copy sits after Nov-1831 letters in the volume; the surveys flag the year for verification against Bancroft/Hutchinson."),
 ("dec-1833-mexican-law", "The Mexican secularization law of Aug 17, 1833",
  "1833-08-17", "August 17, 1833", "exact", [MTY[0]+0.048, MTY[1]], "place",
  "The national statute: 'Sobre secularización de las misiones de Alta y Baja California,' converting each mission to a secular parish. The Californian archive's own copy survives in the Superior Government State Papers, with the 26 Nov 1833 colonization companion law that underwrote the Híjar-Padrés colony.",
  [src("Sup. Govt. St. Pap. (C-A 57) Doc 93, orig. pp. 415–416.", "ca57-d93"),
   src("Sup. Govt. St. Pap. (C-A 57) Doc 94 (the 26 Nov 1833 colonization law).")], ""),
 ("dec-1834-gomez-farias", "Gómez Farías: all missions, four months",
  "1834-04-16", "April 16, 1834", "exact", [MTY[0]+0.076, MTY[1]], "place",
  "The general secularization decree from Mexico: ALL the republic's missions to be secularized within four months. It reached California as Figueroa and the Diputación were already drafting their own, more gradual machinery.",
  [src("Sup. Govt. St. Pap. (C-A 57) Doc 95.", "ca57-d95")], ""),
 ("dec-1834-figueroa-reglamento", "Figueroa's Reglamento Provisional",
  "1834-08-09", "August 9, 1834", "exact", [MTY[0]+0.104, MTY[1]], "place",
  "The instrument that actually dismantled the system: missions partially converted to pueblos; each family head a solar of up to 400 varas and half the livestock; article 18 barring the Indians from alienating their grants; article 22 barring mass slaughter of herds. Enacted through the Diputación's article-by-article debate that July, with same-day instructions to the comisionados — general inventories, dissolution of the monjerío, rancherías of 25 families eligible to form pueblos.",
  [src("St. Pap., Missions & Colonization (C-A 53) Doc 78, Sav. 253–257 (the printed reglamento).", "ca53-d78"),
   src("C-A 53 Doc 79 (Instrucciones para los Comisionados, 12 prevenciones).", "ca53-d79"),
   src("Leg. Rec. (C-A 60) Doc 2 (the Diputación debate, Jul 1834).", "ca60-d2"),
   src("Leg. Rec. (C-A 59) Doc 31 (the c. 1828–30 'Plan para convertir en pueblos las Misiones', the Diputación blueprint).", "ca59-d31")], ""),
 ("dec-1839-alvarado-reglamento", "Alvarado's administrators' reglamento",
  "1839-01-01", "January 1, 1839", "exact", [MTY[0]+0.132, MTY[1]], "place",
  "A ~14-article code for the mission administrators — render accounts, no credit against mission property 'por ningún pretexto,' padrón of neophytes — the government's attempt to police the men it had put over the ex-mission estates. A further mission decree followed on 17 Apr 1839.",
  [src("Dep. St. Pap., San José (C-A 45) Doc 68 (the reglamento).", "ca45-d68"),
   src("Dep. Rec. (C-A 49) Doc 639 (the 17 Apr 1839 decree, sent to Durán).")],
  "The standard accounts' 'Jan 17, 1839 regulation' matches neither vault instrument exactly; both are shown."),
 ("dec-1840-mayordomos", "Administrators suppressed, mayordomos created",
  "1840-03-01", "March 1, 1840", "exact", [MTY[0]+0.16, MTY[1]], "place",
  "Alvarado's 1 March 1840 decree suppresses the mission administrators and replaces them with mayordomos under the Visitador's oversight — the government's verdict on six years of administrator rule. Emancipation power was reserved exclusively to the government that October.",
  [src("Dep. St. Pap., LA: Decrees & Despatches (C-A 36) Doc 63, tomo p. 155.", "ca36-d63"),
   src("Dep. Rec. (C-A 49) Doc 646 (16 copies to Durán, 8 Apr 1840).", "ca49-d646"),
   src("Dep. Rec. (C-A 49) Doc 596 (emancipation reserved to the government, 23 Oct 1840).", "ca49-d596")], ""),
 ("dec-1843-micheltorena-return", "Micheltorena returns 12 missions to the friars",
  "1843-03-29", "March 29, 1843", "exact", [MTY[0]+0.188, MTY[1]], "place",
  "The reversal: twelve named missions returned to the padres 'como en tutoría de los Indígenas,' remitting an eighth of their products — after a February order suspending all further alienation of mission lands. The 3 April circular ordering administrators to hand over names ten of them.",
  [src("St. Pap., Missions & Colonization (C-A 53) Doc 175, Sav. 669–674.", "ca53-d175"),
   src("Dep. Rec. (C-A 49) Doc 1043 (the handover circular, 3 Apr 1843).", "ca49-d1043"),
   src("Dep. Rec. (C-A 49) Doc 1016 (the Feb 1843 alienation freeze).")], ""),
 ("dec-1845-pico-reglamento", "Pico's sale-and-lease reglamento",
  "1845-10-28", "October 28, 1845", "exact", [LA[0]+0.02, LA[1]-0.09], "place",
  "The 23-article 'Reglamento para la enajenación y arriendo de las Misiones': sell San Rafael, Dolores, Soledad, San Miguel, and La Purísima; lease the rest for nine years. Chapter 4 declares the neophytes freed and 'no estando obligados á servir á los arrendatarios'; article 20 lets Indians petition for inalienable title to their house and garden plots. Andrés Pico and Juan Manso had been inventorying the missions since May — the commission's object expressly their arrendamiento.",
  [src("Dep. St. Pap., LA: Decrees & Despatches (C-A 36) Doc 107 (verbatim, 23 arts.).", "ca36-d107"),
   src("Dep. Rec. (C-A 49) Doc 1225 (the commission's lease mandate, 1 Jul 1845).", "ca49-d1225"),
   src("C-A 53 Doc 191 (Pico & Manso commissioned, 11 Jul 1845).", "ca53-d191")], ""),
 ("dec-1845-mexico-suspends", "Mexico orders the sales suspended",
  "1845-11-14", "November 14, 1845", "exact", [LA[0]+0.05, LA[1]-0.13], "place",
  "The supreme government, learning what the Department 'ha dispuesto' with the missions, orders all alienation proceedings reported and suspended. The sales went ahead anyway.",
  [src("St. Pap., Missions & Colonization (C-A 53) Doc 181.", "ca53-d181")], ""),
 ("dec-1846-sale-decree", "The Assembly authorizes outright sale",
  "1846-04-03", "April 3, 1846", "exact", [LA[0]+0.08, LA[1]-0.17], "place",
  "Pico's government, invoking the common defense 'en caso de una invasión extranjera,' authorizes auctioning the missions to pay their creditors, any surplus to each mission's Indian community. The June 1846 deeds of sale cite this decree as their authority.",
  [src("Dep. St. Pap., LA: Decrees & Despatches (C-A 36) Doc 110.", "ca36-d110"),
   src("St. Pap., Missions (C-A 51) Doc 160 (the San Buenaventura escritura quoting the 13 Apr decree).", "ca51-d160")], ""),
 ("dec-1846-assembly-annuls", "The Assembly annuls Pico's sales",
  "1846-10-30", "October 30, 1846", "exact", [LA[0]+0.11, LA[1]-0.21], "place",
  "With the American conquest underway, the Departmental Assembly annuls the mission sales (art. 1) while continuing the leases (art. 3). The U.S. courts finished the job: the Supreme Court later voided the San Gabriel and San Luis Rey sales.",
  [src("Unbound Docs. (C-A 63) Doc 479 (verbatim abstract).", "ca63-d479"),
   src("U.S. v. Workman (1863) per Caragozian, CSCHS (standard account).")], ""),
]
for (fid, name, iso, disp, conf, coords, prec, summary, sources, notes) in D:
    features.append(feat(fid, name, iso, disp, conf, coords, prec, "document",
                         "decrees", summary, sources, notes=notes,
                         tags=["secularization", "decree"]))

# ---------------- Layer: missions (21 pins with series) ----------------
# (key, missions-map id, short name, std yr, iso, display, conf, summary,
#  series rows, sources, notes)
M = [
 ("san-diego", "m-san-diego-de-alcala", "San Diego de Alcalá", 1834,
  "1835-04", "secularized 1834; administrator installed Apr 1835", "month",
  "Secularized under the 1834 program; José Joaquín Ortega administered the ex-mission from April 1835. Sold to Santiago Argüello in the last weeks of Mexican rule.",
  [["1835 Apr", "José Joaquín Ortega administrator ($50/month)", "C-A 51 (vault survey)"],
   ["1839", "Salary roll: Ortega $600/yr; mayordomo Rosario Aguilar $18/month", "C-A 50 Doc 453"],
   ["c. 1839", "Inventory with a hand-drawn plano of the ex-mission; district padrón 780–796 neophytes", "C-A 51 Docs 57–58"],
   ["1846 Jun 8", "Sale to Santiago Argüello authorized", "C-A 63 Doc 393"],
   ["1848 Aug", "Down to 186 head of stock", "C-A 63 (vault survey)"]],
  [src("St. Pap., Missions (C-A 51) Docs 57–58 (inventory & plano).", "ca51-d57"),
   src("Unbound Docs. (C-A 63) Doc 393 (the Argüello sale, 8 Jun 1846).", "ca63-d393"), src(STD)],
  "An 1847 charge alleged the Argüello bill of sale was ante-dated (C-A 63 Doc 190)."),
 ("san-luis-rey", "m-san-luis-rey-de-francia", "San Luis Rey", 1834,
  "1835-08-22", "inventoried August 22, 1835", "exact",
  "The richest inventory in the record: $203,787 existencia across the mission and its ranchos (Pala, Santa Margarita, Temécula, San Jacinto). Pío Pico, first a comisionado, administered it to 1840 — removed only under threat of punishment — and its Luiseño residents mounted the most sustained documented resistance to the new order.",
  [["1834–35", "Comisionados Pablo de la Portilla & Pío Pico", "C-A 51 Doc 15"],
   ["1835 Aug 22", "General inventory: existencia $203,787.37 (net $194,436.50)", "C-A 51 Doc 15"],
   ["1840 Jul", "Pico compelled to hand over the mission 'else be punished for disobedience'", "C-A 49 Doc 657"],
   ["1843", "Returned to Fr. Zalvidea via José Antonio Estudillo", "C-A 39 Doc 220"],
   ["1846 Jul", "Handed to Juan M. Marrón on Pico's order", "C-A 51 (vault survey)"]],
  [src("St. Pap., Missions (C-A 51) Doc 15 (the 1835 general inventory).", "ca51-d15"),
   src("Dep. Rec. (C-A 49) Doc 657 (the forced handover order, 23 Jul 1840).", "ca49-d657"), src(STD)],
  "The Cot & Pico sale of 1846 is not in the vault surveys; the July 1846 Marrón handover is."),
 ("san-juan-capistrano", "m-san-juan-capistrano", "San Juan Capistrano", 1833,
  "1833", "secularized 1833 (Echeandía's experiment)", "year",
  "The earliest secularization — Echeandía's pilot — and in 1841 the first ex-mission formally converted to a pueblo, with a 17-article reglamento and a land repartimiento naming its neófitos libres. Sold in December 1845 for $710.",
  [["1838–39", "Administrators Francisco Sepúlveda, then Santiago Argüello ($1,000/yr)", "C-A 51 Docs 45–46"],
   ["1841", "Pueblo conversion under comisionado Juan Bandini; 17-article reglamento; repartimiento of 7,950 varas", "C-A 33 Docs 163–166"],
   ["1843 May", "Returned to Fr. Estenaga", "C-A 49 (vault survey)"],
   ["1845 Dec", "Sold to John Forster & partner, $710 'en moneda, cueros y sebo'", "C-A 51 Doc 161; C-A 63 Doc 508c"]],
  [src("St. Pap., Missions (C-A 51) Doc 161 (Pico's consolidated alienation record).", "ca51-d161"), src(STD)],
  "The two vault sale records disagree on the second buyer — 'James McKinley' (C-A 51 Doc 161) vs 'Santiago Machado' (the título, C-A 63 Doc 508c). Both shown; unresolved."),
 ("san-gabriel", "m-san-gabriel-arcangel", "San Gabriel Arcángel", 1834,
  "1834-11-24", "handed over November 24, 1834", "exact",
  "Handed from Fr. Estenaga to comisionado Nicolás Gutiérrez in November 1834 with 12,980 cattle on its books; by the 1840 inventory the herd had collapsed to 72. Leased under Pico's program — the lease drive began here — and in the vault record assigned to Henry Dalton in February 1846.",
  [["1834 Nov 24", "Entrega Fr. Estenaga → Nicolás Gutiérrez; debts $9,474.36", "C-A 51 Doc 16"],
   ["c. 1835", "Partial inventory: 12,980 cattle, 6,548 sheep, 2,938 horses; 1,323 souls", "C-A 51 Doc 21"],
   ["1840 Apr", "Inventory: 72 cattle, 715 sheep — the estate stripped", "C-A 51 Doc 54"],
   ["1843 Mar", "Returned to Fr. Estenaga under Micheltorena's decree", "C-A 49 Doc 1023"],
   ["1846 Feb", "To Henry (Enrique) Dalton", "C-A 51 Doc 159"]],
  [src("St. Pap., Missions (C-A 51) Doc 16 (the 1834 handover accounts).", "ca51-d16"),
   src("St. Pap., Missions (C-A 51) Doc 54 (the 1840 inventory).", "ca51-d54"), src(STD)],
  "The Reid & Workman sale of June 1846 is not in the vault surveys as read; the U.S. Supreme Court later voided the San Gabriel sale (standard account)."),
 ("san-fernando", "m-san-fernando-rey", "San Fernando Rey", 1834,
  "1834-12-18", "handed over December 18, 1834", "exact",
  "Entrega to comisionado Antonio del Valle in December 1834; a decade later, leased to Andrés Pico and Juan Manso, then sold to Eulogio Célis in June 1846 for $14,000 'para sostener la integridad del Territorio.'",
  [["1834 Dec 18", "Entrega to comisionado Antonio del Valle", "C-A 50 Doc 445"],
   ["1835", "Avalúo: 32,000 vines ($16,000), a 191-volume library", "C-A 51 Doc 28"],
   ["1838", "Inventory: buildings $56,785 + livestock $53,884", "C-A 51 Doc 126"],
   ["1845 Dec 5", "Leased to Andrés Pico & Juan Manso ($1,120/yr; one record $1,125 split gov't/padre/neophytes)", "C-A 51 Doc 161; C-A 63 Doc 517"],
   ["1846 Jun", "Sold to Eulogio Célis, $14,000", "C-A 51 Doc 161"]],
  [src("St. Pap., Missions (C-A 50) Doc 445 (the 1834 entrega).", "ca50-d445"),
   src("St. Pap., Missions (C-A 51) Doc 161.", "ca51-d161"), src(STD)],
  "Lease figures differ between the two vault records ($1,120 vs $1,125); both shown."),
 ("san-buenaventura", "m-san-buenaventura", "San Buenaventura", 1836,
  "1836-06-23", "handover ordered June 23, 1836", "exact",
  "Among the last secularized: Gov. Chico ordered Fr. Blas Ordaz to hand it to Carlos Carrillo in June 1836 amid the constitutional-oath fight. Sold to its lessee José Arnaz in June 1846 — 'dueño legítimo… para siempre' — followed by an 1846–48 asset-stripping dossier.",
  [["1836 Jun 23", "Chico orders handover to Carlos Carrillo", "C-A 53 Doc 157"],
   ["1839–40", "Administrator Rafael González; 5,387 → 5,907 head, 5 looms", "C-A 51 Doc 66"],
   ["1845 Dec 5", "Leased to Narciso Botello & José Arnaz, $1,630/yr", "C-A 51 Doc 161"],
   ["1846 Jun 8", "Sold to José Arnaz (escritura quoting the 13 Apr defense decree)", "C-A 51 Doc 160"]],
  [src("St. Pap., Missions & Colonization (C-A 53) Doc 157 (the Chico expediente).", "ca53-d157"),
   src("St. Pap., Missions (C-A 51) Doc 160 (the deed of sale).", "ca51-d160"), src(STD)],
  "The 1846–48 fraud dossier on the lease is C-A 63 Doc 464."),
 ("santa-barbara", "m-santa-barbara", "Santa Bárbara", 1834,
  "1835-03-15", "inventoried March 15, 1835", "exact",
  "Comisionado Anastacio Carrillo took the richest coastal plant in the 1835 inventory — $113,960 existencia including Rancho Dos Pueblos — with $2,484 in goods distributed to the Indians. Leased in December 1845 to Nicolás Den and Daniel Hill.",
  [["1834", "Comisionado Anastacio Carrillo", "C-A 50 Doc 443"],
   ["1835 Mar 15", "Inventory + avalúo: existencia $113,960.88", "C-A 50 Doc 443"],
   ["1835", "Goods distributed to the Indians: $2,484.37½", "C-A 50 (vault survey)"],
   ["1845 Dec 5", "Leased to Nicolás A. Den & Daniel Hill, $1,260/yr", "C-A 51 Doc 161; C-A 42 Doc 611"]],
  [src("St. Pap., Missions (C-A 50) Doc 443 (the 1835 inventory).", "ca50-d443"),
   src("St. Pap., Missions (C-A 51) Doc 161.", "ca51-d161"), src(STD)], ""),
 ("santa-ines", "m-santa-ines", "Santa Inés", 1836,
  "1836-08-01", "handed over August 1, 1836", "exact",
  "Secularized in the 1836 wave on Chico's order; Fr. Jimeno handed it to José María Covarrubias that August with an existencia of $56,437 — down to $39,284 within six months. Leased in 1845 to Covarrubias himself with Joaquín Carrillo.",
  [["1836 Jun 23", "Chico orders handover to José Mª Ramírez", "C-A 53 Doc 157"],
   ["1836 Aug 1", "Fr. Jimeno → José María Covarrubias; inventory $56,437, 8,040 cattle", "C-A 51 Doc 36"],
   ["1837 Feb", "Net down to $39,284 (admin Francisco Cota)", "C-A 51 (vault survey)"],
   ["1845 Dec 5", "Leased to José M. Covarrubias & Joaquín Carrillo, $580/yr", "C-A 51 Doc 161"]],
  [src("St. Pap., Missions (C-A 51) Doc 36 (the 1836 inventory).", "ca51-d36"),
   src("St. Pap., Missions (C-A 51) Doc 161.", "ca51-d161"), src(STD)], ""),
 ("la-purisima", "m-la-purisima-concepcion", "La Purísima Concepción", 1834,
  "1834", "inventoried 1834", "year",
  "Inventoried under article 15 of Figueroa's reglamento by comisionado Domingo Carrillo, with William Dana as appraiser: existencia $62,088.50 including ranchos Todos Santos and Guadalupe. One of the five missions Pico's reglamento listed for outright sale — bought by John Temple for $10,110 in December 1845.",
  [["1834", "Comisionado Domingo Carrillo; avaluador William Dana; existencia $62,088.50", "C-A 50 Doc 439"],
   ["1838", "Administrator Joaquín Carrillo", "C-A 51 Doc 25"],
   ["1845 Dec", "Sold to Juan (John) Temple, $10,110", "C-A 51 Doc 161"]],
  [src("St. Pap., Missions (C-A 50) Doc 439 (the 1834 inventory).", "ca50-d439"),
   src("St. Pap., Missions (C-A 51) Doc 161.", "ca51-d161"), src(STD)],
  "The survey flags the inventory digits as scale-2 reads pending verification."),
 ("san-luis-obispo", "m-san-luis-obispo-de-tolosa", "San Luis Obispo", 1835,
  "1835", "secularized 1835", "year",
  "A revolving door of administrators (Trujillo, Moreno, Ayala, Canet, Bonilla); 253 souls in 1834. Erected into a pueblo in July 1844 — its emancipados barred from selling their lands — then sold in December 1845 to Scott, Wilson & McKinley.",
  [["1834", "253 souls", "C-A 51 (vault survey)"],
   ["1842 Sep", "Land reparto to the Indians ordered", "C-A 49 (vault survey)"],
   ["1844 Jul 16", "Erected into a pueblo; emancipados may not sell their lands", "C-A 53 Doc 178"],
   ["1845 Dec", "Sold to Scott, Wilson & James McKinley", "C-A 51 Doc 161"]],
  [src("St. Pap., Missions (C-A 51) Doc 161.", "ca51-d161"), src(STD)],
  "The $510 price is the standard account; the vault record gives the buyers, not the price."),
 ("san-miguel", "m-san-miguel-arcangel", "San Miguel Arcángel", 1834,
  "1834", "secularized 1834 (some accounts 1836)", "circa",
  "In January 1831 its neophytes refused Echeandía's secularization outright — 'quieren seguir bajo el actual sistema' — and in 1831 asked to remain 'en estado de Comunidad.' Listed for outright sale in Pico's reglamento; the vault holds no sale record.",
  [["1831 Jan", "Neophytes refuse secularization: 'quieren seguir bajo el actual sistema'", "C-A 28 Doc 3"],
   ["1837", "General inventory: buildings ~$19,500 (admin Vicente García)", "C-A 51 Doc 128"],
   ["1845 Oct", "Listed to SELL in Pico's reglamento", "C-A 36 Doc 107"]],
  [src("Dep. St. Pap. (C-A 28) Doc 3 (the neophytes' refusal, Jan 1831).", "ca28-d3"),
   src("St. Pap., Missions (C-A 51) Doc 128 (the 1837 inventory).", "ca51-d128"), src(STD)],
  "The 1846 Ríos & Reed purchase is the standard account; not found in the vault surveys."),
 ("san-antonio", "m-san-antonio-de-padua", "San Antonio de Padua", 1834,
  "1834-11-12", "handed over November 12, 1834", "exact",
  "Fr. Pedro Cabot delivered the mission to comisionado Manuel Crespo in November 1834; the 1836 inventory totaled $93,122 across eleven named ranchos, with $13,602 distributed to the Indians and a 'Pueblo de San Antonio' of 557 souls. Offered in 1845, it drew no bidders and was never sold.",
  [["1834 Nov 12", "Entrega Fr. Cabot → comisionado Manuel Crespo", "C-A 50 Doc 448"],
   ["1836 Apr 27", "Inventory + avalúo: $93,122.31; 11 ranchos", "C-A 50 (vault survey)"],
   ["1836", "$13,602.37 distributed to the Indians; 'Pueblo de San Antonio — 557 souls'", "C-A 50 (vault survey)"],
   ["1845", "Offered for sale — no bidders", "standard account"]],
  [src("St. Pap., Missions (C-A 50) Doc 448 (the 1834 entrega).", "ca50-d448"), src(STD)], ""),
 ("soledad", "m-nuestra-senora-de-la-soledad", "Nuestra Señora de la Soledad", 1835,
  "1835-08-12", "inventoried August 12, 1835", "exact",
  "Inventoried in August 1835 (~$47,297 — Savage himself noted the figures don't reconcile); 177 souls by 1837. Sold in June 1846 to Feliciano Soberanes, the same encargado instructed in 1840 that 'ningún indígena será forzado á servir á un particular.'",
  [["1835 Aug 12", "Inventory: existencia ~$47,297 (Savage: doesn't reconcile)", "C-A 50 Doc 456"],
   ["c. 1840", "Encargado Feliciano Soberanes: no Indian to be forced to serve a private party", "C-A 30 Doc 62"],
   ["1846 Jun", "Sold to Feliciano Soberanes, $800", "C-A 51 Doc 161"]],
  [src("St. Pap., Missions (C-A 51) Doc 161.", "ca51-d161"), src(STD)], ""),
 ("san-carlos", "m-san-carlos-borromeo-carmel", "San Carlos Borromeo (Carmel)", 1834,
  "1834", "secularized 1834", "year",
  "One of the two missions Echeandía's 1831 decree named to go first. By 1839 juez interino Marcelino Escobar held the buildings under a room-by-room inventory, with solares assigned — two to the neófitos Josecillo and Antonio. Its surplus buildings were saleable under the 1845 reglamento; no sale appears in the vault.",
  [["1839 Mar 11", "Building inventory under juez interino Marcelino Escobar; solares to neófitos", "C-A 33 Doc 8"],
   ["1845 Oct", "Surplus buildings saleable under Pico's reglamento", "C-A 36 Doc 107"]],
  [src("Dep. St. Pap., Juzgados (C-A 33) Doc 8 (the 1839 inventory).", "ca33-d8"), src(STD)], ""),
 ("san-juan-bautista", "m-san-juan-bautista", "San Juan Bautista", 1835,
  "1835-05-09", "handed over May 9, 1835", "exact",
  "Handed over in May 1835 with a $147,413 existencia including Rancho San Felipe, and a padrón of 63 emancipated Indians holding $5,120 in land. An 1849 retrospective recorded it 'declarada pueblo' a dozen years earlier, its mission houses destroyed for materials.",
  [["1835 May 9", "Handover; comisionados Antonio Buelna & José T. Castro; church appraisal", "C-A 51 Doc 14"],
   ["1835", "General inventory: existencia $147,413.12 (net $138,713)", "C-A 51 Doc 26"],
   ["c. 1836", "Emancipated-Indian padrón: 63 individuals, land value $5,120", "C-A 51 (vault survey)"],
   ["1849", "Retrospective: 'declarada pueblo' 12+ years earlier; houses destroyed for materials", "C-A 63 Doc 282"]],
  [src("St. Pap., Missions (C-A 51) Doc 14 (the 1835 handover).", "ca51-d14"), src(STD)], ""),
 ("santa-cruz", "m-santa-cruz", "Santa Cruz", 1834,
  "1835-12-01", "inventoried December 1, 1835", "exact",
  "Comisionado Ignacio del Valle inventoried ~$84,354 in December 1835. Listed for outright sale in Pico's reglamento; no sale appears in the vault — and in 1849 Hartnell judged that the priest 'has no right at all to sell any real estate or the mission Sta Cruz.'",
  [["1835 Dec 1", "Inventory + avalúo: existencia ~$84,354.62 (comisionado Ignacio del Valle)", "C-A 50 Doc 452"],
   ["1839 Jan", "Francisco Soto named administrator", "C-A 49 (vault survey)"],
   ["1845 Oct", "Listed to SELL in Pico's reglamento", "C-A 36 Doc 107"],
   ["1849", "Hartnell: the priest has no right to sell the mission's real estate", "C-A 63 Doc 132"]],
  [src("St. Pap., Missions (C-A 50) Doc 452 (the 1835 inventory).", "ca50-d452"), src(STD)], ""),
 ("santa-clara", "m-santa-clara-de-asis", "Santa Clara de Asís", 1836,
  "1836", "secularized 1836", "year",
  "Administered by the Estradas, then Ignacio Alviso, whose 1840 handover inventory counted 3,847 cattle (down from 5,500 the year before). Its mission houses were barred from sale in 1845; in 1849 the priests leased Santa Clara and San José together to James D. Steinberger for $22,000.",
  [["1840 May 15", "Handover Estrada → Ignacio Alviso: 3,847 cattle, 4,807 sheep", "C-A 51 Doc 99"],
   ["1845", "Mission houses prohibited from sale", "C-A 53 Doc 179"],
   ["1849", "Sta Clara + S. José leased to James D. Steinberger, $22,000", "C-A 63 Doc 388"]],
  [src("St. Pap., Missions (C-A 51) Doc 99 (the 1840 handover).", "ca51-d99"), src(STD)], ""),
 ("san-jose", "m-san-jose", "San José", 1834,
  "1834", "secularized 1834", "year",
  "Still the great stock estate of the north after secularization — José de Jesús Vallejo's 1840 receipt counted 20,000 cattle and 15,000 sheep — while draining $16,809 to the government. Hartnell's 1840 visita found 589 souls who 'quieren otro administrador.'",
  [["1837 Jan", "Ex-admin J. J. Vallejo → José Mª de Jesús González", "C-A 51 (vault survey)"],
   ["1840", "Receipt from Vallejo: 20,000 cattle, 15,000 sheep, 520 horses", "C-A 51 Doc 102"],
   ["1840 Aug 30", "Hartnell's visita: 589 souls; 'quieren otro administrador'", "C-A 51 Doc 143"],
   ["1849", "Leased with Santa Clara to Steinberger", "C-A 63 Doc 388"]],
  [src("St. Pap., Missions (C-A 51) Doc 143 (Hartnell's San José visita).", "ca51-d143"), src(STD)],
  "The reported 1845/46 sale is disputed between the standard accounts and not in the vault; left open."),
 ("dolores", "m-san-francisco-de-asis-dolores", "San Francisco de Asís (Dolores)", 1834,
  "1835-07-28", "inventoried July 28, 1835", "exact",
  "Inventoried at $67,227 in July 1835 under comisionados Ignacio del Valle and José Joaquín Estudillo; by the 1841 padrón, 78 souls remained. One of the five listed for outright sale in 1845; no sale record survives in the vault.",
  [["1835 Jul 28", "Inventory: existencia $67,227 (net $60,004); Rancho San Mateo $4,346", "C-A 51 Doc 27"],
   ["1840", "Ex-admin José de la Cruz Sánchez → mayordomo Tiburcio Vásquez, via Hartnell", "C-A 51 (vault survey)"],
   ["1841", "Padrón: 78 souls, 1,514 head", "C-A 51 (vault survey)"],
   ["1845 Oct", "Listed to SELL in Pico's reglamento", "C-A 36 Doc 107"]],
  [src("St. Pap., Missions (C-A 51) Doc 27 (the 1835 inventory).", "ca51-d27"), src(STD)], ""),
 ("san-rafael", "m-san-rafael-arcangel", "San Rafael Arcángel", 1834,
  "1834-12-31", "inventoried December 31, 1834", "exact",
  "The poorest inventory of the set ($18,474, with Rancho Nicasio at $7,256), but the most direct distribution: 343 Indians received rams, ewes, horses, and mares by name. By Hartnell's 1840 visita they refused a mayordomo altogether — 'no querían ya misión.'",
  [["1834 Dec 31", "Inventory + avalúo: existencia $18,474; Rancho Nicasio $7,256.50", "C-A 50 Doc 458"],
   ["1834–35", "343 Indians receive 463 rams, 828 ewes, 97 horses, 343 mares", "C-A 50 Doc 457"],
   ["1836 Nov", "Comisionado Ignacio Martínez → John (Juan) Reed", "C-A 51 (vault survey)"],
   ["1840 May", "Indians refuse mayordomo Briones: 'no querían ya misión'", "C-A 51 Doc 149"]],
  [src("St. Pap., Missions (C-A 50) Doc 458 (the 1834 inventory).", "ca50-d458"),
   src("St. Pap., Missions (C-A 51) Doc 149 (Hartnell's San Rafael report).", "ca51-d149"), src(STD)],
  "The reported $8,000 sale of 1846 is the standard account; no vault record."),
 ("solano", "m-san-francisco-solano-sonoma", "San Francisco Solano (Sonoma)", 1834,
  "1834", "secularized 1834", "year",
  "Secularized under M. G. Vallejo as comisionado (standard account); the vault's mission-property record names Vallejo, Salvador Vallejo, and mayordomo Antonio Ortega, and shows the mission's stock drawn down for the frontier colony and recruitment in 1835. Its final disposition does not appear in the vault surveys.",
  [["1834–35", "M. G. Vallejo comisionado; Salvador Vallejo & mayordomo Antonio Ortega in the property record", "C-A 53 Doc 140"],
   ["1835", "Vallejo 'ocupado en recluta, ración de la Misión y matanzas'", "C-A 29 Doc 30"]],
  [src("St. Pap., Missions & Colonization (C-A 53) Doc 140.", None), src(STD)],
  "Excluded (with San Rafael) from the Diputación's c. 1828–30 pueblo plan as too new."),
]
for (key, mid, name, yr, iso, disp, conf, summary, series, sources, notes) in M:
    features.append(feat("sec-" + key, "Mission " + name, iso, disp, conf,
                         MC[mid], "exact", "mission", "missions", summary,
                         sources, series=series, notes=notes,
                         tags=["secularization"]))

# ---------------- Layer: colony (Hijar-Padres) ----------------
C = [
 ("col-natalia-arrival", "The Híjar-Padrés colony lands at San Diego",
  "1834-09-01", "September 1, 1834", "exact", [SD[0]-0.05, SD[1]-0.03], "place",
  "The brigantine Natalia — the Compañía Cosmopolitana's own ship — reaches San Diego with Director General José María Híjar, Buenaventura Araujo, and 129 colonists, the vanguard of the ~204-person colonization scheme budgeted at 45,206 pesos under the 26 Nov 1833 law. The mission estates were to be its endowment.",
  [src("Dep. St. Pap. (C-A 28) Doc 243 (the arrival report, 4 Sep 1834).", "ca28-d243"),
   src("St. Pap., Missions & Colonization (C-A 53) Docs 51–53, 90–93 (appointment, roster, budget).")], ""),
 ("col-contramando", "Figueroa keeps the missions: the contramando",
  "1834-10-22", "October 21–22, 1834", "exact", [MTY[0]-0.03, MTY[1]-0.05], "place",
  "Santa Anna's countermand — carried north 'por extraordinario violento' — orders Figueroa not to hand Híjar the political command; the Diputación's acuerdo goes further: neither the command 'ni los bienes de las Misiones, que son propiedad de los indios.' The colony is stranded, and the principle that the estates belong to the Indians is stated at its plainest.",
  [src("Dep. St. Pap., LA: Official Corr. (C-A 37) Doc 73 (the countermand, leaf-verified).", "ca37-d73"),
   src("C-A 37 Doc 78 (the Diputación acuerdo, 22 Oct 1834).", "ca37-d78")],
  "", ),
 ("col-araujo-rising", "Araujo and the armed rising at San Gabriel",
  "1834-11", "November 1834", "month", off("m-san-gabriel-arcangel", 0.035, -0.045), "place",
  "In the colony crisis's ugliest episode, ~200 armed Indians briefly seize Fr. Estenaga at San Gabriel; colony officer Buenaventura Araujo is charged with instigating the rising. Ten northern missions are nonetheless ordered to provision the stranded colonists for a year.",
  [src("Dep. St. Pap. (C-A 28) Docs 249, 253, 257–260 (the Araujo proceedings).")], ""),
 ("col-loriot-deportation", "Híjar and Padrés deported on the Loriot",
  "1835-04-30", "April 30, 1835", "exact", [MTY[0]-0.055, MTY[1]-0.09], "place",
  "After the Los Angeles plot to depose Figueroa and halt secularization, the colony's leadership is shipped to Mexico: the Loriot's six-article instructions name Híjar, Padrés, Francisco Torres, and Apalátegui among the deportees. Figueroa's manifesto had already given the government's verdict: 'el verdadero y único objeto de su plan es el robo de los bienes de las misiones.' Padrés protested his rights from on board.",
  [src("Dep. St. Pap. (C-A 29) Doc 25 (the Loriot instructions).", "ca29-d25"),
   src("Dep. St. Pap., Benicia (C-A 39) Docs 187–…, and C-A 29 Docs 11–30 (the crisis dossier).")], ""),
]
for (fid, name, iso, disp, conf, coords, prec, summary, sources, notes) in C:
    features.append(feat(fid, name, iso, disp, conf, coords, prec, "event",
                         "colony", summary, sources, notes=notes,
                         tags=["hijar-padres", "secularization"]))

# ---------------- Layer: visitas (Hartnell 1839-40) ----------------
V = [
 ("vis-hartnell-appointed", "Hartnell named Visitador General",
  "1839-01-19", "January 19, 1839", "exact", [MTY[0]-0.03, MTY[1]-0.10], "place",
  "William Hartnell is named Visitador of the missions at $2,000 a year — the government's inspector over its own administrators — his salary apportioned mission by mission. His two circuits of 1839–40 produced the most unsparing record of the ex-mission estates that survives.",
  [src("Dep. Rec. (C-A 49) Doc 397 (the appointment).", "ca49-d397"),
   src("Dep. Rec. (C-A 49) Doc 434 (the salary apportionment).")],
  "He resigned 6 Oct 1840 and ceased functions 7 Nov 1840 (C-A 49 Doc 660; C-A 51 Doc 150).",
  None,
  [["1839 Jan 19", "Named Visitador, $2,000/yr", "C-A 49 Doc 397"],
   ["1839 Mar 30", "Takes the oath; departs on the southern circuit in April", "C-A 49 (vault survey)"],
   ["1839 Aug 28", "His Instructions to Administrators: punishment capped at 25 lashes; no reprisals against Indians who complain", "C-A 51 Doc 109"],
   ["1840 Oct–Nov", "Resigns; functions cease", "C-A 49 Doc 660; C-A 51 Doc 150"]]),
 ("vis-southern-1839", "The southern visita: 'los indios son acreedores'",
  "1839-06-24", "June 24, 1839", "exact", off("m-san-fernando-rey", 0.035, 0.045), "place",
  "Hartnell's report on the missions from San Diego to San Fernando: the San Dieguito Indians 'son acreedores á la tierra que reclaman'; San Juan Capistrano's community memorial against administrator Argüello arrives 'firmado por José Fermín á nombre de la comunidad'; San Fernando counts 416 souls, its Rancho San Francisco 'taken from them and given to Antonio del Valle.'",
  [src("St. Pap., Missions (C-A 51) Doc 151 (the 24 Jun 1839 report).", "ca51-d151")], "", ["Kumeyaay", "Acjachemen", "Tataviam"]),
 ("vis-san-rafael-1840", "San Rafael: 'no querían ya misión'",
  "1840-05", "May 1840", "month", off("m-san-rafael-arcangel", 0.035, 0.045), "place",
  "On the northern circuit Hartnell finds the San Rafael Indians refusing mayordomo Gregorio Briones and refusing the institution itself — 'no querían ya misión.' His 14 May report to Jimeno Casarín is the keystone document of Indian liberty in the northern ex-missions.",
  [src("St. Pap., Missions (C-A 51) Doc 149 (the San Rafael report).", "ca51-d149")], "", ["Coast Miwok"]),
 ("vis-yerba-buena-arrest", "Vallejo arrests the Visitador",
  "1840-05-08", "May 8, 1840", "exact", [37.7985, -122.4056], "place",
  "At Yerba Buena, M. G. Vallejo intercepts and arrests Hartnell rather than let the inspection reach his Sonoma frontier arrangements — the plainest demonstration of where power over the ex-mission estates actually lay.",
  [src("St. Pap., Missions (C-A 51) Doc 149 (reported with the San Rafael visitation).", "ca51-d149")], ""),
 ("vis-san-jose-1840", "San José visita: 589 souls, 50 lashes",
  "1840-08-30", "August 30, 1840", "exact", off("m-san-jose", 0.035, 0.045), "place",
  "Hartnell counts 589 souls at Mission San José, records punishments running to 50 lashes — double his own 25-lash cap — and the Indians' verdict: 'quieren otro administrador.'",
  [src("St. Pap., Missions (C-A 51) Doc 143.", "ca51-d143")], "", ["Ohlone"]),
 ("vis-san-diego-1840", "San Diego district: Pico, Temecula, and inventory fraud",
  "1840-08-26", "August 26, 1840", "exact", [SD[0]+0.045, SD[1]+0.05], "place",
  "The southern return visit: Pico has told the Indians the governor gave him Temecula; Las Flores brings its complaints; and comisionado Carlos Castro's inventory fraud is recorded — the Visitador's file on how the estates were actually being run.",
  [src("St. Pap., Missions (C-A 51) Doc 148 (the 26 Aug 1840 report).", "ca51-d148")], "", ["Luiseño", "Kumeyaay"]),
]
for item in V:
    fid, name, iso, disp, conf, coords, prec, summary, sources, notes = item[:10]
    native = item[10] if len(item) > 10 else None
    series = item[11] if len(item) > 11 else None
    features.append(feat(fid, name, iso, disp, conf, coords, prec, "event",
                         "visitas", summary, sources, notes=notes,
                         native=native, series=series,
                         series_label="Hartnell's visitaduría" if series else None,
                         tags=["hartnell", "secularization"]))

# ---------------- Layer: voices (Indian responses) ----------------
VO = [
 ("voice-san-miguel-1831", "San Miguel refuses secularization",
  "1831-01", "January 1831", "month", off("m-san-miguel-arcangel", 0.035, 0.045),
  "Read Echeandía's bando, the San Miguel neophytes answer that 'quieren seguir bajo el actual sistema' — while San Luis Obispo's elect four Indian comisarios de policía under it. The record of divided Indian judgments on emancipation, at the very start.",
  [src("Dep. St. Pap. (C-A 28) Docs 3–5 (the promulgation record).", "ca28-d3")],
  ["Salinan"], "Later (1831) they ask to remain 'en estado de Comunidad.'"),
 ("voice-1833-southern-mobilization", "The southern missions demand the promised land",
  "1833-02-08", "February 8, 1833", "exact", off("m-san-luis-rey-de-francia", -0.045, -0.05),
  "Neophytes of San Diego, San Juan Capistrano, San Gabriel, and San Luis Rey mobilize to demand the land distribution Echeandía had promised — proclaiming the reformer governor against his replacement. Secularization's first mass Indian politics.",
  [src("Dep. St. Pap., LA (C-A 34) Doc 330.", "ca34-d330"),
   src("Dep. St. Pap. (C-A 28) Docs 115–116.")],
  ["Kumeyaay", "Acjachemen", "Tongva", "Luiseño"], ""),
 ("voice-slr-refusal-1835", "'Somos libres': San Luis Rey refuses to work",
  "1835-01", "December 1834 – March 1835", "circa", off("m-san-luis-rey-de-francia", 0.035, 0.045),
  "Portilla's reports from San Luis Rey: the Luiseños refuse absolutely to return to mission labor — 'somos libres, no queremos volver, no queremos trabajar.' The plainest statement of what emancipation meant to the emancipated.",
  [src("St. Pap., Missions (C-A 51) Doc 156 (Portilla → Figueroa).", "ca51-d156")],
  ["Luiseño"], ""),
 ("voice-sjc-petition-1839", "'Que no nos pelen las nalgas á azotes'",
  "1839-04-08", "April 8, 1839", "exact", off("m-san-juan-capistrano", 0.035, 0.045),
  "The San Juan Capistrano neophytes — fewer than 60 still working, the rest fleeing — petition Alvarado against their administrator in their own unsparing words: that they not be flogged raw. Received weeks into Hartnell's visitaduría, it is the Indian-voice document of the administrator era.",
  [src("St. Pap., Missions (C-A 51) Doc 47 (the petition).", "ca51-d47")],
  ["Acjachemen"], ""),
 ("voice-las-flores-1835", "The Las Flores bargain",
  "1835-08-22", "1835 (Figueroa's oficio of May 29)", "circa", off("a-las-flores-asistencia", 0.0, -0.04),
  "Figueroa's oficio records the pueblo de Las Flores — the neophyte pueblo created from San Luis Rey's asistencia — accepting liberty in exchange for subsisting on its own labor. One of the few documented free-Indian pueblos of the secularization.",
  [src("Unbound Docs. (C-A 63) Doc 15 (transcribing the 29 May 1835 oficio).", "ca63-d15")],
  ["Luiseño"], ""),
 ("voice-temecula-1840", "Temecula and Pala stand armed against the Picos",
  "1840-11", "November 1840", "month", [33.4936, -117.1484],
  "When the Picos moved on Temecula — Pico telling the Indians the governor had given it to him — the juzgado record shows the rancherías in arms: 'toda la gente está armada.' The Luiseño ranchos defended the land through the juzgado and, when needed, with weapons in hand.",
  [src("St. Pap., Missions (C-A 51) Doc 141 (the juzgado record).", "ca51-d141"),
   src("Dep. St. Pap., Benicia Mil. (C-A 20) Doc 226 (the Temecula land conspiracy record: the land 'propiedad de todos').")],
  ["Luiseño"], ""),
 ("voice-cupertino-1840", "José Cupertino petitions for absolute emancipation",
  "1840-09-30", "September 30, 1840", "exact", off("m-santa-clara-de-asis", 0.035, 0.045),
  "A sixty-year-old Santa Clara man, in service since childhood, petitions for his absolute emancipation — the individual face of the paper freedom the decade had constructed.",
  [src("Dep. St. Pap., Prefecturas y Juzgados (C-A 42) Doc 687.", "ca42-d687")],
  ["Ohlone"], ""),
 ("voice-feliciana-valdes-1839", "'Como á hija de la Misión': Feliciana Valdés claims land",
  "1839-06-21", "June 21, 1839", "exact", [SD[0]+0.075, SD[1]+0.09],
  "An Indian woman petitions for her share of the secularized lands 'como á hija de la Misión' — a daughter's claim on the estate. Hartnell denied it; the file preserves a woman's legal argument for what secularization had promised.",
  [src("St. Pap., Missions & Colonization (C-A 53) Docs 168–172.", "ca53-d168")],
  ["Kumeyaay"], ""),
]
for (fid, name, iso, disp, conf, coords, summary, sources, native, notes) in VO:
    features.append(feat(fid, name, iso, disp, conf, coords, "place", "event",
                         "voices", summary, sources, native=native, notes=notes,
                         tags=["indian-voice", "secularization"]))

data = {
 "id": "secularization-missions",
 "title": "The Secularization of the Missions",
 "subtitle": "1826–1846",
 "abstract": ("How the mission system was dismantled: the legal arc from Echeandía's 1826 "
  "emancipations through the Mexican law of 1833, Figueroa's 1834 reglamento, Hartnell's "
  "visitas, Micheltorena's 1843 reversal, and Pico's 1845–46 sales and leases — with all "
  "21 missions' documented handovers, inventories, and dispositions, the Híjar-Padrés "
  "colony crisis, and a layer of Indian responses in their own recorded words. Mission pin "
  "dates follow the vault-verified comisionado handovers and inventories in the Savage "
  "transcripts (C-A 28, 33, 36, 42–43, 45, 47, 49–51, 53, 57, 59–60, 63) wherever they "
  "exist; where only a conventional year survives, the pin says so and carries year-grain "
  "confidence. Per-mission secularization years otherwise follow the standard accounts "
  "(Krell-derived), a tertiary source used at year grain only. This map argues nothing the "
  "documents do not: the estates were declared the Indians' property in 1834 and were "
  "gone by 1846; the record of who took them, and of what the Indians said, is what is "
  "plotted here."),
 "date_range": [1826, 1847],
 "center": [35.3, -119.6],
 "zoom": 6,
 "cite_key": "secularization",
 "last_updated": "2026-07-23",
 "layers": [
  {"id": "decrees", "label": "The Legal Arc (decrees & reglamentos)", "color": "#6d4c2f"},
  {"id": "missions", "label": "The 21 Missions (handover / inventory / disposition)", "color": "#2e5a4b"},
  {"id": "colony", "label": "The Híjar-Padrés Colony Crisis (1834–35)", "color": "#8e44ad"},
  {"id": "visitas", "label": "Hartnell's Visitas (1839–40)", "color": "#275d7a"},
  {"id": "voices", "label": "Indian Responses, in the Record's Words", "color": "#c0392b"}
 ],
 "legend_note": ("Event pins near mission sites are offset slightly for legibility; the "
  "decree pins at Monterey and Los Angeles are laddered by date. Mission popups carry a "
  "dated series table of the documented secularization record."),
 "features": features
}

out = os.path.join(ROOT, "data", "secularization-missions.json")
json.dump(data, open(out, "w"), indent=1, ensure_ascii=False)
print("wrote", out, len(features), "features")
