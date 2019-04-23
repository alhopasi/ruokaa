from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators
from application.foods.models import Ingredient

class NewFoodForm(FlaskForm):
    name = StringField("Ruoka", [validators.Length(min=3, max=20, message="Kentän tulee olla 3-20 kirjainta")])
    recipe = TextAreaField("Ohje", [validators.Length(min=10, max=4000, message="Kentän tulle olla vähintään 10 kirjainta")])
    duration = SelectField("Kesto", choices = [('15','15 min'),('30','30 min'),('45','45 min'),('60','60 min')], validators = [validators.DataRequired('Please choose a duration')])
    
    ingredient1 = StringField("Raaka-aine 1", [validators.Length(max=20, min = 3, message="Kentän tulle olla 3-20 kirjainta")])
    ingredient2 = StringField("Raaka-aine 2", [validators.Length(max=20, message="Kentän tulle olla 3-20 kirjainta")])
    ingredient3 = StringField("Raaka-aine 3", [validators.Length(max=20, message="Kentän tulle olla 3-20 kirjainta")])
    ingredient4 = StringField("Raaka-aine 4", [validators.Length(max=20, message="Kentän tulle olla 3-20 kirjainta")])

    class Meta:
        csrf = False
