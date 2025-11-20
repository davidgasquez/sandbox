#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["httpx", "web3"]
# ///
from __future__ import annotations

import argparse
import base64
import json
import logging
from pathlib import Path
from typing import Any

from hexbytes import HexBytes
from web3 import Web3
from web3.datastructures import AttributeDict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

DEFAULT_RPC_URL = "https://api.node.glif.io/rpc/v1"
DEFAULT_DELEGATED_TARGET = "f410feoy6aghqro4yenelcwug52jg527x6tnkxl36cyi"
DEFAULT_BLOCK_WINDOW = 1_880
DEFAULT_OUTPUT = Path("raw-logs.ndjson")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch raw logs for a delegated Filecoin contract address."
    )
    parser.add_argument(
        "--blocks",
        type=int,
        default=DEFAULT_BLOCK_WINDOW,
        help="Number of most recent blocks to inspect.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="NDJSON file to write raw logs to.",
    )
    parser.add_argument(
        "--delegated-target",
        default=DEFAULT_DELEGATED_TARGET,
        help="Delegated Filecoin address (f4/t4) for the contract to inspect.",
    )
    parser.add_argument(
        "--rpc-url",
        default=DEFAULT_RPC_URL,
        help="JSON-RPC endpoint for the Filecoin node.",
    )
    parser.add_argument(
        "--insecure-rpc",
        action="store_true",
        help="Skip TLS certificate verification for the RPC endpoint.",
    )
    return parser.parse_args()


def delegated_to_eth(address: str) -> str:
    if not address.startswith(("f4", "t4")):
        raise ValueError("Expected delegated (f4/t4) address")

    raw = address[2:]
    namespace_digits = []
    for char in raw:
        if char.isdigit():
            namespace_digits.append(char)
        else:
            break
    if not namespace_digits:
        raise ValueError("Missing delegated namespace")

    namespace = int("".join(namespace_digits))
    if namespace != 10:
        raise ValueError(f"Unsupported delegated namespace: {namespace}")

    if len(raw) == len(namespace_digits) or raw[len(namespace_digits)] != "f":
        raise ValueError("Malformed delegated address")

    payload = raw[len(namespace_digits) + 1 :]
    padding = "=" * ((8 - len(payload) % 8) % 8)
    decoded = base64.b32decode(payload.upper() + padding)
    if len(decoded) < 4:
        raise ValueError("Delegated payload too short")

    sub_address = decoded[:-4]
    if len(sub_address) != 20:
        raise ValueError(
            "Delegated sub-address must be 20 bytes for Ethereum compatibility"
        )

    return Web3.to_checksum_address(sub_address)


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


def write_logs(logs: list[AttributeDict], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as file:
        for log in logs:
            file.write(json.dumps(normalize(dict(log))))
            file.write("\n")


def main() -> None:
    args = parse_args()

    provider_kwargs = {}
    if args.insecure_rpc:
        logger.warning(
            "RPC TLS verification is disabled. Use only in trusted environments."
        )
        provider_kwargs["request_kwargs"] = {"verify": False}

    web3 = Web3(Web3.HTTPProvider(args.rpc_url, **provider_kwargs))
    latest_block = web3.eth.block_number
    window = max(args.blocks, 1)
    start_block = max(0, latest_block - window + 1)
    target_address = delegated_to_eth(args.delegated_target)

    logger.info("Latest block: %s", latest_block)
    logger.info(
        "Fetching logs from block %s to %s for %s (%s)",
        start_block,
        latest_block,
        target_address,
        args.delegated_target,
    )

    raw_logs = web3.eth.get_logs(
        {
            "fromBlock": start_block,
            "toBlock": latest_block,
            "address": target_address,
        }
    )

    write_logs(raw_logs, args.output)
    logger.info("Saved %d raw logs to %s", len(raw_logs), args.output)


if __name__ == "__main__":
    main()
