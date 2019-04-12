# -*- coding:utf-8 -*-

from django.shortcuts import render, render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Summoner
from .forms import SummonerSearchForm

from .utility.api import get_summoner_data_by_api


def index(request):
    return render(request, 'main/index.html')


def get_summoner_data_by_name(name):
    summoner_model = None
    try:
        summoner_model = Summoner.objects.get(pk=name)
    except Summoner.DoesNotExist:
        response = get_summoner_data_by_api(name)
        if response.status_code == 404:
            return None

        summoner_data = response.json()
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

    summonerClientData = summoner_model.get_client_data()
    championMasteries = summoner_model
    return render(request, 'main/summoner.html', {
        'summoner_data': summonerClientData,
    })
