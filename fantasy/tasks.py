from .models import Player, Team, PlayerPoints, PlayerUpdate

import requests, time

def get_daily_players_data():
    start = time.time()

    res = requests.get('https://api-fantasy.llt-services.com/api/v3/players').json()

    players = []
    for player in res:
        players.append(requests.get(f'https://api-fantasy.llt-services.com/api/v3/player/{player['id']}').json())


    for playerData in players:
        team, _ = Team.objects.get_or_create(
            teamId=int(playerData['team']['id']),
            name=playerData['team']['name'],
            shortName=playerData['team']['shortName'],
            slug=playerData['team']['slug']
        )

        player, _ = Player.objects.get_or_create(
            playerId=int(playerData['id']),
            name=playerData['name'],
            shortName=playerData['nickname'],
            slug=playerData['slug'],
            lastSeasonPoints=int(playerData['lastSeasonPoints']) if 'lastSeasonPoints' in playerData else 0
        )

        PlayerUpdate.objects.create(
            player=player,
            team=team,
            position=int(playerData['positionId']),
            market_value=playerData['marketValue'],
            status=playerData['playerStatus']
        )

        for playerStat in playerData['playerStats']:
            PlayerPoints.objects.get_or_create(
                player=player,
                round=int(playerStat['weekNumber']),
                points=playerStat['totalPoints'],
                idealXI=playerStat['isInIdealFormation']
            )

    end = time.time()
    print("Tiempo de ejecución:", end - start, "segundos")