import discord
from discord.ext import commands
from models import inspire


"""This cog uses the Inspire class to get appropriate quote and send to user"""

class InspireCommands(commands.Cog, name="Inspire Commands"):

    def __init__(self, bot):
        self.bot = bot

    # This command returns satirical quotes related to computer programming
    @commands.command(name="get-cs-satire", aliases=["css"])
    async def display_quote(self, ctx, discord_role: str = ''):
        # sanitize input and check if parameter is empty string or contains role
        check_param: bool
        if '<@&' in discord_role and '>' in discord_role:
            check_param = True
        elif discord_role == '':
            check_param = False
        else:
            await ctx.send("Invalid Input, Select New Quote")
            return
        # create a quote object, call the appropriate method and split by author/content
        quote_obj = inspire.Inspire()
        quote = quote_obj.get_cs_satire()
        quote_split = quote.split(':')

        # check if role exists then parse
        if check_param:
            role = quote_obj.parse_role(discord_role)

        # format message using embed for professional looking output
        embed = discord.Embed(
            title='Some Humor For You',
            description='Funny Quotes To Get You Through SE Class',
            color=discord.Colour.blue(),
        )

        embed.add_field(name="Programmer", value=quote_split[0], inline=False)
        embed.add_field(name="Quote", value=quote_split[1], inline=False)

        # Get guild members, and send to members or author depending on true/false of check_param
        server = ctx.guild
        if check_param:
            for role_id in role.split(' '):
                for member in server.members:
                    if role_id in [role.mention for role in member.roles]:
                        await member.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    # This command gets inspirational quotes regardless of industry
    @commands.command(name="get-some-inspiration", aliases=["gsm"])
    async def display_inspirational_quote(self, ctx, discord_role: str = ''):
        # sanitize input and check if parameter is empty string or contains role
        check_param: bool
        if '<@&' in discord_role and '>' in discord_role:
            check_param = True
        elif discord_role == '':
            check_param = False
        else:
            await ctx.send("Invalid Input, Select New Quote")
            return
        # create a quote object, call the appropriate method and split by author/content
        motiv_quote_obj = inspire.Inspire()
        quote = motiv_quote_obj.get_inspiration()
        quote_split = quote.split(':')

        # check if role exists then parse
        if check_param:
            role = motiv_quote_obj.parse_role(discord_role)
        # format message using embed for professional looking output
        embed = discord.Embed(
            title='Inspiration Vibes',
            description='Everything Is Gonna Be Okay',
            color=discord.Colour.blue(), )

        embed.add_field(name="The Sage", value=quote_split[0], inline=False)
        embed.add_field(name="The Quote", value=quote_split[1], inline=False)
        # Get guild members, and send to members or author depending on true/false of check_param
        server = ctx.guild
        if check_param:
            for role_id in role.split(' '):
                for member in server.members:
                    if role_id in [role.mention for role in member.roles]:
                        await member.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    # This command gets motivational quotes related to computer programming
    @commands.command(name="get-cs-motivation", aliases=["csm"])
    async def display_motivational_quote(self, ctx, discord_role: str = ''):
        # sanitize input and check if parameter is empty string or contains role
        check_param: bool
        if '<@&' in discord_role and '>' in discord_role:
            check_param = True
        elif discord_role == '':
            check_param = False
        else:
            await ctx.send("Invalid Input, Select New Quote")
            return
        # create a quote object, call the appropriate method and split by author/content
        insp_quote_obj = inspire.Inspire()
        quote = insp_quote_obj.get_cs_motivated()
        quote_split = quote.split(':')
        # check if role exists then parse
        if check_param:
            role = insp_quote_obj.parse_role(discord_role)
        # format message using embed for professional looking output
        embed = discord.Embed(
            title='Some Motivation',
            description='When You Lost The Will To Progam',
            color=discord.Colour.blue(), )

        embed.add_field(name="Author", value=quote_split[0], inline=False)
        embed.add_field(name="Quote", value=quote_split[1], inline=False)
        # Get guild members, and send to members or author depending on true/false of check_param
        server = ctx.guild
        if check_param:
            for role_id in role.split(' '):
                for member in server.members:
                    if role_id in [role.mention for role in member.roles]:
                        await member.send(embed=embed)
        else:
            await ctx.send(embed=embed)


# Bot setup
def setup(bot):
    bot.add_cog(InspireCommands(bot))
