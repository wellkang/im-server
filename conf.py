# -*- coding: utf8 -*-
import os


class Config(object):

    pass


class DevConfig(Config):
    SECRET_KEY = 'jhjhsjdnbhfjghg'
    DEBUG = True
    DATABASE_URI = "sqlite://:memory:"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOGGING_FILE = BASE_DIR + '/log/debug.log'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR + '/test.db'
