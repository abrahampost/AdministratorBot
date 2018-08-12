import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

client = Bot(description="Administrative bot", command_prefix="$")

@client.event
async def on_ready():
	print("Logged in as " +client.user.name + " (ID: " + client.user.id +")")
	print("https://discordapp.com/oath2/authorize?client_id={}&scope=bot&permission=8".format(client.user.id))

@client.command(pass_context=True)
async def nick(ctx, *args):
	if len(args) < 2:
		await client.say("Error: proper command usage is '$nick <user> <nickname>'")
		return
	
	#get relevant info from the context of the message
	server = ctx.message.server
	mentions = ctx.message.mentions
	
	#if it tries to at multiple people at once, bounce
	if len(mentions) != 1:
		await client.say("Error: {} users mentioned, expected 1".format(len(mentions)))
		return
	member_to_change = mentions[0]
	
	#Disallow from changing own nickname
	if member_to_change == ctx.message.author:
		await client.say("Error: Unable to change own nickname")
		return
		
	#Don't let the bot change his own nickname
	if member_to_change == client.user:
		await client.say("Error: Please don't try and change my nickname")
		return
		
	#if it can't find the member, exit
	if not member_to_change:
		await client.say("No member named '{}' found".format(args[0]))
		return
	nickname = ' '.join(args[1:])
	
	try:
		await client.change_nickname(member_to_change, nickname)
	except Exception as e:
		#if it fails somehow, fail gracefully
		await client.say("Unable to change nickname")
		print(e)
	else:
		#if it doesn't catch any erros
		await client.say("Successfully changed nickname")
	
with open ("token.txt", "r") as file:
	token = file.read()
client.run(token)