import socket
import traceback
import threading
import struct

class BTPeerConnection:
    def __init__(self, peerid, host, port, sock=None):
        self.id = peerid
        
        if not sock:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host,int(port)))
        else:
            self.s = sock
        
        self.sd = self.s.makefile('rw', 0)

    def recvdata(self):
        
        try:
            msgtype = self.sd.read(4)
            if not msgtype:
                return(None, None)
            lenstr = self.sd.read(4)
            msglen = int(struct.unpack("!L", lenstr)[0])
            msg = ""

            while len(msg) != msglen:
                data = self.sd.read(min(2048, msglen - len(msg)))
                if not len(data):
                    break
                msg += data

            if len(msg) != msglen:
                return(None, None)
        
        except KeyboardInterrupt:
            raise

        return (msgtype, msg)
        


class Node:
    def __init__(self, maxpeers, serverport, myid=None, serverhost = None):
        self.maxpeers = int(maxpeers)
        self.serverport = int(serverport)

        # If not supplied, the host name/IP address will be determined
        # by attempting to connect to an Internet host like Google.
        if serverhost:
            self.serverhost = serverhost
        else: 
            self.__initserverhost()

        # If not supplied, the peer id will be composed of the host address
        # and port number
        if myid:
            self.myid = myid
        else:
            self.myid = '%s:%d' % (self.serverhost, self.serverport)

        # list (dictionary/hash table) of known peers
        self.peers = {}  

        # used to stop the main loop
        self.shutdown = False  

        self.handlers = {}
        self.router = None

    def makeserversocket(self, port, backlog=5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(backlog)
        return s

    def __handlepeer(self, clientsock):
        print('Connected' + str(clientsock.getpeername()))

        host, port = clientsock.getpeername()
        peerconn = BTPeerConnection(None, host, port, clientsock)

        try:
            msgtype, msgdata = peerconn.recvdata()
            if msgtype:
                msgtype = msgtype.upper()
            if msgtype not in self.handlers:
                print('Not handled: %s: %s' % (msgtype, msgdata))
            else:
                print('Handling peer msg: %s: %s' % (msgtype,msgdata))
                self.handlers[msgtype](peerconn, msgdata)
        except KeyboardInterrupt:
            raise

        print('Disconnecting ' + str(clientsock.getpeername()))

    def __initserverhost(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("www.google.com",80))
        self.serverhost = s.getsockname()[0]
        s.close
    
    def mainloop(self):
        s = self.makeserversocket(self.serverport)
        print('Server started: %s (%s:%d)' % (self.myid, self.serverhost, self.serverport))
        
        while not self.shutdown:
            try:
                print( 'Listening for connections...')
                clientsock, clientaddr = s.accept()
                t = threading.Thread(target = self.__handlepeer, args = [clientsock])
                print("peer connected")
                t.start()
            except KeyboardInterrupt:
                self.shutdown = True
                continue

        print('Main loop exiting')
        s.close()



# Main
for i in range(0,10):
    print(i)
    try:
        node1 = Node(0, 1000)
        node1.mainloop()
    except:
        pass
        
    try:
        print("network active")
        node2 = Node(0, 1000, '192.168.1.2')
    except:
        print("can't connect to server")