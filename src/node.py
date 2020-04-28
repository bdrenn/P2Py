import logging
import asyncio
import sys
import os
import socket
from kademlia.network import Server
from threading import Thread
from contextlib import closing

class Node(Server):
    """ Class for nodes in our DHT using a Kademlia

    Kademlia uses a binary tree structure and a XOR metric for traversing the tree. 
    The keys are concatanated with 160 bits and hashed, then stored on leaves.
    Because of its efficient use of subtrees and the XOR metric it uses to find the nodes
    in the leaves of each subtree, the algorithm runs at a time of O(log(n)). Given that
    each file has its own unique node, files are also updated on the DHT in that time aswell.

    Args:
        server (object): Server class from kademlia, has event_loops/listening/bootstrapping/get/set
        host_port (int): Takes in the port to bootstrap to, if first node, becomes users port
        port (int): If not first node, random open port is selected
        host_IP (string): Local network IP address of first node to connect for bootstrapping
        file_name (string): Key for storing/retrieving objects in the DHT
        file_value (string): Bytes for objects storing in the DHT
        loop (object): asyncio object for getting events on server, also used for multithreading
    Returns:
        peers: Crawls kademlia DHT and looks for all available bootstrappable neighbors
        file_value (object): Bytes for objects stored in the DHT
    """

    def __init__(self):
        Server.__init__(self)
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)

    def log(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)

    def listening(self, port):
        self.loop.run_until_complete(self.listen(port))
        t = Thread(target=self.handler, args=(self.loop,))
        t.daemon = True
        t.start()

    def handler(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
        
    def join_network_node(self, addr, port):
        asyncio.run_coroutine_threadsafe(self.bootstrap([(addr, int(port))]), self.loop)

    def get_peers(self):
        peers = self.bootstrappable_neighbors()
        return peers

    def set_file(self, file_name, file_value):
        asyncio.run_coroutine_threadsafe(self.set(file_name, file_value), self.loop)

    def get_file(self, file_name):
        file_value = asyncio.run_coroutine_threadsafe(self.get(file_name), self.loop).result()
        return file_value

    def kill_thread(self):
        sys.exit()
        
    def setup(self, host_port, host_IP=None):
        if host_IP is not None:
            try:
                with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
                    s.bind(('', 0))
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    user_port = s.getsockname()[1]
                self.listening(int(user_port))
                self.join_network_node(host_IP, host_port)
                print('Welcome!')
            except Exception as e:
                print(e)
        else:
            try:
                self.listening(host_port)
                print('First node!')
            except Exception as e:
                print(e)
