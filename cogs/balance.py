import discord
from discord.ext import commands
from utils import rpc_module, mysql_module

#result_set = database response with parameters from query
#db_bal = nomenclature for result_set["balance"]
#snowflake = snowflake from message context, identical to user in database
#wallet_bal = nomenclature for wallet reponse

rpc = rpc_module.Rpc()
mysql = mysql_module.Mysql()


class Balance:

    def __init__(self, bot):
        self.bot = bot

    async def do_embed(self, name, db_bal):
        # Simple embed function for displaying username and balance
        embed = discord.Embed(colour=0xff0000)
        embed.add_field(name="User", value=name.mention)
        embed.add_field(name="Balance", value="{:.8f} BWK".format(round(float(db_bal), 8)))

        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission to send this")

    def __check_for_new_balance(self, user):
        balance = rpc.getbalance(user.id)
        mysql.set_balance(user, balance)

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        """Display your balance"""
        # Set important variables
        snowflake = ctx.message.author.id
        name = ctx.message.author.name

        self.__check_for_new_balance(ctx.message.author)

        # Check if user exists in db
        result_set = mysql.check_for_user(name, snowflake)

        # Execute and return SQL Query
        result_set = mysql.get_user(snowflake)

        await self.do_embed(ctx.message.author, result_set['balance'])


def setup(bot):
    bot.add_cog(Balance(bot))
