from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

# We're using flask-wtf for our form

class TodoForm(FlaskForm):
    # these fields are then used to populate our form template
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    # note the "tuples" below - the choices are what the user sees and the value that is sent to the backend
    completed = SelectField("Completed", choices=[("False", "False"), ("True", "True")], validators=[DataRequired()])
    submit = SubmitField("Add Todo")