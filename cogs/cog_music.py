import discord
from discord.ext import commands
import youtube_dl
import os
from factories.embedfactory import EmbedFactory
from utils import music_queue, config


# from utils.config import music_dict, colors


class MusicCommands(commands.Cog, name="Music Commands"):
    """ These are music commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url: str):
        """ Plays sounds with youtube video link """

        guild = ctx.guild
        file_name = f"song_{guild}.mp3"

        song_there = os.path.isfile(file_name)
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

        music_queue.MusicQueue.get_instance().add_url(url, guild.id, ctx)

        voice = discord.utils.get(self.bot.voice_clients, guild=guild)
        if not voice.is_playing() or not config.server_playing_music[guild.id]:
            try:
                if song_there:
                    os.remove(file_name)
            except PermissionError:
                await ctx.send("Wait for the current playing music to end or use the 'stop' command")
                return

            await EmbedFactory.success(ctx, "Downloading! please wait a moment...")

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([music_queue.MusicQueue.get_instance().get_top(guild.id)])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, file_name)
            await EmbedFactory.success(ctx, "Playing track!")
            voice.play(discord.FFmpegPCMAudio(file_name))
            config.server_playing_music[guild.id] = True
        else:
            pass

    @commands.command()
    async def leave(self, ctx):
        """ Bot disconnects from voice channel """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            music_queue.MusicQueue.get_instance().clear_for(ctx.guild.id)
            await voice.disconnect()
        else:
            await EmbedFactory.error(ctx, "The bot is not connected to a voice channel.")

    @commands.command()
    async def pause(self, ctx):
        """ pauses music in voice channel """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await EmbedFactory.success(ctx, "Paused track!")
        else:
            await EmbedFactory.error(ctx, "Currently no audio is playing.")

    @commands.command()
    async def resume(self, ctx):
        """ resumes music in voice channel """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            await EmbedFactory.success(ctx, "Resumed track!")
            voice.resume()
        else:
            await EmbedFactory.error(ctx, "The audio is not paused.")

    @commands.command()
    async def stop(self, ctx):
        """ stops playing music (allows for song change) """
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await EmbedFactory.success(ctx, "Stopped track!")


def setup(bot):
    bot.add_cog(MusicCommands(bot))
