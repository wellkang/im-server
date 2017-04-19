# -*- coding: utf8 -*-

import asynchat
import json
import hashlib
import base64
import logging

logger = logging.getLogger(__name__)

MESSAGE_TYPE = {"one_to_one": 1, "chat_room": 2, "connect": "connect"}
MESSAGE_ERROR = {"unknow_message_type": "1", "unknow_from_user": "2", "unkonw_target": "3"}


def ws_response(content=""):
    """
    :param content:
    :return:
    """
    l = len(content)
    if l < 126:
        return '%c%c%s' % (0x81, len(content), content)
    elif 126 <= l < 65535:
        return '%c%c%c%c%s' % (0x81, 126, l >> 8, l & 255, content)


def parse_http_req(data):
    header = dict()
    params = dict()
    data = data.split('\r\n')
    method, uri, protocol = data[0].split(' ')
    if len(uri.split('?', 1)) == 2:
        params_str = uri.split('?')[-1]
        for _ in params_str.split('&'):
            k, v = _.split('=', 1)
            params[k] = v
    header['method'], header['protocol'] = method, protocol
    for item in data[1:]:
        if ":" in item:
            k, v = item.split(':', 1)
            header[k] = v.strip()
    return {"header": header, "params": params}


def gen_accept_key(sec_websocket_key):
    print sec_websocket_key
    sha1 = hashlib.sha1(sec_websocket_key)
    sha1.update('258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
    return base64.b64encode(sha1.digest())


class BaseClient(asynchat.async_chat, object):

    def __init__(self, client_sock, user_map, sock_map):
        self._user_map = user_map
        self.user_id = None
        super(BaseClient, self).__init__(sock=client_sock, map=sock_map)
        self.set_terminator(None)
        self.handshake = False

    def collect_incoming_data(self, data):
        print data
        self.dispatch(data)

    def found_terminator(self):
        return

    def add_channel(self, map=None):
        super(BaseClient, self).add_channel(map)
        if self.user_id:
            self.handshake = True
            self._user_map[self.user_id] = self._fileno

    def del_channel(self, map=None):
        if self.user_id and self.user_id in self._user_map:
            del self._user_map[self.user_id]
        self.handshake = False
        super(BaseClient, self).del_channel(map)

    def parse_data(self, msg):
        v = ord(msg[1]) & 0x7f
        if v == 0x7e:
            p = 4
        elif v == 0x7f:
            p = 10
        else:
            p = 2
        mask = msg[p:p + 4]
        data = msg[p + 4:]

        return ''.join([chr(ord(v) ^ ord(mask[k % 4])) for k, v in enumerate(data)])

    def dispatch(self, data):
        if not self.handshake:
            self.handle_handshake(data)
        else:
            try:
                raw_data = self.parse_data(data)
                data = json.loads(raw_data)
            except Exception:
                logger.error(raw_data)
                return
            message_type = data.get('message_type')
            if not message_type or message_type not in MESSAGE_TYPE.values():
                self.push(MESSAGE_ERROR['unknow_message_type'])
            elif message_type == MESSAGE_TYPE['one_to_one']:
                self.handle_message_one_to_one(data)

    def handle_message_one_to_one(self, data):
        target = data.get('target')
        content = data.get('content').encode("utf8")
        if target in self._user_map:
            self._map[self._user_map[target]].send(ws_response(json.dumps(data)))
        else:
            self.send(ws_response("offline"))
            # todo: into database

    def handle_handshake(self, data):
        req_data = parse_http_req(data)
        print req_data
        if "token" not in req_data['params']:
            self.del_channel()
            return
        else:
            self.user_id = req_data['params']['token']
        if 'Sec-WebSocket-Key' in req_data['header']:
            hash_key = gen_accept_key(req_data['header']['Sec-WebSocket-Key'])
            resp = """ HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: {}\r\n\r\n""".format(hash_key)
            self.push(resp)
            self.add_channel()
