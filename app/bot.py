import telebot
import logging

# from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from utils import getToken
from vars import START_MESSAGE

def createBot():
    TOKEN = getToken()

    bot = telebot.TeleBot(token=TOKEN)
    telebot.logger.setLevel(logging.DEBUG)

    @bot.message_handler(commands=['start', 'help'])
    def _start(message):
        bot.send_message(message.chat.id, text=START_MESSAGE)
        # bot.send_message(message.chat.id, text, reply_markup=createMarkup())

    return bot

if __name__ == "__main__":
    bot = createBot()