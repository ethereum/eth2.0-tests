# BLS test vectors generator
# Usage:
#   "python tgen_bls path/to/output.yml"

# Standard library
import random
import sys
from typing import Any, Dict, List, Tuple

# Third-party
import yaml

# Ethereum
from eth_utils import int_to_big_endian, big_endian_to_int

# Local imports
import bls
from hash import hash_eth2

# Explanation of BLS12-381 type hierarchy
# The base unit is uint384 of which only 381 bits are used
#
#   - FQ: uint381 modulo field modulus
#   - FQ2: (FQ, FQ)
#   - G2: (FQ2, FQ2, FQ2)

#  Resources:
#   - Eth2.0 spec:
#     https://github.com/ethereum/eth2.0-specs/blob/master/specs/bls_signature.md
#
#   - Finite Field Arithmetic
#     http://www.springeronline.com/sgw/cda/pageitems/document/cda_downloaddocument/0,11996,0-0-45-110359-0,00.pdf
#
#     Chapter 2 of
#       Elliptic Curve Cryptography
#       Darrel Hankerson, Alfred Menezes, and Scott Vanstone 
#       http://cacr.uwaterloo.ca/ecc/
#
#    - Zcash BLS parameters:
#      https://github.com/zkcrypto/pairing/tree/master/src/bls12_381
#
#    - Trinity implementation:
#      https://github.com/ethereum/trinity/blob/master/eth2/_utils/bls.py
#
#  Comments:
#    - Compared to Zcash, Ethereum specs always requires the compressed form
#      (c_flag / most significant bit always set).

def int_to_hex(n: int) -> str:
    return '0x' + int_to_big_endian(n).hex()

# Note: even though a domain is only an uint64,
# To avoid issues with YAML parsers that are limited to 53-bit (JS language limit)
# It is serialized as an hex string as well.
DOMAINS = [
    0,
    1,
    1234,
    2**32-1,
    2**64-1
]

MESSAGES = [
    b'message',
    b'Bigger message',
    b'Very .............. long ............. message .... with entropy: 1234567890-beacon-chain'
]

PRIVKEYS = [
    # Private keys are 48 bytes, Keccack hashing only produces 32 bytes
    # So we concat two and slice
    big_endian_to_int((hash_eth2(b'Alice') + hash_eth2(b'ecilA'))[:48]),
    big_endian_to_int((hash_eth2(b'Bob') + hash_eth2(b'boB'))[:48]),
    big_endian_to_int((hash_eth2(b'Eve') + hash_eth2(b'evE'))[:48])
]

def hash_message(msg: bytes, domain: int,) -> Tuple[Tuple[str, str], Tuple[str, str], Tuple[str, str]]:
    ## Hash message
    ## Input:
    ##   - Message as bytes
    ##   - domain as uint64
    ## Output:
    ##   - Message hash as a G2 point (Tuple[Tuple[str, str], Tuple[str, str], Tuple[str, str]])
    fq2x3 = []
    for fq2 in bls.hash_to_G2(msg, domain):
        fqx2 = []
        for fq in fq2.coeffs: # from py_ecc
            fqx2.append(int_to_hex(fq))
        fq2x3.append(fqx2)
    return fq2x3

def hash_message_compressed(msg: bytes, domain: int) -> Tuple[str, str]:
    ## Hash message
    ## Input:
    ##   - Message as bytes
    ##   - domain as uint64
    ## Output:
    ##   - Message hash as a compressed G2 point
    result = []
    for n in bls.compress_G2(bls.hash_to_G2(msg, domain)):
        result.append(int_to_hex(n))
    return result

if __name__ == '__main__':

    # Order not preserved - https://github.com/yaml/pyyaml/issues/110
    metadata = {
        'title': 'BLS signature and aggregation tests',
        'summary': 'Test vectors for BLS signature',
        'test_suite': 'bls',
        'fork': 'tchaikovsky',
        'version': 1.0
    }

    # 
    case01_message_hash_G2_uncompressed = []
    for msg in MESSAGES:
        for domain in DOMAINS:
            case01_message_hash_G2_uncompressed.append({
                'input': {'message': '0x' + msg.hex(), 'domain': int_to_hex(domain)},
                'output': hash_message(msg, domain)
            })

    # 
    case02_message_hash_G2_compressed = []
    for msg in MESSAGES:
        for domain in DOMAINS:
            case02_message_hash_G2_compressed.append({
                'input': {'message': '0x' + msg.hex(), 'domain': int_to_hex(domain)},
                'output': hash_message_compressed(msg, domain)
            })
    
    #
    case03_private_to_public_key = []
    pubkeys = [] # Used in later cases
    pubkeys_serial = [] # Used in public key aggregation
    for privkey in PRIVKEYS:
        pubkey = bls.privtopub(privkey)
        pubkey_serial = int_to_hex(pubkey)
        case03_private_to_public_key.append({
            'input': int_to_hex(privkey),
            'output': pubkey_serial
        })
        pubkeys.append(pubkey)
        pubkeys_serial.append(pubkey_serial)

    #
    case04_sign_messages = []
    sigs = [] # used in verify
    for privkey in PRIVKEYS:
        for message in MESSAGES:
            for domain in DOMAINS:
                sig = bls.sign(message, privkey, domain)
                sig_serial = [int_to_hex(x) for x in sig]
                case04_sign_messages.append({
                    'input': {
                        'privkey': int_to_hex(privkey),
                        'message': '0x' + msg.hex(),
                        'domain': int_to_hex(domain)
                    },
                    'output': sig_serial
                })
                sigs.append(sig)

    # This takes too long, empty for now
    case05_verify_messages = []
    # for pubkey in pubkeys:
    #     for sig in sigs:
    #         for message in MESSAGES:
    #             for domain in DOMAINS:
    #                 case04_sign_messages.append({
    #                     'input': {
    #                         'pubkey': int_to_hex(pubkey),
    #                         'message': '0x' + msg.hex(),
    #                         'signature': sig,
    #                         'domain': domain
    #                     },
    #                     'output': bls.verify(message, pubkey, sig, domain)
    #                 })

    #
    case06_aggregate_sigs = []
    for domain in DOMAINS:
        for message in MESSAGES:
            sigs = []
            sigs_serial = []
            for privkey in PRIVKEYS:
                sig = bls.sign(message, privkey, domain)
                sigs.append(sig)
                sigs_serial.append([int_to_hex(x) for x in sig])
            case06_aggregate_sigs.append({
                'input': sigs_serial,
                'output': [int_to_hex(x) for x in bls.aggregate_signatures(sigs)]
            })

    #
    case07_aggregate_pubkeys = {
        'input': pubkeys_serial,
        'output': int_to_hex(bls.aggregate_pubkeys(pubkeys))
    }

    # TODO
    # Aggregate verify

    # TODO
    # Proof-of-possession

    with open(sys.argv[1], 'w') as outfile:
        # Dump at top level
        yaml.dump(metadata, outfile, default_flow_style=False)
        # default_flow_style will unravel "ValidatorRecord" and "committee" line, exploding file size
        yaml.dump({'case01_message_hash_G2_uncompressed': case01_message_hash_G2_uncompressed}, outfile)
        yaml.dump({'case02_message_hash_G2_compressed': case02_message_hash_G2_compressed}, outfile)
        yaml.dump({'case03_private_to_public_key': case03_private_to_public_key}, outfile)
        yaml.dump({'case04_sign_messages': case04_sign_messages}, outfile)

        # Too time consuming to generate
        # yaml.dump({'case05_verify_messages': case05_verify_messages}, outfile)
        yaml.dump({'case06_aggregate_sigs': case06_aggregate_sigs}, outfile)
        yaml.dump({'case07_aggregate_pubkeys': case07_aggregate_pubkeys}, outfile)