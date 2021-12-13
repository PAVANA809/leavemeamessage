import os
import telebot
# from telegram import ParseMode
from telebot.types import Message
from dotenv import load_dotenv
from app import send
import crud

load_dotenv()
API_KEY = os.getenv('API_KEY')
host_id = "192.168.1.101"

bot = telebot.TeleBot('5004963820:AAEKRFFX-H7hj8Nz9MM4HQROlPhfqshHAt8')


@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, "It is our great pleasure to have you on board! A hearty welcome to you!")
    bot.send_message(
        message.chat.id, text=str("<b>Enter your username and secrete key used to create account on <a href='https://leavemeamessage.herokuapp.com/'>Leavemeamessage</a> website in the format</b>"), parse_mode='HTML')
    bot.send_message(message.chat.id,"uname xxxxxx skey xxxxx")


@bot.message_handler(commands=['Hello', 'hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello!")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    msg = message.text.split()
    if len(msg) != 4:
        bot.send_message(message.chat.id, "Format Incorrect")
        return
    if msg[0] == "uname":
        x = crud.lmam["Users"].count_documents({"Uname":msg[1]})
        if x == 0:
            bot.send_message(message.chat.id,"Username not found")
            return
        else:
            bot.send_message(message.chat.id, "We found your username")
            y = crud.lmam["Users"].find({"Uname":msg[1]},{"Skey":1,"_id":0})
            for i in y:
                skey = i
            if skey["Skey"] == msg[3]:
                crud.lmam["Users"].update_one({"Uname": msg[1]}, {"$set": {"chat_id": message.chat.id}})
                bot.send_message(message.chat.id, "Chat id updated successfully")
                bot.send_message(message.chat.id, "Your are now ready to receive anonymous messages")
                return
            else:
                bot.send_message(message.chat.id,"Secrete key doesn't match")
                return
    else:
        bot.send_message(message.chat.id,"Format Incorrect")
    return


def response(input_text):
    user_message = str(input_text).lower()
    if user_message in ('hello', 'hi', 'sum', 'hai'):
        return "Hey! Hows is it going?"

    if user_message in ('who are you', 'who are you?', 'who is it?', 'who is it'):
        return "I am a bot!"

    return "I dont understand you!"


bot.polling()
