import socket
import traceback
import threading
import struct
import time

class BTPeerConnection:
    def __init__(self, peerid, host, port, sock=None):
        self.id = peerid
        
        if not sock:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host,int(port)))
        else:
            self.s = sock
        
        self.sd = self.s.makefile('rw', 0)

    def __makemsg(self, msgtype, msgdata):
        msglen = len(msgdata)
        msg = struct.pack("!4sL%ds" % msglen, msgtype, msglen, msgdata)
        return msg
    
    def senddata(self, msgtype, msgdata):
        try:
            msg = self.__makemsg(msgtype, msgdata)
            self.sd.write(msg)
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        except:
            print("False")
            return False
        
        return True

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
        except:
            print("flase")
            return(None,None)

        return (msgtype, msg)

    def close(self):
        self.s.close()
        self.s = None
        self.sd = None
        


class BTPeer:
    def __init__(self, maxpeers, serverport, myid=None, serverhost = None):
        self.maxpeers = int(maxpeers)
        self.serverport = int(serverport)

        if serverhost:
            self.serverhost = serverhost
        else: 
            self.__initserverhost()

        if myid:
            self.myid = myid
        else:
            self.myid = '%s:%d' % (self.serverhost, self.serverport)

        self.peerlock = threading.Lock()
        self.peers = {}  
        self.shutdown = False  

        self.handlers = {}
        self.router = None

    def __initserverhost(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("www.google.com",80))
        self.serverhost = s.getsockname()[0]
        s.close()

    def __handlepeer(self, clientsock):
        
        print('New child ' + str(threading.currentThread().getName()))
        print('Connected ' + str(clientsock.getpeername()))

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
        except:
            print("error in handlepeer")

        print('Disconnecting ' + str(clientsock.getpeername()))
        peerconn.close()

    def __runstablizer(self, stabilizer, delay):
        while not self.shutdown:
            stabilizer()
            time.sleep(delay)

    def setmyid(self, myid):
        self.myid = myid

    def startstablizer(self, stabilizer, delay):
        t = threading.Thread(target=self.__runstablizer, args=[stabilizer,delay])
        t.start()

    def addhandler(self, msgtype, handler):
        assert len(msgtype) == 4
        self.handlers[msgtype] = handler

    def addrouter(self, router):
        self.router = router

    def addpeer(self, peerid, host, port):
        if peerid not in self.peers and (self.maxpeers == 0 or len(self.peers) < self.maxpeers):
            self.peers[peerid] = (host, int(port))
            return True
        else:
            return False

    def getpeer(self, peerid):
        assert peerid in self.peers
        return self.peers[peerid]

    def removepeer(self, peerid):
        if peerid in self.peers:
            del self.peers[peerid]
        
    def addpeerat(self, loc, peerid, host, port):
        self.peers[loc] = (peerid, host, int(port))

    def getpeerat(self, loc):
        if loc not in self.peers:
            return None
        return self.peers[loc]

    def removepeerat(self, loc):
        self.removepeer(loc)

    def getpeerids(self):
        return self.peers.keys()

    def numberofpeers(self):
        return len(self.peers)

    def maxpeersreached(self):
        assert self.maxpeers == 0 or len(self.peers) <= self.maxpeers
        return self.maxpeers > 0 and len(self.peers) == self.maxpeers
    
    def makeserversocket(self, port, backlog=5):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(backlog)
        return s

    def sendtopeer(self, peerid, msgtype, msgdata, waitreply=True):
        if self.router:
            nextpid, host, port = self.router(peerid)
        if not self.router or not nextpid:
            print('Unable to route %s to %s' % (msgtype, peerid))
            return None
        #host,port = self.peers[nextpid]
        return self.connectandsend(host, port, msgtype, msgdata, pid=nextpid, waitreply=waitreply)

    def connectandsend(self, host, port, msgtype, msgdata, pid=None, waitreply=True):
        msgreply = []
        try:
            peerconn = BTPeerConnection(pid, host, port)
            peerconn.senddata(msgtype, msgdata)
            print('Sent %s: %s' % (pid, msgtype))

            if waitreply:
                onereply = peerconn.recvdata()
                while(onereply != (None, None)):
                    msgreply.append(onereply)
                    print("Got reply %s:%s" % (pid, str(msgreply)))
                    onereply = peerconn.recvdata()
            peerconn.close()
        except KeyboardInterrupt:
            raise
        except:
            print("error in connect and send")

        return msgreply

    def checklivepeers(self):
        todelete = []
        for pid in self.peers:
            isconnected = False 
            try:
                print("Check live %s" % pid)
                host,port = self.peers[pid]
                peerconn = BTPeerConnection(pid, host, port)
                isconnected = True
            except:
                todelete.append(pid)
            if isconnected:
                peerconn.close()

            self.peerlock.acquire()
            try:
                for pid in todelete:
                    if pid in self.peers:
                        del self.peers[pid]
            finally:
                self.peerlock.release()

    
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
            except:
                print("error in main loop")
                continue

        print('Main loop exiting')
        s.close()

