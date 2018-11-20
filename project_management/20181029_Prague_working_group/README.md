# Pre-devcon test group meeting

HackMD: https://notes.ethereum.org/Vh-HJcHuSyCU_qj0CY5dQQ

###### tags: `2018_prague_working_group` `testing`

> Eth2.0 test format working group

[TOC]

## Summary
Working group focused on ironing out details related to a common test framework.

## Expected Outcome

* Propose any changes or clarifications to [`test-format.md`](https://github.com/ethereum/eth2.0-specs/pull/39)
* Propose an organizational structure for tests
* Propose any number of "test suite" test case structures
    * SSZ
    * Chain tests
    * shuffle
    * etc
* Propose changes in the eth2.0 cross-client testing to

## Current Status

There is a currently a proposed general format under review [here](https://github.com/ethereum/eth2.0-specs/pull/39). The idea is to have a general outer format for each test file along with an associated `test_suite` field that defines the format for the included `test_cases`.

We are currently opting for YAML due to wide language support and support for inline comments.

There is a ton of knowledge (of what works and does not) from eth1.0 testing that we should leverage in designing this new testing framework.

## References
- PR for [`test-format.md`](https://github.com/ethereum/eth2.0-specs/pull/39)
- [Eth1.0 tests repo](https://github.com/ethereum/tests)

## Participants

* [_Lead_] Mamy Ratsimbazafy (Nimbus/Status) @mratsim
* Everett Hildenbrandt (Runtime Verification/Ethereum Foundation)
* Zak Cole (Whiteblock) @zscole
* Nate Blakely (Whiteblock)
* Raul Jordan (Prysmatic) @rauljordan
* Ryan Lipscombe (Nimbus/Status) @coffeepots
* Paweł Bylica @chfast
* Nishant Das (Prymsatic) @rauljordan
## Fork Choice Stateless Test

```yaml
# Credits to Danny Ryan (Ethereum Foundation)
---

title: Sample Ethereum 2.0 Beacon Chain Test
summary: Basic, functioning fork choice rule for Ethereum 2.0
test_suite: chain_test
test_cases:
  - case:
      config:
        validator_count: 100
        cycle_length: 8
        shard_count: 32
        min_committee_size: 8

      slots:
        # "slot_number" has a minimum of 1
        - slot_number: 1
          new_block:
            id: A
            # "*" is used for the genesis block
            parent: "*"
          attestations:
            - block: A
              # the following is a shorthand string for [0, 1, 2, 3, 4, 5]
              validators: "0-5"
        - slot_number: 2
          new_block:
            id: B
            parent: A
          attestations:
            - block: B
              validators: [0, 1, 2, 3, 4, 5]
        - slot_number: 3
          new_block:
            id: C
            parent: A
          attestations:
            # attestation "committee_slot" defaults to the slot during which the attestation occurs
            - block: C
              validators: "2-7"
            # default "committee_slot" can be directly overridden
            - block: C
              committee_slot: 2
              validators: [6, 7]
        - slot_number: 4
          new_block:
            id: D
            parent: C
          attestations:
            - block: D
              validators: "1-4"
        # slots can be skipped entirely (5 in this case)
        - slot_number: 6
          new_block:
            id: E
            parent: D
          attestations:
            - block: E
              validators: "0-4"
            - block: B
              validators: [5, 6, 7]

      results:
        head: E
        last_justified_block: "*"
        last_finalized_block: "*"
```
