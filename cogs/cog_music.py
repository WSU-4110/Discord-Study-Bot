import discord
from discord.ext import commands
import youtube_dl
import os
from factories.embedfactory import EmbedFactory
# from utils.config import music_dict, colors


class MusicCommands(commands.Cog, name="Music Commands"):
    """ These are music commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url: str):
        """ Plays sounds with youtube video link """
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        vc = ctx.author.voice
        if vc is None:
            await EmbedFactory.error(ctx, "Not in a voice channel!")
            return

        # ignores if already in voice channel because the bot can only
        # be in 1 voice call per server due to discords bot api limitations
        try:
            await vc.channel.connect()
        except discord.ClientException:
            pass

        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        EmbedFactory.success(ctx, "Downloading! please wait a moment...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        EmbedFactory.success(ctx, "Playing Song!")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command()
    async def leave(self, ctx):
        """ Bot disconnects from voice channel """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            EmbedFactory.error(ctx, "The bot is not connected to a voice channel.")

    @commands.command()
    async def pause(self, ctx):
        """ pauses music in voice channel """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            EmbedFactory.success(ctx, "Paused!")
        else:
            EmbedFactory.error(ctx, "Currently no audio is playing.")

    @commands.command()
    async def resume(self, ctx):
        """ resumes music in voice channel """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            EmbedFactory.success(ctx, "Resumed!")
            voice.resume()
        else:
            EmbedFactory.error(ctx, "The audio is not paused.")

    @commands.command()
    async def stop(self, ctx):
        """ stops playing music (allows for song change) """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        EmbedFactory.success(ctx, "Stopped!")


def setup(bot):
    bot.add_cog(MusicCommands(bot))
