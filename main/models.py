import requests
from django.db import models
from main.settings import LOL_URL, PROJECT_PATH
from main.utility.api import get_lol_last_version


class Summoner(models.Model):
    # https://developer.riotgames.com/api-methods/#summoner-v4/GET_getBySummonerName

    name = models.CharField(max_length=20, primary_key=True)
    encrypted_id = models.CharField(max_length=63, unique=True)
    puuid = models.CharField(max_length=78)
    account_id = models.CharField(max_length=56)
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
            'icon_url': (LOL_URL['PROFILE_ICON'] % latest_version) +
            str(self.icon_id) + '.png'
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
        # create unique index
        unique_together = (('summoner', 'champion'), )
