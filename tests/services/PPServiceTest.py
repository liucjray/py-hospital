import unittest
from services.PPService import *


class PPServiceTest(unittest.TestCase):
    def setUp(self):
        self.pp = PPService()

    def test_login(self):
        self.pp.visit()
        self.pp.login()

    def test_goto_member(self):
        self.test_login()
        self.pp.goto_member()
        self.pp.goto_last_article()
        html = self.pp.get_article_content()
        self.pp.fw(html)
        doc = open(self.pp.file_path, 'rb')
        self.pp.send_document(doc)

    def test_bot_send_doc(self):
        doc = open(self.pp.file_path, 'rb')
        self.pp.send_document(doc)
