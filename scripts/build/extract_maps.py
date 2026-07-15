#!/usr/bin/env python3
# ARCHIVAL/one-time or session-built script, kept for provenance and reproducibility.
# Paths referencing the original session scratchpad will need adjusting to rerun.
"""Phase 0 extractor: pull feature data out of the four legacy map HTML files.

Outputs draft JSONs (one per map) + a count report. Draft schema is loose at
this stage — Phase 1 verification will normalize into the final schema.
"""
import json, re, sys, os

REPO = os.path.expanduser("~/california-history-maps")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extracted")
os.makedirs(OUT, exist_ok=True)


def read(fn):
    with open(os.path.join(REPO, fn), encoding="utf-8") as f:
        return f.read()


# ---------- JS call parsing (string-aware, balanced parens) ----------

def find_calls(src, fname):
    """Yield the raw argument strings of every fname(...) call."""
    out = []
    i = 0
    needle = fname + "("
    while True:
        j = src.find(needle, i)
        if j < 0:
            break
        # skip the function definition itself
        prefix = src[max(0, j - 20):j]
        if re.search(r"function\s+$", prefix):
            i = j + len(needle)
            continue
        k = j + len(needle)
        depth = 1
        instr = None  # quote char
        esc = False
        start = k
        while k < len(src) and depth > 0:
            c = src[k]
            if esc:
                esc = False
            elif instr:
                if c == "\\":
                    esc = True
                elif c == instr:
                    instr = None
            elif c in "'\"`":
                instr = c
            elif c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
            k += 1
        out.append(src[start:k - 1])
        i = k
    return out


def split_args(argstr):
    """Split a JS argument string on top-level commas."""
    args, depth, instr, esc, cur = [], 0, None, False, []
    for c in argstr:
        if esc:
            esc = False
            cur.append(c)
            continue
        if instr:
            if c == "\\":
                esc = True
            elif c == instr:
                instr = None
            cur.append(c)
            continue
        if c in "'\"`":
            instr = c
            cur.append(c)
        elif c in "([{":
            depth += 1
            cur.append(c)
        elif c in ")]}":
            depth -= 1
            cur.append(c)
        elif c == "," and depth == 0:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(c)
    if cur:
        args.append("".join(cur).strip())
    return args


def js_str(tok):
    """Decode a JS string literal (possibly 'a'+'b' concatenation)."""
    tok = tok.strip()
    if not tok or tok[0] not in "'\"`":
        return tok  # not a string literal — return raw (identifier/number)
    # handle concatenations conservatively: decode each literal piece
    pieces = re.findall(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"", tok)
    s = "".join(a or b for a, b in pieces)
    return (s.replace("\\'", "'").replace('\\"', '"')
             .replace("\\n", "\n").replace("\\\\", "\\"))


# ---------- JS object-array parsing ----------

def parse_const_array(src, name):
    m = re.search(r"const\s+" + re.escape(name) + r"\s*=\s*\[", src)
    if not m:
        return None
    k = m.end() - 1
    depth = 0
    instr = None
    esc = False
    start = k
    while k < len(src):
        c = src[k]
        if esc:
            esc = False
        elif instr:
            if c == "\\":
                esc = True
            elif c == instr:
                instr = None
        elif c in "'\"":
            instr = c
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                k += 1
                break
        k += 1
    raw = src[start:k]
    # strip // line comments (string-aware)
    lines = []
    for line in raw.split("\n"):
        instr2 = None
        esc2 = False
        cut = len(line)
        for idx, c in enumerate(line):
            if esc2:
                esc2 = False
            elif instr2:
                if c == "\\":
                    esc2 = True
                elif c == instr2:
                    instr2 = None
            elif c in "'\"":
                instr2 = c
            elif c == "/" and idx + 1 < len(line) and line[idx + 1] == "/":
                cut = idx
                break
        lines.append(line[:cut])
    raw = "\n".join(lines)
    # single->double quoted strings, string-aware char walk
    out2 = []
    i2 = 0
    while i2 < len(raw):
        c = raw[i2]
        if c == '"':  # copy double-quoted string verbatim
            j2 = i2 + 1
            while j2 < len(raw):
                if raw[j2] == "\\":
                    j2 += 2
                    continue
                if raw[j2] == '"':
                    break
                j2 += 1
            out2.append(raw[i2:j2 + 1])
            i2 = j2 + 1
        elif c == "'":  # convert single-quoted string
            j2 = i2 + 1
            buf = []
            while j2 < len(raw):
                if raw[j2] == "\\":
                    buf.append(raw[j2 + 1] if raw[j2 + 1] != "'" else "'")
                    if raw[j2 + 1] != "'":
                        buf.insert(-1, "\\")
                    j2 += 2
                    continue
                if raw[j2] == "'":
                    break
                buf.append('\\"' if raw[j2] == '"' else raw[j2])
                j2 += 1
            out2.append('"' + "".join(buf) + '"')
            i2 = j2 + 1
        else:
            out2.append(c)
            i2 += 1
    txt = "".join(out2)
    # quote bare keys + kill trailing commas (string-aware enough now:
    # keys only occur after { or , outside strings — strings already normalized,
    # so guard with a tokenizer-free heuristic applied outside quotes)
    parts = re.split(r'("(?:[^"\\]|\\.)*")', txt)
    for pi in range(0, len(parts), 2):  # even indexes = outside strings
        parts[pi] = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', parts[pi])
        parts[pi] = re.sub(r",\s*([\]}])", r"\1", parts[pi])
    txt = "".join(parts)
    return json.loads(txt)


def parse_coord_arrays(src):
    """Find const NAME=[ [lat,lng], ... ] pure-coordinate arrays."""
    out = {}
    for m in re.finditer(r"const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\[\s*\[", src):
        name = m.group(1)
        arr = parse_const_array(src, name)
        if arr and all(isinstance(x, list) and len(x) == 2 and
                       all(isinstance(v, (int, float)) for v in x) for x in arr):
            out[name] = arr
    return out


def num(tok):
    try:
        return float(tok)
    except ValueError:
        return None


report = {}

# ── 1. military battles ──────────────────────────────────────────
src = read("california-military-battles.html")
feats = []
for call in find_calls(src, "addBattle"):
    a = split_args(call)
    if len(a) != 11:
        print(f"WARN military: {len(a)} args: {a[0][:40]}", file=sys.stderr)
        continue
    feats.append({
        "layer_var": a[0], "type_group": a[1],
        "coords": [num(a[2]), num(a[3])], "icon_raw": a[4],
        "name": js_str(a[5]), "date_display": js_str(a[6]),
        "summary": js_str(a[7]), "result": js_str(a[8]),
        "quote_raw": js_str(a[9]), "source_raw": js_str(a[10]),
    })
json.dump({"map": "military-engagements", "features": feats},
          open(f"{OUT}/military-engagements.draft.json", "w"), indent=1, ensure_ascii=False)
report["military addBattle"] = len(feats)

# ── 2. borderlands ────────────────────────────────────────────────
src = read("borderlands-imperial-frontier.html")
feats = []
for call in find_calls(src, "addM"):
    a = split_args(call)
    if len(a) != 10:
        print(f"WARN borderlands: {len(a)} args: {a[0][:40]}", file=sys.stderr)
        continue
    feats.append({
        "layer_var": a[0], "coords": [num(a[1]), num(a[2])], "icon_raw": a[3],
        "name": js_str(a[4]), "date_display": js_str(a[5]),
        "summary": js_str(a[6]), "result": js_str(a[7]),
        "quote_raw": js_str(a[8]), "source_raw": js_str(a[9]),
    })
arrays = {n: parse_const_array(src, n) for n in ("presidios", "missions", "pueblos")}
json.dump({"map": "borderlands-frontier", "features": feats, "site_arrays": arrays},
          open(f"{OUT}/borderlands-frontier.draft.json", "w"), indent=1, ensure_ascii=False)
report["borderlands addM"] = len(feats)
report["borderlands site arrays"] = {k: len(v or []) for k, v in arrays.items()}

# ── 3. moraga master ─────────────────────────────────────────────
src = read("moraga-expeditions-master.html")
obj_arrays = {}
for m in re.finditer(r"const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\[\s*\n?\s*\{", src):
    n = m.group(1)
    obj_arrays[n] = parse_const_array(src, n)
coords = parse_coord_arrays(src)
json.dump({"map": "moraga-expeditions", "object_arrays": obj_arrays, "routes": coords},
          open(f"{OUT}/moraga-expeditions.draft.json", "w"), indent=1, ensure_ascii=False)
report["moraga master arrays"] = {k: len(v or []) for k, v in obj_arrays.items()}
report["moraga master routes"] = {k: len(v) for k, v in coords.items()}

# ── 4. zalvidea-moraga 1806 ──────────────────────────────────────
src = read("zalvidea-moraga-1806.html")
obj_arrays = {}
for n in ("missions", "zalvideaStops", "moragaNorthStops", "moragaSouthStops",
          "villages", "modernLabels"):
    obj_arrays[n] = parse_const_array(src, n)
coords = parse_coord_arrays(src)
json.dump({"map": "zalvidea-moraga-1806", "object_arrays": obj_arrays, "routes": coords},
          open(f"{OUT}/zalvidea-moraga-1806.draft.json", "w"), indent=1, ensure_ascii=False)
report["zalvidea arrays"] = {k: len(v or []) for k, v in obj_arrays.items()}
report["zalvidea routes"] = {k: len(v) for k, v in coords.items()}

print(json.dumps(report, indent=1))
