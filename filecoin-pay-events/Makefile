.PHONY: run fetch decode format lint

fetch:
uv run fetch_logs.py

decode:
uv run decode_logs.py

run: fetch decode

format:
uvx ruff format .

lint:
uvx ruff check .
