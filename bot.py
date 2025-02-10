import os
import discord

from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands


load_dotenv()
token = os.getenv("DISCORD_TOKEN")


class MyClient(commands.Bot):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    # async def on_message(self, message):
    #     print(f"message from {message.author}: {message.content}")        


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(command_prefix="!", intents=intents)

@client.command()
async def falar(ctx, string=""):
    await ctx.send(f"falando {string}")


client.run(token)