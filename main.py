import discord
from discord.ext import commands
import random
import json
from datetime import datetime
import asyncio
import time

def get_prefix(bot, message):
	with open("settings.json", "r") as f:
		file = json.load(f)

	return file["prefix"]
	
bot = commands.Bot(command_prefix = get_prefix)
start_time = time.time()
bot.remove_command('help')

cogs = ['cogs.Help_command', 'cogs.uptime', 'cogs.mod']

@bot.event
async def on_ready():
	with open("settings.json", "r") as f:
		file = json.load(f)
	
	if file["custom_status"] == "None":
		print("The bot is ready!")
		for cog in cogs:
			bot.load_extension(cog)
	else:
		Game = discord.Game(file["custom_status"])
		await bot.change_presence(activity = Game)
		print("The bot is ready!")
		for cog in cogs:
			bot.load_extension(cog)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)

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
	with open("settings.json", "r") as f:
		file = json.load(f)

	guild_id = file["server_id"]
	if guild_id == "your-server-id": #DO NOT EDIT THIS LINE
		guild = None
	else:
		guild = bot.get_guild(int(guild_id))

	channel_id = file["log_channel"]
	if channel_id == "your-log-channel-id": #DO NOT EDIT THIS LINE
		channel = None
	else:
		channel = bot.get_channel(int(channel_id))

	notify_id = file["notify_role"]
	if notify_id == "your-notify-role-id": #DO NOT EDIT THIS LINE
		notify_role = None
	else:
		if guild is not None:
			notify_role = guild.get_role(int(notify_id))
	
	altage = file[int("alt_age")]

	joined_at = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p")
	precise_member_age = datetime.utcnow() - member.created_at
	member_age = precise_member_age.days	

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

	if channel_id == None:
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
async def whois(ctx, member: discord.Member = None):
	if member == None:
		member = ctx.author

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
async def botinfo(ctx):
	creater = '4041RebL(428185775910420480)'
	embed = discord.Embed(colour = random.choice(ListColours))
	embed.set_author(name = "Bot information")
	embed.add_field(name = "Creator", value = creater, inline = False)
	embed.add_field(name = "Information:", value = "The bot is open sourced in github, for anyone to use.")
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

with open("settings.json", "r") as f:
	file = json.load(f)

token = file["TOKEN"]
if token == "your-bot-token-here":
	print("You need to provide a token in the file settings.json to run the bot.")
else:
	bot.run(token, bot = True, reconnect = True)