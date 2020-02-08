import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from config.config import *
from helpers.Common import *
from services.TelegramBot import *


class SJTAService:
    def __init__(self, settings=None):
        self.settings = settings
        self.reset()

    def reset(self):
        config = dict(get_config())
        self.log_path = dict_get(config, 'LOG.PATH', None)
        self.chrome_driver_path = dict_get(config, 'WEBDRIVER.CHROME_DRIVER_PATH', None)
        self.user_id = dict_get(config, 'TWID.ABBY_ID', None)
        self.tg = TelegramBot({})
        self.chat_id = dict_get(config, 'TG.CHAT_ID_RABBY', None)
        self.browser = self.get_browser()

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
        number = self.browser.find_element_by_id('table1_0_3_c').get_attribute('innerHTML')
        return number

    def register(self):
        try:
            self.visit()
            self.login()
            number = self.fetch_current_number()

            f = open(self.log_path + 'number.txt', 'r')
            if str(number) == str(f.read()):
                f.close()
                print('same number')
            else:
                f.close()
                f = open(self.log_path + 'number.txt', 'w')
                f.write(number)
                self.tg.send_message(self.chat_id, '目前看診號碼: ' + number)

        except Exception as e:
            self.clean()
            print(e)

        finally:
            self.close_windows()
            self.clean()
