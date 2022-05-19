from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, IntegerField, DateTimeLocalField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, length


class NewDestination(FlaskForm):
    place = StringField('Destination', validators=[DataRequired(), length(max=50)])
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    date_of_visit = DateTimeLocalField('Day and time of visit', format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    description = TextAreaField('Describe your experience', validators=[DataRequired()])
    duration = IntegerField('Duration of your stay', validators=[DataRequired()])
    amount_spent = IntegerField('Total amount spent', validators=[DataRequired()])
    submit = SubmitField('submit')
from wtforms import StringField, TextAreaField, SubmitField, validators
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired, Email, length, ValidationError



class ContactForm(FlaskForm):
    firstName =StringField('First Name', [validators.DataRequired("Enter your first name")])
    lastName =StringField('Last Name', [validators.DataRequired("Enter your last name")])
    email = StringField('E-mail', [validators.DataRequired("Enter a valid email address"), validators.Email("Enter a valid email address")])
    subject = StringField('Subject', [validators.DataRequired("What's the nature of your message?")])
    message = TextAreaField('Message', [validators.DataRequired("Didn't you want to say something?")])
    submit = SubmitField('Send')
