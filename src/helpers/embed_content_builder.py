def build_boss_embed_content(data, number_of_placements):
    """
    Builds formatted embed content from player data for bosses, showing top placements. Assumes data is sorted
    """
    embed_content = ""
    current_placement = 1
    for i in range(len(data)):
        embed_content += f"{placement_emoji[current_placement]} {data[i]['osrsUsername']} - {data[i]['pb']}\n"
        if i != len(data):
            # If the next pb is slower, we can increase the placement for the next insert
            if data[i + 1]["pb"] > data[i]["pb"]:
                current_placement = current_placement + 1
                # Line break
                embed_content += f"\n"

        if current_placement > number_of_placements:
            return embed_content

    return embed_content


def build_raid_embed_content(data, number_of_placements, category):
    """
    Builds formatted embed content from player data for raids, showing top placements. Assumes data is sorted
    """
    filtered_data = (result for result in data if result["groupSize"] == category)
    top_placements = list(filtered_data)[:number_of_placements]
    return "\n".join(
        f"{placement_emoji[place]} {player['osrsUsername']} - {player['pb']}"
        for place, player in enumerate(top_placements)
    )


placement_emoji = {
    1: ":first_place:",
    2: ":second_place:",
    3: ":third_place:",
    4: "::",
    5: "::",
    6: ":55",
}
