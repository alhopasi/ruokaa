from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators
from application.foods.models import Ingredient

class NewFoodForm(FlaskForm):
    name = StringField("Ruoka", [validators.Length(min=3, max=20, message="Nimen tulee olla 3-20 kirjainta")])
    recipe = TextAreaField("Ohje", [validators.Length(min=10, max=4000, message="Ohjeen tulle olla vähintään 10 kirjainta")])
    duration = SelectField("Kesto", choices = [('15','15 min'),('30','30 min'),('45','45 min'),('60','60 min')], validators = [validators.DataRequired('Please choose a duration')])
    ingredients = []
    
    ingredient = StringField("Raaka-aine")

    class Meta:
        csrf = False
