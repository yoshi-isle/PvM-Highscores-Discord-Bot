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
    pb_data = await self.database.get_personal_bests()
    pb_highscore_channels = [
        self.bot.get_channel(ChannelIds.tob_pbs),
        self.bot.get_channel(ChannelIds.cox_pbs),
        self.bot.get_channel(ChannelIds.toa_pbs),
        self.bot.get_channel(ChannelIds.tzhaar_pbs),
        self.bot.get_channel(ChannelIds.dt2_pbs),
        self.bot.get_channel(ChannelIds.boss_pbs),
        self.bot.get_channel(ChannelIds.misc_pbs),
    ]
    pb_definitions = [
        theatre_of_blood.INFO,
        chambers_of_xeric.INFO,
        tombs_of_amascut.INFO,
        tzhaar.INFO,
        dt2bosses.INFO,
        bosses.INFO,
        misc_activities.INFO,
    ]
    validate_info(pb_highscore_channels, pb_definitions)

    for channel, info in zip(pb_highscore_channels, pb_definitions):
        highscore_embed = get_highscore_embed(self, channel)
        boss_info = info
        newembeds = generate_new_embeds(boss_info, pb_data)
        await highscore_embed.edit(embeds=newembeds)


async def generate_new_embeds(boss_info, pb_data):
    return [
        await embed_generator.generate_pb_embed(pb_data, boss) for boss in boss_info
    ]


async def get_highscore_embed(self, channel):
    potential_embed_messages = [
        message
        async for message in channel.history(limit=20, oldest_first=True)
        if len(message.embeds) != 0
    ]

    if potential_embed_messages is None:
        raise ValueError(f"Didn't find any highscore embeds in: {channel}")

    num_embeds = len(potential_embed_messages)

    if num_embeds != 1:
        raise ValueError(f"Expected 1 embed in: {channel}. Found {num_embeds}")

    return potential_embed_messages[0]


async def post_changelog_record(self, new_embed):
    changelog_channel = self.bot.get_channel(ChannelIds.changelog)
    return await changelog_channel.send(embed=new_embed)


async def validate_info(channels, definitions):
    if len(channels) != len(definitions):
        raise ValueError(
            f"Number of highscore channels ({len(channels)}) does not match up with number of definitions ({len(definitions)})"
        )
