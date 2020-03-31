import socket
import threading
import sys
import time
from random import randint

class Server:

    # All user connections on network
    connections = []
    peers = []

    def __init__(self):
        # Bind Socket to port and listen
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 10000))
        sock.listen(1)
        print("Server Running")

        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append((a[0]))
            print(str(a[0]) + ':' + str(a[1]), "connected")
            self.sendPeers()

    # Handles connections
    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "Disconnected")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.sendPeers()
                break

    def sendPeers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ","

        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, "utf-8"))



class Client:

    def sendMsg(self, sock):
        while True:
            sock.send(bytes(input(""), 'utf-8'))
    
    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address, 10000))

        iThread = threading.Thread(target=self.sendMsg, args=(sock,))
        iThread.daemon = True
        iThread.start()

        # Connected and receiving Data loop
        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                self.updatePeers(data[1:])
            else:
                print(str(data, 'utf-8'))

    def updatePeers(self, peerData):
        P2P.peers = str(peerData, "utf-8").split(",")[:-1]


class P2P:
    peers = ['127.0.0.1']

while True:
    try:
        print("Trying to connect ...")
        time.sleep(randint(1, 5))
        for peer in P2P.peers:
            try:
                client = Client(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
    
            try:
                server = Server()
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                print("Can't connector to the server")
    except KeyboardInterrupt:
        sys.exit(0)
        
