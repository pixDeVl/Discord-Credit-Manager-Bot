import datetime
from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class user_cmds(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="cog1", description="Sends hello!")
    async def cog1(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Hello!")

    @app_commands.command( name='score', description='Get a users credit score.')
    @app_commands.checks.cooldown(1, 15)
    @app_commands.describe(hidden='To show the result to everyone; defaults to True', user="The user from who to get a score from; defaults to command user")
    async def score(self, interaction: discord.Integration, user: Optional[discord.Member] ,hidden: bool = True):
        if user == None:
            user = interaction.user
            connection = sqlite3.connect('credits.db')
        cur = connection.cursor()
        cur.execute(f'SELECT score FROM luxCredits WHERE uid = {user.id};')
        cScore=cur.fetchone()
        if cScore == None:
            text = f"{user.name} got no credits or bitches"
        else:
            text = f"**{user.name}'s Credit Score is {cScore[0]}!**"
            embed=discord.Embed(title=text,
            color=0xffbb00,
            timestamp=datetime.datetime.now())
            embed.set_author(icon_url=interaction.user.avatar.url, name=interaction.user)
            await interaction.response.send_message(ephemeral=hidden,embed=embed)


    @app_commands.command( name='leadeboard', description='Get a users credit score.')
    @app_commands.checks.cooldown(1, 15)
    @app_commands.describe(hidden='To show the result to everyone; defaults to True')
    async def leaderboard(self, interaction: discord.Integration, hidden: bool = True):
      connection = sqlite3.connect('credits.db')
      cur = connection.cursor()
      cur.execute(f'SELECT uid, score FROM luxCredits ORDER BY score DESC;')
      cScore=cur.fetchmany(5)
      user = interaction.user
      cur.close


      embed=discord.Embed(title="Global Leaderboard",
      color=0xffbb00,
      timestamp=datetime.datetime.now())
      embed.add_field(name=" ", value=f":first_place:**First Place:** <@{cScore[0][0]}>: `{cScore[0][1]}`", inline=False)
      embed.add_field(name=" ", value=f":second_place:**Second Place:** <@{cScore[1][0]}>: `{cScore[1][1]}`", inline=False)
      embed.add_field(name=" ", value=f":third_place:**First Place:** <@{cScore[2][0]}>: `{cScore[2][1]}`", inline=False)
      embed.add_field(name=" ", value=f"**Forth Place:** <@{cScore[3][0]}>: `{cScore[3][1]}`", inline=False)
      embed.add_field(name=" ", value=f"**Fifth Place:** <@{cScore[4][0]}>: `{cScore[4][1]}`", inline=False)
      embed.set_author(icon_url=interaction.user.avatar.url, name=interaction.user)
      await interaction.response.send_message(ephemeral=hidden,embed=embed)




    @leaderboard.error
    async def on_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):

            await interaction.response.send_message(embed = discord.Embed(title="Error",
              description=f"**Command is on cooldown, please wait `{error.retry_after}` until trying again.**",
              color=0xad0011),ephemeral=True)
        else:
          await interaction.response.send_message(embed = discord.Embed(title="Error",
              description=f"**Error: `{str(error)}`.**",
              color=0xad0011),ephemeral=True)


async def setup(client:commands.Bot) -> None:
    await client.add_cog(user_cmds(client))