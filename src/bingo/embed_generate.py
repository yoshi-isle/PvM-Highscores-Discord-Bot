import datetime

from discord import Embed

from bingo.dartboard import Task
from constants.colors import Colors


async def generate_dartboard_task_embed(team_name: str, task: Task):
    """
    Builds the embed message string that will get posted to the channel
    """

    embed = Embed(
        title=f"The {team_name} team must get {task.task_name}!",
        description=f"{task.task_description}",
        colour=Colors.light_blue,
        timestamp=datetime.datetime.now(),
    )

    embed.set_author(name="Kitty Bot")

    embed.add_field(name="Dice roll result:", value=f"{task.task_number}", inline=True)
    embed.add_field(name="Point value", value=f"{task.task_points}", inline=True)

    if task.task_challenge_name:
        # this blank field is for spacing purposes
        embed.add_field(name="", value="", inline=False)
        embed.add_field(
            name="Complete this challenge and win the bonus challenge points!",
            value=f"{task.task_challenge_description}",
            inline=True,
        )
        embed.add_field(
            name="Challenge points", value=f"{task.task_challenge_points}", inline=True
        )

    embed.set_thumbnail(url=task.image_link)

    embed.set_footer(text="👞🗑️")

    return embed
