# Cryo

Getting some chain data with cryo.

```bash
cryo blocks -b 18000000:18100000 \
    --rpc https://eth.merkle.io

cryo transactions --contract "0x03506eD3f57892C85DB20C36846e9c808aFe9ef4" \
    --output-dir data \
    --overwrite \
    -b 18940000:18950000 \
    --rpc https://eth.merkle.io
```

## FEVM

```bash
cryo -r https://api.node.glif.io/rpc/v1 logs -b 5500908:5510938
```

## Docker

```bash
cd cryo
make install
make cli
```
