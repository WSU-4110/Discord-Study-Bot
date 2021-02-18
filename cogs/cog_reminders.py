import discord
from discord.ext import commands
from utils import config, async_tasks, reminder


class ReminderCommands(commands.Cog, name="Reminder Commands"):
    '''These are reminder commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set-reminder", aliases=["sr"])
    async def set_reminder(self, ctx, day: str, hour: int, minute: int, *msg: str):
        userid = ctx.message.author.id
        msg = ' '.join(msg)
        reminder_obj = reminder.Reminder(userid, msg, ctx.message, day, hour, minute)
        config.timer_pqueue.add_task(reminder_obj)
        await ctx.send("Reminder created!")
        await async_tasks.handle_timers()

def setup(bot):
    bot.add_cog(ReminderCommands(bot))