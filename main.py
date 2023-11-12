import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

client = commands.Bot(
    command_prefix=os.environ.get("DISCORD_BOT_PREFIX"),
    intents=discord.Intents.all()
)


@client.event
async def on_ready():
    print("Bot is Up and Ready!")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Except: {e}")

# guild_ids = [os.environ.get("DISCORD_GUILD_ID")] # Server ID for CraftOfDLRP


@client.tree.command(name="hello", description="Say Hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command !",
                                            ephemeral=True)


client.run(os.environ.get("DISCORD_BOT_TOKEN"))