"""
copy-pasted from specs
"""

from typing import Any, Dict, List
from constants import SHUFFLE_ROUND_COUNT

from eth_typing import Hash32

from utils import hash


def int_to_bytes1(x):
    return x.to_bytes(1, 'little')

def int_to_bytes4(x):
    return x.to_bytes(4, 'little')

def bytes_to_int(data: bytes) -> int:
    return int.from_bytes(data, 'little')

# Note: in the spec `seed` is of type `Bytes32`, here it is `Hash32`. I could
# not find such a type in `eth_typing` or `typing`.
def get_permuted_index(index: int, list_size: int, seed: Hash32) -> int:
    """
    Return `p(index)` in a pseudorandom permutation `p` of `0...list_size-1` with ``seed`` as entropy.

    Utilizes 'swap or not' shuffling found in
    https://link.springer.com/content/pdf/10.1007%2F978-3-642-32009-5_1.pdf
    See the 'generalized domain' algorithm on page 3.
    """
    for round in range(SHUFFLE_ROUND_COUNT):
        pivot = bytes_to_int(hash(seed + int_to_bytes1(round))[0:8]) % list_size
        flip = (pivot - index) % list_size
        position = max(index, flip)
        source = hash(seed + int_to_bytes1(round) + int_to_bytes4(position // 256))
        byte = source[(position % 256) // 8]
        bit = (byte >> (position % 8)) % 2
        index = flip if bit else index

    return index
