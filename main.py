from hashlib import sha256
import time
import json

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):

        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
    
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class BlockChain():
    def __init__(self):
        self.chain = []
        self.create_genesis()

    def create_genesis(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def return_last(self):
        return self.chain[-1]

        