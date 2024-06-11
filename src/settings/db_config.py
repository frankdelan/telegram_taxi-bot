import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN')
API_KEY = os.environ.get('API_KEY')
name = "Taxi Delta Bot"

HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASS')
NAME = os.environ.get('DB_NAME')

chat_id = os.environ.get('CHAT_ID')
