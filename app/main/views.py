from . import main
from flask_login import login_required
from flask import render_template, request, redirect, url_for, flash
from .forms import NewDestination


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/about')
@login_required
def about():
    return render_template('about.html')


@main.route('/add-vacation', methods=["GET", "POST"])
@login_required
def add_vacation():
    form = NewDestination()

    if request.method == "POST":
        if form.validate_on_submit():
            print(form.place.data)
    return render_template('add_vacation.html', add_vacation_form=form)


@main.route('/vacations-list', methods=["GET", "POST"])
@login_required
def vacations_list():
    return render_template('vacations-list.html')
