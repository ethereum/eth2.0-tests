"""
copy-pasted from specs
"""

from typing import Any, Dict, List

import yaml
from eth_typing import Hash32

from constants import EPOCH_LENGTH, SHARD_COUNT, TARGET_COMMITTEE_SIZE
from enums import ValidatorStatusCode
from utils import hash
from yaml_objects import ShardCommittee, ValidatorRecord


def is_active_validator(validator: ValidatorRecord) -> bool:
    """
    Checks if ``validator`` is active.
    """
    return validator.status in [ValidatorStatusCode.ACTIVE, ValidatorStatusCode.ACTIVE_PENDING_EXIT]


def get_active_validator_indices(validators: [ValidatorRecord]) -> List[int]:
    """
    Gets indices of active validators from ``validators``.
    """
    return [i for i, v in enumerate(validators) if is_active_validator(v)]


def shuffle(values: List[Any], seed: Hash32) -> List[Any]:
    """
    Returns the shuffled ``values`` with ``seed`` as entropy.
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
            sample_from_source = int.from_bytes(
                source[position:position + rand_bytes], 'big')

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


def split(values: List[Any], split_count: int) -> List[Any]:
    """
    Splits ``values`` into ``split_count`` pieces.
    """
    list_length = len(values)
    return [
        values[
            (list_length * i // split_count): (list_length * (i + 1) // split_count)
        ]
        for i in range(split_count)
    ]


def get_new_shuffling(seed: Hash32,
                      validators: List[ValidatorRecord],
                      crosslinking_start_shard: int) -> List[List[ShardCommittee]]:
    """
    Shuffles ``validators`` into shard committees using ``seed`` as entropy.
    """
    active_validator_indices = get_active_validator_indices(validators)

    committees_per_slot = max(
        1,
        min(
            SHARD_COUNT // EPOCH_LENGTH,
            len(active_validator_indices) // EPOCH_LENGTH // TARGET_COMMITTEE_SIZE,
        )
    )

    # Shuffle with seed
    shuffled_active_validator_indices = shuffle(active_validator_indices, seed)

    # Split the shuffled list into epoch_length pieces
    validators_per_slot = split(
        shuffled_active_validator_indices, EPOCH_LENGTH)

    output = []
    for slot, slot_indices in enumerate(validators_per_slot):
        # Split the shuffled list into committees_per_slot pieces
        shard_indices = split(slot_indices, committees_per_slot)

        shard_id_start = crosslinking_start_shard + slot * committees_per_slot

        shard_committees = [
            ShardCommittee(
                shard=(shard_id_start + shard_position) % SHARD_COUNT,
                committee=indices,
                total_validator_count=len(active_validator_indices),
            )
            for shard_position, indices in enumerate(shard_indices)
        ]
        output.append(shard_committees)

    return output
