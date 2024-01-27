import datetime
from typing import Literal

from discord import Embed

from bingo.dartboard import Task
from constants.colors import Colors


async def generate_dartboard_task_embed(team_name: str, task: Task) -> Embed:
    """Build the dartboard bingo task embed.

    Args:
        team_name (str): team name that was used to generate the task
        task (Task): The task object that was generated in the command

    Returns:
        Embed: Discord embed message
    """

    embed = Embed(
        title=f"The {team_name} team must get {task.task_name}!",
        description=f"{task.task_description}",
        colour=get_task_color(task.task_points),
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


def get_task_color(points: int) -> Literal:
    """Get hexadecimal color for a task based on the value of its tasks points

    Args:
        points (int): task point value

    Returns:
        Literal: color in hexadecimal format
    """

    if points == 5:
        return Colors.easy_task
    elif points == 10:
        return Colors.medium_task
    elif points == 15:
        return Colors.hard_task
    elif points == 25:
        return Colors.elite_task
    elif points == 50:
        return Colors.master_task
