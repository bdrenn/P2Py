import socket 
import threading
import time 

ip = '127.0.0.1'

class Client:
    def __init__(self):
        self.connect()

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 9999

        try: 
            sock.bind(('',port)) # '' indicates that the server will listen to other computers
            sock.listen(1)
            print("System has started!")
            while True:
                client,addr = sock.accept()
                print("Peer added %s " %  str(addr[1]))
        except:
            print("Adding new client")

        # New Peer
        sock.connect((ip,port))
        self.runner()

    def runner(self):
        while True:
            time.sleep(2)
            print("peer active")

# Runner
peer = Client()




