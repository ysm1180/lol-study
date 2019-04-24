# -*- coding:utf-8 -*-

from django.shortcuts import render, render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Summoner, Champion, ChampionMastery

from .utility.api import get_summoner_data_by_api, get_champion_masteries_data_by_api


def index(request):
    return render(request, 'main/index.html')


def get_champion_mastery(id):

    champion_mastery_model = ChampionMastery.objects.filter(summoner=id)
    if len(champion_mastery_model) == 0:
        champion_mastery_data = get_champion_masteries_data_by_api(id)
        if champion_mastery_data is None:
            return None

        for champoin_mastery in champion_mastery_data:
            
            champion_mastery_model = ChampionMastery(summoner=,
                                                                    champion=champoin_mastery['championId'],
                                                                    level=champoin_mastery['championLevel'],
                                                                    point=champoin_mastery['championPoints'],
                                                                    lastPlayTime=champoin_mastery['lastPlayTime'],
                                                                    tokenEarned=champoin_mastery['tokensEarned'])

            champion_mastery_model.save()

    return champion_mastery_model


def get_summoner_data_by_name(name):
    try:
        summoner_model = Summoner.objects.get(pk=name)
    except Summoner.DoesNotExist:
        summoner_data = get_summoner_data_by_api(name)
        if summoner_data is None:
            return None

        summoner_model = Summoner(name=summoner_data['name'],
                                  encryptedId=summoner_data['id'],
                                  puuid=summoner_data['puuid'],
                                  accountId=summoner_data['accountId'],
                                  iconId=summoner_data['profileIconId'],
                                  level=summoner_data['summonerLevel'])
        summoner_model.save()

    return summoner_model


def get_summoner(request):
    try:
        name = request.POST['summoner_name']
    except (KeyError):
        return render(request, 'main/index.html', {
            'error_message': "정상적인 접근이 아닙니다."
        })

    summoner = get_summoner_data_by_name(name)
    if summoner is None:
        return render(request, 'main/index.html', {
            'error_message': "등록되지 않은 소환사입니다."
        })

    return HttpResponseRedirect(reverse('main:summoner', args=[name]))


def summoner(request, name):
    summoner_model = get_summoner_data_by_name(name)
    if summoner_model is None:
        return render(request, 'main/index.html', {
            'error_message': "등록되지 않은 소환사입니다."
        })

    championMasteries = get_champion_mastery(summoner_model.encryptedId)
    if championMasteries is None:
        return render(request, 'main/index.html', {
            'error_message': "정보를 불러오는데에 문제가 생겼습니다."
        })

    summonerClientData = summoner_model.get_client_data()
    return render(request, 'main/summoner.html', {
        'summoner_data': summonerClientData,
    })
