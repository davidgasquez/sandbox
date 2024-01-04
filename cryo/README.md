# Cryo

Trying to get chain data with cryo.

```bash
cryo blocks -b 18000000:18100000 \
    --rpc https://eth.merkle.io

cryo transactions --contract "0x03506eD3f57892C85DB20C36846e9c808aFe9ef4" \
    --output-dir data \
    --overwrite \
    -b 18940000:18950000 \
    --rpc https://eth.merkle.io
```

## EVM Networks RPC

- https://eth-archival-rpc.gateway.pokt.network
- https://eth.merkle.io
- https://eth.llamarpc.com
- https://rpc.mevblocker.io
- More at https://docs.pokt.network/get-rpcs/public-endpoints and https://chainlist.org/

## FEVM

```bash
cryo blocks -b 3536080:3536085 --csv \
    --rpc https://rpc.ankr.com/filecoin
```
