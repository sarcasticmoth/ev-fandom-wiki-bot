from discord.ext import commands
import logging

logging.getLogger('mainLogger')


class SearchCog(commands.Cog, name='Search'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='search', help='$wiki search <term> | searches all page contents')
    async def search_pages(self, ctx, *args):
        logging.info("{} wrote message: $wiki search {}".format(ctx.author, ' '.join(args)))
        search_content = ' '.join(args)
        await ctx.send('searching all pages for [{}]'.format(search_content))

    @commands.command(name='category', help='$wiki category <term>')
    async def search_category(self, ctx, *args):
        logging.info("{} wrote message: $wiki category {}".format(ctx.author, ' '.join(args)))
        search_content = ' '.join(args)
        await ctx.send('searching pages with category [{}]'.format(search_content))
