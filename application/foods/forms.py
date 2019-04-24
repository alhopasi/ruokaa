from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, validators
from application.foods.models import Ingredient

class NewFoodForm(FlaskForm):
    name = StringField("Ruoka", [validators.Length(min=3, max=20, message="Nimen tulee olla 3-20 kirjainta")])
    recipe = TextAreaField("Ohje", [validators.Length(min=10, max=4000, message="Ohjeen tulle olla vähintään 10 kirjainta")])
    duration = SelectField("Kesto", choices = [('15','15 min'),('30','30 min'),('45','45 min'),('60','60 min')], validators = [validators.DataRequired('Valitse kesto')])
    food_type = SelectField("Tyyppi", choices= [('Kala','Kala'),('Kana','Kana'),('Kasvis','Kasvis'),('Nauta','Nauta'),('Porsas','Porsas'),('Riista','Riista')], validators = [validators.DataRequired('Valitse tyyppi')])
    ingredients = []
    
    ingredient = StringField("Raaka-aine")

    class Meta:
        csrf = False

class MenuForm(FlaskForm):
    food_type = SelectField("Tyyppi", choices= [('Kaikki','Kaikki'),('Kala','Kala'),('Kana','Kana'),('Kasvis','Kasvis'),('Nauta','Nauta'),('Porsas','Porsas'),('Riista','Riista')], validators = [validators.DataRequired('Valitse tyyppi')])
    
    class Meta:
        csrf = False