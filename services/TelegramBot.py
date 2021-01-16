import telegram
from config.config import *


class TelegramBot:
    bot = None
    config = get_config()

    def __init__(self, settings):
        self.token = settings.get('token', None) or self.config['TG']['ACCESS_TOKEN_GYOABOT']
        self.set_bot(self.token)
        pass

    def set_bot(self, token):
        token = token or self.token
        self.bot = telegram.Bot(token=token)
        return self

    def get_bot(self):
        self.bot = telegram.Bot(token=self.token)
        return self.bot

    def send_message(self, chat_id, text):
        return self.bot.send_message(chat_id, text)

    def send_document(self, chat_id, file):
        return self.bot.send_document(chat_id, document=file)
