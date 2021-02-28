import discord
from discord.ext import commands
from utils import config, async_tasks
from models import timer


class TimedCommands(commands.Cog, name="Timed Commands"):
    """ Timer commands for StudyBot. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set-timer", aliases=['st'])
    async def set_timer(self, ctx, time: str, *msg: str):
        """ Creates a Timer instance. """

        userid = ctx.message.author.id

        # Timer creation
        msg = ' '.join(msg)
        timer_obj = timer.Timer(userid=userid, time_delta_mins=int(time), msg=msg, discord_message=ctx.message)

        # P-queue update
        config.timer_pqueue.add_task(timer_obj)
        await ctx.send("Timer created!")
        await async_tasks.handle_timers()

    @commands.command(name="get-highest-timer", aliases=['ght'])
    async def highest_timer(self, ctx):
        """ Sends Timer information for nearest pending Timer instance. """

        userid = ctx.message.author.id
        top_timer = config.timer_pqueue.peek()
        await ctx.send(repr(top_timer))

    @commands.command(name="timer-queue", aliases=['tq'])
    async def timer_queue(self, ctx):
        """ Sends information for all pending Timer instances. """

        await ctx.send(repr(config.timer_pqueue.get_all_tasks()))

    @commands.command(name="unset-timer", aliases=['ut'])
    async def unset_timer(self, ctx, idx: str):
        """ Destroys Timer instance. """

        pass


def setup(bot):
    bot.add_cog(TimedCommands(bot))  # automatically called by load_extension() in 'main.py'
