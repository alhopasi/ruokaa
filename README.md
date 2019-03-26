# Ruokaa

## Tsoha-harjoitustyö

[Ruokaa-app](https://ruokaa-app.herokuapp.com "Ruokaa")

[Tietokantakaavio](documentation/database_diagram.md "Tietokantakaavio"), 
[Käyttötapauksia](documentation/user_stories.md "Käyttötapauksia")

Voit luoda oman käyttäjän tai kokeilla testikäyttäjällä:

käyttäjätunnus: *admin*

salasana: *admin*

Ruokaa -nettisivulla käyttäjä voi selata ja etsiä ruokia, joita muut käyttäjät ovat sinne luoneet.

Kirjautuneena käyttäjä voi:
* luoda ruoan **(tehty)**
* poistaa oman ruokansa
* muokata oman ruokansa tietoja:
  * nimeä
  * kestoa
  * ohjetta
  * raaka-aineita
* tykätä ruoista tai antaa miinuksen (+1 / -1)
* kommentoida jonkun toisen ruokaa (yhden kerran / ruoka)
  * muokata tai poistaa oman kommenttinsa
* vaihtaa omaa tunnustansa / nimeänsä / salasanaansa **(tehty)**
* poistaa oman tilinsä **(tehty)**

Ei-kirjautunut käyttäjä voi:
* luoda uuden käyttäjän **(tehty)**
* kirjautua sisään (tunnuksena toimii sähköposti) **(tehty)** - tunnus voi olla mitä tahansa

Kaikki voivat:
* tarkastella ruokia listalta **(tehty)**
* arpoa itselleen ruokalistan

Ylläpitäjä voi:
* tehdä vähän kaikkea

Näkymät:
* ylävalikko (listanäkymä, lisää ruoka, kirjaudu / omat tiedot) **(tehty)**
* listanäkymä **(työn alla)**
* ruokanäkymä (yksittäiselle ruoalle)
* ruoan lisäysnäkymä **(tehty)**
* käyttäjänäkymä (kirjautuneelle käyttäjälle) / kirjautumisnäkymä (ei-kirjautuneelle) **(tehty)**

Muuta:
Jos jonkin ruoan tykkäykset menee tarpeeksi miinukselle, se piilotetaan kokonaan.

Listanäkymässä ruoat listataan aakkosjärjestyksessä nimen mukaan. Näytetään nimi, ruoan valmistusaika ja tykkäykset.
Painamalla tykkäykset, järjestetään lista tykkäysten mukaan. Tai nimeä, järjestetään nimen mukaan.

Listanäkymässä voi myös filtteröidä *(etsiä)* ruokia valmistusajan tai yhden raaka-aineen ja nimen mukaan. *(saako listan päivittymään reaaliajassa?)*

Ruoan nimeä painettaessa päästään ruoan Ruokanäkymään. Tässä näkymässä voi myös kommentoida ruokia sekä antaa tykkäyksiä tai miinuksia.
Jos ruoka on oma, voidaan sen tietoja muuttaa täällä tai poistaa ruoka kokonaan.
Ruokanäkymässä näkyy ruoan luoneen käyttäjän nimi.

Käyttäjänäkymässä käyttäjä voi tarkastella omia tietojaan sekä muuttaa niitä. Täällä myös näkyvät ruoat jotka käyttäjä on luonut (ja voi siirtyä niiden tietoihin).

