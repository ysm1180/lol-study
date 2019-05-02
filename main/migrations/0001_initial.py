# Generated by Django 2.2 on 2019-04-26 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('key', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('key', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('name', models.CharField(db_index=True, max_length=64, unique=True)),
                ('encrypted_id', models.CharField(db_index=True, max_length=63, primary_key=True, serialize=False, unique=True)),
                ('account_id', models.CharField(db_index=True, max_length=56, unique=True)),
                ('puuid', models.CharField(max_length=78)),
                ('level', models.IntegerField(default=0)),
                ('icon_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.BigIntegerField(default=0)),
                ('queue', models.IntegerField(default=0)),
                ('timestamp', models.BigIntegerField(db_index=True, default=0)),
                ('season', models.IntegerField(default=0)),
                ('platform', models.CharField(max_length=2)),
                ('role', models.CharField(max_length=16)),
                ('lane', models.CharField(max_length=16)),
                ('champion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Champion')),
                ('summoner', models.ForeignKey(db_column='account_id', on_delete=django.db.models.deletion.CASCADE, to='main.Summoner', to_field='account_id')),
            ],
            options={
                'unique_together': {('summoner', 'game_id')},
            },
        ),
        migrations.CreateModel(
            name='ChampionMastery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('tokens_earned', models.IntegerField(default=0)),
                ('last_play_time', models.BigIntegerField(default=0)),
                ('champion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Champion')),
                ('summoner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Summoner')),
            ],
            options={
                'unique_together': {('summoner', 'champion')},
            },
        ),
    ]
