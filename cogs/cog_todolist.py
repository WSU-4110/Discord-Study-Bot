import discord
from discord.ext import commands
from utils import config as cfg
from utils import todolist_priority_queue
from models import todolist


class ToDoListCommands(commands.Cog, name="ToDoList Commands"):
    """These are the ToDoList commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="create-item", aliases=["todo"])  # command to create a note
    async def create_item(self, ctx, time: str, *msg: str):
        """ Creates a ToDoList item."""
        userid = ctx.author.id

        # Timer creation
        msg = ' '.join(msg)
        item = todolist.ToDoList(userid=userid, td_secs=int(time) * 60, msg=msg, discord_message=ctx.message)

        # P-queue and database update
        todolist_priority_queue.ToDoListPriorityQueue.get_instance().add_task(item)
        # item.insert(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg'])

        await ctx.send(embed=discord.Embed(
            description="ToDoList Item created!\n",
            colour=cfg.colors.SUCCESS
        ))
        # await async_tasks.handle_timers()

    @commands.command(name="todolist-queue", aliases=['td'])
    async def timer_queue(self, ctx):
        """ Sends information for all pending ToDoList instances. """

        userid = ctx.author.id

        if userid in cfg.author_ids:
            await ctx.send(repr(todolist_priority_queue.ToDoListPriorityQueue.get_instance().get_all_tasks()))
        else:
            await ctx.send("Not authorized to use this command!")


def setup(bot):
    bot.add_cog(ToDoListCommands(bot))  # automatically called by load_extension() in 'main.py'
