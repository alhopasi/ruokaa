from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError

class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus")
    password = PasswordField("Salasana")

    class Meta:
        csrf = False

class NewAccountForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=2, max=20, message="Nimen tulee olla 2-20 kirjainta")])
    username = StringField("Käyttäjätunnus", [validators.Length(min=3, max=20, message="Käyttäjätunnuksen tulee olla 3-20 kirjainta")])
    password = PasswordField("Salasana", [validators.Length(min=5, max=20, message="Salasanan tulee olla 5-20 kirjainta")])

    class Meta:
        csrf = False

class UpdateAccountForm(FlaskForm):
    def empty_or_length(min=-1, max=20):
        message = 'Salasanan tulee olla %d-%d kirjainta.' % (min, max)

        def _empty_or_length(form, field):
            if not (len(field.data) == 0 or (len(field.data) >= min and len(field.data) <= max)):
                raise ValidationError(message)

        return _empty_or_length

    name = StringField("Nimi", [validators.Length(min=2, max=20, message="Nimen tulee olla 2-20 kirjainta")])
    username = StringField("Käyttäjätunnus", [validators.Length(min=3, max=20, message="Käyttäjätunnuksen tulee olla 3-20 kirjainta")])
    password = PasswordField("Salasana", [empty_or_length(min=5, max=20) ])

    class Meta:
        csrf = False
