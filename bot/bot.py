import discord
from discord.ext import commands
from bot.commands.music_commands import MusicCommands
from bot.services.audio_source import AudioSource
from config.settings import TOKEN, PREFIX

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True

# Crear el bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Inicializar el servicio de audio
audio_source = AudioSource()

# Función asíncrona para configurar el bot
async def setup_bot():
    await bot.add_cog(MusicCommands(bot, audio_source))

# Función para ejecutar el bot
def run():
    bot.run(TOKEN)

# Configurar el bot antes de ejecutarlo
async def main():
    await setup_bot()
    await bot.start(TOKEN)  # Usar bot.start en lugar de bot.run

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
