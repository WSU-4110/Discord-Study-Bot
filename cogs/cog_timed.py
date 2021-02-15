import discord
from discord.ext import commands
from utils import timer, config


class TimedCommands(commands.Cog, name="Timed Commands"):
    """These are the timer commands"""

    def __init__(self, bot):
        self.bot = bot

    # *** commands begin below ***

    @commands.command(name="set-timer", aliases=['st'])
    async def set_timer(self, ctx, time: str, *msg: str):
        userid = ctx.message.author.id
        msg = ' '.join(msg)
        timer_obj = timer.Timer(userid=userid, initial_time=int(time), msg=' '.join(msg))
        config.timer_pqueue.add_task(timer_obj)
        await ctx.send("Timer created!")

    @commands.command(name="get-highest-timer", aliases=['ght'])
    async def highest_timer(self, ctx):
        userid = ctx.message.author.id
        top_timer = config.timer_pqueue.peek()
        await ctx.send(repr(top_timer))

    # *** commands end above ***


def setup(bot):
    bot.add_cog(TimedCommands(bot))
