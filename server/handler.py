# -*- coding: utf8 -*-

import json


MESSAGE_TYPE = {"one_to_one": 1, "chat_room": 2}
MESSAGE_ERROR = {"unknow_message_type": "1", "unknow_from_user": "2", "unkonw_target": "3"}


class BaseMessageHandler(object):

    def __init__(self, client, data):
        self.client = client
        self.data = json.loads(data)
        print 'handler:'
        print data


def dispatch(client, data):
    data = json.loads(data)
    message_type = data.get('message_type')
    if not message_type or message_type not in MESSAGE_TYPE:
        client.push(MESSAGE_ERROR['unknow_message_type'])
    elif message_type == MESSAGE_TYPE['one_to_one']:
        client.handle_one_to_one()
