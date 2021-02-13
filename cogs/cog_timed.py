import discord
from discord.ext import commands


class TimedCommands(commands.Cog, name="Timed Commands"):
    """These are the timer commands"""

    def __init__(self, bot):
        self.bot = bot

    # *** commands begin below ***
    @commands.command(name="set-timer", aliases=['st'])
    async def set_timer(self, ctx, time: str, *msg: str):
        pass

    # *** commands end above ***


def setup(bot):
    bot.add_cog(TimedCommands(bot))
