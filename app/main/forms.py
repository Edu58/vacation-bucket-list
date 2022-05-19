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
