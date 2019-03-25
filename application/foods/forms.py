from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, validators

class NewFoodForm(FlaskForm):
    name = StringField("Food", [validators.Length(min=3)])
    recipe = TextAreaField("Recipe", [validators.Length(min=10)])
    duration = RadioField("Duration", choices = [('15','15 min'),('30','30 min'),('45','45 min'),('60','60 min')], validators = [validators.DataRequired('Please choose a duration')])

    class Meta:
        csrf = False