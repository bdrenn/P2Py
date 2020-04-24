import logging
import asyncio
import sys
import os
from kademlia.network import Server
from threading import Thread

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

class Node(Server):
    def __init__(self):
        Server.__init__(self)
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)

    def listening(self, port):
        self.loop.run_until_complete(self.listen(port))
        t = Thread(target=self.handler, args=(self.loop,))
        t.start()

    def handler(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
        
    def join_network_node(self, addr, port):
        asyncio.run_coroutine_threadsafe(self.bootstrap([(addr, int(port))]), self.loop)

    def get_peers(self):
        peers = self.bootstrappable_neighbors()
        return peers
