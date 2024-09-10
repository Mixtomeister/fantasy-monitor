# Generated by Django 5.1 on 2024-09-05 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_api_id', models.IntegerField()),
                ('name', models.CharField(max_length=64)),
                ('short_name', models.CharField(max_length=32)),
                ('slug', models.SlugField(max_length=32)),
                ('last_season_points', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_api_id', models.IntegerField()),
                ('name', models.CharField(max_length=32)),
                ('short_name', models.CharField(max_length=3)),
                ('slug', models.SlugField(max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(choices=[(1, 'Goalkeeper'), (2, 'Defender'), (3, 'Midfielder'), (4, 'Striker'), (5, 'Manager')])),
                ('date', models.DateField()),
                ('market_value', models.IntegerField()),
                ('status', models.CharField(choices=[('suspended', 'Suspended'), ('injured', 'Injured'), ('ok', 'Available'), ('doubtful', 'Doubtful'), ('unknown', 'Unknown')], max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fantasy.player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='fantasy.team')),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='PlayerPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(choices=[(1, 'Goalkeeper'), (2, 'Defender'), (3, 'Midfielder'), (4, 'Striker'), (5, 'Manager')])),
                ('round', models.IntegerField()),
                ('points', models.IntegerField()),
                ('ideal_xi', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fantasy.player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='fantasy.team')),
            ],
        ),
    ]