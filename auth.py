from flask import Blueprint, render_template, redirect, url_for, request, flash
from database.db_manager import DB_Manager
from datetime import date
from hashlib import sha256
from flask_login import login_user, logout_user, login_required, current_user, user_logged_out
from classes.User import User
import secrets
import pyotp
import base64
import qrcode
from io import BytesIO


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
    otp = request.form.get("otp")
    print(f"OTP: {otp}")
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)
    if not data:
        data = ["Fail", "aa"*32, 0, 0]
        mfa = [None]   
    else:
        mfa = DB.get_mfa_by_id(data[2])

    DB.disconnect()
    print(mfa)
    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if mfa[0] and not otp and user_pw == data[0]:
        return render_template("login_2fa.html", email = email, password = password, user_authenticated = current_user.is_authenticated)


    if user_pw == data[0]:
        if mfa[0]:
            if pyotp.TOTP(mfa[0]).verify(otp):
                user = User(data[2])
                login_user(user, remember=True)
                return redirect(url_for('main.profile'))
        else:
            user = User(data[2])
            login_user(user, remember=True)
            return redirect(url_for('main.profile'))
    
    flash('Bitte überprüfe deine Logindaten und versuche es erneut.')
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


@auth.route('/reset_password')
@login_required
def reset_password():
    return render_template('reset_password.html', user_authenticated = current_user.is_authenticated)

@auth.route('/reset_password', methods=['POST'])
@login_required
def reset_password_post():
    email = current_user._email
    password = request.form.get("hashedPasswordOld")

    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)
    DB.disconnect()

    if not data:
        data = ["Fail", "aa"*32]
    
    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if user_pw == data[0]:
            password = request.form.get("hashedPasswordNew")
            salt = secrets.token_hex(32)
            pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(salt), bytes.fromhex(password)))).hexdigest()
            DB = DB_Manager("database/kundendatenbank.sql", "users")
            DB.connect()
            DB.update_user((current_user._id, "password", pw))
            DB.update_user((current_user._id, "salt", salt))
            DB.disconnect()
            flash("Password change was successfully", 'success')
            return redirect(url_for('main.profile'))
    
    flash('Wrong password')
    return redirect(url_for('auth.reset_password'))

@auth.route('/delete_account')
@login_required
def delete_account():
    return render_template('delete_account.html', user_authenticated = current_user.is_authenticated)

@auth.route('/delete_account', methods=['POST'])
@login_required
def delete_account_post():
    email = current_user._email
    password = request.form.get("hashedPassword")
    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)
    DB.disconnect()

    if not data:
        data = ["Fail", "aa"*32]
    
    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if user_pw == data[0]:
        id = current_user._id
        logout_user()
        DB = DB_Manager("database/kundendatenbank.sql", "users")
        DB.connect()
        DB.delete_user(id)
        DB.disconnect()
        return redirect(url_for('main.index'))

    flash("Wrong password")
    return redirect(url_for('auth.delete_account'))

@auth.route("/signup/2fa/")
@login_required
def signup_2fa():
    secret = pyotp.random_base32()
    mail = current_user._email
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(mail, issuer_name='L.B.-Blokus')
    qr = qrcode.make(otp_uri)

    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return render_template("signup_2fa.html", secret=secret, qr_code=qr_base64, user_authenticated = current_user.is_authenticated)

@auth.route("/signup/2fa/", methods=["POST"])
@login_required
def signup_2fa_form():
    secret = request.form.get("secret")
    otp = request.form.get("otp")
    id = current_user._id
    if pyotp.TOTP(secret).verify(otp):
        DB = DB_Manager("database/kundendatenbank.sql", "users")
        DB.connect()
        DB.update_user((id, "mfa", secret))
        DB.disconnect()
        flash("The 2FA Token is valid", "success")
        return redirect(url_for('main.profile'))
    else:
        flash("The 2FA Token is not valid! Please scan the new QR-Code!", "danger")
        return redirect(url_for("auth.signup_2fa"))

@auth.route('/delete_2fa')
@login_required
def delete_2fa():
    return render_template('delete_2fa.html', user_authenticated = current_user.is_authenticated)

@auth.route('/delete_2fa', methods=['POST'])
@login_required
def delete_2fa_post():
    email = current_user._email
    password = request.form.get("hashedPassword")

    DB = DB_Manager("database/kundendatenbank.sql", "users")
    DB.connect()
    data = DB.get_login_data_by_mail(email)
    mfa = DB.get_mfa_by_id(data[2])
    DB.disconnect()

    if not data:
        data = ["Fail", "aa"*32]
    
    user_pw = sha256(bytes(x ^ y for x, y in zip(bytes.fromhex(data[1]), bytes.fromhex(password)))).hexdigest()

    if user_pw == data[0]:
        if not mfa[0]:
            flash("2FA is not active")
            return redirect(url_for('auth.delete_2fa'))


        id = current_user._id
        DB = DB_Manager("database/kundendatenbank.sql", "users")
        DB.connect()
        DB.remove_mfa(id)
        DB.disconnect()
        flash("2FA was removed")
        return redirect(url_for('main.profile'))
        
    flash("Wrong password")
    return redirect(url_for('auth.delete_2fa'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/highscore')
@login_required
def highscore():
    db = DB_Manager("database/kundendatenbank.sql", "users")
    db.connect()
    highscore =db.get_highscore(current_user._id)
    db.disconnect()
    return render_template('highscore.html', highscore=highscore[0])


@user_logged_out.connect
def on_user_logged_out(sender, user, **extra):
    db = DB_Manager("database/kundendatenbank.sql", "users")
    db.connect()
    db.update_user((user._id, "lobby", 0))
    db.disconnect()