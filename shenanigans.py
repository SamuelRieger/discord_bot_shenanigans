import discord
import os
import time
import random
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from threading import Thread
from time import sleep

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = ',', intents=intents)
stop = False

@client.event
async def on_ready():
    print('Bot Online')

@client.command()
async def annoy(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice
    if channel:
        global stop
        stop = False
        channel = ctx.message.author.voice.channel
        channel_name = channel.name
        await ctx.send('**Cover your ears unfortunate souls in `' + channel_name + '`. :skull:**')
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        for i in range(20):
            voice = get(client.voice_clients, guild=ctx.guild)
            if stop == True:
                if voice:
                    await ctx.voice_client.disconnect()
                stop = False
                break
            if voice:
                await ctx.voice_client.disconnect()
            else:
                await channel.connect()
            time.sleep(.200)
        
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice:
            await ctx.voice_client.disconnect()
        await ctx.send('**The pain is over. :innocent:**')
    else:
        await ctx.send('**You have to suffer with them if you want me to start. :smiling_imp:**')

@client.command()
async def stop(ctx):
    global stop
    stop = True
    member = ctx.message.author
    role = discord.utils.get(ctx.message.guild.roles, name = 'Soldat')
    await member.add_roles(role)

@client.command()
async def jumble(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice
    if channel:
        await ctx.send('**Let the fun begin. :game_die:**')
        channel = ctx.message.author.voice.channel
        members = channel.voice_states.keys()
        channels = ctx.guild.voice_channels
        for member in members:
            await client.wait_until_ready()
            cur_channel = channels[random.randint(0, len(channels)-1)]
            cur_member = ctx.guild.get_member(member)
            print(cur_channel)
            print(cur_member.name)
            await cur_member.move_to(cur_channel)
    else:
        await ctx.send('**You have to suffer with them if you want me to start. :smiling_imp:**')

@client.command()
async def degrade(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice
    if channel:
        channel = ctx.message.author.voice.channel
        channel_name = channel.name
        await ctx.send('**`' + channel_name + '`  is now a ham radio. :meat_on_bone:**')
        await channel.edit(bitrate = 8000)
    else:
        await ctx.send('**You have to suffer with them if you want me to start. :smiling_imp:**')

@client.command()
async def repair(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice
    if channel:
        channel = ctx.message.author.voice.channel
        channel_name = channel.name
        channel_bitrate = ctx.guild.bitrate_limit
        await ctx.send('**`' + channel_name + '` has been repaired. :tools:**')
        await channel.edit(bitrate = channel_bitrate)
    else:
        await ctx.send('**Please join a channel in order to repair it.**')

@client.event
async def on_member_join(member):
    if member.guild.name == 'The Meme Surpreme':
        role = discord.utils.get(member.guild.roles, name = 'Soldat')
        await member.add_roles(role)


@client.command()
async def commands(ctx):
    user = ctx.message.author.mention
    await ctx.send(user + ''' My commands are...
        :skull:   **,annoy** - Makes people want to die.
        :octagonal_sign:   **,stop** - Stops making people want to die.
        :game_die:   **,jumble** - You won't have any friends after you type this.
        :meat_on_bone:   **,degrade** - Turns the voice chat into a ham radio.
        :tools:   **,repair** - Repairs your sins.
    ''')


client.run(TOKEN)
