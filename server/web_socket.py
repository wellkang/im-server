# -*- coding: utf8 -*-
import socket


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


class Server(object):

    def __init__(self):
        pass


if __name__ == '__main__':
    host, port = '0.0.0.0', 8090
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    while True:
        client_sock, addr = server.accept()
        ws = BaseWebSocket(client_sock)
        ws.send('username:')
        username = ws.recv()
        ws.send('password')
        password = ws.recv()
        print(username, password)
        ws.close()
        print('connection closed')
    server.close()