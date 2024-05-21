-- 4. wind speeds by latitude and longitude groupings
-- outside venues where might it be trickier to kick a field goal?
with wind_data as (
select venue_id, venue_name, game_id, use_weather_variable,
    avg((value->>'wind_speed_10m')::float) as avg_wind_speed_10m,
    avg((value->>'wind_speed_100m')::float) as avg_wind_speed_100m,
    avg((value->>'soil_moisture_0_to_7cm')::float) as avg_soil_moisture_0_to_7cm
from titans.historical_games,
    jsonb_each(weather_data)
-- for venues with non-closed roofs
where (use_weather_variable->>'wind_speed_10m')::boolean 
    and (use_weather_variable->>'wind_speed_100m')::boolean
group by venue_id, venue_name, game_id
),
lat_lon_binning as (
select venue_id, venue_name, home_team, game_id, venue_geo_latitude, venue_geo_longitude,
    case when venue_geo_latitude < 30 then '0-30'  -- southern cities (new orleans, miami, etc.) 
        when venue_geo_latitude between 30 and 35 then '30 - 35' -- cities like Dallas, Los Angeles, Atlanta
        when venue_geo_latitude between 35 and 40 then '35 - 40' -- cities like denver & indy
        when venue_geo_latitude between 40 and 45 then '40 - 45' -- Chicago, Detroit, Philly
        when venue_geo_latitude >= 45 then '45+' -- north like Seattle, Green Bay
    end as latitude_group,
    case when venue_geo_longitude < -120 then '-120-'  -- west coast like San Francisco, Seattle
        when venue_geo_longitude between -120 and -105 then '-120 - -105' -- west like LA, Phoenix, Denver
        when venue_geo_longitude between -105 and -90 then '-105 - -90'  -- Dallas, Houston, Minneapolis
        when venue_geo_longitude between -90 and -75 then '-90 - -75' -- Atlanta, Jacksonville, Miami
        when venue_geo_longitude >= -75 then '-75+'  -- east coast like East Rutherford, Foxborough
    end as longitude_group
from titans.historical_games
-- for venues with non-closed roofs
where (use_weather_variable->>'wind_speed_10m')::boolean 
    and (use_weather_variable->>'wind_speed_100m')::boolean
),
wind_and_soil_grouped as (
select latitude_group, longitude_group,
    count(*) as num_games_in_group,
    array_agg(distinct home_team) as home_teams_in_group,
    avg(avg_wind_speed_10m) as avg_wind_speed_10m,
    avg(avg_wind_speed_100m) as avg_wind_speed_100m,
    abs(avg(avg_wind_speed_10m) - avg(avg_wind_speed_100m)) as wind_speed_diff_at_elevation,
    avg(avg_soil_moisture_0_to_7cm) as avg_soil_moisture_0_to_7cm
from wind_data wd
join lat_lon_binning lld
using (venue_id, venue_name, game_id)
group by latitude_group, longitude_group
),
wind_and_soil_grouped_ordered as (
select latitude_group, longitude_group,
    num_games_in_group,
    home_teams_in_group,
    wind_speed_diff_at_elevation,
    rank() over (ORDER BY wind_speed_diff_at_elevation desc) as rank_wind_speed_diff_at_elevation,
    avg_soil_moisture_0_to_7cm,
    rank() over (ORDER BY avg_soil_moisture_0_to_7cm desc) as rank_avg_soil_moisture_0_to_7cm,
    avg_wind_speed_10m,
    avg_wind_speed_100m
from wind_and_soil_grouped
order by wind_speed_diff_at_elevation desc
)
select latitude_group, longitude_group,
    num_games_in_group,
    home_teams_in_group,
    wind_speed_diff_at_elevation,
    rank_wind_speed_diff_at_elevation,
    avg_soil_moisture_0_to_7cm,
    rank_avg_soil_moisture_0_to_7cm,
    avg_wind_speed_10m,
    avg_wind_speed_100m
from wind_and_soil_grouped_ordered
order by wind_speed_diff_at_elevation desc;

-- takeaways
-- 1. Kansas City might be the most difficult place to kick a field goal due to the difference in wind speeds at 10m and 100m
-- and checking the soil moisture, it's middle of the road as well
-- therefore, the conversation on Harrison Butker being a great kicker is probably very valid
-- 2. Is it hard to kick a field goal in the Meadowlands?
-- 3.  30 - 35 -90 - -75 24 Jacksonville Jaguars,New Orleans Saints 5.131944444444448
-- The Saints played one game in Jacksonville in 2022 due to Hurricane Ida, so this is an outlier