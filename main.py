import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

client = commands.Bot(
    command_prefix=os.environ.get('DISCORD_BOT_PREFIX'),
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


@client.tree.command(name="hello", description="Say Hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}! "
                                            f"This is a slash command !",
                                            ephemeral=True)


@client.tree.command(name="ping", description="Show bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(client.latency * 1000, 1)} ms",
                                            ephemeral=True)


@client.tree.command(name="creator", description=f"{os.environ.get('DISCORD_BOT_NAME')} creator")
async def creator(interaction: discord.Interaction):
    await interaction.response.send_message(f"This bot was made with :heart: by "
                                            f"{os.environ.get('DISCORD_BOT_CREATOR')}",
                                            ephemeral=True)


@client.tree.command(name="help", description="Show all available commands")
async def help(interaction: discord.Interaction):
    # Create base embed
    embed = (discord.Embed(
        title=f"{os.environ.get('DISCORD_BOT_NAME')}",
        description="Show all currently available commands of this bot"
    ))

    # Set embed fileds
    embed.add_field(
        name="help",
        value="Show all available commands"
    )
    embed.add_field(
        name="ping",
        value="Show bot latency"
    )
    embed.add_field(
        name="creator",
        value="Show bot creator"
    )

    # Set embed footer
    embed.set_footer(
        text=f"Last update: 11/12/2023"
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

client.run(os.environ.get("DISCORD_BOT_TOKEN"))
