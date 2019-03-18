# Tuodaan Flask käyttön
from flask import Flask
app = Flask(__name__)

# Tuodaan SQLAlchemy käyttöön
from flask_sqlalchemy import SQLAlchemy
# Käytetään foods.db-nimistä SQLite-tietokantaa,
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foods.db"
# Pyydetään SQLAlchemyä tulostamaan kaikki SQL-kyselyt
app.config["SQLALCHEMY_ECHO"] = True

# Luodaan db-olio.
db = SQLAlchemy(app)

# Luetaan kansiosta application tiedoston views sisältö
from application import views

# Luetaan tietokantamallit
from application.foods import models

# Luodaan lopulta tarvittavat tietokantataulut
db.create_all()
