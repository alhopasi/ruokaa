from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, validators

class NewFoodForm(FlaskForm):
    name = StringField("Ruoka", [validators.Length(min=3)])
    recipe = TextAreaField("Ohje", [validators.Length(min=10)])
    duration = RadioField("Kesto", choices = [('15','15 min'),('30','30 min'),('45','45 min'),('60','60 min')], validators = [validators.DataRequired('Please choose a duration')])

    class Meta:
        csrf = False

class UpdateFoodForm(FlaskForm):
    name = StringField("Ruoka", [validators.Length(min=3)])

    class Meta:
        csrf = False