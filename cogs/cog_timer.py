import discord
from discord.ext import commands
from utils import config as cfg, async_tasks
from models import timer
from typing import *


class TimedCommands(commands.Cog, name="Timed Commands"):
    """ Timer commands for StudyBot. """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set-timer", aliases=['st'])
    async def set_timer(self, ctx, time: str, *msg: str):
        """ Creates a Timer instance. """

        userid = ctx.author.id

        # Timer creation
        msg = ' '.join(msg)
        timer_obj = timer.Timer(userid=userid, td_secs=int(time) * 60, msg=msg, discord_message=ctx.message)

        # P-queue and database update
        cfg.timer_pqueue.add_task(timer_obj)
        timer_obj.insert(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg'])

        await ctx.send("Timer created!")
        # await async_tasks.handle_timers()

    @commands.command(name="list-timers", aliases=['lt'])
    async def list_timers(self, ctx, limit=None):

        # Identify users and fetch their timers
        userid = ctx.author.id
        user_timers = sorted(
            [obj for obj in cfg.timer_pqueue.user_map[userid] if type(obj) == timer.Timer]
        )

        # Sanitize limit input (always keep in range [-length + 1 .. length - 1] inc.)
        if limit is not None:
            limit = int(limit)
            limit = min(max(limit, -len(user_timers) + 1), len(user_timers))

        await ctx.send('\n'.join(map(str, user_timers[:limit:])))

    @commands.command(name="highest-timer", aliases=['ht'])
    async def highest_timer(self, ctx):
        """ Sends Timer information for nearest pending Timer instance. """

        # Identify users and fetch their timers
        userid = ctx.author.id
        user_timers = sorted(
            [obj for obj in cfg.timer_pqueue.user_map[userid] if type(obj) == timer.Timer]
        )

        if not user_timers:
            await ctx.send("You don't have any timers!")
        else:
            await ctx.send(user_timers[0])

        # userid = ctx.message.author.id
        # top_timer = cfg.timer_pqueue.peek()
        # await ctx.send(repr(top_timer))

    @commands.command(name="unset-timer", aliases=['ut'])
    async def unset_timer(self, ctx, idx: str):
        """ Destroys Timer instance. """

        # Identify users and fetch their timers
        userid = ctx.author.id
        user_timers = sorted(
            [obj for obj in cfg.timer_pqueue.user_map[userid] if type(obj) == timer.Timer]
        )

        idx = int(idx)

        if not user_timers:
            await ctx.send("You don't have any timers!")
        elif not 1 <= idx <= len(user_timers):
            await ctx.send(f"Index input not in range! ({idx} not in [{1} .. {len(user_timers)}])")
        else:
            # delete from database
            target = user_timers[idx - 1]
            target.delete(target.message_id)
            cfg.timer_pqueue.remove_timer(target.message_id)
            await ctx.send("Timer deleted!")

    @commands.command(name="unset-highest-timer", aliases=['uht'])
    async def unset_highest_timer(self, ctx):
        """ Delete the top timer from the priority queue. """

        await self.unset_timer(ctx, str(1))

        # userid = ctx.message.author.id
        # top_timer = cfg.timer_pqueue.peek()
        # removed_top_timer = cfg.timer_pqueue.remove_timer(top_timer.message_id)
        # await ctx.send(repr(removed_top_timer))

    @commands.command(name="timer-queue", aliases=['tq'])
    async def timer_queue(self, ctx):
        """ Sends information for all pending Timer instances. """

        userid = ctx.author.id

        if userid in cfg.author_ids:
            await ctx.send(repr(cfg.timer_pqueue.get_all_tasks()))
        else:
            await ctx.send("Not authorized to use this command!")


def setup(bot):
    bot.add_cog(TimedCommands(bot))  # automatically called by load_extension() in 'main.py'
