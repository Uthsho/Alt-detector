import discord
from discord.ext import commands
import random

ListColours = [
    discord.Colour.blue(),
    discord.Colour.teal(),
    discord.Colour.dark_teal(),
    discord.Colour.green(),
    discord.Colour.dark_green(),
    discord.Colour.blue(),
    discord.Colour.dark_blue(),
    discord.Colour.purple(),
    discord.Colour.dark_purple(),
    discord.Colour.magenta(),
    discord.Colour.dark_magenta(),
    discord.Colour.gold(),
    discord.Colour.dark_gold(),
    discord.Colour.orange(),
    discord.Colour.dark_orange(),
    discord.Colour.red(),
    discord.Colour.dark_red(),
    discord.Colour.lighter_grey(),
    discord.Colour.dark_grey(),
    discord.Colour.light_grey(),
    discord.Colour.darker_grey(),
    discord.Colour.blurple(),
    discord.Colour.greyple(),
]


class Help_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        helpembed = discord.Embed(
            title='Help',
            colour=random.choice(ListColours),
            description=
            "Do `help [command_name]` for further help on various commands.")
        helpembed.set_thumbnail(url=self.bot.user.avatar_url)
        helpembed.add_field(
            name="Moderation commands:",
            value=
            "`fetchalts`: Get a list of alts hiding in your server!\n`whois`: Use this command to know the account information.\n`ban`: Ban members with optional reason.\n`kick`: Kick users with optional reason",
            inline=False)
        helpembed.add_field(
            name="Misc commands:",
            value=
            '`botinfo`: Information about the bot.\n`ping`: Shows the latency of the bot.\n`uptime`: Shows the uptime of the bot.',
            inline=False)
        await ctx.send(embed=helpembed)

    @help.command()
    async def kick(self, ctx):
        embed = discord.Embed(
            title="kick <member> [reason]",
            colour=random.choice(ListColours),
            descriptipon=
            "`<member>` can be replaced by both ID, and mention.\n`[reason] is an optional field."
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name='Note: DO NOT include the [] brackets',
            value=
            'For example:\nad!kick <@!428185775910420480> Example or\nad!kick 428185775910420480 Example'
        )
        await ctx.send(embed=embed)

    @help.command()
    async def ban(self, ctx):
        embed = discord.Embed(
            title="ban <member> [reason]",
            colour=random.choice(ListColours),
            descriptipon=
            "`<member>` can be replaced by both ID, and mention.\n`[reason] is an optional field."
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name='Note: DO NOT include the [] brackets',
            value=
            'For example:\nad!ban <@!428185775910420480> Example or\nad!ban 428185775910420480 Example'
        )
        await ctx.send(embed=embed)

    @help.command()
    async def fetchalts(self, ctx):
        embed = discord.Embed(
            title="fetchalts [days]",
            colour=random.choice(ListColours),
            description=
            "Use this command to find accounts younger than the number of days you provide in the `[days]` parameter."
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name=
            "Note: DO NOT include the [] brackets.\nTo prevent spam, the `[days]` parameter cannot be more than 90 days",
            value='For example:\nad!fetchalts 3.')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help_command(bot))
