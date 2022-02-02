from hashlib import sha256
import json

class Block:
    def __init__(self, index, transactions, timestamp):

        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
    
    def compute_has(block):
        block_string = json.dump(block.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()