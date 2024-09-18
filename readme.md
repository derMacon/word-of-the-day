# Word of the day

## Description
This online dictionary leverages the api of [dict.cc](https://www.dict.cc/) to translate a given input word. The webapp then saves this request to a flash card for the user to learn later on. The flash card app in use is currently anki (see their [website](https://apps.ankiweb.net/)). Anki provides a mobile client as well as a webinterface which the user can interact with and learn previous requested translations.

The webapp also provides the possiblity to select other options other than the default translation for the generated flashcards.


## Usage
1. enter anki web credentials in order to sync generated flash cards with your anki account
2. select the source and target language for the translation (if both are equal we'll simply return a definition of the input word)
3. type in the word which should be translated
4. Optional: select a word which should be generated to serve as a flashcard in anki
5. learn stack in anki [web](https://ankiweb.net/about) or [client](https://apps.ankiweb.net/)

### Screenshots
1. Anki Login
---
![anki-login](_other/media/readme/wotd_login.png)
![anki-login](_other/media/readme/wotd-basic-input_with-login.png)
![anki-login](_other/media/readme/wotd-basic-input_without-login.png)
![anki-login](_other/media/readme/wotd-basic-input_selection.png)

2. Select Languages
---

3. Search Query
---

4. Optional Word Select
---

5. Learn in Anki Web
---


## Technology Used
- TODO

## Miscellaneous

### Credits
- Used [google font](https://fonts.google.com/specimen/Gluten?preview.text=Not%20Logged%20In%0A&preview.size=93&classification=Handwriting)


## Useful Commands

### Development
```bash
psql -d wotd_db -U admin
psql -d wotd_db -U admin -a -f /docker-entrypoint-initdb.d/init.sql
```

```sql
DROP SCHEMA public CASCADE; CREATE SCHEMA public;
```

## TODO
- Delete anki api since anki connect works better


## Credits
- [Logo](https://icon-icons.com/de/symbol/cloud-download/178873)
- [fallback deck](https://github.com/giniedp/media_education/blob/master/drehbuch/doc/resources/vocabulary/more/Vokabellisten_Englisch/Deutsch%20-%20Englisch%20Umfangreicher%20Wortschatz%20%5B18000%5D.csv)
