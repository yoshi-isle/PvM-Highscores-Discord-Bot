def build(data, num_placements):
    embed_content = ""
    for i in range(min(num_placements, len(data))):
        player_data = data[i]
        embed_content += f"{placement_emoji[i]} {player_data['osrsUsername']} - {player_data['pb']}\n"
    return embed_content

placement_emoji = {
    0: ":first_place:",
    1: ":second_place:",
    2: ":third_place:",
}