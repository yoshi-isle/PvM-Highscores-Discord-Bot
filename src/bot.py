import discord
import json
import embed
import database
from discord.ext import commands
from discord import Embed
# Import keys
with open('../config/appsettings.local.json') as settings_json:
    data = json.load(settings_json)

bot_token = data['BotToken']
channel_id = data['HighscoresChannelId']

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.command()
async def updatehighscores(ctx):
    # Load data
    data = database.GetPersonalBests()

    # Post ToB PBs
    await embed.post_raids_embed(ctx, data, "Theatre of Blood")

    # Post HMT PBs
    await embed.post_raids_embed(ctx, data, "Theatre of Blood: Hard Mode")

    # Post CoX PBs
    # await embed.post_embed(ctx, data, "Chambers of Xeric (Trio)")
    # await embed.post_embed(ctx, data, "Chambers of Xeric (Duo)")
    # await embed.post_embed(ctx, data, "Chambers of Xeric (Solo)")

    # Post CoX: CM PBs
    # await embed.post_embed(ctx, data, "Chambers of Xeric: Challenge Mode (Trio)")
    # await embed.post_embed(ctx, data, "Chambers of Xeric: Challenge Mode (Duo)")
    # await embed.post_embed(ctx, data, "Chambers of Xeric: Challenge Mode (Solo)")

    # Post ToA: Expert Mode PBs
    # await embed.post_embed(ctx, data, "Tombs of Amascut: Expert Mode (Duo)")
    # await embed.post_embed(ctx, data, "Tombs of Amascut: Expert Mode (Solo)")

    # Post Nightmare PBs
    # await embed.post_embed(ctx, data, "Nightmare (Solo)")
    # await embed.post_embed(ctx, data, "Phosani's Nightmare")

    # Post DT2 PBs
    await embed.post_boss_embed(ctx, data, "Vardorvis")
    await embed.post_boss_embed(ctx, data, "Duke Succellus")
    await embed.post_boss_embed(ctx, data, "The Whisperer")
    await embed.post_boss_embed(ctx, data, "Leviathan")

    # Post DT2 (Awakened) PBs
    # await embed.post_embed(ctx, data, "Vardorvis (Awakened)")
    # await embed.post_embed(ctx, data, "Duke Succellus (Awakened)")
    # await embed.post_embed(ctx, data, "The Whisperer (Awakened)")
    # await embed.post_embed(ctx, data, "Leviathan (Awakened)")

    # Post Tzhaar PBs
    # await embed.post_embed(ctx, data, "Inferno")
    # await embed.post_embed(ctx, data, "Fight Caves")

    # Post Gauntlet PBs
    # await embed.post_embed(ctx, data, "The Gauntlet")
    # await embed.post_embed(ctx, data, "The Corrupted Gauntlet")

    # Post Misc PBs
    # await embed.post_embed(ctx, data, "Zulrah")
    # await embed.post_embed(ctx, data, "Vorkath")
    # await embed.post_embed(ctx, data, "Grotesque Guardians")
    # await embed.post_embed(ctx, data, "Alchemical Hydra")
    # await embed.post_embed(ctx, data, "Phantom Muspah")
    # await embed.post_embed(ctx, data, "Hespori")
    # await embed.post_embed(ctx, data, "Mimic")
    # await embed.post_embed(ctx, data, "Hallowed Sepulchre (overall)")

print("Bot running")
bot.run(bot_token)