# Repository Guidelines

## Project Structure & Module Organization

- Monorepo of self‑contained experiments. One project, one folder with a simple name.
- Project have a `README.md`, `Makefile`, and relevant files.
- Use per‑project make targets.

## General Guidelines

- Keep Make targets consistent: `dev`, `cli`, `test`, `install`, `snapshot` where applicable.
- Add small, task‑oriented `README.md` per project (what it is, quickstart, common commands).
- Use `uv` when working with Python (e.g., `uv run`, `uv add`). Check `uv help` for options.
- Run `curl`, other UNIX tools, or small termporary Python scripts to gather information before making decisions or writing long scripts. Useful for APIs, exploring datasets, etc.

### Working with `uv`

- If `uv` is not installed, install it via `pip install uv`.
- Write `uv` compatible self contained Python scripts (dependencies included). Start Python scripts with this comment adapted to the relevant dependencies.

  ```python
  #!/usr/bin/env -S uv run --script
  # /// script
  # requires-python = ">=3.12"
  # dependencies = [
  #   "polars",
  #   "duckdb",
  # ]
  # ///
  import polars as pl
  ...
  ```
- Run the scripts with `uv run script.py`.

## Commit & Pull Request Guidelines

- Concise commits in imperative mood with a clear message preceded of a relevant emoji. E.g., `✨ Add new feature`, `🐛 Fix bug`, `📝 Update docs`.
- Small and clear Pull Requests with a summary and any other relevant information (logs, commands to check, ...).
