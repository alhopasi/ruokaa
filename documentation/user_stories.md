# Käyttötapauksia

- Tässä on joitakin käyttötapauksia. Ohjelma on kuitenkin paljon laajempi, kuin mitä näistä selviää.

## Kirjautumaton käyttäjä

### Selaa ruokia
- Käyttäjä pystyy selailemaan kaikkia ruokia.
- SQL kysely: `SELECT * FROM Food;`
- Lisäksi lasketaan tykkäysten määrät jokaiselle ruoalle: `SELECT * FROM Like WHERE Like.food_id = <food_id>;`, missä `<food_id>` on ruoan id.

### Luo uusi tili
- Käyttäjä pystyy luomaan uuden tilin.
- Uutta tiliä luodessa tarkastetaan löytyykö jo samalla käyttäjänimellä olevaa tiliä: `SELECT * FROM Account WHERE Account.username = <tilin_nimi>;`
- Uuden tilin luominen: `INSERT INTO Account (id, date_created, date_modified, name, username, password, role_id) VALUES (<id>, <created>, <modified>, <name>, <username>, <password>, <role_id>);`

### Kirjaudu sisään
- Käyttäjä pystyy kirjautumaan sisään.
- Kirjautuessa tarkastetaan löytyykö tiliä jolla yritetään kirjautua sisään: `SELECT * FROM Account WHERE username = <username> AND password = <password>;`

## Kirjautunut käyttäjä

### Lisää uusi ruoka
- Käyttäjä pystyy lisäämään uuden ruoan.
- `INSERT INTO Food (id, date_created, date_modified, name, preparing_time, recipe, type_id, account_id) VALUES (<id>, <created>, <modified>, <name>, <preparing_time>, <recipe>, <type_id>, <account_id>);`
- Ruokaa lisättäessä katsotaan löytyykö ruoka-aineet jo tietokannasta: `SELECT * FROM Ingredient WHERE Ingredient.name = <ingredient_name>;`
- Jos ei, luodaan uusi: `INSERT INTO Ingredient (id, date_created, date_modified, name) VALUES(<id>, <created>, <modified>, <name>);`
- Ja liitetään ruoka-aineet ruokiin liitostaululla: `INSERT INTO Ingredients (food_id, ingredient_id) VALUES (<food_id>, <ingredient_id>);`

### Muokkaa ruokaa
- Käyttäjä pystyy muokkaamaan omaa ruokaansa.
- `UPDATE Food SET name = <name>, preparing_time = <preparing_time>, recipe = <recipe>, type_id = <type_id> WHERE id = <food_id>;`
- Lisäksi poistetaan tai lisätään ruoka-aineet liitostauluun jos aineita on muutettu: `DELETE FROM Ingredients WHERE food_id = <food_id> AND ingredient_id = <ingredient_id>;`. Lisäykset käsiteltiin jo aiemmassa esimerkissä.

## Pääkäyttäjä (admin)
- Pääkäyttäjä pystyy tekemään kaikkea mitä tavallinenkin käyttäjä.
- Lisäksi pääkäyttäjä pystyy muuttamaan tai poistamaan muiden käyttäjien ruokia.

### Poista ruoka
- Käyttäjä pystyy poistamaan ruoan: `DELETE FROM Food WHERE food_id = <food_id>;`. Tätä ennen täytyy poistaa ruoka-aineet jotka kyseiseen ruokaan on liitetty: `DELETE FROM Ingredients WHERE food_id = <food_id>;`. Lisäksi tarkastetaan jos ruoka-aineita ei ole yhtään jäljellä, jolloin poistetaan ruoka-aine ruoka-aineiden taulusta: `SELECT * FROM Ingredients WHERE ingredient_id = <ingredient_id>;` sekä `DELETE FROM Ingredient WHERE id = <ingredient_id>;`