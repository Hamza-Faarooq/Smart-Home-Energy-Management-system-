import paho.mqtt.client as mqtt
from flask import flask, request, jsonify, render_template, redirect, url_for
from flask_login import loginmanager, usermixin, login_user, logout_user, login_required

import sqlite3
import pandas as pd
from sklearn.linear_model import linearregression
import numpy as np
import json

# initialize flask application
app = flask(__name__)
app.config[‘secret_key’] = ‘your_secret_key’

# initialize flask-login
login_manager = loginmanager()
login_manager.init_app(app)

# create sqlite database for storing user data
conn = sqlite3.connect(‘users.db’)
cursor = conn.cursor()
cursor.execute(‘’’create table if not exists users (
                    id integer primary key,
                    username text unique,
                    password text
                )’’’)
conn.commit()

# define user class for flask-login
class user(usermixin):
    def __init__(self, user_id):
        self.id = user_id

# user loader function for flask-login
@login_manager.user_loader
def load_user(user_id):
    return user(user_id)

# route for user login
@app.route(‘/login’, methods=[‘get’, ‘post’])
def login():
    if request.method == ‘post’:
        username = request.form[‘username’]
        password = request.form[‘password’]

        # check if the user exists in the database and verify password
        cursor.execute(‘’’select * from users where username=? and password=?’’’, (username, password))
        user = cursor.fetchone()

        if user:
            user_obj = user(user[0])
            login_user(user_obj)
            return redirect(url_for(‘dashboard’))
        else:
            return render_template(‘login.html’, error=’invalid username or password’)

    return render_template(‘login.html’, error=none)

# route for user logout
@app.route(‘/logout’)
@login_required
def logout():
    logout_user()
    return redirect(url_for(‘login’))

# route for dashboard (requires login)
@app.route(‘/dashboard’)
@login_required
def dashboard():
    return render_template(‘dashboard.html’)

# rest of the code for energy management system (omitted for brevity)

if __name__ == ‘__main__’:
    app.run(debug=true)

