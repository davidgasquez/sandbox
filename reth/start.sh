#!/bin/env bash

# apt update && apt install -y curl
# curl -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' localhost:8545
# curl -X POST -H "Content-Type: application/json" --data '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}' localhost:8545

# Run in the background
reth node --datadir /reth/data/ --config /reth/reth.toml --http --http.api all

curl -LO https://github.com/sigp/lighthouse/releases/download/v4.5.0/lighthouse-v4.5.0-x86_64-unknown-linux-gnu.tar.gz
tar -xvf lighthouse-v4.5.0-x86_64-unknown-linux-gnu.tar.gz

RUST_LOG=info ./lighthouse bn \
    --checkpoint-sync-url https://mainnet.checkpoint.sigp.io \
    --execution-endpoint http://localhost:8551 \
    --disable-deposit-contract-sync \
    --execution-jwt /reth/data/jwt.hex
