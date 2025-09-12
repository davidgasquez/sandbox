#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "polars",
#   "requests",
# ]
# ///
"""Download Spain Climate TRACE country package and combine into a long table."""

import io
import zipfile
from pathlib import Path

import polars as pl
import requests
import urllib3

URL = "https://downloads.climatetrace.org/v4.6.0/country_packages/co2e_100yr/ESP.zip"
OUT_CSV = Path("esp_emissions_long.csv")


def main(out: Path = OUT_CSV) -> None:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    resp = requests.get(URL, verify=False)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        country_files = [
            f for f in zf.namelist() if f.endswith("country_emissions_v4_6_0.csv")
        ]
        frames = []
        for f in country_files:
            with zf.open(f) as fh:
                df = pl.read_csv(
                    fh, schema_overrides={"emissions_quantity": pl.Float64}
                )
            frames.append(
                df.select(
                    "iso3_country",
                    "sector",
                    "subsector",
                    "start_time",
                    "end_time",
                    "gas",
                    "emissions_quantity",
                    "emissions_quantity_units",
                    "temporal_granularity",
                )
            )
    combined = pl.concat(frames, how="diagonal")
    combined.write_csv(out)
    print(f"wrote {out} with {combined.shape[0]} rows")


if __name__ == "__main__":
    main()
