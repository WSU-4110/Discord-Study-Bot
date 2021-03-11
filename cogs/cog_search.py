import asyncio
import discord
from discord.ext import commands
from models import search
from utils import config as cfg


def format_words(terms: list):
    formatted_terms = '+'.join(word.replace(" ", "+") for word in terms)
    return formatted_terms


def get_url(words_list: list):
    terms = format_words(words_list)
    return f'https://letmegooglethat.com/?q={terms}'


class SearchCommands(commands.Cog, name="Search Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='search', aliases=['srch', 's'])
    async def default_search(self, ctx, *, args):
        """ Search duckduckgo to get results """
        # creates search object and gets results
        results = search.Search(args).get_results()

        # output
        for index, result in enumerate(results):
            embed = discord.Embed(title=("Result " + str(index + 1) + ": " + result['title']),
                                  url=result['url'],
                                  description=result['description'],
                                  color=cfg.colors.LINK)
            await ctx.send(embed=embed)

    @commands.command(name='search-site',
                      aliases=['srch-site', 'ss', 'a-srch', 's-site', 'srch-s', 'searchsite', 's-s'])
    async def search_site(self, ctx):
        """ Search duckduckgo to get results from specific site"""
        try:
            # asks user for site they want to search
            embed = discord.Embed(title="Which website do you want to search?",
                                  description="example: youtube.com",
                                  color=cfg.colors.WSU_GOLD)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            site = await self.bot.wait_for('message',
                                           timeout=60.0,
                                           check=lambda message: message.author == ctx.author)

            # asks user for what they want to search for
            embed = discord.Embed(title="What do you want to find?",
                                  description="example: 7 wonders of the world",
                                  color=cfg.colors.WSU_GOLD)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            args = await self.bot.wait_for('message',
                                           timeout=60.0,
                                           check=lambda message: message.author == ctx.author)

            # creates search object w/ site restriction and gets results
            results = search.Search(args.content + " site:" + site.content).get_results()

            # output
            for index, result in enumerate(results):
                embed = discord.Embed(title=("Result " + str(index + 1) + ": " + result['title']),
                                      url=result['url'],
                                      description=result['description'],
                                      color=cfg.colors.LINK)
                await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            # in case user takes more than 60 seconds to respond, send message
            embed = discord.Embed(title="Timeout Error!!!",
                                  description="took more than 60 seconds to respond.",
                                  color=cfg.colors.TIMEOUT)
            embed.set_thumbnail(url="https://thumbs.dreamstime.com/b/error-icon-16125237.jpg")
            await ctx.send(embed=embed)

    @commands.command(name='big-search', aliases=['.big-srch', 'bs', 'b-srch', 'b-s', 'big-s', 'bigs'])
    async def big_search(self, ctx, *args):
        """ Search google to get results """
        # output
        msg = " ".join(args)
        embed = discord.Embed(title="Link to Big Search",
                              url=get_url(args),
                              description=msg,
                              color=cfg.colors.LINK)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SearchCommands(bot))
