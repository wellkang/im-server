# -*- coding: utf8 -*-
import datetime

from conf import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    mobile = db.Column(db.String(11), unique=True)
    head_photo = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(93))
    nickname = db.Column(db.String(20))
    time_created = db.Column(db.DateTime())

    def __init__(self, username, password, email='', mobile='', head_photo='', nickname=''):
        self.username = username
        self.nickname = nickname
        self.password = password
        self.email = email
        self.mobile = mobile
        self.head_photo = head_photo
        self.time_created = datetime.datetime.now()

    def __repr__(self):
        return '<user %s>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @classmethod
    def get(cls, user_id):
        return User.query.get(int(user_id))


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_created = db.Column(db.DateTime())
    is_delete = db.Column(db.Boolean())

if __name__ == '__main__':
    db.create_all()
