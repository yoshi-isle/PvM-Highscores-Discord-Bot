import wom

KITTY_GROUP_ID: int = 1165

class WiseOldManClient:
    async def __init__(self) -> None:
        self.client = wom.Client()
        await self.client.start()

    async def _disconnect(self):
        await self.client.close()

    async def get_hiscores(self, metric: str, group_id: int = KITTY_GROUP_ID, number_of_ranks: int = 3):
        return await self.client.groups.get_hiscores(id=group_id, metric=metric, limit=number_of_ranks)



    

