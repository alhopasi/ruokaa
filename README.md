# Ruokaa

## Tsoha-harjoitustyö

![luokkakaavio](http://yuml.me/c1b577e2.png)

Ruokaa -nettisivulla käyttäjä voi selata ja etsiä ruokia, joita muut käyttäjät ovat sinne luoneet.
Jotta voi luoda ruoan, pitää olla luonut tunnuksen sekä kirjautunut järjestelmään.
Ruoalla on tieto sen luoneesta käyttäjästä. Käyttäjä voi poistaa omia ruokiaan.
Käyttäjä pystyy muokkaamaan ruoan nimeä ja ohjetta.(CRUD)
Käyttäjä pystyy päivittämään omia tietojaan, sekä myös poistamaan tilinsä. (CRUD)
Ruoalle on aina määritelty avainsana tai avainsanoja. (Esim. Tortillalle: kana, tortilla, tulinen tai makaroonilaatikolle: laatikko, makaroni, jauheliha, liha)

Ruoalle myös syötetään raaka-aineita. Jos kyseistä raaka-ainetta ei vielä ole olemassa, luodaan sellainen. (Jos raaka-aineella ei ole ruokia, poistetaan se)

Ruokanäkymässä ruoat listataan aakkosjärjestyksessä nimen mukaan.

Ruoan nimeä painettaessa päästään katsomaan sen ohjetta, avainsanoja sekä raaka-aineita.

Ruokia etsittäessä voidaan valitaan haetaanko raaka-aineista, avainsanoista vai molemmista, sekä syötetään hakusana. Hakusana etsii (aina) ruoan nimestä sekä raaka-aineista ja/tai avainsanoista ruokia.

Ohjelma pystyy myös luomaan valmiin ruokalistan, joka painottuu monipuolisuuteen, eli etsii ruokia avainsanojen perusteella siten, että se välttää ruokia joissa on sama avainsana.
Jos ruokalistaa luodessa syöttää hakusanan, etsii ohjelma ruokalistalle tämän hakusanan perusteella ruokia.
Käyttäjä voi syöttää ruokalistalle pituuden joka määrittelee montako ruokaa sille arvotaan/etsitään.

Ohjelmasta löytyy myös infosivu, jolla kerrotaan miten haku sekä ruokalistan luonti toimii.
