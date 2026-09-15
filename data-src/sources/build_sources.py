#!/usr/bin/env python3
"""Build maps/sources.html — the site-wide source apparatus.

Every map on this site is driven by a JSON dataset in data/, and almost every feature
in those datasets carries its own citation. This script reads all of them, normalises
~4,600 citation strings into the works they refer to, and writes one page that says
what the site is built on and which map uses which.

It is a GENERATOR, not a hand-written page: rerun it after any data change and the
page follows the data. Three gates run at the end and the build fails if they trip.

    python3 data-src/sources/build_sources.py

WHAT IT WILL NOT DO. It does not invent bibliographic detail. A work's full form is
printed only where that form is already established in the site's own verified
apparatus (the lumber-ports and lighthouses Sources pages, which were audited before
publication) or where the citation string in the data is itself complete. Everything
else is listed in the short form the data actually uses. Unmatched citations are
reported, not silently dropped.
"""
import json, pathlib, re, collections, html, sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = ROOT / "maps" / "sources.html"

SKIP_DATASETS = {"peoples"}  # index/registry files with no map of their own

# Maps whose dataset is a variant kept for comparison rather than a published map
EXPERIMENTAL = {"ranchos-experimental", "ranchos-experimental-nahc"}

MAP_PAGE = {
    "bay-coastal-defense": "bay-coastal-defense.html",
    "bodega-ross-corridor": "bodega-ross-corridor.html",
    "borderlands-frontier": "borderlands-frontier.html",
    "lighthouses": "lighthouses.html",
    "lumber-ports": "lumber-ports.html",
    "military-engagements": "military-engagements.html",
    "missions-establishments": "missions-establishments.html",
    "moraga-expeditions": "moraga-expeditions.html",
    "native-california": "native-california.html",
    "population-californias": "population-californias.html",
    "presidial-system": "presidial-system.html",
    "ranchos": "ranchos.html",
    "secularization-missions": "secularization-missions.html",
    "zalvidea-moraga-1806": "zalvidea-moraga-1806.html",
    "ranchos-experimental": "ranchos-experimental.html",
    "ranchos-experimental-nahc": "ranchos-experimental-nahc.html",
}
OWN_SOURCES_PAGE = {
    "lumber-ports": "lumber-ports-sources.html",
    "lighthouses": "lighthouses-sources.html",
}

# ---------------------------------------------------------------------------
# The works table.
#
# key      stable id
# title    what gets printed. Full forms come from the site's own audited
#          apparatus or from complete citation strings in the data.
# cat      section of the page
# pat      regexes tested against each citation atom (case-insensitive)
# hosts    URL hosts that also indicate this work
# pages    maps whose own Sources page or the site bibliography establishes this work,
#          for works cited in prose rather than in a feature's citation field
# note     an honesty note printed with the entry
# ---------------------------------------------------------------------------
W = [
 # ---- archival & manuscript ----
 dict(key="ca", cat="archival", pat=[r"\bC-?A\s*\d", r"archives of california", r"savage",
        r"prov\.? st\.? pap", r"provincial state papers", r"provincial records",
        r"dep\.? st\.? pap", r"departmental state papers", r"departmental records",
        r"dep\.? rec", r"st\.? pap\.?,? missions", r"state papers", r"sup\.? govt",
        r"unbound doc", r"benicia", r"legis\.? rec"],
      title="<strong>Archives of California</strong> (BANC MSS C&#8211;A), The Bancroft Library, "
            "University of California, Berkeley &#8212; the Thomas Savage transcript copies, 63 volumes.",
      note="The originals burned in 1906; Savage's copies are the record. Most features on this "
           "site that rest on a manuscript rest on these. Pins with a catalog record deep-link to "
           "the <a href='https://archivesofcalifornia.com'>documentary calendar</a> and from there "
           "to the manuscript leaf."),
 dict(key="cb", cat="archival", pat=[r"\bC-?B\s*\d", r"vallejo,? documentos", r"documentos para la historia"],
      title="<strong>Mariano Guadalupe Vallejo, <em>Documentos para la Historia de California</em></strong> "
            "(BANC MSS C&#8211;B), The Bancroft Library &#8212; cited by volume and document.",
      note="The companion collection to C&#8211;A, and the source for much of the presidio "
           "artillery and garrison detail."),
 dict(key="landcase", cat="archival", pat=[r"land case", r"land-claim case", r"\bND \d{2,3}\b", r"\bSD \d{2,3}\b",
        r"digicoll", r"northern district of california", r"southern district of california"],
      hosts=["digicoll.lib.berkeley.edu"],
      title="<strong>United States District Court land case files for California</strong>, The Bancroft "
            "Library (Northern and Southern District series, cited as ND / SD by case number). "
            "Digitised at digicoll.lib.berkeley.edu.",
      note="The evidentiary basis for the rancho maps: each confirmed grant generated a case file "
           "with the claimant's title papers."),
 dict(key="diseno", cat="archival", pat=[r"diseño", r"diseno", r"land case maps"],
      title="<strong>Land Case Maps (<em>dise&#241;os</em>)</strong>, The Bancroft Library &#8212; the "
            "hand-drawn grant sketches filed as evidence in the land cases.",
      note="1,397 catalogued for this project; the gallery reproduces them."),
 dict(key="sfmaritime", cat="archival", pat=[r"porter shaw", r"san francisco maritime", r"sf maritime",
        r"christensen", r"carlos a\.? call", r"canright"],
      hosts=["maritime.org"],
      title="<strong>San Francisco Maritime National Historical Park</strong>, J. Porter Shaw Library "
            "&#8212; Carl Christensen and Carlos A. Call photograph collections; Tooker and Lewis "
            "research files; Canright, &#8220;Coastwise Lumber Transportation.&#8221;"),
 dict(key="humboldt", cat="archival", pat=[r"cal poly humboldt", r"ericson", r"palmquist",
        r"swanlund", r"schoenrock"],
      hosts=["humboldt.edu", "humboldthistory.org", "humboldthistoryresearch.org"],
      title="<strong>Cal Poly Humboldt Special Collections</strong> &#8212; A. W. Ericson, Palmquist, "
            "Swanlund&#8211;Baker, Boyle and Schoenrock photograph collections."),
 dict(key="localsoc", cat="archival", pat=[r"kelley house", r"fort ross conservancy",
        r"sonoma county library", r"mill valley historical", r"historical society"],
      hosts=["kelleyhousemuseum.org", "fortross.org", "cdn.fortross.org", "marinhistory.org",
             "mcmrhs.org", "aptoshistory.org", "cambriahistoricalsociety.com", "delnortehistory.org",
             "tomaleshistory.com", "saltpoint.org", "oceancove.org"],
      title="<strong>Local historical societies and house museums</strong> &#8212; Kelley House Museum "
            "(Mendocino), Fort Ross Conservancy, Sonoma County Library heritage collections, Mill "
            "Valley Historical Society, Marin History Museum, Del Norte, Aptos, Cambria, Tomales "
            "and Salt Point local collections."),
 dict(key="oac", cat="archival", pat=[r"\boac\b", r"online archive of california", r"calisphere"],
      hosts=["oac.cdlib.org", "calisphere.org", "cdm16166.contentdm.oclc.org"],
      title="<strong>Online Archive of California</strong> and <strong>Calisphere</strong> &#8212; "
            "finding aids and digitised images from California repositories."),

 # ---- printed primary ----
 dict(key="bancroft", cat="printed", pat=[r"bancroft,? hist", r"history of california", r"\bbancroft,?\s+[ivx]+\b",
        r"hist\.? cal", r"pioneer register"],
      title="Bancroft, Hubert Howe. <em>History of California</em>, 7 vols. San Francisco: "
            "The History Company, 1884&#8211;1890 &#8212; including the Pioneer Register.",
      note="Used as a printed primary compilation as much as a secondary work: Bancroft quotes and "
           "calendars documents whose originals are gone."),
 dict(key="davidson", cat="printed", pat=[r"davidson", r"coast pilot"],
      title="Davidson, George. <em>Pacific Coast. Coast Pilot of California, Oregon, and "
            "Washington</em>. Washington: GPO, 1869; 4th ed., 1889.",
      note="The single most useful printed source for nineteenth-century coastal positions, "
           "landings and station descriptions."),
 dict(key="lhboard", cat="printed", pat=[r"light-?house board", r"lighthouse board", r"annual report of the light",
        r"commissioner of lighthouses", r"sectreas", r"light list"],
      hosts=["navcen.uscg.gov"],
      title="<em>Annual Report of the Light-House Board</em>, fiscal years 1852&#8211;1910 (printed "
            "within the <em>Annual Report of the Secretary of the Treasury</em> through the 1870s, "
            "thereafter separately and within the Department of Commerce and Labor reports); "
            "<em>Annual Report of the Commissioner of Lighthouses</em>, 1911 onward; U.S. Coast Guard "
            "<em>Light List</em>, Volume VI.",
      note="163 passages are quoted verbatim on the lighthouses map, cited per passage to report "
           "year and printed page."),
 dict(key="usace", cat="printed", pat=[r"corps of engineers", r"chief of engineers"],
      hosts=["spn.usace.army.mil"],
      title="U.S. Army Corps of Engineers. <em>Annual Report of the Chief of Engineers</em> "
            "(harbour and bar works, principally Humboldt)."),
 dict(key="tsheet", cat="printed", pat=[r"t-?sheet", r"topographic sheet", r"coast (?:&|and|&amp;) geodetic",
        r"usc&gs", r"harbor chart", r"historical map (?:&|and|&amp;) chart"],
      title="U.S. Coast &amp; Geodetic Survey topographic sheets (T-sheets) and harbour charts, "
            "1852&#8211;1930s. NOAA Historical Map &amp; Chart Collection."),
 dict(key="diaries", cat="printed", pat=[r"muñoz", r"munoz", r"zalvidea"],
      title="Diary of Fr. Pedro Mu&#241;oz (Moraga expedition, 1806) and Diary of Fr. Jos&#233; Mar&#237;a "
            "de Zalvidea (1806), as edited and translated in Cook."),
 dict(key="gibson", cat="printed", pat=[r"gibson", r"istomin"],
      title="Gibson, James R., and Alexei A. Istomin, eds. <em>Russian California, 1806&#8211;1860: "
            "A History in Documents</em> &#8212; cited by document number.",
      note="Cited in the data as &#8220;Gibson &amp; Istomin, Doc <em>n</em>&#8221;."),
 dict(key="russam", cat="printed", pat=[r"avpri", r"golovnin", r"farris", r"baranov", r"kuskov",
        r"khlebnikov", r"\bRAC\b", r"russian-american company"],
      title="Russian-American Company material &#8212; documents from the Archive of the Foreign "
            "Policy of the Russian Empire (AVPRI), and Golovnin and Khlebnikov as cited in the "
            "data in short form, often at second hand through Farris and through Gibson &amp; "
            "Istomin.",
      note="Where a Russian document is reached through a translation or a secondary work rather "
           "than the archive, the citation says so."),
 dict(key="wagner", cat="printed", pat=[r"wagner 19", r"\bwagner\b"],
      title="Wagner, Henry R. &#8212; the 1931 edition of the Spanish northwest-coast voyage "
            "accounts, cited in the data as &#8220;Wagner 1931&#8221; with page numbers."),
 dict(key="hittell", cat="printed", pat=[r"hittell"], pages=["lumber-ports"],
      title="Hittell, John S. <em>The Commerce and Industries of the Pacific Coast</em>. "
            "San Francisco: A. L. Bancroft, 1882."),
 dict(key="jepson", cat="printed", pat=[r"jepson"],
      title="Jepson, Willis L. <em>California Tanbark Oak</em>. USDA Forest Service Bulletin 75. "
            "Washington: GPO, 1911."),
 dict(key="hoffman", cat="printed", pat=[r"hoffman"],
      title="Hoffman, Ogden. <em>Reports of Land Cases Determined in the United States District "
            "Court for the Northern District of California</em>. San Francisco, 1862."),
 dict(key="vessels", cat="printed", pat=[r"merchant vessels", r"vessel register", r"\blyman\b"],
      title="<em>Annual List of Merchant Vessels of the United States</em>, 1877&#8211;1924 "
            "(vessel tonnages), with Lyman's compilation from the registers."),
 dict(key="news", cat="printed", pat=[r"daily alta", r"mendocino beacon", r"fort bragg advocate",
        r"ukiah", r"san francisco call", r"chronicle", r"newspaper", r"\bcdnc\b", r"california star"],
      hosts=["northcoastjournal.com", "lostcoastoutpost.com", "madriverunion.com", "sfgate.com",
             "ijpr.org"],
      title="Period newspapers &#8212; <em>Daily Alta California</em>, <em>Mendocino Beacon</em>, "
            "<em>Fort Bragg Advocate</em>, <em>Ukiah Republican Press</em>, the San Francisco "
            "<em>Call</em> and <em>Chronicle</em>, the <em>California Star</em>. Via the California "
            "Digital Newspaper Collection and as quoted in the doghole-ports MPDF."),
 dict(key="haer", cat="printed", pat=[r"\bhaer\b", r"\bhabs\b", r"historic american"],
      title="Historic American Engineering Record / Historic American Buildings Survey, "
            "Library of Congress &#8212; HAER No. CA-61 (schooner <em>C. A. Thayer</em>, 1988), "
            "No. CA-67 (steam schooner <em>Wapama</em>, 2001), and light-station documentation."),

 # ---- datasets & GIS ----
 dict(key="nahc", cat="gis", pat=[r"nahc", r"cnra", r"california land grants \(plss"],
      title="<strong>NAHC / California Natural Resources Agency, California Land Grants</strong> "
            "&#8212; grant boundaries reconstructed against the Public Land Survey System.",
      note="One of two independent boundary sets on the site; the rancho maps exist in two versions "
           "precisely because the two disagree."),
 dict(key="ecai", cat="gis", pat=[r"ecai", r"ucsd", r"spanish (?:&|and|&amp;) mexican land grants",
        r"california land grants arcgis"],
      title="<strong>ECAI / UCSD, Spanish &amp; Mexican Land Grants of California</strong> "
            "(via the California Land Grants ArcGIS project) &#8212; boundary and land-case data.",
      note="The base for the published rancho map."),
 dict(key="hnai", cat="gis", pat=[r"handbook of north american indians", r"salton sea database",
        r"smithsonian, 1978", r"vol\.? 8, california"],
      title="<strong>Handbook of North American Indians, vol. 8: California</strong> "
            "(Smithsonian Institution, 1978) &#8212; tribal territory boundaries, as digitised by "
            "the Salton Sea Database Program, University of Redlands.",
      note="Territory lines on a map imply a hard edge that the ethnography does not support. "
           "They are drawn as generalisations, and subgroup labels are positioned without "
           "boundaries implied."),
 dict(key="gnis", cat="gis", pat=[r"\bgnis\b", r"geographic names"],
      title="<strong>USGS Geographic Names Information System (GNIS)</strong> &#8212; used to fix "
            "coordinates for named coastal features, cited by feature ID."),
 dict(key="nhd", cat="gis", pat=[r"\bnhd\b", r"national hydrography", r"flowline"],
      hosts=["prd-tnm.s3.amazonaws.com", "carto.nationalmap.gov"],
      title="<strong>USGS National Hydrography Dataset</strong> and The National Map &#8212; "
            "stream flowlines, used to place inland railheads and creek-mouth landings."),
 dict(key="osm", cat="gis", pat=[r"openstreetmap", r"\bosm\b", r"overpass"],
      title="<strong>OpenStreetMap</strong> &#8212; surviving rail alignments, traced for the "
            "lumber railroads where a historic grade is still on the ground."),
 dict(key="rumsey", cat="gis", pat=[r"rumsey"], hosts=["davidrumsey.com"],
      title="<strong>David Rumsey Map Collection</strong> &#8212; georeferenced historical maps."),

 # ---- secondary ----
 dict(key="cook", cat="secondary", pat=[r"\bcook\b", r"colonial expeditions"],
      title="Cook, Sherburne F. <em>Colonial Expeditions to the Interior of California: Central "
            "Valley, 1800&#8211;1820</em>. Berkeley: University of California Press, 1960.",
      note="The route studies behind the expedition maps, and the source of the village "
           "identifications, which Cook himself gave as approximate."),
 dict(key="thompson", cat="secondary", pat=[r"thompson", r"\bhrs 1979\b", r"defender of the gate",
        r"forts baker"],
      title="Thompson, Erwin N. National Park Service historic resource studies on the Golden Gate "
            "forts &#8212; cited in the data as &#8220;Thompson HRS 1979&#8221; with page numbers.",
      note="The standard documentation for the Bay's coastal batteries."),
 dict(key="cdbooks", cat="secondary", pat=[r"martini", r"\bchin\b", r"haller",
        r"fortress alcatraz", r"artillery at the golden gate", r"last missile site",
        r"fort point \(20"],
      title="The Golden Gate fortification literature &#8212; Martini, <em>Fortress Alcatraz</em> "
            "(1991) and <em>Fort Point</em> (2016); Chin, <em>Artillery at the Golden Gate</em> "
            "(1994); Haller and Martini, <em>The Last Missile Site</em> (2010)."),
 dict(key="mofras", cat="printed", pat=[r"duflot", r"mofras"],
      title="Duflot de Mofras, Eug&#232;ne. The 1844 account of the Pacific coast, cited in the "
            "data by year for the post-sale condition of the Russian establishments."),
 dict(key="chartmaps", cat="printed", pat=[r"cartas esf", r"plano del puerto", r"gallery item",
        r"\bLOC, gallery\b"],
      title="Spanish hydrographic charts &#8212; the <em>Plano del Puerto</em> series and the "
            "<em>Cartas esf&#233;ricas</em>, including the 1793 re-survey, from the Library of "
            "Congress and reproduced in this site&#8217;s "
            "<a href='../gallery/index.html'>gallery</a>."),
 dict(key="langelier", cat="secondary", pat=[r"langelier", r"rosen"],
      title="Langelier, John P., and Daniel B. Rosen. <em>El Presidio de San Francisco: A History "
            "under Spain and Mexico, 1776&#8211;1846</em>. 1992."),
 dict(key="engelhardt", cat="secondary", pat=[r"engelhardt"],
      title="Engelhardt, Zephyrin. The mission histories &#8212; used for mission foundation dates "
            "and estate outstations, at year grain."),
 dict(key="krell", cat="secondary", pat=[r"\bkrell\b"],
      title="Krell, Dorothy, ed. <em>The California Missions: A Pictorial History</em> &#8212; "
            "used with Bancroft and Engelhardt for secularization years."),
 dict(key="kroeber", cat="secondary", pat=[r"kroeber"],
      pages=["native-california", "zalvidea-moraga-1806"],
      title="Kroeber, A. L. <em>Handbook of the Indians of California</em>. Bureau of American "
            "Ethnology Bulletin 78. Washington: GPO, 1925."),
 dict(key="gifford", cat="secondary", pat=[r"gifford", r"schenck"],
      pages=["zalvidea-moraga-1806", "moraga-expeditions"],
      title="Gifford, E. W., and W. E. Schenck. <em>Archaeology of the Southern San Joaquin "
            "Valley</em>. Berkeley, 1926."),
 dict(key="mpdf", cat="secondary", pat=[r"marx", r"jaffke", r"doghole", r"\bmpdf\b"],
      hosts=["ohp.parks.ca.gov"],
      title="Marx, Deborah, and Denise Jaffke. <em>Northern California Doghole Ports Maritime "
            "Cultural Landscape</em>. NRHP Multiple Property Documentation Form, draft. "
            "California Department of Parks and Recreation / Office of Historic Preservation, 2021.",
      note="A DRAFT nomination. The backbone inventory for the lumber-ports map, and flagged as "
           "draft wherever it carries a claim alone."),
 dict(key="delgado", cat="secondary", pat=[r"delgado"], pages=["lumber-ports"],
      title="Delgado, Green, Jaffke, Lawrence and Marx. <em>Maritime Cultural Landscape of "
            "Sonoma's Doghole Ports</em>. Publications in Cultural Heritage 37. Sacramento: "
            "California Department of Parks and Recreation, 2021."),
 dict(key="lumberbooks", cat="secondary", pat=[r"mcnairn", r"macmullen", r"jackson", r"carranco",
        r"labbe", r"stanger", r"kortum", r"olmsted", r"tooker", r"\bwurm\b", r"crump", r"kneiss",
        r"layton", r"\bhenson\b", r"usner", r"munro-fraser", r"palmer", r"elliott", r"bledsoe",
        r"sullenberger", r"county histor"],
      title="The redwood-coast literature &#8212; McNairn &amp; MacMullen, <em>Ships of the Redwood "
            "Coast</em> (1945); Jackson, <em>The Doghole Schooners</em> (1977); Carranco, "
            "<em>Redwood Lumber Industry</em> (1982) and Carranco &amp; Labbe, <em>Logging the "
            "Redwoods</em> (1975); Stanger, <em>Sawmills in the Redwoods</em> (1967); Kortum &amp; "
            "Olmsted in <em>California Historical Quarterly</em> 50:1 (1971); Tooker in <em>Sea "
            "Letter</em> 6:1 (1968); Wurm, Crump and Kneiss on the logging railroads; Layton, "
            "<em>The Voyage of the Frolic</em> (1997); Henson &amp; Usner on Big Sur; and the "
            "county histories of Munro-Fraser, Palmer, Elliott and Bledsoe (1880&#8211;81)."),
 dict(key="milliken", cat="secondary", pat=[r"milliken"],
      title="Milliken, Randall &#8212; cited in the data in short form as &#8220;Milliken 2009&#8221; "
            "with page numbers, for Bay Area tribal geography and mission demography."),
 dict(key="menzies", cat="printed", pat=[r"menzies"],
      title="Menzies, Archibald. The journal of the Vancouver expedition&#8217;s naturalist, "
            "cited in the data in short form as &#8220;Menzies 1924&#8221; with page numbers."),
 dict(key="vaultreg", cat="archival", pat=[r"garrison (?:&|and|&amp;) artillery", r"register \(vault\)",
        r"\(vault\)"],
      title="<strong>Presidio garrison and artillery register</strong> &#8212; an unpublished working "
            "register compiled for this project from the Archives of California transcripts and "
            "the printed accounts.",
      note="Not yet published. Where a feature rests on it alone, the underlying documents are "
           "cited in the register and can be supplied on request."),
 dict(key="shanks", cat="secondary", pat=[r"shanks", r"guardians of the golden gate",
        r"lighthouses and lifeboats"],
      hosts=["uslhs.org"],
      title="Shanks, Ralph, and Lisa Woo Shanks. <em>Guardians of the Golden Gate</em> and "
            "<em>Lighthouses and Lifeboats of the Redwood Coast</em>; U.S. Lighthouse Society, "
            "Lighthouse Research Catalog."),

 # ---- agency & register ----
 dict(key="nrhp", cat="agency", pat=[r"nrhp", r"national register", r"nomination", r"npgallery", r"bookwalter",
        r"\bNRIS\b", r"\bMPS\b", r"listed-properties"],
      hosts=["npgallery.nps.gov"],
      title="<strong>National Register of Historic Places</strong> nominations, via NPGallery "
            "&#8212; cited by reference number, including Bookwalter&#8217;s <em>Light Stations of "
            "California</em> multiple-property submission (1989) and the Bear Harbor Landing "
            "district, with the NRIS listed-properties dataset for listing dates."),
 dict(key="nps", cat="agency", pat=[r"\bnps\b", r"national park service", r"golden gate nra",
        r"ggnra", r"lime point"],
      hosts=["nps.gov"],
      title="<strong>National Park Service</strong> &#8212; Golden Gate National Recreation Area "
            "and Presidio of San Francisco site documentation."),
 dict(key="noaa", cat="agency", pat=[r"noaa", r"farallones", r"gfnms", r"national marine sanctuary"],
      hosts=["farallones.noaa.gov"],
      title="<strong>NOAA Greater Farallones National Marine Sanctuary</strong> &#8212; the "
            "doghole-ports survey pages, with per-port histories and credited historic photographs."),
 dict(key="ohp", cat="agency", pat=[r"state parks", r"\bohp\b", r"california historical landmark",
        r"\bchl\b", r"office of historic preservation"],
      hosts=["parks.ca.gov", "californiahistoricallandmarks.com", "hmdb.org", "noehill.com"],
      title="<strong>California State Parks</strong>, the Office of Historic Preservation, the "
            "California Historical Landmarks register, and the Historical Marker Database."),
 dict(key="uscghist", cat="agency", pat=[r"coast guard historian", r"uscg historian"],
      title="<strong>U.S. Coast Guard Historian's Office</strong> &#8212; historic light-station "
            "information and photography, California."),
 dict(key="loc", cat="agency", pat=[r"library of congress"], hosts=["loc.gov", "tile.loc.gov"],
      title="<strong>Library of Congress</strong> &#8212; photographs, survey documentation and "
            "digitised maps."),
 dict(key="ia", cat="agency", pat=[r"archive\.org", r"internet archive", r"hathitrust", r"openlibrary"],
      hosts=["archive.org", "openlibrary.org"],
      title="<strong>Internet Archive</strong> and <strong>HathiTrust</strong> &#8212; the delivery "
            "mechanism for most of the printed primary sources above, and for the scanned Savage "
            "volumes.",
      note="A finding aid, not an authority: what is cited is the work, not the scan."),
 dict(key="wayback", cat="agency", pat=[r"wayback"], hosts=["web.archive.org"],
      title="<strong>Internet Archive Wayback Machine</strong> &#8212; used where an agency page "
            "that carried a fact has since been taken down. Cited with its capture date."),

 # ---- tertiary web ----
 dict(key="fortwiki", cat="tertiary", pat=[r"fortwiki", r"northamericanforts"],
      hosts=["fortwiki.com", "northamericanforts.com"],
      title="FortWiki and NorthAmericanForts.com &#8212; fortification compendia."),
 dict(key="milmuseum", cat="tertiary", pat=[r"military museum", r"militarymuseum", r"state military"],
      hosts=["militarymuseum.org", "themilitarystandard.com"],
      title="California State Military Museum (militarymuseum.org) and The Military Standard."),
 dict(key="thelen", cat="tertiary", pat=[r"thelen", r"nike database"],
      title="Ed Thelen's Nike missile site database &#8212; the standard hobbyist register of "
            "Nike installations."),
 dict(key="lhfriends", cat="tertiary", pat=[r"lighthousefriends"], hosts=["lighthousefriends.com"],
      title="LighthouseFriends.com &#8212; station histories."),
 dict(key="railfan", cat="tertiary", pat=[r"mendorailhistory", r"pacificng", r"santacruztrains",
        r"skunktrain"],
      hosts=["mendorailhistory.org", "pacificng.com", "santacruztrains.com", "skunktrain.com",
             "wx4.org"],
      title="Railroad-history sites &#8212; MendoRailHistory, PacificNG, Santa Cruz Trains, "
            "the Skunk Train's own history pages."),
 dict(key="wikipedia", cat="tertiary", pat=[r"wikipedia", r"wikimedia"],
      hosts=["en.wikipedia.org", "upload.wikimedia.org", "localwiki.org", "foundsf.org",
             "medium.com", "mobileranger.com", "keith-skinner.com", "sanfranciscostory.com",
             "historylink.org", "coastview.org", "krisweb.com", "hikinginbigsur.com",
             "santacruztrails.org", "santacruzwaves.com", "pescaderomemories.com",
             "sunnyfortuna.com", "trinidad-ca.com", "visitsansimeonca.com", "humboldtbay.org",
             "sheltercove-ca.gov", "mattolehistory.wordpress.com", "foresthistory.org",
             "icce-ojs-tamu.tdl.org"],
      title="Wikipedia, Wikimedia Commons, and general-interest local-history web pages."),
]


# Short forms for the home-page summary. Derived truncation cut names at their
# initials ("Gibson, James R., and Alexei A"), so these are set explicitly.
SHORT = {
 "ca": "Archives of California (BANC MSS C&#8211;A), Bancroft Library",
 "cb": "Vallejo, <em>Documentos para la Historia de California</em> (C&#8211;B)",
 "landcase": "U.S. District Court land case files, Bancroft Library",
 "diseno": "Land Case Maps (<em>dise&#241;os</em>), Bancroft Library",
 "sfmaritime": "SF Maritime NHP, J. Porter Shaw Library",
 "humboldt": "Cal Poly Humboldt Special Collections",
 "localsoc": "Local historical societies and house museums",
 "oac": "Online Archive of California and Calisphere",
 "vaultreg": "Presidio garrison and artillery register (unpublished)",
 "bancroft": "Bancroft, <em>History of California</em>, 7 vols. (1884&#8211;90)",
 "davidson": "Davidson, <em>Coast Pilot</em> (1869; 4th ed. 1889)",
 "lhboard": "<em>Annual Report of the Light-House Board</em> and the <em>Light List</em>",
 "usace": "Army Corps, <em>Annual Report of the Chief of Engineers</em>",
 "tsheet": "USC&amp;GS T-sheets and harbour charts",
 "diaries": "The Mu&#241;oz and Zalvidea diaries (1806)",
 "gibson": "Gibson &amp; Istomin, <em>Russian California, 1806&#8211;1860</em>",
 "russam": "Russian-American Company material (AVPRI, Golovnin, Khlebnikov)",
 "wagner": "Wagner (1931), Spanish northwest-coast voyages",
 "hittell": "Hittell, <em>Commerce and Industries of the Pacific Coast</em> (1882)",
 "jepson": "Jepson, <em>California Tanbark Oak</em> (1911)",
 "hoffman": "Hoffman, <em>Reports of Land Cases</em> (1862)",
 "vessels": "<em>Annual List of Merchant Vessels</em> (1877&#8211;1924)",
 "news": "Period newspapers (<em>Alta California</em>, <em>Mendocino Beacon</em>, and others)",
 "haer": "HAER / HABS documentation, Library of Congress",
 "mofras": "Duflot de Mofras (1844)",
 "chartmaps": "Spanish hydrographic charts (<em>Cartas esf&#233;ricas</em>)",
 "menzies": "Menzies (1924)",
 "nahc": "NAHC / CNRA California Land Grants (PLSS)",
 "ecai": "ECAI / UCSD Spanish &amp; Mexican Land Grants",
 "hnai": "<em>Handbook of North American Indians</em>, vol. 8 (1978)",
 "gnis": "USGS GNIS",
 "nhd": "USGS National Hydrography Dataset",
 "osm": "OpenStreetMap",
 "rumsey": "David Rumsey Map Collection",
 "cook": "Cook, <em>Colonial Expeditions</em> (1960)",
 "thompson": "Thompson, NPS historic resource studies on the Golden Gate forts",
 "cdbooks": "Martini, Chin and Haller on the Golden Gate fortifications",
 "langelier": "Langelier &amp; Rosen, <em>El Presidio de San Francisco</em> (1992)",
 "engelhardt": "Engelhardt, the mission histories",
 "krell": "Krell, <em>The California Missions</em>",
 "kroeber": "Kroeber, <em>Handbook of the Indians of California</em> (1925)",
 "gifford": "Gifford &amp; Schenck, <em>Southern San Joaquin Valley</em> (1926)",
 "milliken": "Milliken (2009)",
 "mpdf": "Marx &amp; Jaffke, Northern California Doghole Ports MPDF (draft, 2021)",
 "delgado": "Delgado et al., <em>Sonoma's Doghole Ports</em> (2021)",
 "lumberbooks": "The redwood-coast literature (McNairn, Jackson, Carranco and others)",
 "shanks": "Shanks, <em>Guardians of the Golden Gate</em>; U.S. Lighthouse Society",
 "nrhp": "National Register nominations (NPGallery)",
 "nps": "National Park Service",
 "noaa": "NOAA Greater Farallones NMS",
 "ohp": "California State Parks and the Office of Historic Preservation",
 "uscghist": "U.S. Coast Guard Historian's Office",
 "loc": "Library of Congress",
 "ia": "Internet Archive and HathiTrust",
 "wayback": "Internet Archive Wayback Machine",
 "fortwiki": "FortWiki and NorthAmericanForts.com",
 "milmuseum": "California State Military Museum",
 "thelen": "Ed Thelen's Nike missile site database",
 "lhfriends": "LighthouseFriends.com",
 "railfan": "Railroad-history sites",
 "wikipedia": "Wikipedia and general-interest local-history pages",
}

CATS = [
 ("archival",  "Archival and manuscript sources",
  "What the maps ultimately rest on. Where a feature has a manuscript behind it, the popup cites it."),
 ("printed",   "Printed primary sources",
  "Published contemporaneously with the events, or printing documents whose originals are gone."),
 ("gis",       "Datasets, boundaries and geographic data",
  "Where the lines and the coordinates come from. These carry their own uncertainties, stated below."),
 ("secondary", "Secondary scholarship and reference works",
  "Used for context, for dating at year grain, and for the interpretive claims the maps make."),
 ("agency",    "Government agencies, registers and digital repositories",
  "Agency documentation, the National Register, and the platforms that deliver the scans."),
 ("tertiary",  "Tertiary web sources",
  "Compendia and enthusiast sites. These are useful for leads and for orientation, and they are "
  "<strong>not treated as authorities</strong>. Where one of these is the only support for a "
  "claim, the popup says so."),
]


# Not citations. These are methodological notes, editorial markers and internal article
# slugs that share the `citation` field with real sources. Counting them as unmatched
# sources would understate coverage; matching them to a work would be a lie.
NOT_A_CITATION = [
    r"^link removed\]?$", r"^\[?no archives of california manuscript",
    r"approximate", r"^follow the link", r"^selected, not exhaustive",
    r"^label positions", r"^locations? ", r"^year grain$", r"^circa$",
    r"^[a-z0-9]+(?:-[a-z0-9]+){2,}$",              # internal article/vault slugs
    r"^ca\d+-[a-z-]+$", r"^cook note \d+$",
    r"^spanish royal presidios$", r"^route reconstruction", r"^exact route",
    r"^see [a-z-]+ article$", r"article$", r"^county histories\)?$", r"^engelhardt\)$",
]
_NOTPAT = [re.compile(p, re.I) for p in NOT_A_CITATION]


def is_citation(atom):
    return not any(p.search(atom) for p in _NOTPAT)


def atoms(cit):
    """Split a citation string into the works it names.

    Semicolons separate works, EXCEPT inside parentheses, where a semicolon is part of
    a single parenthetical gloss ("(Suvorov 1815; passport-proclamation ...)"). Splitting
    blindly on ';' shredded those into fragments that matched nothing and made coverage
    look worse than it was.
    """
    c = re.sub(r"^\s*\[[PS]\]\s*", "", cit)
    parts, buf, depth = [], [], 0
    i = 0
    while i < len(c):
        ch = c[i]
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        if depth == 0 and (ch == ";" or c.startswith(" · ", i)):
            parts.append("".join(buf)); buf = []
            i += 3 if ch != ";" else 1
            continue
        buf.append(ch); i += 1
    parts.append("".join(buf))
    out = []
    for p in parts:
        p = p.strip(" .,")
        if p and is_citation(p):
            out.append(p)
    return out


def collect():
    """-> {dataset: {'title':..,'n':..,'atoms':Counter,'hosts':Counter,'quotes':int}}"""
    out = {}
    for fn in sorted(DATA.glob("*.json")):
        if ".bak" in fn.name or fn.stem in SKIP_DATASETS:
            continue
        d = json.loads(fn.read_text())
        if isinstance(d, list):
            continue
        cits, quotes = [], 0

        def take(o):
            nonlocal quotes
            for s in (o.get("sources") or []):
                if isinstance(s, dict) and s.get("citation"):
                    cits.append(s["citation"])
            if o.get("citation"):
                cits.append(o["citation"])
            if o.get("quote"):
                quotes += 1
            for q in (o.get("quotes") or []):
                quotes += 1
        for f in (d.get("features") or []):
            take(f)
        for r in (d.get("routes") or []):
            take(r)
            for s in (r.get("stops") or []):
                take(s)

        ac = collections.Counter()
        for c in cits:
            for a in atoms(c):
                ac[a] += 1
        hosts = collections.Counter()
        for u in re.findall(r"https?://[^\s\"'<>\\]+", fn.read_text()):
            hosts[urlparse(u).netloc.lower().replace("www.", "")] += 1

        out[fn.stem] = dict(title=d.get("title", fn.stem), n=len(d.get("features") or []),
                            atoms=ac, hosts=hosts, quotes=quotes,
                            cited=sum(1 for f in (d.get("features") or []) if f.get("sources")))
    return out


def match_works(sets):
    """-> works->maps, map->works, unmatched atoms"""
    compiled = [(w, [re.compile(p, re.I) for p in w.get("pat", [])],
                 set(w.get("hosts", []))) for w in W]
    w2m = collections.defaultdict(set)
    m2w = collections.defaultdict(collections.Counter)
    unmatched = collections.Counter()

    for m, info in sets.items():
        for atom, cnt in info["atoms"].items():
            hit = False
            for w, pats, _ in compiled:
                if any(p.search(atom) for p in pats):
                    w2m[w["key"]].add(m); m2w[m][w["key"]] += cnt; hit = True
            if not hit:
                unmatched[atom] += cnt
        for w in W:
            if m in (w.get("pages") or []):
                w2m[w["key"]].add(m)
        for host, cnt in info["hosts"].items():
            for w, _, hosts in compiled:
                if host in hosts:
                    w2m[w["key"]].add(m); m2w[m][w["key"]] += 0
    return w2m, m2w, unmatched


def esc(s):
    return html.escape(s, quote=True)


def build(sets, w2m, m2w, unmatched, total_atoms):
    byk = {w["key"]: w for w in W}
    order = [m for m in MAP_PAGE if m in sets and m not in EXPERIMENTAL]
    order += [m for m in MAP_PAGE if m in sets and m in EXPERIMENTAL]

    P = []
    A = P.append
    A('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A('<title>Sources &amp; Method &#183; California History Maps</title>')
    A('<meta name="description" content="The full source apparatus for every map on '
      'California History Maps: the archives, printed primary sources, datasets and '
      'scholarship each map is built on, and which map uses which.">')
    A('<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">')
    A('<link rel="stylesheet" href="../assets/css/site.css">')
    A("""<style>
.method-page { max-width: 56rem; margin: 0 auto; padding: 1rem 1.2rem 4rem; }
.method-page h2 { margin-top: 2.4rem; }
.method-page h3 { margin-top: 1.4rem; font-size: 1.02rem; }
.method-page .lead { font-size: 1.02rem; }
.method-page .note { background: rgba(140,74,47,0.07); border-left: 3px solid #8c4a2f;
  padding: 0.6rem 0.9rem; margin: 0.9rem 0; }
.srctable { width: 100%; border-collapse: collapse; font-size: 0.9rem; margin: 1rem 0; }
.srctable th, .srctable td { text-align: left; vertical-align: top; padding: 0.42rem 0.55rem;
  border-bottom: 1px solid var(--rule, #d9cfbe); }
.srctable th { font-size: 0.76rem; letter-spacing: 0.05em; text-transform: uppercase;
  color: #6b6257; }
.srctable td.num { text-align: right; white-space: nowrap; color: #6b6257; }
.tablewrap { overflow-x: auto; }
ul.works { list-style: none; padding-left: 0; }
ul.works > li { margin: 0.95rem 0; padding-left: 0.9rem; border-left: 2px solid var(--rule, #d9cfbe); }
ul.works .used { display: block; margin-top: 0.3rem; font-size: 0.82rem; color: #6b6257; }
ul.works .caveat { display: block; margin-top: 0.3rem; font-size: 0.86rem; font-style: italic; }
.mapsec { margin: 1.1rem 0 0; padding-left: 0.9rem; border-left: 2px solid var(--rule, #d9cfbe); }
.mapsec h3 { margin: 0 0 0.2rem; }
.mapsec p { margin: 0.25rem 0; font-size: 0.9rem; }
.mapsec .meta { color: #6b6257; font-size: 0.82rem; }
</style>""")
    A('</head>\n<body>')
    A('<header class="site-header">\n  <a class="brand" href="../index.html">California History Maps</a>')
    A('  <nav aria-label="Site">\n    <a href="../index.html">Maps</a>\n'
      '    <a href="../gallery/index.html">Gallery</a>\n'
      '    <a href="../index.html#about">About</a>\n'
      '    <a href="../errata.html">Errata</a>\n  </nav>\n</header>')
    A('<main class="method-page">')
    A('<h1>Sources &amp; Method</h1>')

    nmaps = len([m for m in order if m not in EXPERIMENTAL])
    nfeat = sum(sets[m]["n"] for m in order if m not in EXPERIMENTAL)
    ncited = sum(sets[m]["cited"] for m in order if m not in EXPERIMENTAL)
    nquote = sum(sets[m]["quotes"] for m in order if m not in EXPERIMENTAL)

    A(f'<p class="lead">Every map on this site is driven by an open dataset, and the great '
      f'majority of the features in those datasets carry their own citation. This page gathers '
      f'what the whole site is built on and says which map uses which. Across '
      f'{nmaps} published maps there are {nfeat:,} features, {ncited:,} of them carrying at least '
      f'one citation of their own, and {nquote:,} carrying a quoted passage from a source. '
      f'This page is generated from the datasets, not maintained by hand, so it follows the data.</p>')

    A('<div class="note"><p>Two maps have their own fuller apparatus, because they were built '
      'to a higher standard of documentation than the rest and audited before publication: '
      '<a href="lumber-ports-sources.html">Lumber Ports</a> and '
      '<a href="lighthouses-sources.html">Lighthouses of California</a>. Where those pages '
      'and this one differ in detail, they are the authority for their own map.</p></div>')

    # ---- how to read ----
    A('<h2>How to read a citation on these maps</h2>')
    A('<p>A pin&#8217;s popup carries its own sources. Several conventions run across the site:</p>')
    A('<ul>')
    A('<li><strong>Coordinate precision is stated, not implied.</strong> A solid marker sits at a '
      'known place; a translucent or dashed marker is approximate within its district; a hollow '
      'marker is conjectural. Dashed route lines mean the party passed roughly this way.</li>')
    A('<li><strong>Manuscript citations give both page systems.</strong> A document in the Savage '
      'transcripts is cited to the original folio or page <em>and</em> to Savage&#8217;s own '
      'pagination and the scan leaf, because the three do not agree.</li>')
    A('<li><strong>Quoted matter is in quotation marks with a citation.</strong> Where a map '
      'paraphrases, it does not use the source&#8217;s wording. The site was audited for unquoted '
      'borrowing in September 2026 and the corrections applied.</li>')
    A('<li><strong>A missing source is shown, not hidden.</strong> Where no source was found for '
      'something, the popup says so rather than leaving a confident blank.</li>')
    A('<li><strong>Dates carry their grain.</strong> Some are exact to the day from a document; '
      'others are a year from the standard accounts, and say so.</li>')
    A('</ul>')

    # ---- which map uses what ----
    A('<h2>Which map uses what</h2>')
    A('<p>Principal sources per map. Ordered by kind first &#8212; manuscript, then printed '
      'primary, then data, then scholarship &#8212; and within a kind by how much of the map '
      'rests on it, so the list leads with the strongest evidence rather than the most '
      'frequently repeated. Every map&#8217;s full citation set lives in its own dataset, '
      'linked in the last column.</p>')
    A('<div class="tablewrap"><table class="srctable">')
    A('<thead><tr><th>Map</th><th class="num">Features</th><th>Principal sources</th>'
      '<th>Dataset</th></tr></thead><tbody>')
    for m in order:
        info = sets[m]
        # Rank by how much of the map rests on a source, but show the strongest KIND of
        # source first: an archival collection cited 20 times should not sit below a
        # fortification wiki cited 52 times.
        catrank = {c: i for i, (c, _, _) in enumerate(CATS)}
        ranked = sorted(m2w[m].items(),
                        key=lambda kv: (catrank.get(byk[kv[0]]["cat"], 9), -kv[1]))
        names = [SHORT[k] for k, _ in ranked[:6] if k in SHORT]
        page = MAP_PAGE.get(m)
        label = html.escape(info["title"], quote=False)
        if m in EXPERIMENTAL:
            label += ' <em>(comparison version)</em>'
        A(f'<tr><td><a href="{page}">{label}</a></td>'
          f'<td class="num">{info["n"]:,}</td>'
          f'<td>{" &#183; ".join(names)}</td>'
          f'<td><a href="../data/{m}.json">{m}.json</a>'
          + (f'<br><a href="{OWN_SOURCES_PAGE[m]}">full sources &#8594;</a>'
             if m in OWN_SOURCES_PAGE else '') + '</td></tr>')
    A('</tbody></table></div>')

    # ---- the works ----
    A('<h2>The sources</h2>')
    for cat, heading, blurb in CATS:
        items = [w for w in W if w["cat"] == cat and w2m.get(w["key"])]
        if not items:
            continue
        A(f'<h3>{heading}</h3>')
        A(f'<p>{blurb}</p>')
        A('<ul class="works">')
        for w in sorted(items, key=lambda x: -len(w2m[x["key"]])):
            used = sorted(w2m[w["key"]])
            links = ", ".join(
                f'<a href="{MAP_PAGE[u]}">{esc(sets[u]["title"])}</a>' for u in used if u in MAP_PAGE)
            A('<li>' + w["title"])
            if w.get("note"):
                A(f'<span class="caveat">{w["note"]}</span>')
            A(f'<span class="used"><strong>Used by:</strong> {links}</span></li>')
        A('</ul>')

    # ---- basemaps ----
    A('<h2>Basemaps</h2>')
    A('<p>The maps are drawn with <a href="https://leafletjs.com/">Leaflet</a> over Esri&#8217;s '
      'World Topographic and Ocean basemaps (&#169; Esri, HERE, Garmin, USGS, NGA, EPA, USDA, NPS, '
      'GEBCO, NOAA) and OpenStreetMap contributors. The basemap is a modern one in every case: no '
      'historical basemap underlies these pins, and modern coastlines, jetties and channels are '
      'not the ones the historical actors saw. Where that matters &#8212; a harbour entrance that '
      'has moved, a bar that has been dredged &#8212; the popup says so.</p>')

    # ---- companion projects ----
    A('<h2>Companion projects</h2>')
    A('<p>These maps are one of four related projects built on the same archive. Each is '
      'separately citable, and each is a source the others draw on.</p>')
    A('<ul class="works">')
    A('<li><a href="https://archivesofcalifornia.com"><strong>Archives of California: A '
      'Documentary Calendar of the Savage Transcripts</strong></a> &#8212; the item-level '
      'catalogue of BANC MSS C&#8211;A 1&#8211;63. The manuscript layer under most of what is '
      'on these maps; pins with a catalog record deep-link into it. '
      '<span class="used">DOI 10.5281/zenodo.21912644</span></li>')
    A('<li><a href="https://ranchos.archivesofcalifornia.com"><strong>Ranchos of Alta '
      'California</strong></a> &#8212; 672 land grants and claims with their adjudication, the '
      'families that held them, and the manuscript <em>dise&#241;os</em> filed as evidence. '
      '<span class="used">The rancho maps here use a different boundary dataset from the '
      'portal, which is why the two disagree; both are published rather than reconciled.</span></li>')
    A('<li><a href="https://ships.archivesofcalifornia.com"><strong>California Ship Registry'
      '</strong></a> &#8212; every recorded vessel visit to the California coast, 2,072 visits '
      'carrying 2,900 citations, from the documentary calendar, Bancroft\'s narrative and marine '
      'lists, and Ogden\'s otter-trade appendix. The maritime counterpart to the landward record '
      'on these maps, and the eighteenth- and early nineteenth-century precursor to the coastwise '
      'traffic on the lumber-ports and lighthouse maps.</li>')
    A('</ul>')

    # ---- limits ----
    A('<h2>What this page does not claim</h2>')
    A('<ul>')
    A('<li>It is a list of what the site draws on, not a bibliography of the field. Works read and '
      'not used are not here.</li>')
    A('<li>Grouped entries stand for families of citation. The exact citation for any single '
      'feature is in that feature&#8217;s popup and in the dataset, which is the authority.</li>')
    A('<li>Full bibliographic form is given where it is established in this site&#8217;s own '
      'audited apparatus or complete in the data. Where the data cites a work in short form, the '
      'short form is what appears here rather than an expansion that was never checked.</li>')
    A('<li>Coverage is uneven by design and by accident. Some maps rest on a long documented '
      'record; others rest on a thin one, and the thin ones say so on the map.</li>')
    A('</ul>')
    A('<p>Corrections are welcome and are logged on the <a href="../errata.html">errata page</a>.</p>')

    A('</main>\n</body>\n</html>')
    return "\n".join(P)


INDEX = ROOT / "index.html"
BEGIN = "<!-- SOURCES-SUMMARY:BEGIN generated by data-src/sources/build_sources.py -->"
END = "<!-- SOURCES-SUMMARY:END -->"


def index_summary(sets, w2m, m2w):
    """The short bibliography on the home page, generated so it cannot drift."""
    byk = {w["key"]: w for w in W}
    reach = collections.Counter()
    for k, maps in w2m.items():
        reach[k] = len(maps)
    lines = []
    A = lines.append
    A(BEGIN)
    A('      <p>The maps draw on roughly sixty distinct bodies of source material. What follows is '
      'the short form; the <a href="maps/sources.html"><strong>full source apparatus</strong></a> '
      'lists every one of them and says which map uses which, and each pin carries its own '
      'citation.</p>')
    for cat, heading, _ in CATS:
        items = [w for w in W if w["cat"] == cat and w2m.get(w["key"])]
        if not items:
            continue
        items.sort(key=lambda w: -reach[w["key"]])
        names = [SHORT[w["key"]] for w in items[:7] if w["key"] in SHORT]
        more = len(items) - len(names)
        label = heading.replace(" and ", " &amp; ")
        txt = " &#183; ".join(names)
        if more > 0:
            txt += f" &#183; and {more} more"
        A(f'      <p><strong>{label}.</strong> {txt}.</p>')
    A('      <p class="small"><a href="maps/sources.html">Sources &amp; Method &#8594;</a> &#183; '
      'per-map apparatus for <a href="maps/lumber-ports-sources.html">Lumber Ports</a> and '
      '<a href="maps/lighthouses-sources.html">Lighthouses</a>.</p>')
    A("    " + END)
    return "\n".join(lines)


def patch_index(summary):
    s = INDEX.read_text()
    if BEGIN in s and END in s:
        s = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), summary, s, flags=re.S)
    else:
        m = re.search(r"(<h2>Sources</h2>\s*<div class=\"prose\">)(.*?)(</div>)", s, re.S)
        if not m:
            print("  ! could not find the Sources block on index.html - left alone")
            return False
        s = s[:m.end(1)] + "\n      " + summary + "\n    " + s[m.start(3):]
    # nav link
    if 'href="maps/sources.html">Sources</a>' not in s:
        s = s.replace('<a href="#data">Data</a>',
                      '<a href="maps/sources.html">Sources</a>\n    <a href="#data">Data</a>', 1)
    INDEX.write_text(s)
    return True


def main():
    sets = collect()
    w2m, m2w, unmatched = match_works(sets)
    total = sum(sum(i["atoms"].values()) for i in sets.values())
    unm = sum(unmatched.values())
    matched_pct = 100.0 * (total - unm) / total if total else 0

    html_out = build(sets, w2m, m2w, unmatched, total)

    print(f"datasets          : {len(sets)}")
    print(f"citation atoms    : {total:,}")
    print(f"matched to a work : {total-unm:,}  ({matched_pct:.1f}%)")
    print(f"works cited       : {len(w2m)} of {len(W)} in the table")

    # ---- gates ----
    fail = []
    if matched_pct < 90:
        fail.append(f"only {matched_pct:.1f}% of citation atoms matched a work (want >=90%)")
    orphan = [w['key'] for w in W if not w2m.get(w['key'])]
    if orphan:
        fail.append("works in the table that nothing actually cites: " + ", ".join(orphan))
    noshort = [w["key"] for w in W if w["key"] not in SHORT]
    if noshort:
        fail.append("works with no SHORT form for the home page: " + ", ".join(noshort))
    nomap = [m for m in sets if not m2w.get(m)]
    if nomap:
        fail.append("datasets whose citations matched nothing: " + ", ".join(nomap))

    print("\ntop unmatched citation fragments:")
    for a, n in unmatched.most_common(12):
        print(f"  {n:5d}  {a[:110]}")

    if fail:
        print("\nGATE FAILED:")
        for f in fail:
            print("  -", f)
        sys.exit(1)

    OUT.write_text(html_out)
    print(f"\nwrote {OUT.relative_to(ROOT)}  ({len(html_out):,} bytes)")
    if patch_index(index_summary(sets, w2m, m2w)):
        print("wrote index.html  (Sources summary + nav link)")


if __name__ == "__main__":
    main()
