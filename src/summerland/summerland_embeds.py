from discord import Embed
from constants.colors import Colors


async def make_team_embed(team_info, bingo_tiles):
    tile_number = team_info["currentTile"]
    current_tile = bingo_tiles.tiles[tile_number]
    team_name = team_info["teamName"]
    tile_name = current_tile["Title"]
    current_progress = team_info["progressCounter"]
    submissions_required = current_tile["SubmissionsRequired"]

    embed = Embed(
        title=f"{team_name}",
        description=f"**{tile_name}** (#{tile_number})",
    )
    if submissions_required > 1:
        embed.description += (
            f"\nAcquired **{current_progress}** out of **{submissions_required}**"
        )
    embed.set_image(url=current_tile["ImageUrl"])
    embed.color = Colors.light_purple
    return embed


async def make_pending_submission_embed(username, tile_name, image):
    embed = Embed(
        title=f"🟡 Pending Submission",
        description=f"Your teammate, **{username}**, submitted an image for: **{tile_name}.**\n\nPlease wait while an admin approves, then your dice will be automatically rolled!",
    )
    embed.color = Colors.yellow
    embed.set_image(url=image)

    return embed


async def make_denied_submission_embed():
    embed = Embed(
        title=f"❌ Submission denied. A bingo moderator will be in touch soon",
    )
    embed.color = Colors.red

    return embed


async def make_approved_submission_embed():
    embed = Embed(
        title=f":white_check_mark: Tile Approved & Complete!",
    )
    embed.color = Colors.green

    return embed


async def make_partially_approved_submission_embed(current_progress, progress_needed):
    embed = Embed(
        title=f":white_check_mark: Partial Submission Approved! Your team now has ({current_progress}/{progress_needed})",
    )
    embed.color = Colors.green

    return embed


async def make_diceroll_embed(choice, new_tile_number):
    embed = Embed(
        title=f"Dice Roll...",
        description=f"You rolled a **{choice}**, landing your team on **{new_tile_number}**.",
    )
    embed.set_image(url="https://media1.tenor.com/m/I-xlZfBoMtQAAAAd/cat-dice.gif")
    return embed
