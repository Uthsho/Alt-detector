import discord
from discord.ext import commands
import random
import os
from datetime import datetime
import sqlite3


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

class rebl_only(commands.Cog):
	def __init__(self, bot):
   		self.bot = bot
	
	@commands.command()
	async def guilds(self, ctx):
		if ctx.author.id == 428185775910420480:
			servers = self.bot.guilds
			embed = discord.Embed(title = "S.No.     -      ID        -       Member count")
			count = 1
			for guild in servers:
				if count > 25:
					await ctx.send(embed = embed)
					embed = discord.Embed(title = "S.No.     -      ID        -       Member count")
					count = 1
				else:
					embed.add_field(name = f"{count}.  {guild.id}     -     {len(guild.members)}", value = f'{guild.name}', inline = False)
					count += 1
			if count < 25:
				await ctx.send(embed = embed)
			else:
				return
		else:
			return

	@commands.command()
	async def leaveguild(self, ctx, id: int):
		if ctx.author.id == 428185775910420480:
			guild = self.bot.get_guild(id)
			name = guild.name
			await guild.leave()
			await ctx.send(f"Left the guild.\nName: `{name}`\nID: `{id}`")
		else:
			return

	@commands.command()
	async def guildinfo(self, ctx, id: int):
		if ctx.author.id == 428185775910420480:
			guild = self.bot.get_guild(id)
			embed = discord.Embed(colour = random.choice(ListColours))
			embed.set_author(name = "Guild Information")
			embed.set_thumbnail(url = guild.icon_url)
			embed.add_field(name = "Guild name:", value = guild.name, inline = False)
			embed.add_field(name = "Guild ID:", value = guild.id, inline = False)
			embed.add_field(name = "Guild owner:", value = guild.owner, inline = False)
			embed.add_field(name = "Member count:", value = len(guild.members), inline = False)
			await ctx.send(embed = embed)
		else:
			return

	@commands.command()
	async def cmd(self, ctx):
		if ctx.author.id == 428185775910420480:
			embed = discord.Embed(title = "Owner only commands", colour = random.choice(ListColours), description = "`guilds`, `guildinfo`, `leaveguild`, `newver`, `check`, `update`, `whois404`, `fetchalts404`")
			await ctx.send(embed = embed)
		else:
			return

	@commands.command()
	async def newver(self, ctx, ver: str):
		if ctx.author.id == 428185775910420480:
			db = sqlite3.connect("version.sqlite")
			cursor = db.cursor()
			cursor.execute(f"SELECT Version FROM main WHERE Title = {ctx.author.id}")
			result = cursor.fetchone()
			if result is None:
				sql = ("INSERT INTO main(Version, Title) VALUES(?, ?)")
				val = (ver, ctx.author.id)
				await ctx.send(f'Version is set to {ver}')
			elif result is not None:
				sql = ("UPDATE main SET Version = ? WHERE Title = ?")
				val = (ver, ctx.author.id)
				await ctx.send(f'Version is updated to {ver}')
			cursor.execute(sql, val)
			db.commit()
			cursor.close()
			db.close()
		else:
			return
		  
	@commands.command()
	async def fetchalts404(self, ctx, arg: int):
		if ctx.author.id == 428185775910420480:
			members = ctx.guild.members
			embed = discord.Embed(title = "S.No.           ID               age(in days)")
			count = 1
			for member in members:
				member_age = datetime.utcnow() - member.created_at
				days = member_age.days
				if days < arg:
					if count > 25:
						await ctx.send(embed = embed)
						embed = discord.Embed(title = "S.No.           ID               age(in days)")
						count = 1
					else:
						embed.add_field(name = f"{count}.    {member.id}     -     {days}", value = f'{member.name}#{member.discriminator}', inline = False)
						count += 1
			if count < 25:
				await ctx.send(embed = embed)
			else:
				return
	@commands.command()
	async def whois404(self, ctx, member: discord.Member = None):
		if ctx.author.id == 428185775910420480:
			if member == None:
				embed = discord.Embed(color = random.choice(ListColours))
				embed.set_thumbnail(url = f'{ctx.author.avatar_url}')
				embed.add_field(name = "Server username:", value = f"{ctx.author.mention}")
				member = ctx.author
				embed.add_field(name = "Member ID:", value = member.id, inline = False)
				embed.add_field(name = "Created at:", value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p"), inline = False)
				joined_at = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p")
				precise_member_age = datetime.utcnow() - member.created_at
				member_age = precise_member_age.days
				embed.add_field(name = "Joined at:", value = joined_at, inline = False)
				year = int(member_age / 365) 
				month = int((member_age % 365) / 30) 
				days = (member_age % 365) % 30
				embed.add_field(name = "Account age:", value = f'{year} year(s), {month} month(s), {days} day(s)')
				embed.set_footer(text = "All times are in GMT to avoid any confusion.")
				embed.set_author(name = "Member details")
				await ctx.send(embed = embed)
			else:
				embed = discord.Embed(color = random.choice(ListColours))
				embed.set_thumbnail(url = f'{member.avatar_url}')
				embed.add_field(name = "Server username:", value = f"{member.mention}")
				embed.add_field(name = "Member ID:", value = member.id, inline = False)
				embed.add_field(name = "Created at:", value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p"), inline = False)
				joined_at = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p")
				precise_member_age = datetime.utcnow() - member.created_at
				member_age = precise_member_age.days
				embed.add_field(name = "Joined at:", value = joined_at, inline = False)
				year = int(member_age / 365) 
				month = int((member_age % 365) / 30) 
				days = (member_age % 365) % 30
				embed.add_field(name = "Account age:", value = f'{year} year(s), {month} month(s), {days} day(s)')
				embed.set_footer(text = "All times are in GMT to avoid any confusion.")
				embed.set_author(name = "Member details")
				await ctx.send(embed = embed)

	@commands.command()
	async def update(self, ctx, version, *, info):
		if ctx.author.id == 428185775910420480:
			embed = discord.Embed(title = f"Version {version}", colour = random.choice(ListColours), description = f"<a:online:700609324602490941> {info}")
			embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
			guild = self.bot.get_guild(699290773799305298)
			channel = guild.get_channel(699314188253921360)
			await channel.send(embed = embed)
			await ctx.send('<a:online:700609324602490941> Update published.')

def setup(bot):
    bot.add_cog(rebl_only(bot))