import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from nerodia.browser import Browser

from config.config import *
from helpers.Common import *
from services.TelegramBot import *


class PPService:
    def __init__(self, settings=None):
        self.settings = settings
        self.reset()
        self.init_file()

    def init_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                f.write('')

    def reset(self):
        config = dict(get_config())
        self.chrome_driver_path = dict_get(config, 'WEBDRIVER.CHROME_DRIVER_PATH', None)
        self.user_id = dict_get(config, 'TWID.ABBY_ID', None)
        self.tg = TelegramBot({})
        # self.chat_id = dict_get(config, 'TG.CHAT_ID_TEST', None)
        self.chat_id = dict_get(config, 'TG.CHAT_ID_STR', None)
        self.browser = self.get_browser()

        self.log_path = dict_get(config, 'LOG.PATH', None)
        self.file_path = self.log_path + 'last_article.html'

    def get_browser(self):
        chrome_options = ChromeOptions()
        if dict_get(self.settings, 'bg', None) is True:
            chrome_options.headless = True
        bw = Browser(executable_path=os.path.abspath(self.chrome_driver_path), options=chrome_options)
        # bw.window().maximize()
        return bw

    def close_windows(self):
        # 關閉所有視窗
        self.browser.close()

    def visit(self):
        login_url = 'https://www.pressplay.cc/'
        self.browser.goto(login_url)

    def wait_and_click(self, htmlelemnt):
        htmlelemnt.wait_for_present()
        htmlelemnt.click()

    def login(self):
        # 輸入 ID 後點擊送出表單
        # self.browser.find_element_by_link_text('登入').click()
        a = self.browser.element(xpath='//div[@id="login-menu"]/ul/li[2]/a')
        self.wait_and_click(a)

        email = self.browser.element(xpath='//input[@id="email"]')
        self.wait_and_click(email)
        email.send_keys('side0806@gmail.com')

        password = self.browser.element(xpath='//input[@id="password"]')
        password.send_keys('1234qwer')

        login_button = self.browser.element(xpath='//button[@id="login-button"]')
        login_button.click()

    def goto_member(self):
        notification_nav = self.browser.element(xpath='//div[@class="member-page"]')
        notification_nav.wait_for_present()
        self.browser.goto('https://www.pressplay.cc/member')

    def goto_last_article(self):
        last_article = self.browser.element(xpath='//a[@class="u-decorationNone link--secondary"]')
        last_article.wait_for_present()
        self.wait_and_click(last_article)

    def get_article_content(self):
        last_article = self.browser.element(xpath='//div[@class="article-content-box-wrap"]')
        last_article.wait_for_present()
        return self.get_html_content()

    def get_html_content(self):
        html = self.browser.element(tag_name='html').inner_html
        return html

    def send_document(self, file):
        self.tg.send_document(self.chat_id, file)

    def clean(self):
        self.browser.quit()
        self.reset()

    def query(self):
        try:
            self.visit()
            self.login()

            number = self.fetch_current_number().strip()
            last_number = self.fr()
            # print('123', 'number: ' + str(number), 'fs: ' + str(last_number))
            # exit()

            if number == last_number:
                print('same number')
            else:
                self.fw(number)
                self.tg.send_message(self.chat_id, '目前看診號碼: ' + number)

        except Exception as e:
            self.clean()
            print(e)

        finally:
            self.close_windows()
            self.clean()

    def fw(self, content):
        self.init_file()
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def fr(self):
        self.init_file()
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
