import socket
import pickle
import time
from settings import PORT_1, PORT_2, A, B, C

def listen_to_request_info(blockchain, user):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('0.0.0.0', PORT_1))

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



def listen_to_new_info():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('0.0.0.0', PORT_2))

    s.listen(5)

    while True:
        c, addr = s.accept()
        print("Connection from:", addr)
        recieved = c.recv(1024).decode()

        if recieved == B:
            c.send(C.encode())

            recieved_b = s.recv(4096)
            blockchain_data = pickle.loads(recieved_b)

            recieved_u = s.recv(4096)
            user_data = pickle.loads(recieved_u)

            if recieved_b != "" and recieved_u != "":
                return blockchain_data, user_data
        else:
            c.send("none")
        c.close()