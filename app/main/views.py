from . import main
from flask import render_template, request, redirect, url_for, flash


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')
    
@main.route('/vacations-list', methods=["GET", "POST"])
def vacations_list():
    return render_template('vacations-list.html')
