-- 5. top 10 "slushiest" & snowiest games
with snow_data as (
select venue_id, venue_name, game_id, season, week, home_team, visit_team,
    avg((value->>'snow_depth')::float) as avg_snow_depth,
    avg((value->>'precipitation')::float) as avg_precipitation,
    avg((value->>'soil_moisture_0_to_7cm')::float) as avg_soil_moisture_0_to_7cm
from titans.historical_games,
    jsonb_each(weather_data)
-- for venues with non-closed roofs
where (use_weather_variable->>'snow_depth')::boolean 
    and (use_weather_variable->>'precipitation')::boolean
    and (use_weather_variable->>'soil_moisture_0_to_7cm')::boolean
group by venue_id, venue_name, game_id, season, week, home_team, visit_team
),
snow_data_ranked as (
select venue_id, venue_name, game_id, season, week, home_team, visit_team,
    avg_snow_depth, avg_precipitation, avg_soil_moisture_0_to_7cm,
    rank() over (ORDER BY avg_snow_depth desc) as rank_avg_snow_depth,
    rank() over (ORDER BY avg_precipitation desc) as rank_avg_precipitation,
    rank() over (ORDER BY avg_soil_moisture_0_to_7cm desc) as rank_avg_soil_moisture_0_to_7cm
from snow_data
where avg_snow_depth > 0
)
select venue_name, 
    season, week, home_team, visit_team,
    avg_snow_depth, rank_avg_snow_depth, 
    avg_precipitation, rank_avg_precipitation, 
    avg_soil_moisture_0_to_7cm, rank_avg_soil_moisture_0_to_7cm,
    (rank_avg_snow_depth + rank_avg_precipitation + rank_avg_soil_moisture_0_to_7cm) / 3.0 as avg_slushiness
from snow_data_ranked
group by
    venue_name, 
    season, week, home_team, visit_team,
    avg_snow_depth, rank_avg_snow_depth, avg_precipitation, rank_avg_precipitation, 
    avg_soil_moisture_0_to_7cm, rank_avg_soil_moisture_0_to_7cm
order by avg_slushiness asc
limit 10;

/*
M&T Bank Stadium, Baltimore, MD - season 2021, week 18, Baltimore Ravens, Pittsburgh Steelers -- field slippery
Gillette Stadium, Foxborough, MA - season 2023, week 18, New England Patriots, New York Jets, lot of precipitation and snow depth
Lumen Field (formerly CenturyLink Field), Seattle, WA - season 2021, week 17, Seattle Seahawks, Detroit Lions, field conditions seem okay but a lot of snow and precipitation
*/