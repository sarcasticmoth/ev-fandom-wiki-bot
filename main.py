import os
import logging
import logging.config
import discord
from discord.ext import commands
from sys import exc_info

from SettingsCog import SettingsCog
from SearchCog import SearchCog

logging.config.fileConfig('logging.conf')
logging.getLogger('mainLogger')

token = os.getenv('DISCORD_BOT_TOKEN')
bot = commands.Bot(command_prefix='$wiki ', pm_help=False)
bot.add_cog(SearchCog(bot))
bot.add_cog(SettingsCog(bot))


# EVENTS

@bot.event
async def on_connect():
    logging.info("----------------------")
    logging.info("Bot is connected to discord")
    logging.info("----------------------")


@bot.event
async def on_ready():
    logging.info("----------------------")
    logging.info("Logged in as: {}".format(bot.user.name))
    logging.info("----------------------")


@bot.event
async def on_error(event, *args, **kwargs):
    logging.error("---- ERROR ----")
    logging.error("Error from:", event)
    logging.error("Error context:", args, kwargs)

    exc_type, value, traceback = exc_info()
    logging.error("Exception type:", exc_type)
    logging.error("Exception value:", value)
    logging.error("Exception traceback object:", traceback)


# TEST COMMANDS

@bot.command(name='test', help='this is a test command')
async def test(ctx, *args):
    logging.info("{} wrote message: {}".format(ctx.author, ' '.join(args)))
    await ctx.send(' '.join(args))


# COMMANDS

# @bot.command(name='help')
# async def help_command(ctx):
#     logging.info("{} wrote message: $wiki help")
#     await ctx.send(commands.bot.HelpCommand)


@bot.command(name='overview', help='$wiki overview | returns details of the wiki site')
async def overview(ctx):
    logging.info("{} wrote message: $wiki overview")


@bot.command(name='random', help='$wiki random | returns a random wiki page')
async def random_page(ctx):
    logging.info("{} wrote message: $wiki random")


# UTILITY


# RUN BOT

bot.run(token)
