import uuid
import time
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class PersonalBest:
        id: uuid
        boss: str
        pb: time
        discord_cdn_url: str
        date_achieved: time
        osrs_username: str
        discord_username: str
        approved: bool

class PersonalBestManager:
    """
    Interface to PersonalBest for setting and getting.
    """
    def __init__(self):
        self.pb_list = {}

    def load_pbs(self, pb_list: List[PersonalBest]):
        for pb_info in pb_list:
            pb = PersonalBest(**pb_info)
            self.add_pb(pb)

    def add_pb(self, pb: PersonalBest):
        self.pb_list[pb.task_number] = pb

    def get_pb(self, boss_name: str, osrs_username: str) -> PersonalBest:
        return self.tasks.get(boss_name, osrs_username, None)
