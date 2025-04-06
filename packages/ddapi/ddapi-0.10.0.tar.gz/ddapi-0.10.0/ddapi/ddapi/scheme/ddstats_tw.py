# ddstats.tw
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

rm_list = ["DD-Persian", "/vDQMHSss8W", '']


class PData(BaseModel):
    rank: int
    points: int


class PPoints(BaseModel):
    Novice: Optional[PData] = None
    Moderate: Optional[PData] = None
    Brutal: Optional[PData] = None
    Insane: Optional[PData] = None
    Dummy: Optional[PData] = None
    DDmaX_Easy: Optional[PData] = Field(default=None, validation_alias='DDmaX.Easy')
    DDmaX_Next: Optional[PData] = Field(default=None, validation_alias='DDmaX.Next')
    DDmaX_Nut: Optional[PData] = Field(default=None, validation_alias='DDmaX.Nut')
    DDmaX_Pro: Optional[PData] = Field(default=None, validation_alias='DDmaX.Pro')
    Oldschool: Optional[PData] = None
    Race: Optional[PData] = None
    Solo: Optional[PData] = None
    total: Optional[PData] = None


class PointG(BaseModel):
    date: str
    points: int
    rank_points: int
    team_points: int


class Profile(BaseModel):
    name: str
    points: int
    clan: Optional[str]
    country: Optional[int]
    skin_name: Optional[str]
    skin_color_body: Optional[int] = None
    skin_color_feet: Optional[int] = None


class DProfile(BaseModel):
    profile: Profile


class DDMap(BaseModel):
    map: str
    server: str
    points: int
    stars: int
    mapper: str
    timestamp: Optional[datetime] = None


class RecentFinishes(BaseModel):
    map: DDMap
    time: float
    timestamp: datetime
    server: str
    cp1: float
    cp2: float
    cp3: float
    cp4: float
    cp5: float
    cp6: float
    cp7: float
    cp8: float
    cp9: float
    cp10: float
    cp11: float
    cp12: float
    cp13: float
    cp14: float
    cp15: float
    cp16: float
    cp17: float
    cp18: float
    cp19: float
    cp20: float
    cp21: float
    cp22: float
    cp23: float
    cp24: float
    cp25: float


class FavouriteTeammates(BaseModel):
    name: str
    ranks_together: int


class Finishes(BaseModel):
    map: DDMap
    name: str
    time: float
    timestamp: Optional[datetime]
    server: str
    rank: int
    team_rank: Optional[int] = None
    seconds_played: Optional[int] = None


class UnfinishedMap(BaseModel):
    map: DDMap
    finishes: int
    finishes_rank: Optional[int] = None
    median_time: Optional[float] = None


class Points(BaseModel):
    weekly_points: Optional[PData] = None
    monthly_points: Optional[PData] = None
    yearly_points: Optional[PData] = None
    points: PPoints
    rank_points: PPoints
    team_points: PPoints


class RecentActivity(BaseModel):
    name: str
    date: str
    map_name: str
    map: DDMap | None = Field(default=None)
    seconds_played: int


class RecentPlayerInfo(BaseModel):
    name: str
    clan: str
    country: int
    skin_name: Optional[str] = None
    skin_color_body: Optional[int] = None
    skin_color_feet: Optional[int] = None
    last_seen: str
    seconds_played: int


class MostPlayedMaps(BaseModel):
    map_name: str
    seconds_played: int
    map: Optional[DDMap] = None


class MostPlayed(BaseModel):
    key: str
    seconds_played: int


class PlaytimePerMonth(BaseModel):
    year_month: str
    month: str
    seconds_played: int


class FavouriteRank1sTeammates(BaseModel):
    name: str
    ranks_together: int


class AllTop10s(BaseModel):
    map: DDMap
    name: str
    time: float
    rank: int
    team_rank: int | None = None
    team_time: float | None = None


class RecentTop10s(BaseModel):
    rank_type: str
    map: str
    time: float
    rank: int
    timestamp: Optional[datetime] = None
    server: str


class GeneralActivity(BaseModel):
    total_seconds_played: int
    start_of_playtime: datetime
    average_seconds_played: int


class Player(BaseModel):
    points_graph: list[PointG]
    recent_finishes: list[RecentFinishes]
    favourite_teammates: Optional[list[FavouriteTeammates]] = None
    profile: Profile
    is_mapper: bool
    finishes: list[Finishes]
    unfinished_maps: Optional[list[UnfinishedMap]] = None
    points: Points
    recent_activity: Optional[list[RecentActivity]] = None
    recent_player_info: Optional[list[RecentPlayerInfo]] = None
    most_played_maps: Optional[list[MostPlayedMaps]] = None
    most_played_gametypes: Optional[list[MostPlayed]] = None
    most_played_categories: Optional[list[MostPlayed]] = None
    most_played_locations: Optional[list[MostPlayed]] = None
    playtime_per_month: list[PlaytimePerMonth]
    general_activity: Optional[GeneralActivity] = None
    favourite_rank1s_teammates: Optional[list[FavouriteRank1sTeammates]] = None
    all_top_10s: Optional[list[AllTop10s]] = None
    recent_top_10s: Optional[list[RecentTop10s]] = None


class Maps(BaseModel):
    maps: list[DDMap]


class InfoSMap(BaseModel):
    map: DDMap
    finishes: int
    finishes_rank: int
    median_time: float


class RankingSMap(BaseModel):
    rank: int
    timestamp: Optional[datetime] = None
    name: str
    time: float
    map: str
    server: str


class TeamRankingSMap(BaseModel):
    rank: int
    timestamp: Optional[datetime] = None
    id: list[int]
    players: list[str]
    time: float
    map: str
    server: str


class TimeCpsSMap(BaseModel):
    name: str
    cp1: float
    cp2: float
    cp3: float
    cp4: float
    cp5: float
    cp6: float
    cp7: float
    cp8: float
    cp9: float
    cp10: float
    cp11: float
    cp12: float
    cp13: float
    cp14: float
    cp15: float
    cp16: float
    cp17: float
    cp18: float
    cp19: float
    cp20: float
    cp21: float
    cp22: float
    cp23: float
    cp24: float
    cp25: float
    time: float


class PlaytimeSMap(BaseModel):
    name: str
    seconds_played: int


class SMap(BaseModel):
    info: InfoSMap
    rankings: list[RankingSMap]
    team_rankings: list[TeamRankingSMap]
    time_cps: list[TimeCpsSMap]
    playtime: list[PlaytimeSMap]
