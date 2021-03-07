from discord.ext import commands
import requests
import logging
import json

from Commands.Entities.Category import CategoryMember, CategoryRoot, CategoryQuery

logging.getLogger('mainLogger')


class TestCog(commands.Cog, name='Test'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='all_chars', help='$w all_chars')
    async def test_get_all_chars(self, ctx, *args):
        logging.info("{} wrote message: $w all_chars".format(ctx.author.display_name))
        await ctx.send("{} wrote message: $w all_chars".format(ctx.author.display_name))
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
            # await ctx.send(r.url)

            decoded_list = json.loads(r.text)

            cat_members = []

            for row in decoded_list['query']['categorymembers']:
                cat_members.append(CategoryMember(row['pageid'], row['ns'], row['title']))

            cat_root = CategoryRoot(decoded_list['batchcomplete'], CategoryQuery(cat_members))
            result_list = []

            for character in cat_root.category_query.category_members:
                url_base = 'https://alohomora.fandom.com/wiki/'
                updated_char_title = character.title.replace(' ', '_')
                updated_url = '<' + url_base + updated_char_title + '>'
                result_list.append(updated_url)

            result_list = '\n'.join(result_list)

            await ctx.send(result_list)
            logging.info(result_list)

            # reaction = await self.bot.wait_for_reaction(['\N{TRACK_NEXT}'])
            # if decoded_list.has_key('continue') is not None and reaction:
            if 'continue' in decoded_list.keys():
                cm_continue = decoded_list['continue']['cmcontinue']
            else:
                done = True

        await ctx.send("end query")

    @commands.command(name='category', help='$w category <term>')
    async def test_get_category(self, ctx, *args):
        logging.info("{} wrote message: $w category {}".format(ctx.author.display_name, ' '.join(args)))
        await ctx.send("{} wrote message: $w category {}".format(ctx.author.display_name, ' '.join(args)))
        done = False
        cm_continue = ''

        while not done:
            payload = dict(action='query',
                           prop='categories',
                           list='categorymembers',
                           cmtitle='Category:{}'.format(' '.join(args)),
                           format='json', cmlimit='10')

            if len(cm_continue) > 1:
                payload['cmcontinue'] = cm_continue

            r = requests.get('https://alohomora.fandom.com/api.php', params=payload)
            # await ctx.send(r.url)

            decoded_list = json.loads(r.text)

            cat_members = []

            for row in decoded_list['query']['categorymembers']:
                cat_members.append(CategoryMember(row['pageid'], row['ns'], row['title']))

            cat_root = CategoryRoot(decoded_list['batchcomplete'], CategoryQuery(cat_members))
            result_list = []

            for character in cat_root.category_query.category_members:
                url_base = 'https://alohomora.fandom.com/wiki/'
                updated_char_title = character.title.replace(' ', '_')
                updated_url = '<' + url_base + updated_char_title + '>'
                result_list.append(updated_url)

            result_list = '\n'.join(result_list)

            await ctx.send(result_list)
            logging.info(result_list)

            # reaction = await self.bot.wait_for_reaction(['\N{TRACK_NEXT}'])
            # if decoded_list.has_key('continue') is not None and reaction:
            if 'continue' in decoded_list.keys():
                cm_continue = decoded_list['continue']['cmcontinue']
            else:
                done = True

        await ctx.send("end query")
