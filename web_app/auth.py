# -*- coding: utf8 -*-
from flask import request, render_template, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash


def login():
    if request.method == "POST":
        from models.user import User
        data = request.form
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(next or url_for('index'))
    return render_template('login.html')


def register():
    if request.method == 'POST':
        from models.user import User
        from manage import db
        data = request.form
        user = User(username=data.get('username'),
                    password=generate_password_hash(data.get('password')),
                    nickname=data.get('username'))
        db.session.add(user)
        db.session.commit()
        return redirect('login')
    return render_template('register.html')
