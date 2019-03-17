# Ruokaa

## Tsoha-harjoitustyö

![luokkakaavio](http://yuml.me/715869f5.png)

Ruokaa -nettisivulla käyttäjä voi selata ja etsiä ruokia, joita muut käyttäjät ovat sinne luoneet.
Jotta voi luoda ruoan, pitää olla luonut tunnuksen sekä kirjautunut järjestelmään.
Ruoalla on tieto sen luoneesta käyttäjästä. Käyttäjä voi poistaa omia ruokiaan.
Käyttäjä pystyy muokkaamaan ruoan nimeä ja ohjetta.(CRUD)
Käyttäjä pystyy päivittämään omia tietojaan, sekä myös poistamaan tilinsä. (CRUD)
Käyttäjä pystyy myös kommentoimaan jokaista ruokaa, sekä antamaan tykkäyksen (tai miinuksen) ruoille.
Jos jonkin ruoan tykkäykset menee tarpeeksi miinuksella, se piilotetaan kokonaan.

Ruoalle myös syötetään raaka-aineita. Jos kyseistä raaka-ainetta ei vielä ole olemassa, luodaan sellainen. (Jos raaka-aineella ei ole ruokia, poistetaan se)

Ruokanäkymässä ruoat listataan aakkosjärjestyksessä nimen mukaan. Näytetään nimi ja tykkäykset ja kesto.

Ruoan nimeä painettaessa päästään katsomaan ruoan kaikkia tietoja. Tässä näkymässä voi myös kommentoida ruokia sekä antaa tykkäyksiä tai miinuksia.

Ruokia etsittäessä voidaan määritellä montaako ruokaa etsitään, sekä jokaiselle (tai kaikille) valmistuksen maksimikesto, sekä yksi raaka-aine joka ruoan tulee sisältää.

Ohjelma pystyy myös arpomaan ruokien järjestyksen näkymässä.
