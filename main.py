import requests
import time
import datetime 
import json
import os
import telebot
import yfinance as yf
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get("API_KEY")
bot = telebot.TeleBot(API_KEY)

# endTime = datetime.datetime.now() + datetime.timedelta(minutes=3)
x = 0
old_id = 274727090

def welcome_msg(item):
    chat_id= item["message"]["chat"]["id"]
    user_id= item["message"]["new_chat_member"]["id"]
    user_name= item["message"]["new_chat_member"].get("username", user_id)

    welcome_msg = '''
                <a href="tg://user?id={}">@{}</a>, Welcome to Cryptoindex Group. Please read rules of the group and adhere to. Use /help to list all commands.
                '''.format(user_id, user_name)

    to_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=HTML'.format(API_KEY,chat_id, welcome_msg)
    resp = requests.get(to_url)

while x < 1: 
    time.sleep(5)
    base_url = 'https://api.telegram.org/bot{}/getUpdates'.format(API_KEY)
    resp = requests.get(base_url)
    data = resp.json()
    # print(data)
    for item in data["result"]:
        print(item["message"]["new_chat_participant"] is not None)
        # a = item["message"]
        # b = a if a["new_chat_participant"] is not None else a["left_chat_participant"] is not None
        # print(b, "ini pokoke bener dah")
        new_id = item["update_id"]
        if old_id < new_id:
            old_id = int(item["update_id"])
            try: 
                if "new_chat_member" in item ["message"]:
                    welcome_msg(item)
            except: 
                pass
        else: 
            @bot.message_handler(commands=['help', "Help"])
            def greet(message):
                bot.reply_to(message, "Here are some useful commands: \n1. /cryptoindex\n2. /cryptonium")

            @bot.message_handler(commands=['cryptoindex'])
            def hello(message):
                bot.send_message(message.chat.id, "Hello!")

            @bot.message_handler(commands=['wsb'])
            def get_stocks(message):
                response = ""
                stocks = ['gme', 'amc', 'nok']
                stock_data = []
                for stock in stocks:
                    data = yf.download(tickers=stock, period='2d', interval='1d')
                    data = data.reset_index()
                    response += f"-----{stock}-----\n"
                    stock_data.append([stock])
                    columns = ['stock']
                    for index, row in data.iterrows():
                        stock_position = len(stock_data) - 1
                        price = round(row['Close'], 2)
                        format_date = row['Date'].strftime('%m/%d')
                        response += f"{format_date}: {price}\n"
                        stock_data[stock_position].append(price)
                        columns.append(format_date)
                        print()

                response = f"{columns[0] : <10}{columns[1] : ^10}{columns[2] : >10}\n"
                for row in stock_data:
                    response += f"{row[0] : <10}{row[1] : ^10}{row[2] : >10}\n"
                response += "\nStock Data"
                print(response)
                bot.send_message(message.chat.id, response)

            def stock_request(message):
                request = message.text.split()
                if len(request) < 2 or request[0].lower() not in "price":
                    return False
                else:
                    return True

            @bot.message_handler(func=stock_request)
            def send_price(message):
                request = message.text.split()[1]
                data = yf.download(tickers=request, period='5m', interval='1m')
                if data.size > 0:
                    data = data.reset_index()
                    data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
                    data.set_index('format_date', inplace=True)
                    print(data.to_string())
                    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
                else:
                    bot.send_message(message.chat.id, "No data!?")

            bot.polling()

