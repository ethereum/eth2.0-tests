# Permutated Index Test Generator

```
2018 Status Research & Development GmbH
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

2018 Sigma Prime
Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

This work uses public domain work under CC0 from the Ethereum Foundation
https://github.com/ethereum/eth2.0-specs
```

This file implements a test vectors generator for the `get_permutated_index` algorithm described in the Ethereum
[specs](https://github.com/ethereum/eth2.0-specs/blob/v0.2.0/specs/core/0_beacon-chain.md#get_permuted_index)

```
fork: tchaikovsky
summary: Test vectors for list shuffling using `get_permutated_index`
test_suite: permutated_index
title: Permutated Index Tests
version: 1.0
test_cases:
- {index: 0, list_size: 1024, permutated_index: 216, seed: '0xc0c7f226fbd574a8c63dc26864c27833ea931e7c70b34409ba765f3d2031633d'}
- {index: 1024, list_size: 1024, permutated_index: 433, seed: '0xb20420b2b7b1c64600cbe962544052d0bbe13da403950d198d4f4ea28762953f'}
```
