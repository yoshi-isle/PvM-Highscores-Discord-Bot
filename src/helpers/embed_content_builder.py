def build_embed_content(data, number_of_placements):
    """
    Builds formatted embed content from player data, showing top placements. Assumes data is sorted
    """

    top_placements = data[:number_of_placements] 
    return "\n".join(
        f"{placement_emoji[place]} {player['osrsUsername']} - {player['pb']}"
        for place, player in enumerate(top_placements)
    )

placement_emoji = {
    0: ":first_place:",
    1: ":second_place:",
    2: ":third_place:",
}