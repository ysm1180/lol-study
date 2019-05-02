# -*- coding:utf-8 -*-

import math
import time
from datetime import datetime

import requests
from django.db import models

from main.settings import LOL_URL, PROJECT_PATH
from main.utility.api import get_lol_last_version
from main.utility.util import load_champion_info


class Champion(models.Model):
    key = models.IntegerField(default=0, primary_key=True)
    id = models.CharField(max_length=32)

    class Meta:
        app_label = 'main'


class Spell(models.Model):
    key = models.IntegerField(default=0, primary_key=True)
    id = models.CharField(max_length=32)

    class Meta:
        app_label = 'main'


class Summoner(models.Model):
    # https://developer.riotgames.com/api-methods/#summoner-v4/GET_getBySummonerName

    name = models.CharField(max_length=64, unique=True, db_index=True)
    encrypted_id = models.CharField(max_length=63,
                                    unique=True,
                                    db_index=True,
                                    primary_key=True)
    account_id = models.CharField(max_length=56, unique=True, db_index=True)
    puuid = models.CharField(max_length=78)
    level = models.IntegerField(default=0)
    icon_id = models.IntegerField(default=0)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'main'

    def get_client_data(self):
        latest_version = get_lol_last_version()

        return {
            'name':
            self.name,
            'level':
            self.level,
            'icon_url':
            (LOL_URL['PROFILE_ICON'] % (latest_version, str(self.icon_id))),
        }


class ChampionMastery(models.Model):
    # https://developer.riotgames.com/api-methods/#champion-mastery-v4

    summoner = models.ForeignKey(Summoner,
                                 to_field='encrypted_id',
                                 on_delete=models.CASCADE)
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    tokens_earned = models.IntegerField(default=0)
    last_play_time = models.BigIntegerField(default=0)

    class Meta:
        app_label = 'main'
        unique_together = (('summoner', 'champion'), )

    def get_client_data(self):
        champion_info = load_champion_info(self.champion_id)
        return {
            'level': self.level,
            'points': self.points,
            'last_play_time': self.last_play_time,
        }


class Match(models.Model):
    summoner = models.ForeignKey(Summoner,
                                 to_field='account_id',
                                 db_column='account_id',
                                 on_delete=models.CASCADE)
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    game_id = models.BigIntegerField(default=0)
    queue = models.IntegerField(default=0)
    timestamp = models.BigIntegerField(default=0, db_index=True)
    season = models.IntegerField(default=0)
    platform = models.CharField(max_length=2)
    role = models.CharField(max_length=16)
    lane = models.CharField(max_length=16)

    class Meta:
        app_label = 'main'
        unique_together = (('summoner', 'game_id'), )

    def get_client_data(self):
        version = get_lol_last_version()
        champion_info = load_champion_info(self.champion_id)

        second_diff = (int(round(time.time() * 1000)) - self.timestamp) / 1000
        diff_format = ''
        if second_diff < 60:
            diff_format = ('%d초 전' % second_diff)
        elif second_diff < 3600:
            diff_format = ('%d분 전' % math.ceil(second_diff / 60))
        elif second_diff < 86400:
            diff_format = ('%d시간 전' % math.ceil(second_diff / 3600))
        else:
            diff_format = ('%d일 전' % math.ceil(second_diff / 86400))

        queue_type = '?'
        if self.queue == 450:
            queue_type = '칼바람'
        elif self.queue == 420:
            queue_type = '솔랭'
        elif self.queue == 430:
            queue_type = '일반'
        elif self.queue == 440:
            queue_type = '자유랭'

        return {
            'game_id':
            self.game_id,
            'champion_name':
            champion_info['name'],
            'champion_icon_url':
            (LOL_URL['CHAMPION_ICON'] % (version, champion_info['id'])),
            'queue':
            queue_type,
            'time':
            datetime.fromtimestamp(self.timestamp / 1000).strftime(
                "%Y년 %m월 %d일 %p %I시 %M분".encode('unicode-escape').decode(
                )).encode().decode('unicode-escape'),
            'diff_time':
            diff_format,
            'role':
            self.role,
            'lane':
            self.lane,
        }


class Game(models.Model):
    game_id = models.BigIntegerField(primary_key=True)
    season = models.IntegerField(default=0)
    queue = models.IntegerField(default=0)
    platform = models.CharField(max_length=2)
    duration = models.BigIntegerField(default=0)
    type = models.CharField(max_length=32)
    mode = models.CharField(max_length=32)
    map_id = models.IntegerField(default=0)

    # participants = ArrayField(JSONField())

    class Meta:
        app_label = 'main'

    def get_client_data(self):
        duration_format = '%d분 %d초' % (math.floor(
            self.duration / 60), self.duration % 60)

        return {
            'id': self.game_id,
            'duration': duration_format,
        }


class GameTeam(models.Model):
    game = models.ForeignKey(Game,
                             to_field='game_id',
                             on_delete=models.CASCADE)
    team_id = models.IntegerField(default=0)
    is_win = models.BooleanField(default=False)
    tower_kills = models.IntegerField(default=0)

    class Meta:
        app_label = 'main'
        unique_together = (('game', 'team_id'), )

    def get_client_data(self):
        return {
            'game_id': self.game_id,
            'team_id': self.team_id,
            'is_win': self.is_win,
            'tower_kills': self.tower_kills,
        }


class GameParticipant(models.Model):
    game = models.ForeignKey(Game,
                             to_field='game_id',
                             on_delete=models.CASCADE)
    participant_id = models.IntegerField()
    summoner_id = models.CharField(max_length=63, db_index=True)
    display_summoner_name = models.CharField(max_length=64, db_index=True)
    team_id = models.IntegerField(default=0)
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    spell_id_1 = models.ForeignKey(Spell,
                                   related_name='spells_1',
                                   on_delete=models.CASCADE)
    spell_id_2 = models.ForeignKey(Spell,
                                   related_name='spells_2',
                                   on_delete=models.CASCADE)
    item_0 = models.IntegerField(default=0)
    item_1 = models.IntegerField(default=0)
    item_2 = models.IntegerField(default=0)
    item_3 = models.IntegerField(default=0)
    item_4 = models.IntegerField(default=0)
    item_5 = models.IntegerField(default=0)
    item_6 = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    champ_level = models.IntegerField(default=0)

    class Meta:
        app_label = 'main'
        unique_together = (('game', 'participant_id'), )

    def get_client_data(self):
        version = get_lol_last_version()
        champion_info = load_champion_info(self.champion_id)

        return {
            'game_id':
            self.game_id,
            'team_id':
            self.team_id,
            'summoner_name':
            self.display_summoner_name,
            'champion_name':
            champion_info['name'],
            'champion_icon_url':
            (LOL_URL['CHAMPION_ICON'] % (version, champion_info['id'])),
            'champion_level':
            self.champ_level,
            'spell_icon_url':
            (LOL_URL['SPELL_ICON'] % (version, champion_info['id'])),
            'item_0_icon_url': (LOL_URL['ITEM_ICON'] % (version, self.item_0)),
            'item_1_icon_url': (LOL_URL['ITEM_ICON'] % (version, self.item_1)),
            'item_2_icon_url': (LOL_URL['ITEM_ICON'] % (version, self.item_2)),
            'item_3_icon_url': (LOL_URL['ITEM_ICON'] % (version, self.item_3)),
            'item_4_icon_url': (LOL_URL['ITEM_ICON'] % (version, self.item_4)),
            'item_5_icon_url': (LOL_URL['ITEM_ICON'] % (version, self.item_5)),
            'item_6_icon_url': (LOL_URL['ITEM_ICON'] % (version, self.item_6)),
            'kills':
            self.kills,
            'deaths':
            self.deaths,
            'assists':
            self.assists,
        }
