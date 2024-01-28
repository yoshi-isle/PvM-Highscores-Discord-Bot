import constants.boss_info as boss_info
from constants.channels import ChannelIds
from hall_of_fame.services import embed_generator_service


async def update_boss_highscores(self):
    self.logger.info(f"Updating boss highscores")

    highscores_channel = self.bot.get_channel(ChannelIds.boss_pbs)

    self.logger.info(f"Getting all messages in boss highscores channel")

    messages = [
        message
        async for message in highscores_channel.history(limit=200, oldest_first=True)
        if len(message.embeds) != 0
    ]

    self.logger.info(f"Got {len(messages)} messages with embeds")

    data = await self.database.get_personal_bests()

    for m in range(len(messages)):
        self.logger.info(f"Updating message")
        newembeds = []

        for boss in boss_info.BOSS_INFO[m]:
            newembeds.append(
                await embed_generator_service.generate_pb_embed(
                    data,
                    boss["boss_name"],
                    number_of_placements=3,
                )
            )
        await messages[m].edit(embeds=newembeds)
