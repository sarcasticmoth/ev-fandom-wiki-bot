import asyncio

import discord
from discord.ext import commands
import requests
import logging
import json

from Commands.Entities.Category import CategoryMember, CategoryRoot, CategoryQuery

logging.getLogger('mainLogger')


class SearchCog(commands.Cog, name='Search'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='all_chars', help='$w allchars')
    async def test_get_all_chars(self, ctx, *args):
        logging.info("{} wrote message: $w allchars".format(ctx.author.display_name))
        await ctx.send("{} wrote message: $w allchars".format(ctx.author.display_name))
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

            decoded_list = json.loads(r.text)
            result_list = self.RequestAndReturn(decoded_list)

            await ctx.send(result_list)
            logging.info(result_list)

            if 'continue' in decoded_list.keys():
                cm_continue = decoded_list['continue']['cmcontinue']
                await ctx.send('react with ⏭️ for more results')
            else:
                done = True

            reaction, user = await self.bot.wait_for('reaction_add', timeout=30)

            if str(reaction) != '⏭️' and user != ctx.author:
                done = True

        await ctx.send("end query")

    @commands.command(name='category', help='$w category <term>')
    async def test_get_category(self, ctx, *args):
        term = ' '.join(args)
        logging.info("{} wrote message: $w category {}".format(ctx.author.display_name, term))
        await ctx.send("{} wrote message: $w category {}".format(ctx.author.display_name, term))
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

            decoded_list = json.loads(r.text)
            result_list = self.RequestAndReturn(decoded_list)

            if len(result_list) < 1:
                await ctx.send("No results for category [{}]".format(term))
                return

            await ctx.send(result_list)
            logging.info(result_list)

            if 'continue' in decoded_list.keys():
                cm_continue = decoded_list['continue']['cmcontinue']
                await ctx.send('react with ⏭️ for more results')
            else:
                done = True

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30)

                if str(reaction) != '⏭️':
                    done = True
            except asyncio.TimeoutError:
                logging.info("--end query--")
                await ctx.send("--end query--")

        await ctx.send("end query")

    @commands.command(name='embeds')
    @commands.guild_only()
    async def example_embed(self, ctx):
        """A simple command which showcases the use of embeds.
        Have a play around and visit the Visualizer."""

        embed = discord.Embed(title='Example Embed',
                              description='Showcasing the use of Embeds...\nSee the visualizer for more info.',
                              colour=0x98FB98)
        embed.set_author(name='MysterialPy',
                         url='https://gist.github.com/MysterialPy/public',
                         icon_url='http://i.imgur.com/ko5A30P.png')
        embed.set_image(url='https://cdn.discordapp.com/attachments/84319995256905728/252292324967710721/embed.png')

        embed.add_field(name='Embed Visualizer', value='[Click Here!](https://leovoel.github.io/embed-visualizer/)')
        embed.add_field(name='Command Invoker', value=ctx.author.mention)
        embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')

        await ctx.send(content='**A simple Embed for discord.py@rewrite in cogs.**', embed=embed)

    @commands.Cog.listener()
    async def on_reaction(self, message):
        if message.author == self.user:
            return

    @staticmethod
    def RequestAndReturn(decoded_list):
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
        return result_list
