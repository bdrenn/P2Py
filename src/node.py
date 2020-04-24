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

class Node(Server):
    def __init__(self):
        Server.__init__(self)
        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)

    async def listening(self, port):
        await self.listen(port)
        
    async def join_network_node(self, addr, port):
        await self.bootstrap([(addr, int(port))])

    async def get_peers(self):
       return self.bootstrappable_neighbors()


