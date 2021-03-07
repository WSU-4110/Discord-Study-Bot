from discord.ext import commands
from models import search


def format_words(terms: list):
    formatted_terms = '+'.join(word.replace(" ", "+") for word in terms)
    return formatted_terms


def get_url(words_list: list):
    terms = format_words(words_list)
    return f'<https://letmegooglethat.com/?q={terms}>'


class SearchCommands(commands.Cog, name="Search Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='search', aliases=['srch', 's'])
    async def default_search(self, ctx, *, args):
        """ Search duckduckgo to get results """
        results = search.Search(args).get_results()

        for index, result in enumerate(results):
            await ctx.send(str(index + 1) + ". " + "**Title:** " + result['title'] +
                           "\n**Description:** " + result['description'] +
                           "\n" + result['url'])

    @commands.command(name='search-site', aliases=['srch-site', 'ss', 'a-srch', 's-site', 'srch-s', 'searchsite', 's-s'])
    async def search_site(self, ctx, site, *, args):
        """ Search duckduckgo to get results from specific site"""
        results = search.Search(args + " site:" + str(site)).get_results()

        for index, result in enumerate(results):
            await ctx.send(str(index + 1) + ". " + "**Title:** " + result['title'] +
                           "\n**Description:** " + result['description'] +
                           "\n" + result['url'])

    @commands.command(name='big-search', aliases=['.big-srch', 'bs', 'b-srch', 'b-s', 'big-s', 'bigs'])
    async def big_search(self, ctx, *args):
        """ Search google to get results """
        await ctx.send(get_url(args))


def setup(bot):
    bot.add_cog(SearchCommands(bot))
