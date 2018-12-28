# Eth 2.0 test vectors generators

[![Join the chat at https://gitter.im/eth2-0-tests/Lobby](https://badges.gitter.im/eth2-0-tests/Lobby.svg)](https://gitter.im/eth2-0-tests/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Test vectors generators based on the specifications at https://github.com/ethereum/eth2.0-specs.

This repo serves as the common tests across eth2.0 implementations. See [YAML testing format](https://github.com/ethereum/eth2.0-specs/blob/master/specs/test-format.md).

## Getting Started

```
make
```

## Implementation

As much as possible the generators copy-paste the specifications. If an example implementation
is not available in the specifications, the generator will be implemented using one of the
Ethereum Foundation library instead.


## License

Similar to Eth 2.0 specifications, all code and generated test vectors
are public domain under [CC0](https://creativecommons.org/publicdomain/zero/1.0/)
