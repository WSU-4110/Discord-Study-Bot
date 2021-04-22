import discord
from discord.ext import commands
from utils import database_utils as dbutils, config as cfg
from models import ticket
import asyncio
from factories.embedfactory import EmbedFactory


class TicketCommands(commands.Cog, name='Ticket Commands'):
    """
    Ticket commands for StudyBot; setting up user-private ticket channels for Q&A.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup-tickets")
    async def setup_tickets(self, ctx):
        """
        Initializes the Ticket category used for tickets in the server.
        """

        # Get server from the context of the command
        guild = ctx.guild

        # If this server already has a ticket category, exit
        if cfg.server_ticket_ctgs.get(guild.id) is not None:
            # await ctx.send(embed=discord.Embed(
            #     description="This server already has tickets set up!",
            #     colour=cfg.colors.ERROR
            # ))
            await EmbedFactory.error(ctx, "This server already has tickets set up!")
            return

        # Prompt the user for the name of the ticket category to be made, cancel if it times out
        # await ctx.send(embed=discord.Embed(
        #     description="Enter the name for the ticket category for this server.",
        #     colour=cfg.colors.WSU_GOLD
        # ))
        #
        # try:
        #     response = await self.bot.wait_for('message', check=lambda rctx: rctx.author == ctx.author, timeout=60)
        # except asyncio.TimeoutError as e:
        #     await ctx.send(embed=discord.Embed(
        #         description="Took too long to respond!",
        #         colour=cfg.colors.TIMEOUT
        #     ))
        #     return

        name = await EmbedFactory.prompt(ctx, self.bot, "Enter the name for the ticket category for this server.")
        if name is None:
            return

        # Overwrites object to specify permissions the category will use
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }

        # Creating, logging ticket and storing it in the DB
        category = await ctx.guild.create_category(name, overwrites=overwrites)
        cfg.server_ticket_ctgs[guild.id] = category.id

        # Connect to DB and write data
        con = dbutils.connection()
        cursor = con.cursor(buffered=True)
        cursor.execute(
            "INSERT INTO SERVER_TICKET_CATEGORIES (server_id, category_id) values (%s, %s)", (guild.id, category.id))
        con.commit()
        cursor.close()

        # await ctx.send(embed=discord.Embed(
        #     description="Ticket category created!",
        #     colour=cfg.colors.SUCCESS
        # ))

        await EmbedFactory.success(ctx, "Ticket category created!")

    @commands.command(name="create-ticket", aliases=["ctkt"])
    async def create_ticket(self, ctx):
        """
        Initializes private ticket creation and setup.
        """

        # Get user and server from context of the command
        userid = ctx.author.id
        msgid = ctx.message.id
        guild = ctx.guild

        # Get ticket category (if not exists, exit)
        category_id = cfg.server_ticket_ctgs.get(guild.id)
        if category_id is None:
            # await ctx.send(embed=discord.Embed(
            #     description="This server doesn't have a ticket category set up yet! Use `setup-tickets` to make one.",
            #     colour=cfg.colors.ERROR
            # ))
            await EmbedFactory.error(ctx,
                                     "This server doesn't have a ticket category set up yet! Use `setup-tickets` to make one.")
            return

        # Generate new channel just for the requesting user (or tell the user to make a ticket category)
        ticket_channel = await guild.create_text_channel(name=ctx.author.display_name,
                                                         category=discord.utils.get(guild.categories,
                                                                                    id=category_id))

        # Set the permissions of the channel such that only the requesting user can see it
        await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=False, embed_links=True,
                                             attach_files=True)

        # q_prompt = await ticket_channel.send(ctx.author.mention, embed=discord.Embed(
        #     description="Type in your question here.",
        #     colour=cfg.colors.WSU_GOLD
        # ))
        #
        # try:
        #     q_response = await self.bot.wait_for('message', check=lambda
        #         rctx: rctx.author == ctx.author and rctx.channel.id == ticket_channel.id, timeout=300)
        # except asyncio.TimeoutError as e:
        #     await ctx.send(embed=discord.Embed(
        #         description="Took too long to respond!",
        #         colour=cfg.colors.TIMEOUT
        #     ))
        #     ticket_channel.delete()
        #     return

        # Continue setup in the ticket channel by prompting user for their question, delete everything if timed out
        question = await EmbedFactory.prompt(ticket_channel, self.bot, "Type in your question here.", check=lambda
            rctx: rctx.author == ctx.author and rctx.channel.id == ticket_channel.id,
                                             body=ctx.author.mention, timeout=300, delete=True)
        print(question)
        if question is None:
            await ticket_channel.delete()
            return

        # r_prompt = await ticket_channel.send(embed=discord.Embed(
        #     description="Which roles would you like to ping with this question? Separate each ping with spaces.",
        #     colour=cfg.colors.WSU_GOLD
        # ))
        #
        # try:
        #     r_response = await self.bot.wait_for('message', check=lambda
        #         rctx: rctx.author == ctx.author and rctx.channel.id == ticket_channel.id, timeout=30)
        # except asyncio.TimeoutError as e:
        #     await ctx.send(embed=discord.Embed(
        #         description="Took too long to respond!",
        #         colour=cfg.colors.TIMEOUT
        #     ))
        #     ticket_channel.delete()
        #     return

        # Prompt users for the roles they want to ping in the question statement, delete everything if timed out
        roles = await EmbedFactory.prompt(ticket_channel, self.bot,
                                          "Which roles would you like to ping with this question? Separate each ping with spaces.",
                                          check=lambda
                                              rctx: rctx.author == ctx.author and rctx.channel.id == ticket_channel.id,
                                          delete=True)
        if roles is None:
            await ticket_channel.delete()
            return

        roles = roles.split()

        # # Extract text from question and roles responses
        # question = q_response.content
        # roles = r_response.content.split()

        # For each specific role, give it read/send/link/file permissions
        for role_string in roles:
            await ticket_channel.set_permissions(discord.utils.get(guild.roles, mention=role_string),
                                                 read_messages=True,
                                                 send_messages=True,
                                                 embed_links=True,
                                                 attach_files=True)

        # Creating, logging and storing ticket in DB
        new_ticket = ticket.Ticket(msgid, userid, ticket_channel.id, question, roles)
        new_ticket.insert(["message_id", "user_id", "channel_id", "question", "roles"])
        cfg.ticket_channels[ticket_channel.id] = new_ticket

        # Display the question in a fancy embed
        await ticket_channel.send(' '.join(roles), embed=discord.Embed(
            title="Ticket Question",
            description=question,
            colour=cfg.colors.WSU_GREEN
        ).set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar_url
        ).set_footer(text=self.bot.user.display_name, icon_url=self.bot.user.avatar_url))

    @commands.command(name="resolve-ticket", aliases=["rtkt"])
    async def resolve_ticket(self, ctx, *, msg: str = None):
        """
        Resolves an existing ticket.
        Note: Use this in a ticket channel!
        """

        # Fetching relevant information (user, channel, server)
        guild = ctx.guild
        userid = ctx.author.id
        channelid = ctx.channel.id

        # Get the ticket object for this channel
        resolved_ticket = cfg.ticket_channels.get(channelid, None)

        # If the channel is not a ticket channel (no ticket associated with it), exit
        if resolved_ticket is None:
            # await ctx.send(embed=discord.Embed(
            #     description="Not a ticket channel!",
            #     colour=cfg.colors.ERROR
            # ))
            await EmbedFactory.error(ctx, "Not a ticket channel!")
            return

        # Notify creator of ticket the channel is deleted
        creator = discord.utils.get(guild.members, id=resolved_ticket.user_id)
        # await creator.send(embed=discord.Embed(
        #     description=f"Your ticket was resolved{'.' if not msg else f' with message: {msg}'}",
        #     colour=cfg.colors.WSU_GREEN
        # ))

        await EmbedFactory.success(creator, f"Your ticket was resolved{'.' if not msg else f' with message: {msg}'}")

        resolved_ticket.delete(resolved_ticket.message_id)
        del cfg.ticket_channels[channelid]
        await discord.utils.get(guild.channels, id=channelid).delete()


def setup(bot):
    bot.add_cog(TicketCommands(bot))
