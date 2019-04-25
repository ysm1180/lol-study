# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import migrations, models

from main.utility.champion import migrate_champion_info


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [migrations.RunPython(migrate_champion_info)]
