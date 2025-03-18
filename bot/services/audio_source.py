import discord
import yt_dlp as youtube_dl
import asyncio

class AudioSource:
    def __init__(self):
        self.ytdl_format_options = {
            'format': 'bestaudio/best[ext=webm]',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'  # IPv4
        }
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -b:a 128k -bufsize 2048k -af volume=1.0'
        }
        self.ytdl = youtube_dl.YoutubeDL(self.ytdl_format_options)

    async def get_audio(self, url, stream=False):
        print(f"Obteniendo audio desde: {url}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: self.ytdl.extract_info(url, download=not stream)
        )
        print(f"Datos obtenidos: {data}")
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else self.ytdl.prepare_filename(data)
        return discord.FFmpegPCMAudio(filename, **self.ffmpeg_options), data

    async def search_audio(self, query):
        print(f"Buscando audio para: {query}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: self.ytdl.extract_info(f"ytsearch:{query}", download=False)
        )
        print(f"Datos obtenidos: {data}")
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url']
        return discord.FFmpegPCMAudio(filename, **self.ffmpeg_options), data
