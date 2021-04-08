import discord
from discord.ext import commands
from utils import config as cfg
from models import ticket
import asyncio


class TicketCommands(commands.Cog, name='Ticket Commands'):
    """These are the ticket commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup-tickets")
    async def setup_tickets(self, ctx):
        guild = ctx.guild

        await ctx.send(embed=discord.Embed(
            description="Enter the name for the ticket category for this server.",
            colour=cfg.colors.WSU_GOLD
        ))

        try:
            response = await self.bot.wait_for('message', check=lambda rctx: rctx.author == ctx.author, timeout=60)
        except asyncio.TimeoutError as e:
            await ctx.send(embed=discord.Embed(
                description="Took too long to respond!",
                colour=cfg.colors.TIMEOUT
            ))
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }

        category = await ctx.guild.create_category(response.content, overwrites=overwrites)

        cfg.server_ticket_ctgs[guild.id] = category.id

        await ctx.send(embed=discord.Embed(
            description="Ticket category created!",
            colour=cfg.colors.SUCCESS
        ))

    @commands.command(name="create-ticket", aliases=["ctkt"])
    async def create_ticket(self, ctx):
        userid = ctx.author.id
        guild = ctx.guild

        ticket_channel = await guild.create_text_channel(name=ctx.author.display_name,
                                                         category=discord.utils.get(guild.categories,
                                                                                    id=cfg.server_ticket_ctgs[
                                                                                        guild.id]))
        perms = ticket_channel.overwrites_for(ctx.author)
        await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=False, embed_links=True,
                                             attach_files=True)

        q_prompt = await ticket_channel.send(ctx.author.mention, embed=discord.Embed(
            description="Type in your question here.",
            colour=cfg.colors.WSU_GOLD
        ))

        try:
            q_response = await self.bot.wait_for('message', check=lambda
                rctx: rctx.author == ctx.author and rctx.channel.id == ticket_channel.id, timeout=300)
        except asyncio.TimeoutError as e:
            await ctx.send(embed=discord.Embed(
                description="Took too long to respond!",
                colour=cfg.colors.TIMEOUT
            ))
            ticket_channel.delete()
            return

        r_prompt = await ticket_channel.send(embed=discord.Embed(
            description="Which roles would you like to ping with this question? Separate each ping with spaces.",
            colour=cfg.colors.WSU_GOLD
        ))

        try:
            r_response = await self.bot.wait_for('message', check=lambda
                rctx: rctx.author == ctx.author and rctx.channel.id == ticket_channel.id, timeout=30)
        except asyncio.TimeoutError as e:
            await ctx.send(embed=discord.Embed(
                description="Took too long to respond!",
                colour=cfg.colors.TIMEOUT
            ))
            ticket_channel.delete()
            return

        question = q_response.content
        roles = r_response.content.split()

        for role_string in roles:
            await ticket_channel.set_permissions(discord.utils.get(guild.roles, mention=role_string),
                                                 read_messages=True,
                                                 send_messages=True,
                                                 embed_links=True,
                                                 attach_files=True)

        await q_prompt.delete()
        await q_response.delete()
        await r_prompt.delete()
        await r_response.delete()

        new_ticket = ticket.Ticket(userid, ticket_channel.id, question, roles)
        cfg.ticket_channel_dict[ticket_channel.id] = new_ticket

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
        guild = ctx.guild
        userid = ctx.author.id
        channelid = ctx.channel.id

        resolved_ticket = cfg.ticket_channel_dict.get(channelid, None)

        if resolved_ticket is None:
            await ctx.send(embed=discord.Embed(
                description="Not a ticket channel!",
                colour=cfg.colors.ERROR
            ))

        print(userid, resolved_ticket.userid)
        # if userid != resolved_ticket.userid:
        await ctx.author.send(embed=discord.Embed(
            description=f"Your ticket was resolved{'.' if not msg else f' with message: {msg}'}",
            colour=cfg.colors.WSU_GREEN
        ))

        del cfg.ticket_channel_dict[channelid]
        await discord.utils.get(guild.channels, id=channelid).delete()


def setup(bot):
    bot.add_cog(TicketCommands(bot))
