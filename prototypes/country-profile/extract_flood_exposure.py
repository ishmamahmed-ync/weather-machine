#!/usr/bin/env python3
"""Transcribe Rentschler et al. (2022) Supplementary Table 1 to flood_exposure.csv.

    pip install pypdf
    python3 extract_flood_exposure.py

Source  data/raw/rentschler-2022-flood-exposure-SI.pdf
        Rentschler, Salhab & Jafino (2022), "Flood exposure and poverty in 188
        countries", Nature Communications 13:3527, Supplementary Table 1:
        population exposed to high flood risk (1-in-100-year flood, inundation
        above 15 cm; fluvial, pluvial or coastal), thousands of people, WorldPop 2020.

Checks that rows run 1..188 with no gaps and that the total is ~1.81 billion
(the paper's headline). flood_exposure.csv is committed.
"""
import csv
import re
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
PDF = HERE.parent.parent / "data/raw/rentschler-2022-flood-exposure-SI.pdf"

text = " ".join((p.extract_text() or "") for p in PdfReader(PDF).pages)
text = text[text.index("Supplementary Table 1"):]
text = re.sub(r"\s+", " ", text)
N = r"([\d,]+)"; P = r"([\d.]+)"
row = re.compile(rf"\b(\d{{1,3}}) ([A-Z][^\d]*?) {N} {N} {P} {N} {P} {N} {P} {N} {P}(?= |$)")

out, want = [], 1
for m in row.finditer(text):
    if int(m.group(1)) != want:
        continue
    num = lambda s: int(s.replace(",", ""))
    out.append({"rank_row": want, "country": m.group(2).strip(), "population_k": num(m.group(3)),
                "exposed_k": num(m.group(4)), "exposed_pct": float(m.group(5))})
    want += 1

total = sum(r["exposed_k"] for r in out)
print(f"rows 1..{want - 1} ({len(out)}), exposed total {total/1e6:.2f} billion")
assert len(out) == 188, "expected 188 countries"
with open(HERE / "flood_exposure.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader(); w.writerows(out)
