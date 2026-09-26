"""
Convert the fixed-width GHCN-Daily station file into geospatial-ready outputs.

    python clean_ghcnd_stations.py <ghcnd-stations file> <outdir>

The input is fixed-width despite often being named ".csv". Field positions follow
NCEI readme.txt v3.34 section IV. Country and network code tables are from
ghcnd-countries.txt and readme.txt section IV respectively.

Outputs
  ghcnd-stations-clean.csv   delimited, quoted, lat/lon named for auto-detection
  ghcnd-stations.geojson     RFC 7946 FeatureCollection of Points
  ghcnd-stations-slim.csv    id/lat/lon/name/country only, for fast plotting
"""

import sys, os, json, csv

# readme.txt section IV: ID 1-11, LAT 13-20, LON 22-30, ELEV 32-37,
# STATE 39-40, NAME 42-71, GSN 73-75, HCN/CRN 77-79, WMO ID 81-85 (1-indexed)
FIELDS = [
    ("station_id", 0, 11),
    ("lat", 12, 20),
    ("lon", 21, 30),
    ("elevation_m", 31, 37),
    ("state", 38, 40),
    ("name", 41, 71),
    ("gsn_flag", 72, 75),
    ("hcn_crn_flag", 76, 79),
    ("wmo_id", 80, 85),
]

ELEV_MISSING = -999.9

NETWORKS = {
    "0": "Unspecified",
    "1": "CoCoRaHS",
    "C": "US Cooperative Observer Program",
    "E": "ECA&D non-blended",
    "M": "WMO",
    "N": "National Meteorological or Hydrological Center",
    "P": "Pre-Coop (NCEI internal)",
    "R": "US Interagency RAWS",
    "S": "NRCS SNOTEL",
    "W": "WBAN",
}

COUNTRIES_RAW = """AC Antigua and Barbuda|AE United Arab Emirates|AF Afghanistan|AG Algeria|AJ Azerbaijan|AL Albania|AM Armenia|AO Angola|AQ American Samoa [United States]|AR Argentina|AS Australia|AU Austria|AY Antarctica|BA Bahrain|BB Barbados|BC Botswana|BD Bermuda [United Kingdom]|BE Belgium|BF Bahamas, The|BG Bangladesh|BH Belize|BK Bosnia and Herzegovina|BL Bolivia|BM Burma|BN Benin|BO Belarus|BP Solomon Islands|BR Brazil|BU Bulgaria|BX Brunei|BY Burundi|CA Canada|CB Cambodia|CD Chad|CE Sri Lanka|CF Congo (Brazzaville)|CG Congo (Kinshasa)|CH China|CI Chile|CJ Cayman Islands [United Kingdom]|CK Cocos (Keeling) Islands [Australia]|CM Cameroon|CO Colombia|CQ Northern Mariana Islands [United States]|CS Costa Rica|CT Central African Republic|CU Cuba|CV Cape Verde|CW Cook Islands [New Zealand]|CY Cyprus|DA Denmark|DO Dominica|DR Dominican Republic|EC Ecuador|EG Egypt|EI Ireland|EK Equatorial Guinea|EN Estonia|ER Eritrea|ES El Salvador|ET Ethiopia|EU Europa Island [France]|EZ Czech Republic|FG French Guiana [France]|FI Finland|FJ Fiji|FK Falkland Islands (Islas Malvinas) [United Kingdom]|FM Federated States of Micronesia|FP French Polynesia|FR France|FS French Southern and Antarctic Lands [France]|GA Gambia, The|GB Gabon|GG Georgia|GH Ghana|GI Gibraltar [United Kingdom]|GL Greenland [Denmark]|GM Germany|GP Guadeloupe [France]|GQ Guam [United States]|GR Greece|GT Guatemala|GV Guinea|GY Guyana|HO Honduras|HR Croatia|HU Hungary|IC Iceland|ID Indonesia|IN India|IO British Indian Ocean Territory [United Kingdom]|IR Iran|IS Israel|IT Italy|IV Cote D'Ivoire|IZ Iraq|JA Japan|JM Jamaica|JN Jan Mayen [Norway]|JO Jordan|JQ Johnston Atoll [United States]|JU Juan De Nova Island [France]|KE Kenya|KG Kyrgyzstan|KN Korea, North|KR Kiribati|KS Korea, South|KT Christmas Island [Australia]|KU Kuwait|KZ Kazakhstan|LA Laos|LE Lebanon|LG Latvia|LH Lithuania|LI Liberia|LO Slovakia|LQ Palmyra Atoll [United States]|LT Lesotho|LU Luxembourg|LY Libya|MA Madagascar|MB Martinique [France]|MC Macau S.A.R|MD Moldova|MF Mayotte [France]|MG Mongolia|MI Malawi|MJ Montenegro|MK Macedonia|ML Mali|MO Morocco|MP Mauritius|MQ Midway Islands [United States]|MR Mauritania|MT Malta|MU Oman|MV Maldives|MX Mexico|MY Malaysia|MZ Mozambique|NC New Caledonia [France]|NE Niue [New Zealand]|NF Norfolk Island [Australia]|NG Niger|NH Vanuatu|NI Nigeria|NL Netherlands|NN Sint Maarten|NO Norway|NP Nepal|NS Suriname|NU Nicaragua|NZ New Zealand|PA Paraguay|PC Pitcairn Islands [United Kingdom]|PE Peru|PK Pakistan|PL Poland|PM Panama|PO Portugal|PP Papua New Guinea|PS Palau|PU Guinea-Bissau|QA Qatar|RE Reunion [France]|RI Serbia|RM Marshall Islands|RO Romania|RP Philippines|RQ Puerto Rico [United States]|RS Russia|RW Rwanda|SA Saudi Arabia|SB Saint Pierre and Miquelon [France]|SE Seychelles|SF South Africa|SG Senegal|SH Saint Helena [United Kingdom]|SI Slovenia|SL Sierra Leone|SN Singapore|SP Spain|ST Saint Lucia|SU Sudan|SV Svalbard [Norway]|SW Sweden|SX South Georgia and the South Sandwich Islands [United Kingdom]|SY Syria|SZ Switzerland|TD Trinidad and Tobago|TE Tromelin Island [France]|TH Thailand|TI Tajikistan|TL Tokelau [New Zealand]|TN Tonga|TO Togo|TS Tunisia|TU Turkey|TV Tuvalu|TX Turkmenistan|TZ Tanzania|UC Curacao|UG Uganda|UK United Kingdom|UP Ukraine|US United States|UV Burkina Faso|UY Uruguay|UZ Uzbekistan|VE Venezuela|VM Vietnam|VQ Virgin Islands [United States]|WA Namibia|WF Wallis and Futuna|WI Western Sahara|WQ Wake Island [United States]|WZ Swaziland|ZA Zambia|ZI Zimbabwe"""
COUNTRIES = dict(e.split(" ", 1) for e in COUNTRIES_RAW.split("|"))

OUT_COLS = [
    "station_id", "lat", "lon", "elevation_m", "name",
    "country_code", "country_name", "state",
    "network_code", "network_name",
    "gsn_flag", "hcn_crn_flag", "wmo_id",
]


def parse(path):
    rows, skipped = [], []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.rstrip("\r\n")
            if not line.strip():
                continue
            r = {k: line[a:b].strip() for k, a, b in FIELDS}

            try:
                lat, lon = float(r["lat"]), float(r["lon"])
            except ValueError:
                skipped.append((lineno, "unparseable coordinates", line[:40]))
                continue
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                skipped.append((lineno, "coordinates out of range", line[:40]))
                continue
            if len(r["station_id"]) != 11:
                skipped.append((lineno, "malformed station id", line[:40]))
                continue

            try:
                elev = float(r["elevation_m"])
            except ValueError:
                elev = None
            if elev is not None and abs(elev - ELEV_MISSING) < 0.001:
                elev = None

            code, net = r["station_id"][:2], r["station_id"][2]
            rows.append({
                "station_id": r["station_id"],
                "lat": round(lat, 4),
                "lon": round(lon, 4),
                "elevation_m": elev,
                "name": " ".join(r["name"].split()),
                "country_code": code,
                "country_name": COUNTRIES.get(code, ""),
                "state": r["state"],
                "network_code": net,
                "network_name": NETWORKS.get(net, ""),
                "gsn_flag": 1 if r["gsn_flag"] == "GSN" else 0,
                "hcn_crn_flag": r["hcn_crn_flag"],
                "wmo_id": r["wmo_id"],
            })
    return rows, skipped


def write_csv(rows, path, cols):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore",
                           quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})


def write_geojson(rows, path):
    """Streamed so memory stays flat regardless of station count."""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write('{"type":"FeatureCollection","features":[\n')
        for i, r in enumerate(rows):
            props = {k: r[k] for k in OUT_COLS if k not in ("lat", "lon")}
            props = {k: v for k, v in props.items() if v not in ("", None)}
            feat = {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
                "properties": props,
            }
            fh.write(("," if i else "") + json.dumps(feat, ensure_ascii=False) + "\n")
        fh.write("]}\n")


def main():
    src, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    rows, skipped = parse(src)

    write_csv(rows, f"{outdir}/ghcnd-stations-clean.csv", OUT_COLS)
    write_csv(rows, f"{outdir}/ghcnd-stations-slim.csv",
              ["station_id", "lat", "lon", "name", "country_name"])
    write_geojson(rows, f"{outdir}/ghcnd-stations.geojson")

    print(f"stations written   {len(rows):,}")
    print(f"rows skipped       {len(skipped):,}")
    for s in skipped[:10]:
        print("   ", s)
    print(f"elevation nulled   {sum(1 for r in rows if r['elevation_m'] is None):,}")
    print(f"countries resolved {len({r['country_code'] for r in rows if r['country_name']}):,}")
    unmapped = sorted({r["country_code"] for r in rows if not r["country_name"]})
    print(f"country codes unmapped {unmapped if unmapped else 'none'}")
    unnet = sorted({r["network_code"] for r in rows if not r["network_name"]})
    print(f"network codes unmapped {unnet if unnet else 'none'}")


if __name__ == "__main__":
    main()
