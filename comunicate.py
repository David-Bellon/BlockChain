from xml.etree.ElementInclude import FatalIncludeError
from settings import get_all_nodes, PORT_1, PORT_2, A, B, C
import socket
import pickle
import time
#send request to server for blochain info
nodes = get_all_nodes()


def request_info_nodes():
    if nodes != False:
        for i in nodes:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((i, PORT_1))
                s.send(A.encode())

                recieved_b = s.recv(4096)
                blockchain_data = pickle.loads(recieved_b)

                recieved_u = s.recv(4096)
                user_data = pickle.loads(recieved_u)


                if recieved_b != "" and recieved_u != "":
                    return blockchain_data, user_data
            except:
                print("Can't connect to node ", str(i))

        return False
            
    else:
        print("Imposible to connect with nodes")
        return False

def alert_new_transaction(blockchain, user, nodes):
    if nodes != False:
        for i in nodes:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((i, PORT_2))
                s.send(B.encode())
                verify = s.recv(1024).decode()
                if verify == C:
                    data = pickle.dumps(blockchain)
                    s.send(data)
                    time.sleep(1)
                    data = pickle.dumps(user)
                    s.send(data)
            except:
                return "Impossible to connect to that node"
    else:
        return False