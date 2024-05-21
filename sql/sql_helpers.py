"""
Some personally created / commonly used SQL helper functions
"""
import os
from collections import namedtuple
from contextlib import closing

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

SCHEMA = "titans"
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")
DB = os.getenv("POSTGRES_DB")

RowDefinition = namedtuple('RowDefinition', ['name', 'type'])
HISTORICAL_TABLE_INSERT_COLS = [
    RowDefinition('season', 'INT'),
    RowDefinition('week', 'INT'),
    RowDefinition('game_date', 'DATE'),
    RowDefinition('start_time', 'TIME'),
    RowDefinition('start_time_gmt_offset', 'INT'),
    RowDefinition('game_site', 'TEXT'),
    RowDefinition('home_team', 'TEXT'),
    RowDefinition('home_team_final_score', 'INT'),
    RowDefinition('visit_team', 'TEXT'),
    RowDefinition('visit_team_final_score', 'INT'),
    RowDefinition('weather_hash', 'TEXT'),
    RowDefinition('weather_data', 'JSONB'),
    RowDefinition('weather_units', 'JSONB'),
    RowDefinition('use_weather_variable', 'JSONB'),
    RowDefinition('venue_id', 'INT'),
    RowDefinition('venue_name', 'TEXT'),
    RowDefinition('venue_geo_latitude', 'FLOAT'),
    RowDefinition('venue_geo_longitude', 'FLOAT'),
    RowDefinition('venue_surface', 'TEXT'),
    RowDefinition('venue_roof_type', 'TEXT'),
]

def create_pg_engine(env="main", timeout=50, pool_size=10, max_overflow=20, pool_recycle=3600):
    if env:
        user = USER
        password = PASSWORD
        host = HOST
        port = PORT
        db = DB

    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    engine = create_engine(url, connect_args={'connect_timeout': timeout},
                           pool_size=pool_size, max_overflow=max_overflow, pool_recycle=pool_recycle, )
    return engine


def execute_postgres_query(query, engine, query_type=None):
    # Determine query type if not provided
    if not query_type:
        query_type = query.strip().split(" ", 1)[0].lower()

    try:
        with closing(engine.connect()) as conn:
            with conn.begin():
                rs = conn.execute(query)

                # If it's a SELECT query, return the result set
                if query_type == "select":
                    result_set = rs.fetchall()
                    return [{column: value for column, value in row.items()} for row in result_set]
                else:
                    # For non-SELECT queries, return the number of rows affected
                    # No attempt to iterate over rs is made here
                    return f"{rs.rowcount} rows affected."

    except Exception as e:
        print(e)
        raise e


