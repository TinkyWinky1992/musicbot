from discord.ext import commands
import yt_dlp
import discord
import asyncio
import os



ffmpeg_options = {
    'options': '-vn',
}

ydl_opts = {
    'socket_timeout': 1000,  # Increase the timeout to 1000 seconds
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}




class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice =None
        self.queue =[]


    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel or ctx.auhtor.voice.channel != channel:
            if not ctx.author.voice:
                await ctx.send("You are not connected to a voice channel.")
                return
            channel = ctx.author.voice.channel

        if self.voice and self.voice.is_connected():
            await self.voice.move_to(channel)
        else:
            self.voice = await channel.connect()

        await ctx.send(f"Joined {channel.name}.")



    @commands.command()
    async def play(self,ctx,song_name):
        self.queue.append(song_name)
        await ctx.send(f"Added '{song_name}' to the Queue")

        if len(self.queue) == 1:
            await self.play_next(ctx)
    
    #function that play the music in the queue
    async def play_next(self, ctx):
        # If the queue is empty, return
        if not self.queue:
            return

        # Get the first song in the queue
        song_name = self.queue[0]

        # Check if the bot is already in a voice channel
        if not ctx.voice_client:
            # If not, get the voice channel of the person who issued the command
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            # If the bot is already in a voice channel, move it to the channel of the person who issued the command
            await ctx.voice_client.move_to(ctx.author.voice.channel)

        async with ctx.typing():
            # Search for the song by name
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                results = ydl.extract_info(f"ytsearch:{song_name}", download=False)
                await ctx.send(f"Playing '{song_name}'")
                if not results:
                    await ctx.send("No results found.")
                    return

                # Get the first result and its url
                song_url = results['entries'][0]['webpage_url']

            # Download the audio and get the file path
            info = ydl.extract_info(song_url, download=True)
            filename = ydl.prepare_filename(info)

            # Play the audio
            source = discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename, **ffmpeg_options)
            ctx.voice_client.play(source)

            # Wait until the audio is finished playing
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

            # Remove the first song from the queue
            self.queue.pop(0)

            # Start playing the next song in the queue
            await self.play_next(ctx)

            # Disconnect from the voice channel after the audio is finished playing
            await ctx.voice_client.disconnect()

            # Delete the audio file
            os.remove(filename)



    @commands.command(name="stop")
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        if ctx.voice_client and ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect()
            await ctx.send("Stopped playback and disconnected from voice channel.")
        else:
            await ctx.send("Not currently connected to a voice channel.")

        # Clear the queue
        self.queue = []

        # Indent the for loop to execute it regardless of the if statement above
        for file in os.listdir("C:/Users/USER/Project studioCode"):
            if file.endswith(".m4a"):
                filename=file
                os.remove(filename)



   
         