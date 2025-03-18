import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('APP_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')

if not TOKEN:
    raise ValueError("No se encontró el token del bot. Asegúrate de configurar APP_TOKEN en el archivo .env.")
