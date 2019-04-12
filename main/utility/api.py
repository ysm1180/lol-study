
from urllib.parse import quote
from django.conf import settings

import requests

from main.constants import LOL_API

def call_lol_api(url):
    params = {
        'api_key': settings.LOL_API_KEY
    }
    response = requests.get(url, params=params)
    return response

def get_summoner_data_by_api(name):
    url = (LOL_API['GET_SUMMONER_BY_NAME'] % quote(name))
    response = call_lol_api(url)
    
    return response

def get_champion_masteries(encryptedId):
    url = (LOL_API['GET_CHAMPION_MASTERIES'] % quote(encryptedId))
    response = call_lol_api(url)
    
    return response