import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from utils import time_utils, config as cfg
from factories.embedfactory import EmbedFactory


class ProfileCommands(commands.Cog, name='Profile Commands'):
    """These are the commands that pertain to user profile initialization and customization."""

    def __init__(self, bot):
        self.bot = bot
        load_dotenv()

    @commands.command(name="init")
    async def init_user(self, ctx):
        """
        Initializes a user in the StudyBot System.
        """

        def check(rctx):
            return rctx.author == ctx.author

        await ctx.send(embed=discord.Embed(
            title="Welcome to StudyBot!",
            description="This process will help you set up your user information to get started with the StudyBot system.\n",
            colour=cfg.colors.WSU_GREEN
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        ).set_footer(text=self.bot.user.display_name, icon_url=self.bot.user.avatar_url))

        # await ctx.send(embed=discord.Embed(
        #     description="Please enter your time zone information as a 3-letter code (eg. EST, PST).\n",
        #     colour=cfg.colors.WSU_GOLD
        # ))

        while True:
            # try:
            #     response = await self.bot.wait_for('message', check=check, timeout=60)
            #     if await self.change_timezone(ctx, response.content):
            #         break
            # except asyncio.TimeoutError as e:
            #     await ctx.send(embed=discord.Embed(
            #         description="Took too long to respond!",
            #         colour=cfg.colors.TIMEOUT
            #     ))
            #     break

            tz = await EmbedFactory.prompt(ctx, self.bot,
                                           "Please enter your time zone information as a 3-letter code (eg. EST, PST)",
                                           check=check)
            if tz is None:
                return

            if await self.change_timezone(ctx, tz):
                break

    @commands.command(name="change-timezone", aliases=['change-tz', 'ctz'])
    async def change_timezone(self, ctx, tz: str) -> bool:
        """
        Changes the user's saved timezone.
        """

        if tz in time_utils.tz_map:
            await EmbedFactory.success(ctx, "nice")
            return True
        else:
            # await ctx.send(embed=discord.Embed(
            #     description="Time zone not recognized!",
            #     colour=cfg.colors.ERROR
            # ))
            await EmbedFactory.error(ctx, "Time zone not recognized!")
            return False

    @commands.command(name="display_score", aliases=['ds'])
    async def display_score(self, ctx):
        """
        Displays the user's participation scoreboard statistics.
        """

    @commands.command(name="userinfo", aliases=['ui'])
    async def userinfo(self, ctx):
        """
        Displays the user's general information.
        """

    @commands.command(name="send-feedback")
    async def send_feedback(self, ctx, *, msg):
        """
        Allows the user to send feedback to the developers of StudyBot.
        """

        channel_id = int(os.getenv("FEEDBACK_CHANNEL_ID"))
        server_id = int(os.getenv("FEEDBACK_SERVER_ID"))

        dev_guild = self.bot.get_guild(server_id)
        channel = discord.utils.get(dev_guild.text_channels, id=channel_id)

        await channel.send(embed=discord.Embed(
            title="New Feedback!",
            description=msg,
            colour=cfg.colors.WSU_GREEN
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        ))

        await EmbedFactory.success(ctx, "Your feedback has been sent!")


def setup(bot):
    bot.add_cog(ProfileCommands(bot))
