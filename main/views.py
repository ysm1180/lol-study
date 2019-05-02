# -*- coding:utf-8 -*-

import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.urls import reverse

from .models import (Champion, ChampionMastery, Game, GameParticipant,
                     GameTeam, Match, Summoner, Spell)
from .utility.api import (call_champion_masteries_api_by_id,
                          call_match_info_api_by_game_id,
                          call_match_list_api_by_account_id,
                          call_summoner_api_by_account_id,
                          call_summoner_api_by_id, call_summoner_api_by_name)


def index(request):
    return render(request, 'main/index.html')


cache_champion_models = {}
cache_spell_models = {}


def get_game_infos(game_ids):
    games = Game.objects.filter(game_id__in=game_ids)
    result_game_ids = list(map(lambda game_model: game_model.game_id, games))
    invalid_game_ids = list(set(game_ids) - set(result_game_ids))

    game_models = []
    game_team_models = []
    game_participant_models = []
    if len(invalid_game_ids) > 0:
        for game_id in invalid_game_ids:
            game_data = call_match_info_api_by_game_id(game_id)
            game_model = Game(game_id=game_id,
                              season=game_data['seasonId'],
                              queue=game_data['queueId'],
                              platform=game_data['platformId'],
                              duration=game_data['gameDuration'],
                              type=game_data['gameType'],
                              mode=game_data['gameMode'],
                              map_id=game_data['mapId'])
            game_models.append(game_model)

            for team in game_data['teams']:
                is_win = False
                if team['win'] == 'Win':
                    is_win = True

                game_team_model = GameTeam(game=game_model,
                                           team_id=team['teamId'],
                                           is_win=is_win,
                                           tower_kills=team['towerKills'])
                game_team_models.append(game_team_model)

            participants_data = {}
            for participant in game_data['participants']:
                participants_data[participant['participantId']] = participant

            summoner_ids = []
            for identity in game_data['participantIdentities']:
                summoner_ids.append(identity['player']['summonerId'])
            summoner_list = Summoner.objects.filter(pk__in=summoner_ids)
            result_summoner_ids = list(
                map(lambda summoner_model: summoner_model.encrypted_id,
                    summoner_list))

            for identity in game_data['participantIdentities']:
                summoner_id = identity['player']['summonerId']
                summoner_name = identity['player']['summonerName']
                if summoner_id in result_summoner_ids:
                    summoner_name = [
                        summoner_model.name for summoner_model in summoner_list
                        if summoner_model.encrypted_id == summoner_id
                    ][0]

                participant_info = participants_data[identity['participantId']]

                try:
                    if participant_info[
                            'championId'] in cache_champion_models.keys():
                        champion_model = cache_champion_models[
                            participant_info['championId']]
                    else:
                        champion_model = Champion.objects.get(
                            pk=participant_info['championId'])
                        cache_champion_models[
                            participant_info['championId']] = champion_model
                except Champion.DoesNotExist:
                    raise

                try:
                    if participant_info['spell1Id'] in cache_spell_models.keys(
                    ):
                        spell_1_model = cache_spell_models[
                            participant_info['spell1Id']]
                    else:
                        spell_1_model = Spell.objects.get(
                            pk=participant_info['spell1Id'])
                        cache_spell_models[
                            participant_info['spell1Id']] = spell_1_model

                    if participant_info['spell2Id'] in cache_spell_models.keys(
                    ):
                        spell_2_model = cache_spell_models[
                            participant_info['spell2Id']]
                    else:
                        spell_2_model = Spell.objects.get(
                            pk=participant_info['spell2Id'])
                        cache_spell_models[
                            participant_info['spell2Id']] = spell_2_model
                except Spell.DoesNotExist:
                    raise

                game_participant_model = GameParticipant(
                    game=game_model,
                    participant_id=identity['participantId'],
                    summoner_id=summoner_id,
                    display_summoner_name=summoner_name,
                    team_id=participant_info['teamId'],
                    champion=champion_model,
                    spell_id_1=spell_1_model,
                    spell_id_2=spell_2_model,
                    item_0=participant_info['stats']['item0'],
                    item_1=participant_info['stats']['item1'],
                    item_2=participant_info['stats']['item2'],
                    item_3=participant_info['stats']['item3'],
                    item_4=participant_info['stats']['item4'],
                    item_5=participant_info['stats']['item5'],
                    item_6=participant_info['stats']['item6'],
                    kills=participant_info['stats']['kills'],
                    deaths=participant_info['stats']['deaths'],
                    assists=participant_info['stats']['assists'],
                    champ_level=participant_info['stats']['champLevel'])
                game_participant_models.append(game_participant_model)

        Game.objects.bulk_create(game_models)
        GameTeam.objects.bulk_create(game_team_models)
        GameParticipant.objects.bulk_create(game_participant_models)

    games = Game.objects.filter(game_id__in=game_ids)
    game_teams = GameTeam.objects.filter(game_id__in=game_ids)
    game_participants = GameParticipant.objects.filter(game_id__in=game_ids)

    return games, game_teams, game_participants


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

    return matches, list(map(lambda match: match.game_id, matches))


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

        if len(cache_spell_models) == 0:
            spells = Spell.objects.all()
            for spell in spells:
                cache_spell_models[spell.key] = spell

        champion_mastery_model_list = get_champion_mastery(
            summoner_model.encrypted_id)

        match_model_list, game_ids = get_champion_match_list(
            summoner_model.account_id, 0, 20)
        game_models, team_models, participant_models = get_game_infos(game_ids)

        games = {}
        for game_model in game_models:
            games[game_model.game_id] = {
                'game': game_model.get_client_data(),
                'teams': {},
                'participants': {},
            }

        for team_model in team_models:
            games[team_model.game_id]['teams'][
                team_model.team_id] = team_model.get_client_data()

        summoner_game_data = {}
        for participant_model in participant_models:
            games[participant_model.game_id]['participants'][
                participant_model.
                participant_id] = participant_model.get_client_data()

            if summoner_model.encrypted_id == participant_model.summoner_id:
                summoner_game = {'team': {}, 'participant': {}}
                summoner_game['team'] = games[
                    participant_model.game_id]['teams'][
                        participant_model.team_id]
                summoner_game[
                    'participant'] = participant_model.get_client_data()
                summoner_game_data[participant_model.game_id] = summoner_game

        matches = []
        for match_model in match_model_list:
            match_data = match_model.get_client_data()
            match_data.update({
                'game':
                games[match_data['game_id']],
                'summoner_game':
                summoner_game_data[match_data['game_id']],
            })
            matches.append(match_data)

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
