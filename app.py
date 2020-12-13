# @Arnav Gupta write comments from next time

from Tool import app, db , mail
import os
from flask_mail import Mail, Message
import pandas as pd
from picture_handler import add_profile_pic
import numpy as np
from Tool.forms import RegistrationForm, LoginForm, UpdateUserForm, DonateForm
from Tool.models import User
from flask import render_template, request, url_for, redirect, flash, abort
from flask_login import current_user, login_required, login_user, logout_user
from picture_handler import add_profile_pic
from sqlalchemy import desc, asc
from werkzeug.utils import secure_filename
from flask import send_from_directory

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.htm")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print('hello')
        if user is not None and user.check_password(form.password.data):

            login_user(user)

            return redirect(url_for('index'))
        elif user is not None and user.check_password(form.password.data) == False:
            error = 'Wrong Password'
        elif user is None:
            error = 'No such login Pls create one'
    return render_template('login.htm', form=form, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        print('bie')
        db.session.add(user)
        db.session.commit()

        if form.picture.data is not None:
            id = user.id
            pic = add_profile_pic(form.picture.data, id)
            user.profile_image = pic
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.htm', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    pic = current_user.profile_image
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data

        if form.picture.data is not None:
            id = current_user.id
            pic = add_profile_pic(form.picture.data, id)
            current_user.profile_image = pic

        flash('User Account Created')
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename=current_user.profile_image)
    return render_template('account.htm', profile_image=profile_image, form=form, pic=pic)


@app.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    form = DonateForm()
    if form.validate_on_submit():
        email = current_user.email
        people = form.people.data
        address = form.address.data
        points = people * 100
        current_user.points += points
        db.session.commit()
        msg = Message('Food Donation', sender = 'xino.technovity@gmail.com', recipients = [email])
        msg.body = "******* will reach your doorstep in 30 mins to collect the food "
        mail.send(msg)
        flash('Check your mail for details')
    return render_template('donate.htm' , form = form)

@app.route('/leaderboard')
def leaderboard():
    all_users = User.query.order_by(User.points.desc()).all()
    n = len(all_users)
    rank = []
    for users in all_users:
        rank.append(n)
        n -= 1
    return render_template('leaderboard.htm',all_users=all_users,rank=rank)

if __name__ == '__main__':
    app.run(debug=True)
