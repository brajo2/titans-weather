# loading game data from csv_utils
from typing import List
from shared.game_venue import Game, Venue

import pandas as pd

def load_venue_data(file_path: str) -> List[Venue]:
    venues: List[Venue] = []
    data = pd.read_csv(file_path)

    for index, row in data.iterrows():
        venue = Venue(
            name=row['Name'],
            capacity=row['Capacity'],
            location=row['Location'],
            surface=row['Surface'],
            roof_type=row['Roof_Type'],
            teams=row['Teams'],
            opened=row['Opened'],
            geo=(row['Latitude'], row['Longitude'])
        )
        venues.append(venue)
    return venues

def load_game_data(file_path: str, venues: List[Venue]) -> List[Game]:
    """
    because venues host games, it'll make sense to load the venue data first

    :param file_path:
    :return:
    """
    games: List[Game] = []
    data = pd.read_csv(file_path)

    for index, row in data.iterrows():
        game = Game(
            season=row['Season'],
            week=row['Week'],
            game_date=row['Game_Date'],
            start_time=row['Start_Time'],
            start_time_gmt_offset=row['Start_Time_GMT_Offset'],
            game_site=row['Game_Site'],
            home_team=row['Home_Team'],
            home_team_final_score=row['Home_Team_Final_Score'],
            visit_team=row['Visit_Team'],
            visit_team_final_score=row['Visit_Team_Final_Score'],
        )
        game.venue = game.set_venue(venues)
        games.append(game)