from discord.ext import commands
from bot.services.audio_source import AudioSource

class MusicCommands(commands.Cog):
    def __init__(self, bot, audio_source):
        self.bot = bot
        self.audio_source = audio_source

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
            await voice_client.disconnect()
        else:
            await ctx.send("El bot no está conectado a un canal de voz.")

    @commands.command(name='play', help='Reproduce una canción desde YouTube')
    async def play(self, ctx, *, query: str):
        async with ctx.typing():
            player, data = await self.audio_source.get_audio(query, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Error:', e) if e else None)
        await ctx.send(f'Ahora reproduciendo: {data["title"]}')
