import discord  
from discord.ext import commands
import requests
import json
from discord import Member
from discord.ext.commands import has_permissions , MissingPermissions 

#import api keys from other .py file
from apikeys import *

#Name of the Discord Bot 
discord_name = "Practice Bot"

intents = discord.Intents.default()
intents.members = True # This intent allows the bot to see members in guilds

client = commands.Bot(command_prefix='&' , intents = discord.Intents.all())

#this will give the informaton that bot is running or not
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)#here you can change bot status
    await client.change_presence(activity=discord.Game('With Your Felings'))
    print("The Bot is online")
    print("................")


#this is the first command to print hello
@client.command()
async def hello(ctx):
    await ctx.send(f"Hello , Iam {discord_name}")
    print("iam working , someone call hello Function")

@client.event
async def on_message(message):
    if message.content.lower() == f'hello {discord_name}':
        await message.channel.send('Hello there!, How Can i Help you?')
        await message.channel.send('Type "&command" ')
        print("Someone need CommandPedia ")
    await client.process_commands(message)

@client.command()
async def command(ctx):
    await ctx.send("hello, joke , join , leave ")
    print("all commands sends")

#On rare chance some one say Thank you 
@client.command()
async def thanks(ctx):
    await ctx.send(f"Your Welcome , Thanks for using {discord_name}")
    print("iam working , someone call hello Function")

#this command give jokes ,  when it get call 
@client.command()
async def joke(ctx):
    jokeurl = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
	    "X-RapidAPI-Key": RapidAPI_key,
	    "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.request("GET", jokeurl, headers=headers)
    data = json.loads(response.text)
    setup = data['body'][0]['setup']
    punchline = data['body'][0]['punchline']
    await ctx.send(setup)
    await ctx.send(punchline)
    print("someone call joke function")

#This command will help to Join the bot into voice channel 
@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        print("join the Voice channel")
    else:
        await ctx.send("Your are not in a voice channel")

#This command will help you to play songs when you are in voice channel 
@client.command(pass_context=True)
async def play(ctx, *, song_name):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = ctx.voice_client
        if not voice_client:
            await channel.connect()
            voice_client = ctx.voice_client
        url = "https://deezerdevs-deezer.p.rapidapi.com/search"

        querystring = {"q": song_name}

        headers = {
        "X-RapidAPI-Key": RapidAPI_key,
         "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)
        # play the song here
        # TODO: Add code to play the song using the voice client
        print("Playing song:", song_name)
        await ctx.send("Now playing this song: {}".format(song_name))
    else:
        await ctx.send("Your are not in a voice channel")

    
#this command will work when you said to leave the voice channel 
@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the Channel")
        print("leave the voice channel")
    else:
        await ctx.send("Iam not in a voice channel ")
    


#this event works when someone joins the server
@client.event
async def on_member_join(member):
    channel = client.get_channel(1088500234142887988)
    await channel.send(f"Hello! Welcome to the server {member.mention}")
    print("Someone joined the server")


#this event works when someone leave  the server
@client.event
async def on_member_remove(member):
    channel = client.get_channel(1088500234142887988)
    #await channel.send("Someone leaved the server")
    print("someone leave the server")


#this event helps to delete inappropiate words and give woring to persion
badword = ['saala' , 'saale' , 'kutta' , 'kamina']
@client.event
async def on_message(message):    
    for word in badword:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f"Don't send inappropriate Words {message.author.mention}")
            print(f"word has been deleted. Said by {message.author} , word is {word}")
    print("badword get deleted")
    await client.process_commands(message)

#this code helps to assign role 
@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def addRole(self, ctx, user: discord.Member, *, role: discord.Role):
    if role in user.roles:
        await ctx.send(f"{user.Member} already has the role {role}")
    else:
        await user.add_roles(role)
        await ctx.send(f"Added {role} to {user}")
    print("Someone call AddRole command")

#this oprates error in assinng ole  
@addRole.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a member and a role.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found. Please specify a valid member.")
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send("Role not found. Please specify a valid role.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command.")
    else:
        await ctx.send("An error occurred while executing the command.")



@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def removeRole(self, ctx, user: discord.Member, *, role: discord.Role):
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f"Removed {role} from {user.mention}")
    else:
        await ctx.send(f"{user.mention} does not have role {role}")

@removeRole.error
async def removeRole_error(self, ctx, error):
    if isinstance(error , commands.MissingPermissions):
        await ctx.send("You dont have Permission  to use this command!")

#this is your discord tiken id
client.run(Bot_token)