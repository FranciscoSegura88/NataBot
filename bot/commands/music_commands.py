import asyncio
from discord.ext import commands
from bot.services.audio_source import AudioSource
from bot.services.queue_manager import QueueManager

class MusicCommands(commands.Cog):
    def __init__(self, bot, audio_source):
        self.bot = bot
        self.audio_source = audio_source
        self.queue_manager = QueueManager()

    @commands.command(name='join', help='Hace que el bot se una a tu canal de voz')
    async def join(self, ctx):
        if not ctx.author.voice:
            await ctx.send(f"{ctx.author.name} no estás en un canal de voz.")
            return
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(name='leave', help='Hace que el bot abandone el canal de voz')
    async def leave(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_connected():
            self.queue_manager.clear_queue()
            await voice_client.disconnect()
        else:
            await ctx.send("El bot no está conectado a un canal de voz.")

    @commands.command(name='play', help='Reproduce una canción desde YouTube')
    async def play(self, ctx, *, query: str):
        async with ctx.typing():
            # Si es una URL, reproducir directamente
            if query.startswith('http'):
                player, data = await self.audio_source.get_audio(query, stream=True)
                self.queue_manager.add_to_queue({'player': player, 'data': data})
            else:
                # Buscar en YouTube
                player, data = await self.audio_source.search_audio(query)
                self.queue_manager.add_to_queue({'player': player, 'data': data})

            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)

        await ctx.send(f'Añadido a la cola: {data["title"]}')

    async def play_next(self, ctx):
        if self.queue_manager.queue:
            next_song = self.queue_manager.get_next_song()
            ctx.voice_client.play(next_song['player'], after=lambda e: self.after_play(ctx, e))
            await ctx.send(f'Ahora reproduciendo: {next_song["data"]["title"]}')
        else:
            await ctx.send("La cola de reproducción está vacía.")

    def after_play(self, ctx, error):
        if error:
            print(f'Error: {error}')
        asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)

    @commands.command(name='skip', help='Salta la canción actual')
    async def skip(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Canción saltada.")
        else:
            await ctx.send("No se está reproduciendo nada.")

    @commands.command(name='queue', help='Muestra la cola de reproducción')
    async def queue(self, ctx):
        if self.queue_manager.queue:
            queue_list = "\n".join([f"{i+1}. {song['data']['title']}" for i, song in enumerate(self.queue_manager.queue)])
            await ctx.send(f"**Cola de reproducción:**\n{queue_list}")
        else:
            await ctx.send("La cola de reproducción está vacía.")

    @commands.command(name='volume', help='Ajusta el volumen (0-100)')
    async def volume(self, ctx, volume: int):
        if 0 <= volume <= 100:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"Volumen ajustado a {volume}%.")
        else:
            await ctx.send("El volumen debe estar entre 0 y 100.")
