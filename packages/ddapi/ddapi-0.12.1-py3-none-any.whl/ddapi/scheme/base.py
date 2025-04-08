from typing import Optional

from pydantic import BaseModel, Field


class DRank(BaseModel):
    points: Optional[int] = None
    rank: Optional[int] = None


class DPoints(BaseModel):
    total: int
    points: Optional[int] = Field(default=None)
    rank: Optional[int] = Field(default=None)


class DData(BaseModel):
    points: Optional[DPoints] = Field(default=None)
    team_rank: Optional[DRank] = Field(default=None)
    rank: Optional[DRank] = Field(default=None)
    maps: Optional[dict] = Field(default=None)


class DDType(BaseModel):
    Novice: Optional[DData] = None
    Moderate: Optional[DData] = None
    Brutal: Optional[DData] = None
    Insane: Optional[DData] = None
    Dummy: Optional[DData] = None
    DDmaX_Easy: Optional[DData] = Field(default=None, validation_alias="DDmaX.Easy")
    DDmaX_Next: Optional[DData] = Field(default=None, validation_alias="DDmaX.Next")
    DDmaX_Nut: Optional[DData] = Field(default=None, validation_alias="DDmaX.Nut")
    DDmaX_Pro: Optional[DData] = Field(default=None, validation_alias="DDmaX.Pro")
    Oldschool: Optional[DData] = Field(default=None)
    Race: Optional[DData] = None
    Solo: Optional[DData] = None
    total: Optional[DData] = None
