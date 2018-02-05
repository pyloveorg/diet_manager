#!/usr/bin/env python
# encoding: utf-8
"""
module: views
"""

from flask import render_template, request, redirect

from main import app
from main import db
# from main import bcrypt
# from main import lm

from models import User


@app.route('/', methods=['GET', 'POST'])
def info():
    """Render homepage"""
    return render_template('info.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""
    if request.method == 'POST':
        password = request.form['user_password']
        password_verify = request.form['user_password_verify']
        email = request.form['user_email']
        if password != password_verify:
            error = "Podane hasła się nie zgadzają!"
            return render_template(
                'register.html', error=error,
                password=password,
                email=email,
                password_verify=password_verify
            )
        post = User(password=password, email=email)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')
