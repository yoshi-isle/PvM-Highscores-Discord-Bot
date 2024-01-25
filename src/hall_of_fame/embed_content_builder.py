from hall_of_fame.time_helpers import convert_pb_to_display_format
import datetime

PLACEMENT_EMOJI = {
    1: ":first_place:",
    2: ":second_place:",
    3: ":third_place:",
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
        pb = await convert_pb_to_display_format(
            datetime.time.fromisoformat(data[i]["pb"])
        )
        print(pb)
        emoji = PLACEMENT_EMOJI[current_placement]
        username = data[i]["osrs_username"]

        if current_placement > number_of_placements:
            return embed_content
        embed_content += f"{emoji} {username} - {pb}\n"
        if i != len(data) - 1:
            # If the next pb is slower, we can increase the placement for the next insert
            if data[i + 1]["pb"] > data[i]["pb"]:
                current_placement = current_placement + 1

    return embed_content
