import socket 
import threading
import time 

ip = '127.0.0.1'

class Client:
    def __init__(self, sock):
        self.connect(sock)

    def connect(self, sock):
        sock.connect((ip,port))
        self.runner()

    def runner(self):
        while True:
            time.sleep(2)
            print("peer active")

# Network
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9999
peers = dict()
user_file = input("Please enter a file: ")

try:
    sock.bind(('',port))
    sock.listen(1)
    print("System has started")
    while True:
        print(peers)
        client, addr = sock.accept()
        peers[user_file] = addr[1]
        print("Peer added %s " % str(addr[1]))
except:
    print("Network active... adding new client")

Client(sock)


