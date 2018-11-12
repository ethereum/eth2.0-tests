# ETH 2.0 Test Group Meeting
November 29, 2018
Devcon, Prague
HackMD: https://notes.ethereum.org/s/SkEnERl6Q


## Overview
This document provides the meeting minutes for the test group meeting at Devcon on Monday 29, 2018.

The primary topic of discussion surrounded YAML test configuration formatting.

### Reference Documentation:
[1.0 Tests](https://ethereum-tests.readthedocs.io/en/latest/)
[Notes on 1.0 Tests](https://github.com/status-im/nimbus/wiki/Understanding-and-debugging-Nimbus-EVM-JSON-tests)
[Test Suite](https://github.com/ethereum/tests)
[Network Tests](https://notes.ethereum.org/s/ByYhlJBs7)


## Current Situation
- Test format: YAML
    - Comments and outcomes in test
- ETH 1.0
    - Transaction test
        - Before
        - After
        - Adding YAML in 1.0
        - Tags
- Blockchain test
- Cannot put manually expected result
- Mistake output tests in repo
- 20k files -> build, artifacts

## Test Coverage
- Normal cases
- Edge cases
    - Overflow
    - Gas exhaustion
- Client confidence

## Categories

- Transaction/Opcode (stateless)
- Utiles/Tooling
    - BLS
    - SSZ
    - Shuffling
- State/Blockchain
- Network
    - Latency
    - Throughput

## Stateless Tests

Input -> Processing -> Output

Examples:
- SSZ
- Fork choice
- BLS
- Shuffling

*See current `test-format.md`*

## `Test-format.md`

- Test_suite
    - Is this needed?
    - Clearer name
- Map output to forks
- Changing gas prices
- Pragmatic, start and if these are resistant, change the format
- Doc for test-format
- Try to reuse name and structure from 1.0

## Additional Topics
- Incentives for contributing to tests
- EIPs with test vectors
- Bounties
