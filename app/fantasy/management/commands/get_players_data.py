from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser

from fantasy.api import FantasyAPI
from fantasy.models import Player, Team, PlayerPoints, PlayerUpdate

import os, json, requests
from datetime import datetime


class Command(BaseCommand):
    help = "Download and store the players data from API or a json file."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--file",
            type=str,
            help="Data source file path for database population, overriding API-based latest data retrieval."
        )
        parser.add_argument(
            "--url",
            type=str,
            help="Data source url path for database population, overriding API-based latest data retrieval."
        )
        parser.add_argument(
            "--date",
            type=str,
            help="Date of the data in the specified file (format: YYYY-MM-DD)."
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        file_path = options['file']
        url_path = options['url']
        date_str = options['date']

        if file_path:

            if not os.path.isfile(file_path):
                raise CommandError(f"The file at {file_path} does not exist or is not accessible.")

            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                raise CommandError(f"The file at {file_path} is not a valid JSON file.")

            if not date_str:
                raise CommandError("The --date parameter is required when specifying the --file parameter.")
            
            try:
                data_dt = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                raise CommandError("The --date parameter must be in the format YYYY-MM-DD.")
            
            self.stdout.write(f"File loaded successfully with {len(data)} records.")
            self.stdout.write(f"Data date: {data_dt}")

        elif url_path:
            if not date_str:
                raise CommandError("The --date parameter is required when specifying the --file parameter.")
            
            try:
                data_dt = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                raise CommandError("The --date parameter must be in the format YYYY-MM-DD.")
            
            try:
                res = requests.get(url_path)
                res.raise_for_status()

                data = res.json()
            except Exception as e:
                raise CommandError(str(e))

        else:
            self.stdout.write("No file specified. Proceeding with API-based data retrieval.")

            data_dt = datetime.now().date()

            api = FantasyAPI()
            try:
                data = api.get_players_with_details()
            except Exception as e:
                raise CommandError(str(e))

        for playerData in data:
            team, _ = Team.objects.get_or_create(
                team_api_id=int(playerData['team']['id']),
                name=playerData['team']['name'],
                short_name=playerData['team']['shortName'],
                slug=playerData['team']['slug']
            )

            player, _ = Player.objects.get_or_create(
                player_api_id=int(playerData['id']),
                name=playerData['name'],
                short_name=playerData['nickname'],
                slug=playerData['slug'],
                last_season_points=int(playerData['lastSeasonPoints']) if 'lastSeasonPoints' in playerData else 0
            )

            PlayerUpdate.objects.update_or_create(
                player=player,
                team=team,
                date=data_dt,
                defaults={
                    "position": int(playerData['positionId']),
                    "market_value": playerData['marketValue'],
                    "status": playerData['playerStatus'],
                }
            )

            for playerStat in playerData['playerStats']:
                PlayerPoints.objects.update_or_create(
                    player=player, 
                    round=int(playerStat['weekNumber']),
                    defaults={
                        "points": playerStat['totalPoints'],
                        "ideal_xi": playerStat['isInIdealFormation'],
                    },
                    create_defaults={
                        "team": team,
                        "position": int(playerData['positionId']),
                        "points": playerStat['totalPoints'],
                        "ideal_xi": playerStat['isInIdealFormation'],
                    }
                )