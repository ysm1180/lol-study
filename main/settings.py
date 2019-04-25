import os

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

BASE_API_URL = 'https://kr.api.riotgames.com'

LOL_URL = {
    'VERSION':
    'https://ddragon.leagueoflegends.com/api/versions.json',
    'PROFILE_ICON':
    'http://ddragon.leagueoflegends.com/cdn/%s/img/profileicon/%s.png',
    'STATIC_CHAMPION_ALL_DATA':
    'http://ddragon.leagueoflegends.com/cdn/%s/data/ko_KR/champion.json',
    'STATIC_CHAMPION_DATA':
    'http://ddragon.leagueoflegends.com/cdn/%s/data/ko_KR/champion/%s.json',
    'CHAMPION_ICON':
    'http://ddragon.leagueoflegends.com/cdn/%s/img/champion/%s.png',
}

LOL_API = {
    'GET_SUMMONER_BY_ACCOUNT_ID':
    BASE_API_URL + '/lol/summoner/v4/summoners/by-account/%s',
    'GET_SUMMONER_BY_ID':
    BASE_API_URL + '/lol/summoner/v4/summoners/%s',
    'GET_SUMMONER_BY_NAME':
    BASE_API_URL + '/lol/summoner/v4/summoners/by-name/%s',
    'GET_CHAMPION_MASTERIES':
    BASE_API_URL +
    '/lol/champion-mastery/v4/champion-masteries/by-summoner/%s',
    'GET_MATCH_LIST_BY_ACCOUNT_ID':
    BASE_API_URL + '/lol/match/v4/matchlists/by-account/%s',
}