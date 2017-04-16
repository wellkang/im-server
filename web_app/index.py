# -*- coding: utf8 -*-
from flask import render_template
from flask_login import login_required, current_user


@login_required
def index():
    content = {
        "user": current_user
    }
    return render_template('index.html', content=content)
