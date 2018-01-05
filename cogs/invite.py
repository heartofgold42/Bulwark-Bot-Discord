from discord.ext import commands


class Invite:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self):
        """
        Get the bots invite link
        """
        await self.bot.say(":tada: https://discordapp.com/oauth2/authorize?permissions=0&client_id={}&scope=bot".format(self.bot.user.id))


def setup(bot):
    bot.add_cog(Invite(bot))
