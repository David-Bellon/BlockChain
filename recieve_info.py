from xml.etree.ElementInclude import FatalIncludeError
from settings import get_all_nodes, PORT, A
import socket
import pickle
#send request to server for blochain info
nodes = get_all_nodes()


def request_info_nodes():
    if nodes != False:
        for i in nodes:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((i, PORT))
                s.send(A.encode())
                recieved_b = s.recv(4096)
                blockchain_data = pickle.loads(recieved_b)

                recieved_u = s.recv(4096)


                if recieved_b != "" and recieved_u != "":
                    return blockchain_data, recieved_u
            except:
                print("Can't connect to node ", str(i))

        return False
            
    else:
        print("Imposible to connect with nodes")
        return False
    



        

