# Pohdintaa

## Tietokannasta

- Paikallinen tietokanta SQLitellä on mielestäni hyvä juttu, mutta aiheuttaa pieniä hankaluuksia jos internet-tietokanta on esim. PSQL:llä.
- Hyvää on se, että SQLite on helppo ja nopea käyttää. Sillä saa nopeasti tarkastettua tietokannan tilan ja voi tehdä muutoksia helposti.
- Hankaluuksia aiheuttaa tietokantojen erilaisuudet. Ne onkin hyvä ottaa huomioon suunnittelussa.
- Esimerkkejä:
  - SQLiten Integer on 8 bittiä kun PSQL vain 4 bittiä. Paikallisessa testauksessa jos syöttää yli 4 bittisen arvon niin se toimii, kun taas PSQL:ssä syöte ei toimi.
  - SQLite osaa konvertoida Stringejä Integereiksi ja päinvastoin. Mutta PSQL ei tätä osaa. Eli kun arvoja syötetään tietokantaan, pitää olla tarkkana että menee oikean tyyppinen arvo sisään, sillä testatessa ei välttämättä huomaa jos on väärä tyyppi.

## Koodista

- Koodi sisältää vähän copy-pastea. Enimmäkseen sellaisissa tapauksissa, kun samalle sivulle on GET ja POST metodit. Tällöin GET:issä ladataan sivu ja sen jälkeen esim. POST:issa lähetetään jokin lomake. Jos lomake ei ole oikein validoitu, tarvitsee sivu ladata uudestaan, jolloin käytännössä pitää tehdä samat asiat kuin GET:issä.
- Kontrolleriluokka `foods/views.py` on aika suuri. En tiedä olisiko sitä kannattanut jakaa osiin. Toisaalta nyt ruokaan liittyvät asiat ovat kaikki samassa luokassa ja sen pilkkominen olisi tehnyt rakenteesta sekavamman.

## Tietoturvasta

- Kaikki SQL-kyselyt tehdään SQLAlchemyn tai queryjen avulla, jolloin SQL-injektioille ei jää mahdollisuutta.
- Salasanat hashataan, niitä ei pysty lukemaan tietokannasta suoraan.