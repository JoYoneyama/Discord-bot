import asyncio
import os
import time
import discord

from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from discord import app_commands, FFmpegPCMAudio
from discord.ext import commands

# --------------

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
queue = []
song_queue = []

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logado como {self.user}!")

    async def on_message(self, command):       # todos os comandos do bot
        if self.user.mention in command.content:           # bot acionado ao ser mencionado
            command_content = command.content[len(self.user.mention):].strip()  # o content possui o id do bot q foi mencionado, ent tem q tirar

             # comandos do bot

            # play
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
                        title = info["title"]
                        duration = info["duration"]

                    source = FFmpegPCMAudio(audio_url)
                    queue.append([title, duration])
                    song_queue.append(source)

                    # funcao intermediaria para chamar next_song. o after n aceita funcoes assincronas, logo, precisa de uma funcao intermediaria usando run_coroutine_threadsafe
                    # para chamar uma funcao assincrona onde n daria
                    def call_next(error):    
                        if error:
                            print("erro")

                        asyncio.run_coroutine_threadsafe(next_song(command, voice), client.loop)

                    # funcao chamada para tocar a fila de musicas
                    async def next_song(command, voice):
                        if song_queue:
                            next = song_queue.pop(0)
                            await asyncio.sleep(3)
                            voice.play(next, after=lambda e: call_next(e))
                        else:
                            await command.channel.send("Sem músicas na fila")

                    if not voice.is_playing():
                        voice.play(song_queue[0], after=lambda e: call_next(e))
                else:
                    await command.channel.send("Você precisa estar em um canal de voz!")

            # disconnect
            elif "disconnect" in command_content:
                if command.guild.voice_client:
                    queue.clear()
                    await command.guild.voice_client.disconnect()
                    await command.channel.send("Desconectando bot do canal.")

            elif "queue" in command_content:
                if command.guild.voice_client and len(queue) > 0:
                    await command.channel.send(queue)
                elif command.guild.voice_client and queue <= 0:
                    await command.channel.send("Sem músicas na fila.")

            else:
                await command.channel.send("Este comando não existe.")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)