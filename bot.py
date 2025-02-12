import asyncio
import os
import discord

from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from discord import FFmpegPCMAudio
from pytube import Search

# --------------

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
queue = []
song_queue = []
pos = 0

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

                    # configuracoes
                    ydl_opts = {
                        "quiet": True,
                        "format": "bestaudio",
                        # "extract_flat": True,
                        # "noplaylist": True,
                        # 'force_generic_extractor': True,
                    }

                    FFMPEG_OPTIONS = {
                        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                        'options': '-vn',  # Não pega vídeo, apenas áudio
                    }

                    # tocando musica
                    if url.startswith("https"):
                        with YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=False)
                            audio_url = info["url"]
                            title = info["title"]
                    else:
                        search = Search(url)
                        results = search.results
                        first = results[0]

                        with YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(first.watch_url, download=False)
                            audio_url = info["url"]
                            title = info["title"]

                    source = FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
                    queue.append(title)
                    song_queue.append([source, title])

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

                            now_playing = f"{next[1]}"
                            embed = discord.Embed(title="Tocando agora", description=now_playing)
                            await command.channel.send(embed=embed)

                            voice.play(next[0], after=lambda e: call_next(e))
                        else:
                            await command.channel.send("Sem músicas na fila")

                    # iniciando fila de musica
                    if not voice.is_playing():
                        now_playing = f"{song_queue[0][1]}"
                        embed = discord.Embed(title="Tocando agora", description=now_playing)
                        await command.channel.send(embed=embed)
                        voice.play(song_queue[0][0], after=lambda e: call_next(e))
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
                    queue_list = ""
                    i = 0

                    for track in queue:
                        i += 1
                        queue_list += f"{i} - {track}\n"

                    embed = discord.Embed(title="Fila", description=queue_list)
                    embed.description = queue_list
                    await command.channel.send(embed=embed)
                elif command.guild.voice_client and queue <= 0:
                    await command.channel.send("Sem músicas na fila.")

            else:
                await command.channel.send("Este comando não existe.")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)