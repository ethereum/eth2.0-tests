# Shuffling Test Generator

```
2018 Status Research & Development GmbH
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

This work uses public domain work under CC0 from the Ethereum Foundation
https://github.com/ethereum/eth2.0-specs
```


This file implements a test vectors generator for the shuffling algorithm described in the Ethereum
[specs](https://github.com/ethereum/eth2.0-specs/blob/2983e68f0305551083fac7fcf9330c1fc9da3411/specs/core/0_beacon-chain.md#get_new_shuffling)



Reference picture: 

![](https://vitalik.ca/files/ShuffleAndAssign.png)

and [description](https://github.com/ethereum/py-evm/blob/f2d0d5d187400ba46a6b8f5b1f1c9997dc7fbb5a/eth/beacon/helpers.py#L272-L344) from Py-EVM

```
validators:
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
After shuffling:
    [6, 0, 2, 12, 14, 8, 10, 4, 9, 1, 5, 13, 15, 7, 3, 11]
Split by slot:
    [
        [6, 0, 2, 12, 14], [8, 10, 4, 9, 1], [5, 13, 15, 7, 3, 11]
    ]
Split by shard:
    [
        [6, 0], [2, 12, 14], [8, 10], [4, 9, 1], [5, 13, 15] ,[7, 3, 11]
    ]
Fill to output:
    [
        # slot 0
        [
            ShardAndCommittee(shard_id=0, committee=[6, 0]),
            ShardAndCommittee(shard_id=1, committee=[2, 12, 14]),
        ],
        # slot 1
        [
            ShardAndCommittee(shard_id=2, committee=[8, 10]),
            ShardAndCommittee(shard_id=3, committee=[4, 9, 1]),
        ],
        # slot 2
        [
            ShardAndCommittee(shard_id=4, committee=[5, 13, 15]),
            ShardAndCommittee(shard_id=5, committee=[7, 3, 11]),
        ],
    ]
```