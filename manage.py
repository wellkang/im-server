# -*- coding: utf8 -*-

import threading
import asyncore
import logging

from flask import Flask
from flask_login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

from server.server import BaseServer
import conf
from web_app import auth, index
from models.user import User


def start_server():
    try:
        s = BaseServer(host='0.0.0.0')
        asyncore.loop()
    except AttributeError:
        pass


def add_url(app):
    app.add_url_rule('/', view_func=index.index)
    app.add_url_rule('/login', view_func=auth.login, methods=['GET', 'POST'])
    app.add_url_rule('/register', view_func=auth.register, methods=['GET', 'POST'])


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


def create_app():
    threading.Thread(target=start_server).start()
    app = Flask(__name__)
    login_manager.init_app(app=app)
    login_manager.login_view = 'auth.login'
    app.config.from_object(conf.DevConfig)
    logging.basicConfig(level=logging.DEBUG, filename=app.config.get('LOGGING_FILE'))
    add_url(app)
    return app

app = create_app()
db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)