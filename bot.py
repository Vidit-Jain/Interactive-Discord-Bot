import discord
from discord.ext import commands
import random
import os

bot = commands.Bot(command_prefix = '.')

def checkName(author):
    'Returns true if the name is already present in the list, else returns false'

    with open("realNames.txt", "r") as f:
        for person in f:
            _id, name = tuple(person.split(" = ", 1))
            if str(author.id) == _id:
                return True
    return False


def selfIdentify(_id, name):
    'Adds the name to the list'

    with open("realNames.txt","a+") as f:
        f.write(f'{_id} = {name}\n')


def findName(person):
    'Gets the identified name of the mentioned user'

    with open("realNames.txt", "r+") as f:
        for entry in f:
            _id, name = entry.split(" = ", 1)
            if str(person.id) == _id:
                return name
    return "not found\n"


def removeName(userId):
    'To remove the identity of the user'

    isPresent = False
    with open("realNames.txt", 'r') as f:
        with open("temp.txt", 'w') as fout:
            for person in f:
                _id, name = person.split(' = ', 1)
                if (str(userId)) == _id:
                    isPresent = True
                else:
                    fout.write(person)
    if (isPresent):
        os.remove('realNames.txt')
        os.rename('temp.txt', 'realNames.txt')
        return "you are removed"
    
    return "your identity doesn't exist"



@bot.event
async def on_ready():
    'Just to show that the bot is online and functioning'

    print ('Bot is ready')


@bot.event
async def on_member_join(member):
    'To keep a track of who has entered the server'

    print(f'{member} has joined a server')


@bot.event
async def on_member_remove(member):
    'To keep a track of who has exited the server'

    print(f'{member} has left the server')


@bot.command()
async def ping(context):
    'To get the time taken by the bot to reply'

    await context.send(f'{round(bot.latency * 1000)}ms')


@bot.command(aliases = ['8ball'])
async def _8ball(context, *, q):
    'A fun section where the bot predicts answers'

    res = list(open('8ballResponses.txt', 'r').readlines())
    await context.send(f'Question: {q}\nAnswer: {random.choice(res)}')


@bot.command(aliases = ['remove'])
async def clear(ctx, amt = 10):
    'To remove some lines from the history'

    await ctx.channel.purge(limit=amt+1)


@bot.command(aliases = ['selfid', 'sid'])
async def selfidentify(ctx, *, name):
    'You can add your identity from here'

    author = ctx.author
    if (checkName(author)):
        await ctx.send(f'{author} your current identity is {findName(author)}To change your identity, remove your current identity and try again')
        return
    
    selfIdentify(author.id ,name)
    await ctx.send(f'{author}, you are identified as {name}!')


@bot.command(aliases = ['id'])
async def identify(ctx):
    'You can find any users identity from here if they have added it'

    ans = ''
    for person in ctx.message.mentions:
        ans += f'{person} is {findName(person)}'
    await ctx.send(ans)


@bot.command(aliases = ['removeid', 'rid'])
async def removeidentity(ctx):
    'To remove your current identity'

    _id = ctx.author.id
    await ctx.send(f'{ctx.author} {removeName(_id)}')


# @bot.command()
# async def sdentify(ctx, *, name):
#     'To self identify a person'
#     await ctx.send(f'{ctx.author}, you are identified as {name}')
#
bot.run(open('token.txt', 'r').readline())