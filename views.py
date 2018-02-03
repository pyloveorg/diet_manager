#!/usr/bin/env python
# encoding: utf-8
from main import app
from main import db
from main import bcrypt
from main import lm

from models import User

from flask import render_template, request, redirect


@app.route('/', methods=['GET', 'POST'])
def info():
    return render_template('info.html')


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/new-user', methods=['POST'])
def new_post():
    password = request.form['user_password']
    email = request.form['user_email']
    post = User(password=password, email=email)
    db.session.add(post)
    db.session.commit()
    return redirect('/register')