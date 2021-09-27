import requests
import time
import datetime 
import json
import os
import telebot
import yfinance as yf
from dotenv import load_dotenv
import urllib3
from flask import Flask, request
load_dotenv()

API_KEY = os.environ.get("API_KEY")
PORT = os.environ.get("PORT")
bot = telebot.TeleBot(API_KEY)
server = Flask(__name__)

@bot.message_handler(commands=['help', "Help", "start", "Start", "greet"])
def greet(message):
    bot.reply_to(message, "Here are some useful commands: \n1. /cryptoindex\n2. /cryptonium")

@bot.message_handler(commands=['cryptoindex'])
def cryptoindex(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    img = open('logo.png', 'rb')
    bot.send_photo(message.chat.id, img, reply_to_message_id=message.message_id)
    img.close()
    bot.send_message(message.chat.id, "Cryptoindex is a New Crypto Exchange Platform in the world. You can trade and invest crypto easily, securely, and convenient in this platform. Multiple crypto assets is available in this Exchange. Some of main crypto assets are Bitcoin, Ethereum, Binance Coin, and other crypto assets. Cryptoindex has built a world-class business that focuses on long-term client relationships, exceptional customer service and continuous innovation. For more information, please visit on https://cryptoindex.id/")


@bot.message_handler(commands=['cryptonium'])
def cryptoindex(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    img = open('logo2.png', 'rb')
    bot.send_photo(message.chat.id, img, reply_to_message_id=message.message_id)
    img.close()
    bot.send_message(message.chat.id, "Cryptonium is a gateway and bridge to the investment community and ecosystem of the cryptoindex platform. present as a token that has a value that continues to grow in accordance with the growth and development of the ecosystem. For more information, please visit on https://cryptonium.digital")

@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    if message.chat.type == "group":
        if('@crypto_index1_bot' in message.text):
            bot.reply_to(message, "Please use /help to see all the commands")

# while True: 
#     try:
#         bot.polling(none_stop=True)
#     except Exception:
#         time.sleep(15)

@server.route('/' + API_KEY, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook(): 
    bot.remove_webhook()
    bot.set_webhook(url='https://cryptoindex-telebot.herokuapp.com/' + API_KEY)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(PORT))
