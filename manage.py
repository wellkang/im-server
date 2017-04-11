# -*- coding: utf8 -*-

import threading
import asyncore
import logging

from flask import Flask
from flask import render_template

from server.server import BaseServer

logging.basicConfig(level=logging.DEBUG, filename="debug.log")


def start_server():
    s = BaseServer(host='0.0.0.0')
    asyncore.loop()


def create_app():
    threading.Thread(target=start_server).start()
    app = Flask(__name__)
    return app

app = create_app()


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)