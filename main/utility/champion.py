import json
import os

import requests

from main.settings import LOL_URL, PROJECT_PATH
from main.utility.api import get_lol_last_version


def make_json_file(data, path):
    with open(path, 'w+') as output:
        json.dump(data, output)


def migrate_champion_info(apps, schema_editor):
    version = get_lol_last_version()
    version_path = os.path.join(PROJECT_PATH, 'static', version)
    all_data_path = os.path.join(version_path, 'champion_all.json')

    if not os.path.exists(version_path):
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

        champion_data_path = os.path.join(version_path, key + '.json')
        if not os.path.exists(champion_data_path):
            response = requests.get(
                (LOL_URL['STATIC_CHAMPION_DATA'] % (version, key)))
            if response.status_code == 200:
                make_json_file(response.json(), champion_data_path)


def update_champion_info():
    version = get_lol_last_version()
    version_path = os.path.join(PROJECT_PATH, 'static', version)
    all_data_path = os.path.join(version_path, 'champion_all.json')

    if not os.path.exists(version_path):
        os.mkdir(version_path)

    if not os.path.exists(all_data_path):
        response = requests.get(
            (LOL_URL['STATIC_CHAMPION_ALL_DATA'] % version))
        if response.status_code == 200:
            make_json_file(response.json(), all_data_path)

    with open(all_data_path) as json_file:
        json_data = json.load(json_file)

    for key, value in json_data['data'].items():
        try:
            champion_model = Champion.objects.get(pk=int(value['key']))
        except Champion.DoesNotExist:
            champion_model = Champion(key=int(value['key']), id=key)
            champion_model.save()

        champion_data_path = os.path.join(version_path, key + '.json')
        if not os.path.exists(champion_data_path):
            response = requests.get(
                (LOL_URL['STATIC_CHAMPION_DATA'] % (version, key)))
            if response.status_code == 200:
                make_json_file(response.json(), champion_data_path)


def load_champion_info(champion_id):
    version = get_lol_last_version()
    version_path = os.path.join(PROJECT_PATH, 'static', version)
    champion_data_path = os.path.join(version_path, champion_id + '.json')

    if not os.path.exists(champion_data_path):
        update_champion_info()

    if not os.path.exists(champion_data_path):
        raise FileNotFoundError('the %s champion data does not exist.' % champion_id)    

    with open(champion_data_path) as json_file:
        json_data = json.load(json_file)

    champion_info = json_data['data'][champion_id]
    return champion_info
