from hashlib import sha256
import time
import json

class Block:
    def __init__(self, index, transactions, timestamp):

        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
    
    def compute_has(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

block = Block(1, "Hey como mola esto", time.time_ns())

print(block.compute_has())