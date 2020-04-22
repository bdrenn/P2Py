import logging
import asyncio
import sys
import os
from kademlia.network import Server



handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)


class Node:
    def __init__(self, port):
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)
        self.server = Server()
        self.loop.run_until_complete(self.server.listen(int(port)))
    
    def check_neighbors(self):
        return self.server.bootstrappable_neighbors()

    def bootstrap_node(self, addr, port):
        bootstrap_node = (addr, int(port))
        self.loop.run_until_complete(self.server.bootstrap([bootstrap_node]))

    def get(self, key): 
        return self.loop.run_until_complete(self.server.get(key))

    def set(self, key, value):
        return self.loop.run_until_complete(self.server.set(key, value))
