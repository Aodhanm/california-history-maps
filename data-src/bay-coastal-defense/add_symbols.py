#!/usr/bin/env python3
"""Give each work on the coastal-defence map the symbol of what it actually was.

Classification is by ARMAMENT, read from the record's own prose, not by guessing
from the feature id. An earlier pass keyed the casemate symbol off id patterns and
got it wrong in both directions: Townsley and Davis are genuinely 16-inch casemated
and were drawn as open gun batteries, while Batteries 243 and 244 are 6-inch and
were drawn as casemates.

Run: python3 data-src/bay-coastal-defense/add_symbols.py
"""
import json, re, pathlib, sys, collections

ROOT = pathlib.Path(__file__).resolve().parents[2]
F = ROOT / "data" / "bay-coastal-defense.json"

WORDS = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,
         "nine":9,"ten":10,"twelve":12,"sixteen":16,"twenty":20}
COUNT = re.compile(r"\b(\d{1,2}|" + "|".join(WORDS) + r")\s+(?:\d+(?:\.\d+)?-inch|\d+-pounder|\d+\s?mm|guns?\b|rifles?\b|mortars?\b|cannons?\b)", re.I)


def prose(f):
    return " ".join(str(f.get(k) or "") for k in ("summary", "notes", "result"))


def symbol_for(f):
    t, layer, fid, txt = f.get("type"), f.get("layer"), f["id"], prose(f)
    if t == "castillo":           return "castillo"
    if t == "presidio":           return "presidio"
    if t == "fort":               return "fort"
    if t == "nike":               return "nike"
    if t == "AA-battery":         return "aagun"
    if t == "mortar-battery":     return "mortar"
    if t == "underwater-defense": return "net" if "net" in fid else "mine"
    # A battery whose own guns sat in casemates gets the casemate symbol, whatever
    # its calibre or its id. Wallace was casemated in 1942-43 at 12-inch; Milagra's
    # 16-inch was designed casemated and never built, so it draws as a casemate and
    # the unbuilt flag renders it hollow.
    # Two things must NOT be caught: Fort Point is a casemated FORT, not a battery,
    # and Battery Baker's record mentions the mine casemate it stood in front of,
    # which is a different structure.
    if t != "fort":
        cm = re.sub(r"mine casemate\w*", "", txt, flags=re.I)
        if re.search(r"casemat", cm, re.I):
            return "casemate"
    if t == "unbuilt":            return "unbuilt"
    if t == "AMTB":               return "rifle"
    if layer in ("spanish", "mexican"):
        return "earthwork" if "earthwork" in fid else "cannon"
    if layer == "thirdsystem":    return "cannon"
    if layer in ("endicott", "wwii"): return "rifle"
    return "cannon"


def gun_count(f):
    best = 0
    for m in COUNT.finditer(prose(f)):
        tok = m.group(1).lower()
        n = WORDS.get(tok)
        if n is None:
            try: n = int(tok)
            except ValueError: continue
        if 1 <= n <= 24: best = max(best, n)
    return best or None


KEY = [
 ("cannon",   "Smoothbore on a carriage (Spanish, Mexican, Civil War)"),
 ("rifle",    "Rifled gun behind a parapet (Endicott, WWII, AMTB)"),
 ("mortar",   "Seacoast mortar battery"),
 ("casemate", "Casemated 16-inch battery"),
 ("aagun",    "Anti-aircraft battery"),
 ("nike",     "Nike missile site"),
 ("fort",     "Masonry fort"),
 ("castillo", "Spanish castillo or battery"),
 ("presidio", "Presidio (a garrison post, not a battery)"),
 ("mine",     "Submarine mine defence"),
 ("net",      "Anti-submarine net"),
 ("unbuilt",  "Projected but never built"),
]


# Positions corrected here so the fix survives a rebuild.
COORD_FIXES = {
 "mare-island-aa": {
   "coords": [38.0950, -122.2685],
   "precision": "conjectural",
   "why": ("The pin sat at 38.065,-122.253, which is open water in Carquinez Strait "
           "rather than the yard the guns defended. The 211th Coast Artillery's 90 mm "
           "guns were MOBILE, so no fixed emplacement exists to pin; the marker is "
           "placed on the Navy Yard at the south end of Mare Island and stays "
           "CONJECTURAL, which is what it is."),
 },
}


def main():
    d = json.loads(F.read_text())
    for fid, fx in COORD_FIXES.items():
        f = next((x for x in d["features"] if x["id"] == fid), None)
        if f is None:
            sys.exit(f"coord fix targets a feature that does not exist: {fid}")
        if f["coords"] != fx["coords"]:
            f["coords"] = fx["coords"]
            f["coord_precision"] = fx["precision"]
            note = f.get("notes") or ""
            if "open water in Carquinez" not in note:
                f["notes"] = (note + " " if note else "") + fx["why"]
            print(f"  moved {fid} -> {fx['coords']}")
    counts = collections.Counter()
    for f in d["features"]:
        sym = symbol_for(f)
        f["symbol"] = sym
        counts[sym] += 1
        n = gun_count(f)
        if n and sym in ("cannon", "rifle", "mortar"):
            f["symbol_count"] = min(n, 4)
            if n >= 4: f["symbol_major"] = True
        else:
            f.pop("symbol_count", None); f.pop("symbol_major", None)
        if f.get("type") == "unbuilt": f["unbuilt"] = True

    d["symbol_min_zoom"] = 11
    d["hover_labels"] = True
    d["symbol_key_title"] = "What the symbols mean"
    d["symbol_key"] = [{"symbol": s, "label": l} for s, l in KEY]

    # gate: every symbol used must exist in glyphs.js
    glyphs = (ROOT / "assets" / "js" / "glyphs.js").read_text()
    known = set(re.findall(r"^\s{4}([a-z]+):", glyphs[glyphs.index("var GLYPHS = {"):], re.M))
    missing = {s for s in counts if s not in known}
    if missing:
        sys.exit(f"symbols with no glyph: {missing}")

    F.write_text(json.dumps(d, ensure_ascii=False))
    print("features :", len(d["features"]))
    print("symbols  :", dict(counts))
    sixteen = [f["id"] for f in d["features"]
               if re.search(r"16-inch|16 inch", prose(f), re.I) and f.get("type") != "unbuilt"]
    print("16-inch works, all casemate:",
          all(next(x for x in d["features"] if x["id"] == i)["symbol"] == "casemate" for i in sixteen),
          sixteen)


if __name__ == "__main__":
    main()
