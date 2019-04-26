# LOL TOOL

LOL tool is for django study project.

## Getting started
To install the packages to test the project, simply use pip:
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
To migragte database and save default static data, run `python manage.py migrate`.

```bash
$ python manage.py migrate 
```



## Celery & Redis
Redis is required to use Celery. The redis connection information is in `lolsite/settings.py`.

Default setting is localhost:6379.
```python
# REDIS related settings
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
```

The project has a daily schedule for updating champion infomation.
In `lolsite/celery.py`, you can modify the schedule.
```python
app.conf.beat_schedule = {
    'update-champion-info-every-day': {
        'task': 'main.tasks.update_champion_info',
        'schedule': crontab(minute=0, hour=0),
        'args': (),
    },
}
```

To start the celery worker:
```bash
$ celery -A lolsite worker -l info
```

To start the celery schedule service:
```bash
$ celery -A lolsite beat
```


## Run
```
$ python manage.py runserver [:port]
```