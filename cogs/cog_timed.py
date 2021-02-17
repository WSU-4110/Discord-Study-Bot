import discord
from discord.ext import commands
from utils import timer, config, async_tasks


class TimedCommands(commands.Cog, name="Timed Commands"):
    """These are the timer commands"""

    def __init__(self, bot):
        self.bot = bot

    # *** commands begin below ***

    @commands.command(name="set-timer", aliases=['st'])
    async def set_timer(self, ctx, time: str, *msg: str):
        userid = ctx.message.author.id
        msg = ' '.join(msg)
        timer_obj = timer.Timer(userid=userid, time_delta_mins=int(time), msg=msg, discord_message=ctx.message)
        config.timer_pqueue.add_task(timer_obj)
        await ctx.send("Timer created!")
        await async_tasks.handle_timers()

    @commands.command(name="get-highest-timer", aliases=['ght'])
    async def highest_timer(self, ctx):
        userid = ctx.message.author.id
        top_timer = config.timer_pqueue.peek()
        await ctx.send(repr(top_timer))

    @commands.command(name="timer-queue", aliases=['tq'])
    async def timer_queue(self, ctx):
        await ctx.send(repr(config.timer_pqueue.get_all_tasks()))

    @commands.command(name="unset-timer", aliases=['ut'])
    async def unset_timer(self, ctx, idx: str):
        pass

    # *** commands end above ***


def setup(bot):
    bot.add_cog(TimedCommands(bot))
