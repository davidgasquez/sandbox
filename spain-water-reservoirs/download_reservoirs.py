#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx",
#   "polars",
# ]
# ///
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence

import httpx
import polars as pl

BASE_ENDPOINT = "https://services-eu1.arcgis.com/RvnYk1PBUJ9rrAuT/ArcGIS/rest/services"
DATASET_NAME = "Embalses_Total"
DEFAULT_PARAMS = {
    "resultType": "standard",
    "outFields": "*",
    "returnGeometry": "false",
    "f": "pjson",
}
START_YEAR = 1988
TIMEOUT = httpx.Timeout(30.0, connect=30.0, read=120.0)


def query_arcgis(
    client: httpx.Client,
    dataset: str,
    params: dict[str, str | int | float] | None = None,
) -> dict:
    url = f"{BASE_ENDPOINT}/{dataset}/FeatureServer/0/query"
    query_params = DEFAULT_PARAMS.copy()
    if params:
        query_params.update(params)

    response = client.get(url, params=query_params)
    response.raise_for_status()
    return response.json()


def iter_yearly_records(
    client: httpx.Client, start_year: int, end_year: int
) -> Iterable[dict]:
    for year in range(start_year, end_year + 1):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        where_clause = (
            "fecha BETWEEN timestamp '"
            f"{start_date:%Y-%m-%d}' AND timestamp '{end_date:%Y-%m-%d}'"
        )
        print(f"Downloading {year}...", flush=True)
        payload = query_arcgis(
            client,
            DATASET_NAME,
            params={"where": where_clause},
        )
        features = payload.get("features", [])
        for feature in features:
            attributes = feature.get("attributes", {})
            if attributes:
                yield attributes


def build_frame(records: Sequence[dict]) -> pl.DataFrame:
    df = pl.from_dicts(records, infer_schema_length=None)
    if "fecha" in df.columns:
        df = df.with_columns(pl.col("fecha").cast(pl.Datetime("ms")))
    return df


def write_parquet(df: pl.DataFrame, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(output_path)
    return output_path


def main() -> None:
    current_year = datetime.now().year
    with httpx.Client(timeout=TIMEOUT, verify=False) as client:
        records = list(iter_yearly_records(client, START_YEAR, current_year))

    if not records:
        raise SystemExit("No records downloaded")

    df = build_frame(records)
    output_path = Path(__file__).resolve().parent / "data" / "water_reservoirs.parquet"
    write_parquet(df, output_path)
    print(f"Saved {len(df)} records to {output_path}")


if __name__ == "__main__":
    main()
