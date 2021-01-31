import os

from discord.ext import commands

import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
pyprefix = os.getenv('PREFIX')

client = commands.Bot(command_prefix=pyprefix)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type= discord.ActivityType.watching, name=f"{len(client.guilds)} servers | ./infohelp"))

@client.command()
async def serveramt(ctx):
    await ctx.send(f"{client.user} is watching {len(client.guilds)} servers.")
    
@client.command()
async def serverinfo(ctx):
    guild_id = ctx.guild.id
    guildfinv = ctx.guild
    embed = discord.Embed(title= ctx.guild.name , description= guild_id , color= discord.Colour.blue())
    embed.set_thumbnail(url = ctx.guild.icon_url)
    my_guild_invite = await guildfinv.text_channels[0].create_invite()
    embed.add_field(name = "Server Invite", value = my_guild_invite , inline = True )
    await ctx.send(embed=embed)

@client.command()
async def infohelp(ctx):
    await ctx.send("serveramt and serverinfo")

client.run(token)
