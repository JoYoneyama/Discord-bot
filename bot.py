import asyncio
import os
import discord

from extension import *
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from discord import app_commands, FFmpegPCMAudio
from discord.ext import commands


load_dotenv()
token = os.getenv("DISCORD_TOKEN")


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logado como {self.user}!")

    async def on_message(self, command):       # todos os comandos do bot
        if self.user.mention in command.content:           # bot acionado ao ser mencionado
            command_content = command.content[len(self.user.mention):].strip()  # o content possui o id do bot q foi mencionado, ent tem q tirar

             # comandos do bot

            if "play" in command_content:
                url = command_content[len("play"):].strip()

                if command.author.voice:
                    if not command.guild.voice_client:
                        channel = command.author.voice.channel
                        voice = await channel.connect()
                    else:                                      # se o bot ja estiver no canal
                        voice = command.guild.voice_client  

                    # tocando musica

                    ydl_opts = {
                        "format": "bestaudio"
                    }

                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        audio_url = info["url"]

                    source = FFmpegPCMAudio(audio_url)
                    voice.play(source)  
                else:
                    await command.channel.send("Você precisa estar em um canal de voz!")

            if "disconnect" in command_content:
                if command.guild.voice_client:
                    await command.guild.voice_client.disconnect()
                    await command.channel.send("Vazei")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)