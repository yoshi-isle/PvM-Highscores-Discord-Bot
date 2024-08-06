import discord
from static_embed.constants.player_names import PlayerNames

NORMIE_ICON = "<:main:1206053914873565266>"
IRON_ICON = "<:ironman:1207739589784113182>"
COOKING_ICON = "<:cooking:1206108579480862730>"
THIEVING_ICON = "<:thieving:1206108085056442378>"
CROWN_ICON = "<:1stplacecrown:1201249547737894972>"
SECONDPLACECROWN_ICON = "<:2ndplacecrown:1201249561423917248>"
THIRDPLACECROWN_ICON = "<:3rdplacecrown:1201249572664643664>"
FARMING_ICON = "<:farming:1206108755499024424>"


def get_candyland_embed():
    embed = discord.Embed(title="Candyland (2023)")

    embed.add_field(
        name="",
        value=", ".join(
            [
                CROWN_ICON + " " + PlayerNames.impressed,
                PlayerNames.kirby,
                PlayerNames.helen_feller,
                PlayerNames.baked,
                PlayerNames.cat_dad,
                PlayerNames.iron_coosa,
            ]
        ),
        inline=False,
    )
    embed.add_field(
        name="",
        value="https://discord.com/channels/847313025919746129/847313574040305704/1097535747902423150\n",
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
        value=", ".join(
            [
                CROWN_ICON + " " + PlayerNames.lamhirh,
                PlayerNames.dopamemes,
                PlayerNames.adaboy,
                PlayerNames.scarlet_cat,
                PlayerNames.zueskin,
                PlayerNames.rotting,
            ]
        ),
        inline=False,
    )

    embed.add_field(
        name="",
        value="https://discord.com/channels/847313025919746129/847313574040305704/1131088765675380847\n",
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
        value=", ".join(
            [
                CROWN_ICON + " " + PlayerNames.lilies,
                PlayerNames.steals,
                PlayerNames.bird,
                PlayerNames.justduff,
                PlayerNames.jalal_mane,
                PlayerNames.fat_cat,
                PlayerNames.silly_cowboy,
                PlayerNames.domimic,
                PlayerNames.virgin_rabbit,
                PlayerNames.shypu,
                PlayerNames.musei,
                PlayerNames.lunas_howl,
                PlayerNames.xtra_icy,
            ]
        ),
        inline=False,
    )

    embed.add_field(
        name="",
        value="https://discord.com/channels/847313025919746129/847313574040305704/1148004422153158666\n",
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
        value=", ".join(
            [
                CROWN_ICON + " " + PlayerNames.nora_cat,
                PlayerNames.unrot,
                PlayerNames.neko,
                PlayerNames.scarlet_cat,
                PlayerNames.lil_yeeter,
                PlayerNames.miggy_spoon,
                PlayerNames.iron_yesu,
            ]
        ),
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Cat_%28black%29.png/180px-Cat_%28black%29.png?1dfde"
    )

    embed.add_field(
        name="",
        value="https://discord.com/channels/847313025919746129/847313574040305704/1165755681664667789\n",
    )

    embed.set_footer(text="October 22nd, 2023")

    return embed


def get_dartboard_embed():
    embed = discord.Embed(title="Zueskin's Dartboard")

    embed.add_field(
        name="",
        value=", ".join(
            [
                CROWN_ICON + " " + PlayerNames.unrot,
                PlayerNames.nora_cat,
                PlayerNames.rat_king,
                PlayerNames.viables,
                PlayerNames.gerg,
                PlayerNames.lt_kasper,
                PlayerNames.pawtrol,
                PlayerNames.bornfury95,
                PlayerNames.wrldsbestsmp,
                PlayerNames.norden,
            ]
        ),
        inline=False,
    )

    embed.set_footer(text="February 11th, 2024")

    embed.add_field(
        name="",
        value="https://discord.com/channels/847313025919746129/847313574040305704/1206795998077132810\n",
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Target_%28Ranging_Guild%29.png/150px-Target_%28Ranging_Guild%29.png?89891"
    )

    return embed

def get_summerland_embed():
    embed = discord.Embed(title="Summerland Bingo")

    embed.add_field(
        name="",
        value=", ".join(
            [
                CROWN_ICON + " " + PlayerNames.radhard,
                PlayerNames.luckyzh,
                PlayerNames.natoh,
                PlayerNames.centac,
                PlayerNames.radsoft,
                PlayerNames.eboji,
                PlayerNames.zezimaspimp,
                PlayerNames.pup_in_a_cup,
                PlayerNames.auzty,
                PlayerNames.inri,
                PlayerNames.lindsey,
            ]
        ),
        inline=False,
    )

    embed.set_footer(text="June 1st, 2024")

    embed.add_field(
        name="",
        value="https://discord.com/channels/847313025919746129/847313574040305704/1253131324483567698\n",
    )

    embed.set_thumbnail(
        url="https://i.imgur.com/RT1AlJj.png"
    )

    return embed

def get_grandmasters_embed():
    embed = discord.Embed(title="__Grandmaster CA's__")

    embed.add_field(
        name="",
        value="\n".join(
            [
                PlayerNames.yoshe,
                PlayerNames.g_fredo,
                PlayerNames.kam,
                PlayerNames.dopamemes,
                "kitty weedXD",
                "charlie du"
            ]
        ),
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/Tzkal_slayer_helmet_chathead.png?ee6a6"
    )
    return embed


def get_fun_stats():
    embed = discord.Embed(
        title="__Blood Torva Gang__",
    )

    embed.add_field(
        name="",
        value="\n".join(
            [
                PlayerNames.yoshe,
                PlayerNames.dopamemes,
                PlayerNames.crayy,
                PlayerNames.rat_king,
                PlayerNames.g_fredo,
                PlayerNames.kam,
                PlayerNames.cats_go_nya,
                PlayerNames.katgirlz,
                PlayerNames.norden,
                PlayerNames.neko,
                PlayerNames.flowers,
                "kitty weedXD",
                "charlie du"
            ]
        ),
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Ancient_blood_ornament_kit_detail.png/130px-Ancient_blood_ornament_kit_detail.png?4b3c1"
    )

    return embed


def get_clogs():
    embed = discord.Embed(
        title="__High Collection Log Slots__",
    )

    embed.add_field(
        name="",
        value=f"{IRON_ICON} {PlayerNames.kainsaw} - 939+",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Collection_log_detail.png/130px-Collection_log_detail.png?70bda"
    )

    return embed


def get_200ms():
    embed = discord.Embed(
        title="__200M in a skill__",
    )

    embed.add_field(
        name="",
        value=f"{PlayerNames.devvy_uwu} {THIEVING_ICON}\n{PlayerNames.kainsaw} {COOKING_ICON}\n{PlayerNames.musei} {FARMING_ICON}",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Max_cape_detail.png/155px-Max_cape_detail.png?4f67e"
    )

    return embed


def get_tears():
    embed = discord.Embed(
        title="__Tears of Guthix (Most pts/game)__",
    )

    embed.add_field(
        name="",
        value=f"{CROWN_ICON} {PlayerNames.adaboy} - 259 Tears\n{SECONDPLACECROWN_ICON} SARPBC - 254 Tears\n{THIRDPLACECROWN_ICON} {PlayerNames.crayy} - 246 Tears",
        inline=False,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Juna.png/200px-Juna.png?90de6"
    )

    return embed
