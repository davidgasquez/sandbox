# Lily

After `make dev`.

```bash
lily init --config config.toml --import-snapshot snapshot.forest.car.zst
```

```bash
lily daemon --bootstrap=false --config config.toml
```

```bash
lily job run --storage=CSV walk --from 1546232 --to 1548171
```

You should see a bunch of CSVs in `/tmp`!
