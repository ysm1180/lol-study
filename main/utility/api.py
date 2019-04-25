from urllib.parse import quote
from django.conf import settings

import requests

from main.settings import LOL_API, LOL_URL


def get_lol_last_version():
    # from main.models import Version

    # versions = Version.objects.order_by('-id')
    # if len(versions) == 0:
    #     response = requests.get(LOL_URL['VERSION'])
    #     latestVersion = None
    #     if response.status_code == 200:
    #         versionData = response.json()
    #         latestVersion = versionData[0]

    #     if latestVersion is None:
    #         raise ValueError('version is None')

    #     Version(version=latestVersion).save()

    # else:
    #     latestVersion = versions[0].version

    # return latestVersion

    # TODO: save to db and improve to speed up.
    return "9.8.1"


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