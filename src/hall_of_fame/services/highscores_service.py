import constants.forum_data.bosses as bosses
import constants.forum_data.chambers_of_xeric as chambers_of_xeric
import constants.forum_data.dt2bosses as dt2bosses
import constants.forum_data.misc_activities as misc_activities
import constants.forum_data.theatre_of_blood as theatre_of_blood
import constants.forum_data.tombs_of_amascut as tombs_of_amascut
import constants.forum_data.tzhaar as tzhaar
from constants.channels import ChannelIds
from hall_of_fame import embed_generator


async def update_all_pb_highscores(self):
    data = await self.database.get_personal_bests()
    updated_amount = 0

    pb_highscore_channels = [
        self.bot.get_channel(ChannelIds.tob_pbs),
        self.bot.get_channel(ChannelIds.cox_pbs),
        self.bot.get_channel(ChannelIds.toa_pbs),
        self.bot.get_channel(ChannelIds.tzhaar_pbs),
        self.bot.get_channel(ChannelIds.dt2_pbs),
        self.bot.get_channel(ChannelIds.boss_pbs),
        self.bot.get_channel(ChannelIds.misc_pbs),
    ]

    pb_info = [
        theatre_of_blood.INFO,
        chambers_of_xeric.INFO,
        tombs_of_amascut.INFO,
        tzhaar.INFO,
        dt2bosses.INFO,
        bosses.INFO,
        misc_activities.INFO,
    ]

    for channel in range(len(pb_highscore_channels)):
        # This is just in case we have text in those channels
        highscore_message = [
            message
            async for message in pb_highscore_channels[channel].history(
                limit=200, oldest_first=True
            )
            if len(message.embeds) != 0
        ]
        highscore_message = highscore_message[0]
        boss_info = pb_info[channel]
        newembeds = []

        for boss in boss_info:
            newembeds.append(
                await embed_generator.generate_pb_embed(
                    data,
                    boss,
                    number_of_placements=3,
                )
            )
            updated_amount += 1
        await highscore_message.edit(embeds=newembeds)

    return updated_amount


async def post_changelog_record(self, new_embed):
    changelog_channel = self.bot.get_channel(ChannelIds.changelog)
    return await changelog_channel.send(embed=new_embed)
