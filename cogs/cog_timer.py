import discord
from discord.ext import commands
from utils import config as cfg, time_utils, timer_priority_queue
from models import timer
from factories.embedfactory import EmbedFactory


class TimedCommands(commands.Cog, name="Timed Commands"):
    """ Timer commands for StudyBot. """

    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        """
        This method is called before any command executes.
        """
        user = ctx.author
        if user.id not in cfg.user_tzs:  # if user has not set their timezone, add them to the DB
            await self.bot.get_cog("Profile Commands").init_user(ctx)

    @commands.command(name="set-timer", aliases=['st'])
    async def set_timer(self, ctx, time: str, *msg: str):
        """
        Creates a Timer instance.
        Note: 'time' must be in range [1 .. 120]
        """

        user = ctx.author

        # Verify time inputted is valid
        try:
            time = int(time)
        except ValueError:  # not an integer
            await EmbedFactory.error(ctx, "Non-numeric timer duration given!")
            return

        if not 1 <= time <= 120:  # not in allowed range of integers
            await EmbedFactory.error(ctx, "Timer duration not in acceptable range! [1 .. 120]")
            return

        # Timer creation
        msg = ' '.join(msg)
        timer_obj = timer.Timer(userid=user.id, td_secs=int(time) * 60, msg=msg, discord_message=ctx.message)

        # P-queue and database update
        timer_priority_queue.TimerPriorityQueue.get_instance().add_task(timer_obj)
        timer_obj.insert(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg'])

        await EmbedFactory.success(ctx, "Timer created!")

    @commands.command(name="list-timers", aliases=['lt'])
    async def list_timers(self, ctx, limit=None):
        """
        Lists all active timers created by the user.
        Note: +limit -> earliest timers, -limit -> latest timers
        """

        # Identify user and fetch their timers
        user = ctx.author
        user_timers = sorted(
            [obj for obj in timer_priority_queue.TimerPriorityQueue.get_instance().user_map.get(user.id, []) if
             type(obj) == timer.Timer]
        )

        # if the user has no timers, exit
        if not user_timers:
            await EmbedFactory.error(ctx, "No timers found!")
            return

        # Sanitize limit input
        if limit is not None:
            limit = int(limit)
            limit = min(max(limit, -len(user_timers) + 1), len(user_timers))  # always keep in range [-len+1 .. len]

        # Create base embed
        embed = discord.Embed(
            title="Active Timers",
            description=f"Listing timer information for {ctx.author.mention}.",
            colour=cfg.colors.WSU_GREEN
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        ).set_footer(text=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)

        # Add new fields for every timer instance
        for i, t in enumerate(user_timers[:limit], 1):
            embed.add_field(
                name=f"Timer __{i}__",  # number
                value=t.msg,  # message
                inline=True
            ).add_field(
                name=f"Expires At",
                value=time_utils.utc_to_dest(t.end_time, cfg.user_tzs[user.id]).strftime("%c"),  # expiration date
                inline=True
            ).add_field(  # empty inline field to allow wrapping of each timer field group
                name='\u200b',
                value='\u200b',
                inline=True
            )

        await ctx.send(embed=embed)

    @commands.command(name="highest-timer", aliases=['ht'])
    async def highest_timer(self, ctx):
        """
        Sends detailed Timer information for the top timer.
        """

        # Identify user and fetch their timers
        user = ctx.author
        user_timers = sorted(
            [obj for obj in timer_priority_queue.TimerPriorityQueue.get_instance().user_map.get(user.id, []) if
             type(obj) == timer.Timer]
        )

        # If user has no timers, exit
        if not user_timers:
            await EmbedFactory.error(ctx, "No timers found!")
            return

        t = user_timers[0]  # earliest expiring timer

        embed = discord.Embed(
            title="Detailed Timer Information",
            colour=cfg.colors.WSU_GREEN
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        ).add_field(  # message
            name="Message",
            value=t.msg,
            inline=False
        ).add_field(  # creation date
            name="Created at",
            value=time_utils.utc_to_dest(t.start_time, cfg.user_tzs[user.id]).strftime("%c"),
            inline=True
        ).add_field(  # expiration date
            name="Expires at",
            value=time_utils.utc_to_dest(t.end_time, cfg.user_tzs[user.id]).strftime("%c"),
            inline=True
        ).set_footer(text=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="unset-timer", aliases=['ut'])
    async def unset_timer(self, ctx, idx: str):
        """
        Destroys Timer instance.
        Note: 'idx' must be in range [1 .. n] where n is number of active timers
        It is suggested to use 'list-timers' before using this command.
        """

        # Identify user and fetch their timers
        user = ctx.author
        user_timers = sorted(
            [obj for obj in timer_priority_queue.TimerPriorityQueue.get_instance().user_map.get(user.id, []) if
             type(obj) == timer.Timer]
        )

        # If user has no timers, exit
        if not user_timers:
            await EmbedFactory.error(ctx, "No timers found!")
            return

        # Validate index input
        try:
            idx = int(idx)
        except ValueError:  # not an integer
            await EmbedFactory.error(ctx, "Non-numeric index given!")
            return

        if not 1 <= idx <= len(user_timers):  # not in accepted range
            await ctx.send(embed=discord.Embed(
                description=f"Index input not in range! Range [1 .. {len(user_timers)}], got {idx}",
                colour=cfg.colors.ERROR
            ))

        else:
            # Delete from database
            target = user_timers[idx - 1]
            target.delete(target.message_id)
            timer_priority_queue.TimerPriorityQueue.get_instance().remove_timer(target.message_id)

            await EmbedFactory.success(ctx, "Timer deleted!")

    @commands.command(name="unset-highest-timer", aliases=['uht'])
    async def unset_highest_timer(self, ctx):
        """
        Deletes the top timer for the user.
        """

        await self.unset_timer(ctx, str(1))

    @commands.command(name="unset-all-timers", aliases=['uat'])
    async def unset_all_timers(self, ctx):
        """
        Deletes all timers for the user.
        """

        # Identify user and fetch their timers
        user = ctx.author
        user_timers = sorted(
            [obj for obj in timer_priority_queue.TimerPriorityQueue.get_instance().user_map.get(user.id, []) if
             type(obj) == timer.Timer]
        )

        # If user has no timers, exit
        if not user_timers:
            await EmbedFactory.error(ctx, "No timers found!")
        else:
            # Delete from database
            for target in user_timers:
                target.delete(target.message_id)
                timer_priority_queue.TimerPriorityQueue.get_instance().remove_timer(target.message_id)

            await EmbedFactory.success(ctx, "All timers deleted!")


def setup(bot):
    bot.add_cog(TimedCommands(bot))  # automatically called by load_extension() in 'main.py'
