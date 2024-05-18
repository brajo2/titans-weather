Guide for how I created the related tables:

Season,Week,Game_Date,Start_Time,Start_Time_GMT_Offset,Game_Site,Home_Team,Home_Team_Final_Score,Visit_Team,Visit_Team_Final_Score
- historical_games
    - game_id (serial primary key)
    - season
    - week
    - game_date
    - start_time
    - start_time_gmt_offset
    - game_site
    - home_team
    - home_team_final_score
    - visit_team
    - visit_team_final_score
    - weather_hash (hash for the weather response)  *[not sure yet how I'll use this]*
    - weather_data (jsonb) _keeping this as a jsonb field for now BECAUSE
      you can therefore add any number of weather data fields without having to change the schema
      (e.g. temperature, humidity, wind_speed, etc.)
      (we can conserve space by storing only relevant weather data in certain months, for
        example, we don't need to store snowfall in August)_
        - _any further statistical analysis can be done in a downstream table (or in the application / API / etc)_
    - use_weather_variable (jsonb) _for whether or not to use the weather data in the analysis, if roof open or closed*
      - { weather_variable0: boolean, weather_variable1: boolean, ... }_
    - venue_id
 
- weather_forecast