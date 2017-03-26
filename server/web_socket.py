# -*- coding: utf8 -*-
import socket;socket.socket.send()

import gevent
from gevent import monkey; monkey.patch_all()


class Client(object):

    def __init__(self, client_sock, session, username, buf=1024):
        self.sock = client_sock
        self.buf = buf
        self.username = username
        self.session = session

    def recv(self):
        while True:
            data = self.sock.recv(self.buf)
            if data.strip().decode() == 'quit':
                self.sock.close()
                self.session.delete(self.sock)
                self.session.send('user{} has logout.'.format(self.username).encode())
                continue
            self.session.send('user{}:'.format(self.username).encode())
            self.session.send(data)

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

    def delete(self, sock):
        if not isinstance(sock, socket.socket):
            raise TypeError('ws is not a socket instance.')
        self.web_sockets.remove(sock)

    def send(self, data):
        for s in self.web_sockets:
            s.send(data)


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
        session = Session()
        user_id = 1
        try:
            while True:
                print('waiting for connect...')
                client_sock, addr = self.server_sock.accept()
                print('connect from %s:%s' % addr)
                session.send('user{} has login.'.format(user_id).encode())
                ws = Client(client_sock, session, user_id)
                session.add(client_sock)
                gevent.spawn(ws.recv)
                user_id += 1
        finally:
            self.server_sock.close()

if __name__ == '__main__':
    host, port = '0.0.0.0', 8090
    server = Server(host, port)
    server.run()