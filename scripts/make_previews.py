#!/usr/bin/env python3
"""Generate landing-card preview images (assets/previews/{id}.jpg) from data/*.json.
Draws each map's own features in its layer colors over a faint state silhouette
(taken from the native-california polygons). Rerun after data changes."""
import json, glob, os
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "previews")
os.makedirs(OUT, exist_ok=True)

W, H = 900, 450
PARCHMENT = (247, 243, 236)
SILH = (222, 214, 198)

# geographic frame (whole area of interest)
LAT0, LAT1 = 31.8, 42.2
LNG0, LNG1 = -125.2, -113.8

def xy(lat, lng):
    x = (lng - LNG0) / (LNG1 - LNG0) * W
    y = (LAT1 - lat) / (LAT1 - LAT0) * H
    return x, y

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

native = json.load(open(os.path.join(ROOT, "data", "native-california.json")))
silhouette = [f["polygon"] for f in native["features"] if f.get("polygon")]

for path in sorted(glob.glob(os.path.join(ROOT, "data", "*.json"))):
    d = json.load(open(path))
    if "id" not in d or "features" not in d:
        continue
    img = Image.new("RGB", (W, H), PARCHMENT)
    dr = ImageDraw.Draw(img, "RGBA")
    # state silhouette
    for polys in silhouette:
        for ring in polys:
            pts = [xy(a, b) for a, b in ring]
            dr.polygon(pts, fill=SILH + (255,), outline=(210, 200, 182, 255))
    colors = {l["id"]: hex2rgb(l["color"]) for l in d.get("layers", [])}
    is_native = d["id"] == "native-california"
    # polygons
    for f in d["features"]:
        c = colors.get(f.get("layer"), (90, 82, 72))
        if f.get("polygon"):
            for ring in f["polygon"]:
                pts = [xy(a, b) for a, b in ring]
                dr.polygon(pts, fill=c + (70,), outline=c + (200,))
    # routes
    for r in d.get("routes", []):
        c = hex2rgb(r.get("color", "#444444"))
        pts = [xy(*s["coords"]) for s in r.get("stops", [])]
        if len(pts) > 1:
            dr.line(pts, fill=c + (230,), width=3)
        for p in pts:
            dr.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], fill=c + (255,))
    # point features
    if not is_native:
        for f in d["features"]:
            if f.get("polygon"):
                continue
            c = colors.get(f.get("layer"), (90, 82, 72))
            x, y = xy(*f["coords"])
            ref = "reference" in (f.get("tags") or [])
            rad = 3 if ref else 5
            a = 130 if ref else 235
            if f.get("area_radius_km"):
                rr = f["area_radius_km"] * 1000 / 111000 / (LAT1 - LAT0) * H
                dr.ellipse([x-rr, y-rr, x+rr, y+rr], outline=c + (180,), width=2)
            else:
                dr.ellipse([x-rad, y-rad, x+rad, y+rad], fill=c + (a,),
                           outline=(255, 255, 255, 200))
    out = os.path.join(OUT, d["id"] + ".jpg")
    img.save(out, quality=82)
    print("wrote", out)
