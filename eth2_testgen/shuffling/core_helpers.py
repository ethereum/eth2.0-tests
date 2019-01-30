"""
copy-pasted from specs. Compatible with v0.1:
https://github.com/ethereum/eth2.0-specs/releases/tag/v0.1
"""

from typing import Any, Dict, List, NewType

import yaml
from eth_typing import Hash32

from constants import EPOCH_LENGTH, SHARD_COUNT, TARGET_COMMITTEE_SIZE
from utils import hash
from yaml_objects import Validator

EpochNumber = NewType("EpochNumber", int)
ValidatorIndex = NewType("ValidatorIndex", int)
Bytes32 = NewType("Bytes32", bytes)


def is_active_validator(validator: Validator, epoch: EpochNumber) -> bool:
    """
    Check if ``validator`` is active.
    """
    return validator.activation_epoch <= epoch < validator.exit_epoch


def get_active_validator_indices(validators: List[Validator], epoch: EpochNumber) -> List[ValidatorIndex]:
    """
    Get indices of active validators from ``validators``.
    """
    return [i for i, v in enumerate(validators) if is_active_validator(v, epoch)]


def shuffle(values: List[Any], seed: Bytes32) -> List[Any]:
    """
    Return the shuffled ``values`` with ``seed`` as entropy.
    """
    values_count = len(values)

    # Entropy is consumed from the seed in 3-byte (24 bit) chunks.
    rand_bytes = 3
    # The highest possible result of the RNG.
    rand_max = 2 ** (rand_bytes * 8) - 1

    # The range of the RNG places an upper-bound on the size of the list that
    # may be shuffled. It is a logic error to supply an oversized list.
    assert values_count < rand_max

    output = [x for x in values]
    source = seed
    index = 0
    while index < values_count - 1:
        # Re-hash the `source` to obtain a new pattern of bytes.
        source = hash(source)
        # Iterate through the `source` bytes in 3-byte chunks.
        for position in range(0, 32 - (32 % rand_bytes), rand_bytes):
            # Determine the number of indices remaining in `values` and exit
            # once the last index is reached.
            remaining = values_count - index
            if remaining == 1:
                break

            # Read 3-bytes of `source` as a 24-bit big-endian integer.
            sample_from_source = int.from_bytes(source[position:position + rand_bytes], 'big')

            # Sample values greater than or equal to `sample_max` will cause
            # modulo bias when mapped into the `remaining` range.
            sample_max = rand_max - rand_max % remaining

            # Perform a swap if the consumed entropy will not cause modulo bias.
            if sample_from_source < sample_max:
                # Select a replacement index for the current index.
                replacement_position = (sample_from_source % remaining) + index
                # Swap the current index with the replacement index.
                output[index], output[replacement_position] = output[replacement_position], output[index]
                index += 1
            else:
                # The sample causes modulo bias. A new sample should be read.
                pass

    return output


def split(values: List[Any], split_count: int) -> List[List[Any]]:
    """
    Splits ``values`` into ``split_count`` pieces.
    """
    list_length = len(values)
    return [
        values[(list_length * i // split_count): (list_length * (i + 1) // split_count)]
        for i in range(split_count)
    ]

def get_epoch_committee_count(active_validator_count: int) -> int:
    return max(
        1,
        min(
            SHARD_COUNT // EPOCH_LENGTH,
            active_validator_count // EPOCH_LENGTH // TARGET_COMMITTEE_SIZE,
        )
    ) * EPOCH_LENGTH


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(i ^ j for (i, j) in zip(a, b))


def int_to_bytes32(x) -> bytes:
    return x.to_bytes(32, 'big')


def get_shuffling(seed: Bytes32, validators: List[Validator], epoch: EpochNumber) -> List[List[ValidatorIndex]]:
    """
    Shuffles ``validators`` into crosslink committees seeded by ``seed`` and ``epoch``.
    Returns a list of ``committees_per_epoch`` committees where each
    committee is itself a list of validator indices.
    """

    active_validator_indices = get_active_validator_indices(validators, epoch)

    committees_per_epoch = get_epoch_committee_count(
        len(active_validator_indices))

    # Shuffle
    seed = xor(seed, int_to_bytes32(epoch))
    shuffled_active_validator_indices = shuffle(active_validator_indices, seed)

    # Split the shuffled list into committees_per_epoch pieces
    return split(shuffled_active_validator_indices, committees_per_epoch)
