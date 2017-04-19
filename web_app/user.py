# -*- coding: utf8 -*-
from flask import request, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_restful import Resource, fields, marshal_with

from models.user import User
from conf import db


@login_required
def find_user():
    users = User.query.filter()
    content = dict()
    content['users'] = users
    return render_template('users.html', content=content)


class FindUserAPI(Resource):
    user_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'head_photo': fields.String
    }

    @login_required
    @marshal_with(user_fields)
    def get(self):
        users = User.query.filter(User.id != current_user.id).all()
        return users
