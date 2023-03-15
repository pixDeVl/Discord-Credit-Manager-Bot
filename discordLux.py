import platform
import discord
import os
import datetime 
from discord import app_commands
from discord.ext import commands
import sqlite3
from typing import Optional
import asyncio
import time
from colorama import Back, Fore, Style
from dotenv import load_dotenv
load_dotenv('.env')


MY_GUILD = discord.Object(1007098070535786587)
#1007098070535786587
#1014918224904724530



def is_dev(interaction: discord.Interaction) -> bool:
    return interaction.user.id == 429708337039278101

goodLux = [
  "Lux is the best", "Lux is cool", "Lux best", "Lux w", "Lux pog",
  "Vestmar lux", "Thank you Lux", "Lux is best", "Lux based", "Based lux",
  "Lux hype", "Vestmar Lux", "Lux best", "Velipix is pog", "Lux is poggers",
  "Praise lux", "Tenebris is the best", "Tenebris is cool", "Tenebris best",
  "Tenebris w", "Tenebris pog", "Vestmar tenebris", "Thank you tenebris",
  "Tenebris is best", "Tenebris based", "Based tenebris", "Tenebris hype",
  "Vestmar tenebris", "Tenebris best", "Velipix is poggers",
  "Tenebris is poggers", "Praise tenebris", "Véstmar Lux", "Véstmar Tenebris",
  "Glory to the Empress", "Glory be to the Empress Lux",
  "Glory be to the Empress", "Praise be to glorious Lux"
]
badLux = [
  "Lux thighs", "Tenebris thighs", "Lux cringe", "Cringe lux", "Lux is cringe",
  "Lux not based", "Lux dumb", "Lux is dumb", "Lix thighs"
]
#connection = sqlite3.connect('credits.db')
#cur = connection.cursor
#print('Connected to Database')

def addcredit(user, amount):
  connection = sqlite3.connect('credits.db')
  cur = connection.cursor()
  print('Connected to Database')
  cur.execute(f'SELECT uid FROM luxCredits WHERE uid = {user.id};')
  dec = cur.fetchone()
  print(dec)
  print('r')
  if not dec == None:
    cur.execute(f'''UPDATE luxCredits SET score = {amount} + score, name = '{user.name}', pin = '{user.discriminator}' WHERE uid = {user.id};''')
    connection.commit()

  else: 
    cur.execute(f'''INSERT INTO luxCredits VALUES({user.id}, {amount}, '{user.name}', {user.discriminator});''')
    connection.commit()


  cur.execute('SELECT * FROM luxCredits;')
  print(cur.fetchall())
  connection.commit()
  connection.close()
  print(f"Added {amount} credits to {user.name}")
  return




#invites = app_commands.Group(name="invite",description="Gets the invite to various Lux related guilds",)
class Client(commands.Bot):
  def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=discord.Intents().all())    
    
  async def setup_hook(self):
    # for filename in os.listdir('./cogs'):
    #   if filename.endswith('.py'):
    await self.load_extension('cogs.user_cmds')


  async def on_ready(self):
    prfx = (Back.BLACK + Fore.BLUE + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prfx + " Logged in as " + Fore.MAGENTA + self.user.name)
    print(prfx + " Bot ID " + Fore.MAGENTA + str(self.user.id))
    print(prfx + " Discord Version " + Fore.MAGENTA + discord.__version__)
    print(prfx + " Python Version " + Fore.MAGENTA + str(platform.python_version()))
    synced = await self.tree.sync()
    print(prfx + " Slash CMDs Synced " + Fore.MAGENTA + str(len(synced)) + " Commands")
    await client.change_presence(status=discord.Status.idle,
                               activity=discord.Activity(
                                 type=discord.ActivityType.listening,
                                 name="the prayers to her Empress Lux"))

  
client=Client()

@client.event
async def on_message(message):
  sender = message.author
  msg = message.content

  if sender == client.user and sender.bot != True:
    return

  if any(word in msg.capitalize() for word in goodLux):
      addcredit(sender, 15)

      print(Fore.YELLOW + "{0}" + Fore.WHITE + "said {1}".format(sender, msg))
      await message.reply(
        "**+15 Lux Credits <:PlusLuxCredit:1021129274956193932>**")
  await client.process_commands(message)

   
  if any(word in message.content.capitalize() for word in badLux):
    ##await message.reply("**MINUS LUX CREDITS <:MinusLuxCredits:905242553727742002>!**")
    await print("{} said {}".format(sender, msg))

#@invites.command(name='lux', description='Get a users credit score.')
#@app_commands.checks.cooldown(1, 15)
#@app_commands.describe(hidden='To show the result to everyone; defaults to True')
#async def lux(interaction: discord.Integration, hidden: bool = True):
#  guild = client.get_guild(829016791849631744)
#  embed=discord.Embed(title=f"{guild.name}",description='The offical Lux religon discord server!\n https://discord.gg/3vRnh8tPef',
#  color=0xffbb00,
#  timestamp=datetime.datetime.now())
#  url=guild.icon.url
#  embed.set_thumbnail()
#  embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
#  await interaction.response.send_message(embed=embed, ephemeral=hidden)
#client.tree.add_command(invites, guild=MY_GUILD)


async def load():
#  for filename in os.listdir("./cogs"):
#     if filename.endswith('.py'):
#        await client.load_extension(f'cogs.{filename[:-3]}')
  await client.load_extension('cogs.user_cmds')

async def main():
  await load()
client.run(os.getenv('TOKEN'))
asyncio.run(main())
