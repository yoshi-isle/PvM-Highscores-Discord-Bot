import random
from management.constants.emojis import Emojis
from typing import List

async def get_emoji(emoji_list: List) -> str:
    lower_bound = 0
    upper_bound = len(emoji_list)
    return emoji_list[random.SystemRandom().randint(lower_bound, upper_bound)]

async def get_random_drop_emoji() -> str:
    return get_emoji(Emojis.drop_emojis)

async def get_random_floof_emoji() -> str:
    return get_emoji(Emojis.drop_emojis)

async def get_random_achievement_emoji() -> str:
    return get_emoji(Emojis.achievement_emojis)