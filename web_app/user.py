# -*- coding: utf8 -*-
from flask import request, render_template, redirect, url_for
from flask_login import login_required

from models.user import User
from conf import db


@login_required
def find_user():
    users = User.query.all()