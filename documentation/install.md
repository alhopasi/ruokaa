# Ruokaa

## Asennusohje

**Paikallinen asennus**

- Kopioi kaikki tiedostot johonkin kansioon.
- Siirry kyseisen kansion juureen.
- Asenna projektin riippuvuudet komennolla `pip install -r requirements.txt`
- Asenna virtuaaliympäristö komennolla `python3 -m venv venv`
- Käynnistä virtuaaliympäristö komennolla `source venv/bin/activate`
- Käynnistä ohjelma komennolla `python run.py`
- Avaa selaimella sivu: http://localhost:5000/

**Asennus Herokuun**
- Kopioi kaikki tiedostot johonkin kansioon.
- Siirry kyseisen kansion juureen.
- Tee kansiosta git-projekti komennolla: `git init`. Jos kloonasit projektin gitHubista, voit ohittaa tämän askeleen.
- Luo Herokuun uusi sovellus komennolla: `heroku create <nimi>`
- Lisätään gitiin tieto Herokusta komennolla: `git remote add heroku https://git.heroku.com/<nimi>.git`
- Lähetetään projekti Herokuun komennolla: `git add .` sekä `git commit -m "Initial commit"` ja `git push heroku master`.
- Nyt sovelluksen pitäisi olla toimivana osoitteessa `https://<nimi>.herokuapp.com`