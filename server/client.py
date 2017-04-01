# -*- coding: utf8 -*-

import asyncore
import asynchat
import json

MESSAGE_TYPE = {"one_to_one": 1, "chat_room": 2}
MESSAGE_ERROR = {"unknow_message_type": "1", "unknow_from_user": "2", "unkonw_target": "3"}


class BaseClient(asynchat.async_chat, object):

    def __init__(self, client_sock, user_map, sock_map, user_id):
        self._user_map = user_map
        self.user_id = user_id
        super(BaseClient, self).__init__(sock=client_sock, map=sock_map)
        self.set_terminator(None)

    def collect_incoming_data(self, data):
        self.dispatch(data)

    def found_terminator(self):
        return

    def add_channel(self, map=None):
        super(BaseClient, self).add_channel(map)
        self._user_map[self.user_id] = self._fileno

    def del_channel(self, map=None):
        if self.user_id in self._user_map:
            del self._user_map[self.user_id]
        super(BaseClient, self).del_channel(map)

    def dispatch(self, data):
        print data
        data = json.loads(data)
        message_type = data.get('message_type')
        if not message_type or message_type not in MESSAGE_TYPE.values():
            self.push(MESSAGE_ERROR['unknow_message_type'])
        elif message_type == MESSAGE_TYPE['one_to_one']:
            target = data.get('target')
            content = data.get('content')
            if target in self._user_map:
                fileno = self._user_map[target]
                self._map[fileno].push(content)
            else:
                self.push("offline")
