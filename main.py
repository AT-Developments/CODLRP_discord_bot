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
    guild = client.get_guild(int(os.environ.get("DISCORD_GUILD_ID")))
    # Create Base Embed
    embed = discord.Embed(
        title="Help Command",
        description="Show all currently available commands of this bot",
        color=discord.Color.blurple(),
    )

    # Set Embed Author
    embed.set_author(
        name=f"{os.environ.get('DISCORD_BOT_NAME')}",
        icon_url=client.user.avatar.url,
    )

    # Set Embed Thumbnails
    embed.set_thumbnail(url=guild.icon.url)

    # Set Embed Fields
    embed.add_field(name="help", value="Show all available commands", inline=False)
    embed.add_field(name="ping", value="Show bot latency", inline=False)
    embed.add_field(name="creator", value="Show bot creator", inline=False)
    embed.add_field(name="discord", value="Show invite link", inline=False)
    embed.add_field(name="help_admin", value="Show admin commands", inline=False)

    # Set Embed Footer
    embed.set_footer(text="Last update: 11/12/2023")
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="discord", description="Actual infinite invite link")
async def discord_invite(interaction: discord.Interaction):
    guild = client.get_guild(int(os.environ.get("DISCORD_GUILD_ID")))
    list_invites = await guild.invites()

    # Set base embed
    embed = discord.Embed(
        title=f"Invite link for {guild.name}",
        description=f"{list_invites[0].url}",
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
    guild = client.get_guild(int(os.environ.get("DISCORD_GUILD_ID")))
    # Check if the user is a moderator
    member = interaction.user
    if member.guild_permissions.administrator is None:
        await interaction.response.send_message(
            "You do not have permission to use this command.", ephemeral=True
        )
        return

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

    await interaction.response.send_message(embed=embed, ephemeral=False)


@client.event
async def on_member_join(member):
    if member.guild.name == os.environ.get("DISCORD_GUILD_NAME"):  # Server Name
        guild = client.get_guild(int(os.environ.get("DISCORD_GUILD_ID")))
        role = discord.utils.get(
            member.guild.roles, id=int(os.environ.get("DISCORD_GUILD_MEMBER_ID"))
        )
        await member.add_roles(role)

        # Engish Embed
        embed_en = discord.Embed(
            title="Member Joined",
            description=f"{member.mention}, Welcome to {member.guild.name}. "
            f"\nWe hope that your time with us is a happy one!",
            color=0x9B26B9,
            timestamp=datetime.datetime.now(),
        )
        embed_en.add_field(
            name="Please check out the Rules Channel!",
            value=client.get_channel(
                int(os.environ.get("DISCORD_GUILD_RULES_CHANNEL"))
            ).mention,
            inline=True,
        )
        embed_en.add_field(
            name="Latest announcements are made here!",
            value=client.get_channel(
                int(os.environ.get("DISCORD_GUILD_ANNOUNCEMENT_CHANNEL"))
            ).mention,
            inline=True,
        )
        # Add thumbnail to embed
        embed_en.set_thumbnail(url=guild.icon.url)

        # French Embed
        embed_fr = discord.Embed(
            title="Un nouveau membre viens de nous rejoindre",
            description=f"{member.mention}, Bienvenue chez {member.guild.name}. "
            f"\nNous espérons que vous passerez un bon moment avec nous !",
            color=0x9B26B9,
            timestamp=datetime.datetime.now(),
        )
        embed_fr.add_field(
            name="Merci de lire les règles du serveur",
            value=client.get_channel(
                int(os.environ.get("DISCORD_GUILD_RULES_CHANNEL"))
            ).mention,
            inline=True,
        )
        embed_fr.add_field(
            name="Les dernières annonces sont faites ici!",
            value=client.get_channel(
                int(os.environ.get("DISCORD_GUILD_ANNOUNCEMENT_CHANNEL"))
            ).mention,
            inline=True,
        )
        # Add thumbnail to embed
        embed_fr.set_thumbnail(url=guild.icon.url)

        both_languages_embed = [embed_en, embed_fr]
        c = client.get_channel(int(os.environ.get("DISCORD_GUILD_JOIN_CHANNEL")))
        await c.send(embeds=both_languages_embed)


@client.tree.command(
    name="minecraft", description="Provide information about our minecraft server"
)
async def minecraft(interaction: discord.Interaction):
    guild = client.get_guild(int(os.environ.get("DISCORD_GUILD_ID")))
    # Create EN Base Embed
    embed_en = discord.Embed(
        title="Minecraft Server",
        description="Our server is currently under construction"
        "\nThe opening date will be announced soon",
        color=discord.Color.blurple(),
    )
    # Set Embed Author
    embed_en.set_author(
        name=f"{os.environ.get('DISCORD_BOT_NAME')}",
        icon_url=f"{os.environ.get('DISCORD_BOT_ICON')}",
    )
    # Set Embed Thumbnails
    embed_en.set_thumbnail(url=guild.icon.url)
    # Set Embed Footer
    embed_en.set_footer(text="Last update: 11/14/2023")

    # Create FR Base Embed
    embed_fr = discord.Embed(
        title="Serveur Minecraft",
        description="Notre serveur est actuellement en cours de construction"
        "\nLa date d'ouverture sera annoncée utlérieurement",
        color=discord.Color.blurple(),
    )
    # Set Embed Author
    embed_fr.set_author(
        name=f"{os.environ.get('DISCORD_BOT_NAME')}",
        icon_url=f"{os.environ.get('DISCORD_BOT_ICON')}",
    )
    # Set Embed Thumbnails
    embed_fr.set_thumbnail(url=guild.icon.url)
    # Set Embed Footer
    embed_fr.set_footer(text="Last update: 11/14/2023")

    both_language_embeds = [embed_en, embed_fr]
    await interaction.response.send_message(embeds=both_language_embeds)


client.run(os.environ.get("DISCORD_BOT_TOKEN"))
