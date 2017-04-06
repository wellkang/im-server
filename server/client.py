# -*- coding: utf8 -*-

import asynchat
import json
import hashlib
import base64

MESSAGE_TYPE = {"one_to_one": 1, "chat_room": 2, "connect": "connect"}
MESSAGE_ERROR = {"unknow_message_type": "1", "unknow_from_user": "2", "unkonw_target": "3"}


class BaseClient(asynchat.async_chat, object):

    def __init__(self, client_sock, user_map, sock_map):
        self._user_map = user_map
        self.user_id = None
        super(BaseClient, self).__init__(sock=client_sock, map=sock_map)
        self.set_terminator(None)
        self.handshake = False

    def collect_incoming_data(self, data):
        self.dispatch(data)

    def found_terminator(self):
        return

    def add_channel(self, map=None):
        super(BaseClient, self).add_channel(map)
        if self.user_id:
            self._user_map[self.user_id] = self._fileno

    def del_channel(self, map=None):
        if self.user_id and self.user_id in self._user_map:
            del self._user_map[self.user_id]
        super(BaseClient, self).del_channel(map)

    def dispatch(self, data):
        print data
        if not self.handshake:
            self.handle_handshake(data)
        else:
            message_type = data.get('message_type')
            if not message_type or message_type not in MESSAGE_TYPE.values():
                self.push(MESSAGE_ERROR['unknow_message_type'])
            elif message_type == MESSAGE_TYPE['one_to_one']:
                self.handle_message_one_to_one(data)

    def handle_message_one_to_one(self, data):
        target = data.get('target')
        content = data.get('content')
        if target in self._user_map:
            self._map[self._user_map[target]].push(content)
        else:
            self.push("offline")
            # todo: into database

    def handle_handshake(self, data):
        req_data = self.parse_http_req(data)
        print req_data
        self.del_channel()

    def parse_http_req(self, data):
        header = dict()
        data = data.split('\r\n')
        for item in data[1:]:
            if ":" in item:
                k, v = item.split(':', 1)
                header[k] = v
        return {"header": header}

    def gen_accept_key(self, sec_websocket_key):
        sha1 = hashlib.sha1(sec_websocket_key)
        sha1.update('258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
        return base64.b64encode(sha1.hexdigest())