# LOL TOOL

LOL tool is for django study.

## Getting started
The project use Requests. To install Requests, simply use pip:
```
pip install requests
```


To deploy this site, you must get LOL Develoment API key in https://developer.riotgames.com/.

After you get the api key, modify `LOL_API_KEY` in `lolsite/settings.py`

```python
lolsite/settings.py

LOL_API_KEY = [HERE YOUR API KEY]
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
$ python manage.py runserver
```