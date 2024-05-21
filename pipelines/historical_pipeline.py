# Define the function that fetches weather for a single game
import concurrent
import json
import uuid
from importlib import resources
from typing import List

import pandas as pd
from sqlalchemy import text
from tqdm import tqdm

from api.api_requests import get_weather
from shared.constants import BASE_HOURLY_PARAMS, GAME_LENGTH, PRE_GAME_WINDOW
from shared.game_venue import Venue, Game, NoMatchingVenueError
from sql import templates
from sql.jinja_helpers import generate_templated_sql
from sql.sql_helpers import SCHEMA, execute_postgres_query, HISTORICAL_TABLE_INSERT_COLS


def fetch_weather_for_game(game: Game):
    if game.venue:
        game.weather = get_weather(
            game.venue.geo[0],
            game.venue.geo[1],
            game.game_date,  # the beginning of the day
            game.game_date,  # the end of the same day effectively
            variables=BASE_HOURLY_PARAMS
        )
        game.narrow_weather_hour_window(start_hour=game.start_time.hour,
                                        game_length=GAME_LENGTH,
                                        pre_game_window=PRE_GAME_WINDOW)
        return game


def multithread_process_games(game_data):
    processed_games = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_game = {executor.submit(fetch_weather_for_game, game): game for game in game_data}

        for future in tqdm(concurrent.futures.as_completed(future_to_game), total=len(game_data)):
            game = future_to_game[future]
            if game is None: continue
            try:
                processed_game = future.result()
                processed_games.append(processed_game)
            except Exception as e:
                print(f"Error processing game {game}: {str(e)}")
    return processed_games


# todo - deprecate
def enrich_game_weather(game_data):
    for game in tqdm(game_data):
        if game.venue:
            game.weather = get_weather(
                game.venue.geo[0],
                game.venue.geo[1],
                game.game_date,  # the beginning of the day
                game.game_date,  # the end of the same day effectively
                variables=BASE_HOURLY_PARAMS
            )
            game.narrow_weather_hour_window(start_hour=game.start_time.hour,
                                            game_length=GAME_LENGTH,
                                            pre_game_window=PRE_GAME_WINDOW)


def enrich_venue_data(file_path: str) -> List[Venue]:
    venues: List[Venue] = []
    try:
        data = pd.read_csv(file_path)

        for index, row in data.iterrows():
            venue = Venue(
                name=escape_single_quotes(row['name']),
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


def enrich_game_data(file_path: str, venues: List[Venue]) -> List[Game]:
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

            # check if the game finished... (Cincinnati vs Buffalo 2022?)
            if not game.check_if_game_finished(): continue

            try:
                game.set_venue(venues)
            except NoMatchingVenueError as e:
                print(f"Error setting venue for game {game}: {e}, skipping game")
                game.venue = None
            game.set_use_weather_variables(venues)
            games.append(game)
    except Exception as e:
        print(f"Error loading game data: {e}")
        raise e

    return games


def create_historical_table(engine):
    params = {
        'schema': SCHEMA,
    }
    query_template = resources.read_text(templates, 'create_historical_table.j2.sql')
    query = generate_templated_sql(
        sql_template=query_template,
        **params,
    )
    query = text(query)

    execute_postgres_query(query, engine, query_type="create")


def insert_into_historical_table(engine, games: List[Game]):
    """
    Insert game data into the historical_games table
    :param engine:
    :param games:
    :return:
    """
    def build_games_df(games):
        all_data = []
        for game in games:
            if game is not None:
                data = {
                        "season": game.season,
                        "week": game.week,
                        "game_date": game.game_date,
                        "start_time": f"{game.start_time.hour:02}:{game.start_time.minute:02}",
                        "start_time_gmt_offset": game.start_time_gmt_offset,
                        "game_site": game.game_site,
                        "home_team": game.home_team,
                        "home_team_final_score": game.home_team_final_score,
                        "visit_team": game.visit_team,
                        "visit_team_final_score": game.visit_team_final_score,
                        "weather_hash": uuid.uuid4().hex,  # hash for the weather response
                        "venue_id": game.venue.id,
                        "venue_name": game.venue.name,
                        "venue_geo_latitude": game.venue.geo[0],
                        "venue_geo_longitude": game.venue.geo[1],
                        "venue_surface": game.venue.surface,
                        "venue_roof_type": game.venue.roof_type,
                    }
                # add weather units to the dictionary
                data.update({"weather_units": game.weather['hourly_units']})

                # add weather data to the dictionary
                weather_data = [{field: getattr(hourly_tuple, field) for field in hourly_tuple._fields}
                                for hourly_tuple in game.weather['hourly']]
                data.update({"weather_data": weather_data})

                # add "use_weather_variables" to the dictionary
                # todo - revisit, this is a rough implementation to find 'snow_depth': True, 'snowfall': True, etc.
                weather_variables_usage_dict = {v.value.param_name: w for v, w in game.use_weather_variables.items() \
                                     if v.value.param_name in game.weather['hourly'][0]._fields}
                data.update({"use_weather_variable": weather_variables_usage_dict})

                all_data.append(data)

        df = pd.DataFrame(all_data)

        # convert weather data list of dictionaries to JSON
        df['weather_data'] = (
            df['weather_data']
            .apply(lambda x: {i: v for i, v in enumerate(x)})
            .apply(json.dumps)
        )
        # json dumps to weather units and use_weather_variables
        df['weather_units'] = df['weather_units'].apply(json.dumps)
        df['use_weather_variable'] = df['use_weather_variable'].apply(json.dumps)

        # convert integer columns to integer
        integer_col_names = [col.name for col in HISTORICAL_TABLE_INSERT_COLS if col.type == 'INT']
        for col in integer_col_names:
            df[col] = df[col].astype(int)

        return df


    games_df = build_games_df(games)

    params = {
        'schema': SCHEMA,
        'df': games_df,
        'columns': HISTORICAL_TABLE_INSERT_COLS,
        'list_columns': ['weather_data'],
    }
    query_template = resources.read_text(templates, 'insert_into_historical_table.j2.sql')
    query = generate_templated_sql(
        sql_template=query_template,
        **params,
    )
    query = text(query)

    execute_postgres_query(query, engine, query_type="insert")


def escape_single_quotes(value):
    if isinstance(value, str):
        new_value = str(value)
        new_value = new_value.replace("'", "''")
        return new_value
    return value