# Cryo

Trying to get chain data with cryo.

```bash
cryo blocks -b 18000000:18100000 \
    --rpc https://eth.merkle.io

cryo blocks --contract "0x4AAcca72145e1dF2aeC137E1f3C5E3D75DB8b5f3" \
    --chunk-size 10000 \
    --output-dir data \
    --overwrite \
    -b 18790000:18800000 \
    --rpc https://eth.merkle.io
```

## EVM Networks RPC

- https://eth-archival-rpc.gateway.pokt.network
- https://eth.merkle.io
- https://eth.llamarpc.com
- https://rpc.mevblocker.io
- More at https://docs.pokt.network/get-rpcs/public-endpoints and https://chainlist.org/
