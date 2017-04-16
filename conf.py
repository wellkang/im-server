# -*- coding: utf8 -*-
import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


class Config(object):

    pass


class DevConfig(Config):
    SECRET_KEY = 'jhjhsjdnbhfjghg'
    DEBUG = True
    DATABASE_URI = "sqlite://:memory:"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOGGING_FILE = BASE_DIR + '/log/debug.log'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR + '/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


def create_app(config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)
    logging.basicConfig(level=logging.DEBUG, filename=flask_app.config.get('LOGGING_FILE'))
    return flask_app


app = create_app(DevConfig)
db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

