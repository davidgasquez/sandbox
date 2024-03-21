# Forest

Some random tinkering with Forest, the Rust Filecoin Node Implementation.

## Tinkering

Let's download a little and diff snapshots from the [Forest Archive](https://forest-archive.chainsafe.dev/list/), add it to a `snapshots` folder.

```bash
mkdir snapshots
wget https://forest-archive.chainsafe.dev/mainnet/lite/forest_snapshot_mainnet_2024-01-06_height_3540000.forest.car.zst -P snapshots
wget https://forest-archive.chainsafe.dev/mainnet/diff/forest_diff_mainnet_2024-01-07_height_3540000+3000.forest.car.zst -P snapshots
```

Running `make cli` will spin up the latest published Forest Docker image and drop you into a shell with the relevant binaries available.

```bash
make cli
```

Let's try to get some data out of the snapshots!

```bash
forest-tool api serve snapshots/forest_*
```

Wait for the `Ready for RPC connections` and then run the following command in a new shell to get info about the first block of the chain.

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetTipSetByHeight",
      "params": [3540000, null],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq '.result'
```

You should get this:

```json
{
  "Cids": [
    {
      "/": "bafy2bzacec35ks5ory5hyimqw5zu3dot3gemlv4j5uozs3gu34ak7dx5pdjho"
    },
    {
      "/": "bafy2bzaced6o66fsewzfbhx6fmhc74yxqifzhrvyucs7xkknrjhoz5p753f6y"
    },
    {
      "/": "bafy2bzaceds737e64etnw2mkzbjgdxa37wmsj73hmpqg5foridzdzg6dzylzc"
    },
    {
      "/": "bafy2bzaceddjsagvtvduzkijekqy64jhwy5bctihq3mbugdw73sp4zspf3tek"
    },
    {
      "/": "bafy2bzacedhkqbdwfxk3e2futiw4usphx5zpfbso3lvxzhp7kwrwmc7i4taz2"
    },
    {
      "/": "bafy2bzacebiazvbomkj64q2s5drfdmr2jvy7sviaurhtiebdlminhb3cez3m6"
    }
  ],
  .
  .
  .
  "Height": 3540000
}
```

Let's see `ChainHead` for example.

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainHead",
      "params": [],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq '.result.Height'
```

You should get `3543000`!

Now, we can get any tipset from height `3540000` to `3543000`. Let's get the tipset at height `3541000`.

```bash
TIPSET=$(curl -sX POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetTipSetByHeight",
      "params": [3541000, null],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq -c '.result.Cids')

echo $TIPSET
```

Sweet! Got the following:

```json
[{"/":"bafy2bzacedqqhzaoqbgj5lrtnicxrjehbzfw7yblmvja4p5hdskcpspgc6lkk"},{"/":"bafy2bzacebyw54k3jrjlyvrohof6xavjqjfyhzd3i7rmneabjkheqilk7d4ki"},{"/":"bafy2bzacectie4pdpvwkotiwiryvqgfnglcnt6fwgr4gij2ktxu3sp6bhyh62"}]
```

Now let's get the CIDs of the messages of that tipset (height `3541000`) by using the Block CID we just got from `ChainGetTipSetByHeight`.

```bash
BLOCK_CID=$(echo $TIPSET | jq -c '.[0]')
curl -s -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetParentMessages",
      "params": ['$BLOCK_CID'],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq -r '.result[].Cid."/"' | sort
```

The last one I've got is `bafy2bzacedzx4hrz5fg7bja4isqul73xjlggpy5bshxgrjpx7b5d63tn2hnpq`. We can [search for the message with that CID in FilFox](https://filfox.info/en/message/bafy2bzacedzx4hrz5fg7bja4isqul73xjlggpy5bshxgrjpx7b5d63tn2hnpq) and compare the results with the ones we got from the RPC.

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.ChainGetMessage",
      "params": [{"/":"bafy2bzacedzx4hrz5fg7bja4isqul73xjlggpy5bshxgrjpx7b5d63tn2hnpq"}],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0 | jq '.result'
```

Which gives us:

```json
{
  "Version": 0,
  "To": "f02002827",
  "From": "f3vztcuqxjpfhojsflilz3roqznqkvv5zczjxuqcmxgr7mhyeam757adpfuuukfybtf52yiqwkz6x6vr6aybca",
  "Nonce": 73062,
  "Value": "0",
  "GasLimit": 30349275,
  "GasFeeCap": "9000000000",
  "GasPremium": "99621",
  "Method": 5,
  "Params": "hQCBggBAgYINWMCMjVmFiiYeBTSrKGxRL+QXKHnyqcaIXT9jfRaGINOtXbD3BwK8k7mgZnYSdjJhpKCu8kFyRa4pBxCbjngjqQ0DnCOuEJbDVeFRfQQMSy9ElYCRYpu3kj1bhcyPWncanNgN+xC2bBuF4coFtUhk2C4jIlv+3pyCFMqcbN7V11e3ZVmR9AXfrjsayhedBksz/a+lgrNM3D3WIkQQlnDRWUffjXrjVIkb1z8fvyNm4FMuu0ae/jIfysnNNtQd25aADaIaADYH7VggkwMFWNi3tusv2md6Rkc7RJKqVZoScX1Hu9lAhf9pUrk=",
  "CID": {
    "/": "bafy2bzacedzx4hrz5fg7bja4isqul73xjlggpy5bshxgrjpx7b5d63tn2hnpq"
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
      "params": ["f02002827", 5,"hQCBggBAgYINWMCMjVmFiiYeBTSrKGxRL+QXKHnyqcaIXT9jfRaGINOtXbD3BwK8k7mgZnYSdjJhpKCu8kFyRa4pBxCbjngjqQ0DnCOuEJbDVeFRfQQMSy9ElYCRYpu3kj1bhcyPWncanNgN+xC2bBuF4coFtUhk2C4jIlv+3pyCFMqcbN7V11e3ZVmR9AXfrjsayhedBksz/a+lgrNM3D3WIkQQlnDRWUffjXrjVIkb1z8fvyNm4FMuu0ae/jIfysnNNtQd25aADaIaADYH7VggkwMFWNi3tusv2md6Rkc7RJKqVZoScX1Hu9lAhf9pUrk=", [{"/":"bafy2bzacedqqhzaoqbgj5lrtnicxrjehbzfw7yblmvja4p5hdskcpspgc6lkk"},{"/":"bafy2bzacebyw54k3jrjlyvrohof6xavjqjfyhzd3i7rmneabjkheqilk7d4ki"},{"/":"bafy2bzacectie4pdpvwkotiwiryvqgfnglcnt6fwgr4gij2ktxu3sp6bhyh62"}]],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0
```

Getting `Method not found`. Not sure what's going on here (maybe the method is not implemented in Forest yet).

## Exploring State

Can we call things like `StateListMiners`?

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  --data '{
      "jsonrpc": "2.0",
      "method": "Filecoin.StateListMiners",
      "params": ['$TIPSET'],
      "id": 1
    }' \
  http://127.0.0.1:2345/rpc/v0
```

Yes! After a while you should get a long list of miners.
