# Filecoin Pay events

This experiment pulls recent events emitted by the Filecoin Pay v1 contract through a Filecoin JSON-RPC endpoint. It converts delegated Filecoin addresses to Ethereum checksum addresses, stores the raw logs as newline-delimited JSON, and offers a separate decoder that expands the logs into typed events using the contract ABI.

## Quickstart

```bash
# Fetch the last 1,880 blocks as raw logs
uv run fetch_logs.py

# Decode those logs with the published ABI
uv run decode_logs.py

# Override the window or output path
uv run fetch_logs.py --blocks 500 --output data/raw.ndjson
uv run decode_logs.py --input data/raw.ndjson --output data/decoded.ndjson

# Use the RPC endpoint without TLS verification (only if needed)
uv run fetch_logs.py --insecure-rpc
uv run decode_logs.py --insecure-abi
```

The default contract target is `f410feoy6aghqro4yenelcwug52jg527x6tnkxl36cyi` (Filecoin Pay v1). Use `--delegated-target` to inspect another delegated address.

## Flow example

Recent runs produced the following raw and decoded lines:

```json
// raw
{"address": "0x23b1e018F08BB982348b15a86ee926eEBf7F4DAa", "blockHash": "0xe306796b02fdccadfeb97a259a5e6ad889421485e9ad70fabef35c5e9dc903a9", "blockNumber": 5510778, "data": "0x000000000000000000000000000000000000000000000000160aa318bf0fc37400000000000000000000000000000000000000000000000000000000001e51057e154000000000000000000000000000000000000000000000000000000000054167a", "logIndex": 41, "removed": false, "topics": ["0x25db253b018b2168f226371d77fc91f15152c02e8242c25af92a8271d239f450", "0x00000000000000000000000080b98d3aa09ffff255c3ba4a241111ff1262f045", "0x000000000000000000000000af992fbc0c22bc941a232c63dc1b0c0cd572d145"], "transactionHash": "0x7c8e6cb42ac741614049ca7c9c6da5253269df773667376a9b1170227adb87b8", "transactionIndex": 16}

// decoded
{"event": "AccountLockupSettled", "args": {"token": "0x80B98d3aa09ffff255c3ba4A241111Ff1262F045", "owner": "0xAf992Fbc0c22BC941A232c63dc1b0c0cD572D145", "lockupCurrent": 1588261145281545076, "lockupRate": 2083333333332, "lockupLastSettledAt": 5510778}, "height": 5510778, "logIndex": 41, "transactionHash": "0x7c8e6cb42ac741614049ca7c9c6da5253269df773667376a9b1170227adb87b8", "raw": {"address": "0x23b1e018F08BB982348b15a86ee926eEBf7F4DAa", "blockHash": "0xe306796b02fdccadfeb97a259a5e6ad889421485e9ad70fabef35c5e9dc903a9", "blockNumber": 5510778, "data": "0x000000000000000000000000000000000000000000000000160aa318bf0fc37400000000000000000000000000000000000000000000000000000000001e51057e154000000000000000000000000000000000000000000000000000000000054167a", "logIndex": 41, "removed": false, "topics": ["0x25db253b018b2168f226371d77fc91f15152c02e8242c25af92a8271d239f450", "0x00000000000000000000000080b98d3aa09ffff255c3ba4a241111ff1262f045", "0x000000000000000000000000af992fbc0c22bc941a232c63dc1b0c0cd572d145"], "transactionHash": "0x7c8e6cb42ac741614049ca7c9c6da5253269df773667376a9b1170227adb87b8", "transactionIndex": 16}}
```

## Development

- `make fetch` – pull raw logs with defaults
- `make decode` – decode the most recent raw file
- `make run` – fetch then decode in sequence
- `make format` – format the code with Ruff
- `make lint` – run Ruff checks
