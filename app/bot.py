import pendulum
import requests
import telebot
import logging

# from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from utils import getToken, loadSecrets
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

class TelebotHelper:
    def __init__(self):
        self.token = getToken()
        if self.token is None:
            raise Exception('Invalid Telebot Token')
        self.configVars = loadSecrets()
        

    def callTelegramAPI(self, method, params):
        url = 'https://api.telegram.org/bot{}/{}'.format(self.token, method)
        response = requests.post(url=url, params=params)
        # print(response.json())
        return response.json()

    def sendMessage(self, appName, logs, timeStamp):
        formattedTime = pendulum.from_timestamp(timeStamp, tz='Asia/Singapore').format('DD-MMM-YYYY HH:mm:ss')
        method = 'sendMessage'
        responses = {}
        for chatId in self.configVars['Telegram']['Admins']:
            params = {
                'chat_id': chatId,
                'parse_mode': 'HTML',
                'text': f'<i>[{formattedTime}]</i> <b>{appName}</b>\n{logs}'
            }
            response = self.callTelegramAPI(method, params)
            ### Convert chatId to username ###
            responses[chatId] = response
        return responses

if __name__ == "__main__":
    bot = createBot()