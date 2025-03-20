from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    # The task says about some "Email/login" but in the DB we store emails
    # and I have no clue where to store login according to the given schema
    email = EmailField("Email", validators=[DataRequired()])
    passwd = PasswordField("Password", validators=[DataRequired()])
    passwd_confirmation = PasswordField("Repeat password", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    position = StringField("Position", validators=[DataRequired()])
    speciality = StringField("Speciality", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Submit")
