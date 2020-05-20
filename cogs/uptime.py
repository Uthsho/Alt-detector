import discord, datetime, time
from discord.ext import commands
import random 

start_time = time.time()

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

class uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour = random.choice(ListColours))
        embed.set_author(name = "Uptime")
        embed.add_field(name = "h : m: s", value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

def setup(bot):
    bot.add_cog(uptime(bot))