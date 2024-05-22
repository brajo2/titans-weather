from typing import List
from pipeline.pipeline_util import multithread_process_games, enrich_game_weather, enrich_venue_data, enrich_game_data, \
    insert_into_postgres_table, create_postgres_table
from shared.constants import BASE_HOURLY_PARAMS
from shared.game_venue import Venue, Game
from shared.hourly_param import HourlyWeatherParam
from shared.weather_enum import Forecast
from sql.sql_helpers import create_pg_engine


def run_forecast():
    # create pipeline titans table
    engine = create_pg_engine()
    create_postgres_table(engine, is_forecast=True)

    # load in the primary csvs, enrich games with Venue classes
    venue_data: List[Venue] = enrich_venue_data('csv/venues.csv')
    game_data: List[Game] = enrich_game_data('csv/future_games.csv', venue_data)

    # get weather for each game, not too many games so non-multithreaded is fine
    game_data = enrich_game_weather(game_data,
                                    weather_variables=BASE_HOURLY_PARAMS + [
                                        HourlyWeatherParam.PRECIPITATION_PROBABILITY_FUTURE],
                                    weather_forecast_type=Forecast.UPCOMING)

    # insert game data into pipeline titans table
    # options here, insert one by one, or in bulk
    # I think bulk is better/quicker for this example but if we ever
    # want to log each game individually to see whether it fails to insert (and why)
    # this game.insert_into_historical() would be a sensible code path
    insert_into_postgres_table(engine, game_data, is_forecast=True)


if __name__ == '__main__':
    run_forecast()
