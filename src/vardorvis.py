from discord import Embed
import osrswiki

async def PostEmbed(ctx, data):
   print(data)
   vardorvis_data = sorted(
       [result for result in data if result["boss"] == "Vardorvis"],
       key=lambda x: x["pb"],
   )

   embed = Embed(title="Vardorvis", color=0xFF1E6D)
   embed_content = ""

   # Handle up to 3 placements with specific emojis
   for i in range(min(3, len(vardorvis_data))):
       player_data = vardorvis_data[i]
       placement_emoji = {
           0: ":first_place:",
           1: ":second_place:",
           2: ":third_place:",
       }.get(i, f":regional_indicator_{i + 1}:")  # Fallback for 4th and beyond
       embed_content += f"{placement_emoji} {player_data['osrsUsername']} - {player_data['pb']}\n"

   embed.add_field(name="", value=embed_content, inline=False)
   embed.set_thumbnail(url=osrswiki.vardorvisCdnUrl)
   await ctx.send(embed=embed)