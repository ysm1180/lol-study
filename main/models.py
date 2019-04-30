import time

import requests
from django.db import models

from main.settings import LOL_URL, PROJECT_PATH
from main.utility.api import get_lol_last_version
from main.utility.champion import load_champion_info


class Summoner(models.Model):
    # https://developer.riotgames.com/api-methods/#summoner-v4/GET_getBySummonerName

    name = models.CharField(max_length=20, primary_key=True)
    encrypted_id = models.CharField(max_length=63, unique=True, db_index=True)
    account_id = models.CharField(max_length=56, unique=True, db_index=True)
    puuid = models.CharField(max_length=78)
    level = models.IntegerField(default=0)
    icon_id = models.IntegerField(default=0)

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


class Champion(models.Model):
    key = models.IntegerField(default=0, primary_key=True)
    id = models.CharField(max_length=32)

    class Meta:
        app_label = 'main'

    def get_data(self):
        pass


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
        champion_info = load_champion_info(self.champion.id)
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
        champion_info = load_champion_info(self.champion.id)

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
