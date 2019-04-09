from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError

class LoginForm(FlaskForm):
    username = StringField("Käyttäjätunnus")
    password = PasswordField("Salasana")

    class Meta:
        csrf = False

class NewAccountForm(FlaskForm):
    name = StringField("Nimi", [validators.Length(min=2, max=20)])
    username = StringField("Käyttäjätunnus", [validators.Length(min=3, max=20)])
    password = PasswordField("Salasana", [validators.Length(min=5, max=20)])

    class Meta:
        csrf = False

class UpdateAccountForm(FlaskForm):

    def empty_or_length(min=-1, max=20):
        message = 'Pitää olla %d-%d kirjainta.' % (min, max)

        def _empty_or_length(form, field):
            if not (len(field.data) == 0 or len(field.data) >= min) or len(field.data <= max):
                raise ValidationError(message)

        return _empty_or_length

    name = StringField("Nimi", [empty_or_length(min=2, max=20) ])
    username = StringField("Käyttäjätunnus", [empty_or_length(min=3, max=20) ])
    password = PasswordField("Salasana", [empty_or_length(min=5, max=20) ])

    class Meta:
        csrf = False
