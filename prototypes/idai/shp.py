"""Minimal ESRI shapefile reader, standard library only (no GDAL/shapely here).

    from shp import read
    for geom, props in read("path/to/file"):     # path without extension
        geom = {"type": "Polygon"|"LineString"|"Point", "parts": [[(x, y), ...], ...]}

Handles point (1), polyline (3), polygon (5) and their Z / M variants
(11/13/15, 21/23/25). Coordinates are returned as stored; every file used here
is WGS 84 lon/lat (checked from the .prj).
"""
import struct
from pathlib import Path

KIND = {1: "Point", 3: "LineString", 5: "Polygon"}


def _dbf(path):
    b = Path(path).read_bytes()
    n, hlen, rlen = struct.unpack("<IHH", b[4:12])
    fields, off = [], 32
    while b[off] != 0x0D:
        name = b[off:off + 11].split(b"\0")[0].decode("latin-1")
        fields.append((name, chr(b[off + 11]), b[off + 16]))
        off += 32
    rows = []
    for i in range(n):
        r = b[hlen + i * rlen: hlen + (i + 1) * rlen]
        if r[:1] == b"*":                 # deleted record
            rows.append(None); continue
        p, rec = 1, {}
        for name, typ, ln in fields:
            v = r[p:p + ln].decode("utf-8", "replace").strip(); p += ln
            if typ in "NF" and v:
                try: v = float(v) if "." in v or "e" in v.lower() else int(v)
                except ValueError: pass
            rec[name] = v
        rows.append(rec)
    return rows


def read(base):
    base = str(base)
    b = Path(base + ".shp").read_bytes()
    props = _dbf(base + ".dbf") if Path(base + ".dbf").exists() else None
    off, i = 100, 0
    while off < len(b):
        _, clen = struct.unpack(">II", b[off:off + 8])
        rec = b[off + 8: off + 8 + clen * 2]
        off += 8 + clen * 2
        st = struct.unpack("<i", rec[:4])[0]
        base_type = st % 10 if st not in (0,) else 0
        p = props[i] if props else {}
        i += 1
        if st == 0 or p is None:
            continue
        if base_type == 1:
            x, y = struct.unpack("<2d", rec[4:20])
            yield {"type": "Point", "parts": [[(x, y)]]}, p
            continue
        nparts, npts = struct.unpack("<2i", rec[36:44])
        starts = list(struct.unpack(f"<{nparts}i", rec[44:44 + 4 * nparts])) + [npts]
        q = 44 + 4 * nparts
        pts = list(struct.iter_unpack("<2d", rec[q:q + 16 * npts]))
        yield {"type": KIND[base_type], "parts": [pts[starts[k]:starts[k + 1]] for k in range(nparts)]}, p
