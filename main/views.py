# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.urls import reverse

from main.models import Champion, ChampionMastery, Match, Summoner
from main.utility.api import (call_champion_masteries_api_by_id,
                              call_match_list_api_by_account_id,
                              call_summoner_api_by_account_id,
                              call_summoner_api_by_id,
                              call_summoner_api_by_name)


def index(request):
    return render(request, 'main/index.html')


cache_champion_models = {}

def get_champion_match_list(account_id, start, end):
    matches = Match.objects.filter(
        summoner_id=account_id).order_by('-timestamp')[start:end]
    if len(matches) == 0:
        matches = []

        match_list = call_match_list_api_by_account_id(account_id, 0, 20)
        summoner_model = get_summoner_data_by_account_id(account_id)
        for match in match_list['matches']:
            try:
                if match['champion'] in cache_champion_models.keys():
                    champion_model = cache_champion_models[match['champion']]
                else:
                    champion_model = Champion.objects.get(pk=match['champion'])
                    cache_champion_models[match['champion']] = champion_model
            except Champion.DoesNotExist:
                raise

            match_model = Match(summoner=summoner_model,
                                champion=champion_model,
                                game_id=match['gameId'],
                                platform=match['platformId'],
                                queue=match['queue'],
                                season=match['season'],
                                role=match['role'],
                                lane=match['lane'],
                                timestamp=match['timestamp'])

            matches.append(match_model)
        Match.objects.bulk_create(matches)

    return matches


def get_champion_mastery(id):
    champion_masteries = ChampionMastery.objects.filter(summoner_id=id)
    if len(champion_masteries) == 0:
        champion_masteries = []
        champion_mastery_data = call_champion_masteries_api_by_id(id)
        summoner_model = get_summoner_data_by_id(id)
        for champoin_mastery in champion_mastery_data:
            try:
                if champoin_mastery[
                        'championId'] in cache_champion_models.keys():
                    champion_model = cache_champion_models[
                        champoin_mastery['championId']]
                else:
                    champion_model = Champion.objects.get(
                        pk=champoin_mastery['championId'])
                    cache_champion_models[
                        champoin_mastery['championId']] = champion_model

            except Champion.DoesNotExist:
                continue

            champion_mastery_model = ChampionMastery(
                summoner=summoner_model,
                champion=champion_model,
                level=champoin_mastery['championLevel'],
                points=champoin_mastery['championPoints'],
                last_play_time=champoin_mastery['lastPlayTime'],
                tokens_earned=champoin_mastery['tokensEarned'])

            champion_masteries.append(champion_mastery_model)
        ChampionMastery.objects.bulk_create(champion_masteries)

    return champion_masteries


def get_summoner_data_by_account_id(account_id):
    try:
        summoner_model = Summoner.objects.get(account_id=account_id)
    except Summoner.DoesNotExist:
        summoner_data = call_summoner_api_by_account_id(account_id)
        summoner_model = Summoner(name=summoner_data['name'],
                                  encrypted_id=summoner_data['id'],
                                  puuid=summoner_data['puuid'],
                                  account_id=summoner_data['accountId'],
                                  icon_id=summoner_data['profileIconId'],
                                  level=summoner_data['summonerLevel'])
        summoner_model.save()

    return summoner_model


def get_summoner_data_by_id(encrypted_id):
    try:
        summoner_model = Summoner.objects.get(pk=encrypted_id)
    except Summoner.DoesNotExist:
        summoner_data = call_summoner_api_by_id(encrypted_id)
        summoner_model = Summoner(name=summoner_data['name'],
                                  encrypted_id=summoner_data['id'],
                                  puuid=summoner_data['puuid'],
                                  account_id=summoner_data['accountId'],
                                  icon_id=summoner_data['profileIconId'],
                                  level=summoner_data['summonerLevel'])
        summoner_model.save()

    return summoner_model


def get_summoner_data_by_name(name):
    try:
        summoner_model = Summoner.objects.get(name=name)
    except Summoner.DoesNotExist:
        summoner_data = call_summoner_api_by_name(name)
        summoner_model = Summoner(name=summoner_data['name'],
                                  encrypted_id=summoner_data['id'],
                                  puuid=summoner_data['puuid'],
                                  account_id=summoner_data['accountId'],
                                  icon_id=summoner_data['profileIconId'],
                                  level=summoner_data['summonerLevel'])
        summoner_model.save()

    return summoner_model


def get_summoner(request):
    try:
        name = request.POST['summoner_name']
    except (KeyError):
        return render(request, 'main/index.html',
                      {'error_message': "정상적인 접근이 아닙니다."})

    try:
    summoner = get_summoner_data_by_name(name)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            render(request, 'main/index.html',
                      {'error_message': "등록되지 않은 소환사입니다."})
        else:
            render(request, 'main/index.html', {'error_message': e.msg})

    return HttpResponseRedirect(reverse('main:summoner', args=[name]))


def summoner(request, name):
    try:
    summoner_model = get_summoner_data_by_name(name)

    if len(cache_champion_models) == 0:
        champions = Champion.objects.all()
        for champion in champions:
            cache_champion_models[champion.key] = champion

    champion_mastery_model_list = get_champion_mastery(
        summoner_model.encrypted_id)
    if champion_mastery_model_list is None:
        return render(request, 'main/index.html',
                      {'error_message': "정보를 불러오는데에 문제가 생겼습니다."})

    match_model_list = get_champion_match_list(summoner_model.account_id, 0,
                                               20)

    matches = []
    for match_model in match_model_list:
        matches.append(match_model.get_client_data())

    summoner_client_data = summoner_model.get_client_data()
    return render(request, 'main/summoner.html', {
        'summoner_data': summoner_client_data,
        'match_list': matches,
    })

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return render(request, 'main/index.html',
                          {'error_message': "등록되지 않은 소환사입니다."})
        else:
            msg = e.response.json()['status']['message']
            return render(request, 'main/index.html', {'error_message': msg})
