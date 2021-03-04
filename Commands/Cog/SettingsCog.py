from discord.ext import commands
import validators
import logging

logging.getLogger('mainLogger')


class SettingsCog(commands.Cog, name='Settings'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='site', help='$w site http://site.com | enter wiki site')
    # @has_permissions(administrator=True, manage_messages=True, manage_roles=True)
    async def set_wiki_site(self, ctx, *args):
        logging.info("{} wrote message: $w site {}".format(ctx.author, ' '.join(args)))
        await ctx.send("command entered: $w site {}".format(args[0]))
        if ctx.message.author.guild_permissions.administrator:
            logging.info("User is a server administrator")
            await ctx.send("you CAN use this command")
        else:
            logging.info("User is not a server administrator")
            await ctx.send("You do not have permissions to use this command.")
        if not validators.domain(args[0]) or validators.url(args[0]):
            await ctx.send("Invalid URL: {}".format(args[0]))
            raise Exception("Invalid Exception")
        else:
            await ctx.send("Valid URL entered.")
