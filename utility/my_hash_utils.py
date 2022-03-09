import hashlib
import json


def my_hash(value):
    return hashlib.sha256(value).hexdigest()


def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block["transactions"] = [t.to_ordered_dict()
                                      for t in hashable_block["transactions"]]
    return my_hash(json.dumps(hashable_block, sort_keys=True).encode())
