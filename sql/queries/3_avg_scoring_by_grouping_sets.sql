-- 3. avg scoring by surface type
-- by roof type
-- by rain type
-- by surface + roof type
-- by surface + roof + rain type
-- where rain type is classified like:
/*
if drizzle is <0.5, light rain between 0.5 & 4, then what's rain and what's heavy rain and what's a downpour

ChatGPT
Rainfall intensity can be categorized as follows:

Rain (Moderate Rain): This typically involves precipitation rates between 4 and 16 millimeters per hour. It's steady and can saturate the ground over time.

Heavy Rain: This is characterized by rates greater than 16 millimeters per hour but less than 50 millimeters per hour. Visibility can be significantly reduced, and there may be rapid water accumulation on roads and other surfaces.

Downpour (or Torrential Rain): This involves very intense rainfall rates, usually exceeding 50 millimeters per hour. Downpours are often brief but can lead to sudden flooding and other hazardous conditions.
*/
-- but we also need to consider whether the "use_weather_variable" is true or false, which would mean there's no rain
with scoring_and_rain as (
select venue_id, venue_name, game_id, venue_surface, venue_roof_type,
    (use_weather_variable->>'rain')::boolean AS use_rain,
    max(home_team_final_score + visit_team_final_score) as total_score,  -- avg/max works because jsonb_each returns multiple rows of the same game
    avg(case when (use_weather_variable->>'rain')::boolean then (value->>'rain')::float
        else 0 end) as avg_rain  -- if we aren't supposed to count the rain then we won't
from titans.historical_games,
    jsonb_each(weather_data)
group by venue_id, venue_name, game_id, venue_surface, venue_roof_type,
    (use_weather_variable->>'rain')::boolean
),
combined_data as (
select venue_id, venue_name, game_id, venue_surface, venue_roof_type, 
    total_score,
    case when use_rain = FALSE then 'No Rain'
        when use_rain and avg_rain = 0 then 'No Rain'
        when use_rain and avg_rain < 0.5 then 'Drizzle'
        when use_rain and avg_rain >= 0.5 and avg_rain < 4 then 'Light Rain'
        when use_rain and avg_rain >= 4 and avg_rain < 16 then 'Rain'
        when use_rain and avg_rain >= 16 and avg_rain < 50 then 'Heavy Rain'
        when use_rain and avg_rain >= 50 then 'Downpour'
        else 'Unknown'
    end as rain_type
from scoring_and_rain
)
select venue_surface, venue_roof_type,
    rain_type,
    avg(total_score) as avg_total_score,
    count(*) as num_games,
    CASE WHEN venue_surface IS NOT NULL AND venue_roof_type IS NULL AND rain_type IS NULL THEN 0
    WHEN venue_surface IS NULL AND venue_roof_type IS NOT NULL AND rain_type IS NULL THEN 1
    WHEN venue_surface IS NULL AND venue_roof_type IS NULL AND rain_type IS NOT NULL THEN 2
    WHEN venue_surface IS NOT NULL AND venue_roof_type IS NOT NULL AND rain_type IS NULL THEN 3
    WHEN venue_surface IS NOT NULL AND venue_roof_type IS NOT NULL AND rain_type IS NOT NULL THEN 4
    END AS grouping_set_id
from combined_data
group by grouping sets (
    (venue_surface),
    (venue_roof_type),
    (rain_type),
    (venue_surface, venue_roof_type),
    (venue_surface, venue_roof_type, rain_type)
)
order by grouping_set_id, avg_total_score desc;
/*
-- takeaways
Teams scored a lot on grassmaster, but not much on Kentucky bluegrass (grouping set id - 0)
Teams score less in open roofs than closed roofs (grouping set id - 1)
Teams don't really play during torrential downpours, but light rain *might* affect the game (grouping set id - 2)
FieldTurf Core + Fixed (closed) dome could the best for scoring 
    but it could also be the team [New York Giants] or their opponent (b.c of their own team defense) (grouping set id - 3)
*/