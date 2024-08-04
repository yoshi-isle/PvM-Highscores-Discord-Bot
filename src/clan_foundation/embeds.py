import datetime
from summerland.constants.tiles import BINGO_TILES
from summerland.constants.team_icon_emojis import TEAM_ICON_EMOJIS
from discord import Embed

"""
Static Embeds. Used for instructional purposes and take no inputs
"""
async def draw_clan_foundation_embed():
    embed = Embed(title="",
                      url="",
                      timestamp=datetime.datetime.now())

    embed.add_field(name="Welcome",
                    value="Welcome to kittycord. \nWe are an OSRS clan (some fluff to make us sound cool) \nThis is our purrmemnent invite link: discord.gg/kittycats\n\nWant to submit points for your rank? Go here: https://discord.com/channels/1197595466657968158/1269456876026990612",
                    inline=False)

    embed.set_image(url="https://i.imgur.com/RT1AlJj.png")

    return embed

async def draw_clan_rules_embed():
    embed = Embed(
        title="Clan Rulebook",
        description="""**__General__**\n```• Change your Discord nickname to match your RSN or put in your bio so we know who you are!\n• We are an English-speaking server\n• Be kind to everyone.\n• No gear shaming or showing toxicity towards goals\n• No selfies. Other IRL stuff is fine just keep it within the rules\n• Avoid political arguments\n• Please hide from the clan channel if deathmatching as we don't promote gambling
                    ```\n__**Absolutely NO tolerance for the following:**__\n```ansi\n• Harassing other clanmates\n• Malicious links, scamming, doxing\n• Begging for gear loans/GP\n• Advertisement of non-Jagex ToS OSRS services\n• NSFW\n• Racism/hate speech```
                    \nAbove all else, have fun and enjoy your time in the clan!""",
        colour=0xAD0000,
    )

    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Journal_%28Horror_from_the_Deep%29_detail.png/130px-Journal_%28Horror_from_the_Deep%29_detail.png?0752e"
    )

    return embed

async def draw_staff_embed():
    embed = Embed()
    embed.add_field(name="Staff Members",
                value="Kanao - @kittycats.\nTanjiro - @yoshe_\nAdaboy23 - @adaboy23")
    embed.add_field(name="Chat Moderators",
                value="G Fredo - @pira\nZezima - @zezimaRS\n")
    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/thumb/Journal_%28Horror_from_the_Deep%29_detail.png/130px-Journal_%28Horror_from_the_Deep%29_detail.png?0752e"
    )

    return embed





async def draw_clan_profile_embed():
    embed = Embed(title="Tanjiro's Clan Profile",
                      url="https://wiseoldman.net/players/tanjiro",
                      colour=0x7195a8,
                      timestamp=datetime.datetime.now())

    embed.add_field(name="",
                    value="**Joined:** Mar 2021\n**Rank:** Deputy Owner\n**Total pts:** 42\n\nNext rankup at: 60 (+18 points)",
                    inline=False)
    embed.add_field(name="__Points Breakdown__",
                    value="(5) Legacy\n(20) Event\n(6) Split\n(10) Assist",
                    inline=False)

    embed.set_image(url="https://oldschool.runescape.wiki/images/Clan_icon_-_Deputy_owner.png?b0561")

    embed.set_thumbnail(url="https://wallpapers-clan.com/wp-content/uploads/2022/02/demon-slayer-tanjiro-pfp-2.jpg")

    return embed
    