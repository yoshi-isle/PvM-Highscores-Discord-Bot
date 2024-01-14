def build_boss_embed_content(data, number_of_placements):
    """
    Builds formatted embed content from player data for bosses, showing top placements. Assumes data is sorted
    """

    top_placements = data[:number_of_placements] 
    return "\n".join(
        f"{placement_emoji[place]} {player['osrsUsername']} - {player['pb']}"
        for place, player in enumerate(top_placements)
    )

def build_raid_embed_content(data, number_of_placements, category):
  """
  Builds formatted embed content from player data for raids, showing top placements. Assumes data is sorted
  """
  filtered_data = (result for result in data if result["groupSize"] == category)
  return "\n".join(
      f"{placement_emoji[place]} {player['osrsUsername']} - {player['pb']}"
      for place, player in enumerate(filtered_data)
  )

placement_emoji = {
  0: ":first_place:",
  1: ":second_place:",
  2: ":third_place:",
}