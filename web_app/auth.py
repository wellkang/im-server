# -*- coding: utf8 -*-
from flask import request, render_template


def login():
    if request.method == "POST":
        pass
    return render_template('login.html')