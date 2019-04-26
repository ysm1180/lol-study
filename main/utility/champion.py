import json
import os

import requests

from main.settings import LOL_URL, PROJECT_PATH
from main.utility.api import get_lol_last_version

champions = {}


def make_json_file(data, path):
    with open(path, 'w+') as output:
        json.dump(data, output)


def load_champion_info(champion_id):
    version = get_lol_last_version()
    data_folder_path = os.path.join(PROJECT_PATH, 'data')
    version_path = os.path.join(data_folder_path, version)
    champion_data_path = os.path.join(version_path, champion_id + '.json')

    if not os.path.exists(champion_data_path):
        raise FileNotFoundError('the %s champion data does not exist.' %
                                champion_id)

    if champion_id in champions.keys():
        return champions[champion_id]

    with open(champion_data_path) as json_file:
        json_data = json.load(json_file)

    champions[champion_id] = json_data['data'][champion_id]
    return champions[champion_id]
