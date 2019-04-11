# -*- coding:utf-8 -*-

from django.shortcuts import render, render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Summoner
from .forms import SummonerSearchForm

from urllib.parse import quote
import requests


def index(request):
    return render(request, 'main/index.html')


def get_summoner_data_by_api(name):
    params = {
        'api_key': settings.LOL_API_KEY
    }
    url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    url = url + quote(name)
    response = requests.get(url, params=params)
    
    return response

def get_summoner(request):
    try:
        name = request.POST['summoner_name']
    except (KeyError):
        return render(request, 'main/index.html', {
            'error_message': "정상적인 접근이 아닙니다."
        })

    response = get_summoner_data_by_api(name)
    if response.status_code == 404:
        return render(request, 'main/index.html', {
            'error_message': "등록되지 않은 소환사입니다."
        })

    summonerData = response.json()
    summoner = Summoner(name=summonerData['name'],
                        encryptedId=summonerData['id'],
                        puuid=summonerData['puuid'],
                        accountId=summonerData['accountId'],
                        iconId=summonerData['profileIconId'],
                        level=summonerData['summonerLevel'])
    summoner.save()
    return HttpResponseRedirect(reverse('main:summoner', args=[name]))


def summoner(request, name):
    try:
        summoner = Summoner.objects.get(pk=name)
    except Summoner.DoesNotExist:
        response = get_summoner_data_by_api(name)
        if response.status_code == 404:
            return render(request, 'main/index.html', {
                'error_message': "등록되지 않은 소환사입니다."
            })

        summonerData = response.json()
        summoner = Summoner(name=summonerData['name'],
                            encryptedId=summonerData['id'],
                            puuid=summonerData['puuid'],
                            accountId=summonerData['accountId'],
                            iconId=summonerData['profileIconId'],
                            level=summonerData['summonerLevel'])
        summoner.save()

    summonerClientData = summoner.get_client_data()
    return render(request, 'main/summoner.html', {
        'summoner_data': summonerClientData,
    })
