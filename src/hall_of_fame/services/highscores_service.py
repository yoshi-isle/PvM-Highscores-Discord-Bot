from hall_of_fame.hall_of_fame_cog import HallOfFame
from constants.channels import ChannelIds
import constants.boss_info as boss_info
import embed_generator

async def update_boss_highscores(self: HallOfFame):
    
    highscores_channel = self.bot.get_channel(ChannelIds.boss_pbs)

    messages = [
        message
        async for message in highscores_channel.history(
            limit=200, oldest_first=True
        )
    ]

    data = await self.database.get_personal_bests()

    for m in range(len(messages)):

        newembeds = []

        for boss in boss_info.BOSS_INFO[m]:
            newembeds.append(
                await embed_generator.generate_pb_embed(
                    data,
                    boss["boss_name"],
                    number_of_placements=3,
                )
            )
        await messages[m].edit(embeds=newembeds)