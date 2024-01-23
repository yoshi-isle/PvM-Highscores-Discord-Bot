import time
import uuid
from dataclasses import dataclass


@dataclass(frozen=False)
class PersonalBest:
    id: uuid
    boss: str
    pb: float
    discord_cdn_url: str
    date_achieved: time
    osrs_username: str
    discord_username: str
    approved: bool
