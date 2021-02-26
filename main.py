import os
import logging
import logging.config
from discord.ext import commands
from sys import exc_info

logging.config.fileConfig('logging.conf')
logging.getLogger('mainLogger')

token = os.getenv('DISCORD_BOT_TOKEN')
bot = commands.Bot(command_prefix='$test ', pm_help=False)
bot.add_cog(EasterEggCog(bot))
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


# RUN BOT

bot.run(token)
