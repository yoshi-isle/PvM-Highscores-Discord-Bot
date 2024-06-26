import datetime
from urllib.parse import urljoin, urlparse

from hall_of_fame.time_helpers import convert_pb_to_display_format

PLACEMENT_EMOJI = {
    1: "<:1stplacecrown:1201249547737894972>",
    2: "<:2ndplacecrown:1201249561423917248>",
    3: "<:3rdplacecrown:1201249572664643664>",
    4: "",
    5: "",
}


async def build_embed_content(data, number_of_placements):
    """
    Builds formatted embed content from player data for bosses, showing top placements. Assumes data is sorted
    """
    embed_content = ""
    current_placement = 1

    for i in range(len(data)):
        pb = await convert_pb_to_display_format(datetime.time.fromisoformat(data[i]["pb"]))
        # TODO - move this out
        epoch = round(data[i]["date_achieved"].timestamp())
        disc_dt = f"<t:{epoch}:D>"

        # TODO - clean
        emoji = PLACEMENT_EMOJI[current_placement]
        username = data[i]["osrs_username"]

        url = data[i]["discord_cdn_url"]

        if current_placement > number_of_placements:
            return embed_content
        embed_content += f"{emoji} **{pb}** - {username} - {disc_dt} - [proof]({url})\n"
        if i != len(data) - 1:
            # If the next pb is slower, we can increase the placement for the next insert
            if data[i + 1]["pb"] > data[i]["pb"]:
                current_placement = current_placement + 1

    return embed_content
