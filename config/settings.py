import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('APP_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')
