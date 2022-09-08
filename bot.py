from multiprocessing.dummy import current_process
import discord
from discord.ext import commands
import time
import aiohttp
import io
from pip._vendor import requests
from sqlite3.dbapi2 import Cursor
import sqlite3

client = commands.Bot(command_prefix= "?")
client.remove_command("help")


@client.event
async def on_ready():
    db = sqlite3.connect("warns.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS warns(guild_id INT, user_id INT, content STR, author_id INT, time INT)")
    cursor.close()
    db.close()
    print("gotowe")

##banowanie

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
  await user.ban(reason=reason)
  await ctx.send(f"{user} został zbanowany za {reason}")

##warnowanie

@client.command()
@commands.has_permissions(ban_members=True)
async def warn(ctx, member: discord.Member, *,reason):
    db = sqlite3.connect("warns.db")
    cursor = db.cursor()
    cursor.execute("INSERT INTO warns(guild_id, user_id, content, author_id, time) VALUES(?, ?, ?, ?, ?)", (ctx.author.guild.id, member.id, reason, ctx.author.id, time.time()))
    db.commit()
    cursor.close()
    db.close()
    await ctx.send(f"Zwarnowałeś użytkownika {member.name} za {reason}")

## help

@client.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(title = "Pomoc", description = "", color = discord.Colour.green())
    embed.add_field(name = "Lista komend", value = "Tutaj są wszystkie komendy", inline = False)
    embed.add_field(name = "?trol", value = "Sprawdź a się dowiesz", inline = False)
    embed.add_field(name = "?triggered", value = "Triggeruje oznaczoną osobę", inline = False)
    embed.add_field(name = "?godzina", value = "Pokazuje aktualną godzinę", inline = False)
    embed.add_field(name = "?pies", value = "Wysyła ci zdjęcie słodkiego piseka UwU", inline = False)
    embed.add_field(name = "?warn [@użytkownik] [powód]", value = "Ostrzerzenie", inline = False)
    embed.add_field(name = "?join", value = "Dołączanie bota do voice channelu", inline = False)
    embed.add_field(name = "?play", value = "Puszczanie muzyki", inline = False)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

##pokazuje aktualną godzinę

@client.command()
async def godzina(ctx):
    strings = time.strftime("**godzina %H**,**minuta %M**,**sekunda %S**")
    t = strings.split(',')
    await ctx.send(strings)

##nakładka 'triggered' na profilowe oznaczonego członka

@client.command()
async def triggered(ctx, member: discord.Member = None):
    if not member:  # if no member is mentioned
        member = ctx.author  # the user who ran the command will be the member

    async with aiohttp.ClientSession() as wastedSession:
        async with wastedSession.get(
                f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage:  # get users avatar as png with 1024 size
            imageData = io.BytesIO(await wastedImage.read())  # read the image/bytes
            await wastedSession.close()  # closing the session and;
            await ctx.reply(file=discord.File(imageData, 'triggered.gif'))  # sending the file

##wysyła ci zdjęcie słodkiego piseka UwU

@client.command()
async def pies(ctx):
    response = requests.get('https://some-random-api.ml/img/dog')
    data = response.json()
    embed = discord.Embed(
        title = 'pies!',
        description = '',
        colour = discord.Colour.green()
          )
    embed.set_image(url=data['link'])
    embed.set_footer(text="")
    await ctx.send(embed=embed)

##rick roll

@client.command()
async def trol(ctx):
    embed=discord.Embed()
    embed.set_thumbnail(url="https://media0.giphy.com/media/10kABVanhwykJW/giphy.gif?cid=790b7611e7d60e8d6e375ab47e280a482e4973a3f70af0a7&rid=giphy.gif&ct=g%22")
    embed.add_field(name="zostałeś", value="zrickrollowany", inline=False)
    await ctx.send(embed=embed)



client.run("token")
