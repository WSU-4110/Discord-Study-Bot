import discord
from discord.ext import commands
from utils import config as cfg, time_utils, timer_priority_queue
from models import reminder


class ReminderCommands(commands.Cog, name="Reminder Commands"):
    '''These are reminder commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set-reminder", aliases=["sr"])
    async def set_reminder(self, ctx):
        """ (sr) Grabs user reminder data and pushes it to the time priority que """
        # asks user for day of week
        embed = discord.Embed(title="Which day of the week?",
                              description="Please type in the one of the following short-forms:",
                              color=cfg.colors.WSU_GOLD)
        embed.add_field(name="Monday:", value="m", inline=False)
        embed.add_field(name="Tuesday:", value="t", inline=False)
        embed.add_field(name="Wednesday:", value="w", inline=False)
        embed.add_field(name="Thursday:", value="th", inline=False)
        embed.add_field(name="Friday:", value="f", inline=False)
        embed.add_field(name="Saturday:", value="s", inline=False)
        embed.add_field(name="Sunday:", value="su", inline=False)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        day = await self.bot.wait_for('message',
                                      timeout=60.0,
                                      check=lambda message: message.author == ctx.author)
        day = day.content

        # asks user for what time
        embed = discord.Embed(title="What time?",
                              description="Use military time!\nexamples:\n9 25\n17 30",
                              color=cfg.colors.WSU_GOLD)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        time_msg = await self.bot.wait_for('message',
                                           timeout=60.0,
                                           check=lambda message: message.author == ctx.author)
        time_msg = time_msg.content.split(' ')
        hour = int(time_msg[0])
        minute = int(time_msg[1])

        # asks user for message
        embed = discord.Embed(title="What would you like to be reminded of?",
                              description="example: Time for software engineering lab class",
                              color=cfg.colors.WSU_GOLD)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        msg = await self.bot.wait_for('message',
                                      timeout=60.0,
                                      check=lambda message: message.author == ctx.author)
        msg = msg.content.split(' ')

        # create reminder object and store to database
        userid = ctx.message.author.id
        msg_str = ' '.join(msg)
        if tz := msg[0] in time_utils.tz_map:
            msg_str = ' '.join(msg[1:])
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, 0, tz)
        else:
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, 0)

        reminder_obj.insert(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg', 'recurrence'])
        timer_priority_queue.TimerPriorityQueue.get_instance().add_task(reminder_obj)

        # output
        embed = discord.Embed(title="Reminder Created!",
                              description=repr(reminder_obj),
                              color=cfg.colors.SUCCESS)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="set-infinite-reminder", aliases=["sir"])
    async def set_infinite_reminder(self, ctx):
        """ (sir) Grabs user reminder data and pushes it to the time priority que """
        # asks user for day of week
        embed = discord.Embed(title="Which day of the week?",
                              description="Please type in the one of the following short-forms:",
                              color=cfg.colors.WSU_GOLD)
        embed.add_field(name="Monday:", value="m", inline=False)
        embed.add_field(name="Tuesday:", value="t", inline=False)
        embed.add_field(name="Wednesday:", value="w", inline=False)
        embed.add_field(name="Thursday:", value="th", inline=False)
        embed.add_field(name="Friday:", value="f", inline=False)
        embed.add_field(name="Saturday:", value="s", inline=False)
        embed.add_field(name="Sunday:", value="su", inline=False)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        day = await self.bot.wait_for('message',
                                      timeout=60.0,
                                      check=lambda message: message.author == ctx.author)
        day = day.content

        # asks user for what time
        embed = discord.Embed(title="What time?",
                              description="Use military time!\nexamples:\n9 25\n17 30",
                              color=cfg.colors.WSU_GOLD)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        time_msg = await self.bot.wait_for('message',
                                           timeout=60.0,
                                           check=lambda message: message.author == ctx.author)
        time_msg = time_msg.content.split(' ')
        hour = int(time_msg[0])
        minute = int(time_msg[1])

        # asks user for message
        embed = discord.Embed(title="What would you like to be reminded of?",
                              description="example: Time for software engineering lab class",
                              color=cfg.colors.WSU_GOLD)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        msg = await self.bot.wait_for('message',
                                      timeout=60.0,
                                      check=lambda message: message.author == ctx.author)
        msg = msg.content.split(' ')

        userid = ctx.message.author.id
        if tz := msg[0] in time_utils.tz_map:
            msg_str = ' '.join(msg[1:])
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, -1, tz)
        else:
            msg_str = ' '.join(msg)
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, -1)

        reminder_obj.insert(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg', 'recurrence'])

        timer_priority_queue.TimerPriorityQueue.get_instance().add_task(reminder_obj)

        # output
        embed = discord.Embed(title="Reminder Created!",
                              description=repr(reminder_obj),
                              color=cfg.colors.SUCCESS)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="set-repetitive-reminder", aliases=["srr"])
    async def set_repetitive_reminder(self, ctx):
        """ (srr) Grabs user reminder data and pushes it to the time priority que """
        # asks user for day of week
        embed = discord.Embed(title="Which day of the week?",
                              description="Please type in the one of the following short-forms:",
                              color=cfg.colors.WSU_GOLD)
        embed.add_field(name="Monday:", value="m", inline=False)
        embed.add_field(name="Tuesday:", value="t", inline=False)
        embed.add_field(name="Wednesday:", value="w", inline=False)
        embed.add_field(name="Thursday:", value="th", inline=False)
        embed.add_field(name="Friday:", value="f", inline=False)
        embed.add_field(name="Saturday:", value="s", inline=False)
        embed.add_field(name="Sunday:", value="su", inline=False)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        day = await self.bot.wait_for('message',
                                      timeout=60.0,
                                      check=lambda message: message.author == ctx.author)
        day = day.content

        # asks user for what time
        embed = discord.Embed(title="What time?",
                              description="Use military time!\nexamples:\n9 25\n17 30",
                              color=cfg.colors.WSU_GOLD)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        time_msg = await self.bot.wait_for('message',
                                           timeout=60.0,
                                           check=lambda message: message.author == ctx.author)
        time_msg = time_msg.content.split(' ')
        hour = int(time_msg[0])
        minute = int(time_msg[1])

        # asks user for message
        embed = discord.Embed(title="What would you like to be reminded of?",
                              description="example: Time for software engineering lab class",
                              color=cfg.colors.WSU_GOLD)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        msg = await self.bot.wait_for('message',
                                      timeout=60.0,
                                      check=lambda message: message.author == ctx.author)
        msg = msg.content.split(' ')

        # asks user for message
        embed = discord.Embed(title="How many weeks should the reminder repeat?",
                              description="example: 3",
                              color=cfg.colors.WSU_GOLD)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        repetitions = await self.bot.wait_for('message',
                                              timeout=60.0,
                                              check=lambda message: message.author == ctx.author)
        repetitions = repetitions.content

        userid = ctx.message.author.id
        if tz := msg[0] in time_utils.tz_map:
            msg_str = ' '.join(msg[1:])
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, int(repetitions), tz)
        else:
            msg_str = ' '.join(msg)
            reminder_obj = reminder.Reminder(userid, msg_str, ctx.message, day, hour, minute, int(repetitions))

        reminder_obj.insert(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg', 'recurrence'])

        timer_priority_queue.TimerPriorityQueue.get_instance().add_task(reminder_obj)

        # output
        embed = discord.Embed(title="Reminder Created!",
                              description=repr(reminder_obj),
                              color=cfg.colors.SUCCESS)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ReminderCommands(bot))
