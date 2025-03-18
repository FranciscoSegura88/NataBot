import discord
import yt_dlp as youtube_dl
import asyncio

class AudioSource:
    def __init__(self):
        self.ytdl_format_options = {
            'format': 'bestaudio/best[ext=webm]/best',
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
            'options': '-vn -b:a 128k -bufsize 256k'
        }
        self.ytdl = youtube_dl.YoutubeDL(self.ytdl_format_options)

    async def get_audio(self, url, stream=False):
        # Run ytdl extract_info in a thread pool since it's blocking
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: self.ytdl.extract_info(url, download=not stream)
        )

        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else self.ytdl.prepare_filename(data)
        return discord.FFmpegPCMAudio(filename, **self.ffmpeg_options), data

    async def search_audio(self, query):
        # Run ytdl extract_info in a thread pool since it's blocking
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: self.ytdl.extract_info(f"ytsearch:{query}", download=False)
        )

        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url']
        return discord.FFmpegPCMAudio(filename, **self.ffmpeg_options), data
