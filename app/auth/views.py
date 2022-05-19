from flask import render_template, redirect, url_for, flash, request
from . import auth
from ..models import Users
from .forms import SignupForm, LoginForm
from flask_login import login_required, login_user, logout_user
from .. import db
# from flask_login import login_required, login_user, logout_user
# from .. import db
import os



@auth.route('/register', methods=["GET", "POST"])
def register():
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = Users(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data,
                         password=form.password.data, role_id='users')
            db.session.add(user)
            db.session.commit()

            flash("Account created Successfully", category='success')

            return redirect(url_for('auth.login'))

    return render_template('auth/register.html', signup_form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if request.method == "POST":
        if login_form.validate_on_submit():
            user = Users.query.filter_by(email=login_form.email.data).first()
            if user is not None and user.verify_password(login_form.password.data):
                login_user(user)
                flash('Login successful', category='success')
                return redirect(request.args.get('next') or url_for('main.vacations_list'))
            else:
                flash("Wrong credentials", category="danger")
        else:
            flash("Please provide the necessary credentials below")

    return render_template('auth/login.html', login_form=login_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
    if login_form.validate_on_submit():
        # user = User.query.filter_by(email = login_form.email.data).first()
        # if user is not None and user.verify_password(login_form.password.data):
        #     login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

    # flash('Invalid username or Password')

    
    return render_template('auth/login.html',login_form = login_form)




            

# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("main.index"))
