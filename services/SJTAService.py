import os
import time
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config.config import *
from helpers.Common import *
from services.TelegramBot import *


class SJTAService:
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
        self.log_path = dict_get(config, 'LOG.PATH', None)
        self.chrome_driver_path = dict_get(config, 'WEBDRIVER.CHROME_DRIVER_PATH', None)
        self.user_id = dict_get(config, 'TWID.ABBY_ID', None)
        self.tg = TelegramBot({})
        # self.chat_id = dict_get(config, 'TG.CHAT_ID_TEST', None)
        self.chat_id = dict_get(config, 'TG.CHAT_ID_RABBY', None)
        self.browser = self.get_browser()
        self.file_path = self.log_path + 'number.txt'

    def get_browser(self):
        options = ChromeOptions()
        if dict_get(self.settings, 'bg', None) is True:
            options.headless = True
        return webdriver.Chrome(self.chrome_driver_path, options=options)

    def close_windows(self):
        # 關閉所有視窗
        self.browser.close()

    def visit(self):
        login_url = 'http://118.163.223.157:8080/webrege/faces/webClinInfo.jsp'
        self.browser.get(login_url)

    def login(self):
        # 輸入 ID 後點擊送出表單
        self.browser.find_element_by_id('form1:qcid').send_keys(self.user_id)
        self.browser.find_element_by_id('form1:button1').click()

    def clean(self):
        self.browser.quit()
        self.reset()

    def fetch_current_number(self):
        number = '0'
        try:
            number = self.browser.find_element_by_id('table1_0_3_c').get_attribute('innerHTML')
            if len(number) == 0:
                number = '0'
        except Exception as e:
            print(e)
        finally:
            return number

    def query(self):
        try:
            self.visit()
            self.login()

            number = self.fetch_current_number().strip()
            last_number = self.fr()
            # print('123', 'number: ' + str(number), 'fs: ' + str(last_number))
            # exit()

            if number == last_number:
                msg = '[{}] same number: {} '.format(datetime.datetime.now(), number)
                print(msg)
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
