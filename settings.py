from hashlib import sha256
import os
import requests
import random

ROOT = os.path.dirname(os.path.abspath(__file__))


def verifyPassword(password):
    url = os.path.join(ROOT, "info.txt")
    f = open(url, "r")
    id = f.readline()
    words = f.readline()
    secret = f.readline()
    f.close()
    return sha256(bytearray.fromhex(words) + bytearray.fromhex(id) + bytearray.fromhex(sha256(str(password).encode()).hexdigest())).hexdigest() == secret
    

def generateAdress(id, paswd):
    list = []
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

    response = requests.get(word_site)

    WORDS = response.content.splitlines()

    for i in range(15):
        word = random.choice(WORDS)
        list.append(word)
        WORDS.remove(word)
    

    url = os.path.join(ROOT, "info.txt")
    f = open(url, "w")
    f.write(sha256(str(id).encode()).hexdigest())
    f.write("\n")
    f.write(sha256(str(list).encode()).hexdigest())
    secret = sha256(bytearray.fromhex(sha256(str(list).encode()).hexdigest()) + bytearray.fromhex(sha256(str(id).encode()).hexdigest()) + bytearray.fromhex(sha256(str(paswd).encode()).hexdigest())).hexdigest()
    f.write("\n")
    f.write(secret)
    f.close()

    return secret