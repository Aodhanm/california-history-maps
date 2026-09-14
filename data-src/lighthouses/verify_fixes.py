"""Corrections from the pre-publish verification pass, 2026-09-14.

An independent adversarial agent audited all 48 features (~310 assertions) against
the NRHP files, the USCG Historian's records, the Coast Pilots, and the Light-House
Board passages the popups themselves quote. 18 corrections and 7 unsupported claims
came back. They are applied here STRICTLY: any find-string that fails to match fails
the build, because a correction that silently misses is worse than none.

The four coordinate corrections are the important ones. Two PUBLISHED Coast and
Geodetic Survey positions existed for stations this project had treated as
unlocatable, and one derived pin was 1.4 km wrong. Both published positions were
re-verified against the Coast Pilot's own text before being adopted here.
"""
import math, sys

# ---- coordinate corrections (verified independently against Davidson 1889) ----
# Mare Island: "Latitude 38 deg 04' 19" north; Longitude 122 deg 15' 16" west"
#   — USC&GS Pacific Coast Pilot, 4th ed. (1889), p. 240.
MARE_ISLAND_PUBLISHED = [38 + 4/60 + 19/3600, -(122 + 15/60 + 16/3600)]
# Humboldt Harbor: "Latitude 40 deg 46' 01" north; Longitude 124 deg 13' 14" west"
#   — same volume, p. 325.
HUMBOLDT_PUBLISHED = [40 + 46/60 + 1/3600, -(124 + 13/60 + 14/3600)]

def offset(lat, lon, metres, bearing_deg):
    b = math.radians(bearing_deg)
    return [round(lat + metres * math.cos(b) / 111320.0, 5),
            round(lon + metres * math.sin(b) / (111320.0 * math.cos(math.radians(lat))), 5)]

# Carquinez hangs off Mare Island by the 1910 Notice's bearing and distance, so it
# moves with the corrected anchor.
CARQUINEZ_REDERIVED = offset(MARE_ISLAND_PUBLISHED[0], MARE_ISLAND_PUBLISHED[1], 905, 106.5)

COORD_FIXES = {
 "mare-island-light": {
   "coords": [round(MARE_ISLAND_PUBLISHED[0], 5), round(MARE_ISLAND_PUBLISHED[1], 5)],
   "precision": "exact",
   "note": ("Position PUBLISHED, not derived: the Coast and Geodetic Survey fixed this light at "
            "latitude 38° 04′ 19″ north, longitude 122° 15′ 16″ west (USC&GS Pacific Coast Pilot, "
            "4th ed., 1889, p. 240). That volume also settles where the station stood, describing it "
            "in its words: \"a Light-house has been established on the extreme southeastern part of Mare "
            "Island\" — which reconciles the "
            "Light-House Board's own inconsistency between the \"southern end\" it ordered in 1872 and "
            "the \"extreme eastern end\" its 1874 list printed. An earlier version of this map estimated "
            "the position and placed it about 300 m away; the published fix supersedes that estimate."),
 },
 "carquinez-strait-light": {
   "coords": CARQUINEZ_REDERIVED,
   "precision": "area",
   "note": ("Position DERIVED from the Notice to Mariners of January 1910, which placed the new station "
            "\"about 9/16 mile 106 degrees 30 minutes true from Mare Island lighthouse\" — that bearing "
            "and distance are applied here to the published Coast and Geodetic Survey position of the "
            "Mare Island light. Expect ±400 m, with a further ±140 m because the notice does not say "
            "whether its miles are statute or nautical. The building itself survives, moved: barged to "
            "Glen Cove in 1955, where it serves as a marina office."),
 },
 "humboldt-harbor-light-1856": {
   "coords": [round(HUMBOLDT_PUBLISHED[0], 5), round(HUMBOLDT_PUBLISHED[1], 5)],
   "precision": "place",
   "note": ("Position PUBLISHED, not derived: \"Its geographical position, as determined by the U.S. "
            "Coast and Geodetic Survey, is: Latitude 40° 46′ 01″ north, Longitude 124° 13′ 14″ west\" "
            "(USC&GS Pacific Coast Pilot, 4th ed., 1889, p. 325). An earlier version of this map "
            "estimated the site by measuring north from the modern jettied entrance and landed about "
            "1.4 km too far north — the 1889 \"entrance to the bay\" was not today's. The Board's 1858 "
            "printed light list gives a slightly different longitude (124° 12′ 21″ W)."),
 },
 "oakland-harbor-light": {
   "coords": None,      # unchanged
   "precision": "area",
   "note": ("Position NOT ESTABLISHED. No published latitude and longitude for either the 1890 or the "
            "1903 structure was found; the 1889 Coast Pilot predates the station and the 1943 edition "
            "gives none. What the record does say is that the station stood on eleven piles off the end "
            "of the northern training wall, the two walls spaced 750 feet apart and running some two "
            "miles into the bay. This pin marks that approach, and should be read as an area with an "
            "uncertainty of about 1.5 km — an earlier version of this map cited a modern channel buoy "
            "as its anchor, which does not in fact produce this position. The 1903 building survives, "
            "moved about six miles to Embarcadero Cove."),
 },
}

# ---- text corrections: (feature id, field, find, replace) ----
# field: summary | notes | date_display | facts:<label prefix>
TEXT_FIXES = [
 # self-contradiction: the popup quotes the Board giving the day, then calls the day tertiary
 ("st-george-reef-light-station", "date_display",
  "First-order lens installed August 1892",
  "First exhibited 20 October 1892"),
 ("st-george-reef-light-station", "facts:First lit",
  "The commonly cited day, 20 October 1892, is tertiary-level only in this survey.",
  "The Board's report for 1893 (p. 167) describes the lens reaching the station in August and the "
  "light going into service that October; 20 October 1892 is the day given in the lighthouse literature."),
 ("trinidad-head-light-station", "facts:First lit",
  "the customary day, 1 December 1871, is tertiary-level in this survey)",
  "and the Board's own report for 1872 (p. 547) dates the first lighting to the night of "
  "1 December 1871)"),
 ("table-bluff-light-station", "facts:First lit",
  "The customary day, 31 October 1892, is tertiary-level only",
  "The day, 31 October 1892, follows the Board's report for 1893"),
 ("farallon-islands-light-southeast-farallon", "facts:First lit",
  "frequently cited first exhibition of the first-order lens on 1 January 1856 is tertiary-level in this survey",
  "tower was well advanced in October 1855 (Bache to the Board, Annual Report 1855, appendix 25) and "
  "the first-order lens was first exhibited on 1 January 1856 in the standard accounts"),
 ("point-arguello-light-station", "facts:First lit",
  "The customary day, 1 March 1901, is tertiary-level in this survey",
  "The Board's own list of new lights for 1901 (p. 11) records a fourth-order light established "
  "22 February 1901"),
 ("roe-island-light", "facts:Optic",
  "Lens type not established from located sources (lantern-room fixed/flashing apparatus; USCG Historian's lens field is blank) - unverified.",
  "Fifth-order Fresnel, fixed white, 1891 — the Board's report for that year (p. 158) records a fixed "
  "white light exhibited when the station went into operation; the later flashing characteristic in the "
  "Coast Guard's records reflects a subsequent change, not the original apparatus."),
 ("blunts-reef-lightship-station", "facts:First lit",
  "the LV-83 vessel page says the ship was 'placed on Blunts Reef (CA) off Cape Mendocino' in 1906 - discrepancy noted",
  "Light-Vessel No. 83 took station off Blunts Reef on 28 June 1905, per the Twelfth District report "
  "for that fiscal year"),
 ("yerba-buena-island-light-and-12th-district-lighthouse-depot", "facts:NRHP",
  "No individual listing verified this session.",
  "Listed 3 September 1991, reference 91001096, under the Light Stations of California multiple-property "
  "submission (as Yerba Buena Island Lighthouse; also Goat Island Lighthouse)."),
 # superlatives: attribute or soften
 ("st-george-reef-light-station", "summary",
  "The most expensive American lighthouse of its century,",
  "Long described in the lighthouse literature as the most expensive American lighthouse ever built,"),
 ("point-arena-light-station", "summary",
  "the first concrete lighthouse in the country and the model for many later towers",
  "the first reinforced-concrete lighthouse in California, per its National Register nomination"),
 ("point-blunt-light", "facts:Automated",
  "; last of the bay's staffed light stations)",
  "; the last manned lighthouse BUILT in California, though Point Bonita kept its keepers five years longer)"),
 ("mile-rocks-light", "facts:Why built",
  "- the worst shipwreck at the Golden Gate",
  "— usually described as the deadliest wreck in San Francisco Bay's history"),
 ("roe-island-light", "summary",
  "The delta's only true staffed lighthouse",
  "The only staffed light station east of Carquinez Strait"),
 ("anacapa-island-light-station", "summary",
  "the final full station of its kind on this coast",
  "the last full residential light station built on the California coast"),
 # keeper claims
 ("mare-island-light", "facts:Keeper",
  "meaning women kept this light for its entire 44-year staffed life",
  "meaning every head keeper from 1873 to May 1917 was a woman; a man, Angus Murray, tended the light "
  "only through its last weeks before discontinuance"),
 ("santa-cruz-light-station", "facts:Keeper",
  "served until 1916 - a 33-year tenure",
  "served until her retirement in 1916 or 1917 (the Coast Guard's station page and its women-keepers "
  "list disagree) — a tenure of 33 or 34 years"),
 # measurement per the Board's own figure
 ("trinidad-head-light-station", "summary",
  "whose modest 20-foot height",
  "whose modest height — 18 feet from ground line to focal plane, in the Board's own figure —"),
]

# Point Bonita's fog-gun date is genuinely contested between its own sources.
BONITA_FIND = "an army 24-pounder cannon fired from August 8, 1855"
BONITA_REPL = ("an army 24-pounder cannon; the Lighthouse Service's own later account dates the first "
               "firing to August 1855, while the Board's 1874 fog-signal appendix says the notice took "
               "effect 8 August 1856 — the sources conflict")

def apply(features, ar_cite_fixer=None):
    import sys
    by = {f["id"]: f for f in features}
    misses = []

    for fid, spec in COORD_FIXES.items():
        f = by.get(fid)
        if f is None:
            misses.append((fid, "NO FEATURE")); continue
        if spec["coords"]:
            f["coords"] = spec["coords"]
        f["coord_precision"] = spec["precision"]
        # replace the old derivation note, keeping anything appended after it
        old_note = f.get("notes", "")
        tail = ""
        for marker in ("Also known as:", "⚠ Corrected here"):
            i = old_note.find(marker)
            if i >= 0:
                tail = " " + old_note[i:]
                break
        f["notes"] = spec["note"] + tail

    for fid, field, find, repl in TEXT_FIXES:
        f = by.get(fid)
        if f is None:
            misses.append((fid, field, "NO FEATURE")); continue
        if field == "date_display":
            if find in f["date"]["display"]:
                f["date"]["display"] = f["date"]["display"].replace(find, repl)
            else:
                misses.append((fid, field, find[:55]))
        elif field.startswith("facts:"):
            lab = field.split(":", 1)[1]
            hit = False
            for row in f.get("facts", []):
                if row[0] == lab and find in row[1]:
                    row[1] = row[1].replace(find, repl); hit = True
            if not hit:
                misses.append((fid, field, find[:55]))
        else:
            if find in f.get(field, ""):
                f[field] = f[field].replace(find, repl)
            else:
                misses.append((fid, field, find[:55]))

    # Point Bonita: the phrase may sit in summary or a facts row
    fb = by.get("point-bonita-light")
    if fb:
        hit = False
        if BONITA_FIND in fb.get("summary", ""):
            fb["summary"] = fb["summary"].replace(BONITA_FIND, BONITA_REPL); hit = True
        for row in fb.get("facts", []):
            if BONITA_FIND in row[1]:
                row[1] = row[1].replace(BONITA_FIND, BONITA_REPL); hit = True
        if not hit:
            misses.append(("point-bonita-light", "fog-gun", BONITA_FIND[:55]))

    if misses:
        for m in misses:
            print("VERIFY-FIX MISS:", m, file=sys.stderr)
        sys.exit(f"verify_fixes: {len(misses)} operations failed to apply")
    return len(COORD_FIXES) + len(TEXT_FIXES) + 1
