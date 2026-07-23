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

# ---- curatorial headnotes (the "why this chart" + "what to look for" layer) ----
# Additive: attached to matching items by id; the working captions above are untouched.
# Each is verified from the chart's cartobibliography. Extend this dict to curate more maps.
HEADNOTES = {
    "sutil-mexicana-1802-carta-esferica": {
        "headnote": "The California coast as Spain itself charted it, from the 1792 survey of the "
                    "schooners Sutil and Mexicana and published in the official Relacion of 1802. It is "
                    "the Spanish-hand chart contemporary with the founding decades, and the same "
                    "hydrographic source the Bodega project reads for the coast's legal geography: the "
                    "empire mapping the frontier it claimed but rarely visited.",
        "look_for": "the still-tentative rendering of the northern anchorages Spain claimed but seldom "
                    "entered, Bodega and the coast above San Francisco Bay.",
    },
    "vancouver-1798-nw-coast": {
        "headnote": "The outside power charting a coast Spain claimed. Vancouver surveyed this shore in "
                    "1792 to 1794, during the Nootka-crisis decade when the imperial door was forced "
                    "open, and his calls at California ports are themselves events in the record. Drawn "
                    "by the visitor rather than the sovereign, the British survey is often the more "
                    "accurate one.",
        "look_for": "how the British survey of New Albion compares with the Spanish Sutil chart of the "
                    "same coast; the rival's map is frequently the better.",
    },
    "duflot-1844-carte-generale-cote-pacifique": {
        "headnote": "The late-Mexican coast on a single detailed sheet, from a French diplomatic and "
                    "scientific survey made on the eve of the American conquest. Duflot de Mofras "
                    "recorded every anchorage from Sitka to San Blas in the last years of Mexican rule, "
                    "the natural ground for the hide-and-tallow decades and a companion to the Fort Ross "
                    "and Bodega roadstead plan in the same atlas.",
        "look_for": "the named coastal establishments and soundings that show how thoroughly foreign "
                    "navies knew a coast Mexico could barely garrison.",
    },
    "beechey-1833-san-francisco-harbour": {
        "headnote": "The definitive chart of San Francisco Bay, surveyed by Beechey's HMS Blossom in 1826 "
                    "to 1827, the decade the bay filled with the hide-trade fleet. The Blossom's own call "
                    "is part of the same maritime record; the chart is the geography of the anchorage "
                    "where the Boston droghers rode off Yerba Buena.",
        "look_for": "the anchorage grounds off Yerba Buena, the working geography of the licensed foreign "
                    "trade.",
    },
    "duflot-1844-fort-ross-bodega-mouillage": {
        "headnote": "The roadstead the Bodega argument turns on, charted by Duflot de Mofras in 1844 as "
                    "the Russians were withdrawing: the anchorage Spain ordered occupied in 1793 and "
                    "never held. It shows in detail how shallow and exposed the port actually was.",
        "look_for": "how open and shallow the Bodega anchorage is, the geographic objection the Bodega "
                    "study answers.",
    },
    "canizares-1781-plano-puerto-san-francisco": {
        "headnote": "Jose de Canizares was the pilot who first sounded San Francisco Bay aboard Ayala's "
                    "San Carlos in 1775; this 1781 plano is his worked-up chart of that survey, the "
                    "earliest Spanish rendering of the harbour every ship of the founding decades came to "
                    "know.",
        "look_for": "the first systematic soundings of a bay no European had charted a decade earlier.",
    },
    "loc-bq05-plano-puerto-capitan-bodega-1775": {
        "headnote": "The founding map of the Bodega claim. Bodega y Quadra and his pilot Francisco "
                    "Mourelle drew it in 1775, the year the Sonora entered and named the bay, and it is "
                    "the document the whole Open Door argument rests on: Spain discovered and charted the "
                    "anchorage, then left it open. The Library of Congress acquired this manuscript only "
                    "in 2024.",
        "look_for": "the keyed points and the soundings at the entrance, the survey Spain made of a port "
                    "it would claim for seventy years and never hold.",
    },
    "loc-bq07-bahia-asumpcion-entrada-ezeta-1775": {
        "headnote": "The Spanish discovery chart of the Columbia River mouth. Bruno de Hezeta sighted and "
                    "sketched the entrance in August 1775, seventeen years before the American Robert Gray "
                    "gave the river its lasting name. It is the northern reach of the same 1775 voyage "
                    "that charted Bodega.",
        "look_for": "the bay Hezeta marked at the river's mouth, the basis of a Spanish claim to a coast "
                    "the United States would later argue was its own by discovery.",
    },
    "loc-bq13-plano-san-diego-1782-pantoja": {
        "headnote": "Pantoja's 1782 chart of San Diego harbor, the base survey behind most later Spanish "
                    "renderings of the southern anchorage. San Diego was the province's first presidio and "
                    "its southern gate; this is the port as the Spanish navy fixed it.",
        "look_for": "the soundings and shoreline that later charts, Spanish and American alike, would "
                    "copy.",
    },
    "duhaut-cilly-fort-ross-1828": {
        "headnote": "The classic eyewitness image of Fort Ross, drawn by the French trader Auguste "
                    "Duhaut-Cilly on his 1828 visit and published in his 1834 narrative. It shows the "
                    "blockhouses, chapel, and stockade on the terrace above the sea, the Russian colony at "
                    "its height on a coast Spain claimed but never held.",
        "look_for": "the finished stockade and bastions, the permanence of a settlement Mexico could not "
                    "dislodge.",
    },
    "duhaut-cilly-bodega-1828": {
        "headnote": "Duhaut-Cilly's eyewitness view of the Russian anchorage at Bodega in 1828, the "
                    "working harbor that supplied Fort Ross. This is the port Spain discovered in 1775 and "
                    "ordered occupied in 1793, shown in Russian use a half-century later.",
        "look_for": "how the Russians used an anchorage the Spanish had charted and then abandoned.",
    },
    "voznesensky-settlement-ross-1841": {
        "headnote": "Fort Ross in its last year, sketched in 1841 before the sale to Sutter, in a view "
                    "attributed to the Russian naturalist Voznesensky. The windmill and the village have "
                    "grown outside the stockade: the colony at its fullest, on the eve of withdrawal.",
        "look_for": "the settlement spread beyond the walls, the scale of what Russia gave up when it "
                    "sold.",
    },
    "la-perouse-monterey": {
        "headnote": "The French plan of Monterey Bay from La Perouse's 1786 call, the first foreign "
                    "scientific expedition to visit Spanish California. His hosts received him warmly, and "
                    "his published account carried the province and its missions into the European "
                    "Enlightenment's view.",
        "look_for": "the capital's roadstead as the first outside observers recorded it.",
    },
    "wilkes-atlas-entrance-san-francisco": {
        "headnote": "The American naval survey of the Golden Gate from the Wilkes expedition of 1841, five "
                    "years before the conquest. The United States was charting the entrance to San "
                    "Francisco Bay well before it took the bay.",
        "look_for": "the mouth of the harbor the US Navy would enter in 1846.",
    },
    "humboldt-carte-generale-nouvelle-espagne": {
        "headnote": "Humboldt's general map of New Spain, the most authoritative published picture of "
                    "Mexico's north for a generation. Drawn from the viceregal archives he was allowed to "
                    "read, it framed how Europe and the United States alike understood the far northwest, "
                    "Alta California included.",
        "look_for": "how the interior west is drawn, the shape later American mapmakers inherited from "
                    "Humboldt.",
    },
    "disturnell-1847-mapa-estados-unidos-mejico": {
        "headnote": "The Disturnell map, the family of maps named in the Treaty of Guadalupe Hidalgo that "
                    "ended the war and ceded California. Its errors in placing the Rio Grande and El Paso "
                    "seeded a boundary dispute the Gadsden Purchase later had to resolve.",
        "look_for": "the treaty line, drawn on a map whose mistakes became a diplomatic problem.",
    },
    "melish-1816-united-states": {
        "headnote": "The first American map to color a United States claim running unbroken to the "
                    "Pacific. Melish drew the nation as a transcontinental one three decades before it "
                    "was, and the forty-second parallel here anticipates the Adams-Onis line of 1819.",
        "look_for": "the band of US color reaching the Pacific, a claim made on paper long before it was "
                    "made on the ground.",
    },
    "fremont-preuss-1845-rocky-mountains-oregon-california": {
        "headnote": "The map that put California into the American imagination. Charles Preuss drew it "
                    "from Fremont's expeditions of the early 1840s, and it gave emigrants and "
                    "expansionists their first authoritative picture of the overland routes to a province "
                    "still Mexican.",
        "look_for": "the trails west, the cartography that helped bring the wagon trains and, behind them, "
                    "the conquest.",
    },
    "ord-hutton-1849-plan-la-LAPL-period": {
        "headnote": "The first survey of Los Angeles, made in August 1849, the hinge document between the "
                    "Mexican pueblo and the American city. Lieutenant Ord laid the grid that would govern "
                    "the town's growth over the old rancho landscape.",
        "look_for": "the new American survey grid set over the Spanish and Mexican town plan.",
    },
    "costanso-1770-carta-reducida-oceano-asiatico": {
        "headnote": "Costanso's synthesis map from the Portola expedition, dated Mexico, October 1770: the "
                    "cartographic record of the overland march that founded San Diego and Monterey and "
                    "first reached San Francisco Bay by land. This is Alta California entering the map as a "
                    "Spanish possession.",
        "look_for": "the coast as the Portola party fixed it, the province at the moment of its founding.",
    },
    "sanson-1657-audience-guadalajara-california-island": {
        "headnote": "California as an island, the error that ruled European maps for much of the "
                    "seventeenth and eighteenth centuries. Sanson's elegant 1657 sheet is the classic "
                    "statement of the mistake, a reminder of how little the powers that claimed this coast "
                    "actually knew of it.",
        "look_for": "the clean channel separating the island of California from the mainland, geography "
                    "that did not exist.",
    },
    "plano-puerto-san-francisco-1825": {
        "headnote": "The Mexican republic's own chart of San Francisco Bay, engraved in Mexico in 1825, "
                    "three years after independence. The outline still descends from Canizares' 1775 "
                    "survey: the new nation inherited the old empire's cartography of its far northwest.",
        "look_for": "the mission, Alcatraz, and the Farallones named on a chart the republic made of a "
                    "port it barely governed.",
    },
    # ---- 1775 expedition ----
    "loc-bq01-carta-reducida-bodega-mourelle-1775": {
        "headnote": "The large general chart of the 1775 voyage, the whole track of the expedition that discovered Bodega laid down on one sheet. This is the working master chart behind the individual port plans.",
        "look_for": "the continuous coastal track running north from Mexico, the reach of a single season's survey.",
    },
    "loc-bq04-carta-reducida-bodega-small-1775": {
        "headnote": "The pocket version of the 1775 general chart, the same voyage reduced to a sheet that could travel: Spain's coastal knowledge in portable form.",
        "look_for": "how much coast the survey claimed to fix in one season, compressed to a working scale.",
    },
    "loc-bq02-carta-reducida-hezeta-1775": {
        "headnote": "Hezeta's own general chart of the 1775 expedition. Hezeta commanded the voyage while Bodega y Quadra took the schooner Sonora farther north; this is the commander's summary of the whole.",
        "look_for": "the coast as the expedition's commander drew it, the counterpart to Bodega's own charts.",
    },
    "loc-bq03-carta-reducida-hezeta-small-1775": {
        "headnote": "The reduced version of Hezeta's general chart, the commander's survey of the 1775 coast in portable form.",
        "look_for": "the northern shore Spain was racing to fix before Russia and Britain reached it.",
    },
    "loc-bq06-plano-puerto-trinidad-1775": {
        "headnote": "The chart of Trinidad harbor, where the expedition raised a cross and took formal possession in June 1775. An act of sovereignty recorded in cartography.",
        "look_for": "the anchorage where Spain performed possession, the ritual that underwrote the paper claim.",
    },
    "loc-bq08-rada-bucareli-1775": {
        "headnote": "Hezeta's chart of an anchorage on the Washington coast, part of the 1775 push to fix the shore north of California before rival powers did.",
        "look_for": "the far-northern reach of a survey mounted to forestall Russia and Britain.",
    },
    "loc-bq09-puerto-bucareli-1775": {
        "headnote": "The port at 55 degrees north in southeast Alaska, the farthest major survey of the Sonora's push north in 1775 and the high-water mark of Spain's claim by discovery.",
        "look_for": "how far north the charting reached, a coast Spain could map but never settle.",
    },
    "loc-bq10-puerto-remedios-1775": {
        "headnote": "A chart near the northern limit of the 1775 voyage, the edge of what Spain surveyed on its boldest reach up the Pacific coast.",
        "look_for": "the northern frontier of the Spanish survey, ground it charted and abandoned.",
    },
    "loc-bq12-carta-reducida-1780-expediciones": {
        "headnote": "Bodega y Quadra's summary chart of both his northern voyages, 1775 and 1779, the ships named in the cartouche: one officer's decade of charting the coast Spain meant to hold against Russia.",
        "look_for": "the combined reach of two expeditions, the scope of the Spanish claim by survey.",
    },
    "loc-bq11-puerto-sidman-1792": {
        "headnote": "A Spanish chart of a port reconnoitered by Captain Baker of Vancouver's expedition, evidence of how quickly Spanish cartographers absorbed British survey work. The rival's discoveries copied into Spain's own records.",
        "look_for": "the borrowing itself, a Spanish sheet built on a British survey.",
    },
    "loc-bq14-carta-descubrimientos-costa-no-1850copy": {
        "headnote": "A circa-1850 manuscript copy of an early-1790s chart of the northwest-coast discoveries, dedicated to Viceroy Revilla Gigedo. Valuable for content, but a later copy rather than a period sheet.",
        "look_for": "the sweep of the discoveries the viceroy's surveys claimed, read with the caveat that this is a copy.",
    },
    # ---- 1799 Hydrographic Atlas ----
    "loc-cartas-esfericas-1799-sheet01": {
        "headnote": "The atlas's general chart, running the whole coast from Acapulco to Unalaska, drawn under Bodega y Quadra in 1792. The single sheet that frames the enterprise: Spain's claim to the Pacific edge of its empire on one page.",
        "look_for": "the full span of the coast Spain claimed, from Mexico to the Aleutians.",
    },
    "loc-cartas-esfericas-1799-sheet02": {
        "headnote": "Per the atlas contents list, the port of Acapulco, surveyed by Montes in 1796, the Pacific terminus of the Manila galleon and a naval base behind the northern enterprise. The sheet's own title has not yet been read.",
        "look_for": "the harbor that anchored Spain's Pacific, the far southern end of the coast the atlas charts.",
    },
    "loc-cartas-esfericas-1799-sheet03": {
        "headnote": "Per the atlas contents list, San Blas, surveyed by Camacho in 1779, the naval yard whose supply ships were the lifeline of Alta California. Every founding-era vessel in the record sailed from here.",
        "look_for": "the working port from which the settlement of California was supplied.",
    },
    "loc-cartas-esfericas-1799-sheet04": {
        "headnote": "Per the atlas contents list, the port of San Diego, the province's southern gate and the site of the first Spanish landfall of 1769. The sheet's own title has not yet been read.",
        "look_for": "the harbor where Alta California's colonization began.",
    },
    "loc-cartas-esfericas-1799-sheet05": {
        "headnote": "Per the atlas contents list, the Santa Barbara and Purisima ensenadas, surveyed by Pantoja and Tovar in 1782, the open roadsteads of the central coast.",
        "look_for": "the exposed anchorages that served the missions of the Channel.",
    },
    "loc-cartas-esfericas-1799-sheet06": {
        "headnote": "Per the atlas contents list, the port of Monterey, the capital's roadstead and the busiest anchorage of Spanish and Mexican California. The sheet's own title has not yet been read.",
        "look_for": "the harbor that served the seat of government for the whole period.",
    },
    "loc-cartas-esfericas-1799-sheet07": {
        "headnote": "Per the atlas contents list, the port of San Francisco, credited to Camacho in 1779, the great bay whose survey opened the coast's finest harbor to the founding decades.",
        "look_for": "the bay every founding-era ship came to know, as the navy fixed it.",
    },
    "loc-cartas-esfericas-1799-sheet08-bodega-1793": {
        "headnote": "Bodega Bay as resurveyed in 1793, the year of the failed Spanish attempt to occupy it; the title records discovery in 1775 and reconnaissance in 1793. The cartographic heart of the Open Door argument: the port charted, claimed, and left open.",
        "look_for": "the 1793 resurvey of the anchorage Spain twice examined and never held.",
    },
    "loc-cartas-esfericas-1799-sheet09": {
        "headnote": "Per the atlas contents list, Puerto de la Trinidad, surveyed by Hezeta in 1775, the harbor where the expedition took formal possession that June, folded now into the navy's master atlas.",
        "look_for": "the northern possession-site preserved in the compiled record.",
    },
    "loc-cartas-esfericas-1799-sheet10": {
        "headnote": "Per the atlas contents list, the entrance Hezeta found in 1775 and reexamined in 1793, the Columbia mouth as Spanish surveys left it before Gray and Vancouver gave it other names.",
        "look_for": "the river-mouth Spain claimed by prior discovery.",
    },
    "loc-cartas-esfericas-1799-sheet11": {
        "headnote": "Per the atlas contents list, a northwest-coast port surveyed by Martinez y Zayas in 1793, part of Spain's last push to chart the shore in the Nootka years. The sheet's own title has not yet been read.",
        "look_for": "the late Spanish surveys of a coast already contested with Britain.",
    },
    "loc-cartas-esfericas-1799-sheet12": {
        "headnote": "Per the atlas contents list, the interior channels between 48 and 50 degrees with five port insets, from the 1791 surveys, the intricate island coast of the Pacific Northwest.",
        "look_for": "the maze of channels Spanish pilots threaded in the Nootka decade.",
    },
    "loc-cartas-esfericas-1799-sheet13": {
        "headnote": "Per the atlas contents list, the Strait of Juan de Fuca, surveyed 1793, the passage whose exploration fed both the myth of a northwest route and the reality of the Nootka dispute.",
        "look_for": "the strait at the center of the Spanish-British contest for the coast.",
    },
    "loc-cartas-esfericas-1799-sheet14": {
        "headnote": "Per the atlas contents list, Nitinat on the Vancouver Island coast, surveyed by Carrasco, one of the fine-grained Spanish surveys of the contested northern shore. The sheet's own title has not yet been read.",
        "look_for": "the detail of a Spanish survey on a coast Spain would soon cede.",
    },
    "loc-cartas-esfericas-1799-sheet15": {
        "headnote": "Per the atlas contents list, Clayoquot on the Vancouver Island coast, part of the Spanish charting of the Nootka region. The sheet's own title has not yet been read.",
        "look_for": "a Spanish plan of the sounds where Spain and Britain nearly went to war.",
    },
    "loc-cartas-esfericas-1799-sheet16": {
        "headnote": "Per the atlas contents list, the coast running down to San Francisco, surveyed 1793, the stretch that ties the northern surveys back to Alta California.",
        "look_for": "the link between the far-northern charts and the California coast.",
    },
    "loc-cartas-esfericas-1799-sheet17": {
        "headnote": "Per the atlas contents list, Nootka, the harbor at the center of the 1789 to 1794 crisis between Spain and Britain, the flashpoint of the whole northern enterprise. The sheet's own title has not yet been read.",
        "look_for": "the port whose seizure nearly brought two empires to war.",
    },
    "loc-cartas-esfericas-1799-sheet18": {
        "headnote": "Per the atlas contents list, San Lorenzo de Nuca, surveyed by the Malaspina expedition in 1791, the great Spanish scientific voyage's contribution to the atlas.",
        "look_for": "a plan drawn from Malaspina's Enlightenment survey of the Pacific.",
    },
    "loc-cartas-esfericas-1799-sheet19": {
        "headnote": "Per the atlas contents list this sheet is Puerto Gaston, one of the port surveys the Spanish Navy gathered into its 1799 atlas of the Pacific coast. The sheet's own title has not yet been read.",
        "look_for": "the fine harbor detail that made each of these surveys a working sailing document.",
    },
    "loc-cartas-esfericas-1799-sheet20": {
        "headnote": "Per the atlas contents list this sheet is Puerto Floridablanca, one of the port surveys compiled into the Spanish Navy's 1799 atlas. The sheet's own title has not yet been read.",
        "look_for": "the close survey of a single anchorage within the larger imperial atlas.",
    },
    "loc-cartas-esfericas-1799-sheet21": {
        "headnote": "Per the atlas contents list this sheet is Puerto Bazan, another of the port surveys gathered into the 1799 atlas. The sheet's own title has not yet been read.",
        "look_for": "the working detail of one harbor among the atlas's many.",
    },
    "loc-cartas-esfericas-1799-sheet22": {
        "headnote": "Per the atlas contents list this sheet is Puerto de los Dolores, one of the anchorages fixed on the northern voyages and compiled into the 1799 atlas. The sheet's own title has not yet been read.",
        "look_for": "a single anchorage surveyed and filed within Spain's master record of the coast.",
    },
    "loc-cartas-esfericas-1799-sheet23": {
        "headnote": "Per the atlas contents list, Puerto de Bucareli in the far north, the harbor that carries the name of the viceroy who ordered the northern voyages. It marks near the top of Spain's reach up the coast.",
        "look_for": "the far-north harbor named for the viceroy behind the whole enterprise.",
    },
    "loc-cartas-esfericas-1799-sheet24": {
        "headnote": "Per the atlas contents list, Puerto de la Regla, surveyed in 1779, one of the ports added on Bodega's second northern voyage. The sheet's own title has not yet been read.",
        "look_for": "the 1779 surveys that extended the reach of 1775.",
    },
    "loc-cartas-esfericas-1799-sheet25": {
        "headnote": "Per the atlas contents list, Puerto de Santiago, surveyed in 1779, another anchorage from the second northern expedition. The sheet's own title has not yet been read.",
        "look_for": "the ports Spain added on its return voyage north.",
    },
    # ---- Spanish and Mexican California ----
    "ca52-plano-pueblo-san-jose-suertes-1782": {
        "headnote": "The plan of the farm plots handed to the first settlers of Pueblo San Jose in 1782, each suerte carrying a settler's name over Jose Moraga's signature: a rare cadastral record of how a Spanish civil town was actually laid out. The original burned in 1906, and this Savage transcript is the only surviving version.",
        "look_for": "the named plots along the Guadalupe and the acequia, the anatomy of a founding land grant.",
    },
    "ca52-plano-pueblo-los-angeles-1786": {
        "headnote": "The earliest town plan of Los Angeles, from the pueblo's 1786 possession papers: plaza, church, house lots, and the Acequia Madre. With Ord's 1849 survey in the Conquest group it brackets the whole pueblo era. The original burned in 1906; this is the Savage transcript.",
        "look_for": "the plaza and the water-ditch that organized the town, the Spanish city before the American grid.",
    },
    "sutil-mexicana-1802-carta-esferica-sheet2": {
        "headnote": "The companion sheet of the published Sutil and Mexicana survey chart, extending along the coast Spain's official answer to Vancouver's atlas.",
        "look_for": "the continuation of the coast on Spain's public 1802 chart.",
    },
    "carta-esferica-1823-alta-baja-californias-sonora": {
        "headnote": "The young Mexican republic's frame for the Californias and Sonora, made the year after independence and still the standard image of Mexican California's administrative geography: the new nation drawing the far northwest it had just inherited.",
        "look_for": "how the republic bounded and divided the province it could barely reach.",
    },
    # ---- Russian California and Duflot ----
    "duflot-1844-port-san-francisco": {
        "headnote": "Duflot's plan of San Francisco Bay on the eve of the American conquest, a French diplomat's look at the harbor everyone knew would decide the coast.",
        "look_for": "the bay a French agent charted while sizing up California's future.",
    },
    "duflot-1844-monterey-trinidad": {
        "headnote": "Duflot's plan of Monterey, the capital's harbor, paired with Trinidad: the French atlas's record of the seat of Mexican California just before it fell.",
        "look_for": "the capital's roadstead in its last Mexican years.",
    },
    "duflot-1844-rio-colombia": {
        "headnote": "The Columbia up to Fort Vancouver, the Hudson's Bay Company anchor of a coast Duflot was quietly assessing for France: the imperial competition behind a scientific atlas.",
        "look_for": "the British fur-trade capital a French agent thought worth charting.",
    },
    "duflot-1844-rio-colorado-san-diego": {
        "headnote": "The mouth of the Colorado and the port of San Diego on one plate, the southern edges of the territory Duflot surveyed.",
        "look_for": "the desert river and the southern harbor that bounded Mexican California.",
    },
    "duflot-1844-quadra-nutka": {
        "headnote": "Two harbor plans on one plate, Port Quadra and Nootka, the Vancouver Island ports where Spain and Britain fought out the Nootka crisis of 1789 to 1794, redrawn by Duflot fifty years later. The old imperial flashpoint remembered in a later atlas.",
        "look_for": "the harbors that nearly caused an Anglo-Spanish war, mapped in hindsight.",
    },
    "duflot-1844-mouillage-san-pedro-santa-barbara": {
        "headnote": "Duflot's anchorage plans for San Pedro and the Santa Barbara roadstead, the open working ports of the southern hide trade.",
        "look_for": "the exposed roadsteads where the hide droghers loaded, the ports of the pastoral economy.",
    },
    "duflot-1844-plan-geometrique-mission-san-luis-rey": {
        "headnote": "The only measured ground plan of a California mission in Duflot's atlas, drawn at San Luis Rey in mid-secularization: a rare architectural record of what was being dismantled.",
        "look_for": "the plan of a mission complex at the moment the system was being taken apart.",
    },
    "voznesensky-ross-1841-variation": {
        "headnote": "A second 1841 view of Fort Ross, attributed to Voznesensky, the colony in its final year before the sale to Sutter.",
        "look_for": "the settlement on the eve of Russia's withdrawal, in a second eyewitness hand.",
    },
    "voznesensky-chernykh-ranch-1841": {
        "headnote": "The Russian farm inland from Ross, sketched in the colony's last year: the agricultural spread beyond the stockade that Vallejo's 1833 reconnaissance had been tracking, the reach of Russian settlement the Mexican north feared.",
        "look_for": "the farming Russia pushed inland, the expansion that alarmed Mexican California.",
    },
    # ---- Foreign Surveys ----
    "vancouver-1798-coast-30N-38-30N-california": {
        "headnote": "Vancouver's southern sheet, San Diego past the Golden Gate to the latitude of Bodega, the best foreign survey of the Alta California coast at the century's end. The visitor charting the province better than its sovereign had.",
        "look_for": "the California coast fixed by the British survey, more accurate than Spain's own.",
    },
    "vancouver-1798-general-chart-29N-58N": {
        "headnote": "The general chart of Vancouver's whole survey, Baja California to Alaska, the British master map of the coast the Nootka crisis had just contested.",
        "look_for": "the full sweep of the British survey that put Spain's claims to the test.",
    },
    "la-perouse-cote-no-amerique": {
        "headnote": "The general northwest-coast sheet from the atlas of La Perouse's expedition, the French scientific voyage that called at Monterey in 1786, the first foreign expedition to the province.",
        "look_for": "the coast as the first foreign scientific voyage recorded it.",
    },
    "wilkes-1841-oregon-territory": {
        "headnote": "The US Exploring Expedition's map of the Oregon country, reaching into the San Francisco and Sacramento country the squadron surveyed in 1841. American ambition for both Oregon and California on one sheet, five years before the war.",
        "look_for": "how far south the Oregon map reaches, the American eye already on California.",
    },
    "wilkes-atlas-carquinez-vallejo-bay": {
        "headnote": "Wilkes's chart of the Carquinez Strait and the northern arms of the bay, the water road inland the American survey fixed in 1841, ground the interactive maps here cross constantly.",
        "look_for": "the straits and inland bays the US Navy charted before the conquest.",
    },
    "beechey-plan-harbour-san-francisco": {
        "headnote": "A second Beechey sheet of San Francisco Bay, companion to the harbour chart in this group. The Royal Navy's survey remained the standard picture of the bay for two decades.",
        "look_for": "the survey that served every ship in the bay until the American charts replaced it.",
    },
    # ---- Claims and Boundary Maps ----
    "bowen-north-america-composite": {
        "headnote": "The standard British mid-eighteenth-century map of the continent, carrying New Albion on the Pacific coast: Drake's claim kept alive in print for two centuries. Cartography as a long-running territorial argument.",
        "look_for": "the label New Albion on the California coast, an English claim by prior discovery.",
    },
    "arrowsmith-new-discoveries-north-america": {
        "headnote": "London's running state-of-knowledge map of the west, the Hudson's Bay Company world; this 1814 state is the issue that first folded in the Lewis and Clark discoveries. The map continually rewritten as the interior was learned.",
        "look_for": "the freshly added Lewis and Clark route, knowledge arriving on the plate.",
    },
    "lewis-1804-louisiana": {
        "headnote": "The purchase-era map of the Louisiana territory, what the United States thought it had just bought in 1803: the eastern half of the continental ambition that would end at the Pacific.",
        "look_for": "the vast, vaguely bounded interior the young republic had acquired.",
    },
    "robinson-1819-mexico-louisiana-missouri": {
        "headnote": "The maximal American cartographic claim of the treaty moment, published in 1819 as the boundary was being negotiated: the United States' case drawn at its most aggressive.",
        "look_for": "how far west and south the American claim is pushed on the eve of the Adams-Onis line.",
    },
    "tanner-1847-map-united-states-of-mexico": {
        "headnote": "The Fourth Edition of Tanner's map of the Mexican republic, Philadelphia 1847, the most influential general map of the Mexican-American War and the first to carry Fremont's discoveries. Its boundary, through an earlier issue, fed the line Disturnell's map carried into the Treaty of Guadalupe Hidalgo.",
        "look_for": "the boundary and Fremont's routes, the cartography that framed the war's settlement.",
    },
    "mitchell-1846-texas-oregon-california": {
        "headnote": "The annexation-year synthesis, sold to emigrants and expansionists alike: Texas, Oregon, and California as one connected American question. This first 1846 issue captures the expansionist moment whole.",
        "look_for": "the three prizes of Manifest Destiny drawn as a single continental claim.",
    },
    "wyld-mexico-british-possessions-composite": {
        "headnote": "London's view of the continental partition in the Oregon-question years, a reduced reissue of Wyld's 1824 map updated with the Oregon Trail and Fremont's South Pass: Britain watching the American advance west.",
        "look_for": "the emigrant trail and passes added as London tracked the American push.",
    },
    # ---- Conquest and Gold Rush ----
    "emory-1847-military-reconnaissance": {
        "headnote": "Emory's route map of the Army of the West's march to California, the conquest's own cartographic record, made by the officer who marched it.",
        "look_for": "the invasion route itself, the conquest drawn as it happened.",
    },
    "fremont-preuss-1848-oregon-upper-california": {
        "headnote": "The first US government map of the newly conquered territory, drawn by Preuss from Fremont's surveys: the official American picture of the prize just taken.",
        "look_for": "the ceded territory as the conquering government first published it.",
    },
    "mitchell-1849-oregon-uc-nm": {
        "headnote": "The ceded conquest as first mapped for the American public in 1849, with Upper or New California still filling the whole interior basin, the old Mexican geography not yet redrawn by the states to come.",
        "look_for": "the enormous undivided California before the survey grid carved it up.",
    },
    "uscs-city-of-san-francisco-and-vicinity": {
        "headnote": "The federal survey of the instant city, San Francisco charted by the Coast Survey as the Gold Rush turned a village into a port overnight.",
        "look_for": "the boomtown grid the American survey rushed to fix.",
    },
    "uscs-bodega-bay-california": {
        "headnote": "The American chart of Bodega Bay, the port Spain discovered in 1775 and never held, surveyed at last by the power that ended up with it: the Open Door argument's final cartographic bookend.",
        "look_for": "the anchorage the United States charted after three empires had passed it by.",
    },
    "gibbes-1852-new-map-of-california": {
        "headnote": "Gibbes's Gold Rush synthesis of the new state, the Southern Mines country included: the map that sold California to the miners and settlers pouring in.",
        "look_for": "the mining country drawn for the men rushing to it.",
    },
    "ringgold-1851-general-chart-sf-bay": {
        "headnote": "From Ringgold's charts with sailing directions, the first thorough American survey of San Francisco Bay after the conquest, made for the Gold Rush shipping that Beechey's old chart could no longer serve.",
        "look_for": "the bay resurveyed for a traffic the old British chart could not handle.",
    },
    "ringgold-1851-san-pablo-carquinez": {
        "headnote": "The strait's first American navigation chart, the narrows the Karkin once controlled, sounded for the river traffic to the gold country.",
        "look_for": "the Carquinez narrows opened to the steamers bound upriver.",
    },
    "ringgold-1851-suisun-vallejo-bays": {
        "headnote": "Ringgold's chart of Suisun Bay and the Vallejo anchorage, the water road to Sacramento and Solano County's shore in its first American survey.",
        "look_for": "the inland bays that carried the Gold Rush to the mines.",
    },
    "coast-survey-monterey-bay-1857": {
        "headnote": "The federal survey of Monterey Bay, harbor of the old Spanish and Mexican capital, charted by the power that had just taken it, under A. D. Bache of the Coast Survey.",
        "look_for": "the former capital's harbor precisely fixed by the new sovereign.",
    },
    "coast-survey-san-diego-bay-1857": {
        "headnote": "The Coast Survey chart of San Diego Bay, the southern anchor of the province and the first Spanish landfall of 1769, mapped in detail by the American survey a decade after the conquest.",
        "look_for": "the harbor where Spanish California began, redrawn by the United States.",
    },
}
for it in items:
    hn = HEADNOTES.get(it["id"])
    if hn:
        it["headnote"] = hn["headnote"]
        it["look_for"] = hn.get("look_for", "")
print("headnotes attached:", sum(1 for it in items if it.get("headnote")))

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
