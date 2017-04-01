# -*- coding: utf8 -*-

import asyncore
import socket

from client import BaseClient


class BaseServer(asyncore.dispatcher, object):

    def __init__(self, host='localhost', port=8090):
        super(BaseServer, self).__init__()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.user_map = {}
        self.count = 1

    def handle_accept(self, client=BaseClient):
        conn, addr = self.accept()
        client(conn, self.user_map, self._map, self.count)
        self.count += 1


if __name__ == '__main__':
    s = BaseServer(host='0.0.0.0')
    asyncore.loop()
