import socket
import pickle
import time
from settings import PORT, A

def send_blockchain_info(blockchain, user):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('0.0.0.0', PORT))

    s.listen(5)

    while True:
        c, addr = s.accept()
        print("Connection from:", addr)
        recieved = c.recv(1024).decode()
        if recieved == A:
            print("Enviando info")
            data = pickle.dumps(blockchain)
            c.send(data)
            time.sleep(1)
            data = pickle.dumps(user)
            c.send(data)
        else:
            c.send("none")
        c.close()
