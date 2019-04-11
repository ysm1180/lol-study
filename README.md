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

```bash
$ python manage.py makemigrations main

Migrations for 'main':
  main\migrations\0001_initial.py
    - Create model Summoner

$ python manage.py migrate 

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, main, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying main.0001_initial... OK
  Applying sessions.0001_initial... OK
```

## Development
```
$ python manage.py runserver
```