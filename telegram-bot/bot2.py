import logging
import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram

load_dotenv()


API_KEY = os.environ.get("API_KEY")
PORT = os.environ.get("PORT")
PHOTO_PATH = "./logo.png"
PHOTO_PATH2 = "./logo2.png"
bot = telegram.Bot(API_KEY)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help(update, context):
    update.message.reply_text("Here are some useful commands: \n1. /cryptoindex\n2. /cryptonium")

def cryptoindex(update, context):
    update.send_photo()
    update.message.reply_text('Cryptoindex is a New Crypto Exchange Platform in the world. You can trade and invest crypto easily, securely, and convenient in this platform. Multiple crypto assets is available in this Exchange. Some of main crypto assets are Bitcoin, Ethereum, Binance Coin, and other crypto assets. Cryptoindex has built a world-class business that focuses on long-term client relationships, exceptional customer service and continuous innovation. For more information, please visit on https://cryptoindex.id/')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("cryptoindex", cryptoindex))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
