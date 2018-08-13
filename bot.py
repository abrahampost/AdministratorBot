import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import requests
import random
import markovify

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

@client.command(pass_context=True)
async def slay(ctx):
	#get a random member from the server
	server = ctx.message.server
	members = server.members
	random_member = get_random(members)
	
	#get a random insult and change its format to mention someone
	insult = requests.get("https://insult.mattbas.org/api/insult")
	insult = insult.text[8:]
	
	#Connect the two and send it
	final_insult = "<@!{}> is {}".format(random_member.id, insult)
	await client.say(final_insult)
	
@client.command(pass_context=True)
async def flavortown(ctx):
	text = ""
	#make a big list of messages
	async for message in client.logs_from(ctx.message.channel, limit=400):
		#if message.author != client.user:
		text += message.content
		text += " \n"
	#build the model
	model = markovify.NewlineText(text)
	#say some stuff
	for i in range(5):
		response = model.make_sentence(test_output=False)
		if response:
			await client.say(response)

def get_random(members):
	rand_index = random.randint(0, len(members))
	i = 0
	for member in members:
		if i != rand_index:
			i += 1
		else:
			return member
	
with open ("token.txt", "r") as file:
	token = file.read()
client.run(token)