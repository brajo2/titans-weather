from typing import List
from pipeline.pipeline_util import multithread_process_games, enrich_venue_data, enrich_game_data, \
    create_postgres_table, insert_into_postgres_table
from shared.game_venue import Venue, Game
from shared.weather_enum import Forecast
from sql.sql_helpers import create_pg_engine


def run_historical():
    # create pipeline titans table
    engine = create_pg_engine()
    create_postgres_table(engine, is_forecast=False)

    # load in the primary csvs, enrich games with Venue classes
    venue_data: List[Venue] = enrich_venue_data('csv/venues.csv')
    game_data: List[Game] = enrich_game_data('csv/games.csv', venue_data)

    # could get weather for each game, one at a time, but very slow (5+ minutes)
    # but could be multithreaded to speed up
    # as there are 800+ calls to the API (takes 40 seconds instead)
    game_data = multithread_process_games(game_data, weather_forecast_type=Forecast.ARCHIVE)


    # insert game data into pipeline titans table
    # options here, insert one by one, or in bulk
    # I think bulk is better/quicker for this example but if we ever
    # want to log each game individually to see whether it fails to insert (and why)
    # this game.insert_into_postgres() would be a sensible code path
    insert_into_postgres_table(engine, game_data, is_forecast=False)

if __name__ == '__main__':
    run_historical()