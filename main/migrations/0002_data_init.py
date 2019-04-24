# -*- coding: utf-8 -*-

from django.conf import settings
import requests
import os
import json

from main.utility.api import get_lol_last_version
from main.settings import LOL_URL, PROJECT_PATH
from django.db import migrations, models


def make_static_champion_data(data, path):
    with open(path, 'w+') as output:
        json.dump(data, output)


def load_champion_info(apps, schema_editor):
    static_champion_data_path = os.path.join(
        PROJECT_PATH, 'static/champion_KR.json')
    if not os.path.exists(static_champion_data_path):
        version = get_lol_last_version()
        response = requests.get((LOL_URL['STATIC_CHAMPION_DATA'] % version))
        if response.status_code == 200:
            make_static_champion_data(response.json(), static_champion_data_path)
    else:
        with open(static_champion_data_path) as json_file:
            json_data = json.load(json_file)

    Champion = apps.get_model('main', 'Champion')
    for key, value in json_data['data'].items():
        try:
            champion = Champion.objects.get(pk=int(value['key']))
        except Champion.DoesNotExist:
            champion_model = Champion(key=int(value['key']), id=key)
            champion_model.save()


class Migration(migrations.Migration):
    dependencies=[
        ('main', '0001_initial'),
    ]

    operations=[
        migrations.RunPython(load_champion_info)
    ]
