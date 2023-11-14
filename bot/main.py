import datetime
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
    await client.change_presence(activity=discord.Game(name="/help"))
    print("Bot is Up and Ready!")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Except: {e}")


@client.tree.command(name="ping", description="Show bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong 🏓 {round(client.latency * 1000, 1)} ms", ephemeral=True
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
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="discord", description="Actual infinite invite link")
async def discord_invite(interaction: discord.Interaction):
    # Set guild information
    guild = client.get_guild(int(os.environ.get("DISCORD_GUILD_ID")))
    list_invites = await guild.invites()

    # Set base embed
    embed = discord.Embed(
        title=f"Invite link for {guild.name}",
        description=f"Click [here]({list_invites[0].url}) to join the server!",
        color=discord.Color.green(),
    )

    # Add thumbnail to embed
    embed.set_thumbnail(url=guild.icon.url)

    # Add footer to embed
    embed.set_footer(
        text=f"Requested by {interaction.user.name}",
        icon_url=interaction.user.avatar.url,
    )

    await interaction.response.send_message(embed=embed)


@client.tree.command(name="all_invites", description="All active invite link")
async def all_discord_invite(interaction: discord.Interaction):
    # Check if the user is a moderator
    member = interaction.user
    if member.guild_permissions.administrator is None:
        await interaction.response.send_message(
            "You do not have permission to use this command.", ephemeral=True
        )
        return

    # Set guild information
    guild = client.get_guild(int(os.environ.get("DISCORD_GUILD_ID")))
    list_invites = await guild.invites()

    # Set base embed
    embed = discord.Embed(
        title=f"Invite link for {guild.name}",
        description=f"Click [here]({list_invites[0].url}) to join the server!",
        color=discord.Color.red(),
    )

    # Add all invites to embed
    for unique_invite in list_invites:
        embed.add_field(
            name=f"Invite created by {unique_invite.inviter}",
            value=unique_invite.url,
            inline=False,
        )

    # Add thumbnail to embed
    embed.set_thumbnail(url=guild.icon.url)

    # Add footer to embed
    embed.set_footer(
        text=f"Requested by {interaction.user.name}",
        icon_url=interaction.user.avatar.url,
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)


@client.event
async def on_member_join(member):
    if member.guild.name == os.environ.get("DISCORD_GUILD_NAME"):  # Server Name
        role = discord.utils.get(
            member.guild.roles, id=int(os.environ.get("DISCORD_GUILD_MEMBER_ID"))
        )
        await member.add_roles(role)
        embed = discord.Embed(
            title="Member Joined",
            description=f"{member.mention}, Welcome to {member.guild.name}. "
            f"We hope that your time with us is a happy one!",
            color=0x9B26B9,
            timestamp=datetime.datetime.now(),
        )
        # you don't need the f before Strings with no variables or statements in it

        embed.add_field(
            name="Please check out the Rules Channel!",
            value="Coming soon",
            inline=False,
        )
        embed.add_field(
            name="Latest announcements are made here!",
            value="Coming soon",
            inline=False,
        )

        c = client.get_channel(int(os.environ.get("DISCORD_GUILD_JOIN_CHANNEL")))
        await c.send(embed=embed)


client.run(os.environ.get("DISCORD_BOT_TOKEN"))
