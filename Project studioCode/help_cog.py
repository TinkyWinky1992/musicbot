import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot_music):
        self.bot = bot_music
        self.help_message = """
        ```
        General commands: 
        .p - To starting playing the music in the queue
        .pa - To Pause the music that corrently playing
        .r - To conntinue the music that is corrently on pause
        .s - To Skip the music 
        .q - To see  Every music in the queue
        .c - TO Clear the music
        .dis/d/l - To disconnecting the bot from the channel
        ```
        """
        self.text_channel_text = []

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)
        
        await self.send_to_all(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)

    @commands.command(name="greet", help="Greets the user if they are mentioned")
    async def greet(self, ctx):
        message = ctx.message
        if message.author.mentioned_in(message):
            await ctx.send(f"Hello {message.author.mention}!")
        else:
            await ctx.send("Please mention me in your message.")
