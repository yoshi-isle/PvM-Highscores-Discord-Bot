import embed
import database


async def create_raid_pbs(ctx):
    # Load data
    data = database.GetPersonalBests()

    # Post ToB PBs
    await embed.post_raids_embed(
        ctx,
        data,
        "Theatre of Blood",
        pb_categories=[5, 4, 3, 2, 1],
        number_of_placements=3,
    )

    # Post HMT PBs
    await embed.post_raids_embed(
        ctx,
        data,
        "Theatre of Blood: Hard Mode",
        pb_categories=[5, 4, 3, 2, 1],
        number_of_placements=3,
    )

    # Post CoX PBs
    await embed.post_raids_embed(
        ctx,
        data,
        "Chambers of Xeric",
        pb_categories=[5, 3, 2, 1],
        number_of_placements=3,
    )

    # Post CoX: CM PBs
    await embed.post_raids_embed(
        ctx,
        data,
        "Chambers of Xeric: Challenge Mode",
        pb_categories=[5, 3, 2, 1],
        number_of_placements=3,
    )

    # Post ToA: Expert Mode PBs
    await embed.post_raids_embed(
        ctx, data, "Tombs of Amascut: Expert Mode", [5, 3, 2, 1], 3
    )


async def create_boss_pbs(ctx):
    # Load data
    data = database.GetPersonalBests()

    # Post Nightmare PBs
    await embed.post_boss_embed(ctx, data, "Nightmare (Solo)", 3)
    await embed.post_boss_embed(ctx, data, "Phosani's Nightmare", 3)

    # Post DT2 PBs
    await embed.post_boss_embed(ctx, data, "Vardorvis", 3)
    await embed.post_boss_embed(ctx, data, "Duke Succellus", 3)
    await embed.post_boss_embed(ctx, data, "The Whisperer", 3)
    await embed.post_boss_embed(ctx, data, "Leviathan", 3)

    # Post DT2 (Awakened) PBs
    await embed.post_boss_embed(ctx, data, "Vardorvis (Awakened)", 3)
    await embed.post_boss_embed(ctx, data, "Duke Succellus (Awakened)", 3)
    await embed.post_boss_embed(ctx, data, "The Whisperer (Awakened)", 3)
    await embed.post_boss_embed(ctx, data, "Leviathan (Awakened)", 3)

    # Post Tzhaar PBs
    await embed.post_boss_embed(ctx, data, "Inferno", 5)
    await embed.post_boss_embed(ctx, data, "Fight Caves", 5)

    # Post Gauntlet PBs
    await embed.post_boss_embed(ctx, data, "The Gauntlet", 3)
    await embed.post_boss_embed(ctx, data, "The Corrupted Gauntlet", 3)

    # Post Misc PBs
    await embed.post_boss_embed(ctx, data, "Zulrah", 3)
    await embed.post_boss_embed(ctx, data, "Vorkath", 3)
    await embed.post_boss_embed(ctx, data, "Grotesque Guardians", 3)
    await embed.post_boss_embed(ctx, data, "Alchemical Hydra", 3)
    await embed.post_boss_embed(ctx, data, "Phantom Muspah", 3)
    await embed.post_boss_embed(ctx, data, "Hespori", 3)
    await embed.post_boss_embed(ctx, data, "Mimic", 3)
    await embed.post_boss_embed(ctx, data, "Hallowed Sepulchre (overall)", 3)
