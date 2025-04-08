# Status.tw
from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field


class ChartEnum(StrEnum):
    day = "day"
    week = "week"
    month = "month"


class DataTw(BaseModel):
    name: str
    created_at: datetime = Field(serialization_alias="createdAt")


class VersionTw(BaseModel):
    version: str
    created_at: datetime = Field(serialization_alias="createdAt")


class CountryTw(BaseModel):
    identifier: str
    code: int
    icon_url: str = Field(serialization_alias="iconUrl")


class ClientTw(BaseModel):
    name: str
    country: CountryTw
    score: int
    is_player: bool = Field(serialization_alias="isPlayer")
    is_afk: bool = Field(serialization_alias="isAfk")
    team: int
    created_at: datetime = Field(serialization_alias="createdAt")
    clan: DataTw | None
    server: "ServerTw" = None


class ServerTw(BaseModel):
    ip: str
    port: int
    name: str
    num_clients: int = Field(serialization_alias="numClients")
    num_players: int = Field(serialization_alias="numPlayers")
    max_clients: int = Field(serialization_alias="maxClients")
    max_players: int = Field(serialization_alias="maxPlayers")
    has_password: bool = Field(serialization_alias="hasPassword")
    supports6: bool
    supports7: bool
    created_at: datetime = Field(serialization_alias="createdAt")
    relevance_score: int = Field(serialization_alias="relevanceScore")
    client_score_kind: str | None = Field(serialization_alias="clientScoreKind")
    logo_url: str = Field(serialization_alias="logoUrl")
    map: DataTw
    website: Optional[str] = None
    discord_invite: Optional[str] = Field(None, serialization_alias="discordInvite")
    description: Optional[str] = None
    game_type: DataTw = Field(serialization_alias="gameType")
    version: VersionTw
    clients: list[ClientTw]


class ServerTwOne(BaseModel):
    ip: str
    port: int
    online: ServerTw


class Chart(BaseModel):
    avg_players: float = Field(serialization_alias="avgPlayers")
    max_players: int = Field(serialization_alias="maxPlayers")
    min_players: int = Field(serialization_alias="minPlayers")
    timestamp: datetime


class Charts(BaseModel):
    charts: list[Chart]


class MasterTw(BaseModel):
    servers: list[ServerTw]


class Info(BaseModel):
    app: str
    version: str


class BannedMasterData(BaseModel):
    ip: str
    is_active: bool = Field(serialization_alias="isActive")
    reason: str | None
    unban_date: datetime | None = Field(serialization_alias="unbanDate")
    created_at: datetime = Field(serialization_alias="createdAt")


class BannedMaster(BaseModel):
    servers: list[BannedMasterData]


class ListData(BaseModel):
    name: str
    created_at: datetime = Field(serialization_alias="createdAt")
    servers: list[ServerTw]


class List(BaseModel):
    data: list[ListData]


class ListPlData(BaseModel):
    name: str
    created_at: datetime = Field(serialization_alias="createdAt")
    players: list[ClientTw]


class ListPl(BaseModel):
    data: list[ListPlData]


class Stats(BaseModel):
    num_players: int = Field(serialization_alias="numPlayers")
    num_clans: int = Field(serialization_alias="numClans")
    num_servers: int = Field(serialization_alias="numServers")
    num_maps: int = Field(serialization_alias="numMaps")
    num_game_types: int = Field(serialization_alias="numGameTypes")
    num_versions: int = Field(serialization_alias="numVersions")
