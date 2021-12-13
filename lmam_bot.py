import os
import telebot
from telebot.types import Message
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot('5004963820:AAEKRFFX-H7hj8Nz9MM4HQROlPhfqshHAt8')

def sendmessage(chat_id,msg):
    bot.send_message(chat_id, msg)

