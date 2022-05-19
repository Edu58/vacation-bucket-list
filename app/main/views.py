from . import main
from app import photos, db, mail
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash
from .forms import NewDestination
from app.models import Vacations
from werkzeug.utils import secure_filename
from sqlalchemy import desc
from flask_mail import Message, Mail
from .forms import ContactForm


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

    if request.method == "POST" and form.validate_on_submit():
        image = form.photo.data

        filename = secure_filename(image.filename)
        photos.save(image)
        path = f'photos/{filename}'

        new_vacation = Vacations(place=form.place.data, description=form.description.data,
                                 pricing=form.amount_spent.data, days=form.duration.data,
                                 date_of_visit=form.date_of_visit.data, destination_photo=path,
                                 user_id=current_user.user_id)

        db.session.add(new_vacation)
        db.session.commit()
        flash("Vacation added successfully", category='success')
        return redirect(url_for('main.vacation_list'))

    return render_template('add_vacation.html', add_vacation_form=form)


@main.route('/contact', methods=["GET", "POST"])
@login_required
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if not form.validate():
            flash('You must enter something into all of the fields')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='[SENDER EMAIL]', recipients=['[RECIPIENT EMAIL]'])
            msg.body = """
                        From: %s %s <%s>
                        %s
                        """ % (form.firstName.data, form.lastName.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('contact.html', success=True)
    return render_template('contact.html', title='Contact Us', form=form)


@main.route('/vacations-list', methods=["GET", "POST"])
@login_required
def vacations_list():
    vacations = Vacations.query.order_by(desc(Vacations.posted_on))
    return render_template('vacations-list.html', vacations=vacations)


@main.route('/vacation/<place>/<vacation_id>', methods=["GET", "POST"])
@login_required
def vacation_details(place, vacation_id):
    vacation = Vacations.query.filter_by(vacation_id=vacation_id).first()
    return render_template('vacation-details.html', vacation=vacation)
