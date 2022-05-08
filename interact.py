from hashlib import sha256
from time import sleep
from main import blockchain, User
from win32api import GetSystemMetrics
from tkinter import *
from settings import *
import socket

import threading



def blockChainActions():
    master = Tk()
    width = int(GetSystemMetrics(0) * 0.7)
    height = int(GetSystemMetrics(1) * 0.7)
    resolution = str(width) + "x" + str(height)
    master.geometry(resolution)




    master.mainloop()


def main():

    def SignUp():

        if paswd_sig.get() != "" and len(paswd_sig.get()) >= 6 and not " " in paswd_sig.get():
            url = os.path.join(ROOT, "info.txt")
            if os.path.isfile(url):
                a = Label(w, text="Device Already exist. Please LogIn", bg="gray", fg="white")
                a.place(x= width / 1.44, y= height / 1.4)
                a.after(1000, a.destroy)
            else:
                secret = generateAdress(User.id, paswd_sig.get())
                blockchain.add_user(User(secret))
                ip = get_ip()
                blockchain.add_node(secret, ip)
        else:
            l = Label(w, text="Password must be more than 6 characters and not empty", bg="gray", fg="white")
            l.place(x= width / 1.57, y= height / 1.6)
            l.after(1000, l.destroy)

        if w.state == "normal":
            paswd_sig.delete(0, END)

    def LogIn():

        if paswd_log.get() != "":
            url = os.path.join(ROOT, "info.txt")
            if os.path.isfile(url):
                if verifyPassword(paswd_log.get()):
                    p = Label(w, text="Access Guranted")
                    p.place(x=width /2, y = width / 2)
                    w.destroy()
                    #Abrir otra ventana y acceso a la blockchain
                    blockChainActions()
                else:
                    b = Label(w, text="Wrong Password")
                    b.place(x=width /2, y = width / 2)
                    b.after(1300, b.destroy)
            else:
                a = Label(w, text="You are not register in the blockchain please do it", bg="gray", fg="white")
                a.place(x= width / 5.33, y= height / 1.5)
                a.after(1400, a.destroy)

        else:
            l = Label(w, text="Enter a valid password", bg="gray", fg="white")
            l.place(x= width / 4.3, y= height / 1.3)
            l.after(1000, l.destroy)

        if w.state == "normal":
            paswd_log.delete(0, END)
        
            

    w =Tk("Buenas tardes")
    width = int(GetSystemMetrics(0) * 0.7)
    height = int(GetSystemMetrics(1) * 0.7)
    resolution = str(width) + "x" + str(height)
    w.geometry(resolution)

    #Text for Log In
    label_log = Label(w, text="Log In", font=("Helvetica", 16))
    label_log.place(x= width/4, y= height / 7)
    
    #Text for sign up
    label_sig = Label(w, text="Sign In", font=("Helvetica", 16))
    label_sig.place(x= width/1.4, y= height / 7)

    #Canvas for log In
    c_log = Canvas(w, bg="gray", width= width / 4, height= height/1.6)
    c_log.place(x = width / 6.6, y= height / 4.3)

    #Canvas for Sign Up
    c_sig = Canvas(w, bg="gray", width= width / 4, height= height/1.6)
    c_sig.place(x = width / 1.6, y= height / 4.3)


    #Text and boxes for Log In

    Label(w, text="Password", font=("Helvetica", 16),bg="gray").place(x= width/4.1, y= height / 2.8)

    paswd_log = Entry(w, width=20, bd=3, show="*")
    paswd_log.place(x = width / 4.3, y = height / 2.2)

    #Text and boxes for Sign Up

    Label(w, text="Password", font=("Helvetica", 16),bg="gray").place(x= width/1.38, y= height / 2.8)
    paswd_sig = Entry(w, width=20, bd=3, show="*")
    paswd_sig.place(x = width / 1.4, y = height / 2.2)


    #Buttons to trigger functions
    Button(w, text="Log In", command=LogIn).place(x = width / 3.8, y= height / 1.8)

    Button(w, text="Sign Up", command=SignUp).place(x = width / 1.34, y= height / 1.8)

    
    w.mainloop()

def alwaysMine():

    while True:
        blockchain.mine()
        if len(blockchain.chain) - 1 == 1:
            break


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    local_ip_address = s.getsockname()[0]
    return local_ip_address

main()

'''
x = threading.Thread(target= main)
y = threading.Thread(target=alwaysMine)
x.start()
y.start()

x.join()
y.join()

print(blockchain)
'''