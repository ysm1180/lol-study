from django.db import models
from django.conf import settings
import requests

class Summoner(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    encryptedId = models.CharField(max_length=63)
    puuid = models.CharField(max_length=78)
    accountId = models.CharField(max_length=56)
    level = models.IntegerField(default=0)
    iconId = models.IntegerField(default=0)

    def get_client_data(self):
        response = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
        latestVersion = '9.7.1'
        if response.status_code == 200:
            versionData = response.json()
            latestVersion = versionData[0]
        
        return {
            'name': self.name,
            'level': self.level,
            'icon_url': (settings.LOL_PROFILE_ICON_URL % latestVersion) + str(self.iconId) + '.png'
        }
