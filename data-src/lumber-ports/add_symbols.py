#!/usr/bin/env python3
"""Give each lumber port the symbol of how it actually loaded.

The map's point is that these places differed: a trough chute is not a wire chute
is not a pier is not a bar harbour. Colour alone could not carry that. The symbol
is read from the port's own class and prose, never guessed from its id.

Run: python3 data-src/lumber-ports/add_symbols.py
"""
import json, re, pathlib, sys, collections

ROOT = pathlib.Path(__file__).resolve().parents[2]
F = ROOT / "data" / "lumber-ports.json"

CLASS = {
    "chute-only doghole":      "chute",
    "doghole with pier":       "pier",
    "river bar harbor":        "riverbar",
    "deepwater / major wharf": "anchor",
}

WIRE = re.compile(r"wire[- ]chute|wire chute|high[- ]?line|trolley|cable chute", re.I)
# The data flags a chute that never loaded a stick as "NEVER ACTIVE". Match that
# and the explicit phrasings only: the records are full of other nevers (a mill
# that never ran, a tramway that never had a locomotive) which are not this.
NEVER = re.compile(r"NEVER ACTIVE|chute (?:was )?never (?:used|loaded)|built but never used", re.I)


def prose(f):
    txt = " ".join(str(f.get(k) or "") for k in ("summary", "notes"))
    for row in (f.get("facts") or []):
        if isinstance(row, (list, tuple)) and len(row) > 1:
            txt += " " + str(row[1])
    return txt


def symbol_for(f):
    t = f.get("type")
    if t == "shipyard":               return "shipyard"
    if t in ("mill", "feeder-mill"):  return "mill"
    if t == "lighthouse":             return "lighthouse"
    txt = prose(f)
    # a chute that was built and never loaded a stick is its own story
    if NEVER.search(txt):             return "ruin"
    sym = CLASS.get(f.get("port_class"))
    if sym == "chute" and WIRE.search(txt):
        return "wirechute"
    return sym or "anchor"


KEY = [
    ("chute",      "Doghole with a trough or apron chute"),
    ("wirechute",  "Doghole with a wire chute"),
    ("pier",       "Doghole with a pier"),
    ("riverbar",   "River-bar harbour"),
    ("anchor",     "Deepwater or major wharf port"),
    ("shipyard",   "Shipyard"),
    ("mill",       "Mill that shipped through another port"),
    ("lighthouse", "Lighthouse of the trade"),
    ("ruin",       "Built but never used"),
]


def main():
    d = json.loads(F.read_text())
    counts = collections.Counter()
    for f in d["features"]:
        s = symbol_for(f)
        f["symbol"] = s
        counts[s] += 1
        if f.get("port_class") == "deepwater / major wharf":
            f["symbol_major"] = True          # the big harbours hold their glyph when zoomed out
        else:
            f.pop("symbol_major", None)

    d["symbol_min_zoom"] = 8
    d["symbol_key_title"] = "What the symbols mean"
    d["symbol_key"] = [{"symbol": s, "label": l} for s, l in KEY]

    glyphs = (ROOT / "assets" / "js" / "glyphs.js").read_text()
    known = set(re.findall(r"^\s{4}([a-z]+):", glyphs[glyphs.index("var GLYPHS = {"):], re.M))
    missing = {s for s in counts if s not in known} | {s for s, _ in KEY if s not in known}
    if missing:
        sys.exit(f"symbols with no glyph: {missing}")

    F.write_text(json.dumps(d, ensure_ascii=False))
    print("features:", len(d["features"]))
    print("symbols :", dict(counts))
    for f in d["features"]:
        if f["symbol"] in ("wirechute", "ruin"):
            print(f"   {f['symbol']:10s} {f['name'][:52]}")


if __name__ == "__main__":
    main()
