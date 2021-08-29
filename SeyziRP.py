import discord
from discord.ext import commands
import sqlite3
import datetime

client = commands.Bot(command_prefix = '&')
client.remove_command('help')
connection = sqlite3.connect('users.db')
cursor = connection.cursor()

@client.event
async def on_ready():
  cursor.execute("""CREATE TABLE IF NOT EXISTS users (name TEXT,id INT,cash BIGINT,rep TEXT,lvl INT,imu TEXT,bank BIGINT,voen TEXT)""")

  for guild in client.guilds:
    for member in guild.members:
      if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 500, '0', 1, 'Нету', '0', 'Нету')")
      else:
        pass

 
  connection.commit()
  print('bot connected')

  await client.change_presence(status = discord.Status.online, activity = discord.Game("Сейзи РП"))


@client.event
async def on_member_join(member):
  if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
    cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 500, '0', 1, 'Нету', '0', 'Нету')")
    connection.commit()
  else:
    pass


@client.command(aliases = ['balance', 'cash', 'Balance', 'Cash', 'BALANCE', 'CASH'])
async def __balance(ctx):
  await ctx.message.add_reaction('✅')
  await ctx.author.send(embed = discord.Embed(
   description = f"""Ваш баланс составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :dollar:**
   На банковском счету: **{cursor.execute("SELECT bank FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :dollar:**"""
  ))


@client.command(aliases = ['time', 'Time'])
async def __time(ctx):
  offset = datetime.timezone(datetime.timedelta(hours=3))
  await ctx.message.add_reaction('✅')
  await ctx.author.send(embed = discord.Embed(
  	description = f"""**{datetime.datetime.now(offset)}**"""))


@client.command(aliases = ['showpass', 'Showpass'])
async def __pass(ctx, member: discord.Member = None):
  if member is None:
    await ctx.send(embed = discord.Embed(
     description = f"""**{ctx.author}** просматривает свой паспорт"""
    ))
    await ctx.author.send(embed = discord.Embed(
     description = f"""Ваш паспорт:
     Имя: **{ctx.author}**
     Лет в штате: **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**
     Военный билет: **{cursor.execute("SELECT voen FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**"""
    ))
  else:
    await ctx.send(embed = discord.Embed(
     description = f"""**{ctx.author}** показывает свой паспорт **{member}**"""
    ))
    await member.send(embed = discord.Embed(
     description = f"""паспорт **{ctx.author}**:
     Имя: **{ctx.author}**
     Лет в штате: **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**
     Военный билет: **{cursor.execute("SELECT voen FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**"""
    ))


@client.command(aliases = ['showmc', 'Showmc'])
@commands.has_role(880420171293003796)
async def __mc(ctx, member: discord.Member = None):
  if member is None:
    await ctx.send(embed = discord.Embed(
     description = f"""**{ctx.author}** просматривает свою мед.карту"""
    ))
    await ctx.author.send(embed = discord.Embed(
     description = f"""
     Ваша мед.карта:
     ``Полностью здоров``""", color = 0x32CD32
    ))
  else:
    await ctx.send(embed = discord.Embed(
     description = f"""**{ctx.author}** показывет свою мед.карту **{member}**"""
    ))
    await ctx.author.send(embed = discord.Embed(
     description = f"""
     мед.карта **{ctx.author}**:
     ``Полностью здоров``""", color = 0x32CD32
    ))

@__mc.error
async def __mc_error(ctx, error):
  await ctx.author.send(embed = discord.Embed(
   description = f"""Ошибка. У вас нет мед.карты"""
  ))

@client.command(aliases = ['showlic', 'Showlic'])
async def __lic(ctx, member: discord.Member = None):
  if commands.has_any_role("Мед.карта"):
    if member is None:
      await ctx.send(embed = discord.Embed(
       description = f"""**{ctx.author}** просматривает свой паспорт"""
      ))
      await ctx.author.send(embed = discord.Embed(
       description = f"""Ваш паспорт:
       Имя: **{ctx.author}**
       Лет в штатЛИЦ ЕСТЬе: **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**
       Военный билет: **{cursor.execute("SELECT voen FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**"""
      ))
  else:
    await ctx.send(embed = discord.Embed(
     description = f"""**{ctx.author}** показывает свой паспорт *dsdsdsd**"""
    ))
    await member.send(embed = discord.Embed(
     description = f"""паспорт **{ctx.author}**:
     Имя: **{ctx.author}**
     Лет в штате: **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**
     Военный билет: **{cursor.execute("SELECT voen FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**"""
    ))


client.run('ODgwMzM2MTkyNjYxNDkxNzIy.YScy-A.IxAkBZGO3tgIKQo4qpHH92VIB6k')