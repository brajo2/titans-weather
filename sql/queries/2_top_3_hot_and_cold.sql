-- 2. top 3 hottest (by apparent temperature) averages and top 3 coldest  on average (by apparent temperature) per season per venue
with apparent_temp_data as (
select venue_id, venue_name, game_site, season, game_id,
    avg((value->>'apparent_temperature')::float) as avg_hourly_apparent_temperature
from titans.historical_games,
    jsonb_each(weather_data)
group by venue_id, venue_name, game_site, season, game_id
),
hottest_and_coldest as (
select venue_id, venue_name, game_site, season,
    avg(avg_hourly_apparent_temperature) as avg_seasonal_hourly_apparent_temperature
from apparent_temp_data
group by venue_id, venue_name, game_site, season
),
ranked_hottest as (
select venue_id, venue_name, game_site, season,
    avg_seasonal_hourly_apparent_temperature,
    rank() over (partition by season order by avg_seasonal_hourly_apparent_temperature desc) as r
from hottest_and_coldest
),
ranked_coldest as (
select venue_id, venue_name, game_site, season,
    avg_seasonal_hourly_apparent_temperature,
    rank() over (partition by season order by avg_seasonal_hourly_apparent_temperature asc) as r
from hottest_and_coldest
)
select ranked_hottest.season,
    ranked_hottest.r as rank_hot, 
    ranked_hottest.venue_name as venue_hot,
    ranked_hottest.game_site as game_site_hot,
    ranked_hottest.avg_seasonal_hourly_apparent_temperature as avg_temp_hot,
    ranked_coldest.r as rank_cold,
    ranked_coldest.venue_name as venue_cold,
    ranked_coldest.game_site as game_site_cold,
    ranked_coldest.avg_seasonal_hourly_apparent_temperature as avg_temp_cold
from ranked_hottest
join ranked_coldest
on ranked_hottest.r = ranked_coldest.r
and ranked_hottest.season = ranked_coldest.season
where ranked_hottest.r <= 3
or ranked_coldest.r <= 3
order by season;
-- takeaways
-- very basic but Florida is hot and the upper midwest is cold.