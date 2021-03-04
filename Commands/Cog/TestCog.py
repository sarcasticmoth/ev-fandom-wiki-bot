from discord.ext import commands
import requests
import logging
import json

from Commands.Entities.Category import CategoryMember, CategoryRoot, CategoryQuery

logging.getLogger('mainLogger')


class TestCog(commands.Cog, name='Test'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='who', help='$w who <ooc name>')
    async def test_char_player(self, ctx, *args):
        term = ' '.join(args)
        if not term or term is None:
            logging.error("invalid value.")
            await ctx.send("invalid value.")
            return
        logging.info("{} wrote message: $w who {}".format(ctx.author, term))
        await ctx.send("{} wrote message: $w who {}".format(ctx.author, term))
        done = False
        cm_continue = ''

        while not done:
            payload = dict(action='query',
                           prop='categories',
                           list='categorymembers',
                           cmtitle='Category:{}'.format(term),
                           format='json', cmlimit='10')

            if len(cm_continue) > 1:
                payload['cmcontinue'] = cm_continue

            r = requests.get('https://alohomora.fandom.com/api.php', params=payload)
            await ctx.send(r.url)

            decoded_list = json.loads(r.text)

            cat_members = []

            for row in decoded_list['query']['categorymembers']:
                cat_members.append(CategoryMember(row['pageid'], row['ns'], row['title']))

            cat_root = CategoryRoot(decoded_list['batchcomplete'], CategoryQuery(cat_members))
            result_list = []

            for character in cat_root.category_query.category_members:
                result_list.append(character.title)

            result_list = '\n'.join(result_list)

            await ctx.send(result_list)

            if decoded_list.has_key('continue') is not None:
                cm_continue = decoded_list['continue']['cmcontinue']
            else:
                done = True

        await ctx.send("end query")

    @commands.command(name='test_cat', help='$w')
    async def test_get_category(self, ctx, *args):
        logging.info("{} wrote message: $w test_cat".format(ctx.author))
        await ctx.send("{} wrote message: $w test_cat".format(ctx.author))
        done = False
        cm_continue = ''

        while not done:
            payload = dict(action='query',
                           prop='categories',
                           list='categorymembers',
                           cmtitle='Category:Character',
                           format='json', cmlimit='10')

            if len(cm_continue) > 1:
                payload['cmcontinue'] = cm_continue

            r = requests.get('https://alohomora.fandom.com/api.php', params=payload)
            await ctx.send(r.url)

            decoded_list = json.loads(r.text)

            cat_members = []

            for row in decoded_list['query']['categorymembers']:
                cat_members.append(CategoryMember(row['pageid'], row['ns'], row['title']))

            cat_root = CategoryRoot(decoded_list['batchcomplete'], CategoryQuery(cat_members))
            result_list = []

            for character in cat_root.category_query.category_members:
                result_list.append(character.title)

            result_list = '\n'.join(result_list)

            await ctx.send(result_list)

            # reaction = await self.bot.wait_for_reaction(['\N{TRACK_NEXT}'])
            # if decoded_list.has_key('continue') is not None and reaction:
            if decoded_list.has_key('continue') is not None:
                cm_continue = decoded_list['continue']['cmcontinue']
            else:
                done = True

        await ctx.send("end query")
