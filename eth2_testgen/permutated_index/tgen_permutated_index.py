import random
import sys
from typing import Any, Dict, List

import yaml

from core_helpers import get_permuted_index
from constants import SHUFFLE_ROUND_COUNT


def noop(self, *args, **kw):
    # Prevent !!str or !!binary tags
    pass

def random_seed():
    return bytes(random.randint(0, 255) for byte in range(32))


yaml.emitter.Emitter.process_tag = noop


if __name__ == '__main__':

    # Order not preserved - https://github.com/yaml/pyyaml/issues/110
    metadata = {
        'title': 'Permutated Index Tests',
        'summary': 'Test vectors for list shuffling using `get_permutated_index`',
        'test_suite': 'permutated_index',
        'fork': 'tchaikovsky',
        'version': 1.0
    }

    # Config
    random.seed(int("0xEF00BEAC", 16))
    random_cases = 32
    max_list_size = 4096
    test_results = []

    # Manual cases
    cases = [
        {"index": 0, "list_size": 1024, "seed": random_seed()},
        {"index": 1024, "list_size": 1024, "seed": random_seed()},
    ]

    # Randomly generated cases
    for _ in range(random_cases):
        index = random.randint(0, max_list_size)
        list_size = random.randint(0, max_list_size)
        cases.append({
            "index": random.randint(0, max_list_size),
            "list_size": random.randint(0, max_list_size),
            "seed": random_seed(),
        })

    # Execute cases
    for case in cases:
        index = case["index"]
        seed = case["seed"]
        list_size = case["list_size"]

        permutated_index = get_permuted_index(index, list_size, seed)

        case["seed"] = '0x' + seed.hex()
        case["permutated_index"] = permutated_index
        case["shuffle_round_count"] = SHUFFLE_ROUND_COUNT

        test_results.append(case)

    # Write to YAML file
    with open(sys.argv[1], 'w') as outfile:
        yaml.dump(metadata, outfile, default_flow_style=False)
        yaml.dump({'test_cases': test_results}, outfile)
