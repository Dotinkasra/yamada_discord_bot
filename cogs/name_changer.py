from discord.ext import commands
from discord import app_commands
import discord
import json

class NameChanger(commands.Cog):
    """
    名前を変更する機能

    Parameters
    ----------
    commands : commands.Bot
        Botのインスタンス
    """
    def __init__(self, bot: commands.Cog):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Successfully loaded : NameChanger')

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        config = self.get_nicknames()

        if str(before.id) not in config:
            return
        
        await before.edit(nick = config[str(before.id)])

    def get_nicknames(self) -> dict:
        with open("./env/config.json") as j:
            config = json.load(j)
        return config["nickname"]

async def setup(bot: commands.Bot):
    await bot.add_cog(NameChanger(bot))
