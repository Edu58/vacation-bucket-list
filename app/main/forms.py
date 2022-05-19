from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, DateTimeField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, length


class NewDestination(FlaskForm):
    place = StringField('Destination', validators=[DataRequired(), length(max=50)])
    photo = FileField('Cover image',
                      validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    date_of_visit = DateTimeField('Date of visit', validators=[DataRequired()])
    description = TextAreaField('Pitch Content', validators=[DataRequired()])
    amount_spent = IntegerField('Amount spent', validators=[DataRequired()])
    submit = SubmitField('submit')
