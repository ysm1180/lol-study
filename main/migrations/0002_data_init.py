# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import migrations, models

import json
import os

import requests

from main.models import Champion
from main.settings import LOL_URL, PROJECT_PATH
from main.utility.api import get_lol_last_version
from main.utility.util import make_json_file


def migrate_champion_info(apps, schema_editor):
    version = get_lol_last_version()
    data_folder_path = os.path.join(PROJECT_PATH, 'data')
    version_path = os.path.join(data_folder_path, version)
    all_data_path = os.path.join(version_path, 'champion_all.json')

    if not os.path.exists(version_path):
        if not os.path.exists(data_folder_path):
            os.mkdir(data_folder_path)
        os.mkdir(version_path)

    if not os.path.exists(all_data_path):
        response = requests.get(
            (LOL_URL['STATIC_CHAMPION_ALL_DATA'] % version))
        if response.status_code == 200:
            make_json_file(response.json(), all_data_path)

    with open(all_data_path) as json_file:
        json_data = json.load(json_file)

    ChampionModel = apps.get_model('main', 'Champion')
    for key, value in json_data['data'].items():
        try:
            champion_model = ChampionModel.objects.get(pk=int(value['key']))
        except ChampionModel.DoesNotExist:
            champion_model = ChampionModel(key=int(value['key']), id=key)
            champion_model.save()

        champion_data_path = os.path.join(version_path, str(value['key']) + '.json')
        if not os.path.exists(champion_data_path):
            response = requests.get(
                (LOL_URL['STATIC_CHAMPION_DATA'] % (version, key)))
            if response.status_code == 200:
                make_json_file(response.json(), champion_data_path)


def migrate_spell_info(apps, schema_editor):
    version = get_lol_last_version()
    data_folder_path = os.path.join(PROJECT_PATH, 'data')
    version_path = os.path.join(data_folder_path, version)
    all_data_path = os.path.join(version_path, 'spell_all.json')

    if not os.path.exists(version_path):
        if not os.path.exists(data_folder_path):
            os.mkdir(data_folder_path)
        os.mkdir(version_path)

    if not os.path.exists(all_data_path):
        response = requests.get((LOL_URL['STATIC_SPELL_ALL_DATA'] % version))
        if response.status_code == 200:
            make_json_file(response.json(), all_data_path)

    with open(all_data_path) as json_file:
        json_data = json.load(json_file)

    SpellModel = apps.get_model('main', 'Spell')
    for key, value in json_data['data'].items():
        try:
            spell_model = SpellModel.objects.get(pk=int(value['key']))
        except SpellModel.DoesNotExist:
            spell_model = SpellModel(key=int(value['key']), id=key)
            spell_model.save()


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_champion_info),
        migrations.RunPython(migrate_spell_info),
    ]
