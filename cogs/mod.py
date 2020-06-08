import discord
from discord.ext import commands
import random

ListColours = [discord.Colour.blue(), discord.Colour.teal(), discord.Colour.dark_teal(), discord.Colour.green(), discord.Colour.dark_green(), discord.Colour.blue(), discord.Colour.dark_blue(), discord.Colour.purple(), discord.Colour.dark_purple(), discord.Colour.magenta(), discord.Colour.dark_magenta(), discord.Colour.gold(), discord.Colour.dark_gold(), discord.Colour.orange(), discord.Colour.dark_orange(),   discord.Colour.red(), discord.Colour.dark_red(), discord.Colour.lighter_grey(), discord.Colour.dark_grey(), discord.Colour.light_grey(), discord.Colour.darker_grey(), discord.Colour.blurple(), discord.Colour.greyple()]
#colour = random.choice(ListColours)

class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, member: discord.Member = None, *, reason = None):
    if reason == None:
      if member == None: 
        await ctx.send(embed = discord.Embed(title = "Please provide a user to ban!", colour = random.choice(ListColours), description = "For example: `ad!ban <member> [reason]`"))
      elif member == ctx.message.author:
        await ctx.send(embed = discord.Embed(title = "You cannot ban yourself!", colour = random.choice(ListColours), description = "*You dumb!*" ))
      elif member.id == 649254309451530292:
        await ctx.send(embed = discord.Embed(title = "You cannot ban the bot!", colour = random.choice(ListColours), description = "*You seriously cannot use the bot to ban the bot smh!*" ))
      else:
        message = discord.Embed(title = f'You have been banned from {ctx.guild.name}', colour = random.choice(ListColours), description = 'The reason was not specified by the moderator')
        reply = discord.Embed(title = f'{member} has been banned from **{ctx.guild.name}** by {ctx.message.author}.', colour = random.choice(ListColours), description = f'Reason was not specified by {ctx.message.author}')
        await member.send(embed = message)
        await ctx.guild.ban(member)
        await ctx.send(embed = reply)
    else:
      if member == None: 
        await ctx.send(embed = discord.Embed(title = "Please provide a user to ban!", colour = random.choice(ListColours), description = "For example: `ad!ban <member> [reason]`"))
      elif member == ctx.message.author:
        await ctx.send(embed = discord.Embed(title = "You cannot ban yourself!", colour = random.choice(ListColours), description = "*You dumb!*" ))
      elif member.id == 649254309451530292:
        await ctx.send(embed = discord.Embed(title = "You cannot ban the bot!", colour = random.choice(ListColours), description = "*You seriously cannot use the bot to ban the bot smh!*" ))
      else:
        message = discord.Embed(title = f'You have been banned from {ctx.guild.name}', colour = random.choice(ListColours), description = f'Reason: {reason}')
        reply = discord.Embed(title = f'{member} has been banned from **{ctx.guild.name}** by {ctx.message.author}.', colour = random.choice(ListColours), description = f'Reason: {reason}')
        await member.send(embed = message)
        await ctx.guild.ban(member)
        await ctx.send(embed = reply)
  
  @commands.command()                                    
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member: discord.Member = None, *, reason = None):
    if reason == None:
      if member == None: 
        await ctx.send(embed = discord.Embed(title = "Please provide a user to kick!", colour = random.choice(ListColours), description = "For example: `ad!kick <member> [reason]`"))
      elif member == ctx.message.author:
        await ctx.send(embed = discord.Embed(title = "You cannot kick yourself!", colour = random.choice(ListColours), description = "*You dumb!*" ))
      elif member.id == 649254309451530292:
        await ctx.send(embed = discord.Embed(title = "You cannot kick bot!", colour = random.choice(ListColours), description = "*You seriously cannot use the bot to kick the bot smh!*" ))
      else:
        message = discord.Embed(title = f'You have been kicked from {ctx.guild.name}', colour = random.choice(ListColours), description = 'The reason was not specified by the moderator')
        reply = discord.Embed(title = f'{member} has been kicked from **{ctx.guild.name}** by {ctx.message.author}.', colour = random.choice(ListColours), description = f'Reason was not specified by {ctx.message.author}')
        await member.send(embed = message)
        await ctx.guild.kick(member)
        await ctx.send(embed = reply)
    else:
      if member == None: 
        await ctx.send(embed = discord.Embed(title = "Please provide a user to kick!", colour = random.choice(ListColours), description = "For example: `ad!kick <member> [reason]`"))
      elif member == ctx.message.author:
        await ctx.send(embed = discord.Embed(title = "You cannot kick yourself!", colour = random.choice(ListColours), description = "*You dumb!*" ))
      elif member.id == 649254309451530292:
        await ctx.send(embed = discord.Embed(title = "You cannot kick bot!", colour = random.choice(ListColours), description = "*You seriously cannot use the bot to kick the bot smh!*" ))
      else:
        message = discord.Embed(title = f'You have been kicked from {ctx.guild.name}', colour = random.choice(ListColours), description = f'Reason: {reason}')
        reply = discord.Embed(title = f'{member} has been kicked from **{ctx.guild.name}** by {ctx.message.author}.', colour = random.choice(ListColours), description = f'Reason: {reason}')
        await member.send(embed = message)
        await ctx.guild.kick(member)
        await ctx.send(embed = reply)


def setup(bot):
    bot.add_cog(Moderation(bot))
