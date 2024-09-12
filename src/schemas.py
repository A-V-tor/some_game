from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BoostBase(BaseModel):
    id: int
    type: str
    player_id: int

    class Config:
        from_attributes = True


class PrizeBase(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class LevelPrizeBase(BaseModel):
    id: int
    received: datetime
    level_id: int
    prize_id: int
    prize: PrizeBase

    class Config:
        from_attributes = True


class LevelBase(BaseModel):
    id: int
    title: str
    order: int
    level_prizes: list[LevelPrizeBase] | None

    class Config:
        from_attributes = True


class PlayerLevelBase(BaseModel):
    id: int
    completed: datetime | None = None
    is_completed: bool
    score: int
    player_id: int
    level_id: int
    level: LevelBase

    class Config:
        from_attributes = True


class PlayerSchema(BaseModel):
    id: int
    player_id: str
    last_visit: datetime
    first_visit: datetime
    is_daily_visit: bool

    player_levels: list[PlayerLevelBase]
    boosts: list[BoostBase]

    class Config:
        from_attributes = True


class LevelCompleteRequest(BaseModel):
    player_id: str
    order: int
    score: int
