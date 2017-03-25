# -*- coding: utf8 -*-
import socket

import gevent
# from gevent import monkey; monkey.patch_all()


class BaseWebSocket(object):

    def __init__(self, client_sock, buf=1024):
        self.sock = client_sock
        self.buf = buf

    def recv(self):
        return self.sock.recv(self.buf)

    def send(self, data):
        self.sock.send(data)

    def close(self):
        self.sock.close()


class Session(object):

    def __init__(self):
        self.web_sockets = []

    def add(self, ws):
        if not isinstance(ws, socket.socket):
            raise TypeError('ws is not a socket instance.')
        self.web_sockets.append(ws)


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
        try:
            while True:
                print('waiting for connect...')
                client_sock, addr = self.server_sock.accept()
                print('connect from %s:%s' % addr)
                client_sock.close()
        except KeyboardInterrupt:
            self.server_sock.close()
            raise KeyboardInterrupt('stop')

if __name__ == '__main__':
    host, port = '0.0.0.0', 8090
    server = Server(host, port)
    server.run()