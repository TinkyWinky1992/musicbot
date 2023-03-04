import discord
from discord.ext import commands
import os
from help_cog import help_cog
from music_cog import music_cog

bot_music = commands.Bot(command_prefix='.')
bot_music.remove_command('help')

bot_music.add_cog(help_cog(bot_music))
bot_music.add_cog(music_cog(bot_music))
os.environ["TOKEN"]="MTA4MTUzMDM2NzE2NjY1NjYyMg.GAhC4m.YgLdW6QlO3f35uPv6_OrSdCv9shmW27Sjf7jrc"
bot_music.run(os.environ.get("TOKEN"))
