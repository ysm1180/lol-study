# LOL TOOL

LOL tool is for django study.

## Getting started
The project use django, requests. To install these packages, simply use pip:
```
pip install -r requirements.txt
```

To deploy this site, you must get LOL Develoment API key in https://developer.riotgames.com/.
After you get the api key, modify `LOL_API_KEY` in `secrets.json`

In addition, the project has django secert key in `secrets.json` not `lolsite/settings.py`. 
you can find `SECRET_KEY` in `secrets.json` and put your django secret key.

```json
{
    "SECRET_KEY": "HERE YOUR SECRET KEY",
    "LOL_API_KEY": "HERE YOUR API KEY"
}
```

## Database Migration

Default database in the project is sqlite3.
To migragte database, run `makemigrations` and `migrate`.

```bash
$ python manage.py makemigrations main
$ python manage.py migrate 
```

## Development
```
$ python manage.py runserver [:port]
```