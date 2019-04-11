from django import forms

class SummonerSearchForm(forms.Form):
    summoner_name = forms.CharField()
    