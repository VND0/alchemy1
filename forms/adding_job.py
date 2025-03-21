from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired()])
    lead_id = IntegerField("Team Leader ID", validators=[DataRequired()])
    work_size = IntegerField("Work Size", validators=[DataRequired()])
    collab_list = StringField("Collaborators", validators=[DataRequired()])
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField("Submit")
