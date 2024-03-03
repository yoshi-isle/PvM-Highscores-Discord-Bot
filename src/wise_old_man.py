import logging
from typing import List, Tuple

import wom

from settings import get_environment_variable

KITTY_GROUP_ID: int = 1165


class WiseOldManClient:
    def __init__(self) -> None:
        wom_token = get_environment_variable("WOM_TOKEN")
        self.client = wom.Client(wom_token)
        self.logger = logging.getLogger("discord")

    async def _connect(self) -> None:
        await self.client.start()

    async def _disconnect(self) -> None:
        await self.client.close()

    async def get_top_placements_players(self, players: List[wom.GroupHiscoresEntry], placements: int = 1) -> Tuple[List[wom.Player], List[wom.Player]]:
        top_placements_normal_players = [player for player in players if player.player.type == wom.PlayerType.Regular][:placements]
        top_placements_iron_players = [
            player
            for player in players
            if player.player.type
            in (
                wom.PlayerType.Ironman,
                wom.PlayerType.Hardcore,
                wom.PlayerType.Ultimate,
            )
        ][:placements]
        return top_placements_normal_players, top_placements_iron_players

    async def get_top_placements_hiscores(
        self,
        metric: wom.Metric,
        group_id: int = KITTY_GROUP_ID,
        number_of_ranks: int = 30,
        placements: int = 1,
    ) -> Tuple[List[wom.Player], List[wom.Player]]:
        result = await self.client.groups.get_hiscores(id=group_id, metric=metric, limit=number_of_ranks)
        if result.is_ok:
            return await self.get_top_placements_players(players=result.unwrap(), placements=placements)
        else:
            self.logger.critical("WOM error: %s" % result.unwrap_err)

        return [], []
