from hashlib import sha256
from xml.etree.ElementInclude import FatalIncludeError

import pandas as pd
import os
import requests
import random
import socket

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT_1 = 5647
PORT_2 = 5648

A = "f077da9fe55fee31284d9a09456c3652991e37e1babc53deb92546a477f856cf"
B = "66912966cd4e07b9a1b1ce551b66e9ca4449d54f17ab703023eb6d9723501554"
C = "f54c05823757695c0b4fa9154f2ee331a21ea7f538bef46f8c7ce83055c522ad"

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

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    local_ip_address = s.getsockname()[0]
    return local_ip_address

def get_all_nodes():
    try:
        df = pd.read_csv("Blockchain\ip_nodes.csv")
        return list(df["ip_nodes"])
    except:
        return False
