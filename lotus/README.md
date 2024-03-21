# Lotus

Get Lotus with the following command:

```bash
wget https://github.com/filecoin-project/lotus/releases/download/v1.25.2/lotus_v1.25.2_linux_amd64.tar.gz -O lotus.tar.gz && tar -xvf lotus.tar.gz && rm lotus.tar.gz && mv lotus_v1.25.2_linux_amd64 lotus
```

Download snapshots from Forest Archive.

```bash
mkdir snapshots
wget https://forest-archive.chainsafe.dev/mainnet/diff/forest_diff_mainnet_2020-08-24_height_0+3000.forest.car.zst -P snapshots
wget https://forest-archive.chainsafe.dev/mainnet/lite/forest_snapshot_mainnet_2020-08-24_height_0.forest.car.zst -P snapshots
```

Run Lotus with the following command:

```bash
./lotus daemon \
    --import-snapshot snapshots/forest_* \
    --bootstrap=false \
    --remove-existing-chain \
    --halt-after-import
```

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetTipSetByHeight",
      "params": [0, null],
      "id": 1
    }' \
  http://127.0.0.1:1234/rpc/v0 | jq '.result'
```
