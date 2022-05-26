from hashlib import sha256
from random import randint
from settings import get_ip, ROOT
from comunicate import alert_new_transaction
import os
import pandas as pd
import time
import json
import threading


sem = threading.Semaphore()


class User():
        id = 0
        def __init__(self, adress):
            self.count = User.id
            self.adress = adress
            self.voted = False
            User.id +=1


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):

        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
    
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True, default=vars)
        return sha256(block_string.encode()).hexdigest()


class BlockChain():

    class EventUserCreated():
        def __init__(self, adress):
            self.date = time.time()
            self.adress = adress
            self.notes = "Adress Created"

    class EventNodeCreated():
        def __init__(self, adress, ip) -> None:
            self.adress = adress
            self.ip = ip

    class EventVote():
        def __init__(self, option, user):
            self.user = user
            self.option = option
            

    difficulty = 3
    
    
    def __init__(self):

        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis()
        
    
    def create_genesis(self):
        self.nodes = {
            }
        self.users = []
        self.votes = {
            "Partido A": 0,
            "Partido B": 0,
            "Partido C": 0,
            "Partido D": 0,
        }
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        genesis_block.mineDate = time.time()
        self.add_node("0x0", get_ip())
        self.add_user(User("0x0"))
        self.chain.append(genesis_block)

    def last_block(self):
        return self.chain[-1]


    def add_vote_transaction(self, option, user):
        self.add_new_transaction(self.EventVote(option, user))
        user.voted = True
        alert_new_transaction(self, User, self.nodes.values())

    def add_vote(self, option, user):
        if option == 1:
            self.votes["Partido A"] +=1
        elif option == 2:
            self.votes["Partido B"] += 1
        elif option == 3:
            self.votes["Partido C"] += 1
        elif option == 4:
            self.votes["Partido D"] += 1
        

    def add_node_transaction(self, adress, ip):
        self.add_new_transaction(self.EventNodeCreated(adress, ip))
        alert_new_transaction(self, User, self.nodes.values())

    def add_node(self, adress, ip):
        self.nodes[adress] = ip
        url = os.path.join(ROOT, "ip_nodes.csv")
        if os.path.isfile(url):
            df = pd.read_csv(url)
            df.append([ip])
        else:
            df = pd.DataFrame({"ip_nodes": [ip]})
            df.to_csv(url, index=False)


    def add_user_transaction(self, user):
        self.add_new_transaction(self.EventUserCreated(user.adress))
        alert_new_transaction(self, User, self.nodes.values())

    def add_user(self, user):
        sem.acquire()
        self.users.append(user)
        sem.release()

    def proof_of_work(self, block):
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0" * self.difficulty):
            block.nonce += randint(1, 34566)
            computed_hash = block.compute_hash()
        return computed_hash
    

    def add_block(self, block, proof):
        previous_hash = self.last_block().hash

        if previous_hash != block.previous_hash:
            return False
        
        if not self.is_valid(block, proof):
            return False

        block.hash = proof
        block.mineDate = time.time()
        self.chain.append(block)
        return True

    def is_valid(self, block, block_hash):
        return (block_hash.startswith("0" * self.difficulty) and block_hash == block.compute_hash())


    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        sem.acquire()

        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block()

        new_block = Block(index=last_block.index + 1, transactions=self.unconfirmed_transactions, timestamp=time.time(), previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.compute_transactions(new_block.transactions)
        self.unconfirmed_transactions = []
        print("Block Mined")
        sem.release()
        return new_block.index

    def compute_transactions(self, transactions):
        for i in transactions:
            if type(i) == self.EventUserCreated:
                self.add_user(i.adress)
            elif type(i) == self.EventNodeCreated:
                self.add_node(i.adress, i.ip)
            elif type(i) == self.EventVote:
                self.add_vote(i.option)
            else:
                return False
        alert_new_transaction(self, User, self.nodes.values())