# @Arnav Gupta write comments from next time

from Tool import app, db
import os
import pandas as pd
from picture_handler import add_profile_pic
import numpy as np
from Tool.forms import RegistrationForm, LoginForm, QueryForm, UpdateUserForm
from Tool.models import User
from flask import render_template, request, url_for, redirect, flash, abort
from flask_login import current_user, login_required, login_user, logout_user
from picture_handler import add_profile_pic
from sqlalchemy import desc, asc
from werkzeug.utils import secure_filename
from flask import send_from_directory
import csv
from sklearn.linear_model import LinearRegression, LogisticRegression
import stripe

ALLOWED_EXTENSIONS = {'csv'}
public_key = 'pk_test_6pRNASCoBOKtIshFeQd4XMUh'

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.htm")


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def linear():
    try:
        mylist = ['import pandas as pd', 'import numpy as np',
                  'from sklearn.linear_model import LinearRegression']
        numeric_column = []
        df_test = pd.read_csv('Tool/static/csvs/' +
                              current_user.username + 'test' + '.csv')
        df_train = pd.read_csv('Tool/static/csvs/' +
                               current_user.username + 'train' + '.csv')
        for i in df_train.columns:
            if df_train[i].dtypes == object:
                continue
            else:
                numeric_column.append(i)
        if request.method == 'POST':
            train_csv_name = request.form.get("train_csv")
            test_csv_name = request.form.get("test_csv")
            y = request.form.get("column_name")
            numeric_column.remove(y)
            mylist.append("df_train = pd.read_csv('" + train_csv_name + "')")
            mylist.append("df_test = pd.read_csv('" + test_csv_name + "')")
            mylist.append('X_train = df_train[' + str(numeric_column) + ']')
            mylist.append("y_train = df_train['" + y + "']")
            mylist.append('X_test = df_test[' + str(numeric_column) + ']')
            mylist.append('lm = LinearRegression()')
            mylist.append('lm.fit(X_train , y_train)')
            mylist.append('predictions = lm.predict(X_test)')
            flash(mylist)
    except:
        return redirect(url_for('upload_file'))
    return render_template("dashboard.htm", numeric_column=numeric_column)


@app.route('/ytakelinear', methods=['GET', 'POST'])
@login_required
def ylinear():
    if current_user.membership == 'premium':
        numeric_column = []
        df_train = pd.read_csv('Tool/static/csvs/' +
                               current_user.username + 'train' + '.csv')
        for i in df_train.columns:
            if df_train[i].dtypes == object:
                continue
            else:
                numeric_column.append(i)
        if request.method == 'POST':
            y = request.form.get("y_column")
            print(y)
            return redirect(url_for('linear_predict', y=y))
    else:
        return redirect(url_for('get_premium'))
    return render_template('linearpredicty.htm', numeric_column=numeric_column)


@app.route('/linearpredict/<y>', methods=['GET', 'POST'])
@login_required
def linear_predict(y):
    if current_user.membership == 'premium':
        numeric_column = []
        X_test = []
        df_train = pd.read_csv('Tool/static/csvs/' +
                               current_user.username + 'train' + '.csv')
        for i in df_train.columns:
            if df_train[i].dtypes == object:
                continue
            else:
                numeric_column.append(i)
        numeric_column.remove(y)
        if request.method == 'POST':
            X_train = df_train[numeric_column]
            y_train = df_train[y]
            for j in request.form.getlist('x_cases'):
                X_test.append(float(j))
            X_test = pd.DataFrame([X_test], index=[0], columns=numeric_column)
            lm = LinearRegression()
            lm.fit(X_train, y_train)
            predictions = lm.predict(X_test)
            flash(predictions)
    else:
        return redirect(url_for('get_premium'))
    return render_template('linear_predict.htm', numeric_column=numeric_column, y=y)

# logistic regression


@app.route('/dashboard2', methods=['GET', 'POST'])
@login_required
def logistic():
    if current_user.membership == 'premium':
        try:
            mylist = ['import pandas as pd', 'import numpy as np',
                      'from sklearn.linear_model import LogisticRegression']
            numeric_column = []
            df_test = pd.read_csv('Tool/static/csvs/' +
                                  current_user.username + 'test' + 'logic' + '.csv')
            df_train = pd.read_csv('Tool/static/csvs/' +
                                   current_user.username + 'train' + 'logic' + '.csv')
            for i in df_train.columns:
                if df_train[i].dtypes == object:
                    continue
                else:
                    numeric_column.append(i)
            if request.method == 'POST':
                train_csv_name = request.form.get("train_csv")
                test_csv_name = request.form.get("test_csv")
                y = request.form.get("column_name")
                numeric_column.remove(y)
                for i in numeric_column:
                    for j in df_train[i]:
                        if j:
                            continue
                        else:
                            numeric_column.remove(i)
                            break
                mylist.append(
                    "df_train = pd.read_csv('" + train_csv_name + "')")
                mylist.append("df_test = pd.read_csv('" + test_csv_name + "')")
                mylist.append(
                    'X_train = df_train[' + str(numeric_column) + ']')
                mylist.append("y_train = df_train['" + y + "']")
                mylist.append('X_test = df_test[' + str(numeric_column) + ']')
                mylist.append('lg = LogisticRegression()')
                mylist.append('lg.fit(X_train , y_train)')
                mylist.append('predictions = lg.predict(X_test)')
                flash(mylist)
        except:
            return redirect(url_for('upload_file_logic'))
    else:
        return redirect(url_for('get_premium'))
    return render_template("dashboard2.htm", numeric_column=numeric_column)

# logistic regression predict y




    # knn


@app.route('/dashboard3', methods=['GET', 'POST'])
@login_required
def knn():
    if current_user.membership == 'premium':
        try:
            mylist = ['import pandas as pd', 'import numpy as np',
                      'from sklearn.preprocessing import StandardScaler',
                      'from sklearn.neighbors import KNeighborsClassifier']
            numeric_column = []
            df_test = pd.read_csv('Tool/static/csvs/' +
                                  current_user.username + 'test' + 'knn' + '.csv')
            df_train = pd.read_csv('Tool/static/csvs/' +
                                   current_user.username + 'train' + 'knn' '.csv')
            for i in df_train.columns:
                if type(df_train[i][0]) == str:
                    continue
                else:
                    numeric_column.append(i)
            if request.method == 'POST':
                train_csv_name = request.form.get("train_csv")
                test_csv_name = request.form.get("test_csv")
                y = request.form.get("column_name")
                numeric_column.remove(y)
                mylist.append(
                    "df_train = pd.read_csv('" + train_csv_name + "')")
                mylist.append("df_test = pd.read_csv('" + test_csv_name + "')")
                mylist.append('scaler = StandardScaler()')
                mylist.append('scaler.fit(df_train)')
                mylist.append('scaled_features = scaler.transform(df_train)')
                mylist.append(
                    'df_feat = pd.DataFrame(scaled_features, columns=df_train.columns)')
                mylist.append(
                    'X_train = df_train[' + str(numeric_column) + ']')
                mylist.append("y_train = df_train['" + y + "']")
                mylist.append('X_test = df_test[' + str(numeric_column) + ']')
                mylist.append('knn = KNeighborsClassifier(n_neighbors=10)')
                mylist.append('knn.fit(X_train , y_train)')
                mylist.append('predictions = knn.predict(X_test)')
                flash(mylist)
        except:
            return redirect(url_for('upload_file_knn'))
    else:
        return redirect(url_for('get_premium'))
    return render_template("dashboard3.htm", numeric_column=numeric_column)


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

        if user is not None and user.check_password(form.password.data):

            login_user(user)

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('linear')
            return redirect(next)
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


@app.route('/queryform', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        train = request.files['train']
        test = request.files['test']
        train.save('Tool/static/csvs/' +
                   current_user.username + 'train' + '.csv')
        test.save('Tool/static/csvs/' +
                  current_user.username + 'test' + '.csv')
        return redirect(url_for('linear'))
    return render_template('query.htm')


@app.route('/queryform2', methods=['GET', 'POST'])
@login_required
def upload_file_logic():
    if request.method == 'POST':
        train = request.files['train']
        test = request.files['test']
        train.save('Tool/static/csvs/' +
                   current_user.username + 'train' + 'logic' + '.csv')
        test.save('Tool/static/csvs/' +
                  current_user.username + 'test' + 'logic' + '.csv')
        return redirect(url_for('logistic'))
    return render_template('query.htm')


@app.route('/queryform3', methods=['GET', 'POST'])
@login_required
def upload_file_knn():
    if request.method == 'POST':
        train = request.files['train']
        test = request.files['test']
        train.save('Tool/static/csvs/' +
                   current_user.username + 'train' + 'knn' + '.csv')
        test.save('Tool/static/csvs/' +
                  current_user.username + 'test' + 'knn' + '.csv')
        return redirect(url_for('knn'))
    return render_template('query.htm')


@app.route('/get/premium', methods=['GET', 'POST'])
@login_required
def get_premium():
    return render_template('premium_get.htm')

@app.route('/to/premium/adshsdjkavnjzsvngb/NFvdbnadifbsrt/ojgbdobmkdgvdkgbmsfksrn', methods=['GET', 'POST'])
@login_required
def premium_to():
    current_user.membership = 'premium'
    db.session.commit()
    return redirect(url_for('index'))


########## PAYMENTS ##################

@app.route('/<id>/payment2', methods=['GET','POST'])
def sub(id):
    sub = User.query.get_or_404(id)
    return render_template('payment.htm', public_key=public_key, id=id)

@app.route('/thankyou')
def thankyou():
    return redirect(url_for('premium_to'))

@app.route('/payment', methods=['POST'])
def payment():

    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
        amount=4999,
        customer=customer.id,
        currency='usd',
        description='Book'
    )


    return redirect(url_for('thankyou'))

if __name__ == '__main__':
    app.run(debug=True)
