import discord
from discord.ext import commands
from utils import config, async_tasks, time_utils
from models import reminder


class ReminderCommands(commands.Cog, name="Reminder Commands"):
    '''These are reminder commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set-reminder", aliases=["sr"])
    async def set_reminder(self, ctx, day: str, hour: int, minute: int, *msg: str):
        """ (sr) Grabs user reminder data and pushes it to the time priority que """
        userid = ctx.message.author.id
        if tz := msg[0] in time_utils.tz_map:
            msg_str = ' '.join(msg[1:])
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, 0, tz)
        else:
            msg_str = ' '.join(msg)
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, 0)

        reminder_obj.insert(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg', 'recurrence'])

        config.timer_pqueue.add_task(reminder_obj)
        await ctx.send("Reminder created!")
        # await async_tasks.handle_timers()

    @commands.command(name="set-infinite-reminder", aliases=["sir"])
    async def set_infinite_reminder(self, ctx, day: str, hour: int, minute: int, *msg: str):
        """ (sir) Grabs user reminder data and pushes it to the time priority que """
        userid = ctx.message.author.id
        if tz := msg[0] in time_utils.tz_map:
            msg_str = ' '.join(msg[1:])
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, -1, tz)
        else:
            msg_str = ' '.join(msg)
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, -1)

        reminder_obj.insert(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg', 'recurrence'])

        config.timer_pqueue.add_task(reminder_obj)
        await ctx.send("Reminder created!")
        # await async_tasks.handle_timers()

    @commands.command(name="set-repetitive-reminder", aliases=["srr"])
    async def set_repetitive_reminder(self, ctx, day: str, hour: int, minute: int, repetitions: int, *msg: str):
        """ (srr) Grabs user reminder data and pushes it to the time priority que """
        userid = ctx.message.author.id
        if tz := msg[0] in time_utils.tz_map:
            msg_str = ' '.join(msg[1:])
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, int(repetitions), tz)
        else:
            msg_str = ' '.join(msg)
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, int(repetitions))

        reminder_obj.insert(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg', 'recurrence'])

        config.timer_pqueue.add_task(reminder_obj)
        await ctx.send("Reminder created!")
        # await async_tasks.handle_timers()


def setup(bot):
    bot.add_cog(ReminderCommands(bot))
