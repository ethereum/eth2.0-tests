import random
import sys
from typing import Any, Dict, List

import yaml

from constants import SHARD_COUNT
from core_helpers import get_new_shuffling
from enums import ValidatorStatusCode
from yaml_objects import ShardCommittee, ValidatorRecord


def noop(self, *args, **kw):
    # Prevent !!str or !!binary tags
    pass


yaml.emitter.Emitter.process_tag = noop


def yaml_ValidatorStatusCode(dumper, data):
    # Try to deal with enums - otherwise for "ValidatorStatus.Active" you get [1], instead of 1
    return dumper.represent_data(data.value)


yaml.add_representer(ValidatorStatusCode, yaml_ValidatorStatusCode)

if __name__ == '__main__':

    # Order not preserved - https://github.com/yaml/pyyaml/issues/110
    metadata = {
        'title': 'Shuffling Algorithm Tests',
        'summary': 'Test vectors for shuffling a list based upon a seed using `shuffle`',
        'test_suite': 'shuffle',
        'fork': 'tchaikovsky',
        'version': 1.0
    }

    # Config
    random.seed(int("0xEF00BEAC", 16))
    num_cases = 10
    list_val_state = list(ValidatorStatusCode)
    test_cases = []

    for case in range(num_cases):
        seedhash = bytes(random.randint(0, 255) for byte in range(32))
        num_val = random.randint(128, 512)
        validators = [
            ValidatorRecord(
                status=random.choice(list_val_state),
                original_index=num_val)
            for num_val in range(num_val)
        ]
        input_ = {
            'validators_status': [v.status.value for v in validators],
            'crosslinking_start_shard': random.randint(0, SHARD_COUNT)
        }
        output = get_new_shuffling(
            seedhash, validators, input_['crosslinking_start_shard'])

        test_cases.append({
            'seed': '0x' + seedhash.hex(), 'input': input_, 'output': output
        })

    with open(sys.argv[1], 'w') as outfile:
        # Dump at top level
        yaml.dump(metadata, outfile, default_flow_style=False)
        # default_flow_style will unravel "ValidatorRecord" and "committee" line, exploding file size
        yaml.dump({'test_cases': test_cases}, outfile)
