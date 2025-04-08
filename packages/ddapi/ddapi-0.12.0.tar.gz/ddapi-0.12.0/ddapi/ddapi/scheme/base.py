from typing import Optional

from pydantic import BaseModel, Field

from ddapi import DData


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
