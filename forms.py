from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class StudentForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    age = IntegerField(label="Age", validators=[DataRequired()])
    major = StringField(label="Major")
    submit = SubmitField(label="Submit")
