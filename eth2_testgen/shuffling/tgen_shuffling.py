import random
import sys
from typing import Any, Dict, List

import yaml

from constants import ENTRY_EXIT_DELAY, FAR_FUTURE_EPOCH
from core_helpers import get_shuffling
from yaml_objects import Validator


def noop(self, *args, **kw):
    # Prevent !!str or !!binary tags
    pass


yaml.emitter.Emitter.process_tag = noop


EPOCH = 1000  # The epoch, also a mean for the normal distribution

# Standard deviation, around 8% validators will activate or exit within
# ENTRY_EXIT_DELAY inclusive from EPOCH thus creating an edge case for validator
# shuffling
RAND_EPOCH_STD = 35

MAX_EXIT_EPOCH = 5000  # Maximum exit_epoch for easier reading


if __name__ == '__main__':

    # Order not preserved - https://github.com/yaml/pyyaml/issues/110
    metadata = {
        'title': 'Shuffling Algorithm Tests',
        'summary': 'Test vectors for validator shuffling. Note: only relevant validator fields are defined.',
        'test_suite': 'shuffle',
        'fork': 'tchaikovsky',
        'version': 1.0
    }

    # Config
    random.seed(int("0xEF00BEAC", 16))
    num_cases = 10

    test_cases = []
    for case in range(num_cases):
        seedhash = bytes(random.randint(0, 255) for byte in range(32))
        idx_max = random.randint(128, 512)

        validators = []
        for idx in range(idx_max):
            v = Validator(original_index=idx)
            # 4/5 of all validators are active
            if random.random() < 0.8:
                # Choose a normally distributed epoch number
                rand_epoch = round(random.gauss(EPOCH, RAND_EPOCH_STD))

                # for 1/2 of *active* validators rand_epoch is the activation epoch
                if random.random() < 0.5:
                    v.activation_epoch = rand_epoch

                    # 1/4 of active validators will exit in forseeable future
                    if random.random() < 0.5:
                        v.exit_epoch = random.randint(
                            rand_epoch + ENTRY_EXIT_DELAY + 1, MAX_EXIT_EPOCH)
                    # 1/4 of active validators in theory remain in the set indefinitely
                    else:
                        v.exit_epoch = FAR_FUTURE_EPOCH
                # for the other active 1/2 rand_epoch is the exit epoch
                else:
                    v.activation_epoch = random.randint(
                        0, rand_epoch - ENTRY_EXIT_DELAY)
                    v.exit_epoch = rand_epoch

            # The remaining 1/5 of all validators is not activated
            else:
                v.activation_epoch = FAR_FUTURE_EPOCH
                v.exit_epoch = FAR_FUTURE_EPOCH

            validators.append(v)

        input_ = {
            'validators': validators,
            'epoch': EPOCH
        }
        output = get_shuffling(
            seedhash, validators, input_['epoch'])

        test_cases.append({
            'seed': '0x' + seedhash.hex(), 'input': input_, 'output': output
        })

    with open(sys.argv[1], 'w') as outfile:
        # Dump at top level
        yaml.dump(metadata, outfile, default_flow_style=False)
        # default_flow_style will unravel "ValidatorRecord" and "committee" line, exploding file size
        yaml.dump({'test_cases': test_cases}, outfile)
