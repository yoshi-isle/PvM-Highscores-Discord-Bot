from summerland.constants.tiles import BINGO_TILES


class TeamInfo:
    def __init__(self, team) -> None:
        print(team)
        self.team_number = team["team_number"]
        self.team_name = team["team_name"]
        self.channel_id = team["channel_id"],
        self.team_members = team["team_members"],
        self.current_tile = team["current_tile"]
        self.last_reroll = team["last_reroll"],
        self.tile_history = team["tile_history"],
        self.tile = BINGO_TILES[int(self.current_tile)]