import unittest
from helpers.Common import *
from services.TelegramBot import *


class TelegramTest(unittest.TestCase):
    def setUp(self):
        self.tg = TelegramBot({})
        self.config = dict(self.tg.config)
        self.bot = self.tg.get_bot()

    def test_send_message(self):
        chat_id_alias = 'TG.CHAT_ID_TEST'
        chat_id = dict_get(self.config, chat_id_alias)
        a = self.bot.send_message(chat_id, 'test')
        self.assertIs(telegram.message.Message, type(a))
