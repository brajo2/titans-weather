from typing import List

"""
Venues are where games are played
So a game has-a venue
----------------

Name,Capacity,Location,Surface,Roof Type,Team(s),Opened,Geo
Acrisure Stadium,68400,"Pittsburgh, Pennsylvania",Kentucky bluegrass,Open,Pittsburgh Steelers,2001,"40.446667,�-80.015833"
"""


class Venue:
    def __init__(self, name, capacity, location, surface, roof_type, teams, opened, geo):
        self.name = name
        self.capacity = capacity
        self.location = location
        self.surface = surface
        self.roof_type = roof_type
        self.teams = teams
        self.opened = opened
        self.geo = geo

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


"""
Season,Week,Game_Date,Start_Time,Start_Time_GMT_Offset,Game_Site,Home_Team,Home_Team_Final_Score,Visit_Team,Visit_Team_Final_Score
2021,1,9/9/2021,20:20,-5,Tampa Bay,Tampa Bay Buccaneers,31,Dallas Cowboys,29

I'm making a "game" class object to store this game's data in a more structured way
then I will be able to add the weather data to the game object once we request it
"""


class Game:
    def __init__(self, season, week, game_date, start_time, start_time_gmt_offset, game_site, home_team,
                 home_team_final_score, visit_team, visit_team_final_score,
                 venue=None):
        self.season = season
        self.week = week
        self.game_date = game_date
        self.start_time = start_time
        self.start_time_gmt_offset = start_time_gmt_offset
        self.game_site = game_site
        self.home_team = home_team
        self.home_team_final_score = home_team_final_score
        self.visit_team = visit_team
        self.visit_team_final_score = visit_team_final_score
        self.weather = None
        self.venue = venue

    def __str__(self):
        return f"{self.season} {self.week} {self.game_date} {self.start_time} {self.start_time_gmt_offset} {self.game_site} {self.home_team} {self.home_team_final_score} {self.visit_team} {self.visit_team_final_score}"

    def __repr__(self):
        return f"{self.season} {self.week} {self.game_date} {self.start_time} {self.start_time_gmt_offset} {self.game_site} {self.home_team} {self.home_team_final_score} {self.visit_team} {self.visit_team_final_score}"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def set_venue(self, venues: List[Venue]):
        if self.game_site in venues:
            self.venue = venues[self.game_site]
        else:
            print(f"No venue found for {self.game_site}")
