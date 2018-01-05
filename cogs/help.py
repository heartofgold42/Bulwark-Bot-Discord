import discord
from discord.ext import commands


class Help:
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot
        bot.remove_command('help')

    @commands.command(pass_context=True)
    async def help(self, ctx):
        """
        Displays a useful list of commands.
        """
        desc = ""
        for key in self.bot.commands.keys():
            command = self.bot.get_command(key)
            if command.aliases and not command.hidden:
                desc += "`!{}`".format(command.name)+" - {}\nAliases: `{}`\n".format(command.short_doc,
                ",".join(command.aliases))
                desc += "\n"

            elif command.short_doc and not command.hidden:
                desc += "`!{}`".format(command.name)+" - {}\n".format(command.short_doc)
                desc += "\n"

            else:
                if not command.hidden:
                    desc += "`!{}`\n".format(command.name)
                    desc += "\n"

        embed = discord.Embed(description=desc)
        embed.set_author(icon_url=self.bot.user.avatar_url, name="BulwarkBot commands!")
        try:
            await self.bot.send_message(ctx.message.author, embed=embed)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this")


def setup(bot):
    bot.add_cog(Help(bot))
