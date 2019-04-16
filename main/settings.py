import os

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

LOL_URL = {
    'VERSION': 'https://ddragon.leagueoflegends.com/api/versions.json',
    'PROFILE_ICON': 'http://ddragon.leagueoflegends.com/cdn/%s/img/profileicon/',
    'STATIC_CHAMPION_DATA': 'http://ddragon.leagueoflegends.com/cdn/%s/data/ko_KR/champion.json'
}

LOL_API = {
    'GET_SUMMONER_BY_NAME': 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s',
    'GET_CHAMPION_MASTERIES': 'https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/%s'
}