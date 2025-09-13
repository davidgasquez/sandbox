#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx",
#   "certifi",
# ]
# ///

from pathlib import Path
import certifi

import httpx

API_URL = "https://servicios.ine.es/wstempus/js/ES/TABLAS_OPERACION/ADRH"
CSV_BASE = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc"

def fetch_table_ids():
    resp = httpx.get(API_URL, timeout=30, verify=certifi.where())
    resp.raise_for_status()
    tables = resp.json()
    return [
        (t["Id"], t["Nombre"]) for t in tables if t.get("Codigo") == "MUN-DIST-SECC"
    ]


def download_csv(table_id, out_dir):
    url = f"{CSV_BASE}/{table_id}.csv"
    resp = httpx.get(url, timeout=60, verify=certifi.where())
    resp.raise_for_status()
    (out_dir / f"{table_id}.csv").write_bytes(resp.content)


def main():
    out_dir = Path("data")
    out_dir.mkdir(parents=True, exist_ok=True)

    tables = fetch_table_ids()
    for tid, name in tables:
        print(f"Downloading {tid} - {name}")
        download_csv(tid, out_dir)

    print(f"Downloaded {len(tables)} tables to {out_dir}")


if __name__ == "__main__":
    main()
