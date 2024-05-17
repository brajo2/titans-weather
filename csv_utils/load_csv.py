# loading game data from csv_utils
from typing import List
from shared.game_venue import Game, Venue

import pandas as pd

def load_venue_data(file_path: str) -> List[Venue]:
    venues: List[Venue] = []
    try:
        data = pd.read_csv(file_path)

        for index, row in data.iterrows():
            venue = Venue(
                name=row['name'],
                capacity=row['capacity'],
                location=row['location'],
                surface=row['surface'],
                roof_type=row['roof_type'],
                teams=row['teams'],
                opened=row['opened'],
                geo=row['geo'],
                id=index,
            )
            venues.append(venue)
    except Exception as e:
        print(f"Error loading venue data: {e}")
        raise e

    return venues

def load_game_data(file_path: str, venues: List[Venue]) -> List[Game]:
    """
    because venues host games, it'll make sense to load the venue data first

    :param file_path:
    :return:
    """
    games: List[Game] = []
    try:
        data = pd.read_csv(file_path)

        for index, row in data.iterrows():
            game = Game(
                season=row['season'],
                week=row['week'],
                game_date=row['game_date'],
                start_time=row['start_time'],
                start_time_gmt_offset=row['start_time_gmt_offset'],
                game_site=row['game_site'],
                home_team=row['home_team'],
                home_team_final_score=row['home_team_final_score'],
                visit_team=row['visit_team'],
                visit_team_final_score=row['visit_team_final_score'],
            )
            game.venue = game.set_venue(venues)
            games.append(game)
    except Exception as e:
        print(f"Error loading game data: {e}")
        raise e

    return games