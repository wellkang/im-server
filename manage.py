# -*- coding: utf8 -*-

import threading
import asyncore

from flask_login import LoginManager

from web_socket.server import BaseServer
from conf import app, manager, api
from web_app import auth, index, user
from models.user import User


def start_ws_server():
    try:
        s = BaseServer(host='0.0.0.0')
        asyncore.loop()
    except AttributeError:
        pass


def init_app(flask_app):
    # ==== 设置flask-login ====
    login_manager = LoginManager()
    login_manager.init_app(app=flask_app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    # ==== 添加路由 ====
    flask_app.add_url_rule('/', view_func=index.index)
    flask_app.add_url_rule('/login', view_func=auth.login, methods=['GET', 'POST'])
    flask_app.add_url_rule('/register', view_func=auth.register, methods=['GET', 'POST'])
    flask_app.add_url_rule('/logout', view_func=auth.logout, methods=['GET', 'POST'])
    # flask_app.add_url_rule('/users', view_func=user.find_user, methods=['GET', 'POST'])

    # ===== api路由 ====
    api.add_resource(user.FindUserAPI, '/users')

    # ===== websocket服务端 ====
    threading.Thread(target=start_ws_server).start()


init_app(app)


application = app


if __name__ == '__main__':
    init_app(app)
    manager.run()
