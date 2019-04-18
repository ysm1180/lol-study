from django.db import models
import requests

from .settings import LOL_URL
from .utility.api import get_lol_last_version


class Summoner(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    encryptedId = models.CharField(max_length=63)
    puuid = models.CharField(max_length=78)
    accountId = models.CharField(max_length=56)
    level = models.IntegerField(default=0)
    iconId = models.IntegerField(default=0)

    class Meta:
        app_label = 'main'

    def get_client_data(self):
        latestVersion = get_lol_last_version()

        return {
            'name': self.name,
            'level': self.level,
            'icon_url': (LOL_URL['PROFILE_ICON'] % latestVersion) + str(self.iconId) + '.png'
        }


class Champion(models.Model):
    key = models.IntegerField(default=0, primary_key=True)
    id = models.CharField(max_length=32)

    class Meta:
        app_label = 'main'
