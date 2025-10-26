# Spain Water Reservoirs

Download Spain's water reservoir time series from the MITECO ArcGIS service and store them as a Parquet file.

## Quickstart

```sh
make data
```

The command runs `download_reservoirs.py`, which pulls records from 1988 to the current year and saves them to `data/water_reservoirs.parquet` inside this folder.

## Notes

- The script uses `httpx` and `polars` and is meant to be executed with `uv run`.
- SSL verification is disabled in the script because the ArcGIS endpoint currently presents an incomplete certificate chain in this environment.
- Data source: [MITECO ArcGIS services](https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico.html).
- API reference: [REE Datos API](https://www.ree.es/es/datos/apidatos).
