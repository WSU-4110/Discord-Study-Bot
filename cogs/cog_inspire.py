import discord
from discord.ext import commands
from models import inspire


class InspireCommands(commands.Cog, name="Inspire Commands"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get-cs-satire", aliases=["css"])
    async def display_quote(self, ctx):

    #create a quote oject, call the appropriate method and split by author/content
        quote_obj = inspire.Inspire()
        quote = quote_obj.get_cs_satire()
        quote_split = quote.split(':')
        #basic embed for displaying quote
        embed = discord.Embed(
            title='Some Humor For You',
            description='Funny Quotes To Get You Through SE Class',
            color=discord.Colour.blue(),
        )

        embed.add_field(name="Programmer", value=quote_split[0], inline=False)
        embed.add_field(name="Quote", value=quote_split[1], inline=False)
        #currently sends to the author, however I want to send to user roles
        await ctx.send(embed = embed)

    @commands.command(name="get-some-inspiration", aliases=["gsm"])
    async def display_inspirational_quote(self, ctx):
        insp_quote_obj = inspire.Inspire()

        quote = insp_quote_obj.get_inspiration()
        quote_split = quote.split(':')

        embed = discord.Embed(
        title='Inspiration Vibes',
        description='Everything Is Gonna Be Okay',
        color=discord.Colour.blue(),)

        embed.add_field(name="The Sage", value=quote_split[0], inline=False)
        embed.add_field(name="The Quote", value=quote_split[1], inline=False)

        await ctx.send(embed = embed)


    @commands.command(name="get-cs-motivation", aliases=["csm"])
    async def display_motivational_quote(self, ctx):
        insp_quote_obj = inspire.Inspire()

        quote = insp_quote_obj.get_cs_motivated()
        quote_split = quote.split(':')

        embed = discord.Embed(
            title='Some Motivation',
            description='When You Lost The Will To Progam',
            color=discord.Colour.blue(), )

        embed.add_field(name="Author", value=quote_split[0], inline=False)
        embed.add_field(name="Quote", value=quote_split[1], inline=False)

        await ctx.send(embed=embed)


# Bot setup
def setup(bot):
    bot.add_cog(InspireCommands(bot))
