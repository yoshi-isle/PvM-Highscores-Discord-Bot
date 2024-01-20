import discord
import json
import typing
import embed_generator
import database
import constants.boss_names as boss_names
import constants.raid_names as raid_info
from discord.ext import commands
from discord import app_commands
from dartboard import Dartboard

# Import keys
with open("../config/appsettings.local.json") as appsettings:
    data = json.load(appsettings)

bot_token = data["BotToken"]
channel_id = data["HighscoresChannelId"]



bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

dartboard = Dartboard()


@bot.event
async def on_ready():
    await bot.tree.sync()


@bot.command()
async def raidpbs(ctx):
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


@bot.command()
async def bosspbs(ctx):
    channel = ctx.channel
    await channel.purge()
    data = database.GetPersonalBests()

    for name in boss_names.BOSS_NAMES:
        await embed_generator.post_boss_embed(ctx, data, name, number_of_placements=3)


async def throw_a_dart_autocomplete(
    interaction: discord.Interaction,
    current:str,
) -> typing.List[app_commands.Choice[str]]:
    data = []
    for team_name in ['Sapphire', 'Ruby', 'Emerald', 'Diamond', 'Dragonstone', 'Opal', 'Jade', 'Topaz']:
        if current.lower() in team_name.lower():
            data.append(app_commands.Choice(name=team_name, value=team_name))
    return data


@bot.tree.command(name="throw_a_dart")
@app_commands.describe(team="Generate a new task for your team")
@app_commands.autocomplete(team=throw_a_dart_autocomplete)
async def throw_a_dart(
    interaction: discord.Interaction,
    team: str,
):
    new_task = dartboard.get_task()
    embed = await embed_generator.generate_dartboard_task_embed(
        team_name=f"{team}",
        task=new_task,
    )

    await interaction.response.send_message(embed=embed)




bot.run(bot_token)
