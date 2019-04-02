from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SelectField, validators
from application.foods.models import Ingredient

class NewFoodForm(FlaskForm):
    name = StringField("Ruoka", [validators.Length(min=3, max=20)])
    recipe = TextAreaField("Ohje", [validators.Length(min=10, max=4000)])
    duration = RadioField("Kesto", choices = [('15','15 min'),('30','30 min'),('45','45 min'),('60','60 min')], validators = [validators.DataRequired('Please choose a duration')])
    
    ingredient1 = StringField("Raaka-aine 1", [validators.Length(max=20, min = 3)])
    ingredient2 = StringField("Raaka-aine 2", [validators.Length(max=20)])
    ingredient3 = StringField("Raaka-aine 3", [validators.Length(max=20)])
    ingredient4 = StringField("Raaka-aine 4", [validators.Length(max=20)])

    class Meta:
        csrf = False

class UpdateFoodForm(FlaskForm):
    name = StringField("Ruoka", [validators.Length(min=3, max=20)])
    ingredient = StringField("Raaka-aine", [validators.Length(max=20, min = 3)])
    recipe = TextAreaField("Ohje", [validators.Length(min=10, max=4000)])
    duration = RadioField("Kesto", choices = [('15','15 min'),('30','30 min'),('45','45 min'),('60','60 min')], validators = [validators.DataRequired('Please choose a duration')])

    class Meta:
        csrf = False