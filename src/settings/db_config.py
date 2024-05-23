import os

from dotenv import load_dotenv

load_dotenv()

token = os.environ.get('TOKEN')
name = "Taxi Delta Bot"

host = os.environ.get('HOST')
port = int(os.environ.get('PORT'))
user = os.environ.get('USER')
password = os.environ.get('PASS')
db_name = os.environ.get('DB_NAME')

chat_id = os.environ.get('CHAT_ID')
