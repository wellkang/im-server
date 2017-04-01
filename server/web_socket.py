# -*- coding: utf8 -*-
import socket;socket.socket.connect

import gevent


class BaseClient(object):

    def __init__(self, client_sock, key, buf=1024):
        self.sock = client_sock
        self.buf = buf
        self.key = key

    def run(self, data):
        print(data)

    def start(self):
        data = 'start'
        while data:
            data = self.sock.recv(self.buf).decode()
            self.run(data)
        print('client closed')
        self.sock.close()


class ClientManager(object):

    def __init__(self):
        self.clients = {}

    def add(self, key, client):
        if not isinstance(client, BaseClient):
            raise TypeError('%s is not a BaseClient instance.' % client)
        self.clients[key] = client

    def delete(self, key):
        self.clients.pop(key)

    def send(self, key, data):
        if key in self.clients:
            try:
                self.clients[key].send(data)
            except Exception as e:
                raise e
        else:
            pass


class Server(object):

    def __init__(self, host, port, listen=5):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.listen = listen

    def run(self):
        print('start server...')
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(self.listen)
        manager = ClientManager()
        user_id = 1
        try:
            while True:
                print('waiting for connect...')
                client_sock, addr = self.server_sock.accept()
                print('connect from %s:%s' % addr)
                c = BaseClient(client_sock, user_id)
                manager.add(user_id, client_sock)
                gevent.spawn(c.start)
                user_id += 1
        finally:
            self.server_sock.close()

if __name__ == '__main__':
    from gevent import monkey;monkey.patch_all()
    host, port = '0.0.0.0', 8090
    server = Server(host, port)
    server.run()