import wom
from typing import List, Tuple

KITTY_GROUP_ID: int = 1165

class WiseOldManClient:
    async def __init__(self) -> None:
        self.client = wom.Client()
        await self.client.start()

    async def _disconnect(self) -> None:
        await self.client.close()

    async def get_top_placements_players(self, players: List[wom.GroupHiscoresEntry], placements:int = 3) -> Tuple[List[wom.Player], List[wom.Player]]:
        top_placements_normal_players =  [value for value in players if value.player.type == wom.PlayerType.Regular][:placements]
        top_placements_iron_players = [value for value in players if value.player.type in (wom.PlayerType.Ironman, wom.PlayerType.Hardcore, wom.PlayerType.Ultimate)][:placements]
        return  top_placements_normal_players, top_placements_iron_players

    async def get_top_placements_hiscores(self, metric: wom.Metric, group_id: int = KITTY_GROUP_ID, number_of_ranks: int = 20, placements: int = 3)-> Tuple[List[wom.Player], List[wom.Player]]:
        result = await self.client.groups.get_hiscores(id=group_id, metric=metric, limit=number_of_ranks)
        if result.is_ok:
            return await self.get_top_placements_players(players=result.unwrap(), placements=placements)
        return [], []
