from discord.ext import commands
import requests
import logging

from Commands import ResultsFactory

logging.getLogger('mainLogger')


class TestCog(commands.Cog, name='Test'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test_cat', help='$w')
    async def test_get_category(self, ctx, *args):
        logging.info("{} wrote message: $w test_cat".format(ctx.author))
        payload = {'action': 'query', 'prop': 'categories', 'list': 'categorymembers',
                   'cmtitle': 'Category:Character', 'format': 'json', 'cmlimit': '500'}
        r = requests.get('https://alohomora.fandom.com/api.php', params=payload)
        logging.info(r.url)
        await ctx.send(ResultsFactory.ResultsFactory.process_category_list(r.text))
        await ctx.send("{} wrote message: $w test_cat".format(ctx.author))
        await ctx.send(r.url)

