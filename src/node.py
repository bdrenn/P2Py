import logging
import asyncio
import sys
import os
from kademlia.network import Server
from threading import Thread

host_port = 1001
user_port = 1002
host_IP = '0.0.0.0'

class Node(Server):
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
        file_value = asyncio.run_coroutine_threadsafe(self.get(file_name), self.loop)
        return file_value

    def setup(self):
        try:
            self.listening(host_port)
            print("First node!")
        except Exception as e:
            try:
                self.listening(int(user_port))
                self.join_network_node(host_IP, host_port)
                print('Welcome!')
            except Exception as e:
                print(e)
