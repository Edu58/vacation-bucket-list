from crypt import methods
import email
from turtle import title
from xml.etree.ElementTree import Comment
from . import main
from flask import render_template, request, redirect, url_for, flash




@main.route('/contact')
def contact():
    
    title = 'Contact Us'
    return render_template('contact/contact.html', title = title)

@main.route('/enquire', methods=['GET','POST'])
def enquire():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    county = request.form.get("county")
    destination_county = request.form.get("destination_county")
    comment = request.form.get("comment")
    
    title = 'Thank you,we have recieved your details'
    return render_template('contact/enquire.html', title = title, first_name = first_name, last_name = last_name, email=email, county=county,destination_county = destination_county, comment = comment)