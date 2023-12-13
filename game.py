from flask import Blueprint, render_template, redirect, url_for, request, flash
from database.db_manager import DB_Manager
from datetime import date
from hashlib import sha256
from flask_login import login_user, logout_user, login_required, current_user, user_logged_out
from classes.User import User


game = Blueprint('game', __name__)

