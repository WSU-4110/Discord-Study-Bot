import discord
from discord.ext import commands
from utils import config


class TicketCommands(commands.Cog, name='Ticket Commands'):
    """These are the ticket commands"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(TicketCommands(bot))
