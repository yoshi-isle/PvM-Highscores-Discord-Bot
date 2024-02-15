import discord

NORMIE_ICON = "<:main:1206053914873565266>"
IRON_ICON = "<:ironman:1206051054270029876>"
COOKING_ICON = "<:cooking:1206108579480862730>"
THIEVING_ICON = "<:thieving:1206108085056442378>"
CROWN_ICON = "<:1stplacecrown:1201249547737894972>"
FARMING_ICON = "<:farming:1206108755499024424>"


def get_candyland_embed():
    embed = discord.Embed(title="Candyland (2023)")

    embed.add_field(
        name="",
        value=f"{CROWN_ICON} Impressed, Alchoholic, Helen Feller. Baked, A Cat Dad, Iron Coosa\n\nhttps://discord.com/channels/847313025919746129/847313574040305704/1097535747902423150",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Purple_sweets_detail.png/120px-Purple_sweets_detail.png?41120"
    )
    embed.set_footer(text="April 17th, 2023")
    return embed


def get_snakeandladders_embed():
    embed = discord.Embed(title="Snakes & Ladders (2023)")

    embed.add_field(
        name="",
        value=f"{CROWN_ICON} Lamhirh, Dopamemes, Adaboy23, scarlet x3, Zueskin, Rotting\n\nhttps://discord.com/channels/847313025919746129/847313574040305704/1131088765675380847",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/Ladders.png?b5be8&20150310211136"
    )

    embed.set_footer(text="July 19th, 2023")
    return embed


def get_battleofgods_embed():
    embed = discord.Embed(title="Battle of the Gods (2023)")

    embed.add_field(
        name="",
        value=f"{CROWN_ICON} Lilies, Steals, Bir d, justduff, jalals mane, Fat Cat, silly cowboy, Domimic, VirginRabbi, Shypu, Musei, LunasHowl, XtraIcy\n\nhttps://discord.com/channels/847313025919746129/847313574040305704/1148004422153158666",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Zamorak%27s_statue_%28Slepe%29.png/122px-Zamorak%27s_statue_%28Slepe%29.png?7e7ee"
    )

    embed.set_footer(text="September 3rd, 2023")
    return embed


def get_blackcatbingo_embed():
    embed = discord.Embed(title="Black Cat Halloween Bingo (2023)")

    embed.add_field(
        name="",
        value=f"{CROWN_ICON} nora cat, unrot, cat nya, scarlet x3, Lil Yeeter, Miggy Spoon, Iron Yesu\n\nhttps://discord.com/channels/847313025919746129/847313574040305704/1165755681664667789",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Cat_%28black%29.png/180px-Cat_%28black%29.png?1dfde"
    )

    embed.set_footer(text="October 22nd, 2023")

    return embed


def get_dartboard_embed():
    embed = discord.Embed(title="Zueskin's Dartboard")

    embed.add_field(
        name="",
        value=f"{CROWN_ICON} unrot, nora cat, Rat K ing, Viables, GIM unrot, Lt Kasper, PAWtrol, Bornfury95, Wrldsbstsimp, The Norden\n\nhttps://discord.com/channels/847313025919746129/847313574040305704/1206795998077132810",
        inline=False,
    )

    embed.set_footer(text="February 11th, 2024")

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Target_%28Ranging_Guild%29.png/150px-Target_%28Ranging_Guild%29.png?89891"
    )

    return embed


def get_grandmasters_embed():
    embed = discord.Embed(title="__Grandmaster CA's__")

    embed.add_field(
        name="",
        value="G Fredo\nYoshe",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Ghommal%27s_hilt_6_detail.png/100px-Ghommal%27s_hilt_6_detail.png?ca917"
    )
    return embed


def get_fun_stats():
    embed = discord.Embed(
        title="__Blood Torva Gang__",
    )

    embed.add_field(
        name="",
        value=f"Yoshe\nDopamemes\nEtyl\nCrayy\nunrot\nNot Solstice\nRat K ing\nG Fredo\nCentac",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Ancient_blood_ornament_kit_detail.png/130px-Ancient_blood_ornament_kit_detail.png?4b3c1"
    )

    return embed


def get_clogs():
    embed = discord.Embed(
        title="__Collection Log Slots__",
    )

    embed.add_field(
        name="",
        value=f"{NORMIE_ICON} Etyl - 1,000\n{IRON_ICON} Kainsaw - 868",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Collection_log_detail.png/130px-Collection_log_detail.png?70bda"
    )

    return embed


def get_grandmasters_embed():
    embed = discord.Embed(title="__Grandmaster CA's__")

    embed.add_field(
        name="",
        value="G Fredo\nYoshe",
        inline=False,
    )

    embed.set_thumbnail(url="https://oldschool.runescape.wiki/images/thumb/Ghommal%27s_hilt_6_detail.png/100px-Ghommal%27s_hilt_6_detail.png?ca917")
    return embed


def get_fun_stats():
    embed = discord.Embed(
        title="__Blood Torva Gang__",
    )

    embed.add_field(
        name="",
        value=f"Yoshe\nDopamemes\nEtyl\nCrayy\nunrot\nNot Solstice\nRat K ing\nG Fredo\nCentac",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Ancient_blood_ornament_kit_detail.png/130px-Ancient_blood_ornament_kit_detail.png?4b3c1"
    )

    return embed


def get_200ms():
    embed = discord.Embed(
        title="__200M in a skill__",
    )

    embed.add_field(
        name="",
        value=f"Devvy uwu {THIEVING_ICON}\nKainsaw {COOKING_ICON}\nMusei {FARMING_ICON}",
        inline=False,
    )

    embed.set_thumbnail(url="https://oldschool.runescape.wiki/images/thumb/Max_cape_detail.png/155px-Max_cape_detail.png?4f67e")

    return embed


def get_clogs():
    embed = discord.Embed(
        title="__Collection Log Slots__",
    )

    embed.add_field(
        name="",
        value=f"{NORMIE_ICON} Etyl - 1,000\n{IRON_ICON} Kainsaw - 868",
        inline=False,
    )

    embed.set_thumbnail(url="https://oldschool.runescape.wiki/images/thumb/Collection_log_detail.png/130px-Collection_log_detail.png?70bda")

    return embed
