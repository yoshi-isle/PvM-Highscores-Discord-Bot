import embed_generator
import database
import constants.boss_names as boss_names
import constants.raid_names as raid_info


async def create_raid_pbs(ctx):
    channel = ctx.channel
    await channel.purge()
    data = database.GetPersonalBests()

    for info in raid_info.RAID_INFO:
        await embed_generator.post_raids_embed(
            ctx,
            data,
            info,
            pb_categories=raid_info.RAID_INFO[info],
            number_of_placements=3,
        )


async def create_boss_pbs(ctx):
    channel = ctx.channel
    await channel.purge()
    data = database.GetPersonalBests()

    for name in boss_names.BOSS_NAMES:
        await embed_generator.post_boss_embed(ctx, data, name, 3)
