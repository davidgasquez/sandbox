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
forest-tool api serve data/forest_*
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

Let's see `ChainHead` for example.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainHead",
      "params": [],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq '.result.Height'
```

You should get `3000`!

Now, we can get any tipset from height 0 to 3000. Let's get the tipset at height 2000.

```bash
BLOCK_CID=$(curl -sX POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetTipSetByHeight",
      "params": [2000, null],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq -c '.result.Cids.[0]')

echo $BLOCK_CID
```

Sweet! Got `{"/":"bafy2bzacealmy4ndoghpt2nnwa2cw4vbyhh57knnxa3szzmus6mbizjeorq3e"}`.

Now let's get the CIDs of the messages of that tipset (height 2000) by using the Block CID we just got from `ChainGetTipSetByHeight`.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetParentMessages",
      "params": ['$BLOCK_CID'],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq -r '.result[].Cid."/"' | sort
```

The last one I've got is `bafy2bzacedzyo6iivqfrtheortwkmisle3p6icfp56pmwt7muhpddfj6n25xm`. We can [search for the message with that CID in FilFox](https://filfox.info/en/message/bafy2bzacedzyo6iivqfrtheortwkmisle3p6icfp56pmwt7muhpddfj6n25xm?t=1) and compare the results with the ones we got from the RPC.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetMessage",
      "params": [{"/":"bafy2bzacedzyo6iivqfrtheortwkmisle3p6icfp56pmwt7muhpddfj6n25xm"}],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq '.result'
```

Which gives us:

```json
{
  "Version": 0,
  "To": "f02398",
  "From": "f3ufiyjlx6rdk4u5qsekbrzr3b3ho536esjc4tbvjlzrhcvulnnhramebnhpcre3tzvvndgmjkftgntbrlrdja",
  "Nonce": 33741,
  "Value": "0",
  "GasLimit": 53115946,
  "GasFeeCap": "241359419",
  "GasPremium": "1",
  "Method": 7,
  "Params": "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",
  "CID": {
    "/": "bafy2bzacedzyo6iivqfrtheortwkmisle3p6icfp56pmwt7muhpddfj6n25xm"
  }
}
```

We can decode it's [`params` field with `StateDecodeParams`](https://github.com/filecoin-project/lotus/blob/master/api/api_full.go#L455):

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.StateDecodeParams",
      "params": ["f02398", 7,"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", [{"/": "bafy2bzacealmy4ndoghpt2nnwa2cw4vbyhh57knnxa3szzmus6mbizjeorq3e"},{"/": "bafy2bzaceafatug7se2uu7kv3vk556nauf4q62wrlgkzyhldipzczuu7byfpy"},{"/": "bafy2bzacecqlgmd6q5nbejgnjdrmdgphvdtawipthymesqbi52tm4vxvmevvc"},{"/": "bafy2bzaceckns77n64soazv7kklaoazp6lepvxkfzfgsemvyzxrmwesv2vn44"}]],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0
```

Getting `Method not found`. Not sure what's going on here.

## Exploring State

Can we call things like `StateListMiners`?

Get the tipset CIDs at height 2000.

```bash
TIPSET=$(curl -sX POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetTipSetByHeight",
      "params": [2000, null],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq -rc '.result.Cids')

echo $TIPSET
```

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.StateListMiners",
      "params": ['$TIPSET'],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0
```

Getting:

```json
{
    "jsonrpc":"2.0",
    "error": {
        "code":-32603,
        "message":"Unknown power actor code bafkqaetgnfwc6mjpon2g64tbm5sxa33xmvza"
    },
    "id":1
}
```
