from typing import Optional
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from settings import token


MY_GUILD = discord.Object(id=835192897690402866)  # replace with your guild id
channelID = 1107328095763042384  # channel ID goes here
role = "TEST - Net Controller" #role for checking



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
    await channel.send(content='@everyone', embed=embed)


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
    await channel.send(content='@everyone', embed=embed)

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
                        description="No active NWS alerts or severe weather is expected. Repeater will be operational as usual.",
                        colour=0xff0000,
                        timestamp=datetime.now())
    embed.add_field(name="Repeater",
                value="WR4CC (146.700 (-) PL 77.0)",
                inline=False)
    embed.set_image(url="https://i.imgur.com/VVgp41c.png")
    embed.set_footer(text=f'Activated by: {interaction.user.display_name}')

    #Gets channel and sends message
    channel = bot.get_channel(int(channelID))
    await channel.send(content='@everyone', embed=embed)
    

@green.error
async def handler(ctx: commands.Context, error: commands.CommandError):
    #print(error)
    await ctx.response.send_message(
        error, ephemeral=True, delete_after=30
    )

bot.run(token)