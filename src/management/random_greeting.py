import random

from management.constants.greetings import Greetings


async def get_random_greeting_url() -> str:
    greeting_rarity = random.SystemRandom().randint(1, 100)

    lower_bound = 0
    if greeting_rarity % 100 == 0:
        upper_bound = len(Greetings.rare_urls) - 1
        return Greetings.rare_urls[random.SystemRandom().randint(lower_bound, upper_bound)]
    elif greeting_rarity % 5 == 0:
        upper_bound = len(Greetings.uncommon_urls) - 1
        return Greetings.uncommon_urls[random.SystemRandom().randint(lower_bound, upper_bound)]
    else:
        upper_bound = len(Greetings.common_urls) - 1
        return Greetings.common_urls[random.SystemRandom().randint(lower_bound, upper_bound)]
