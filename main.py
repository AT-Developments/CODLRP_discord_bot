import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(
    command_prefix=os.environ.get("DISCORD_BOT_PREFIX"),
    intents=discord.Intents.all(),
    description=f"{os.environ.get('DISCORD_BOT_NAME')} discord bot",
    owner_id=os.environ.get("DISCORD_BOT_CREATOR_ID"),
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
    await interaction.response.send_message(
        f"Hey {interaction.user.mention}! " f"This is a slash command !", ephemeral=True
    )


@client.tree.command(name="ping", description="Show bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong! {round(client.latency * 1000, 1)} ms", ephemeral=True
    )


@client.tree.command(
    name="creator", description=f"{os.environ.get('DISCORD_BOT_NAME')} creator"
)
async def creator(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"This bot was made with :heart: by "
        f"{os.environ.get('DISCORD_BOT_CREATOR')}",
        ephemeral=True,
    )


@client.tree.command(name="help", description="Show all available commands")
async def help(interaction: discord.Interaction):
    # Create Base Embed
    embed = discord.Embed(
        title="Help Command",
        description="Show all currently available commands of this bot",
        color=discord.Color.blurple(),
    )

    # Set Embed Author
    embed.set_author(
        name=f"{os.environ.get('DISCORD_BOT_NAME')}",
        icon_url=f"{os.environ.get('DISCORD_BOT_ICON')}",
    )

    # Set Embed Thumbnails
    embed.set_thumbnail(url=f"{os.environ.get('DISCORD_BOT_ICON')}")

    # Set Embed Fields
    embed.add_field(name="help", value="Show all available commands", inline=False)
    embed.add_field(name="ping", value="Show bot latency", inline=False)
    embed.add_field(name="creator", value="Show bot creator", inline=False)

    # Set Embed Footer
    embed.set_footer(text="Last update: 11/12/2023")
    await interaction.response.send_message(embed=embed, ephemeral=True)


client.run(os.environ.get("DISCORD_BOT_TOKEN"))
