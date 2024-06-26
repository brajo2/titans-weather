CREATE TABLE if not exists {{schema}}.{% if is_forecast %}forecast{% else %}historical{% endif %}_games (
    game_id SERIAL PRIMARY KEY,
    season INT,
    week INT,
    game_date DATE,
    start_time TIME,
    start_time_gmt_offset INT,
    game_site text,
    home_team text,
    home_team_final_score INT,
    visit_team text,
    visit_team_final_score INT,
    weather_hash text,
    weather_data JSONB,
    weather_units JSONB,
    use_weather_variable JSONB,
    venue_id INT,
    venue_name text,
    venue_geo_latitude FLOAT,
    venue_geo_longitude FLOAT,
    venue_surface text,
    venue_roof_type text
    {% if is_forecast %}
    , is_played BOOLEAN
    , home_team_score_predicted FLOAT DEFAULT NULL
    , visit_team_score_predicted FLOAT DEFAULT NULL
    , home_team_win_probability_predicted FLOAT DEFAULT NULL
    , visit_team_win_probability_predicted FLOAT DEFAULT NULL
    {% endif %}
);