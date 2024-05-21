-- 1. per week per season total points vs average apparent temperature
with apparent_temp_data as (
select season, week, game_id,
	avg((value->>'apparent_temperature')::float) as avg_hourly_apparent_temperature
from titans.historical_games,
	jsonb_each(weather_data)
group by season, week, game_id
),
total_score_data as (
select season, week, game_id,
    sum(home_team_final_score + visit_team_final_score) as total_score
from titans.historical_games
group by season, week, game_id
)
select season, 
week, 
avg(avg_hourly_apparent_temperature) as avg_hourly_apparent_temperature_per_week, 
avg(total_score) as avg_total_score_per_week
from apparent_temp_data atd
join total_score_data tsd
using (season, week, game_id)
group by 1,2;
/*
- takeaways 
To check a correlation between apparent temperature and total points scored
Some colder weeks have lower overall scores, but defenses also have more offensive tendencies that have been studied by that point in the season.
*/
