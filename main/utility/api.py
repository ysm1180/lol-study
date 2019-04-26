from urllib.parse import quote

import redis
import requests
from django.conf import settings

from main.settings import LOL_API, LOL_URL
from main.utility.redis_client import REDIS_CONNECTION_POOL

def get_lol_last_version():
    r = redis.Redis(connection_pool=REDIS_CONNECTION_POOL)
    version = r.get('VERSION')
    if version is None:
        response = requests.get(LOL_URL['VERSION'])
        version = None
        if response.status_code == 200:
            versionData = response.json()
            version = versionData[0]
            r.set('VERSION', version.encode('utf-8'), 86400)

        if version is None:
            raise ValueError('version data does not exist.')
    else:
        version = version.decode('utf-8')
    
    return version


def call_lol_api(url, additional_params={}):
    params = {'api_key': settings.LOL_API_KEY}
    params.update(additional_params)
    response = requests.get(url, params=params)
    return response


def call_summoner_api_by_account_id(account_id):
    url = (LOL_API['GET_SUMMONER_BY_ACCOUNT_ID'] % quote(account_id))
    response = call_lol_api(url)
    if response.status_code == 404:
        return None

    return response.json()


def call_summoner_api_by_id(id):
    url = (LOL_API['GET_SUMMONER_BY_ID'] % quote(id))
    response = call_lol_api(url)
    if response.status_code == 404:
        return None

    return response.json()


def call_summoner_api_by_name(name):
    url = (LOL_API['GET_SUMMONER_BY_NAME'] % quote(name))
    response = call_lol_api(url)
    if response.status_code == 404:
        return None

    return response.json()


def call_champion_masteries_api_by_id(encrypted_id):
    url = (LOL_API['GET_CHAMPION_MASTERIES'] % quote(encrypted_id))
    response = call_lol_api(url)

    if response.status_code == 404:
        return None

    return response.json()


def call_match_list_api_by_account_id(account_id, start, end):
    url = (LOL_API['GET_MATCH_LIST_BY_ACCOUNT_ID'] % quote(account_id))
    response = call_lol_api(url, {'beginIndex': start, 'endIndex': end})

    if response.status_code == 404:
        return None

    return response.json()