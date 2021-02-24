import discord
from discord.ext import commands
from utils import config, async_tasks, reminder, timeutils


class ReminderCommands(commands.Cog, name="Reminder Commands"):
    '''These are reminder commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set-reminder", aliases=["sr"])
    async def set_reminder(self, ctx, day: str, hour: int, minute: int, *msg: str):
        '''Grabs user reminder data and pushes it to the time priority que'''
        userid = ctx.message.author.id
        if tz := msg[0] in timeutils.tz_map:
            msg_str = ' '.join(msg[1:])
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, tz)
        else:
            msg_str = ' '.join(msg)
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute)
        config.timer_pqueue.add_task(reminder_obj)
        await ctx.send("Reminder created!")
        await async_tasks.handle_timers()


def setup(bot):
    bot.add_cog(ReminderCommands(bot))
