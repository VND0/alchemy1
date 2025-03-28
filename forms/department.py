from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    chief = IntegerField("Chief", validators=[DataRequired()])
    members = StringField("Members", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
