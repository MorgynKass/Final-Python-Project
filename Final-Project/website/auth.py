from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Protein, Goal
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('tracker.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist. Please create an account.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        goal = 0
        daily = 0

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 6:
            flash('Email must be greater than 5 characters.', category='error')
        elif len(first_name) < 1:
            flash('First name must be greater than 0 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 4 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            new_info = Protein(daily_protein=daily, user_id=current_user.id)
            new_goal = Goal(goal=goal, percent=0, remaining_value=0,user_id=current_user.id)
            db.session.add(new_info)
            db.session.add(new_goal)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('tracker.home'))

    return render_template("sign_up.html", user=current_user)
