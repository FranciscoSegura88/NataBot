import discord
import asyncio
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

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error en el evento {event}: {args} {kwargs}")

@bot.event
async def on_ready():
    print(f'Bot está listo. Conectado como {bot.user}')
    print(f'Usando prefijo: {PREFIX}')

    # Registrar comandos una vez que el bot esté listo
    await bot.add_cog(MusicCommands(bot, audio_source))
    print("Comandos de música registrados")

# Función para ejecutar el bot
def run():
    discord.utils.setup_logging()
    bot.run(TOKEN)

if __name__ == '__main__':
    run()
