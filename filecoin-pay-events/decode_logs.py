#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["httpx", "web3"]
# ///
from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import httpx
from eth_utils.abi import event_abi_to_log_topic
from hexbytes import HexBytes
from web3 import Web3
from web3._utils.events import get_event_data
from web3.datastructures import AttributeDict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

FILECOIN_PAY_ABI_URL = "https://raw.githubusercontent.com/FilOzone/filecoin-services/refs/heads/main/service_contracts/abi/FilecoinPayV1.abi.json"
DEFAULT_INPUT = Path("raw-logs.ndjson")
DEFAULT_OUTPUT = Path("decoded-logs.ndjson")


@dataclass
class DecodedLog:
    event: str | None
    args: dict[str, Any] | None
    height: int
    log_index: int
    transaction_hash: str
    raw: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "event": self.event,
            "args": self.args,
            "height": self.height,
            "logIndex": self.log_index,
            "transactionHash": self.transaction_hash,
            "raw": self.raw,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Decode raw Filecoin Pay logs into typed events."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="NDJSON file containing raw logs fetched from the chain.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="NDJSON file to write decoded logs to.",
    )
    parser.add_argument(
        "--abi-url",
        default=FILECOIN_PAY_ABI_URL,
        help="Location of the contract ABI JSON.",
    )
    parser.add_argument(
        "--insecure-abi",
        action="store_true",
        help="Skip TLS certificate verification for the ABI download.",
    )
    return parser.parse_args()


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


def load_event_map(abi_url: str, *, verify: bool = True) -> dict[str, dict[str, Any]]:
    response = httpx.get(abi_url, follow_redirects=True, timeout=10, verify=verify)
    response.raise_for_status()
    abi: list[dict[str, Any]] = response.json()

    event_map: dict[str, dict[str, Any]] = {}
    for entry in abi:
        if entry.get("type") != "event":
            continue
        topic = "0x" + event_abi_to_log_topic(entry).hex()
        event_map[topic.lower()] = entry
    return event_map


def log_from_json(entry: dict[str, Any]) -> AttributeDict:
    return AttributeDict(
        {
            "address": entry["address"],
            "blockHash": HexBytes(entry["blockHash"]),
            "blockNumber": entry["blockNumber"],
            "data": HexBytes(entry["data"]),
            "logIndex": entry["logIndex"],
            "removed": entry["removed"],
            "topics": [HexBytes(topic) for topic in entry["topics"]],
            "transactionHash": HexBytes(entry["transactionHash"]),
            "transactionIndex": entry["transactionIndex"],
        }
    )


def decode_log_entry(
    web3: Web3, log: AttributeDict, event_map: dict[str, dict[str, Any]]
) -> DecodedLog:
    topic0 = log["topics"][0].hex()
    if not topic0.startswith("0x"):
        topic0 = "0x" + topic0

    abi_entry = event_map.get(topic0.lower())
    normalized_raw = normalize(dict(log))
    transaction_hash = "0x" + log["transactionHash"].hex()

    if abi_entry is None:
        return DecodedLog(
            event=None,
            args=None,
            height=log["blockNumber"],
            log_index=log["logIndex"],
            transaction_hash=transaction_hash,
            raw=normalized_raw,
        )

    decoded = get_event_data(web3.codec, abi_entry, log)
    return DecodedLog(
        event=decoded["event"],
        args={key: normalize(value) for key, value in decoded["args"].items()},
        height=log["blockNumber"],
        log_index=log["logIndex"],
        transaction_hash=transaction_hash,
        raw=normalized_raw,
    )


def read_raw_logs(source: Path) -> Iterable[dict[str, Any]]:
    with source.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def write_logs(logs: Iterable[DecodedLog], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as file:
        for log in logs:
            file.write(json.dumps(log.as_dict()))
            file.write("\n")


def main() -> None:
    args = parse_args()

    event_map = load_event_map(args.abi_url, verify=not args.insecure_abi)
    web3 = Web3()

    decoded_logs = [
        decode_log_entry(web3, log_from_json(entry), event_map)
        for entry in read_raw_logs(args.input)
    ]

    write_logs(decoded_logs, args.output)
    logger.info("Saved %d decoded logs to %s", len(decoded_logs), args.output)


if __name__ == "__main__":
    main()
