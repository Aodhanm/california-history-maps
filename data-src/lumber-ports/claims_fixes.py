"""Corrections from the 2026-09-13 adversarial claims audit (5 agents, ~382 verdicts).

Applied by build_lumber_ports.py AFTER feature/route assembly, BEFORE output.
Every text op is STRICT: if the find-string is absent, the build fails — a fix
that silently misses is worse than no fix. Vault record: the audit ledger in
`Research Projects/lumber-ports/`; raw verdicts in data-src rigor/audit JSONs.
"""

# (feature_id, field, find, replace)   field: summary | notes | date_display
TEXT_FIXES = [
 ("needle-rock-landing", "summary", "half-way between Bear Harbor and Shelter Cove",
  "about 2 miles up the coast from Bear Harbor (Davidson 1889 places it 6¾ miles from Point Delgada, Bear Harbor 8⅔)"),
 ("bear-harbor-landing", "facts_any", "Weller & Stewart (1890-92)", "Weller & Stewart (1889-92)"),
 ("rockport-landing", "summary", "Finkbine-Guild Lumber Co. 1925-27", "Finkbine-Guild Lumber Co. 1924-27"),
 ("rockport-landing", "summary", "Rockport Redwood Co. chartered und", "Rockport Redwood Co. (from 1938, per the MPDF) chartered und"),
 ("kibesilah-landing", "summary", "grew to 20-30 buildings with three hotels and its own newspaper",
  "grew to 'a dozen or twenty buildings... two hotels, one store, one livery stable, and two saloons' (Palmer 1880)"),
 ("iversons-landing", "summary", "vessels of 100 tons lay stern-in 17 ft of water moored to the rocks",
  "vessels at the trapeze lay stern-to in 17 ft of water moored to the rocks, while the Rough and Ready point chute took vessels of 100 tons on six mooring-lines (Davidson 1889)"),
 ("newport-landing", "summary", "no spot on the coast demanded more shiphandling skill",
  "Davidson called it 'one of the most contracted anchorages' on the coast"),
 ("laguna-landing", "summary", "the Laguna mill closed November 1904, ending the port",
  "the Laguna mill closed November 1904; the landing itself saw residual use to c.1920 (MPDF; Borden gives 1923)"),
 ("noyo-landing", "summary", "Uniquely for this coast there was NO chute:",
  "No chute served the schooner era (a wire chute was added on the north point c.1900, active to the 1920s - MPDF):"),
 ("chisholm-landing", "date_display", "c.1870-1889", "c.1870 (chute already gone by 1889)"),
 ("greenwood-creek-landing", "summary", "By 1877-1889 a long wharf/chute complex",
  "By 1889 (built 1886-89 per the MPDF) a long wharf/chute complex"),
 ("gualala-landing", "summary", "the mill burned 14 September 1906", "the mill burned in 1906"),
 ("bihler-landing", "summary", "Ernest Rufus grant, 1845", "Ernest Rufus grant, 1846"),
 ("russian-gulch-landing-sonoma", "summary", "2 mooring buoys", "3 mooring buoys (Davidson 1889)"),
 ("fort-ross-landing", "summary", "shipwright Vasily Grudinin built the first ships constructed in California",
  "shipwright Vasily Grudinin built vessels here at what California State Parks calls the first shipbuilding yard in California"),
 ("walsh-landing", "summary", "Not among the 11 ports surveyed by NOAA/CSP in 2016",
  "Not among the doghole ports surveyed in the 2016 NOAA/CSP Sonoma project"),
 ("fort-bragg-landing", "summary", "after which Fort Bragg was the only coast mill with rail access to market",
  "after which Fort Bragg was the only Mendocino coast mill with a rail connection over the coast range (the CWR to Willits)"),
 # non-canonical slice
 ("mattole-wharf-sea-lion-rock", "sources", "pp. ~300-301 (page cite corrected in the 2026-09-13 audit)", "p. 308"),
 ("eureka-humboldt-bay", "facts_any", "shifting bar with 13-25 ft", "shifting bar with 12-24 ft at low water (Davidson 1889)"),
 ("samoa", "date_display", "Louisiana-Pacific after", "Georgia-Pacific 1956, Louisiana-Pacific after 1972-73"),
 ("samoa", "facts_any", "sold to Louisiana-Pacific 1956", "sold to Georgia-Pacific 1956 (Louisiana-Pacific took Samoa in the 1972-73 split)"),
 ("arcata-wharf", "facts_any", "to reach水deep water", "to reach deep water"),
 ("smith-river-mouth", "facts_any", "Smith River Mill 12 mi upstream", "Smith River Mill, 12 miles from Crescent City on the river"),
 ("a-o-nuevo-point-new-year-wharf-crescent-bay-cove-beach", "summary",
  "Davidson still records it in 1889 as a functioning coaster wharf",
  "Davidson's 1889 text carries the wharf over from earlier survey data - the wharf was in fact washed away by 1883 ('In 1883 we found the wharf washed away')"),
 ("san-simeon", "date_display", "whaling/landing 1850s-60s", "shore whaling 1852-1893; general landing"),
 ("usal", "summary", "Wikipedia's Lost Coast article credits Robert Dollar with building it in 1889, while other accounts have Dollar acquiring the works in 1894",
  "the Usal Redwood Co. built the mill, town, and 1,600-ft wharf in 1889; Robert Dollar took the operation over and started the mill up in 1893 per his own memoirs (some accounts say 1894), running it about six years"),
 ("bodega-bay", "summary", "Capt. Stephen Smith erected California's first steam saw- and grist-mill near Bodega in 1843",
  "Capt. Stephen Smith landed machinery in 1843 for California's first steam saw- and grist-mill near Bodega (in operation 1843/44; Bancroft and the MPDF say 1844)"),
 ("corte-madera-creek-landings-ross-landing-baltimore-wharf", "summary",
  "the Baltimore & Frederick company's 1849 steam mill (brought around Cape Horn)",
  "the Baltimore & Frederick company's Cape Horn machinery of 1849 (sold unrun to B.R. Buckelew in 1850, whose Baltimore Canyon mill cut the lumber)"),
 ("corte-madera-creek-landings-ross-landing-baltimore-wharf", "facts_any",
  "John T. Reed's water mill (1833-34, first in Marin - for the Presidio trade)",
  "John T. Reed's water mill (construction date disputed, c.1834-1843; the Presidio trade predates it - see the Reed's Sawmill feature)"),
 # context slice
 ("st-george-reef-lighthouse", "summary", "Built 1882-92", "Built 1883-92"),
 ("st-george-reef-lighthouse", "summary", "its granite quarried and finished on Humboldt Bay",
  "its granite quarried on the Mad River and finished at a depot on Humboldt Bay's north spit"),
 ("point-cabrillo-lighthouse", "summary", "built — in the station's own words — to protect the doghole schooners of the redwood trade",
  "built to protect the lumber fleet of the redwood trade (station history: 'a lighthouse was critical to the safety of the ships and their valuable cargo')"),
 ("point-arena-lighthouse", "summary", "sited after the surge of Mendocino-coast wrecks in the 1860s",
  "sited as redwood traffic and wrecks mounted along the Mendocino coast in the 1850s-60s"),
 ("bendixsen-shipyard-fairhaven", "date_display", "1875–c.1920", "1875-1901 (Bendixsen; successor yard to c.1920)"),
 ("peterson-shipyard-little-river", "date_display", "c.1868–1880s", "c.1868-1879"),
 ("howard-creek-feeder", "summary", "output moved by rail to Union Landing and by road to Westport",
  "output moved by rail to Union Landing and also shipped via Westport (MPDF)"),
 ("howard-creek-feeder", "summary", "Mills on Howard Creek (c.1903-1924)", "Mills on Howard Creek (c.1899-1920 per the MPDF)"),
 ("reeds-sawmill-mill-valley", "notes", "Full dossier in the project research files.",
  "Hoffman's land-case citation given as reported (case-number spelling pending verification against the Bancroft catalog). Full dossier in the project research files."),
]

# facts-row text fixes: (feature_id, find, replace) applied across facts values
FACTS_FIXES = [
 ("hardy-creek-landing", "wharf (per MCMRHS)", "590-ft wharf (R.A. Hardy, 1892, per MCMRHS) with a wire chute at its end"),
 ("union-landing", "W.P. McFaul", "C.A. (Charles Arthur) McFaul"),
 ("navarro-landing", "river-mouth wharf + moorings; bar-bound scow/schooner entry",
  "pier with a derrick at its end supporting two chutes, lumber brought by tramway (MPDF; Davidson 1889); bar-bound entry"),

 ("walsh-landing", "bluff loading (method — chute vs wire — not specified in sources located)",
  "single wire chute on the north side of Ocean Cove, installed 1900 by lessee Fred Linderman (MPDF)"),
 ("reeds-sawmill-mill-valley", "Land Case 183 ND", "Hoffman's Reports I:74 (case number as reported)"),
]

# company facet removals / renames: (feature_id, remove_value, add_value_or_None)
COMPANY_FIXES = [
 ("bear-harbor-landing", "L.E. White Lumber Co.", None),
 ("noyo-landing", "Richardson family (Stewarts Point)", "Capt. William A. Richardson"),
 ("albion-landing", "Richardson family (Stewarts Point)", "Capt. William A. Richardson"),
 ("hardy-creek-landing", None, "Hardy Creek Lumber Co."),
 ("saunders-landing", None, "A. Saunders (mill 1875); Nealon & Young"),
 ("new-haven-landing", None, "C.A. McFaul (1892)"),
 ("steens-landing", None, "L.B. Doe & Co. (mill 1883)"),
 ("walsh-landing", None, "Fred Linderman (lessee 1900)"),
]

# cargo facet fixes: (feature_id, remove_list, add_list)
CARGO_FIXES = [
 ("hardy-creek-landing", [], ["railroad ties", "tanbark", "posts & split stuff"]),
 ("bridgeport-landing", [], ["farm produce"]),
 ("new-haven-landing", ["redwood lumber"], ["tanbark", "railroad ties", "posts & split stuff"]),
 ("nip-and-tuck-landing", ["redwood lumber"], ["railroad ties", "posts & split stuff", "tanbark", "cordwood & firewood"]),
 ("del-mar-landing", [], ["railroad ties", "posts & split stuff", "cordwood & firewood"]),
 ("shelter-cove", ["redwood lumber"], []),
 ("mattole-wharf-sea-lion-rock", ["redwood lumber"], ["tanbark"]),
 ("klamath-river-mouth-requa", ["redwood lumber"], []),
]

# notes to append (unverified-flagging the audit demanded): (feature_id, text)
NOTE_APPENDS = [
 ("rockport-landing", "Audit 2026-09-13: the David-and-Edward machinery-landing anecdote and the 'Southern Redwood 1928-29' span are re-sourcing tasks; Rockport Redwood Co. from 1938 (MPDF; the Dusenbury attribution is unsourced)."),
 ("caspar-landing", "Audit: the Krebs succession and the 'longest-lived family firm' superlative are not in the located sources; treat as local tradition pending a Kelley House citation."),
 ("timber-cove-landing", "Active-from c.1856 per NOAA settlement history; the MPDF's canonical span opens 1860 (chute built by Benitz in the 1860s)."),
 ("duncans-landing", "The Duncans' mill dates from 1860; the MPDF's canonical LANDING span opens with the 1876 T-sheet chutes."),
 ("salt-point-landing", "The 1853 Hendy-Duncan mill predates the doghole landing; the MPDF's canonical span is 1870-1917 (Funcke & Gerstle era)."),
 ("eureka-humboldt-bay", "Audit: Vance chronology corrected (John Vance died 1892; his heirs built the Samoa mill 1893); Eureka & Klamath River RR incorporated 1896; the Humboldt Northern claim awaits a rail-history citation."),
 ("samoa", "Audit: Hammond's Vance purchase closed 30 Aug 1900 (about $1 million as reported); mill built 1893, first-lumber and capacity figures unverified."),
 ("arcata-wharf", "Audit: wharf chronology (Jan/May 1855, 1875 extension) and length (sources range 1.5-2 miles with the plank walk) rest on local-history pages; corporate name = Union Plank Walk, Rail Track and Wharf Co. (inc. 15 Dec 1854); A&MR incorporated July 1881 (sources differ 16 vs 22)."),
 ("crescent-city", "Audit: the May-1903 first-locomotive date and the modern breakwater dimensions are unverified pending DNCHS/USACE sources."),
 ("bolinas", "Audit: the 25-million-board-feet total is local-history tradition (Bolinas Museum lineage), not a period figure."),
 ("santa-cruz-wharves", "Audit: Loma Prieta figures need re-sourcing (founded 1882, mill opened spring 1884, ~70,000 bf/day per santacruztrains); the 140,000 bf/day and 1923 end-date are unconfirmed."),
 ("davenport-landing", "Audit: wharf length 400-450 ft (sources differ), built c.1867-68; silted and defunct by the 1880s."),
 ("pigeon-point-gazos-creek-traffic", "Audit: the 1860 boom-and-cable and early-1870s wharf/chute dates await Stanger page cites; the Gazos flume detail is unverified. The Gazos operator was Pacific Lumber & MILL Co. - unrelated to Scotia's Pacific Lumber Co."),
 ("san-francisco-lumber-wharves-and-yards-the-receiving-end", "Audit: the finger-pier and open-wharf descriptions and the 1855 Mission Creek date are FoundSF-derived and await re-verification."),
 ("oakland-estuary-lumber-yards", "Audit: the 1891 arrival and yard list are LocalWiki-derived, unverified; the pin sits at the 1949 office address (727 Kennedy St) - the historic yard was at King & Frederick Sts."),
 ("trinidad", "Audit: the 1850s lumber-to-San-Francisco and early-1900s whaling-pier claims are unfootnoted local history."),
 ("fields-landing", "Audit: the 1884 spur date awaits Stindt; the WWII British-tugs claim is HCHS-cited but unverified."),
 ("bucksport", "Audit: Davidson's ten-foot/northward description dates to the 1889 edition (1886 conditions); the preserved-Falk-locomotive claim awaits a live THA citation."),
 ("shelter-cove", "Audit: lumber export is not documented for the pier; wool, produce, and tanbark are the attested cargoes."),
 ("klamath-river-mouth-requa", "Audit: the rafting cargo was cedar logs/timber, not sawn redwood."),
]

# company facet rename on pigeon point (unrelated firms with near-identical names)
COMPANY_FIXES.append(("pigeon-point-gazos-creek-traffic", "Pacific Lumber Co.", "Pacific Lumber & Mill Co. (Gazos)"))

# route/stop text fixes: (route_id_prefix, where: label|notes|stop, find, replace)
ROUTE_FIXES = [
 ("bear-harbor-eel-river", "stopnotes", "Rohde NCJ", "NCJ (byline correction per audit: Evans)"),
 ("caspar-south-fork-eastern", "stop", "1884 160-ft trestle", "1884 trestle, 1,000 ft long and 160 ft high"),
 ("albion-lumber-co-line", "label", "standard (4 ft 8.5 in)", "40-in narrow gauge 1881-c.1902; standard after the A&SE rebuild"),
 ("glen-blair-branch", "stopdate", "Track laid 1885 (first CWR-system rails)",
  "First Fort Bragg RR rails 1885; rails reached the Glen Blair mill 1887"),
 ("humboldt-bay-eel-river", "label", "became part of the NWP main li",
  "into the NWP system 1907; through main line opened 1914"),

]


def apply(features, unlocated, routes, data):
    """Strict application; raises SystemExit on any miss."""
    import sys
    by_id = {f["id"]: f for f in features}
    for u in unlocated:
        by_id.setdefault(u["id"], u)
    misses = []

    for fid, field, find, repl in TEXT_FIXES:
        f = by_id.get(fid)
        if f is None:
            misses.append((fid, field, "NO FEATURE")); continue
        if field == "date_display":
            disp = f["date"]["display"]
            done = False
            for probe in {find, find.replace("–", "-"), find.replace("-", "–")}:
                if probe in disp:
                    f["date"]["display"] = disp.replace(probe, repl); done = True; break
            if not done:
                misses.append((fid, field, find[:60]))
            continue
        if field == "facts_any":
            hit = False
            for row in f.get("facts", []):
                if find in row[1]:
                    row[1] = row[1].replace(find, repl); hit = True
            if not hit:
                misses.append((fid, field, find[:60]))
            continue
        if field == "sources":
            hit = False
            for src in f.get("sources", []):
                if find in src["citation"]:
                    src["citation"] = src["citation"].replace(find, repl); hit = True
            if not hit:
                misses.append((fid, field, find[:60]))
            continue
        tgt = f.get(field, "") or ""
        if find in tgt:
            f[field] = tgt.replace(find, repl)
        else:
            misses.append((fid, field, find[:60]))

    for fid, find, repl in FACTS_FIXES:
        f = by_id.get(fid)
        hit = False
        for row in (f or {}).get("facts", []):
            if find in row[1]:
                row[1] = row[1].replace(find, repl); hit = True
        if not hit:
            misses.append((fid, "facts", find[:60]))

    for fid, remove, add in COMPANY_FIXES:
        f = by_id.get(fid)
        if f is None:
            misses.append((fid, "company", "NO FEATURE")); continue
        comp = f.get("company", [])
        if remove is not None and remove in comp:
            comp.remove(remove)
        if add and add not in comp:
            comp.append(add)
        f["company"] = comp

    for fid, removes, adds in CARGO_FIXES:
        f = by_id.get(fid)
        if f is None:
            misses.append((fid, "cargo", "NO FEATURE")); continue
        cg = f.get("cargo", [])
        for r in removes:
            if r in cg:
                cg.remove(r)
        for a in adds:
            if a not in cg:
                cg.append(a)
        f["cargo"] = cg

    for fid, text in NOTE_APPENDS:
        f = by_id.get(fid)
        if f is None:
            misses.append((fid, "note", "NO FEATURE")); continue
        f["notes"] = (f.get("notes", "") + " " + text).strip()

    for rid_prefix, where, find, repl in ROUTE_FIXES:
        hit = False
        for r in routes:
            if not r["id"].startswith(rid_prefix):
                continue
            if where == "label" and find in r["label"]:
                r["label"] = r["label"].replace(find, repl); hit = True
            elif where == "notes" and find in r.get("notes", ""):
                r["notes"] = r["notes"].replace(find, repl); hit = True
            elif where == "stop":
                for st in r["stops"]:
                    if find in st["name"]:
                        st["name"] = st["name"].replace(find, repl); hit = True
            elif where == "stopnotes":
                for st in r["stops"]:
                    if find in st.get("notes", ""):
                        st["notes"] = st["notes"].replace(find, repl); hit = True
            elif where == "stopdate":
                for st in r["stops"]:
                    if find in st["date"]["display"]:
                        st["date"]["display"] = st["date"]["display"].replace(find, repl); hit = True
        if not hit:
            misses.append((rid_prefix, where, find[:60]))

    # abstract: periodization is editorial, not sourced
    data["abstract"] = data["abstract"].replace(
        "era buttons snap the timeline to the trade's four periods",
        "era buttons snap the timeline to four editorial periods of the trade")

    if misses:
        for m in misses:
            print("CLAIMS-FIX MISS:", m, file=sys.stderr)
        sys.exit(f"claims_fixes: {len(misses)} operations failed to apply")
    return len(TEXT_FIXES) + len(FACTS_FIXES) + len(COMPANY_FIXES) + len(CARGO_FIXES) + len(NOTE_APPENDS) + len(ROUTE_FIXES) + 1
