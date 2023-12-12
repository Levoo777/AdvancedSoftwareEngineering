
from flask import Blueprint, render_template
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html', user_authenticated = current_user.is_authenticated)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user._name, lobby=current_user._lobby, user_authenticated = current_user.is_authenticated)