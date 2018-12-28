from typing import Any

import yaml


class ValidatorRecord(yaml.YAMLObject):
    fields = {
        # Status code
        'status': 'ValidatorStatusCode',
        # Extra index field to ease testing/debugging
        'original_index': 'uint64'
    }

    def __init__(self, **kwargs):
        for k in self.fields.keys():
            setattr(self, k, kwargs.get(k))

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


class ShardCommittee(yaml.YAMLObject):
    fields = {
        # Shard number
        'shard': 'uint64',
        # Validator indices
        'committee': ['uint24'],
        # Total validator count (for proofs of custody)
        'total_validator_count': 'uint64',
    }

    def __init__(self, **kwargs):
        for k in self.fields.keys():
            setattr(self, k, kwargs.get(k))

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)
