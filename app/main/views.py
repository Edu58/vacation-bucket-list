from . import main
from app import photos, db, mail
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, flash, abort
from .forms import NewDestination
from app.models import Vacations
from werkzeug.utils import secure_filename
from sqlalchemy import desc
from flask_mail import Message
from app.models import Comments, Users
from .forms import ContactForm, CommentForm


@main.route('/')
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
        return redirect(url_for('main.vacations_list'))

    return render_template('add_vacation.html', add_vacation_form=form)


@main.route('/contact', methods=["GET", "POST"])
@login_required
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if not form.validate():
            flash('You must enter something into all of the fields', category="warning")
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
    form = CommentForm()
    vacation = Vacations.query.filter_by(vacation_id=vacation_id).first()
    comments = Comments.query.filter_by(vacation_id=vacation_id).all()

    if request.method == "POST" and form.validate_on_submit():
        new_comment = Comments(comment=form.comment.data, vacation_id=vacation_id, user_id=current_user.user_id)
        Comments.save_comment(new_comment)

        flash("Comment posted successfully", category="success")
        return redirect(url_for('main.vacation_details', vacation=vacation, comment_form=form, comments=comments,
                                place=vacation.place, vacation_id=vacation_id))

    return render_template('vacation-details.html', vacation=vacation, comment_form=form, comments=comments)


@main.route('/delete-vacation/<vacation_id>', methods=["GET", "POST"])
@login_required
def delete_vacation(vacation_id):
    vacation_to_delete = Vacations.query.filter_by(vacation_id=vacation_id).first()

    if vacation_to_delete:
        db.session.delete(vacation_to_delete)
        db.session.commit()
        flash('Post deleted successfully', category='success')
        return redirect(url_for('main.vacations_list'))
    else:
        pass

    return redirect(url_for('main.vacations_list'))


@main.route('/profile/<first_name>', methods=["GET", "POST"])
@login_required
def profile(first_name):
    return render_template('profile.html', user=current_user)


@main.route('/user/<user_id>/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_pic(user_id):
    user = Users.query.filter_by(user_id=user_id).first()

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_path = path
        db.session.commit()

    return redirect(url_for('main.profile', first_name=current_user.first_name))


@main.route('/user/update-profile-picture/<user_id>', methods=['POST'])
@login_required
def update_profile_pic(user_id):
    user = Users.query.filter_by(user_id=user_id).first()

    if user is None:
        abort(404)

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_path = path
        db.session.commit()

    return redirect(url_for('main.profile', first_name=current_user.first_name))
