# import constants.boss_info as boss_info
from constants.channels import ChannelIds
from hall_of_fame import embed_generator
import hall_of_fame.constants.personal_best as personal_best
from datetime import datetime
import uuid
from enum import Enum


async def update_boss_highscores(self, channel_id, activity_data):
    highscores_channel = self.bot.get_channel(channel_id)

    messages = [
        message
        async for message in highscores_channel.history(limit=200, oldest_first=True)
        if len(message.embeds) != 0
    ]

    data = await self.database.get_personal_bests()

    for m in range(len(messages)):
        newembeds = []

        for boss in activity_data.INFO[m]:
            newembeds.append(
                await embed_generator.generate_pb_embed(
                    data,
                    boss["boss_name"],
                    number_of_placements=3,
                )
            )
        await messages[m].edit(embeds=newembeds)
