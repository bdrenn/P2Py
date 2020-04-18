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


print("new node ")
node3 = BTPeerConnection(25,'192.168.1.2',1000)



