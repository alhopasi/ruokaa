# Tuodaan Flask käyttön
from flask import Flask
app = Flask(__name__)

# Tuodaan SQLAlchemy käyttöön
from flask_sqlalchemy import SQLAlchemy
# Käytetään foods.db-nimistä SQLite-tietokantaa
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foods.db"
# Pyydetään SQLAlchemyä tulostamaan kaikki SQL-kyselyt
app.config["SQLALCHEMY_ECHO"] = True
# Joku asetus mistä tuli valitusta
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Luodaan db-olio.
db = SQLAlchemy(app)

# Lisätään näkymät
from application import views
from application.foods import views

# Luetaan tietokantamallit
from application.foods import models

# Luodaan lopulta tarvittavat tietokantataulut
db.create_all()
