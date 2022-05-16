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
                s.connect(i, PORT)
            except:
                raise FatalIncludeError()

            s.send(A.encode())

            recieved = s.recv(4096)
            data = pickle.loads(recieved)

            if recieved != "":
                return data
    else:
        return "Imposible to get connect"
    



        

