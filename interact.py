from listen import listen_to_request_info
from comunicate import request_info_nodes
from win32api import GetSystemMetrics
from tkinter import *
from settings import *
from to_use import *

import threading



def blockChainActions(address, current_user):

    current_user = current_user[0]
    def expand(event):
        w = event.widget
        try:
            index = int(w.curselection()[0])
        except:
            return False
        transac = w.get(index)
        
        for i in blockchain.unconfirmed_transactions:
            if transac == str(i):
                l = Listbox(master, width = 100, height= 23)
                variables = [attr for attr in dir(i) if not callable(getattr(i, attr)) and not attr.startswith("__")]
                for j in variables:
                    text = str(j) + ": " + str(getattr(i, j))
                    l.insert(0, text)

        l.place(x = width + 30, y = height * 0.1)

    def show_pending_transactions():
        while True:
            if len(blockchain.unconfirmed_transactions) == 0:
                if blo_trans.size() != 0:
                    blo_trans.delete(0, END)
            else:
                if blo_trans.size() == 0:
                    for i in blockchain.unconfirmed_transactions:
                        blo_trans.insert(0,i)
                else:
                    for i in blockchain.unconfirmed_transactions:
                        if str(i) not in blo_trans.get(0, END):
                            blo_trans.insert(0,i)


    def vote(option):
        if option.get() != 0:
            if current_user.voted == False:
                blockchain.add_vote_transaction(option.get(), current_user)
            else:
                print("User Already Voted")
        else:
            z = Label(master, text="Elija una opcion")
            z.place(x = width - 1300, y = height * 0.73)
            z.after(1300, z.destroy)
            
    def infinite_mine():
        #while True:5
        blockchain.mine()

    def start_mine():
        x = threading.Thread(target=infinite_mine)
        x.start()
        print("Started Mining")


    master = Tk()
    width = int(GetSystemMetrics(0) * 0.7)
    height = int(GetSystemMetrics(1) * 0.7)
    v = Scrollbar(master)
    v.pack(side= RIGHT,fill= Y)
    h = Scrollbar(master, orient="horizontal")
    h.pack(side = BOTTOM, fill = X)
    resolution = str(width) + "x" + str(height)
    master.geometry(resolution)

    #Show all the pending transactions in a list
    text = Label(master, text= str(address), font=("Helvetica", 9), background="grey")
    text.place(x= width - 465, y= height *0.02)

    blo_trans = Listbox(master, width=70,height= 50, yscrollcommand= v.set, xscrollcommand=h.set)

    blo_trans.place(x= width - 470, y = height * 0.1)

    v.config(command=blo_trans.yview)
    h.config(command=blo_trans.xview)

    blo_trans.bind('<<ListboxSelect>>', expand)
    
    trans_gui = threading.Thread(target=show_pending_transactions, daemon=True)
    trans_gui.start()

    #Button for mine but just one not infinite.
    button_mine = Button(master, width= 20, height=8, text="Mine", background="grey", command=start_mine, borderwidth=5)
    button_mine.place(x = width - 1000, y = height * 0.1)

    #Options to vote and cast transaction
    Canvas(master, bg="grey", width= 150, height= 400).place(x= width - 1285, y = height * 0.13)
    option = IntVar()
    Radiobutton(master, text="Partido A", variable= option, value=1, bg="grey").place(x = width - 1250, y = height * 0.2)
    Radiobutton(master, text="Partido B", variable= option, value=2, bg="grey").place(x = width - 1250, y = height * 0.32)
    Radiobutton(master, text="Partido C", variable= option, value=3, bg="grey").place(x = width - 1250, y = height * 0.44)
    Radiobutton(master, text="Partido D", variable= option, value=4, bg="grey").place(x = width - 1250, y = height * 0.56)
    Button(master, width= 10, text="Vote",command = lambda: vote(option)).place(x = width - 1247, y = height * 0.68)

    y = threading.Thread(target=listen_to_request_info, daemon=True)
    y.start()
    
    master.mainloop()



def main():

    current_user = []
    
    def SignUp():

        if paswd_sig.get() != "" and len(paswd_sig.get()) >= 6 and not " " in paswd_sig.get():
            url = os.path.join(ROOT, "info.txt")
            if os.path.isfile(url):
                a = Label(w, text="Device Already exist. Please LogIn", bg="gray", fg="white")
                a.place(x= width / 1.44, y= height / 1.4)
                a.after(1000, a.destroy)
            else:
                secret = generateAdress(users.id, paswd_sig.get())
                new_user = users(secret)
                current_user.append(new_user)
                blockchain.add_user_transaction(new_user)
                ip = get_ip()
                blockchain.add_node_transaction(secret, ip)
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
                    f = open(url, "r")
                    s = f.readlines()[2]
                    f.close()
                    blockChainActions(s, current_user)
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

data = request_info_nodes()

if data != False:
    blockchain = data[0]
    users = data[1]
    main()
else:
    print("Impossible to get acces to blockchain info")

'''
x = threading.Thread(target= main)
y = threading.Thread(target=alwaysMine)
x.start()
y.start()

x.join()
y.join()

print(blockchain)
'''