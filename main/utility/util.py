import json
import os

import requests

from main.settings import LOL_URL, PROJECT_PATH
from main.utility.api import get_lol_last_version

champions = {}


def make_json_file(data, path):
    with open(path, 'w+') as output:
        json.dump(data, output)


def load_champion_info(champion_key):
    version = get_lol_last_version()
    data_folder_path = os.path.join(PROJECT_PATH, 'data')
    version_path = os.path.join(data_folder_path, version)
    champion_data_path = os.path.join(version_path, str(champion_key) + '.json')

    if not os.path.exists(champion_data_path):
        raise FileNotFoundError('the %d champion data does not exist.' %
                                champion_key)

    if champion_key in champions.keys():
        return champions[champion_key]

    with open(champion_data_path) as json_file:
        json_data = json.load(json_file)

    key = list(json_data['data'].keys())[0]
    champions[champion_key] = json_data['data'][key]
    return champions[champion_key]
