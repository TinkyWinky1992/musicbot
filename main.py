from discord.ext import commands
from help_cog import help_cog
from music_cog import Music
from dotenv import load_dotenv
import discord
import asyncio
import os






intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description='Relatively simple music bot example',
    intents=intents,
)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')



intents = discord.Intents.all()
bot_music = commands.Bot(command_prefix='!',intents=intents)
bot_music.remove_command('help')


async def setup():

    await bot_music.add_cog(help_cog(bot_music))
    await bot_music.add_cog(Music(bot_music))





load_dotenv()
loop=asyncio.get_event_loop()   
loop.run_until_complete(setup())
bot_music.run(os.getenv("TOKEN"))   