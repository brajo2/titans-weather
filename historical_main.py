from typing import List

from tqdm import tqdm

from api.historical_request import get_weather
from historical.historical_pipeline import enrich_venue_data, enrich_game_data, multithread_process_games, \
    create_historical_table, insert_into_historical_table, enrich_game_weather
from shared.constants import BASE_HOURLY_PARAMS, GAME_LENGTH, PRE_GAME_WINDOW
from shared.game_venue import Venue, Game
from sql.sql_helpers import create_pg_engine


def run_historical():
    # create historical titans table
    engine = create_pg_engine()
    create_historical_table(engine)

    # load in the primary csvs, enrich games with Venue classes
    venue_data: List[Venue] = enrich_venue_data('csv/venues.csv')
    game_data: List[Game] = enrich_game_data('csv/games.csv', venue_data)

    # get weather for each game
    # one at a time, very slow (5+ minutes)
    # game_data = enrich_game_weather(game_data)

    # but could be multithreaded for speed!!
    # as there are 800+ calls to the API (takes 40 seconds instead)
    game_data = multithread_process_games(game_data)


    # insert game data into historical titans table
    # options here, insert one by one, or in bulk
    # I think bulk is better/quicker for this example but if we ever
    # want to log each game individually to see whether it fails to insert (and why)
    # this game.insert_into_historical() would be a sensible code path
    insert_into_historical_table(engine, game_data)

if __name__ == '__main__':
    run_historical()