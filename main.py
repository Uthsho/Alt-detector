import discord
from discord.ext import commands
from keep_alive import keep_alive
import random
import os
from datetime import datetime
import sqlite3
import asyncio
import time

def get_prefix(bot, message):
	db = sqlite3.connect("db.sqlite")
	cursor = db.cursor()
	cursor.execute(f"SELECT prefix FROM main WHERE guild_id = {message.guild.id}")
	result = cursor.fetchone()
	if result:
		return result[0]
	else:
		return "ad!"
	
bot = commands.Bot(command_prefix = get_prefix)
start_time = time.time()
bot.remove_command('help')

cogs = ['cogs.Help_command', 'cogs.rebl_only', 'cogs.rolemen', 'cogs.uptime', 'cogs.eval', 'cogs.mod']

@bot.event
async def on_ready():
	status1 = discord.Status.dnd
	Game = discord.Game("ad!help for help! Check ad!knownerrors for common errors troubleshooting.")
	await bot.change_presence(status = status1, activity = Game)
	print("The bot is ready!")
	for cog in cogs:
		bot.load_extension(cog)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)

@bot.event
async def on_command(ctx):
	CmdName = ctx.command
	argums = ctx.args
	result = ctx.command_failed
	embed = discord.Embed()
	embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
	embed.add_field(name = "Server name:", value = ctx.guild.name, inline = False)
	embed.add_field(name = "Server ID", value = ctx.guild.id, inline = False)
	embed.add_field(name = "Command Name:", value = CmdName, inline = False)
	embed.add_field(name = "Arguments Passed:", value = argums, inline = False)
	embed.add_field(name = "Failure?", value = result, inline = False)
	guild = bot.get_guild(699290773799305298)
	channel = guild.get_channel(710535283036127304)
	await channel.send(embed = embed)

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

@bot.event
async def on_member_join(member):
	guild = member.guild
	db = sqlite3.connect("db.sqlite")
	cursor = db.cursor()

	cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {member.guild.id}")
	channelid_raw = cursor.fetchone()
	if channelid_raw[0]:
		channel = guild.get_channel(int(channelid_raw[0]))
	else:
		channel = None

	"""
	cursor.execute(f"SELECT muted_role FROM main WHERE guild_id = {member.guild.id}")
	muteid_raw = cursor.fetchone()
	if muteid_raw[0]:
		muted_role = guild.get_role(int(muteid_raw[0]))
	else:
		muted_role = None
	"""

	cursor.execute(f"SELECT notify FROM main WHERE guild_id = {member.guild.id}")
	notifyid_raw = cursor.fetchone()
	if notifyid_raw[0]:
		notify_role = guild.get_role(int(notifyid_raw[0]))
	else:
		notify_role = None


	cursor.execute(f"SELECT alt_age FROM main WHERE guild_id = {member.guild.id}")
	altage_raw = cursor.fetchone()
	if altage_raw[0]:
		altage = int(altage_raw[0])
	else:
		altage = 7

	joined_at = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p")
	precise_member_age = datetime.utcnow() - member.created_at
	member_age = precise_member_age.days	 #in days

	year = int(member_age / 365) 
	month = int((member_age % 365) / 30) 
	days = (member_age % 365) % 30

	embed = discord.Embed(color = random.choice(ListColours))
	embed.set_thumbnail(url = f'{member.avatar_url}')
	embed.add_field(name = "Server username:", value = f"{member}")
	embed.add_field(name = "Member ID:", value = member.id, inline = False)
	embed.add_field(name = "Created at:", value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p"), inline = False)
	embed.add_field(name = "Joined at:", value = joined_at, inline = False)
	embed.add_field(name = "Account age:", value = f'{year} year(s), {month} month(s), {days} day(s)')
	embed.add_field(name = "Join Position:", value = len(list(member.guild.members)), inline = False)
	embed.set_footer(text = "All times are in GMT to avoid any confusion.")

	if channel == None:
		return

	else:
		if member_age <= altage:
			if notify_role == None:
				embed.set_author(name = f"Suspicious! Account age less than {altage} days!")
				await channel.send(embed = embed)

			else:
				if notify_role.mentionable:
					embed.set_author(name = f"Suspicious! Account age less than {altage} days!")
					await channel.send(notify_role.mention, embed = embed)
				else:
					await notify_role.edit(mentionable = True)
					embed.set_author(name = f"Suspicious! Account age less than {altage} days!")
					await channel.send(notify_role.mention, embed = embed)
					await notify_role.edit(mentionable = False)

		elif altage < member_age < 30:
			embed.set_author(name = "Account age less than 30 days!")
			await channel.send(embed = embed)

		elif 90 > member_age >= 30:
			embed.set_author(name = "This account is older than 1 month.")
			await channel.send(embed = embed)

		elif 180 > member_age >= 90:
			embed.set_author(name = "This account is older than 3 month.")
			await channel.send(embed = embed)

		elif 365 > member_age >= 180:
			embed.set_author(name = "This account is older than 6 month.")
			await channel.send(embed = embed)

		else:
			embed.set_author(name = "This account is older than 1 year.")
			await channel.send(embed = embed)

@bot.command()
@commands.has_permissions(administrator = True)
async def setchannel(ctx, channel: discord.TextChannel = None):
	if channel == None:
		db = sqlite3.connect("db.sqlite")
		cursor = db.cursor()
		cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result is None:
			embed = discord.Embed(title = "Channel feed has not been set yet.", colour = random.choice(ListColours), description = "Please use `ad!setchannel [#channel/channel_id]` to set a feeds channel.")
			await ctx.send(embed = embed)
		elif result is not None:
			embed = discord.Embed(title = f"Channel feed is set to {result[0]}.", colour = random.choice(ListColours), description = "Use `ad!setchannel [#channel/channel_id]` to change the feeds channel.")
			await ctx.send(embed = embed)
	else:
		db = sqlite3.connect("db.sqlite")
		cursor = db.cursor()
		cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?, ?)")
			val = (ctx.guild.id, channel.id)
			await ctx.send(f'Channel feed has been set to {channel.mention}. Please make sure the bot has permissions to message in that channel.')
		elif result is not None:
			sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
			val = (channel.id, ctx.guild.id)
			await ctx.send(f'Channel feed has been updated to {channel.mention}. Please make sure the bot has permissions to message in that channel.')
		txt = bot.get_channel(channel.id)
		await txt.send(f"Log channel is set to {channel.mention}.")
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()

@setchannel.error
async def setchannel_error(ctx, error):
		if isinstance(error, commands.CheckFailure):
				await ctx.send('You do not have the permissions to invoke this command.\nRequired permission: `Administrator`.')

@bot.command()
@commands.has_permissions(administrator = True)
async def setage(ctx, age: int = None):
	if age == None:
		db = sqlite3.connect("db.sqlite")
		cursor = db.cursor()
		cursor.execute(f"SELECT alt_age FROM main WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result is None:
			embed = discord.Embed(title = "Alt age has not been set yet. Using default: 7 days.", colour = random.choice(ListColours), description = "Please use `ad!setage [days]` to set a the alt age identification.")
			await ctx.send(embed = embed)
		elif result is not None:
			embed = discord.Embed(title = f"Alt age is set to {result[0]}.", colour = random.choice(ListColours), description = "Use `ad!setage [days]` to set a the alt age identification.")
			await ctx.send(embed = embed)
	else:
		db = sqlite3.connect("db.sqlite")
		cursor = db.cursor()
		cursor.execute(f"SELECT alt_age FROM main WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO main(guild_id, alt_age) VALUES(?, ?)")
			val = (ctx.guild.id, age)
			await ctx.send(f'Alt age has been set to {age} days.')
		elif result is not None:
			sql = ("UPDATE main SET alt_age = ? WHERE guild_id = ?")
			val = (age, ctx.guild.id)
			await ctx.send(f'Alt age has been updated to {age} days.')
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()

@setage.error
async def setage_error(ctx, error):
		if isinstance(error, commands.CheckFailure):
				await ctx.send('You do not have the permissions to invoke this command.\nRequired permission: `Administrator`.')


'''
@bot.command()
@commands.has_permissions(administrator = True)
async def setmute(ctx, role: discord.Role):
	db = sqlite3.connect("db.sqlite")
	cursor = db.cursor()
	cursor.execute(f"SELECT muted_role FROM main WHERE guild_id = {ctx.guild.id}")
	result = cursor.fetchone()
	if result is None:
		sql = ("INSERT INTO main(guild_id, muted_role) VALUES(?, ?)")
		val = (ctx.guild.id, role.id)
		await ctx.send(f'Mute role has been set to {role.mention}')
	elif result is not None:
		sql = ("UPDATE main SET muted_role = ? WHERE guild_id = ?")
		val = (role.id, ctx.guild.id)
		await ctx.send(f'muted role has been updated to {role.mention}')
	cursor.execute(sql, val)
	db.commit()
	cursor.close()
	db.close()
'''

@bot.command()
@commands.has_permissions(administrator = True)
async def setnotify(ctx, role: discord.Role = None):
	if role == None:
		db = sqlite3.connect("db.sqlite")
		cursor = db.cursor()
		cursor.execute(f"SELECT notify FROM main WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result is None:
			embed = discord.Embed(title = "Notify role feed has not been set yet.", colour = random.choice(ListColours), description = "Please use `ad!setnotify [@role/role_id]` to set a Notify role.")
			await ctx.send(embed = embed)
		elif result is not None:
			embed = discord.Embed(title = f"Notify role is been set to {result[0]}.", colour = random.choice(ListColours), description = "Use `ad!setnotify [@role/role_id]` to change the Notify role.")
			await ctx.send(embed = embed)
	else:
		db = sqlite3.connect("db.sqlite")
		cursor = db.cursor()
		cursor.execute(f"SELECT notify FROM main WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO main(guild_id, notify) VALUES(?, ?)")
			val = (ctx.guild.id, role.id)
			await ctx.send(f"Notify role has been set to {role.mention}. Please make sure the bots role is above the role to be notified.")
		elif result is not None:
			sql = ("UPDATE main SET notify = ? WHERE guild_id = ?")
			val = (role.id, ctx.guild.id)
			await ctx.send(f'Notify role has been updated to {role.mention}. Please make sure the bots role is above the role to be notified.')
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()

@setnotify.error
async def setnotify_error(ctx, error):
		if isinstance(error, commands.CheckFailure):
				await ctx.send('You do not have the permissions to invoke this command.\nRequired permission: `Administrator`.')

@bot.command()
@commands.has_permissions(administrator = True)
async def setprefix(ctx, prefix = None):
	db = sqlite3.connect("db.sqlite")
	cursor = db.cursor()
	cursor.execute(f"SELECT prefix FROM main WHERE guild_id = {ctx.guild.id}")
	result = cursor.fetchone()
	if prefix is None:
		await ctx.send(f'{ctx.author.mention} the current prefix for this server is `{result[0]}`.')
	elif prefix is not None:
		sql = ("UPDATE main SET prefix = ? WHERE guild_id = ?")
		val = (prefix, ctx.guild.id)
		await ctx.send(f'{ctx.author.mention} the prefix has been successfully set to `{prefix}`')
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()

@bot.command()
@commands.has_permissions(administrator = True)
async def whois(ctx, member: discord.Member = None):
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

@whois.error
async def whois_error(ctx, error):
		if isinstance(error, commands.CheckFailure):
				await ctx.send('You do not have the permissions to invoke this command.\nRequired permission: `Administrator`.')

@bot.command()
async def invite(ctx):
	embed = discord.Embed(colour = random.choice(ListColours))
	embed.set_author(name = "Invite links!", icon_url = bot.user.avatar_url)
	embed.add_field(name = "Invite the bot", value = "[Invite me](https://discordapp.com/oauth2/authorize?client_id=699174992046456832&permissions=268435456&scope=bot)")
	embed.add_field(name = "Support server", value = "[Click here](http://discord.gg/wnGWA5K)")
	await ctx.send(embed = embed)

@bot.command()
async def botinfo(ctx):
	db = sqlite3.connect("version.sqlite")
	cursor = db.cursor()
	cursor.execute(f"SELECT Version FROM main WHERE Title = 428185775910420480")
	result = cursor.fetchone() 
	number = len(bot.guilds)
	creater = '4041RebL(428185775910420480)'
	version = result[0]
	invite = "[Invite me](https://discordapp.com/oauth2/authorize?client_id=699174992046456832&permissions=268435456&scope=bot)"
	server = "[Click here](http://discord.gg/wnGWA5K)"
	count = 0
	for guild in bot.guilds:
		count += len(guild.members)
	embed = discord.Embed(colour = random.choice(ListColours))
	embed.set_author(name = "Bot information")
	embed.add_field(name = "Creator", value = creater, inline = False)
	embed.add_field(name = "Version", value = version, inline = False)
	embed.add_field(name = "Server Count", value = number, inline = False)
	embed.add_field(name = "Watching over", value = f"{count} users.", inline = False)
	embed.add_field(name = "Invite", value = invite)
	embed.add_field(name = "Support Server", value = server)
	await ctx.send(embed = embed)

@bot.event
async def on_guild_join(guild):

	db = sqlite3.connect("db.sqlite")
	cursor = db.cursor()
	cursor.execute(f"SELECT prefix FROM main WHERE guild_id = {guild.id}")
	result = cursor.fetchone() 
	if result is None:
		sql = ("INSERT INTO main(guild_id, prefix) VALUES(?, ?)")
		val = (guild.id, "ad!")
	elif result is not None:
		sql = ("UPDATE main SET prefix = ? WHERE guild_id = ?")
		val = ("ad!", guild.id)
	cursor.execute(sql, val)
	db.commit()
	cursor.close()
	db.close()

	embed = discord.Embed(colour = random.choice(ListColours))
	embed.set_author(name = "Guild Joined")
	embed.set_thumbnail(url = guild.icon_url)
	embed.add_field(name = "Guild name:", value = guild.name, inline = False)
	embed.add_field(name = "Guild ID:", value = guild.id, inline = False)
	embed.add_field(name = "Guild owner:", value = guild.owner, inline = False)
	embed.add_field(name = "Total server count:", value = len(bot.guilds), inline = False)
	embed.add_field(name = "Member count:", value = len(guild.members), inline = False)
	channel = bot.get_channel(699295182558068786)
	await channel.send(embed = embed)

@bot.event
async def on_guild_remove(guild):
	embed = discord.Embed(colour = random.choice(ListColours))
	embed.set_author(name = "Guild Left")
	embed.set_thumbnail(url = guild.icon_url)
	embed.add_field(name = "Guild name:", value = guild.name, inline = False)
	embed.add_field(name = "Guild ID:", value = guild.id, inline = False)
	embed.add_field(name = "Guild owner:", value = guild.owner, inline = False)
	embed.add_field(name = "Total server count:", value = len(bot.guilds), inline = False)
	embed.add_field(name = "Member count:", value = len(guild.members), inline = False)
	channel = bot.get_channel(699295182558068786)
	await channel.send(embed = embed)

@bot.command()
async def knownerrors(ctx):
	embed = discord.Embed(colour = random.choice(ListColours))
	embed.add_field(name = "Bot doesn't log!", value = "If the bot doesn't log, make sure to use `ad!setchannel` and `ad!setnotify`. If the bot still does not respond, report it to 4041RebL in the support server.", inline = False)
	embed.add_field(name = "Bot does not ping role!", value = "Make sure the bot's role is above the role to be pinged. The role to be pinged, initially, must be set to unmentionable. The bot also needs the MANAGE_ROLES permission to work perfectly!.", inline = False)
	embed.add_field(name = "Bot still doesn't log!", value = "Please double-check if the bot has permissions to send message in the channel you designated", inline = False)
	embed.add_field(name = "Support server", value = "[Click Here](http://discord.gg/wnGWA5K)")
	await ctx.send(embed = embed)


@bot.command()
@commands.has_permissions(administrator = True)
async def fetchalts(ctx, arg: int):
	msg = await ctx.send(f'<a:bot_offline:700602112949747772> Fetching accounts younger than `{arg}` days.\nIf the list is long, it may cause a big embed to popup in this channel.\nReact with a <a:online:700609324602490941> to confirm.\nThe reaction confirmation will timeout in 60 seconds.')
	await msg.add_reaction('<a:online:700609324602490941>')

	def check(reaction, user):
		return user == ctx.author and str(reaction.emoji) == '<a:online:700609324602490941>'

	try:
		reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
	except asyncio.TimeoutError:
		await ctx.send("Reaction timed out.")
		await msg.remove_reaction('<a:online:700609324602490941>', bot.user)
	else:
		if ctx.author.id == 428185775910420480:
				members = ctx.guild.members
				count = 1
				page = 1
				embed = discord.Embed(title = "S.No.					 ID							 age(in days)", color = random.choice(ListColours))
				embed.set_footer(text = f"Page number: {page}")
				for member in members:
						member_age = datetime.utcnow() - member.created_at
						days = member_age.days
						if days < arg:
							if count > 10:
								if page == 1:
									await msg.remove_reaction('<a:online:700609324602490941>', bot.user)
									await msg.edit(embed = embed)
									page = page + 1
									await msg.add_reaction('<:next:709326566945062934>')

									def check1(reaction, user):
										return user == ctx.author and str(reaction.emoji) == '<:next:709326566945062934>'
									
									try:
										reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check1)
									except asyncio.TimeoutError:
										await msg.remove_reaction('<:next:709326566945062934>', bot.user)
									else:
											embed = discord.Embed(title = "S.No.					 ID							 age(in days)", color = random.choice(ListColours))
											embed.set_footer(text = f"Page number: {page}")
											count = 1
								else:
									await msg.edit(embed = embed)

									def check1(reaction, user):
										return user == ctx.author and str(reaction.emoji) == '<:next:709326566945062934>'
									
									try:
										reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check1)
									except asyncio.TimeoutError:
										await msg.remove_reaction('<:next:709326566945062934>', bot.user)
									else:
										page = page + 1
										embed = discord.Embed(title = "S.No.					 ID							 age(in days)", color = random.choice(ListColours))
										embed.set_footer(text = f"Page number: {page}")
										count = 1
							else:
								embed.add_field(name = f"{count}.		{member.id}		 -		 {days}", value = f'{member.name}#{member.discriminator}', inline = False)
								count += 1
				if count <= 10:
						await msg.edit(embed = embed)
						await msg.remove_reaction('<:next:709326566945062934>', bot.user)
				else:
						return
		else:
				if arg < 90:
						members = ctx.guild.members
						count = 1
						page = 1
						embed = discord.Embed(title = "S.No.		 -			ID				-			 age(in days)", color = random.choice(ListColours))
						embed.set_footer(text = f"Page number: {page}")
						for member in members:
								member_age = datetime.utcnow() - member.created_at
								days = member_age.days
								if days < arg:
									if count > 10:
										if page == 1:
											await msg.remove_reaction('<a:online:700609324602490941>', bot.user)
											await msg.edit(embed = embed)
											page = page + 1
											await msg.add_reaction('<:next:709326566945062934>')

											def check1(reaction, user):
												return user == ctx.author and str(reaction.emoji) == '<:next:709326566945062934>'
									
											try:
												reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check1)
											except asyncio.TimeoutError:
												await msg.remove_reaction('<:next:709326566945062934>', bot.user)
											else:
												embed = discord.Embed(title = "S.No.					 ID							 age(in days)", color = random.choice(ListColours))
												embed.set_footer(text = f"Page number: {page}")
												count = 1
										else:
											await msg.edit(embed = embed)

											def check1(reaction, user):
												return user == ctx.author and str(reaction.emoji) == '<:next:709326566945062934>'
									
											try:
												reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check1)
											except asyncio.TimeoutError:
												await msg.remove_reaction('<:next:709326566945062934>', bot.user)
											else:
												page = page + 1
												embed = discord.Embed(title = "S.No.					 ID							 age(in days)", color = random.choice(ListColours))
												embed.set_footer(text = f"Page number: {page}")
												count = 1
									else:
										embed.add_field(name = f"{count}.		{member.id}		 -		 {days}", value = f'{member.name}#{member.discriminator}', inline = False)
										count += 1
						if count <= 10:
							await msg.edit(embed = embed)
						else:
							return
				else: 
						await ctx.send("The `days` argument cannot be higher than 90.\nOnly the bot owner, `4041RebL`, may enter the `[day]` parameter's value higher than 90 days.\nPlease contanct him incase you need to use this command.\nThis is to prevent spam")

@fetchalts.error
async def fetchalts_error(ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
				await ctx.send('Please proved a `[days]` argument.\nFor more information, use `ad!help fetchalts`.')
		if isinstance(error, commands.CheckFailure):
				await ctx.send('You do not have the permissions to invoke this command.\nRequired permission: `Administrator`.')

@bot.command()
async def ping(ctx):
		before = time.monotonic()
		message = await ctx.send("Pong!")
		ping = (time.monotonic() - before) * 1000
		await message.edit(content=f"Pong! `{int(ping)} ms`")

@bot.command()
@commands.has_permissions(administrator = True)
async def members(ctx, *, role: discord.Role):
	guild = ctx.guild
	members = guild.members
	string = ""
	space = "			"
	count = 1
	for member in members:
		if role in member.roles:
			if count == 1:
				string = string + member.mention + space
				count +=1
			else:
				string = f"{string}\n{member.mention}{space}"
	embed = discord.Embed(color = random.choice(ListColours), description = string)
	embed.set_author(name = "Members in "+role.name)
	await ctx.send(embed = embed)

@bot.command()
async def check(ctx, id: int):
		if ctx.author.id == 428185775910420480:
			guild = bot.get_guild(id)
			db = sqlite3.connect("db.sqlite")
			cursor = db.cursor()
			cursor.execute(f"SELECT prefix FROM main WHERE guild_id = {guild.id}")
			prefix_raw = cursor.fetchone()
			prefix = prefix_raw[0]
			cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {guild.id}")
			channel_id = cursor.fetchone()
			cursor.execute(f"SELECT notify FROM main WHERE guild_id = {guild.id}")
			notify_id = cursor.fetchone()
			cursor.execute(f"SELECT alt_age FROM main WHERE guild_id = {guild.id}")
			alt_age = cursor.fetchone()

			if channel_id[0]:
				channel = "#"+guild.get_channel(int(channel_id[0])).name
			else:
				channel = "Not Set"

			if notify_id[0]:
				notify = "@"+guild.get_role(int(notify_id[0])).name
			else:
				notify = "Not Set"

			if alt_age[0]:
				age = alt_age[0]
			else:
				age = "7(default)"

			embed = discord.Embed()
			embed.set_author(name = guild.name)
			embed.set_thumbnail(url = guild.icon_url)
			embed.add_field(name = "Prefix:", value = prefix, inline = False)
			embed.add_field(name = "Feeds Channel:", value = "`"+ channel +"`", inline = False)
			embed.add_field(name = "Notify role:", value = "`"+ notify +"`", inline = False)
			embed.add_field(name = "Alt age:", value = age, inline = False)
			await ctx.send(embed = embed)

@bot.command()
async def upvote(ctx):
	embed = discord.Embed(color = random.choice(ListColours), description = "**[Discord.Bots.gg](https://discord.bots.gg/bots/699174992046456832)**\n\n**[Discord Boats](https://discord.boats/bot/699174992046456832)**\n\n**[Botlist.space](https://botlist.space/bot/699174992046456832)**\n\n**[Bots for Discord](https://botsfordiscord.com/bot/699174992046456832)**")
	embed.set_author(name = "Bot listing sites", icon_url = bot.user.avatar_url)
	await ctx.send(embed = embed)

keep_alive()
token = os.environ.get("TOKEN")
bot.run(token, bot = True, reconnect = True)