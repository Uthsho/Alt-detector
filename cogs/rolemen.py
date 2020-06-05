import discord
from discord.ext import commands
import random
import asyncio

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

class rolemen(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.group(invoke_without_command = True)	
	@commands.has_permissions(administrator = True)
	async def rolemen(self, ctx):
		msg = await ctx.send(f'<a:bot_offline:700602112949747772> Fetching roles.\nIf the list is long i.e. if there are too many roles, it may cause a big embed to popup in this channel.\nReact with a <a:online:700609324602490941> to confirm.\nThe reaction confirmation will timeout in 60 seconds.')
		await msg.add_reaction('<a:online:700609324602490941>')

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) == '<a:online:700609324602490941>'

		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			await ctx.send("Reaction timed out.")
			await msg.remove_reaction('<a:online:700609324602490941>', self.bot.user)
		else:
			roles = ctx.guild.roles
			embed = discord.Embed(title = "S.No.		 -				 ID							-	 Mentionable?", color = random.choice(ListColours))
			count = 1
			page = 1
			for role in roles:
							if count > 10:
								if page == 1:
									await msg.remove_reaction('<a:online:700609324602490941>', self.bot.user)
									await msg.edit(embed = embed)
									page = page + 1
									await msg.add_reaction('<:next:709326566945062934>')

									def check1(reaction, user):
										return user == ctx.author and str(reaction.emoji) == '<:next:709326566945062934>'
									
									try:
										reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check1)
									except asyncio.TimeoutError:
										await msg.remove_reaction('<:next:709326566945062934>', self.bot.user)
									else:
											embed = discord.Embed(title = "S.No.		 -				 ID							-	 Mentionable?", color = random.choice(ListColours))
											embed.set_footer(text = f"Page number: {page}")
											count = 1
								else:
									await msg.edit(embed = embed)

									def check1(reaction, user):
										return user == ctx.author and str(reaction.emoji) == '<:next:709326566945062934>'
									
									try:
										reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check1)
									except asyncio.TimeoutError:
										await msg.remove_reaction('<:next:709326566945062934>', self.bot.user)
									else:
										page = page + 1
										embed = discord.Embed(title = "S.No.		 -				 ID							-	 Mentionable?", color = random.choice(ListColours))
										embed.set_footer(text = f"Page number: {page}")
										count = 1
							else:
								embed.add_field(name = f"{count}.			 {role.id}						 {role.mentionable}", value = role.name, inline = False)
								count += 1
			if count <= 10:
						await msg.edit(embed = embed)
						await msg.remove_reaction('<:next:709326566945062934>', self.bot.user)
			else:
						return















	@rolemen.command()	
	@commands.has_permissions(administrator = True)
	async def true(self, ctx):
		msg = await ctx.send(f'<a:bot_offline:700602112949747772> Fetching roles.\nIf the list is long i.e. if there are too many roles, it may cause a big embed to popup in this channel.\nReact with a <a:online:700609324602490941> to confirm.\nThe reaction confirmation will timeout in 60 seconds.')
		await msg.add_reaction('<a:online:700609324602490941>')

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) == '<a:online:700609324602490941>'

		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			await ctx.send("Reaction timed out.")
			await msg.remove_reaction('<a:online:700609324602490941>', self.bot.user)
		else:
			roles = ctx.guild.roles
			embed = discord.Embed(title = "S.No.		 -				 ID							-	 Mentionable?", color = random.choice(ListColours))
			count = 1
			for role in roles:
				if role.mentionable:
					embed.add_field(name = f"{count}.			 {role.id}						 {role.mentionable}", value = role.name, inline = False)
					count = count + 1
				else:
					pass
			await ctx.send(embed = embed)

	@rolemen.command()	
	@commands.has_permissions(administrator = True)
	async def false(self, ctx):
		msg = await ctx.send(f'<a:bot_offline:700602112949747772> Fetching roles.\nIf the list is long i.e. if there are too many roles, it may cause a big embed to popup in this channel.\nReact with a <a:online:700609324602490941> to confirm.\nThe reaction confirmation will timeout in 60 seconds.')
		await msg.add_reaction('<a:online:700609324602490941>')

		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) == '<a:online:700609324602490941>'

		try:
			reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
		except asyncio.TimeoutError:
			await ctx.send("Reaction timed out.")
			await msg.remove_reaction('<a:online:700609324602490941>', self.bot.user)
		else:
			roles = ctx.guild.roles
			embed = discord.Embed(title = "S.No.		 -				 ID							-	 Mentionable?", color = random.choice(ListColours))
			count = 1
			for role in roles:
				if role.mentionable:
					pass
				else:
					embed.add_field(name = f"{count}.			 {role.id}						 {role.mentionable}", value = role.name, inline = False)
					count = count + 1
			await ctx.send(embed = embed)

def setup(bot):
		bot.add_cog(rolemen(bot))