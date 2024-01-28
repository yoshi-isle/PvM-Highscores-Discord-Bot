import random

from management.constants.greetings import Greetings


async def get_random_greeting_url() -> str:
    greeting_rarity = random.SystemRandom().randint(1, 20)

    lower_bound = 0
    if greeting_rarity % 20 == 0:
        upper_bound = len(Greetings.rare_urls)
        return Greetings.rare_urls[
            random.SystemRandom().randint(lower_bound, upper_bound)
        ]
    elif greeting_rarity % 5 == 0:
        upper_bound = len(Greetings.uncommon_urls)
        return Greetings.uncommon_urls[
            random.SystemRandom().randint(lower_bound, upper_bound)
        ]
    else:
        upper_bound = len(Greetings.common_urls)
        return Greetings.common_urls[
            random.SystemRandom().randint(lower_bound, upper_bound)
        ]
