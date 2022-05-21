import socket
import pickle
from settings import PORT, A

def send_blockchain_info(blockchain):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('', PORT))

    s.listen(5)

    while True:
        c, addr = s.accept()
        recieved = c.recv(1024).decode()
        if recieved == A:
            data = pickle.dumps(blockchain)
            c.send(data)
        else:
            c.send("none")
        c.close()