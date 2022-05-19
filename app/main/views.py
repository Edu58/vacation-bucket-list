from . import main
from flask import render_template, request, redirect, url_for, flash
from flask_mail import Message, Mail
from .forms import ContactForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contact',methods = ["GET","POST"])
def contact():
        form = ContactForm()
        if request.method == 'POST':
                if form.validate() == False:
                        flash('You must enter something into all of the fields')
                        return render_template('contact.html', form = form)
                else:
                        msg = Message(form.subject.data, sender='[SENDER EMAIL]', recipients=['[RECIPIENT EMAIL]'])
                        msg.body = """
                        From: %s %s <%s>
                        %s
                        """ % (form.firstName.data, form.lastName.data, form.email.data, form.message.data)
                        mail.send(msg)
                        return render_template('contact.html', success=True)
        return render_template('contact.html',title = 'Contact Us',form = form)
            
    
@main.route('/vacations-list', methods=["GET", "POST"])
def vacations_list():
    return render_template('vacations-list.html')
