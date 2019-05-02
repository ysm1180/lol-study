import json
import os

import requests

from lolsite.celery import app
from main.models import Champion
from main.settings import LOL_URL, PROJECT_PATH
from main.utility.api import get_lol_last_version
from main.utility.champion import make_json_file


@app.task
def update_champion_info():
    from main.models import Champion

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

    for key, value in json_data['data'].items():
        try:
            champion_model = Champion.objects.get(pk=int(value['key']))
        except Champion.DoesNotExist:
            champion_model = Champion(key=int(value['key']), id=key)
            champion_model.save()

        champion_data_path = os.path.join(version_path, str(value['key']) + '.json')
        if not os.path.exists(champion_data_path):
            response = requests.get(
                (LOL_URL['STATIC_CHAMPION_DATA'] % (version, key)))
            if response.status_code == 200:
                make_json_file(response.json(), champion_data_path)
