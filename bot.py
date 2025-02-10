import os
import discord

from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from discord import app_commands, FFmpegPCMAudio
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
client = MyClient(command_prefix="@Testando", intents=intents)

# comandos do bot

@client.command()
async def falar(ctx, string=""):
    await ctx.send(f"falando {string}")

@client.command()
async def play(ctx, url):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()

        ydl_opts = {
            "format": "bestaudio"
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info["url"]

        source = FFmpegPCMAudio(audio_url)
        voice.play(source)        
    else:
        await ctx.send("Você precisa estar em um canal de voz!")

@client.command()
async def disconnect(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Vazei")

# ---------------------

client.run(token)