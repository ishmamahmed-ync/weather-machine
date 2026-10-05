#!/usr/bin/env python3
"""Transcribe the CRI 2026 annex ranking table to cri2026.csv.

    pip install pypdf cryptography     # the PDF is permission-encrypted (AES)
    python3 extract_cri.py

Source  data/raw/germanwatch-cri-2026-full-report.pdf
        Germanwatch, Climate Risk Index 2026 (November 2025), Annex, pp. 71-76:
        "Country | Rank 2024 | Rank 1995-2024 | Rank 2023 | Rank 1994-2023"
        https://www.germanwatch.org/en/cri

cri2026.csv is committed, so build_data.py doesn't need pypdf.
"""
import csv
import re
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
PDF = HERE.parent.parent / "data/raw/germanwatch-cri-2026-full-report.pdf"
LINE = re.compile(r"^(.+?) (\d{1,3}) (\d{1,3}) (\d{1,3}) (\d{1,3})$")

rows, seen = [], set()
for page in PdfReader(PDF).pages:
    text = page.extract_text() or ""
    if "Rank 1995" not in text:
        continue
    for line in text.splitlines():
        m = LINE.match(line.strip())
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            rows.append([m.group(1), *m.group(2, 3, 4, 5)])

with open(HERE / "cri2026.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["country", "rank_2024", "rank_1995_2024", "rank_2023", "rank_1994_2023"])
    w.writerows(rows)
print(f"cri2026.csv: {len(rows)} countries")
