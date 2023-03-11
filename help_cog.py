import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot_music):
        self.bot = bot_music
        
        self.help_message = """
        ```
        General commands: 
        !play - To play the music
        !stop - To disconnecting the bot from the channel
        
        ```
        """
        self.text_channel_text = []

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)
        

  

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)
        
       

    @commands.Cog.listener()
    async def on_message(self,message):
        if self.bot.user.mentioned_in(message): 
            await message.channel.send(self.help_message)
