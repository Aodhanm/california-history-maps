#!/usr/bin/env python3
# ARCHIVAL/one-time or session-built script, kept for provenance and reproducibility.
# Paths referencing the original session scratchpad will need adjusting to rerun.
"""Build gallery/gallery-data.json from the vault catalog (historical-map-collection.md).

Captions: Aodhan's placeholder voice (plain sentences, no dashes, brief analysis).
Facts only from the catalog's verified rows or the holding library's record;
catalog-label dates say so. He may rewrite any caption later.
"""
import json, os, subprocess

REPO = os.path.expanduser("~/california-history-maps")
IMG = os.path.join(REPO, "gallery", "img")

LOC = "Library of Congress, Geography and Map Division. Public domain."
RUM = "Courtesy David Rumsey Map Collection, David Rumsey Map Center, Stanford Libraries. CC BY-NC-SA."
JCB = "John Carter Brown Library, Brown University. Open access."
STA = "Stanford Libraries, Barry Lawrence Ruderman Map Collection."
LAPL = "Los Angeles Public Library, Tessa digital collection."
COM = "Wikimedia Commons. Public domain."

GROUPS = [
    {"id": "g1775", "label": "The 1775 Expedition Charts",
     "intro": "Manuscript charts from the 1775 Hezeta and Bodega y Quadra expedition, the voyage that discovered Bodega Bay, plus related Spanish manuscript charts. The Library of Congress acquired this collection in 2024, so several of these charts may be unrecorded in Wagner's standard cartobibliography."},
    {"id": "atlas1799", "label": "The Spanish Hydrographic Atlas (1799)",
     "intro": "A 25 sheet manuscript atlas, Cartas esfericas y planos de los puertos, the Spanish Navy's synthesis of its Pacific coast port surveys from 1775 to 1796. Sheet identifications follow the Library of Congress contents list and sheet order. Where a sheet's own title has not been read yet, the caption says so."},
    {"id": "spanmex", "label": "Spanish and Mexican California",
     "intro": "Spanish colonial cartography of Alta California and the maps the independent Mexican republic made of it."},
    {"id": "russian", "label": "Russian California and the Duflot de Mofras Atlas",
     "intro": "The cartography of the Russian presence at Fort Ross and Bodega, mostly through Duflot de Mofras, the French attache whose 1844 atlas recorded the coast in the last years of Mexican rule."},
    {"id": "foreign", "label": "Foreign Surveys",
     "intro": "British, French, and American naval surveys of the California coast. For most of its existence Spanish and Mexican California was better charted by foreign navies than by its own government."},
    {"id": "claims", "label": "Claims and Boundary Maps",
     "intro": "The maps empires argued with. American, British, and Mexican maps drawing competing claims across the continent, from Drake's New Albion to the Treaty of Guadalupe Hidalgo."},
    {"id": "conquest", "label": "Conquest and Gold Rush",
     "intro": "The American arrival on paper. Military reconnaissance, the first US government maps of the ceded territory, and the first American surveys of California's towns and harbors."},
]

I = []  # (file, group, title, maker, year, source_url, credit, caption, flags)

def add(file, group, title, maker, year, url, credit, caption, better_copy=False):
    I.append({"file": file, "group": group, "title": title, "maker": maker,
              "year": year, "source_url": url, "credit": credit,
              "caption": caption, "better_copy": better_copy})

# ── 1775 expedition set ──
add("loc-bq05-plano-puerto-capitan-bodega-1775.jpg", "g1775",
    "Plano del Puerto del Capitan Bodega", "Bodega y Quadra and Francisco Mourelle", "1775",
    "https://www.loc.gov/resource/gmdfindingaids.2024593595/?sp=10", LOC,
    "Manuscript chart of Bodega Bay, drawn by Bodega y Quadra and his pilot Francisco Mourelle on the voyage that discovered it. Keyed points mark Punta del Cordon, Punta de Arenas, and Punta de Murguia, with soundings at the entrance. This is the founding map of the Spanish claim to the port.")
add("loc-bq01-carta-reducida-bodega-mourelle-1775.jpg", "g1775",
    "Carta reducida de las costas y mares septentrionales de la California", "Bodega y Quadra and Mourelle", "1775 or after",
    "https://www.loc.gov/resource/gmdfindingaids.2024593595/?sp=2", LOC,
    "The large general chart of the 1775 voyage, 130 by 81 cm in the original. It carries the whole track of the expedition up the coast.")
add("loc-bq04-carta-reducida-bodega-small-1775.jpg", "g1775",
    "Carta reducida (small version)", "Bodega y Quadra and Mourelle", "1775 or after",
    "https://www.loc.gov/resource/gmdfindingaids.2024593595/?sp=8", LOC,
    "The small version of the same general chart, 40 by 24 cm in the original.")
add("loc-bq02-carta-reducida-hezeta-1775.jpg", "g1775",
    "Carta reducida (Hezeta)", "Bruno de Hezeta", "1775",
    "https://www.loc.gov/resource/gmdfindingaids.2024593595/?sp=4", LOC,
    "Hezeta's own general chart of the 1775 expedition, 68 by 45 cm in the original. Hezeta commanded the voyage; Bodega y Quadra commanded the schooner Sonora.")
add("loc-bq03-carta-reducida-hezeta-small-1775.jpg", "g1775",
    "Carta reducida (Hezeta, small version)", "Bruno de Hezeta", "1775",
    "https://www.loc.gov/resource/gmdfindingaids.2024593595/?sp=6", LOC,
    "The small version of Hezeta's chart, 40 by 28 cm in the original.")
add("loc-bq06-plano-puerto-trinidad-1775.jpg", "g1775",
    "Plano del Puerto de la Trinidad", "Hezeta, Bodega y Quadra, and Mourelle", "1775",
    "https://www.loc.gov/resource/gmdfindingaids.2024593595/?sp=12", LOC,
    "Chart of Trinidad harbor at 41 degrees 7 minutes, where the expedition raised a cross and took possession in June 1775.")
add("loc-bq07-bahia-asumpcion-entrada-ezeta-1775.jpg", "g1775",
    "Plano de la Bahia de la Asumpcion o entrada de Ezeta", "Bruno de Hezeta", "1775",
    "https://www.loc.gov/resource/gmdfindingaids.2024593595/?sp=14", LOC,
    "The Spanish discovery chart of the Columbia River mouth, drawn seventeen years before Robert Gray crossed the bar and named the river. Hezeta sighted the entrance in August 1775 but could not enter it.")
add("loc-bq08-rada-bucareli-1775.jpg", "g1775",
    "Plano de la Rada de Bucareli", "Bruno de Hezeta", "1775",
    "https://www.loc.gov/resource/gmdfindingaids.2024593595/?sp=16", LOC,
    "Hezeta's chart of an anchorage at 47 degrees 24 minutes on the Washington coast.")
add("loc-bq09-puerto-bucareli-1775.jpg", "g1775",
    "Plano de la entrada o Puerto de Bucareli", "Bodega y Quadra and Mourelle", "1775",
    "https://www.loc.gov/resource/gmdfindingaids.2024593595/?sp=18", LOC,
    "The port at 55 degrees 17 minutes in southeast Alaska, the farthest major survey of the Sonora's push north.")
add("loc-bq10-puerto-remedios-1775.jpg", "g1775",
    "Plano del Puerto de los Remedios", "Bodega y Quadra and Mourelle", "1775",
    "https://www.loc.gov/resource/gmdfindingaids.2024593595/?sp=20", LOC,
    "Chart of the port at 57 degrees 18 minutes, near the northern limit of the 1775 voyage.")
add("loc-bq12-carta-reducida-1780-expediciones.jpg", "g1775",
    "Carta reducida entre el grado 36 y el 61", "Bodega y Quadra", "circa 1780",
    "https://lccn.loc.gov/2024593609", LOC,
    "Bodega y Quadra's summary chart of both his northern voyages, 1775 and 1779. The cartouche names the ships Hezeta, Sonora, Princesa, and Favorita.")
add("loc-bq11-puerto-sidman-1792.jpg", "g1775",
    "Plano del Puerto Sidman", "after Captain Baker", "circa 1792",
    "https://lccn.loc.gov/2024593596", LOC,
    "Spanish manuscript chart of a port reconnoitered by Captain Baker of Vancouver's expedition, evidence of how quickly Spanish cartographers absorbed British survey work.")
add("loc-bq13-plano-san-diego-1782-pantoja.jpg", "g1775",
    "Plano del puerto de San Diego", "Juan Pantoja y Arriaga", "1782",
    "https://lccn.loc.gov/2017588148", LOC,
    "Pantoja's chart of San Diego harbor, the base survey behind most later Spanish charts of the port.")
add("loc-bq14-carta-descubrimientos-costa-no-1850copy.jpg", "g1775",
    "Carta de los descubrimientos de la costa N.O. (19th century copy)", "unknown copyist, after an original of the early 1790s", "circa 1850",
    "https://lccn.loc.gov/99446215", LOC,
    "A manuscript copy, dated by the Library of Congress to about 1850, of a chart of the northwest coast discoveries dedicated to Viceroy Revilla Gigedo. Useful for content, but it is a copy, not a period sheet.")

# ── 1799 atlas ──
ATLAS = [
    ("01", "Carta reducida, Acapulco to Unalaska", "Bodega y Quadra, 1792",
     "The atlas's general chart, running the whole coast from Acapulco to Unalaska. Drawn under Bodega y Quadra in 1792. This is the largest sheet in the set and its identity is confirmed from the sheet.", True),
    ("02", "Puerto de Acapulco", "Montes, 1796", None, False),
    ("03", "Puerto de San Blas", "Camacho, 1779", None, False),
    ("04", "Puerto de San Diego", "after the Vizcaino era surveys", None, False),
    ("05", "Santa Barbara and Purisima ensenadas, with Todos Santos", "Pantoja and Tovar, 1782", None, False),
    ("06", "Puerto de Monterey", None, None, False),
    ("07", "Puerto de San Francisco", "Camacho, 1779", None, False),
    ("08", "Plano del Puerto de la Bodega", "surveyed 1775, resurveyed 1793",
     "Bodega Bay as resurveyed in 1793, the year of the failed Spanish attempt to occupy it. The title states the port was discovered by Bodega y Quadra in 1775 and reconnoitered in 1793. Identity confirmed from the sheet. The left margin of this file is soft because the Library of Congress high resolution derivative is corrupt and the sheet was rebuilt from tiles.", True),
    ("09", "Puerto de la Trinidad", "Hezeta, 1775", None, False),
    ("10", "Entrada de Ezeta o Rio de la Columbia", "as reexamined 1793", None, False),
    ("11", "Puerto Grek", "Martinez y Zayas, 1793", None, False),
    ("12", "Interior channels, 48 to 50 degrees, with five port insets", "1791 surveys", None, False),
    ("13", "Strait of Juan de Fuca", "1793", None, False),
    ("14", "Nitinat", "Carrasco", None, False),
    ("15", "Clayocuat", None, None, False),
    ("16", "Coast from Futusi to San Francisco", "1793", None, False),
    ("17", "Nutka", None, None, False),
    ("18", "San Lorenzo de Nuca", "Malaspina expedition, 1791", None, False),
    ("19", "Puerto Gaston", None, None, False),
    ("20", "Puerto Floridablanca", None, None, False),
    ("21", "Puerto Bazan", None, None, False),
    ("22", "Puerto de los Dolores", None, None, False),
    ("23", "Puerto de Bucarely", None, None, False),
    ("24", "Puerto de la Regla", "1779", None, False),
    ("25", "Puerto de Santiago", "1779", None, False),
]
CAVEAT = ("The identification follows the Library of Congress contents list and the sheet order, "
          "and has not been confirmed from the sheet itself.")
for nn, sub, maker, cap, confirmed in ATLAS:
    f = f"loc-cartas-esfericas-1799-sheet{nn}.jpg" if nn != "08" else "loc-cartas-esfericas-1799-sheet08-bodega-1793.jpg"
    caption = cap or (f"Sheet {int(nn)} of the Spanish Navy's manuscript atlas of Pacific port surveys, 1775 to 1796. "
                      f"Per the contents list it shows {sub}" + (f", surveyed by {maker}" if maker else "") + f". {CAVEAT}")
    add(f, "atlas1799", f"Cartas esfericas, sheet {int(nn)}: {sub}",
        maker or "Spanish Navy hydrographers", "1799 (compilation)",
        "https://www.loc.gov/item/2012593219/", LOC, caption)

# ── C-A 52 diseños (added 2026-07-15) ──
add("ca52-plano-pueblo-san-jose-suertes-1782.jpg", "spanmex",
    "Plano of the Pueblo San Jose suertes", "Jose Moraga; Savage transcript copy", "1782 (copy ca. 1870s)",
    "https://archive.org/details/bancarchca_81_14/page/n238", "The Bancroft Library, University of California, Berkeley, via Internet Archive. BANC MSS C-A 52.",
    "Plan of the farm plots distributed to the settlers of the Pueblo San Jose, dated April 23, 1782, over Jose Moraga's signature. Each suerte in the grid carries a settler's name, with the Rio de Guadalupe and the acequia drawn alongside. The original burned in 1906; this is the plan as copied into the Savage transcripts, the only surviving version.")
add("ca52-plano-pueblo-los-angeles-1786.jpg", "spanmex",
    "Plano of the Pueblo de la Reina de los Angeles", "Savage transcript copy of the 1786 original", "1786 (copy ca. 1870s)",
    "https://archive.org/details/bancarchca_81_14/page/n302", "The Bancroft Library, University of California, Berkeley, via Internet Archive. BANC MSS C-A 52.",
    "The earliest town plan of Los Angeles, from the pueblo's 1786 possession papers. It shows the plaza with the church marked by a cross, the grid of house lots and farm plots, the Rio de Porciuncula, and the Acequia Madre. The original burned in 1906; this is the Savage transcript copy. It pairs with the Ord and Hutton survey of 1849 in the Conquest section as the beginning and end of the pueblo era.")

# ── Spanish and Mexican California ──
add("sanson-1657-audience-guadalajara-california-island.jpg", "spanmex",
    "Audience de Guadalajara, Nouveau Mexique, Californie", "Nicolas Sanson", "1657 (catalog date)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~295189~90066276", RUM,
    "A classic map showing California as an island, the error that dominated European cartography for a century. Included here as the starting point the later surveys corrected. The date comes from the catalog record.")
add("costanso-1770-carta-reducida-oceano-asiatico.jpg", "spanmex",
    "Carta reducida del Oceano Asiatico o Mar del Sur", "Miguel Costanso", "1770",
    "https://jcb.lunaimaging.com/luna/servlet/detail/JCBMAPS~1~1~3868~101989", JCB,
    "Costanso's synthesis map from the Portola expedition, dated Mexico, October 1770. This is the cartographic base of the colonization of Alta California, drawn by the engineer who marched with the founding expedition.", better_copy=True)
add("canizares-1781-plano-puerto-san-francisco.jpg", "spanmex",
    "Plano del Puerto de San Francisco", "Jose de Canizares", "1781 engraving of 1775 to 1776 surveys",
    "https://commons.wikimedia.org/wiki/File:1781_Ca%C3%B1izares_Map_of_San_Francisco_Bay.pdf", COM,
    "The first map of San Francisco Bay, from the surveys Canizares made in 1775 and 1776. This is the engraved state published in 1781. The manuscript original is at the Bancroft Library.")
add("sutil-mexicana-1802-carta-esferica.jpg", "spanmex",
    "Carta esferica de los reconocimientos hechos en la costa N.O.", "Sutil y Mexicana atlas", "1802 (catalog date)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~715~80043", RUM,
    "From the published atlas of the Sutil and Mexicana voyage, Madrid 1802. This was Spain's public answer to Vancouver's atlas, its case that Spanish surveys had covered the coast first. Edition details come from the catalog record.")
add("sutil-mexicana-1802-carta-esferica-sheet2.jpg", "spanmex",
    "Carta esferica de los reconocimientos, second sheet", "Sutil y Mexicana atlas", "1802 (catalog date)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~714~80042", RUM,
    "The companion sheet of the same published survey chart.")
add("carta-esferica-1823-alta-baja-californias-sonora.jpg", "spanmex",
    "Carta esferica de los territorios de la alta y baja Californias y estado de Sonora", None, "1823",
    "https://www.loc.gov/item/99446199/", LOC,
    "The young Mexican republic's frame for the Californias and Sonora, made in the year after independence. Hornbeck reproduces this same sheet as the standard image of Mexican California's administrative geography.")
add("plano-puerto-san-francisco-1825.jpg", "spanmex",
    "Plano del Puerto de San Francisco", "engraved in Mexico", "1825",
    "https://purl.stanford.edu/jy754rc8040", STA,
    "The Mexican republic's own chart of San Francisco Bay, engraved in Mexico in 1825. The outline descends from Canizares. The key lists the mission, Isla de Alcatraces, and the Farallones. The imprint was read from the sheet.")

# ── Russian California / Duflot ──
add("duflot-1844-fort-ross-bodega-mouillage.jpg", "russian",
    "Carte detaillee du mouillage du Fort Ross et du Port de la Bodega ou Romanzoff", "Duflot de Mofras", "1844",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1798~210011", RUM,
    "The most detailed period map of the Russian anchorages. It shows Fort Ross and Bodega harbor under their Russian name Romanzoff, drawn in the last years of the colony. Scanned at full resolution, so the soundings and shore details are all legible.")
add("duflot-1844-carte-generale-cote-pacifique.jpg", "russian",
    "Carte de la cote de l'Amerique sur l'Ocean Pacifique Septentrional", "Duflot de Mofras", "1844",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1788~210001", RUM,
    "Duflot's general map of the Pacific coast, covering Oregon, the Californias, and the Gulf of California. Plate details come from the catalog record.")
add("duflot-1844-port-san-francisco.jpg", "russian",
    "Port de San Francisco dans la Haute Californie", "Duflot de Mofras", "1844",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1797~210010", RUM,
    "Duflot's plan of San Francisco Bay on the eve of the American conquest.")
add("duflot-1844-monterey-trinidad.jpg", "russian",
    "Plan du Port et de la Baie de Monte-Rey", "Duflot de Mofras", "1844",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1796~210009", RUM,
    "Duflot's plan of Monterey, the capital's harbor, with the Bay of Trinidad as a companion.")
add("duflot-1844-rio-colombia.jpg", "russian",
    "Carte du Rio Colombia", "Duflot de Mofras", "1844",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1799~210012", RUM,
    "The Columbia River up to Fort Vancouver, the Hudson's Bay Company anchor of the coast Duflot was sizing up for France.")
add("duflot-1844-rio-colorado-san-diego.jpg", "russian",
    "Plan de l'embouchure du Rio Colorado, with the Port of San Diego", "Duflot de Mofras", "1844",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1794~210007", RUM,
    "The mouth of the Colorado and the port of San Diego on one plate, the southern edges of the territory.")
add("duflot-1844-quadra-nutka.jpg", "russian",
    "Port de Quadra ou de la Decouverte, with the Plan du Port de Nutka", "Duflot de Mofras", "1844",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1800~210013", RUM,
    "Two harbor plans on one plate, Port Quadra or Discovery and Nootka with the Cala de los Amigos. These are the Vancouver Island ports where Spain and Britain fought out the Nootka crisis of 1789 to 1794, redrawn by Duflot fifty years later.")
add("duflot-1844-mouillage-san-pedro-santa-barbara.jpg", "russian",
    "Mouillage de San Pedro, with the Mouillage de la Mission de Santa Barbara", "Duflot de Mofras", "1844",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1795~210008", RUM,
    "Duflot's anchorage plans for San Pedro and the Santa Barbara roadstead, numbers 12 and 13 of the atlas. These open roadsteads were the working ports of the southern hide trade.")
add("duflot-1844-plan-geometrique-mission-san-luis-rey.jpg", "russian",
    "Plan geometrique de la Mission de St. Louis Roi de France", "Duflot de Mofras", "1844",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1803~210020", RUM,
    "The only measured ground plan of a California mission complex in Duflot's atlas, drawn at San Luis Rey in the middle of secularization. A rare architectural record of what was being dismantled.")

# ── Foreign surveys ──
add("vancouver-1798-nw-coast.jpg", "foreign",
    "A Chart Shewing Part of the Coast of N.W. America (New Albion sheet)", "George Vancouver, prepared under Lt. Joseph Baker", "1798",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~2275~200018", RUM,
    "Vancouver's California sheet, lettered Part of the Coast of New Albion, with an inset of Trinidad Bay. The British claim language is on the map itself. New Albion was Drake's name, and using it on a 1798 chart of Spanish California was a statement.")
add("vancouver-1798-coast-30N-38-30N-california.jpg", "foreign",
    "Chart of the Coast of N.W. America, 30 degrees to 38 degrees 30 minutes north", "George Vancouver", "1798",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~2280~200023", RUM,
    "The southern companion sheet, running from San Diego past the Golden Gate to the latitude of Bodega. The best foreign survey of the Alta California coast at the century's end.")
add("vancouver-1798-general-chart-29N-58N.jpg", "foreign",
    "General chart of the coast, 29 degrees 54 minutes to 58 degrees 52 minutes north", "George Vancouver", "1798",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~2286~200029", RUM,
    "The general chart of Vancouver's whole survey, Baja California to Alaska.")
add("la-perouse-cote-no-amerique.jpg", "foreign",
    "Cote N.O. de l'Amerique (general sheet)", "La Perouse expedition atlas", "published 1797 (edition unverified)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~20398~550016", RUM,
    "The general northwest coast sheet from the atlas of the La Perouse expedition, the French scientific voyage that visited Monterey in 1786.")
add("la-perouse-monterey.jpg", "foreign",
    "Baie de Monterey", "La Perouse expedition atlas", "published 1797 (edition unverified)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~20337~550034", RUM,
    "The French plan of Monterey Bay from the 1786 visit, the first foreign scientific expedition received in Spanish California.")
add("beechey-1833-san-francisco-harbour.jpg", "foreign",
    "The Harbour of San Francisco, Nueva California", "F. W. Beechey", "published 1833 (catalog date)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~291131~90062697", RUM,
    "The Royal Navy survey of San Francisco Bay from Beechey's 1826 to 1828 voyage. This stayed the standard chart of the bay into the 1840s, which says something about who was actually mapping Mexican California.")
add("wilkes-1841-oregon-territory.jpg", "foreign",
    "Map of the Oregon Territory", "Charles Wilkes, US Exploring Expedition", "1841",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~24331~890027", RUM,
    "The US Exploring Expedition's map of the Oregon country, which reaches down into the San Francisco Bay and Sacramento country the squadron surveyed. It fed American ambitions for both Oregon and California.")
add("wilkes-atlas-entrance-san-francisco.jpg", "foreign",
    "Entrance, San Francisco", "Wilkes expedition atlas", "circa 1841",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~24348~890039", RUM,
    "The American naval survey of the Golden Gate from the Wilkes expedition.")
add("wilkes-atlas-carquinez-vallejo-bay.jpg", "foreign",
    "Carquines Straits, Vallejo Bay, and other anchorages", "Wilkes expedition atlas", "circa 1841",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~24359~890050", RUM,
    "Wilkes's chart of the Carquinez Strait and the northern arms of the bay, ground the interactive maps here cross constantly.")

# ── Claims and boundary maps ──
add("bowen-north-america-composite.jpg", "claims",
    "An Accurate Map of North America", "Emanuel Bowen and John Gibson", "1755 to 1770s (edition unverified)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1901~120008", RUM,
    "The standard British mid eighteenth century map of the continent, carrying New Albion on the Pacific coast. The Drake claim, kept alive in print for two hundred years.")
add("arrowsmith-new-discoveries-north-america.jpg", "claims",
    "A Map Exhibiting All the New Discoveries in the Interior Parts of North America", "Aaron Arrowsmith", "1814 state (first published 1795)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~910~50002", RUM,
    "London's running state of knowledge map of the west and the northwest coast, the Hudson's Bay Company world. This copy is the 1814 state, the plate of 1795 carried forward with additions to 1811 and 1814, the issue that first incorporated the Lewis and Clark discoveries (Stevens and Tree 48; Wheat 313).")
add("lewis-1804-louisiana.jpg", "claims",
    "Louisiana", "Samuel Lewis", "1804 (catalog date)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~31655~1150131", RUM,
    "The purchase era map of the Louisiana territory, from the Arrowsmith and Lewis atlas. What the United States thought it had just bought.")
add("humboldt-carte-generale-nouvelle-espagne.jpg", "claims",
    "Carte generale du Royaume de la Nouvelle Espagne", "Alexander von Humboldt", "1811 atlas (plate engraved 1809)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1866~170004", RUM,
    "Humboldt's general map of New Spain, the most authoritative published picture of Mexico's geography before independence. Every claims map of the next generation argued with this one. This is the northern sheet of the Carte generale, drawn at Mexico in 1804 and engraved in 1809, from the first French edition of Humboldt's atlas, 1811 (Wheat 272 to 275).")
add("melish-1816-united-states.jpg", "claims",
    "Map of the United States with the Contiguous British and Spanish Possessions", "John Melish", "1822 second state (first issued 1816)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~281825~90054769", RUM,
    "American map of the continent, the first to color a United States claim running unbroken to the Pacific. The coloring was read from this copy. This is the second state of the 1822 edition, the improved to 1822 issue and the last Melish published before his death in 1823, of a map he first issued in 1816 (Martin and Ristow 24; Streeter 3812). The 42 degree line here anticipates the Adams Onis treaty boundary of 1819.")
add("robinson-1819-mexico-louisiana-missouri.jpg", "claims",
    "A Map of Mexico, Louisiana, and the Missouri Territory", "John H. Robinson", "1819",
    "https://www.loc.gov/item/2004631496/", LOC,
    "The maximal American cartographic claim of the treaty moment, published in Philadelphia in 1819. Robinson drew the American case at its most aggressive just as the boundary was being negotiated.")
add("tanner-1847-map-united-states-of-mexico.jpg", "claims",
    "Map of the United States of Mexico", "H. S. Tanner", "1847 (Fourth Edition)",
    "https://purl.stanford.edu/nd391yp3930", STA,
    "The Fourth Edition of Tanner's map of the Mexican republic, Philadelphia 1847, the most influential general map of the Mexican American War and the first to carry Fremont's discoveries. This edition is distinguished by its added inset of the harbor of Vera Cruz (Streeter 3825, Wheat 695). An earlier Tanner issue was the source, through the White, Gallaher and White map of 1828, of the boundary that Disturnell's map later carried into the Treaty of Guadalupe Hidalgo.")
add("disturnell-1847-mapa-estados-unidos-mejico.jpg", "claims",
    "Mapa de los Estados Unidos de Mejico", "J. Disturnell", "1847 (seventh edition, the Treaty Map)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~228~20030", RUM,
    "The Disturnell map, the family of maps referenced by the Treaty of Guadalupe Hidalgo. Disturnell issued several editions in 1847 with differing boundaries. This copy is catalogued as the seventh edition, the one the Rumsey and Streeter records identify as the Treaty Map consulted in the negotiations of February 1848, distinguished by having only two insets in the Gulf of Mexico where later issues have four (Streeter 255, Wheat 540).")
add("mitchell-1846-texas-oregon-california.jpg", "claims",
    "A New Map of Texas, Oregon and California", "S. A. Mitchell", "1846 (first issue)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~238~20003", RUM,
    "The annexation year synthesis, sold to emigrants and expansionists alike. Texas, Oregon, and California as one connected American question. This is the first issue of 1846, entered for copyright in 1845, before the later editions of 1849, 1851, and 1852 (Wheat 520, Streeter 2511).")
add("wyld-mexico-british-possessions-composite.jpg", "claims",
    "Mexico, the British Possessions in North America and the United States", "James Wyld", "1846",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~258993~5522262", RUM,
    "London's view of the continental partition in the Oregon question era, on two sheets joined. Published by James Wyld in London in 1846, a reduced reissue of his 1824 Map of North America, updated with the Oregon Trail, Fremont's South Pass, and Forts Hall and Boise.")

# ── Conquest and Gold Rush ──
add("emory-1847-military-reconnaissance.jpg", "conquest",
    "Military Reconnaissance of the Arkansas, Rio del Norte and Rio Gila", "W. H. Emory", "1847 (catalog date)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1810~180024", RUM,
    "Emory's route map of the Army of the West's march to California, the conquest's own cartographic record.")
add("fremont-preuss-1848-oregon-upper-california.jpg", "conquest",
    "Map of Oregon and Upper California", "John C. Fremont and Charles Preuss", "1848 (catalog date)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~1820~170046", RUM,
    "The first US government map of the newly conquered territory, drawn by Preuss from Fremont's surveys.")
add("oregon-upper-california-new-mexico-1849.jpg", "conquest",
    "Oregon, Upper California and New Mexico", "S. Augustus Mitchell", "1849",
    "https://purl.stanford.edu/wk370rr6021", STA,
    "The ceded conquest as first mapped for the American public, published in Philadelphia in 1849. Upper or New California still fills the whole interior basin. The maker and date were read from the sheet.", better_copy=True)
add("ord-hutton-1849-plan-la-LAPL-period.jpg", "conquest",
    "Plan de la Ciudad de Los Angeles", "E. O. C. Ord and William Hutton", "1849",
    "https://tessa2.lapl.org/digital/collection/maps/id/42/", LAPL,
    "The first survey of Los Angeles, August 1849. This is the hinge document between rancho land tenure and American property law, the sheet on which the pueblo's lands became lots. This scan is of a period copy held by the Los Angeles Public Library.")
add("uscs-city-of-san-francisco-and-vicinity.jpg", "conquest",
    "City of San Francisco and its Vicinity", "US Coast Survey", "1850s (year on sheet unchecked)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~2212~180003", RUM,
    "The federal survey of the instant city.")
add("uscs-bodega-bay-california.jpg", "conquest",
    "Bodega Bay, California", "US Coast Survey", "1850s or 1860s (year unchecked)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~220766~5505165", RUM,
    "The American chart of Bodega Bay. The port the Spanish discovered in 1775 and never held, surveyed at last by the power that ended up with it.")
add("gibbes-1852-new-map-of-california.jpg", "conquest",
    "New Map of California", "Charles Drayton Gibbes", "1852 (catalog date)",
    "https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~220139~5504923", RUM,
    "Gibbes's Gold Rush synthesis of the new state, including the Southern Mines country.")

# ---- attach dims + write ----
items = []
for it in I:
    p = os.path.join(IMG, it["file"])
    if not os.path.exists(p):
        raise SystemExit("missing derivative: " + it["file"])
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", p],
                         capture_output=True, text=True).stdout
    w = h = 0
    for line in out.split("\n"):
        if "pixelWidth" in line: w = int(line.split()[-1])
        if "pixelHeight" in line: h = int(line.split()[-1])
    it["w"], it["h"] = w, h
    it["id"] = os.path.splitext(it["file"])[0]
    items.append(it)

files_on_disk = {f for f in os.listdir(IMG) if f.endswith(".jpg")}
listed = {it["file"] for it in items}
print("on disk not listed:", sorted(files_on_disk - listed))
print("listed not on disk:", sorted(listed - files_on_disk))

data = {
    "updated": "2026-07-14",
    "note": ("Captions are working placeholders written from the collection catalog and the holding "
             "institutions' records. Dates marked as catalog dates or unverified have not been checked "
             "against the sheet imprint."),
    "wanted": [
        "Narvaez, Plano del Territorio de la Alta California 1830 (digitized on Calisphere, blocked to scripts, needs a manual browser save)",
        "1839 Carta esferica de la costa de la Alta California (CSUMB Hornbeck, gated, manual save)",
        "Higher resolution Costanso 1770 (1331 px is the John Carter Brown Library's full size; a larger scan would need another holder)",
        "Higher resolution Mitchell 1849 Oregon, Upper California and New Mexico (1200 px is Stanford's full size for this item)",
        "Kotzebue and Choris, chart of San Francisco Bay from the Rurik voyage, 1816 (not on Rumsey; check LOC and Commons)",
        "Tanner, Map of the United States of Mexico, earlier edition (copy in collection has an unverified edition and is held back)"
    ],
    "groups": GROUPS,
    "items": items
}
out_path = os.path.join(REPO, "gallery", "gallery-data.json")
json.dump(data, open(out_path, "w"), indent=1, ensure_ascii=False)
print("items:", len(items), "->", out_path)
