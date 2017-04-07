# -*- coding: utf8 -*-

import threading
import asyncore

from flask import Flask
from flask import render_template

from server.server import BaseServer


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def start_server():
    s = BaseServer(host='0.0.0.0')
    asyncore.loop()


if __name__ == '__main__':
    threading.Thread(target=start_server).start()
    app.run(host='0.0.0.0', port=5000, debug=True)