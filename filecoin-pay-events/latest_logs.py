#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["web3", "hexbytes"]
# ///
from __future__ import annotations

import csv
import logging
from pathlib import Path
from typing import Any

from hexbytes import HexBytes
from web3 import Web3
from web3.datastructures import AttributeDict


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

RPC_URL = "https://rpc.ankr.com/filecoin"
EPOCH_WINDOW = 1_000
CHUNK_SIZE = 100
OUTPUT = Path("latest-logs.csv")


def normalize(value: Any) -> Any:
    if isinstance(value, AttributeDict):
        return {key: normalize(inner) for key, inner in value.items()}
    if isinstance(value, dict):
        return {key: normalize(inner) for key, inner in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(inner) for inner in value]
    if isinstance(value, (HexBytes, bytes, bytearray)):
        return "0x" + value.hex()
    return value


def fetch_logs(web3: Web3, start_block: int, end_block: int) -> list[AttributeDict]:
    logs: list[AttributeDict] = []
    current = start_block

    while current <= end_block:
        chunk_end = min(current + CHUNK_SIZE - 1, end_block)
        batch = web3.eth.get_logs({"fromBlock": current, "toBlock": chunk_end})
        logs.extend(batch)
        logger.info(
            "Fetched %d logs from %s-%s (running total: %d)",
            len(batch),
            current,
            chunk_end,
            len(logs),
        )
        current = chunk_end + 1

    return logs


def write_csv(logs: list[AttributeDict], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "blockNumber",
        "transactionHash",
        "transactionIndex",
        "logIndex",
        "address",
        "topics",
        "data",
        "blockHash",
        "removed",
    ]

    with destination.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for raw in logs:
            normalized = normalize(dict(raw))
            writer.writerow(
                {
                    "blockNumber": normalized.get("blockNumber"),
                    "transactionHash": normalized.get("transactionHash"),
                    "transactionIndex": normalized.get("transactionIndex"),
                    "logIndex": normalized.get("logIndex"),
                    "address": normalized.get("address"),
                    "topics": ",".join(normalized.get("topics", [])),
                    "data": normalized.get("data"),
                    "blockHash": normalized.get("blockHash"),
                    "removed": normalized.get("removed"),
                }
            )

    logger.info("Saved %d logs to %s", len(logs), destination)


def main() -> None:
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    latest_block = web3.eth.block_number
    start_block = max(0, latest_block - EPOCH_WINDOW + 1)

    logger.info("Latest block: %s", latest_block)
    logger.info("Fetching logs from block %s to %s", start_block, latest_block)

    raw_logs = fetch_logs(web3, start_block=start_block, end_block=latest_block)
    write_csv(raw_logs, OUTPUT)


if __name__ == "__main__":
    main()
