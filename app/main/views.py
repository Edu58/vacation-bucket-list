from . import main
from flask import render_template, request, redirect, url_for, flash


@main.route('/')
def index():
    return render_template('index.html')