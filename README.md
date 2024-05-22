### Rough Outline of Engineering Process
#### Created a virtual environment for this in the parent folder:
- virtualenv venv
- source venv/bin/activate
##### Installed some necessary packages:
- `pip install requests tenacity jinja2==3.0.1 pandas tqdm psycopg2-binary sqlalchemy python-dotenv jinjasql` 
  - requests: for making HTTP requests
  - tenacity: for retrying requests (probably not necessary for this API [b/c I don't believe I'll be making more than 10k API calls for this project](https://open-meteo.com/en/terms)
  - jinja2: for templating the SQL insert statements
  - pandas: mostly for reading the csvs in this case, generally used b/c of superior compatibility (also downloads numpy?)
  - tqdm: for progress bars (not necessary for this project, but I like to use it because I can be impatient)
  - psycopg2-binary: for connecting to the postgres database  ( might've been superfluous )
  - python-dotenv: for reading the .env file
  - sqlalchemy: for creating the tables in the database
#### Adjusted the venues.csv and games.csv column headers to be snakecase, because that can become an unnecessary headache. 
  - Looking back I could have written a helper function to do this.

~~#### Added a mechanism to find the geolocation of each city in the game site column of the games.csv (using geocoding API)~~
#### Created map for outlier game site names like Tampa Bay and Las Vegas
  - I had another idea to use the geocoding API to find the latitude and longitude of the game site, but there weren't SO many outliers that it was necessary. And it would've required a good number of additional API calls that would've extended the length of the work. In addition, I would've had to use a methodology to find the closest stadium to the geocoded location, and use manhattan distance or haversine distance formula to find close stadiums for a problem that really only existed for a few stadiums.
#### I opted against using games without venues accounted for in the csv
  - This could be an outstanding issue for calculation around international games or past stadiums that no longer exist. 
  - It'd be possible to scavenge for the stats about those venues, but seemed outside of scope.
#### Set up local .env variables in the parent folder (for the database connection), but didn't include them in the repo for security reasons.
#### Created a database called "titans" in postgres

### The historical_main.py script
#### How to run:
- `python3 historical_main.py`
#### What it does:
- creates the tables (if not exists)
- reads the local csvs & creates a Game class for each row (where each game is assigned a Venue, which makes it later possible to find weather)
- requests the API for the weather data for each game and stores it into the Game class.
- inserts each games data into the denormalized database table (historical_games) using Jinja templating
- connects to postgres database (provided that the ENV variable for the user is set to a certain host/port/etc.)

### The forecast_main.py script
#### How to run:
- `python3 forecast_main.py`
- (this script can only run weather for certain games that are to be played within the next 14 days)
- If outside the window, then the game would be considered None by the pipeline and not show up in the final database.

### Thoughts on the API & developing interesting features
#### Open Meteo API thoughts:
  - One thing I should have taken into account a little more was the amount of parameters in the API requrest, if you add enough then you can make the equivalent of ~1.8 calls in one call, for example.
  - Particularly because of the way `venues.csv` is set up to acknowledge both surface and roof, it made sense for me to use a dictionary of variables that are affected by the ground and the variables affected by the air/wind/temperature/humidity.
    - I think we can imagine a simple grass field in a park would be fully affected by the weather: air, wind, temperature, humidity, soil moisture, etc.
    - But if we play in a closed roof stadium, the temperature, humidity, wind, air pressure, soil moisture, snow depth, etc. are all "balanced" (I don't know what stable #s are)
    - unless the roof was open before the day of the game, and it rained into the stadium, but I think that's too complex for now
    - If we play on turf, the soil moisture, etc. are still affected by the weather but probably less, so therefore we may be able to ignore soil moisture from the forecast.
    - Since this is complex, I think it's at least best to store information about whether or not to use the weather variable--but at this stage of the pipeline, we don't necessarily have to know all about how we'll handle the field variances.
#### Retractable Roof (determining where to assume it's been closed, didn't handle this dynamically (and just assumed closure for sake of simplicity))
#### Prospective querying thoughts:
  - Downstream tables with venue summary data (e.g. average temperature, average humidity, average wind speed, etc.) could be useful for analysis
    - and moreso w.r.t. months, seasons, etc. (particularly as there are more entries to stabilize)
  - per venue, per venue per season, per season
  - rollup tables
##### future goals, cool stuff:
- projected scores based on weather situations
- rostered players & EPA/play based on weather situations
- team EPA/play vs weather situations

--------
### Directories
  - api: interacts with the open meteo API
  - sql: contains the SQL code for creating the tables & the jinja templating (& also has a readme for data table design decisions)
    - **also includes the 5 queries that I chose to investigate my datamart table**
  - csv: obtains the csvs from the API
  - shared: shared functions, helpers, constants, parameters
    - Game & Venue objects, core methods for identifying weather for a game
  - pipeline: the modularized pipeline for both forecast and historical data
  - final_dataset: the final datasets that are created from the pipeline
  
### Output files/queries for task:
##### SQL queries:
[5 Interesting Queries](sql/queries)

##### 2021-2023 final datasets:
[historical_games](final_dataset/historical_games_202405211916.xlsx)

##### 2024 forecasted games (fake data):
[forecasted games](final_dataset/forecast_games_202405211930.xlsx)

