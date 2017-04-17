# -*- coding: utf8 -*-
from flask import request, render_template, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user

from models.user import User
from conf import db


def login():
    if request.method == "POST":
        data = request.form
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('index'))
    return render_template('login.html')


def register():
    if request.method == 'POST':
        data = request.form
        user = User(username=data.get('username'),
                    password=generate_password_hash(data.get('password')),
                    nickname=data.get('username'),)
        db.session.add(user)
        db.session.commit()
        return redirect('login')
    return render_template('register.html')


@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
