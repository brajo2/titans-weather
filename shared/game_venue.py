from collections import namedtuple
from typing import List, Tuple

from api_utils.geocoding import get_geolocations
from shared.constants import SURFACE_VARIABLES, ROOF_VARIABLES
from shared.util import convert_date_format

"""
Venues are where games are played
So a game has-a venue
----------------

Name,Capacity,Location,Surface,Roof Type,Team(s),Opened,Geo
Acrisure Stadium,68400,"Pittsburgh, Pennsylvania",Kentucky bluegrass,Open,Pittsburgh Steelers,2001,"40.446667,�-80.015833"
"""

Geolocation = namedtuple('geo', ['latitude', 'longitude'])
City = namedtuple('city', ['city', 'state'])
MilitaryTime = namedtuple('hour_minute', ['hour', 'minute'])

# SOME GAME SITES ARE NOT EQUIVALENT TO THE CITY OF THE VENUE
CITY_NAME_MAP = {
    "Tampa Bay": "Tampa",  # game is in Tampa, Florida not Tampa Bay, Florida
    "Las Vegas": "Paradise",  # game is in Paradise, Nevada not Las Vegas, Nevada
}

##########################
#### ALTERNATIVE IDEA based upon discrepancy between game site names like "Tampa Bay" and venue cities like "Tampa"
# class GameLocation:  # todo - deprecate
#     # found this necessary when it was apparent that the game sites had names
#     # that were not equivalent to the names of the cities of the Venues
#     # so we need to match geolocations to game sites
#     def __init__(self, city: City, geolocation: Geolocation, population: int):
#         self.city = city
#         self.geolocation = geolocation
#         self.population = population
#
#     def __repr__(self):
#         return f"GameLocation(city={self.city}, geolocation={self.geolocation}, population={self.population})"
##########################
# downside to me, was the potential for a lot of API calls to get the geolocations
# and the time it'd take would increase the more returns the user chose from geocoding API
# and the more venues there were to match to the game sites
##########################

# Needed a custom exception when no matching venue is found
class NoMatchingVenueError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Venue:
    def __init__(self, name, capacity, location, surface, roof_type, teams, opened, geo, id):
        reprocessed_geo = self.split_and_clean_geo(geo=geo)
        reprocessed_city = self.split_city(location=location)

        self.name = name
        self.capacity = capacity
        self.location = location
        self.surface = surface
        self.roof_type = roof_type
        self.teams = teams
        self.opened = opened
        self.geo = geo
        self.id = id
        self.geo = reprocessed_geo
        self.location = reprocessed_city

    def __str__(self):
        return f"{self.name} {self.capacity} {self.location} {self.surface} {self.roof_type} {self.teams} {self.opened} {self.geo}"

    def __repr__(self):
        return f"{self.name} {self.capacity} {self.location} {self.surface} {self.roof_type} {self.teams} {self.opened} {self.geo}"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def split_and_clean_geo(self, geo) -> Geolocation:
        """
        split the geo string and clean it b/c there's a strange character in the upload
        these should be two floats
        :param geo:
        :return:
        """
        geo = geo.replace('�', '')  # todo - hacky
        return Geolocation(*geo.split(','))

    def split_city(self, location) -> City:
        return City(*location.split(','))

    def set_should_use_weather_data(self):  # todo - get "business" rules update
        # only would know if the venue is set though
        """
        could use refinement on this logic
        If the venue is closed, we *may* not need to use weather data
        If the venue is turf, we *may* not need to use the weather data for the surface variables
        :return:
        """
        weather_usage = {x: True for x in [*SURFACE_VARIABLES, *ROOF_VARIABLES]}
        if self.roof_type.lower() == 'closed':
            weather_usage = {x: False for x in [*SURFACE_VARIABLES, *ROOF_VARIABLES]}
        if 'turf' in self.surface.lower():  # string comparison here is a bit tricky / could be improved
            for key in SURFACE_VARIABLES:
                weather_usage[key] = False

        return weather_usage


"""
Season,Week,Game_Date,Start_Time,Start_Time_GMT_Offset,Game_Site,Home_Team,Home_Team_Final_Score,Visit_Team,Visit_Team_Final_Score
2021,1,9/9/2021,20:20,-5,Tampa Bay,Tampa Bay Buccaneers,31,Dallas Cowboys,29

I'm making a "game" class object to store this game's data in a more structured way
then I will be able to add the weather data to the game object once we request it
"""


class Game:
    def __init__(self, season, week, game_date, start_time, start_time_gmt_offset, game_site, home_team,
                 home_team_final_score, visit_team, visit_team_final_score,
                 use_weather_variables: dict = {},  # this is a flag to determine if we should use the weather data
                 venue: Venue = None):
        # todo - deprecate reprocessed game sites
        # reprocessed_game_sites: List[City] = self.find_game_cities_ranked_by_population(game_site=game_site)
        reprocessed_game_date = convert_date_format(game_date)
        reprocessed_start_time: MilitaryTime = self._split_hour_minute(start_time)

        self.season = season
        self.week = week
        self.game_date = reprocessed_game_date
        self.start_time = reprocessed_start_time
        self.start_time_gmt_offset = start_time_gmt_offset
        self.game_site = game_site
        self.home_team = home_team
        self.home_team_final_score = home_team_final_score
        self.visit_team = visit_team
        self.visit_team_final_score = visit_team_final_score
        self.venue = venue
        self.use_weather_variables = use_weather_variables
        self.weather = None  # this will be set after we request the weather data
        # self.game_location_options: List[GameLocation] = reprocessed_game_sites

    def __str__(self):
        return f"{self.season} {self.week} {self.game_date} {self.start_time} {self.start_time_gmt_offset} {self.game_site}" \
               f" {self.home_team} {self.home_team_final_score} {self.visit_team} {self.visit_team_final_score} {self.venue} {self.use_weather_variables} {self.weather} "

    def __repr__(self):
        return f"{self.season} {self.week} {self.game_date} {self.start_time} {self.start_time_gmt_offset} {self.game_site}" \
               f" {self.home_team} {self.home_team_final_score} {self.visit_team} {self.visit_team_final_score} {self.venue} {self.use_weather_variables} {self.weather}"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    # todo - deprecate (see above)
    # def set_venue_with_geolocation_proximity(self, venues: List[Venue]):
    #     venue_geolocations = [x.geo for x in venues]
    #     game_site_geolocations = [x.geolocation for x in self.game_location_options]
    #     if set(venue_geolocations).intersection(set(game_site_geolocations)):
    #         pass

    def _split_hour_minute(self, start_time: str) -> MilitaryTime:
        time_tuple = tuple(map(int, start_time.split(':')))
        return MilitaryTime(*time_tuple)

    def set_venue(self, venues: List[Venue]):
        venue_cities_catalog: dict = {x.location.city: x for x in venues}
        game_city = CITY_NAME_MAP.get(self.game_site, self.game_site)
        if game_city in venue_cities_catalog:
            self.venue = venue_cities_catalog[game_city]
        else:  # use the no-matching venue exception (because this is a special instance that shouldn't keep the
            # program from running
            raise NoMatchingVenueError(f"Game site city {game_city} not found in venues")

    def set_use_weather_variables(self, venues: List[Venue]):
        if self.venue:
            self.use_weather_variables = self.venue.set_should_use_weather_data()
        else:
            try:
                self.set_venue(venues=venues)
                self.set_use_weather_variables()
            except NoMatchingVenueError as e:
                print(f"Error setting venue for game {self}: {e}, can't set variables for game")
                self.use_weather_variables = {x: False for x in [*SURFACE_VARIABLES, *ROOF_VARIABLES]}  # if we can't find a venue, we can't use weather data

    def narrow_weather_hour_window(self,
                                   start_hour: int,
                                   game_length: int = 3,
                                   pre_game_window: int = 2):
        """
            There's weather returned for the entire day but we don't care about ALL of it
            We care about the weather during the game
            and maybe a little bit before
        :param start_hour: military time hour
        :param game_length: in hours
        :param pre_game_window: in hours
        :return:
        """
        self.weather['hourly'] = self.weather['hourly'][start_hour - pre_game_window: start_hour + game_length + 1]

    ##################
    # todo - deprecate, cool idea but no need to run it in favor of just a map that adjusts for certain game_site names
    # being different from venue cities
    # def find_game_locations_ranked_by_population(self, game_site: str) -> List[GameLocation]:
    #     # need to hit the geocoding api to get the most relevant US cities by population
    #     # then we can match the game site to the city
    #     city_responses_raw = get_geolocations(name=game_site)
    #
    #     # rank by the POPULATION of each result: list with dictionaries [{}, {}, ...]
    #     city_responses_ranked = sorted(city_responses_raw, key=lambda x: x['population'], reverse=True)
    #
    #     # return list of GameLocation objects
    #     return [GameLocation(city=City(city=x['city'], state=x['state']),
    #                          geolocation=Geolocation(latitude=x['latitude'], longitude=x['longitude']),
    #                          population=x['population']) \
    #             for x in city_responses_ranked]
    ##################