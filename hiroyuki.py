from discord.ext import commands
import discord
from env.config import Config
import asyncio

INITIAL_EXTENSIONS = [
    'cogs.call_counter',
    'cogs.post_forum',
    'cogs.send_dm',
    'cogs.random_grouping',
    'cogs.image_catcher',
    'cogs.name_changer',
]

config = Config()

intents = discord.Intents.all()

TOKEN = config.token
guilds = config.guilds

activity = discord.Activity(name="東京チンポコ大学", type=discord.ActivityType.competing)
bot = commands.Bot(command_prefix='h!', intents = intents, activity = activity)

async def load_extension():
    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)
        
async def main():
    async with bot:
        await load_extension()
        
        await bot.start(TOKEN)

@bot.event
async def on_ready():
    print("BOT Started!")
    sever_id = 1054929219144130703
    await bot.tree.sync(guild=discord.Object(sever_id))
    print("Sync tree finished")

asyncio.run(main())
