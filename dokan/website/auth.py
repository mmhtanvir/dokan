from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User , Role
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('Email does not exist', category='error')



    return render_template("login.html", user=current_user)

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        name = request.form.get("name")
        email = request.form.get("email")
        number = request.form.get("number")
        password = request.form.get("password")

        email_exists = User.query.filter_by(email=email).first()

        if email_exists:
            flash('Email already in use', category='error')
        elif len(name) < 2:
            flash('Name to short', category='error')
        elif len(email) < 4:
            flash('Invalid Email', category='error')
        elif len(number) < 9:
            flash('Invalid Email', category='error')
        elif len(password) < 8:
            flash('Password too short', category='error')
        else:
            role = Role.query.first() 
            new_user = User(email=email, name=name, number=number, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))