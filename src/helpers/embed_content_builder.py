def build_embed_content(data, number_of_placements):
    """
    Builds formatted embed content from player data for bosses, showing top placements. Assumes data is sorted
    """
    embed_content = ""
    current_placement = 1
    for i in range(len(data)):
        if current_placement > number_of_placements:
            return embed_content
        embed_content += f"{placement_emoji[current_placement]} {data[i]['osrsUsername']} - {data[i]['pb']}\n"
        if i != len(data) - 1:
            # If the next pb is slower, we can increase the placement for the next insert
            if data[i + 1]["pb"] > data[i]["pb"]:
                current_placement = current_placement + 1

    return embed_content


placement_emoji = {
    1: ":first_place:",
    2: ":second_place:",
    3: ":third_place:",
    4: "",
    5: "",
}
