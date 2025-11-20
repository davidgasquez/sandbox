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

DEFAULT_RPC_URL = "https://api.node.glif.io/rpc/v1"
DEFAULT_DELEGATED_TARGET = "f410feoy6aghqro4yenelcwug52jg527x6tnkxl36cyi"
FILECOIN_PAY_ABI_URL = "https://raw.githubusercontent.com/FilOzone/filecoin-services/refs/heads/main/service_contracts/abi/FilecoinPayV1.abi.json"
DEFAULT_BLOCK_WINDOW = 1_880
DEFAULT_OUTPUT = Path("logs.ndjson")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch and decode Filecoin Pay contract events."
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
        help="NDJSON file to write decoded logs to.",
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
        "--abi-url",
        default=FILECOIN_PAY_ABI_URL,
        help="Location of the contract ABI JSON.",
    )
    parser.add_argument(
        "--insecure-rpc",
        action="store_true",
        help="Skip TLS certificate verification for the RPC endpoint and ABI download.",
    )
    return parser.parse_args()


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


def write_logs(logs: Iterable[DecodedLog], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as file:
        for log in logs:
            file.write(json.dumps(log.as_dict()))
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

    event_map = load_event_map(args.abi_url, verify=not args.insecure_rpc)
    raw_logs = web3.eth.get_logs(
        {
            "fromBlock": start_block,
            "toBlock": latest_block,
            "address": target_address,
        }
    )
    decoded_logs = [decode_log_entry(web3, log, event_map) for log in raw_logs]

    write_logs(decoded_logs, args.output)
    logger.info("Saved %d decoded logs to %s", len(decoded_logs), args.output)


if __name__ == "__main__":
    main()
