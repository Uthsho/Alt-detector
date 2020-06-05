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
            name="Log commands:",
            value=
            '`setchannel`: Set joins log channel.\n`setnotify`: Sets the role to be notified when suspicious accounts join the server.\n`setage`: Sets the number of days by which the bot identifies any account as alt.',
            inline=False)
        helpembed.add_field(
            name="Moderation commands:",
            value=
            "`fetchalts`: Get a list of alts hiding in your server!\n`whois`: Use this command to know the account information.\n`rolemen`: Get a list of roles which can be mentioned by everyone.\n`ban`: Ban members with optional reason.\n`kick`: Kick users with optional reason",
            inline=False)
        helpembed.add_field(
            name="Misc commands:",
            value=
            '`setprefix`: Change the prefix of the bot for this server.\n`invite`: Invite the bot to your server.\n`botinfo`: Information about the bot.\n`knownerrors`: Find out about the common errors.\n`ping`: Shows the latency of the bot.\n`uptime`: Shows the uptime of the bot.',
            inline=False)
        helpembed.add_field(
            name="Note:",
            value=
            "The bot does not have any start or initiate command, as soon as the log channel and notify roles are setup, the bot will start logging.",
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
    async def setchannel(self, ctx):
        embed = discord.Embed(
            title="setchannel [#channel/channel_id]",
            colour=random.choice(ListColours),
            description=
            "This will be the channel where the bot logs the member joins.")
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name=
            'Note: DO NOT include the [] brackets, make sure the bot has permissions to send message in the designated channel.',
            value='For example:\nad!setchannel #abcd or\nad!setchannel self.')
        await ctx.send(embed=embed)

    @help.command()
    async def setage(self, ctx):
        embed = discord.Embed(
            title="setage [days]",
            colour=random.choice(ListColours),
            description=
            "If the age of the account joining is less than the number you provide in the parameter days, it will be identified as an alt."
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name=
            'Note: DO NOT include the [] brackets, the default value is 7.',
            value='For example:\nad!setage 15.')
        await ctx.send(embed=embed)

    @help.command()
    async def setnotify(self, ctx):
        embed = discord.Embed(
            title="setnotify [@role/role_id]",
            colour=random.choice(ListColours),
            description=
            "This will be the which the bot would ping when suspicious members join."
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name=
            "Note: DO NOT include the [] brackets, make sure the bots role is above the role to be pinged",
            value='For example:\nad!setnotify @role or\nad!setrole self.')
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

    @help.command()
    async def rolemen(self, ctx):
        embed = discord.Embed(
            title="rolemen",
            colour=random.choice(ListColours),
            description=
            "Use this command to find a list of roles which can be mentioned by anyone."
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name="Sub-commands:",
            value=
            "`true`: Returns a list of mentionable roles.\n`false`: Returns a list of unmentionable roles."
        )
        embed.add_field(
            name="For example:",
            value='ad!rolemen\nad!rolemen true\nad!rolemen false',
            inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help_command(bot))
