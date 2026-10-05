"""Minimal .xlsx reader, standard library only (no openpyxl on this machine).

    from xlsx import read_rows
    for row in read_rows("file.xlsx"):   # first sheet, list of cell strings
        ...
"""
import re
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def _col(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group():
        n = n * 26 + ord(ch) - 64
    return n - 1


def read_rows(path, sheet=1):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))
    root = ET.fromstring(z.read(f"xl/worksheets/sheet{sheet}.xml"))
    for r in root.iter(f"{{{NS['m']}}}row"):
        out = []
        for c in r.findall("m:c", NS):
            i = _col(c.get("r"))
            while len(out) < i:
                out.append("")
            v = c.find("m:v", NS)
            t = c.get("t")
            if t == "s" and v is not None:
                out.append(shared[int(v.text)])
            elif t == "inlineStr":
                out.append("".join(x.text or "" for x in c.iter(f"{{{NS['m']}}}t")))
            else:
                out.append(v.text if v is not None else "")
        yield out
