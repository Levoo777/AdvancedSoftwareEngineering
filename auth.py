from flask import Blueprint, render_template, redirect, url_for, request, flash
from database.db_manager import DB_Manager
from datetime import date
from hashlib import sha256
from flask_login import login_user, logout_user, login_required, current_user, user_logged_out
from classes.User import User
import secrets


from functools import wraps
from flask import abort

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email_input')
    password = request.form.get("hashedPassword")
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)
    DB.disconnect()

    if not data:
        data = ["Fail", "aa"*32]

    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if user_pw == data[0]:
        user = User(data[2])
        login_user(user, remember=True)
        return redirect(url_for('main.profile'))

    
    flash('Please check your login details and try again.')
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email_input')
    username = request.form.get('username_input')
    joining = date.today()
    password = request.form.get("hashedPassword")
    salt = secrets.token_hex(32)
    pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(salt), bytes.fromhex(password)))).hexdigest()

    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    if DB.get_login_data_by_mail(email):
        DB.disconnect()
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    else:
        DB.insert_user(("NULL", email, username, joining, pw), salt)
        DB.show_all_users()
        DB.disconnect()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@user_logged_out.connect
def on_user_logged_out(sender, user, **extra):
    db = DB_Manager("database/kundendatenbank.sql", "users")
    db.connect()
    db.update_user((user._id, "lobby", 0))
    db.disconnect()