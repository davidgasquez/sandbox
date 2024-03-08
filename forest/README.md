# Forest

Some random tinkering with Forest, the Rust Filecoin Node Implementation.

You can get the snapshots from the [Forest Archive](https://forest-archive.chainsafe.dev/list/).

## Tinkering

Let's download a little and diff snapshots from the [Forest Archive](https://forest-archive.chainsafe.dev/list/), add it to a `data` folder and then run the following commands to import the snapshot and serve an offline RPC endpoint.

```bash
mkdir data
wget https://forest-archive.chainsafe.dev/mainnet/diff/forest_diff_mainnet_2020-08-24_height_0+3000.forest.car.zst -P data
wget https://forest-archive.chainsafe.dev/mainnet/lite/forest_snapshot_mainnet_2020-08-24_height_0.forest.car.zst -P data
```

Running `make cli` will spin up the latest Docker image and drop you into a shell with the relevant binaries available.

Let's try to get some data out of it.

```bash
forest-tool api serve data/forest_snapshot_mainnet_2020-08-24_height_0.forest.car.zst
```

Wait for the `Ready for RPC connections` and then run the following command in a new shell to get info about the first block of the chain.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetTipSetByHeight",
      "params": [0, null],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq '.result'
```

You should get this:

```json
{
  "Cids": [
    {
      "/": "bafy2bzacecnamqgqmifpluoeldx7zzglxcljo6oja4vrmtj7432rphldpdmm2"
    }
  ],
  "Blocks": [
    {
      "Miner": "f00",
      "Ticket": {
        "VRFProof": "X4oDOWswmmD7fT0z3RNIPQVGS85f2dBhceeowoDiQhY="
      },
      "ElectionProof": {
        "VRFProof": null,
        "WinCount": 0
      },
      "BeaconEntries": [
        {
          "Round": 0,
          "Data": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
        }
      ],
      "WinPoStProof": null,
      "Parents": [
        {
          "/": "bafyreiaqpwbbyjo4a42saasj36kkrpv4tsherf2e7bvezkert2a7dhonoi"
        }
      ],
      "ParentWeight": "0",
      "Height": 0,
      "ParentStateRoot": {
        "/": "bafy2bzacech3yb7xlb7c57v2xh7rvmt4skeidk7z2g36llksaz4biflblbt24"
      },
      "ParentMessageReceipts": {
        "/": "bafy2bzacedswlcz5ddgqnyo3sak3jmhmkxashisnlpq6ujgyhe4mlobzpnhs6"
      },
      "Messages": {
        "/": "bafy2bzacecmda75ovposbdateg7eyhwij65zklgyijgcjwynlklmqazpwlhba"
      },
      "Timestamp": 1598306400,
      "ForkSignaling": 0,
      "ParentBaseFee": "100000000"
    }
  ],
  "Height": 0
}
```

There isn't much we can do with only the first block, so let's merge the snapshot with the diff and continue exploring.

Let's merge with the diff.

```bash
forest-tool archive merge data/forest_snapshot_mainnet_2020-08-24_height_0.forest.car.zst data/forest_diff_mainnet_2020-08-24_height_0+3000.forest.car.zst  -o data/forest_merged_snapshot.forest.car.zst
```

Now compressing it? Not sure if needed.

```bash
forest-tool snapshot compress data/forest_merged_snapshot.forest.car.zst  -o data/forest_merged_compressed_snapsh
ot.forest.car.zst
```

Load the merged compressed snapshot and serve the RPC endpoint again.

```bash
forest-tool api serve data/forest_merged_compressed_snapshot.forest.car.zst
```

Wait a little bit for the `Ready for RPC connections`... and, let's get the first block CIDs of the tipset at height 2999 and store them in a variable.

```bash
BLOCK_CID=$(curl -sX POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetTipSetByHeight",
      "params": [2999, null],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq -c '.result.Cids.[0]')

echo $BLOCK_CID
```

Sweet! Got `{"/":"bafy2bzaceb24byzgj7fn74owp7p34d3dratvqj6gy5mtb4ypl3g6a6th5pjga"}`.

Now let's get the tipset messages of that block at height 2999 by using the CIDs we just got in the params.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetParentMessages",
      "params": ['$BLOCK_CID'],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0
```

Getting `{"jsonrpc":"2.0","result":null,"id":1}`.

TO BE CONTINUED...
