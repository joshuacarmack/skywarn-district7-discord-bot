from typing import Optional
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands

from settings import token


MY_GUILD = discord.Object(id=835192897690402866)  # replace with your guild id
channelID = 1107328095763042384  # channel ID goes here



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
    


@bot.tree.command()
async def green(interaction: discord.Interaction):
    """Sets the current status to level Green"""
    # await interaction.response.send_message(f'Hi, {interaction.user.mention}')
    await interaction.response.send_message(
        f'Setting to Green status.', ephemeral=True
    )

    embed = discord.Embed(title="District 7 Status: Green",
                        description="No active NWS alerts or severe weather is expected. Repeater will be operational as usual.",
                        colour=0x00ff00,
                        timestamp=datetime.now())

    embed.set_image(url="https://i.imgur.com/kaGKstv.png")

    embed.set_footer(text=f'Activated by: {interaction.user.display_name}')


    channel = bot.get_channel(int(channelID))
    await channel.send(content='@everyone', embed=embed)
    


# This context menu command only works on messages
# @client.tree.context_menu(name='Report to Moderators')
# async def report_message(interaction: discord.Interaction, message: discord.Message):
#     # We're sending this response message with ephemeral=True, so only the command executor can see it
#     await interaction.response.send_message(
#         f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
#     )

#     # Handle report by sending it into a log channel
#     log_channel = interaction.guild.get_channel(0)  # replace with your channel id

#     embed = discord.Embed(title='Reported Message')
#     if message.content:
#         embed.description = message.content

#     embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
#     embed.timestamp = message.created_at

#     url_view = discord.ui.View()
#     url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

#     await log_channel.send(embed=embed, view=url_view)


bot.run(token)