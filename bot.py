import os

from discord.ext import commands

import discord
import json
import random

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
pyprefix = os.getenv('PREFIX')

client = commands.Bot(command_prefix=pyprefix)

@client.event
async def on_command_error(ctx,error):
    embed = discord.Embed(title= "Uh Oh!" , description= "InfoBot has recieved an error!" , color= discord.Colour.red())
    embed.add_field(name = "Error", value = f"`{error}`")
    await ctx.send(embed=embed)

async def open_account(user):
    
    users = await get_bank_data()
    
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 100
        users[str(user.id)]["bank"] = 0
    
    with open("infobank.json","w") as f:
        json.dump(users,f)
    return True

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type= discord.ActivityType.watching, name=f"{len(client.guilds)} servers | ./infohelp"))

@client.command()
async def serveramt(ctx):
    print("serveramt command")
    await ctx.send(f"{client.user} is watching {len(client.guilds)} servers.")
    
@client.command()
async def serverinfo(ctx):
    print("serverinfo command")
    guild_id = ctx.guild.id
    guildfinv = ctx.guild
    embed = discord.Embed(title= ctx.guild.name , description= f"Guild ID {guild_id}" , color= discord.Colour.blue())
    embed.set_thumbnail(url = ctx.guild.icon_url)
    my_guild_invite = await guildfinv.text_channels[0].create_invite()
    embed.add_field(name = "Server Invite", value = my_guild_invite , inline = True )
    embed.add_field(name = "Amount of Boosts", value = ctx.guild.premium_subscription_count , inline = False )
    embed.add_field(name = "Number of Members", value = ctx.guild.member_count , inline = False )
    embed.add_field(name = "Rules", value = ctx.guild.rules_channel , inline = False )
    embed.add_field(name = "Date of Creation", value = ctx.guild.created_at , inline = False )
    embed.add_field(name = "Description", value = ctx.guild.description , inline = False)
    embed.set_footer(text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command()
async def bal(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    
    em = discord.Embed(title = f"{ctx.author.name}'s Balance", color = discord.Colour.green())
    em.add_field(name = "Wallet", value = wallet_amt)
    em.add_field(name = "Bank", value = bank_amt)
    await ctx.send(embed = em)
    
    with open("infobank.json","w") as f:
        json.dump(users,f)


@client.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    
    user = ctx.author
    
    users = await get_bank_data()
    
    earnings = random.randrange(329)
    
    negearnings = random.randrange(56)
    
    if earnings > negearnings:
        await ctx.send(f"A karen attempted to murder you, You pressed charges and got ${earnings}")
    else:
        await ctx.send(f"A karen murdered you, the karen got away with it and you got nothing.")
    if earnings > negearnings:
        users[str(user.id)]["wallet"] += earnings
    else:
        users[str(user.id)]["wallet"] += 0
    
    with open("infobank.json","w") as f:
        json.dump(users,f)

async def get_bank_data():
    with open("infobank.json","r") as f:
        users = json.load(f)
    return users

async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()
    
    users[str(user.id)][mode] += change
    
    with open("infobank.json","w") as f:
        json.dump(users,f)
    
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

@client.command()
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    
    users = await get_bank_data()
    
    if amount == None:
        await ctx.send("you are 100% stupid")
        return
    
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("Wow, you are trying to break me aren't you.")
        return
    if amount<0:
        await ctx.send("what the frick")
        return
    
    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")
    
    await ctx.send(f"well you did it you withdrawed ${amount}")
    

@client.command()
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    
    users = await get_bank_data()
    
    if amount == None:
        await ctx.send("you are 100% stupid")
        return
    
    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("Wow, you are trying to break me aren't you.")
        return
    if amount<0:
        await ctx.send("what the frick")
        return
    
    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,"bank")
    
    await ctx.send(f"well you did it you deposited ${amount}")

client.run(token)
