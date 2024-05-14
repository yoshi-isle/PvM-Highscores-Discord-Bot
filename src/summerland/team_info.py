import summerland.constants.tiles as bingo_tiles


class TeamInfo:
    def __init__(self, team_info):
        # From the db
        self.team_number = team_info["teamNumber"]
        self.channel_id = team_info["channelId"]
        self.team_name = team_info["teamName"]
        self.team_members = team_info["teamMembers"]
        self.tile_number = team_info["currentTile"]
        self.current_progress = team_info["progressCounter"]
        self.tile_history = team_info["tileHistory"]

        # From their position in tiles.py
        current_tile = bingo_tiles.tiles[team_info["currentTile"]]

        self.tile_name = current_tile["Title"]
        self.tile_image = current_tile["ImageUrl"]
        self.quirky_header = current_tile["QuirkyHeader"]
        self.description = current_tile["Description"]
        self.challenge = current_tile["Challenge"]
        self.submissions_required = current_tile["SubmissionsRequired"]

        # Misc
        self.is_partial = current_tile["SubmissionsRequired"] > 1
