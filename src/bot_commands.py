import embed_generator
import database
import helpers.boss_names as boss_names
import helpers.raid_names as raid_info


async def create_raid_pbs(ctx):
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
    data = database.GetPersonalBests()

    for name in boss_names.BOSS_NAMES:
        await embed_generator.post_boss_embed(ctx, data, name, 3)


async def update_boss_pbs(ctx):
    data = database.GetPersonalBests()

    channel = ctx.channel
    messages = [message async for message in channel.history()]
    messages = messages[::-1]

    for message in messages:
        if message.embeds:
            for embed in message.embeds:
                await embed_generator.update_boss_embed(
                    ctx, data, message, embed.title, 3
                )
                break


async def update_raids_pbs(ctx):
    data = database.GetPersonalBests()

    channel = ctx.channel
    messages = [message async for message in channel.history()]
    messages = messages[::-1]

    for message in messages:
        if message.embeds:
            for embed in message.embeds:
                await embed_generator.update_raids_embed(
                    ctx, data, message, embed.title, raid_info.RAID_INFO[embed.title], 3
                )
                break
