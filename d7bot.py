from typing import Optional
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

import os

#from settings import token

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MY_GUILD = discord.Object(id=os.getenv('GUILD'))
channelID = os.getenv('CHANNEL')
role = os.getenv('ROLE')


#MY_GUILD = discord.Object(id=1089329396868993084)  # replace with your guild id
#channelID = 1090402258031751228  # channel ID goes here
#role = "Net Control" #role for checking



class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
bot = MyClient(intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the radar"))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    

# STATUS GREEN
@bot.tree.command()
@app_commands.checks.has_role(role)
async def green(interaction: discord.Interaction):
    """Sets the current status to level Green"""
    
    #Sends confirmation message to user
    await interaction.response.send_message(
        f'Setting to Green status.', ephemeral=True, delete_after=30
    )

    #Builds the embed
    embed = discord.Embed(title="District 7 Status: Green",
                        description="No active NWS alerts or severe weather is expected. Repeater will be operational as usual.",
                        colour=0x00ff00,
                        timestamp=datetime.now())
    embed.add_field(name="Repeater",
                value="WR4CC (146.700 (-) PL 77.0)",
                inline=False)
    embed.set_image(url="https://i.imgur.com/kaGKstv.png")
    embed.set_footer(text=f'Activated by: {interaction.user.display_name}')

    #Gets channel and sends message
    channel = bot.get_channel(int(channelID))
    await channel.send(content='@everyone Status: Green', embed=embed)


# STATUS YELLOW
@bot.tree.command()
@app_commands.checks.has_role(role)
async def yellow(interaction: discord.Interaction):
    """Sets the current status to level Yellow"""
    
    #Sends confirmation message to user
    await interaction.response.send_message(
        f'Setting to Yellow status.', ephemeral=True, delete_after=30
    )

    #Builds the embed
    embed = discord.Embed(title="District 7 Status: Yellow",
                        description="A severe thunderstorm watch, tornado watch, or flash flood watch is issued for any of the counties in the district by NWS Morristown. Severe weather will likely occur in our area. Please keep all conversations to the point on the repeater and be prepared to relinquish the repeater to net control should the watch be upgraded to a warning.",
                        colour=0xffff00,
                        timestamp=datetime.now())
    embed.add_field(name="Repeater",
                value="WR4CC (146.700 (-) PL 77.0)",
                inline=False)
    embed.set_image(url="https://i.imgur.com/QdIQgRj.png")
    embed.set_footer(text=f'Activated by: {interaction.user.display_name}')

    #Gets channel and sends message
    channel = bot.get_channel(int(channelID))
    await channel.send(content='@everyone Status: Yellow', embed=embed)

# STATUS RED
@bot.tree.command()
@app_commands.checks.has_role(role)
async def red(interaction: discord.Interaction):
    """Sets the current status to level Red"""
    
    #Sends confirmation message to user
    await interaction.response.send_message(
        f'Setting to Red status.', ephemeral=True, delete_after=30
    )

    #Builds the embed
    embed = discord.Embed(title="District 7 Status: Red",
                        description="A severe thunderstorm warning, tornado warning, or flash flood warning has been issued for any of the counties in the district by NWS Morristown. This means severe weather is occurring in our area. Take cover. The severe WX net will be operational at this time and the repeater will only be open to emergency traffic, severe reports, or questions about the storm. No other traffic will be permitted on the repeater. All traffic must go through net control.",
                        colour=0xff0000,
                        timestamp=datetime.now())
    embed.add_field(name="Repeater",
                value="WR4CC (146.700 (-) PL 77.0)",
                inline=False)
    embed.set_image(url="https://i.imgur.com/VVgp41c.png")
    embed.set_footer(text=f'Activated by: {interaction.user.display_name}')

    #Gets channel and sends message
    channel = bot.get_channel(int(channelID))
    await channel.send(content='@everyone Status: Red', embed=embed)

# STATUS UPDATE
@bot.tree.command(name="status", description="Alerts everyone of the status.")
@app_commands.describe(message="Sends a weather update")
@app_commands.checks.has_role(role)
async def status(interaction: discord.Interaction, message: str) -> None:
    """Gives an update"""
    
    await interaction.response.send_message(
        f'Posting status update', ephemeral=True, delete_after=1
    )

    #Gets channel and sends message
    channel = bot.get_channel(int(channelID))
    await channel.send(content=f'@everyone {message}')
    await channel.send(content=f'Updated by: {interaction.user.display_name}')

# BOT TEST
@bot.tree.command()
@app_commands.checks.has_role(role)
async def test(interaction: discord.Interaction):
    """Tests the bot"""
    
    #Sends confirmation message to user
    await interaction.response.send_message(
        f'Bot responded okay. Permissions granted.', ephemeral=True, delete_after=30
    )    

@green.error
async def handler(ctx: commands.Context, error: commands.CommandError):
    #print(error)
    await ctx.response.send_message(
        error, ephemeral=True, delete_after=30
    )

@yellow.error
async def handler(ctx: commands.Context, error: commands.CommandError):
    #print(error)
    await ctx.response.send_message(
        error, ephemeral=True, delete_after=30
    )

@red.error
async def handler(ctx: commands.Context, error: commands.CommandError):
    #print(error)
    await ctx.response.send_message(
        error, ephemeral=True, delete_after=30
    )

@test.error
async def handler(ctx: commands.Context, error: commands.CommandError):
    #print(error)
    await ctx.response.send_message(
        error, ephemeral=True, delete_after=30
    )

bot.run(DISCORD_TOKEN)