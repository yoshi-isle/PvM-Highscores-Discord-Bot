import uuid
import time
from dataclasses import dataclass
from typing import List

@dataclass(frozen=False)
class PersonalBest:
        id: uuid
        boss: str
        pb: time
        discord_cdn_url: str
        date_achieved: time
        osrs_username: str
        discord_username: str
        approved: bool